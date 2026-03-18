from __future__ import annotations

from dataclasses import dataclass

from exec_trace.dsl import ExecutionResult, Opcode

from .ir import BytecodeOpcode, BytecodeProgram
from .types import BytecodeMemoryCell, BytecodeMemoryRegion, BytecodeType
from .verifier import ControlFrame


@dataclass(frozen=True, slots=True)
class AbstractStackValue:
    value_type: BytecodeType
    addresses: frozenset[int] = frozenset()


@dataclass(frozen=True, slots=True)
class MemorySurfaceVerificationResult:
    program_name: str
    passed: bool
    first_error_pc: int | None
    error_class: str | None
    message: str
    reachable_frame_addresses: tuple[int, ...]
    reachable_heap_addresses: tuple[int, ...]
    max_call_depth: int


@dataclass(frozen=True, slots=True)
class MemoryAccessRecord:
    step: int
    pc: int
    opcode: str
    access_kind: str
    address: int
    region: str
    label: str
    alias_group: str | None
    call_depth: int


@dataclass(frozen=True, slots=True)
class MemoryBoundarySnapshot:
    step: int
    pc: int
    opcode: str
    call_depth_before: int
    call_depth_after: int
    stack_before: tuple[int, ...]
    stack_after: tuple[int, ...]
    frame_memory: tuple[tuple[int, int], ...]
    heap_memory: tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class MemorySurfaceReport:
    program_name: str
    declared_frame_addresses: tuple[int, ...]
    declared_heap_addresses: tuple[int, ...]
    touched_frame_addresses: tuple[int, ...]
    touched_heap_addresses: tuple[int, ...]
    undeclared_addresses: tuple[int, ...]
    max_call_depth: int
    accesses: tuple[MemoryAccessRecord, ...]
    boundary_snapshots: tuple[MemoryBoundarySnapshot, ...]
    final_frame_memory: tuple[tuple[int, int], ...]
    final_heap_memory: tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class MemorySurfaceHarnessRow:
    program_name: str
    suite: str
    comparison_mode: str
    base_trace_match: bool
    base_final_state_match: bool
    memory_surface_verifier_passed: bool
    memory_surface_error_class: str | None
    memory_surface_match: bool
    boundary_snapshot_count: int
    max_call_depth: int
    undeclared_address_count: int
    touched_frame_addresses: tuple[int, ...]
    touched_heap_addresses: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class _ControlState:
    pc: int
    frames: tuple[ControlFrame, ...] = ()


@dataclass(frozen=True, slots=True)
class _AnalysisFacts:
    stack: tuple[AbstractStackValue, ...]
    addr_cells: tuple[tuple[int, frozenset[int]], ...]

    @property
    def addr_cell_map(self) -> dict[int, frozenset[int]]:
        return {address: values for address, values in self.addr_cells}


def _layout_map(program: BytecodeProgram) -> dict[int, BytecodeMemoryCell]:
    return program.memory_layout_map


def _make_result(
    program: BytecodeProgram,
    *,
    passed: bool,
    first_error_pc: int | None,
    error_class: str | None,
    message: str,
    reachable_addresses: set[int],
    max_call_depth: int,
) -> MemorySurfaceVerificationResult:
    layout = _layout_map(program)
    reachable_frame = sorted(
        address
        for address in reachable_addresses
        if address in layout and layout[address].region == BytecodeMemoryRegion.FRAME
    )
    reachable_heap = sorted(
        address
        for address in reachable_addresses
        if address in layout and layout[address].region == BytecodeMemoryRegion.HEAP
    )
    return MemorySurfaceVerificationResult(
        program_name=program.name,
        passed=passed,
        first_error_pc=first_error_pc,
        error_class=error_class,
        message=message,
        reachable_frame_addresses=tuple(reachable_frame),
        reachable_heap_addresses=tuple(reachable_heap),
        max_call_depth=max_call_depth,
    )


def _fail(
    program: BytecodeProgram,
    *,
    pc: int | None,
    error_class: str,
    message: str,
    reachable_addresses: set[int],
    max_call_depth: int,
) -> MemorySurfaceVerificationResult:
    return _make_result(
        program,
        passed=False,
        first_error_pc=pc,
        error_class=error_class,
        message=message,
        reachable_addresses=reachable_addresses,
        max_call_depth=max_call_depth,
    )


