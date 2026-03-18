from __future__ import annotations

from dataclasses import dataclass

from exec_trace import (
    Program as TraceProgram,
    alternating_memory_loop_program,
    dynamic_latest_write_program as trace_dynamic_latest_write_program,
    equality_branch_program,
    flagged_indirect_accumulator_program,
    loop_indirect_memory_program,
    selector_checkpoint_bank_program,
)
from exec_trace.dsl import Opcode as TraceOpcode

from .ir import BytecodeInstruction, BytecodeOpcode, BytecodeProgram
from .types import BytecodeMemoryCell, BytecodeMemoryRegion, BytecodeType


@dataclass(frozen=True, slots=True)
class BytecodeCase:
    suite: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram


@dataclass(frozen=True, slots=True)
class StressReferenceCase:
    suite: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram
    diagnostic_surface: bool = False


def _frame_cell(
    address: int,
    cell_type: BytecodeType,
    label: str,
    *,
    allowed_targets: tuple[int, ...] = (),
) -> BytecodeMemoryCell:
    return BytecodeMemoryCell(
        address=address,
        cell_type=cell_type,
        region=BytecodeMemoryRegion.FRAME,
        label=label,
        allowed_targets=allowed_targets,
    )


def _heap_cell(address: int, cell_type: BytecodeType, label: str, *, alias_group: str | None = None) -> BytecodeMemoryCell:
    return BytecodeMemoryCell(
        address=address,
        cell_type=cell_type,
        region=BytecodeMemoryRegion.HEAP,
        label=label,
        alias_group=alias_group,
    )


def _convert_trace_program(
    program: TraceProgram,
    *,
    name: str,
    addr_constant_pcs: set[int] | None = None,
    jz_i32_pcs: set[int] | None = None,
    static_cell_types: dict[int, BytecodeType] | None = None,
) -> BytecodeProgram:
    addr_constant_pcs = addr_constant_pcs or set()
    jz_i32_pcs = jz_i32_pcs or set()
    static_cell_types = static_cell_types or {}
    instructions: list[BytecodeInstruction] = []

    for pc, instruction in enumerate(program.instructions):
        match instruction.opcode:
            case TraceOpcode.PUSH_CONST:
                opcode = BytecodeOpcode.CONST_ADDR if pc in addr_constant_pcs else BytecodeOpcode.CONST_I32
                instructions.append(BytecodeInstruction(opcode, instruction.arg))
            case TraceOpcode.ADD:
                instructions.append(BytecodeInstruction(BytecodeOpcode.ADD_I32))
            case TraceOpcode.SUB:
                instructions.append(BytecodeInstruction(BytecodeOpcode.SUB_I32))
            case TraceOpcode.EQ:
                instructions.append(BytecodeInstruction(BytecodeOpcode.EQ_I32))
            case TraceOpcode.DUP:
                instructions.append(BytecodeInstruction(BytecodeOpcode.DUP))
            case TraceOpcode.POP:
                instructions.append(BytecodeInstruction(BytecodeOpcode.POP))
            case TraceOpcode.LOAD:
                cell_type = static_cell_types.get(instruction.arg, BytecodeType.I32)
                instructions.append(
                    BytecodeInstruction(
                        BytecodeOpcode.LOAD_STATIC,
                        instruction.arg,
                        out_types=(cell_type,),
                    )
                )
            case TraceOpcode.STORE:
                cell_type = static_cell_types.get(instruction.arg, BytecodeType.I32)
                instructions.append(
                    BytecodeInstruction(
                        BytecodeOpcode.STORE_STATIC,
                        instruction.arg,
                        in_types=(cell_type,),
                    )
                )
            case TraceOpcode.LOAD_AT:
                instructions.append(BytecodeInstruction(BytecodeOpcode.LOAD_INDIRECT))
            case TraceOpcode.STORE_AT:
                instructions.append(BytecodeInstruction(BytecodeOpcode.STORE_INDIRECT))
            case TraceOpcode.JMP:
                instructions.append(BytecodeInstruction(BytecodeOpcode.JMP, instruction.arg))
            case TraceOpcode.JZ:
                if pc in jz_i32_pcs:
                    instructions.append(
                        BytecodeInstruction(
                            BytecodeOpcode.JZ_ZERO,
                            instruction.arg,
                            in_types=(BytecodeType.I32,),
                        )
                    )
                else:
                    instructions.append(BytecodeInstruction(BytecodeOpcode.JZ_ZERO, instruction.arg))
            case TraceOpcode.HALT:
                instructions.append(BytecodeInstruction(BytecodeOpcode.HALT))
            case _:
                raise ValueError(f"Unsupported trace opcode for bytecode conversion: {instruction.opcode}")

    return BytecodeProgram(instructions=tuple(instructions), name=name)


