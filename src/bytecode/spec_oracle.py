from __future__ import annotations

from dataclasses import dataclass

from .ir import BytecodeOpcode, BytecodeProgram
from .types import BytecodeMemoryRegion, BytecodeType


_SPEC_OPCODE_NAMES = {
    BytecodeOpcode.CONST_I32: "push_const",
    BytecodeOpcode.CONST_ADDR: "push_const",
    BytecodeOpcode.DUP: "dup",
    BytecodeOpcode.POP: "pop",
    BytecodeOpcode.ADD_I32: "add",
    BytecodeOpcode.SUB_I32: "sub",
    BytecodeOpcode.EQ_I32: "eq",
    BytecodeOpcode.LOAD_STATIC: "load",
    BytecodeOpcode.STORE_STATIC: "store",
    BytecodeOpcode.LOAD_INDIRECT: "load_at",
    BytecodeOpcode.STORE_INDIRECT: "store_at",
    BytecodeOpcode.JMP: "jmp",
    BytecodeOpcode.JZ_ZERO: "jz",
    BytecodeOpcode.CALL: "call",
    BytecodeOpcode.RET: "ret",
    BytecodeOpcode.HALT: "halt",
}


@dataclass(frozen=True, slots=True)
class SpecValidationResult:
    program_name: str
    passed: bool
    first_error_pc: int | None
    error_class: str | None
    expected_stack: tuple[str, ...]
    actual_stack: tuple[str, ...]
    message: str


@dataclass(frozen=True, slots=True)
class SpecSurfaceValidationResult:
    program_name: str
    passed: bool
    first_error_pc: int | None
    error_class: str | None
    message: str


@dataclass(frozen=True, slots=True)
class SpecEvent:
    step: int
    pc: int
    opcode: str
    arg: int | None
    popped: tuple[int, ...]
    pushed: tuple[int, ...]
    branch_taken: bool | None
    memory_read_address: int | None
    memory_read_value: int | None
    memory_write: tuple[int, int] | None
    next_pc: int
    stack_depth_before: int
    stack_depth_after: int
    halted: bool


@dataclass(frozen=True, slots=True)
class SpecExecutionState:
    pc: int = 0
    stack: tuple[int, ...] = ()
    frame_memory: tuple[tuple[int, int], ...] = ()
    heap_memory: tuple[tuple[int, int], ...] = ()
    call_stack: tuple[int, ...] = ()
    halted: bool = False
    steps: int = 0

    @property
    def memory(self) -> tuple[tuple[int, int], ...]:
        merged = dict(self.frame_memory)
        merged.update(self.heap_memory)
        return tuple(sorted(merged.items()))


@dataclass(frozen=True, slots=True)
class SpecExecutionResult:
    program_name: str
    events: tuple[SpecEvent, ...]
    final_state: SpecExecutionState


def _stack_names(stack: tuple[BytecodeType, ...]) -> tuple[str, ...]:
    return tuple(value.value for value in stack)


def _validation_fail(
    program: BytecodeProgram,
    *,
    pc: int | None,
    error_class: str,
    expected_stack: tuple[BytecodeType, ...] = (),
    actual_stack: tuple[BytecodeType, ...] = (),
    message: str,
) -> SpecValidationResult:
    return SpecValidationResult(
        program_name=program.name,
        passed=False,
        first_error_pc=pc,
        error_class=error_class,
        expected_stack=_stack_names(expected_stack),
        actual_stack=_stack_names(actual_stack),
        message=message,
    )


def _surface_fail(
    program: BytecodeProgram,
    *,
    pc: int | None,
    error_class: str,
    message: str,
) -> SpecSurfaceValidationResult:
    return SpecSurfaceValidationResult(
        program_name=program.name,
        passed=False,
        first_error_pc=pc,
        error_class=error_class,
        message=message,
    )