def _validate_layout(program: BytecodeProgram) -> MemorySurfaceVerificationResult | None:
    if not program.memory_layout:
        return _fail(
            program,
            pc=0 if program.instructions else None,
            error_class="missing_layout",
            message="memory-surface analysis requires a declared memory layout.",
            reachable_addresses=set(),
            max_call_depth=0,
        )

    seen: set[int] = set()
    layout = _layout_map(program)
    for cell in program.memory_layout:
        if cell.address < 0:
            return _fail(
                program,
                pc=0,
                error_class="negative_layout_address",
                message=f"memory-layout address {cell.address} must be non-negative.",
                reachable_addresses=set(),
                max_call_depth=0,
            )
        if cell.address in seen:
            return _fail(
                program,
                pc=0,
                error_class="duplicate_layout_address",
                message=f"memory-layout address {cell.address} was declared more than once.",
                reachable_addresses=set(),
                max_call_depth=0,
            )
        seen.add(cell.address)

    for cell in program.memory_layout:
        if cell.allowed_targets and cell.cell_type != BytecodeType.ADDR:
            return _fail(
                program,
                pc=0,
                error_class="non_addr_targets",
                message=f"only addr cells may declare allowed_targets; got {cell.label!r}.",
                reachable_addresses=set(),
                max_call_depth=0,
            )
        for target in cell.allowed_targets:
            if target not in layout:
                return _fail(
                    program,
                    pc=0,
                    error_class="unknown_allowed_target",
                    message=f"layout target {target} for cell {cell.label!r} is undeclared.",
                    reachable_addresses=set(),
                    max_call_depth=0,
                )
    return None


def _abstract_value(value_type: BytecodeType, *, addresses: set[int] | frozenset[int] | None = None) -> AbstractStackValue:
    addr_values = frozenset() if addresses is None else frozenset(addresses)
    if value_type != BytecodeType.ADDR:
        addr_values = frozenset()
    return AbstractStackValue(value_type=value_type, addresses=addr_values)


def _merge_value(previous: AbstractStackValue, current: AbstractStackValue) -> AbstractStackValue | None:
    if previous.value_type != current.value_type:
        return None
    if previous.value_type != BytecodeType.ADDR:
        return previous
    return _abstract_value(BytecodeType.ADDR, addresses=previous.addresses | current.addresses)


def _merge_facts(previous: _AnalysisFacts, current: _AnalysisFacts) -> _AnalysisFacts | None:
    if len(previous.stack) != len(current.stack):
        return None

    merged_stack: list[AbstractStackValue] = []
    for previous_value, current_value in zip(previous.stack, current.stack, strict=True):
        merged_value = _merge_value(previous_value, current_value)
        if merged_value is None:
            return None
        merged_stack.append(merged_value)

    previous_cells = previous.addr_cell_map
    current_cells = current.addr_cell_map
    if tuple(sorted(previous_cells)) != tuple(sorted(current_cells)):
        return None
    merged_cells = tuple(
        (address, previous_cells[address] | current_cells[address])
        for address in sorted(previous_cells)
    )
    return _AnalysisFacts(stack=tuple(merged_stack), addr_cells=merged_cells)


def _initial_facts(program: BytecodeProgram) -> _AnalysisFacts:
    addr_cells = tuple(
        (cell.address, frozenset(cell.allowed_targets))
        for cell in sorted(program.memory_layout, key=lambda item: item.address)
        if cell.cell_type == BytecodeType.ADDR
    )
    return _AnalysisFacts(stack=(), addr_cells=addr_cells)