def arithmetic_smoke_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 7),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 5),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ),
        name="bytecode_arithmetic_smoke",
    )


def static_memory_roundtrip_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 11),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ),
        name="bytecode_static_memory_roundtrip",
    )


def indirect_memory_roundtrip_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 17),
            BytecodeInstruction(BytecodeOpcode.CONST_ADDR, 4),
            BytecodeInstruction(BytecodeOpcode.STORE_INDIRECT),
            BytecodeInstruction(BytecodeOpcode.CONST_ADDR, 4),
            BytecodeInstruction(BytecodeOpcode.LOAD_INDIRECT),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ),
        name="bytecode_indirect_memory_roundtrip",
    )


def eq_branch_true_program() -> BytecodeProgram:
    return _convert_trace_program(
        equality_branch_program(7, 7),
        name="bytecode_eq_branch_true",
    )


def eq_branch_false_program() -> BytecodeProgram:
    return _convert_trace_program(
        equality_branch_program(7, 9),
        name="bytecode_eq_branch_false",
    )


def call_add_halt_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 7),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 5),
            BytecodeInstruction(BytecodeOpcode.CALL, 4),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name="bytecode_call_add_halt",
    )


def branch_then_call_true_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 4),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 4),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 7),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 10),
            BytecodeInstruction(BytecodeOpcode.CALL, 9),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name="bytecode_branch_then_call_true",
    )


def branch_then_call_false_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 4),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 5),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 6),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 10),
            BytecodeInstruction(BytecodeOpcode.CALL, 10),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.POP),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 2),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name="bytecode_branch_then_call_false",
    )


def call_chain_smoke_program() -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 2),
            BytecodeInstruction(BytecodeOpcode.CALL, 4),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 3),
            BytecodeInstruction(BytecodeOpcode.CALL, 8),
            BytecodeInstruction(BytecodeOpcode.RET),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name="bytecode_call_chain_smoke",
    )


def call_frame_roundtrip_program(*, slot_address: int = 192) -> BytecodeProgram:
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 9),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, slot_address),
            BytecodeInstruction(BytecodeOpcode.CALL, 4),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, slot_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.DUP),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, slot_address),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name=f"bytecode_call_frame_roundtrip_a{slot_address}",
        memory_layout=(
            _frame_cell(slot_address, BytecodeType.I32, "local_slot"),
        ),
    )


def countdown_loop_program(start: int) -> BytecodeProgram:
    if start < 0:
        raise ValueError("countdown_loop_program expects a non-negative start.")
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.DUP),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 7),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.POP),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.JMP, 1),
        ),
        name=f"bytecode_countdown_{start}",
    )


def countdown_helper_call_program(start: int, *, counter_address: int = 0) -> BytecodeProgram:
    if start < 0:
        raise ValueError("countdown_helper_call_program expects a non-negative start.")
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 8),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.CALL, 10),
            BytecodeInstruction(BytecodeOpcode.JMP, 2),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name=f"bytecode_countdown_helper_call_{start}_a{counter_address}",
        memory_layout=(
            _frame_cell(counter_address, BytecodeType.I32, "counter"),
        ),
    )


def accumulator_loop_program(start: int) -> BytecodeProgram:
    if start < 0:
        raise ValueError("accumulator_loop_program expects a non-negative start.")
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, 1),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 10),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, 1),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, 1),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, 1),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, 0),
            BytecodeInstruction(BytecodeOpcode.JMP, 4),
        ),
        name=f"bytecode_accumulator_{start}",
    )


def loop_with_subroutine_update_program(
    start: int,
    *,
    counter_address: int = 0,
    accumulator_address: int = 1,
) -> BytecodeProgram:
    if start < 0:
        raise ValueError("loop_with_subroutine_update_program expects a non-negative start.")
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, accumulator_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 10),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, accumulator_address),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.CALL, 12),
            BytecodeInstruction(BytecodeOpcode.JMP, 4),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, accumulator_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, accumulator_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name=f"bytecode_loop_with_subroutine_update_{start}_a{counter_address}_b{accumulator_address}",
        memory_layout=(
            _frame_cell(counter_address, BytecodeType.I32, "counter"),
            _frame_cell(accumulator_address, BytecodeType.I32, "accumulator"),
        ),
    )