def _transfer(
    program: BytecodeProgram,
    *,
    pc: int,
    stack: tuple[BytecodeType, ...],
) -> tuple[tuple[tuple[int, tuple[BytecodeType, ...]], ...], SpecValidationResult | None]:
    instruction = program.instructions[pc]
    opcode = instruction.opcode

    if opcode in {BytecodeOpcode.CONST_I32, BytecodeOpcode.CONST_ADDR} and instruction.arg is None:
        return (), _validation_fail(
            program,
            pc=pc,
            error_class="missing_arg",
            message=f"{opcode.value} requires an integer argument.",
        )
    if opcode in {BytecodeOpcode.LOAD_STATIC, BytecodeOpcode.STORE_STATIC}:
        if instruction.arg is None:
            return (), _validation_fail(
                program,
                pc=pc,
                error_class="missing_arg",
                message=f"{opcode.value} requires a non-negative static address.",
            )
        if instruction.arg < 0:
            return (), _validation_fail(
                program,
                pc=pc,
                error_class="static_address",
                message=f"{opcode.value} expects a non-negative static address.",
            )
    if opcode in {BytecodeOpcode.JMP, BytecodeOpcode.JZ_ZERO}:
        if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
            return (), _validation_fail(
                program,
                pc=pc,
                error_class="branch_target",
                message=f"{opcode.value} target must stay within program bounds.",
            )
    if opcode == BytecodeOpcode.CALL:
        if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
            return (), _validation_fail(
                program,
                pc=pc,
                error_class="call_target",
                message="call target must stay within program bounds.",
            )

    if opcode == BytecodeOpcode.DUP:
        if not stack:
            return (), _validation_fail(
                program,
                pc=pc,
                error_class="stack_underflow",
                expected_stack=(BytecodeType.I32,),
                actual_stack=stack,
                message="dup requires at least one stack value.",
            )
        return (((pc + 1, stack + (stack[-1],)),), None)

    if opcode == BytecodeOpcode.POP:
        if not stack:
            return (), _validation_fail(
                program,
                pc=pc,
                error_class="stack_underflow",
                expected_stack=(BytecodeType.I32,),
                actual_stack=stack,
                message="pop requires at least one stack value.",
            )
        return (((pc + 1, stack[:-1]),), None)

    required_stack = instruction.in_types
    if len(stack) < len(required_stack):
        return (), _validation_fail(
            program,
            pc=pc,
            error_class="stack_underflow",
            expected_stack=required_stack,
            actual_stack=stack,
            message=f"{opcode.value} requires stack suffix {', '.join(item.value for item in required_stack)}.",
        )

    actual_suffix = stack[-len(required_stack) :] if required_stack else ()
    if required_stack and actual_suffix != required_stack:
        return (), _validation_fail(
            program,
            pc=pc,
            error_class="type_mismatch",
            expected_stack=required_stack,
            actual_stack=actual_suffix,
            message=f"{opcode.value} expected {', '.join(item.value for item in required_stack)}.",
        )

    base_stack = stack[: len(stack) - len(required_stack)] if required_stack else stack
    next_stack = base_stack + instruction.out_types

    if opcode == BytecodeOpcode.HALT:
        return (), None
    if opcode == BytecodeOpcode.CALL:
        return (((instruction.arg, next_stack),), None)
    if opcode == BytecodeOpcode.RET:
        return (((pc + 1, next_stack),), None)
    if opcode == BytecodeOpcode.JMP:
        return (((instruction.arg, next_stack),), None)
    if opcode == BytecodeOpcode.JZ_ZERO:
        return (((pc + 1, next_stack), (instruction.arg, next_stack)), None)
    return (((pc + 1, next_stack),), None)