def verify_memory_surfaces(program: BytecodeProgram) -> MemorySurfaceVerificationResult:
    layout_error = _validate_layout(program)
    if layout_error is not None:
        return layout_error

    layout = _layout_map(program)
    incoming: dict[_ControlState, _AnalysisFacts] = {_ControlState(0): _initial_facts(program)}
    worklist: list[_ControlState] = [_ControlState(0)]
    reachable_addresses: set[int] = set()
    halted_reachable = False
    max_call_depth = 0

    while worklist:
        state = min(
            worklist,
            key=lambda item: (item.pc, tuple((frame.return_pc, frame.call_target) for frame in item.frames)),
        )
        worklist.remove(state)
        facts = incoming[state]
        stack = list(facts.stack)
        addr_cells = facts.addr_cell_map
        next_addr_cells = dict(addr_cells)
        max_call_depth = max(max_call_depth, len(state.frames))

        if not (0 <= state.pc < len(program.instructions)):
            return _fail(
                program,
                pc=state.pc,
                error_class="pc_out_of_range",
                message="memory-surface verifier reached an out-of-range pc.",
                reachable_addresses=reachable_addresses,
                max_call_depth=max_call_depth,
            )

        instruction = program.instructions[state.pc]
        opcode = instruction.opcode
        next_pc = state.pc + 1
        transitions: list[tuple[_ControlState, _AnalysisFacts]] = []

        def pop_exact(expected: tuple[BytecodeType, ...]) -> list[AbstractStackValue] | None:
            if len(stack) < len(expected):
                return None
            values = stack[-len(expected) :] if expected else []
            if expected and tuple(value.value_type for value in values) != expected:
                return None
            del stack[len(stack) - len(expected) :]
            return list(values)

        def transition_to(pc: int, *, frames: tuple[ControlFrame, ...] | None = None) -> None:
            target_frames = state.frames if frames is None else frames
            target_facts = _AnalysisFacts(
                stack=tuple(stack),
                addr_cells=tuple((address, next_addr_cells[address]) for address in sorted(next_addr_cells)),
            )
            transitions.append((_ControlState(pc, target_frames), target_facts))

        if opcode in {BytecodeOpcode.CONST_I32, BytecodeOpcode.CONST_ADDR} and instruction.arg is None:
            return _fail(
                program,
                pc=state.pc,
                error_class="missing_arg",
                message=f"{opcode.value} requires an integer argument.",
                reachable_addresses=reachable_addresses,
                max_call_depth=max_call_depth,
            )

        match opcode:
            case BytecodeOpcode.CONST_I32:
                stack.append(_abstract_value(BytecodeType.I32))
                transition_to(next_pc)
            case BytecodeOpcode.CONST_ADDR:
                if instruction.arg not in layout:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="undeclared_address_literal",
                        message=f"const_addr target {instruction.arg} is not declared in the memory layout.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                reachable_addresses.add(int(instruction.arg))
                stack.append(_abstract_value(BytecodeType.ADDR, addresses={int(instruction.arg)}))
                transition_to(next_pc)
            case BytecodeOpcode.DUP:
                if not stack:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="stack_underflow",
                        message="dup requires one stack value.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                stack.append(stack[-1])
                transition_to(next_pc)
            case BytecodeOpcode.POP:
                if not stack:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="stack_underflow",
                        message="pop requires one stack value.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                stack.pop()
                transition_to(next_pc)
            case BytecodeOpcode.ADD_I32 | BytecodeOpcode.SUB_I32:
                if pop_exact((BytecodeType.I32, BytecodeType.I32)) is None:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="type_mismatch",
                        message=f"{opcode.value} expects i32, i32.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                stack.append(_abstract_value(BytecodeType.I32))
                transition_to(next_pc)
            case BytecodeOpcode.EQ_I32:
                if pop_exact((BytecodeType.I32, BytecodeType.I32)) is None:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="type_mismatch",
                        message="eq_i32 expects i32, i32.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                stack.append(_abstract_value(BytecodeType.FLAG))
                transition_to(next_pc)
            case BytecodeOpcode.LOAD_STATIC:
                if instruction.arg not in layout:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="undeclared_static_address",
                        message=f"load_static address {instruction.arg} is not declared in the memory layout.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                cell = layout[int(instruction.arg)]
                expected_type = instruction.out_types[0] if instruction.out_types else cell.cell_type
                if cell.cell_type != expected_type:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="layout_type_mismatch",
                        message=f"load_static address {instruction.arg} expects layout type {cell.cell_type.value}, got {expected_type.value}.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                if cell.cell_type == BytecodeType.ADDR:
                    addresses = next_addr_cells.get(cell.address, frozenset(cell.allowed_targets))
                    if not addresses:
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="addr_cell_unbound",
                            message=f"addr cell {cell.label!r} has no reachable targets.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                    reachable_addresses.update(addresses)
                    stack.append(_abstract_value(BytecodeType.ADDR, addresses=addresses))
                else:
                    stack.append(_abstract_value(cell.cell_type))
                transition_to(next_pc)
            case BytecodeOpcode.STORE_STATIC:
                if instruction.arg not in layout:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="undeclared_static_address",
                        message=f"store_static address {instruction.arg} is not declared in the memory layout.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                values = pop_exact(instruction.in_types)
                if values is None:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="type_mismatch",
                        message=f"store_static expects {', '.join(item.value for item in instruction.in_types)}.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                cell = layout[int(instruction.arg)]
                if cell.cell_type != values[0].value_type:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="layout_type_mismatch",
                        message=f"store_static address {instruction.arg} expects layout type {cell.cell_type.value}.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                if cell.cell_type == BytecodeType.ADDR:
                    allowed_targets = set(cell.allowed_targets) if cell.allowed_targets else set(layout)
                    if not values[0].addresses:
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="unknown_addr_value",
                            message=f"store_static into addr cell {cell.label!r} requires known targets.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                    if not values[0].addresses.issubset(allowed_targets):
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="address_escape",
                            message=f"addr cell {cell.label!r} received a target outside its declared surface.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                    next_addr_cells[cell.address] = values[0].addresses
                    reachable_addresses.update(values[0].addresses)
                transition_to(next_pc)
            case BytecodeOpcode.LOAD_INDIRECT:
                values = pop_exact((BytecodeType.ADDR,))
                if values is None:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="type_mismatch",
                        message="load_indirect expects addr.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                targets = set(values[0].addresses)
                if not targets:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="unknown_indirect_target",
                        message="load_indirect requires a known reachable target set.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                for target in targets:
                    if target not in layout:
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="indirect_target_undeclared",
                            message=f"load_indirect target {target} is not declared in the memory layout.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                    if layout[target].cell_type != BytecodeType.I32:
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="indirect_type_mismatch",
                            message=f"load_indirect target {target} is typed {layout[target].cell_type.value}, not i32.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                reachable_addresses.update(targets)
                stack.append(_abstract_value(BytecodeType.I32))
                transition_to(next_pc)
            case BytecodeOpcode.STORE_INDIRECT:
                values = pop_exact((BytecodeType.I32, BytecodeType.ADDR))
                if values is None:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="type_mismatch",
                        message="store_indirect expects i32, addr.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                targets = set(values[1].addresses)
                if not targets:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="unknown_indirect_target",
                        message="store_indirect requires a known reachable target set.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                for target in targets:
                    if target not in layout:
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="indirect_target_undeclared",
                            message=f"store_indirect target {target} is not declared in the memory layout.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                    if layout[target].cell_type != values[0].value_type:
                        return _fail(
                            program,
                            pc=state.pc,
                            error_class="indirect_type_mismatch",
                            message=f"store_indirect target {target} is typed {layout[target].cell_type.value}, not {values[0].value_type.value}.",
                            reachable_addresses=reachable_addresses,
                            max_call_depth=max_call_depth,
                        )
                reachable_addresses.update(targets)
                transition_to(next_pc)
            case BytecodeOpcode.JMP:
                if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="branch_target",
                        message="jmp target must stay within program bounds.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                transition_to(int(instruction.arg))
            case BytecodeOpcode.JZ_ZERO:
                if pop_exact(instruction.in_types) is None:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="type_mismatch",
                        message=f"jz_zero expects {', '.join(item.value for item in instruction.in_types)}.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="branch_target",
                        message="jz_zero target must stay within program bounds.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                transition_to(next_pc)
                transition_to(int(instruction.arg))
            case BytecodeOpcode.CALL:
                if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="call_target",
                        message="call target must stay within program bounds.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                active_targets = {frame.call_target for frame in state.frames}
                if instruction.arg in active_targets:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="recursive_call",
                        message="recursive or mutually recursive call cycles are out of scope.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                next_frames = state.frames + (ControlFrame(return_pc=next_pc, call_target=int(instruction.arg)),)
                max_call_depth = max(max_call_depth, len(next_frames))
                transition_to(int(instruction.arg), frames=next_frames)
            case BytecodeOpcode.RET:
                if not state.frames:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="empty_return",
                        message="ret requires one pending call frame.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                transition_to(state.frames[-1].return_pc, frames=state.frames[:-1])
            case BytecodeOpcode.HALT:
                if state.frames:
                    return _fail(
                        program,
                        pc=state.pc,
                        error_class="unterminated_frame",
                        message="halt is only valid when the call stack is empty.",
                        reachable_addresses=reachable_addresses,
                        max_call_depth=max_call_depth,
                    )
                halted_reachable = True
            case _:
                return _fail(
                    program,
                    pc=state.pc,
                    error_class="unsupported_opcode",
                    message=f"unsupported opcode {opcode.value!r} in memory-surface verifier.",
                    reachable_addresses=reachable_addresses,
                    max_call_depth=max_call_depth,
                )

        for target_state, target_facts in transitions:
            previous = incoming.get(target_state)
            if previous is None:
                incoming[target_state] = target_facts
                worklist.append(target_state)
                continue
            merged = _merge_facts(previous, target_facts)
            if merged is None:
                return _fail(
                    program,
                    pc=target_state.pc,
                    error_class="abstract_join_mismatch",
                    message="memory-surface join requires one consistent stack and alias shape.",
                    reachable_addresses=reachable_addresses,
                    max_call_depth=max_call_depth,
                )
            if merged != previous:
                incoming[target_state] = merged
                worklist.append(target_state)

    if not halted_reachable:
        return _make_result(
            program,
            passed=False,
            first_error_pc=None,
            error_class="no_halt",
            message="memory-surface verifier found no reachable halt.",
            reachable_addresses=reachable_addresses,
            max_call_depth=max_call_depth,
        )

    return _make_result(
        program,
        passed=True,
        first_error_pc=None,
        error_class=None,
        message="ok",
        reachable_addresses=reachable_addresses,
        max_call_depth=max_call_depth,
    )