def iterated_helper_accumulator_program(
    start: int,
    *,
    counter_address: int = 0,
    accumulator_address: int = 1,
) -> BytecodeProgram:
    base_program = loop_with_subroutine_update_program(
        start,
        counter_address=counter_address,
        accumulator_address=accumulator_address,
    )
    return BytecodeProgram(
        instructions=base_program.instructions,
        name=f"bytecode_iterated_helper_accumulator_{start}_a{counter_address}_b{accumulator_address}",
        memory_layout=base_program.memory_layout,
    )


def dynamic_latest_write_program() -> BytecodeProgram:
    return _convert_trace_program(
        trace_dynamic_latest_write_program(),
        name="bytecode_dynamic_latest_write",
        addr_constant_pcs={1, 4, 6},
    )


def alternating_memory_loop_bytecode_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    return _convert_trace_program(
        alternating_memory_loop_program(start, base_address=base_address),
        name=f"bytecode_alternating_memory_loop_{start}_a{base_address}",
        jz_i32_pcs={10, 13},
    )


def selector_checkpoint_bank_bytecode_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    return _convert_trace_program(
        selector_checkpoint_bank_program(start, base_address=base_address),
        name=f"bytecode_selector_checkpoint_bank_{start}_a{base_address}",
        addr_constant_pcs={4, 6, 8, 10},
        jz_i32_pcs={20, 24, 45},
        static_cell_types={
            base_address + 2: BytecodeType.ADDR,
            base_address + 3: BytecodeType.ADDR,
            base_address + 4: BytecodeType.ADDR,
            base_address + 5: BytecodeType.ADDR,
        },
    )


def indirect_counter_bank_program(
    start: int,
    *,
    counter_address: int = 4,
    accumulator_address: int = 5,
) -> BytecodeProgram:
    trace_program = loop_indirect_memory_program(
        start,
        counter_address=counter_address,
        accumulator_address=accumulator_address,
    )
    addr_constant_pcs = {1, 4, 6, 10, 13, 15, 19, 23}
    return _convert_trace_program(
        trace_program,
        name=f"bytecode_indirect_counter_bank_{start}_a{counter_address}_b{accumulator_address}",
        addr_constant_pcs=addr_constant_pcs,
        jz_i32_pcs={9},
    )


def stack_memory_braid_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    return _convert_trace_program(
        flagged_indirect_accumulator_program(start, base_address=base_address),
        name=f"bytecode_stack_memory_braid_{start}_a{base_address}",
        addr_constant_pcs={4, 6},
        jz_i32_pcs={14, 17},
        static_cell_types={
            base_address + 2: BytecodeType.ADDR,
            base_address + 3: BytecodeType.ADDR,
        },
    )


def checkpoint_replay_long_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    return _convert_trace_program(
        selector_checkpoint_bank_program(start, base_address=base_address),
        name=f"bytecode_checkpoint_replay_long_{start}_a{base_address}",
        addr_constant_pcs={4, 6, 8, 10},
        jz_i32_pcs={20, 24, 45},
        static_cell_types={
            base_address + 2: BytecodeType.ADDR,
            base_address + 3: BytecodeType.ADDR,
            base_address + 4: BytecodeType.ADDR,
            base_address + 5: BytecodeType.ADDR,
        },
    )


def subroutine_braid_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    if start < 0:
        raise ValueError("subroutine_braid_program expects a non-negative start.")
    counter_address = base_address
    flag_address = base_address + 1
    left_address = base_address + 2
    right_address = base_address + 3
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, flag_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 16),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, flag_address),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 22, in_types=(BytecodeType.I32,)),
            BytecodeInstruction(BytecodeOpcode.CALL, 30),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, flag_address),
            BytecodeInstruction(BytecodeOpcode.JMP, 25),
            BytecodeInstruction(BytecodeOpcode.CALL, 35),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, flag_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.JMP, 8),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.RET),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.RET),
        ),
        name=f"bytecode_subroutine_braid_{start}_a{base_address}",
        memory_layout=(
            _frame_cell(counter_address, BytecodeType.I32, "counter"),
            _frame_cell(flag_address, BytecodeType.I32, "flag"),
            _heap_cell(left_address, BytecodeType.I32, "left_accumulator", alias_group="braid_left"),
            _heap_cell(right_address, BytecodeType.I32, "right_accumulator", alias_group="braid_right"),
        ),
    )