def validate_program_contract(program: BytecodeProgram) -> SpecValidationResult:
    if not program.instructions:
        return _validation_fail(
            program,
            pc=None,
            error_class="empty_program",
            message="bytecode program must contain at least one instruction.",
        )

    start_state = (0, ())
    incoming: dict[tuple[int, tuple[tuple[int, int], ...]], tuple[BytecodeType, ...]] = {start_state: ()}
    worklist = [start_state]
    halted_reachable = False

    while worklist:
        state = min(worklist, key=lambda item: (item[0], item[1]))
        worklist.remove(state)
        pc, frames = state
        stack = incoming[state]
        instruction = program.instructions[pc]

        if instruction.opcode == BytecodeOpcode.CALL:
            target = instruction.arg
            if target is None or not (0 <= target < len(program.instructions)):
                return _validation_fail(
                    program,
                    pc=pc,
                    error_class="call_target",
                    actual_stack=stack,
                    message="call target must stay within program bounds.",
                )
            active_targets = {frame[1] for frame in frames}
            if target in active_targets:
                return _validation_fail(
                    program,
                    pc=pc,
                    error_class="recursive_call",
                    actual_stack=stack,
                    message="recursive or mutually recursive call cycles are out of scope.",
                )
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            next_frames = frames + ((pc + 1, target),)
            stacked_transitions = tuple(((target_pc, next_frames), target_stack) for target_pc, target_stack in transitions)
        elif instruction.opcode == BytecodeOpcode.RET:
            if not frames:
                return _validation_fail(
                    program,
                    pc=pc,
                    error_class="empty_return",
                    actual_stack=stack,
                    message="ret requires one pending call frame.",
                )
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            return_pc = frames[-1][0]
            stacked_transitions = (((return_pc, frames[:-1]), transitions[0][1]),)
        elif instruction.opcode == BytecodeOpcode.HALT:
            if frames:
                return _validation_fail(
                    program,
                    pc=pc,
                    error_class="unterminated_frame",
                    actual_stack=stack,
                    message="halt is only valid when the call stack is empty.",
                )
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            stacked_transitions = ()
        else:
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            stacked_transitions = tuple(((target_pc, frames), target_stack) for target_pc, target_stack in transitions)

        if not stacked_transitions:
            halted_reachable = True
            continue

        for target_state, target_stack in stacked_transitions:
            previous_stack = incoming.get(target_state)
            if previous_stack is None:
                incoming[target_state] = target_stack
                worklist.append(target_state)
                continue
            if previous_stack != target_stack:
                return _validation_fail(
                    program,
                    pc=target_state[0],
                    error_class="stack_join_mismatch",
                    expected_stack=previous_stack,
                    actual_stack=target_stack,
                    message="control-flow join requires one consistent stack typing.",
                )

    if not halted_reachable:
        return _validation_fail(
            program,
            pc=None,
            error_class="no_halt",
            message="bytecode program has no reachable halt.",
        )

    return SpecValidationResult(
        program_name=program.name,
        passed=True,
        first_error_pc=None,
        error_class=None,
        expected_stack=(),
        actual_stack=(),
        message="ok",
    )


def validate_surface_literals(program: BytecodeProgram) -> SpecSurfaceValidationResult:
    if not program.memory_layout:
        return SpecSurfaceValidationResult(
            program_name=program.name,
            passed=True,
            first_error_pc=None,
            error_class=None,
            message="no layout restrictions",
        )

    layout = program.memory_layout_map
    for pc, instruction in enumerate(program.instructions):
        if instruction.opcode == BytecodeOpcode.CONST_ADDR:
            if instruction.arg is None or instruction.arg < 0:
                return _surface_fail(
                    program,
                    pc=pc,
                    error_class="undeclared_address_literal",
                    message="const_addr requires one declared non-negative address literal.",
                )
            if instruction.arg not in layout:
                return _surface_fail(
                    program,
                    pc=pc,
                    error_class="undeclared_address_literal",
                    message=f"address literal {instruction.arg} is not declared in the memory layout.",
                )
        if instruction.opcode in {BytecodeOpcode.LOAD_STATIC, BytecodeOpcode.STORE_STATIC}:
            if instruction.arg is None or instruction.arg < 0:
                return _surface_fail(
                    program,
                    pc=pc,
                    error_class="undeclared_static_address",
                    message=f"{instruction.opcode.value} requires one declared non-negative static address.",
                )
            if instruction.arg not in layout:
                return _surface_fail(
                    program,
                    pc=pc,
                    error_class="undeclared_static_address",
                    message=f"static address {instruction.arg} is not declared in the memory layout.",
                )
    return SpecSurfaceValidationResult(
        program_name=program.name,
        passed=True,
        first_error_pc=None,
        error_class=None,
        message="ok",
    )