def _region_snapshot(
    layout: dict[int, BytecodeMemoryCell],
    memory: dict[int, int],
    region: BytecodeMemoryRegion,
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (address, memory.get(address, 0))
        for address in sorted(layout)
        if layout[address].region == region
    )


def analyze_memory_surfaces(program: BytecodeProgram, execution: ExecutionResult) -> MemorySurfaceReport:
    layout = _layout_map(program)
    stack: list[int] = []
    memory: dict[int, int] = {}
    call_depth = 0
    max_call_depth = 0
    touched_frame: set[int] = set()
    touched_heap: set[int] = set()
    undeclared: set[int] = set()
    accesses: list[MemoryAccessRecord] = []
    boundary_snapshots: list[MemoryBoundarySnapshot] = []

    for event in execution.events:
        stack_before = tuple(stack)
        if event.popped:
            observed = tuple(stack[-len(event.popped) :])
            if observed != event.popped:
                raise RuntimeError(
                    f"stack replay mismatch while building memory surfaces for {program.name!r}: "
                    f"{observed} != {event.popped}"
                )
            del stack[-len(event.popped) :]
        stack.extend(event.pushed)
        stack_after = tuple(stack)

        call_depth_before = call_depth
        if event.opcode == Opcode.CALL:
            call_depth += 1
        elif event.opcode == Opcode.RET:
            call_depth = max(0, call_depth - 1)
        max_call_depth = max(max_call_depth, call_depth_before, call_depth)

        for access_kind, address in (
            ("read", event.memory_read_address),
            ("write", None if event.memory_write is None else event.memory_write[0]),
        ):
            if address is None:
                continue
            cell = layout.get(address)
            if cell is None:
                undeclared.add(address)
                region = "undeclared"
                label = "undeclared"
                alias_group = None
            else:
                region = cell.region.value
                label = cell.label
                alias_group = cell.alias_group
                if cell.region == BytecodeMemoryRegion.FRAME:
                    touched_frame.add(address)
                else:
                    touched_heap.add(address)
            accesses.append(
                MemoryAccessRecord(
                    step=event.step,
                    pc=event.pc,
                    opcode=event.opcode.value,
                    access_kind=access_kind,
                    address=address,
                    region=region,
                    label=label,
                    alias_group=alias_group,
                    call_depth=call_depth_before,
                )
            )

        if event.memory_write is not None:
            address, value = event.memory_write
            memory[address] = value

        if event.opcode in {Opcode.CALL, Opcode.RET}:
            boundary_snapshots.append(
                MemoryBoundarySnapshot(
                    step=event.step,
                    pc=event.pc,
                    opcode=event.opcode.value,
                    call_depth_before=call_depth_before,
                    call_depth_after=call_depth,
                    stack_before=stack_before,
                    stack_after=stack_after,
                    frame_memory=_region_snapshot(layout, memory, BytecodeMemoryRegion.FRAME),
                    heap_memory=_region_snapshot(layout, memory, BytecodeMemoryRegion.HEAP),
                )
            )

    declared_frame = tuple(
        address
        for address in sorted(layout)
        if layout[address].region == BytecodeMemoryRegion.FRAME
    )
    declared_heap = tuple(
        address
        for address in sorted(layout)
        if layout[address].region == BytecodeMemoryRegion.HEAP
    )
    return MemorySurfaceReport(
        program_name=program.name,
        declared_frame_addresses=declared_frame,
        declared_heap_addresses=declared_heap,
        touched_frame_addresses=tuple(sorted(touched_frame)),
        touched_heap_addresses=tuple(sorted(touched_heap)),
        undeclared_addresses=tuple(sorted(undeclared)),
        max_call_depth=max_call_depth,
        accesses=tuple(accesses),
        boundary_snapshots=tuple(boundary_snapshots),
        final_frame_memory=_region_snapshot(layout, memory, BytecodeMemoryRegion.FRAME),
        final_heap_memory=_region_snapshot(layout, memory, BytecodeMemoryRegion.HEAP),
    )