def subroutine_braid_long_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    base_program = subroutine_braid_program(start, base_address=base_address)
    return BytecodeProgram(
        instructions=base_program.instructions,
        name=f"bytecode_subroutine_braid_long_{start}_a{base_address}",
        memory_layout=base_program.memory_layout,
    )


def _helper_checkpoint_braid_layout(
    base_address: int,
    *,
    include_replay_slot: bool = True,
) -> tuple[BytecodeMemoryCell, ...]:
    counter_address = base_address
    selector_address = base_address + 1
    checkpoint_address = base_address + 2
    replay_address = base_address + 3
    left_address = base_address + 4
    right_address = base_address + 5
    layout = [
        _frame_cell(counter_address, BytecodeType.I32, "counter"),
        _frame_cell(selector_address, BytecodeType.I32, "selector"),
        _frame_cell(
            checkpoint_address,
            BytecodeType.ADDR,
            "checkpoint_slot",
            allowed_targets=(left_address, right_address),
        ),
        _heap_cell(left_address, BytecodeType.I32, "left_accumulator", alias_group="helper_left"),
        _heap_cell(right_address, BytecodeType.I32, "right_accumulator", alias_group="helper_right"),
    ]
    if include_replay_slot:
        layout.insert(3, _frame_cell(replay_address, BytecodeType.I32, "replay_value"))
    return tuple(layout)


def _helper_checkpoint_braid_instructions(
    start: int,
    *,
    base_address: int,
    selector_seed: int,
    typed_selector_branch: bool,
) -> tuple[BytecodeInstruction, ...]:
    if start < 0:
        raise ValueError("_helper_checkpoint_braid_instructions expects a non-negative start.")
    if selector_seed not in {0, 1}:
        raise ValueError("_helper_checkpoint_braid_instructions expects selector_seed in {0, 1}.")

    counter_address = base_address
    selector_address = base_address + 1
    checkpoint_address = base_address + 2
    replay_address = base_address + 3
    left_address = base_address + 4
    right_address = base_address + 5
    selector_branch = BytecodeInstruction(
        BytecodeOpcode.JZ_ZERO,
        24,
        in_types=(BytecodeType.I32,),
    )
    if not typed_selector_branch:
        selector_branch = BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 24)
    return (
        BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, selector_seed),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, selector_address),
        BytecodeInstruction(BytecodeOpcode.CONST_ADDR, left_address),
        BytecodeInstruction(
            BytecodeOpcode.STORE_STATIC,
            checkpoint_address,
            in_types=(BytecodeType.ADDR,),
        ),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, replay_address),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, left_address),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, right_address),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
        BytecodeInstruction(BytecodeOpcode.EQ_I32),
        BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 18),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, replay_address),
        BytecodeInstruction(BytecodeOpcode.HALT),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, selector_address),
        selector_branch,
        BytecodeInstruction(BytecodeOpcode.CALL, 44),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, selector_address),
        BytecodeInstruction(BytecodeOpcode.JMP, 27),
        BytecodeInstruction(BytecodeOpcode.CALL, 35),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, selector_address),
        BytecodeInstruction(
            BytecodeOpcode.LOAD_STATIC,
            checkpoint_address,
            out_types=(BytecodeType.ADDR,),
        ),
        BytecodeInstruction(BytecodeOpcode.LOAD_INDIRECT),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, replay_address),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
        BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
        BytecodeInstruction(BytecodeOpcode.SUB_I32),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
        BytecodeInstruction(BytecodeOpcode.JMP, 12),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, left_address),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
        BytecodeInstruction(BytecodeOpcode.ADD_I32),
        BytecodeInstruction(BytecodeOpcode.DUP),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, left_address),
        BytecodeInstruction(BytecodeOpcode.CONST_ADDR, left_address),
        BytecodeInstruction(
            BytecodeOpcode.STORE_STATIC,
            checkpoint_address,
            in_types=(BytecodeType.ADDR,),
        ),
        BytecodeInstruction(BytecodeOpcode.POP),
        BytecodeInstruction(BytecodeOpcode.RET),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, right_address),
        BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
        BytecodeInstruction(BytecodeOpcode.ADD_I32),
        BytecodeInstruction(BytecodeOpcode.DUP),
        BytecodeInstruction(BytecodeOpcode.STORE_STATIC, right_address),
        BytecodeInstruction(BytecodeOpcode.CONST_ADDR, right_address),
        BytecodeInstruction(
            BytecodeOpcode.STORE_STATIC,
            checkpoint_address,
            in_types=(BytecodeType.ADDR,),
        ),
        BytecodeInstruction(BytecodeOpcode.POP),
        BytecodeInstruction(BytecodeOpcode.RET),
    )