def run_spec_program(program: BytecodeProgram, max_steps: int = 10_000) -> SpecExecutionResult:
    layout = program.memory_layout_map
    frame_memory: dict[int, int] = {}
    heap_memory: dict[int, int] = {}
    stack: list[int] = []
    call_stack: list[int] = []
    events: list[SpecEvent] = []
    pc = 0
    steps = 0
    halted = False

    while not halted:
        if steps >= max_steps:
            raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
        if not (0 <= pc < len(program.instructions)):
            raise RuntimeError(f"Program counter out of range: {pc}")

        instruction = program.instructions[pc]
        popped: tuple[int, ...] = ()
        pushed: tuple[int, ...] = ()
        branch_taken: bool | None = None
        memory_read_address: int | None = None
        memory_read_value: int | None = None
        memory_write: tuple[int, int] | None = None
        next_pc = pc + 1

        match instruction.opcode:
            case BytecodeOpcode.CONST_I32 | BytecodeOpcode.CONST_ADDR:
                if instruction.arg is None:
                    raise RuntimeError(f"{instruction.opcode.value} requires an integer argument.")
                stack.append(instruction.arg)
                pushed = (instruction.arg,)
            case BytecodeOpcode.DUP:
                if not stack:
                    raise RuntimeError("dup requires at least one stack element.")
                stack.append(stack[-1])
                pushed = (stack[-1],)
            case BytecodeOpcode.POP:
                if not stack:
                    raise RuntimeError("pop requires at least one stack element.")
                popped = (stack.pop(),)
            case BytecodeOpcode.ADD_I32:
                if len(stack) < 2:
                    raise RuntimeError("add_i32 requires at least two stack elements.")
                rhs = stack.pop()
                lhs = stack.pop()
                result = lhs + rhs
                stack.append(result)
                popped = (lhs, rhs)
                pushed = (result,)
            case BytecodeOpcode.SUB_I32:
                if len(stack) < 2:
                    raise RuntimeError("sub_i32 requires at least two stack elements.")
                rhs = stack.pop()
                lhs = stack.pop()
                result = lhs - rhs
                stack.append(result)
                popped = (lhs, rhs)
                pushed = (result,)
            case BytecodeOpcode.EQ_I32:
                if len(stack) < 2:
                    raise RuntimeError("eq_i32 requires at least two stack elements.")
                rhs = stack.pop()
                lhs = stack.pop()
                result = int(lhs == rhs)
                stack.append(result)
                popped = (lhs, rhs)
                pushed = (result,)
            case BytecodeOpcode.LOAD_STATIC:
                if instruction.arg is None or instruction.arg < 0:
                    raise RuntimeError("load_static requires one non-negative address.")
                memory_read_address = instruction.arg
                region = layout.get(instruction.arg)
                if region is not None and region.region == BytecodeMemoryRegion.HEAP:
                    memory_read_value = heap_memory.get(instruction.arg, 0)
                else:
                    memory_read_value = frame_memory.get(instruction.arg, 0)
                stack.append(memory_read_value)
                pushed = (memory_read_value,)
            case BytecodeOpcode.STORE_STATIC:
                if instruction.arg is None or instruction.arg < 0:
                    raise RuntimeError("store_static requires one non-negative address.")
                if not stack:
                    raise RuntimeError("store_static requires a value on the stack.")
                value = stack.pop()
                region = layout.get(instruction.arg)
                if region is not None and region.region == BytecodeMemoryRegion.HEAP:
                    heap_memory[instruction.arg] = value
                else:
                    frame_memory[instruction.arg] = value
                popped = (value,)
                memory_write = (instruction.arg, value)
            case BytecodeOpcode.LOAD_INDIRECT:
                if not stack:
                    raise RuntimeError("load_indirect requires an address on the stack.")
                address = stack.pop()
                if address < 0:
                    raise RuntimeError("load_indirect address must be non-negative.")
                region = layout.get(address)
                if region is not None and region.region == BytecodeMemoryRegion.HEAP:
                    value = heap_memory.get(address, 0)
                else:
                    value = frame_memory.get(address, 0)
                popped = (address,)
                pushed = (value,)
                memory_read_address = address
                memory_read_value = value
                stack.append(value)
            case BytecodeOpcode.STORE_INDIRECT:
                if len(stack) < 2:
                    raise RuntimeError("store_indirect requires a value and an address on the stack.")
                address = stack.pop()
                value = stack.pop()
                if address < 0:
                    raise RuntimeError("store_indirect address must be non-negative.")
                region = layout.get(address)
                if region is not None and region.region == BytecodeMemoryRegion.HEAP:
                    heap_memory[address] = value
                else:
                    frame_memory[address] = value
                popped = (value, address)
                memory_write = (address, value)
            case BytecodeOpcode.JMP:
                if instruction.arg is None:
                    raise RuntimeError("jmp requires a target PC.")
                branch_taken = True
                next_pc = instruction.arg
            case BytecodeOpcode.JZ_ZERO:
                if instruction.arg is None:
                    raise RuntimeError("jz_zero requires a target PC.")
                if not stack:
                    raise RuntimeError("jz_zero requires a condition value on the stack.")
                condition = stack.pop()
                popped = (condition,)
                branch_taken = condition == 0
                next_pc = instruction.arg if branch_taken else pc + 1
            case BytecodeOpcode.CALL:
                if instruction.arg is None:
                    raise RuntimeError("call requires a target PC.")
                call_stack.append(pc + 1)
                branch_taken = True
                next_pc = instruction.arg
            case BytecodeOpcode.RET:
                if not call_stack:
                    raise RuntimeError("ret requires a pending return address.")
                branch_taken = True
                next_pc = call_stack.pop()
            case BytecodeOpcode.HALT:
                halted = True
                next_pc = pc
            case _:
                raise RuntimeError(f"Unsupported bytecode opcode: {instruction.opcode}")

        events.append(
            SpecEvent(
                step=steps,
                pc=pc,
                opcode=_SPEC_OPCODE_NAMES[instruction.opcode],
                arg=instruction.arg,
                popped=popped,
                pushed=pushed,
                branch_taken=branch_taken,
                memory_read_address=memory_read_address,
                memory_read_value=memory_read_value,
                memory_write=memory_write,
                next_pc=next_pc,
                stack_depth_before=len(stack) - len(pushed) + len(popped),
                stack_depth_after=len(stack),
                halted=halted,
            )
        )
        pc = next_pc
        steps += 1

    return SpecExecutionResult(
        program_name=program.name,
        events=tuple(events),
        final_state=SpecExecutionState(
            pc=pc,
            stack=tuple(stack),
            frame_memory=tuple(sorted(frame_memory.items())),
            heap_memory=tuple(sorted(heap_memory.items())),
            call_stack=tuple(call_stack),
            halted=halted,
            steps=steps,
        ),
    )