def helper_checkpoint_braid_program(
    start: int,
    *,
    base_address: int = 200,
    selector_seed: int = 0,
) -> BytecodeProgram:
    return BytecodeProgram(
        instructions=_helper_checkpoint_braid_instructions(
            start,
            base_address=base_address,
            selector_seed=selector_seed,
            typed_selector_branch=True,
        ),
        name=f"bytecode_helper_checkpoint_braid_{start}_a{base_address}_s{selector_seed}",
        memory_layout=_helper_checkpoint_braid_layout(base_address),
    )


def helper_checkpoint_braid_long_program(
    start: int,
    *,
    base_address: int = 200,
    selector_seed: int = 0,
) -> BytecodeProgram:
    base_program = helper_checkpoint_braid_program(
        start,
        base_address=base_address,
        selector_seed=selector_seed,
    )
    return BytecodeProgram(
        instructions=base_program.instructions,
        name=f"bytecode_helper_checkpoint_braid_long_{start}_a{base_address}_s{selector_seed}",
        memory_layout=base_program.memory_layout,
    )


def invalid_helper_checkpoint_braid_branch_program(
    start: int,
    *,
    base_address: int = 248,
    selector_seed: int = 0,
) -> BytecodeProgram:
    return BytecodeProgram(
        instructions=_helper_checkpoint_braid_instructions(
            start,
            base_address=base_address,
            selector_seed=selector_seed,
            typed_selector_branch=False,
        ),
        name=f"invalid_helper_checkpoint_braid_branch_{start}_a{base_address}_s{selector_seed}",
        memory_layout=_helper_checkpoint_braid_layout(base_address),
    )


def invalid_helper_checkpoint_braid_surface_program(
    start: int,
    *,
    base_address: int = 264,
    selector_seed: int = 1,
) -> BytecodeProgram:
    return BytecodeProgram(
        instructions=_helper_checkpoint_braid_instructions(
            start,
            base_address=base_address,
            selector_seed=selector_seed,
            typed_selector_branch=True,
        ),
        name=f"invalid_helper_checkpoint_braid_surface_{start}_a{base_address}_s{selector_seed}",
        memory_layout=_helper_checkpoint_braid_layout(base_address, include_replay_slot=False),
    )


def verifier_negative_programs() -> tuple[BytecodeProgram, ...]:
    return (
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CONST_ADDR, 4),
                BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
                BytecodeInstruction(BytecodeOpcode.STORE_INDIRECT),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_store_indirect_order",
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.JMP, 9),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_branch_target",
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
                BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 0),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_non_flag_branch",
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CALL, 9),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_call_target",
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.RET),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_empty_return",
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CALL, 2),
                BytecodeInstruction(BytecodeOpcode.HALT),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_unterminated_frame",
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CALL, 2),
                BytecodeInstruction(BytecodeOpcode.HALT),
                BytecodeInstruction(BytecodeOpcode.CALL, 0),
            ),
            name="invalid_recursive_call",
        ),
    )


def harness_cases() -> tuple[BytecodeCase, ...]:
    return (
        BytecodeCase("smoke", "short_exact_trace", 32, arithmetic_smoke_program()),
        BytecodeCase("smoke", "short_exact_trace", 32, eq_branch_true_program()),
        BytecodeCase("smoke", "short_exact_trace", 32, eq_branch_false_program()),
        BytecodeCase("smoke", "short_exact_trace", 32, call_add_halt_program()),
        BytecodeCase("smoke", "short_exact_trace", 32, branch_then_call_true_program()),
        BytecodeCase("smoke", "short_exact_trace", 32, branch_then_call_false_program()),
        BytecodeCase("smoke", "short_exact_trace", 32, call_chain_smoke_program()),
        BytecodeCase("memory", "short_exact_trace", 32, static_memory_roundtrip_program()),
        BytecodeCase("memory", "short_exact_trace", 32, indirect_memory_roundtrip_program()),
        BytecodeCase("memory", "medium_exact_trace", 64, dynamic_latest_write_program()),
        BytecodeCase("loops", "medium_exact_trace", 128, countdown_loop_program(6)),
        BytecodeCase("loops", "medium_exact_trace", 256, alternating_memory_loop_bytecode_program(6, base_address=16)),
        BytecodeCase("loops", "medium_exact_trace", 512, selector_checkpoint_bank_bytecode_program(6, base_address=32)),
        BytecodeCase("control_flow", "medium_exact_trace", 128, countdown_helper_call_program(6, counter_address=48)),
        BytecodeCase(
            "control_flow",
            "medium_exact_trace",
            256,
            loop_with_subroutine_update_program(8, counter_address=64, accumulator_address=65),
        ),
        BytecodeCase("control_flow", "medium_exact_trace", 256, subroutine_braid_program(6, base_address=80)),
        BytecodeCase("loops", "long_exact_final_state", 512, accumulator_loop_program(12)),
        BytecodeCase("loops", "long_exact_final_state", 512, indirect_counter_bank_program(12, counter_address=32, accumulator_address=33)),
        BytecodeCase("loops", "long_exact_final_state", 768, stack_memory_braid_program(8, base_address=64)),
        BytecodeCase("loops", "long_exact_final_state", 1024, checkpoint_replay_long_program(8, base_address=96)),
        BytecodeCase(
            "control_flow",
            "long_exact_final_state",
            512,
            iterated_helper_accumulator_program(20, counter_address=128, accumulator_address=129),
        ),
        BytecodeCase("control_flow", "long_exact_final_state", 768, subroutine_braid_long_program(12, base_address=160)),
    )


def memory_surface_negative_programs() -> tuple[BytecodeProgram, ...]:
    return (
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
                BytecodeInstruction(BytecodeOpcode.STORE_STATIC, 999),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_memory_surface_undeclared_static",
            memory_layout=(
                _frame_cell(200, BytecodeType.I32, "local_slot"),
            ),
        ),
        BytecodeProgram(
            instructions=(
                BytecodeInstruction(BytecodeOpcode.CONST_ADDR, 302),
                BytecodeInstruction(BytecodeOpcode.LOAD_INDIRECT),
                BytecodeInstruction(BytecodeOpcode.HALT),
            ),
            name="invalid_memory_surface_indirect_escape",
            memory_layout=(
                _frame_cell(300, BytecodeType.I32, "counter"),
                _heap_cell(301, BytecodeType.I32, "heap_value"),
            ),
        ),
    )


def memory_surface_cases() -> tuple[BytecodeCase, ...]:
    return (
        BytecodeCase("control_flow_memory", "short_exact_trace", 64, call_frame_roundtrip_program(slot_address=192)),
        BytecodeCase("control_flow_memory", "medium_exact_trace", 128, countdown_helper_call_program(6, counter_address=48)),
        BytecodeCase(
            "control_flow_memory",
            "medium_exact_trace",
            256,
            loop_with_subroutine_update_program(8, counter_address=64, accumulator_address=65),
        ),
        BytecodeCase("control_flow_memory", "medium_exact_trace", 256, subroutine_braid_program(6, base_address=80)),
        BytecodeCase(
            "control_flow_memory",
            "long_exact_final_state",
            512,
            iterated_helper_accumulator_program(20, counter_address=128, accumulator_address=129),
        ),
        BytecodeCase("control_flow_memory", "long_exact_final_state", 768, subroutine_braid_long_program(12, base_address=160)),
    )


def stress_reference_cases() -> tuple[StressReferenceCase, ...]:
    return (
        StressReferenceCase(
            suite="stress_reference",
            comparison_mode="medium_exact_trace",
            max_steps=256,
            program=helper_checkpoint_braid_program(6, base_address=200, selector_seed=0),
            diagnostic_surface=True,
        ),
        StressReferenceCase(
            suite="stress_reference",
            comparison_mode="medium_exact_trace",
            max_steps=256,
            program=helper_checkpoint_braid_program(6, base_address=216, selector_seed=1),
            diagnostic_surface=True,
        ),
        StressReferenceCase(
            suite="stress_reference",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=helper_checkpoint_braid_long_program(18, base_address=232, selector_seed=0),
            diagnostic_surface=True,
        ),
        StressReferenceCase(
            suite="stress_reference",
            comparison_mode="verifier_negative",
            max_steps=256,
            program=invalid_helper_checkpoint_braid_branch_program(6, base_address=248, selector_seed=0),
        ),
        StressReferenceCase(
            suite="stress_reference",
            comparison_mode="memory_surface_negative",
            max_steps=256,
            program=invalid_helper_checkpoint_braid_surface_program(6, base_address=264, selector_seed=1),
        ),
    )