def normalize_event(event: object) -> tuple[object, ...]:
    opcode = getattr(getattr(event, "opcode", None), "value", getattr(event, "opcode", None))
    return (
        getattr(event, "step"),
        getattr(event, "pc"),
        opcode,
        getattr(event, "arg"),
        tuple(getattr(event, "popped")),
        tuple(getattr(event, "pushed")),
        getattr(event, "branch_taken"),
        getattr(event, "memory_read_address"),
        getattr(event, "memory_read_value"),
        getattr(event, "memory_write"),
        getattr(event, "next_pc"),
        getattr(event, "stack_depth_before"),
        getattr(event, "stack_depth_after"),
        getattr(event, "halted"),
    )


def normalize_final_state(state: object) -> tuple[object, ...]:
    memory = getattr(state, "memory", None)
    if callable(memory):
        memory = memory()
    if memory is None:
        frame_memory = dict(getattr(state, "frame_memory"))
        frame_memory.update(dict(getattr(state, "heap_memory")))
        memory = tuple(sorted(frame_memory.items()))
    return (
        getattr(state, "pc"),
        tuple(getattr(state, "stack")),
        tuple(memory),
        tuple(getattr(state, "call_stack")),
        getattr(state, "halted"),
        getattr(state, "steps"),
    )


def first_divergence_step(reference_events: tuple[object, ...], candidate_events: tuple[object, ...]) -> int | None:
    for reference_event, candidate_event in zip(reference_events, candidate_events, strict=False):
        if normalize_event(reference_event) != normalize_event(candidate_event):
            return getattr(candidate_event, "step", getattr(reference_event, "step", None))
    if len(reference_events) != len(candidate_events):
        return min(len(reference_events), len(candidate_events))
    return None
