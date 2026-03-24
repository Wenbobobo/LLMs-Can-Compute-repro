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
from .restricted_frontend import (
    RestrictedFrontendProgram,
    count_nonzero_i32_buffer_frontend_program,
    histogram16_u8_frontend_program,
    sum_i32_buffer_frontend_program,
)
from .restricted_tinyc import (
    RestrictedTinyCProgram,
    compile_restricted_tinyc_program,
    count_nonzero_i32_buffer_tinyc_program,
    histogram16_u8_tinyc_program,
    sum_i32_buffer_tinyc_program,
)
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


@dataclass(frozen=True, slots=True)
class LongHorizonScalingCase:
    family: str
    baseline_stage: str
    baseline_program_name: str
    baseline_start: int
    horizon_multiplier: int
    scaled_start: int
    suite: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram
    diagnostic_surface: bool = False


@dataclass(frozen=True, slots=True)
class RetrievalPressureCase:
    family: str
    baseline_stage: str
    baseline_program_name: str
    baseline_horizon_multiplier: int
    baseline_start: int
    retrieval_horizon_multiplier: int
    scaled_start: int
    suite: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram
    diagnostic_surface: bool = False


@dataclass(frozen=True, slots=True)
class BoundedMemoryVMCase:
    family_id: str
    description: str
    family_role: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram
    gated_on_previous_exact: bool = False


@dataclass(frozen=True, slots=True)
class RestrictedWasmKernelCase:
    kernel_id: str
    description: str
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram


@dataclass(frozen=True, slots=True)
class UsefulCaseSurfaceGeneralizationCase:
    kernel_id: str
    variant_id: str
    description: str
    axis_tags: tuple[str, ...]
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram


@dataclass(frozen=True, slots=True)
class RestrictedFrontendTranslationCase:
    kernel_id: str
    variant_id: str
    description: str
    axis_tags: tuple[str, ...]
    comparison_mode: str
    max_steps: int
    frontend_program: RestrictedFrontendProgram
    canonical_program: BytecodeProgram


@dataclass(frozen=True, slots=True)
class UsefulCaseNumericScalingCase:
    bucket_id: str
    kernel_id: str
    variant_id: str
    description: str
    axis_tags: tuple[str, ...]
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram
    precision_reference_sampled: bool = False


@dataclass(frozen=True, slots=True)
class RestrictedTinyCLoweringCase:
    kernel_id: str
    variant_id: str
    description: str
    axis_tags: tuple[str, ...]
    comparison_mode: str
    max_steps: int
    tinyc_program: RestrictedTinyCProgram
    canonical_program: BytecodeProgram


@dataclass(frozen=True, slots=True)
class MemoryControlSurfaceSufficiencyCase:
    family_id: str
    variant_id: str
    description: str
    axis_tags: tuple[str, ...]
    comparison_mode: str
    max_steps: int
    program: BytecodeProgram
    tinyc_program: RestrictedTinyCProgram | None = None


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


AssemblyRow = str | tuple[BytecodeOpcode, int | str | None] | tuple[
    BytecodeOpcode,
    int | str | None,
    tuple[BytecodeType, ...],
    tuple[BytecodeType, ...],
]


def _assemble_program(
    *,
    name: str,
    rows: list[AssemblyRow],
    memory_layout: tuple[BytecodeMemoryCell, ...],
) -> BytecodeProgram:
    labels: dict[str, int] = {}
    emitted_rows: list[tuple[BytecodeOpcode, int | str | None] | tuple[
        BytecodeOpcode,
        int | str | None,
        tuple[BytecodeType, ...],
        tuple[BytecodeType, ...],
    ]] = []

    for row in rows:
        if isinstance(row, str):
            if not row.endswith(":"):
                raise ValueError(f"Assembly label must end with ':'; got {row!r}.")
            labels[row[:-1]] = len(emitted_rows)
            continue
        emitted_rows.append(row)

    instructions: list[BytecodeInstruction] = []
    for row in emitted_rows:
        if len(row) == 2:
            opcode, arg = row
            in_types: tuple[BytecodeType, ...] = ()
            out_types: tuple[BytecodeType, ...] = ()
        else:
            opcode, arg, in_types, out_types = row
        if isinstance(arg, str):
            if arg not in labels:
                raise ValueError(f"Unknown assembly label {arg!r} in {name}.")
            arg = labels[arg]
        instructions.append(
            BytecodeInstruction(
                opcode,
                arg,
                in_types=in_types,
                out_types=out_types,
            )
        )
    return BytecodeProgram(
        instructions=tuple(instructions),
        name=name,
        memory_layout=memory_layout,
    )


def _frame_i32_range(base_address: int, count: int, label_prefix: str) -> tuple[BytecodeMemoryCell, ...]:
    return tuple(
        _frame_cell(base_address + offset, BytecodeType.I32, f"{label_prefix}_{offset}")
        for offset in range(count)
    )


def _repeat_pattern(pattern: tuple[int, ...], length: int) -> tuple[int, ...]:
    if length <= 0:
        raise ValueError("length must be positive.")
    return tuple(pattern[index % len(pattern)] for index in range(length))


def _scaled_sum_values(length: int) -> tuple[int, ...]:
    return _repeat_pattern((4, -1, 9, -5, 3, -2, 8, -4), length)


def _dense_nonzero_count_values(length: int) -> tuple[int, ...]:
    return _repeat_pattern((1, 2, 3, 4, 5), length)


def _low_bin_histogram_values(length: int) -> tuple[int, ...]:
    return _repeat_pattern((0, 1, 2, 3), length)


def sum_i32_buffer_program(
    *,
    input_values: tuple[int, ...] = (7, 0, -3, 5),
    input_base_address: int = 400,
    output_address: int = 404,
    name: str | None = None,
) -> BytecodeProgram:
    rows: list[AssemblyRow] = []
    for offset, value in enumerate(input_values):
        rows.extend(
            (
                (BytecodeOpcode.CONST_I32, value),
                (BytecodeOpcode.STORE_STATIC, input_base_address + offset),
            )
        )
    rows.extend(
        (
            (BytecodeOpcode.CONST_I32, 0),
            (BytecodeOpcode.STORE_STATIC, output_address),
            (BytecodeOpcode.LOAD_STATIC, output_address),
        )
    )
    for offset in range(len(input_values)):
        rows.extend(
            (
                (BytecodeOpcode.LOAD_STATIC, input_base_address + offset),
                (BytecodeOpcode.ADD_I32, None),
            )
        )
    rows.extend(
        (
            (BytecodeOpcode.STORE_STATIC, output_address),
            (BytecodeOpcode.LOAD_STATIC, output_address),
            (BytecodeOpcode.HALT, None),
        )
    )
    memory_layout = _frame_i32_range(input_base_address, len(input_values), "sum_input") + (
        _frame_cell(output_address, BytecodeType.I32, "sum_output"),
    )
    return _assemble_program(
        name=name or "bytecode_sum_i32_buffer_fixed4",
        rows=rows,
        memory_layout=memory_layout,
    )


def count_nonzero_i32_buffer_program(
    *,
    input_values: tuple[int, ...] = (5, 0, -2, 0, 3),
    input_base_address: int = 416,
    output_address: int = 432,
    name: str | None = None,
) -> BytecodeProgram:
    rows: list[AssemblyRow] = []
    for offset, value in enumerate(input_values):
        rows.extend(
            (
                (BytecodeOpcode.CONST_I32, value),
                (BytecodeOpcode.STORE_STATIC, input_base_address + offset),
            )
        )
    rows.extend(
        (
            (BytecodeOpcode.CONST_I32, 0),
            (BytecodeOpcode.STORE_STATIC, output_address),
        )
    )
    for offset in range(len(input_values)):
        increment_label = f"count_nonzero_inc_{offset}"
        continue_label = f"count_nonzero_next_{offset}"
        rows.extend(
            (
                (BytecodeOpcode.LOAD_STATIC, input_base_address + offset),
                (BytecodeOpcode.CONST_I32, 0),
                (BytecodeOpcode.EQ_I32, None),
                (BytecodeOpcode.JZ_ZERO, increment_label),
                (BytecodeOpcode.JMP, continue_label),
                f"{increment_label}:",
                (BytecodeOpcode.LOAD_STATIC, output_address),
                (BytecodeOpcode.CONST_I32, 1),
                (BytecodeOpcode.ADD_I32, None),
                (BytecodeOpcode.STORE_STATIC, output_address),
                f"{continue_label}:",
            )
        )
    rows.extend(
        (
            (BytecodeOpcode.LOAD_STATIC, output_address),
            (BytecodeOpcode.HALT, None),
        )
    )
    memory_layout = _frame_i32_range(input_base_address, len(input_values), "count_input") + (
        _frame_cell(output_address, BytecodeType.I32, "count_nonzero_output"),
    )
    return _assemble_program(
        name=name or "bytecode_count_nonzero_i32_buffer_fixed5",
        rows=rows,
        memory_layout=memory_layout,
    )


def _append_histogram_dispatch(
    rows: list[AssemblyRow],
    *,
    input_address: int,
    bin_base_address: int,
    next_label: str,
    label_prefix: str,
) -> None:
    rows.append((BytecodeOpcode.LOAD_STATIC, input_address))
    for bucket in range(16):
        next_check_label = f"{label_prefix}_next_check_{bucket}"
        rows.extend(
            (
                (BytecodeOpcode.DUP, None),
                (BytecodeOpcode.CONST_I32, bucket),
                (BytecodeOpcode.EQ_I32, None),
                (BytecodeOpcode.JZ_ZERO, next_check_label),
                (BytecodeOpcode.POP, None),
                (BytecodeOpcode.LOAD_STATIC, bin_base_address + bucket),
                (BytecodeOpcode.CONST_I32, 1),
                (BytecodeOpcode.ADD_I32, None),
                (BytecodeOpcode.STORE_STATIC, bin_base_address + bucket),
                (BytecodeOpcode.JMP, next_label),
                f"{next_check_label}:",
            )
        )
    rows.extend(
        (
            (BytecodeOpcode.POP, None),
            (BytecodeOpcode.HALT, None),
        )
    )


def histogram16_u8_program(
    *,
    input_values: tuple[int, ...] = (3, 1, 3, 15),
    input_base_address: int = 448,
    bin_base_address: int = 464,
    name: str | None = None,
) -> BytecodeProgram:
    rows: list[AssemblyRow] = []
    for offset, value in enumerate(input_values):
        rows.extend(
            (
                (BytecodeOpcode.CONST_I32, value),
                (BytecodeOpcode.STORE_STATIC, input_base_address + offset),
            )
        )
    for bucket in range(16):
        rows.extend(
            (
                (BytecodeOpcode.CONST_I32, 0),
                (BytecodeOpcode.STORE_STATIC, bin_base_address + bucket),
            )
        )
    for offset in range(len(input_values)):
        next_label = f"histogram_next_{offset}"
        _append_histogram_dispatch(
            rows,
            input_address=input_base_address + offset,
            bin_base_address=bin_base_address,
            next_label=next_label,
            label_prefix=f"histogram_input_{offset}",
        )
        rows.append(f"{next_label}:")
    rows.append((BytecodeOpcode.HALT, None))
    memory_layout = _frame_i32_range(input_base_address, len(input_values), "histogram_input") + _frame_i32_range(
        bin_base_address,
        16,
        "histogram_bin",
    )
    return _assemble_program(
        name=name or "bytecode_histogram16_u8_fixed4",
        rows=rows,
        memory_layout=memory_layout,
    )


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


def _permute_subroutine_braid_helper_surface(program: BytecodeProgram, *, name: str) -> BytecodeProgram:
    instructions = list(program.instructions)
    instructions[18] = BytecodeInstruction(
        instructions[18].opcode,
        35,
        in_types=instructions[18].in_types,
        out_types=instructions[18].out_types,
    )
    instructions[22] = BytecodeInstruction(
        instructions[22].opcode,
        30,
        in_types=instructions[22].in_types,
        out_types=instructions[22].out_types,
    )
    helper_a = instructions[30:35]
    helper_b = instructions[35:40]
    instructions[30:35] = helper_b
    instructions[35:40] = helper_a
    return BytecodeProgram(
        instructions=tuple(instructions),
        name=name,
        memory_layout=program.memory_layout,
    )


def subroutine_braid_permuted_helpers_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    base_program = subroutine_braid_program(start, base_address=base_address)
    return _permute_subroutine_braid_helper_surface(
        base_program,
        name=f"bytecode_subroutine_braid_permuted_helpers_{start}_a{base_address}",
    )


def subroutine_braid_long_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    base_program = subroutine_braid_program(start, base_address=base_address)
    return BytecodeProgram(
        instructions=base_program.instructions,
        name=f"bytecode_subroutine_braid_long_{start}_a{base_address}",
        memory_layout=base_program.memory_layout,
    )


def subroutine_braid_long_permuted_helpers_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    base_program = subroutine_braid_long_program(start, base_address=base_address)
    return _permute_subroutine_braid_helper_surface(
        base_program,
        name=f"bytecode_subroutine_braid_long_permuted_helpers_{start}_a{base_address}",
    )


def bounded_scalar_flag_loop_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    if start < 0:
        raise ValueError("bounded_scalar_flag_loop_program expects a non-negative start.")
    counter_address = base_address
    flag_address = base_address + 1
    local_address = base_address + 2
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, local_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(
                BytecodeOpcode.STORE_STATIC,
                flag_address,
                in_types=(BytecodeType.FLAG,),
            ),
            BytecodeInstruction(
                BytecodeOpcode.LOAD_STATIC,
                flag_address,
                out_types=(BytecodeType.FLAG,),
            ),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 12),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, local_address),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, local_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, local_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.JMP, 4),
        ),
        name=f"bytecode_bounded_scalar_flag_loop_{start}_a{base_address}",
        memory_layout=(
            _frame_cell(counter_address, BytecodeType.I32, "counter"),
            _frame_cell(flag_address, BytecodeType.FLAG, "done_flag"),
            _frame_cell(local_address, BytecodeType.I32, "local_sum"),
        ),
    )


def bounded_scalar_flag_loop_long_program(start: int, *, base_address: int = 0) -> BytecodeProgram:
    if start < 0:
        raise ValueError("bounded_scalar_flag_loop_long_program expects a non-negative start.")
    counter_address = base_address
    flag_address = base_address + 1
    left_address = base_address + 2
    right_address = base_address + 3
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, start),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 0),
            BytecodeInstruction(BytecodeOpcode.EQ_I32),
            BytecodeInstruction(
                BytecodeOpcode.STORE_STATIC,
                flag_address,
                in_types=(BytecodeType.FLAG,),
            ),
            BytecodeInstruction(
                BytecodeOpcode.LOAD_STATIC,
                flag_address,
                out_types=(BytecodeType.FLAG,),
            ),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 16),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, left_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, right_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.SUB_I32),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.JMP, 6),
        ),
        name=f"bytecode_bounded_scalar_flag_loop_long_{start}_a{base_address}",
        memory_layout=(
            _frame_cell(counter_address, BytecodeType.I32, "counter"),
            _frame_cell(flag_address, BytecodeType.FLAG, "done_flag"),
            _frame_cell(left_address, BytecodeType.I32, "left_local"),
            _frame_cell(right_address, BytecodeType.I32, "right_local"),
        ),
    )


def invalid_bounded_scalar_flag_branch_program(*, base_address: int = 0) -> BytecodeProgram:
    local_address = base_address
    flag_address = base_address + 1
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, local_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, local_address),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 5),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ),
        name=f"invalid_bounded_scalar_flag_branch_a{base_address}",
        memory_layout=(
            _frame_cell(local_address, BytecodeType.I32, "local_slot"),
            _frame_cell(flag_address, BytecodeType.FLAG, "done_flag"),
        ),
    )


def invalid_bounded_scalar_flag_layout_program(*, base_address: int = 0) -> BytecodeProgram:
    local_address = base_address
    flag_address = base_address + 1
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 1),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, local_address),
            BytecodeInstruction(
                BytecodeOpcode.LOAD_STATIC,
                local_address,
                out_types=(BytecodeType.FLAG,),
            ),
            BytecodeInstruction(BytecodeOpcode.JZ_ZERO, 5),
            BytecodeInstruction(BytecodeOpcode.HALT),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ),
        name=f"invalid_bounded_scalar_flag_layout_a{base_address}",
        memory_layout=(
            _frame_cell(local_address, BytecodeType.I32, "local_slot"),
            _frame_cell(flag_address, BytecodeType.FLAG, "done_flag"),
        ),
    )


def invalid_bounded_scalar_heap_escape_program(*, base_address: int = 0) -> BytecodeProgram:
    counter_address = base_address
    spilled_address = base_address + 1
    return BytecodeProgram(
        instructions=(
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 2),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.CONST_I32, 5),
            BytecodeInstruction(BytecodeOpcode.STORE_STATIC, spilled_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, counter_address),
            BytecodeInstruction(BytecodeOpcode.LOAD_STATIC, spilled_address),
            BytecodeInstruction(BytecodeOpcode.ADD_I32),
            BytecodeInstruction(BytecodeOpcode.HALT),
        ),
        name=f"invalid_bounded_scalar_heap_escape_a{base_address}",
        memory_layout=(
            _frame_cell(counter_address, BytecodeType.I32, "counter"),
            _heap_cell(spilled_address, BytecodeType.I32, "spilled_local"),
        ),
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


def bounded_scalar_family_cases() -> tuple[BytecodeCase, ...]:
    return (
        BytecodeCase(
            "bounded_scalar_family",
            "medium_exact_trace",
            256,
            bounded_scalar_flag_loop_program(6, base_address=320),
        ),
        BytecodeCase(
            "bounded_scalar_family",
            "long_exact_final_state",
            768,
            bounded_scalar_flag_loop_long_program(12, base_address=336),
        ),
    )


def r43_bounded_memory_vm_cases() -> tuple[BoundedMemoryVMCase, ...]:
    return (
        BoundedMemoryVMCase(
            family_id="bounded_static_sum_loop",
            description="Bounded static accumulator loop over one fixed-address memory slot.",
            family_role="core",
            comparison_mode="long_exact_final_state",
            max_steps=512,
            program=accumulator_loop_program(12),
        ),
        BoundedMemoryVMCase(
            family_id="bounded_branch_accumulator",
            description="Bounded branch-and-accumulate loop over a fixed static address pair.",
            family_role="core",
            comparison_mode="medium_exact_trace",
            max_steps=512,
            program=alternating_memory_loop_bytecode_program(6, base_address=16),
        ),
        BoundedMemoryVMCase(
            family_id="bounded_memory_reuse_loop",
            description="Bounded memory reuse loop with fixed address checkpoints and replay reads.",
            family_role="core",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=selector_checkpoint_bank_bytecode_program(6, base_address=32),
        ),
        BoundedMemoryVMCase(
            family_id="stack_depth_revisit_loop",
            description="Bounded stack-depth revisit loop with repeated stack/memory braid reads.",
            family_role="core",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=stack_memory_braid_program(8, base_address=64),
        ),
        BoundedMemoryVMCase(
            family_id="single_call_return_accumulator",
            description="Single-layer call/return accumulator executed only after the first four families stay exact.",
            family_role="gated_optional",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=iterated_helper_accumulator_program(20, counter_address=128, accumulator_address=129),
            gated_on_previous_exact=True,
        ),
    )


def r44_restricted_wasm_useful_case_cases() -> tuple[RestrictedWasmKernelCase, ...]:
    return (
        RestrictedWasmKernelCase(
            kernel_id="sum_i32_buffer",
            description="Read-heavy fixed-buffer sum over one bounded static address range.",
            comparison_mode="medium_exact_trace",
            max_steps=256,
            program=sum_i32_buffer_program(),
        ),
        RestrictedWasmKernelCase(
            kernel_id="count_nonzero_i32_buffer",
            description="Fixed-buffer nonzero count with data-dependent branching and unchanged memory surface.",
            comparison_mode="medium_exact_trace",
            max_steps=512,
            program=count_nonzero_i32_buffer_program(),
        ),
        RestrictedWasmKernelCase(
            kernel_id="histogram16_u8",
            description="Fixed 16-bin histogram with repeated latest-write-by-address pressure on bounded bin cells.",
            comparison_mode="long_exact_final_state",
            max_steps=2048,
            program=histogram16_u8_program(),
        ),
    )


def r46_useful_case_surface_generalization_cases() -> tuple[UsefulCaseSurfaceGeneralizationCase, ...]:
    return (
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="sum_i32_buffer",
            variant_id="sum_len6_shifted_base",
            description="Longer fixed-buffer sum with shifted base address and mixed-sign values.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=384,
            program=sum_i32_buffer_program(
                input_values=(4, -1, 9, 0, 3, -2),
                input_base_address=520,
                output_address=532,
                name="bytecode_sum_i32_buffer_len6_a520",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="sum_i32_buffer",
            variant_id="sum_len8_dense_mixed_sign",
            description="Wider fixed-buffer sum with denser mixed-sign values on a new static range.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=512,
            program=sum_i32_buffer_program(
                input_values=(12, -5, 7, -4, 3, 0, 9, -1),
                input_base_address=560,
                output_address=576,
                name="bytecode_sum_i32_buffer_len8_a560",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_sparse_len8_shifted_base",
            description="Sparse nonzero count with low branch-taken density and shifted base range.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "zero_density_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=768,
            program=count_nonzero_i32_buffer_program(
                input_values=(0, 7, 0, -5, 0, 0, 2, 0),
                input_base_address=600,
                output_address=616,
                name="bytecode_count_nonzero_i32_buffer_sparse_len8_a600",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_dense_len7_shifted_base",
            description="Dense nonzero count with near-max branch-taken density on a new static range.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "value_distribution_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=768,
            program=count_nonzero_i32_buffer_program(
                input_values=(1, 2, 3, -1, 4, 5, 6),
                input_base_address=640,
                output_address=656,
                name="bytecode_count_nonzero_i32_buffer_dense_len7_a640",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_mixed_len9_shifted_base",
            description="Longer mixed-density nonzero count with alternating zero runs and later nonzero bursts.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "zero_density_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=1024,
            program=count_nonzero_i32_buffer_program(
                input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
                input_base_address=680,
                output_address=700,
                name="bytecode_count_nonzero_i32_buffer_mixed_len9_a680",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_bimodal_len6_shifted_base",
            description="Bimodal histogram with repeated pressure on bins 0 and 15 only.",
            axis_tags=("buffer_length_shift", "base_address_shift", "histogram_skew_shift"),
            comparison_mode="long_exact_final_state",
            max_steps=3072,
            program=histogram16_u8_program(
                input_values=(0, 15, 0, 15, 15, 0),
                input_base_address=720,
                bin_base_address=736,
                name="bytecode_histogram16_u8_bimodal_len6_a720",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_low_bin_skew_len8",
            description="Low-bin skew histogram with repeated hits concentrated on bins 1 and 2.",
            axis_tags=("buffer_length_shift", "base_address_shift", "histogram_skew_shift"),
            comparison_mode="long_exact_final_state",
            max_steps=4096,
            program=histogram16_u8_program(
                input_values=(1, 1, 1, 2, 2, 2, 2, 2),
                input_base_address=760,
                bin_base_address=776,
                name="bytecode_histogram16_u8_low_bin_skew_len8_a760",
            ),
        ),
        UsefulCaseSurfaceGeneralizationCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_wide_len10_shifted_base",
            description="Longer histogram with wider bin coverage and repeated late-bin revisits.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift", "histogram_skew_shift"),
            comparison_mode="long_exact_final_state",
            max_steps=6144,
            program=histogram16_u8_program(
                input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
                input_base_address=800,
                bin_base_address=816,
                name="bytecode_histogram16_u8_wide_len10_a800",
            ),
        ),
    )


def r47_restricted_frontend_translation_cases() -> tuple[RestrictedFrontendTranslationCase, ...]:
    return (
        RestrictedFrontendTranslationCase(
            kernel_id="sum_i32_buffer",
            variant_id="sum_len6_shifted_base",
            description="Restricted frontend lowers a longer fixed-buffer sum onto the preserved sum kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=384,
            frontend_program=sum_i32_buffer_frontend_program(
                input_values=(4, -1, 9, 0, 3, -2),
                input_base_address=520,
                output_address=532,
                name="frontend_sum_i32_buffer_len6_a520",
            ),
            canonical_program=sum_i32_buffer_program(
                input_values=(4, -1, 9, 0, 3, -2),
                input_base_address=520,
                output_address=532,
                name="bytecode_sum_i32_buffer_len6_a520",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="sum_i32_buffer",
            variant_id="sum_len8_dense_mixed_sign",
            description="Restricted frontend lowers a wider mixed-sign sum onto the preserved sum kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=512,
            frontend_program=sum_i32_buffer_frontend_program(
                input_values=(12, -5, 7, -4, 3, 0, 9, -1),
                input_base_address=560,
                output_address=576,
                name="frontend_sum_i32_buffer_len8_a560",
            ),
            canonical_program=sum_i32_buffer_program(
                input_values=(12, -5, 7, -4, 3, 0, 9, -1),
                input_base_address=560,
                output_address=576,
                name="bytecode_sum_i32_buffer_len8_a560",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_sparse_len8_shifted_base",
            description="Restricted frontend lowers a sparse nonzero count onto the preserved count kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "zero_density_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=768,
            frontend_program=count_nonzero_i32_buffer_frontend_program(
                input_values=(0, 7, 0, -5, 0, 0, 2, 0),
                input_base_address=600,
                output_address=616,
                name="frontend_count_nonzero_i32_buffer_sparse_len8_a600",
            ),
            canonical_program=count_nonzero_i32_buffer_program(
                input_values=(0, 7, 0, -5, 0, 0, 2, 0),
                input_base_address=600,
                output_address=616,
                name="bytecode_count_nonzero_i32_buffer_sparse_len8_a600",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_dense_len7_shifted_base",
            description="Restricted frontend lowers a dense nonzero count onto the preserved count kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "value_distribution_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=768,
            frontend_program=count_nonzero_i32_buffer_frontend_program(
                input_values=(1, 2, 3, -1, 4, 5, 6),
                input_base_address=640,
                output_address=656,
                name="frontend_count_nonzero_i32_buffer_dense_len7_a640",
            ),
            canonical_program=count_nonzero_i32_buffer_program(
                input_values=(1, 2, 3, -1, 4, 5, 6),
                input_base_address=640,
                output_address=656,
                name="bytecode_count_nonzero_i32_buffer_dense_len7_a640",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_mixed_len9_shifted_base",
            description="Restricted frontend lowers a mixed-density nonzero count onto the preserved count kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "zero_density_shift"),
            comparison_mode="medium_exact_trace",
            max_steps=1024,
            frontend_program=count_nonzero_i32_buffer_frontend_program(
                input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
                input_base_address=680,
                output_address=700,
                name="frontend_count_nonzero_i32_buffer_mixed_len9_a680",
            ),
            canonical_program=count_nonzero_i32_buffer_program(
                input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
                input_base_address=680,
                output_address=700,
                name="bytecode_count_nonzero_i32_buffer_mixed_len9_a680",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_bimodal_len6_shifted_base",
            description="Restricted frontend lowers a bimodal histogram onto the preserved 16-bin histogram kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "histogram_skew_shift"),
            comparison_mode="long_exact_final_state",
            max_steps=3072,
            frontend_program=histogram16_u8_frontend_program(
                input_values=(0, 15, 0, 15, 15, 0),
                input_base_address=720,
                bin_base_address=736,
                name="frontend_histogram16_u8_bimodal_len6_a720",
            ),
            canonical_program=histogram16_u8_program(
                input_values=(0, 15, 0, 15, 15, 0),
                input_base_address=720,
                bin_base_address=736,
                name="bytecode_histogram16_u8_bimodal_len6_a720",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_low_bin_skew_len8",
            description="Restricted frontend lowers a low-bin skew histogram onto the preserved 16-bin histogram kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "histogram_skew_shift"),
            comparison_mode="long_exact_final_state",
            max_steps=4096,
            frontend_program=histogram16_u8_frontend_program(
                input_values=(1, 1, 1, 2, 2, 2, 2, 2),
                input_base_address=760,
                bin_base_address=776,
                name="frontend_histogram16_u8_low_bin_skew_len8_a760",
            ),
            canonical_program=histogram16_u8_program(
                input_values=(1, 1, 1, 2, 2, 2, 2, 2),
                input_base_address=760,
                bin_base_address=776,
                name="bytecode_histogram16_u8_low_bin_skew_len8_a760",
            ),
        ),
        RestrictedFrontendTranslationCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_wide_len10_shifted_base",
            description="Restricted frontend lowers a wider histogram onto the preserved 16-bin histogram kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift", "histogram_skew_shift"),
            comparison_mode="long_exact_final_state",
            max_steps=6144,
            frontend_program=histogram16_u8_frontend_program(
                input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
                input_base_address=800,
                bin_base_address=816,
                name="frontend_histogram16_u8_wide_len10_a800",
            ),
            canonical_program=histogram16_u8_program(
                input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
                input_base_address=800,
                bin_base_address=816,
                name="bytecode_histogram16_u8_wide_len10_a800",
            ),
        ),
    )


def r50_restricted_tinyc_lowering_cases() -> tuple[RestrictedTinyCLoweringCase, ...]:
    return (
        RestrictedTinyCLoweringCase(
            kernel_id="sum_i32_buffer",
            variant_id="sum_len6_shifted_base",
            description="Restricted tiny-C lowers a longer fixed-buffer sum onto the preserved sum kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift", "tinyc_lowering_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=384,
            tinyc_program=sum_i32_buffer_tinyc_program(
                input_values=(4, -1, 9, 0, 3, -2),
                input_base_address=520,
                output_address=532,
                name="tinyc_sum_i32_buffer_len6_a520",
            ),
            canonical_program=sum_i32_buffer_program(
                input_values=(4, -1, 9, 0, 3, -2),
                input_base_address=520,
                output_address=532,
                name="bytecode_sum_i32_buffer_len6_a520",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="sum_i32_buffer",
            variant_id="sum_len8_dense_mixed_sign",
            description="Restricted tiny-C lowers a wider mixed-sign sum onto the preserved sum kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift", "tinyc_lowering_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=512,
            tinyc_program=sum_i32_buffer_tinyc_program(
                input_values=(12, -5, 7, -4, 3, 0, 9, -1),
                input_base_address=560,
                output_address=576,
                name="tinyc_sum_i32_buffer_len8_a560",
            ),
            canonical_program=sum_i32_buffer_program(
                input_values=(12, -5, 7, -4, 3, 0, 9, -1),
                input_base_address=560,
                output_address=576,
                name="bytecode_sum_i32_buffer_len8_a560",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_sparse_len8_shifted_base",
            description="Restricted tiny-C lowers a sparse nonzero count onto the preserved count kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "zero_density_shift", "tinyc_lowering_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=768,
            tinyc_program=count_nonzero_i32_buffer_tinyc_program(
                input_values=(0, 7, 0, -5, 0, 0, 2, 0),
                input_base_address=600,
                output_address=616,
                name="tinyc_count_nonzero_i32_buffer_sparse_len8_a600",
            ),
            canonical_program=count_nonzero_i32_buffer_program(
                input_values=(0, 7, 0, -5, 0, 0, 2, 0),
                input_base_address=600,
                output_address=616,
                name="bytecode_count_nonzero_i32_buffer_sparse_len8_a600",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_dense_len7_shifted_base",
            description="Restricted tiny-C lowers a dense nonzero count onto the preserved count kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "value_distribution_shift", "tinyc_lowering_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=768,
            tinyc_program=count_nonzero_i32_buffer_tinyc_program(
                input_values=(1, 2, 3, -1, 4, 5, 6),
                input_base_address=640,
                output_address=656,
                name="tinyc_count_nonzero_i32_buffer_dense_len7_a640",
            ),
            canonical_program=count_nonzero_i32_buffer_program(
                input_values=(1, 2, 3, -1, 4, 5, 6),
                input_base_address=640,
                output_address=656,
                name="bytecode_count_nonzero_i32_buffer_dense_len7_a640",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_mixed_len9_shifted_base",
            description="Restricted tiny-C lowers a mixed-density nonzero count onto the preserved count kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "branch_density_shift", "zero_density_shift", "tinyc_lowering_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=1024,
            tinyc_program=count_nonzero_i32_buffer_tinyc_program(
                input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
                input_base_address=680,
                output_address=700,
                name="tinyc_count_nonzero_i32_buffer_mixed_len9_a680",
            ),
            canonical_program=count_nonzero_i32_buffer_program(
                input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
                input_base_address=680,
                output_address=700,
                name="bytecode_count_nonzero_i32_buffer_mixed_len9_a680",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_bimodal_len6_shifted_base",
            description="Restricted tiny-C lowers a bimodal histogram onto the preserved 16-bin histogram kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "histogram_skew_shift", "tinyc_lowering_gate"),
            comparison_mode="long_exact_final_state",
            max_steps=3072,
            tinyc_program=histogram16_u8_tinyc_program(
                input_values=(0, 15, 0, 15, 15, 0),
                input_base_address=720,
                bin_base_address=736,
                name="tinyc_histogram16_u8_bimodal_len6_a720",
            ),
            canonical_program=histogram16_u8_program(
                input_values=(0, 15, 0, 15, 15, 0),
                input_base_address=720,
                bin_base_address=736,
                name="bytecode_histogram16_u8_bimodal_len6_a720",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_low_bin_skew_len8",
            description="Restricted tiny-C lowers a low-bin skew histogram onto the preserved 16-bin histogram kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "histogram_skew_shift", "tinyc_lowering_gate"),
            comparison_mode="long_exact_final_state",
            max_steps=4096,
            tinyc_program=histogram16_u8_tinyc_program(
                input_values=(1, 1, 1, 2, 2, 2, 2, 2),
                input_base_address=760,
                bin_base_address=776,
                name="tinyc_histogram16_u8_low_bin_skew_len8_a760",
            ),
            canonical_program=histogram16_u8_program(
                input_values=(1, 1, 1, 2, 2, 2, 2, 2),
                input_base_address=760,
                bin_base_address=776,
                name="bytecode_histogram16_u8_low_bin_skew_len8_a760",
            ),
        ),
        RestrictedTinyCLoweringCase(
            kernel_id="histogram16_u8",
            variant_id="histogram_wide_len10_shifted_base",
            description="Restricted tiny-C lowers a wider histogram onto the preserved 16-bin histogram kernel exactly.",
            axis_tags=("buffer_length_shift", "base_address_shift", "value_distribution_shift", "histogram_skew_shift", "tinyc_lowering_gate"),
            comparison_mode="long_exact_final_state",
            max_steps=6144,
            tinyc_program=histogram16_u8_tinyc_program(
                input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
                input_base_address=800,
                bin_base_address=816,
                name="tinyc_histogram16_u8_wide_len10_a800",
            ),
            canonical_program=histogram16_u8_program(
                input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
                input_base_address=800,
                bin_base_address=816,
                name="bytecode_histogram16_u8_wide_len10_a800",
            ),
        ),
    )


def r51_origin_memory_control_surface_sufficiency_cases() -> tuple[MemoryControlSurfaceSufficiencyCase, ...]:
    widened_histogram_program = histogram16_u8_tinyc_program(
        input_values=(15, 3, 7, 3, 15, 2, 3, 2, 0, 7, 9, 2),
        input_base_address=832,
        bin_base_address=864,
        name="tinyc_histogram16_u8_len12_a832",
    )
    return (
        MemoryControlSurfaceSufficiencyCase(
            family_id="latest_write_overwrite_after_gap",
            variant_id="checkpoint_replay_long_start8_shift96",
            description="Checkpointed three-bank replay forces delayed last-write recovery after repeated overwrites and selector gaps.",
            axis_tags=("latest_write", "overwrite_after_gap", "checkpoint_replay", "memory_control_surface"),
            comparison_mode="long_exact_final_state",
            max_steps=4096,
            program=checkpoint_replay_long_program(8, base_address=96),
        ),
        MemoryControlSurfaceSufficiencyCase(
            family_id="stack_relative_read_under_deeper_control",
            variant_id="stack_memory_braid_start7_shift208",
            description="Branchy stack-memory braid exercises stack-relative reads under deeper control and alternating indirect updates.",
            axis_tags=("stack_relative", "deeper_control", "branchy_surface", "memory_control_surface"),
            comparison_mode="long_exact_final_state",
            max_steps=4096,
            program=stack_memory_braid_program(7, base_address=208),
        ),
        MemoryControlSurfaceSufficiencyCase(
            family_id="loop_carried_state",
            variant_id="alternating_memory_loop_start9_shift144",
            description="Alternating memory loop keeps loop-carried state alive across repeated flag-controlled updates and delayed reads.",
            axis_tags=("loop_carried_state", "flag_control", "latest_write", "memory_control_surface"),
            comparison_mode="long_exact_final_state",
            max_steps=3072,
            program=alternating_memory_loop_bytecode_program(9, base_address=144),
        ),
        MemoryControlSurfaceSufficiencyCase(
            family_id="nested_call_return",
            variant_id="call_chain_smoke_nested_two_level",
            description="Two-level nested call/return chain tests return-target reconstruction without hidden call-stack side state.",
            axis_tags=("nested_call_return", "return_target_identity", "control_surface", "memory_control_surface"),
            comparison_mode="medium_exact_trace",
            max_steps=256,
            program=call_chain_smoke_program(),
        ),
        MemoryControlSurfaceSufficiencyCase(
            family_id="bounded_static_memory_lowered_row",
            variant_id="tinyc_histogram_len12_shift832",
            description="Restricted tiny-C histogram row increases bounded static-memory pressure without widening to arbitrary C.",
            axis_tags=("restricted_tinyc", "static_memory", "lowered_row", "memory_control_surface"),
            comparison_mode="long_exact_final_state",
            max_steps=8192,
            program=compile_restricted_tinyc_program(widened_histogram_program),
            tinyc_program=widened_histogram_program,
        ),
    )


def r49_useful_case_numeric_scaling_cases() -> tuple[UsefulCaseNumericScalingCase, ...]:
    return (
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_a_2x",
            kernel_id="sum_i32_buffer",
            variant_id="sum_len16_shift256",
            description="2x sum bucket with longer fixed buffer and +256 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "numeric_precision_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=600,
            program=sum_i32_buffer_program(
                input_values=_scaled_sum_values(16),
                input_base_address=816,
                output_address=848,
                name="bytecode_sum_i32_buffer_len16_a816",
            ),
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_a_2x",
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_len18_dense_shift256",
            description="2x count bucket with dense nonzero branch pressure and +256 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "branch_density_shift", "numeric_precision_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=600,
            program=count_nonzero_i32_buffer_program(
                input_values=_dense_nonzero_count_values(18),
                input_base_address=936,
                output_address=972,
                name="bytecode_count_nonzero_i32_buffer_len18_a936",
            ),
            precision_reference_sampled=True,
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_a_2x",
            kernel_id="histogram16_u8",
            variant_id="histogram_len16_lowbin_shift256",
            description="2x histogram bucket with low-bin skew and +256 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "histogram_low_bin_skew", "numeric_precision_gate"),
            comparison_mode="long_exact_final_state",
            max_steps=600,
            program=histogram16_u8_program(
                input_values=_low_bin_histogram_values(16),
                input_base_address=1056,
                bin_base_address=1088,
                name="bytecode_histogram16_u8_len16_a1056",
            ),
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_b_4x",
            kernel_id="sum_i32_buffer",
            variant_id="sum_len32_shift1024",
            description="4x sum bucket with longer fixed buffer and +1024 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "numeric_precision_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=1600,
            program=sum_i32_buffer_program(
                input_values=_scaled_sum_values(32),
                input_base_address=1584,
                output_address=1648,
                name="bytecode_sum_i32_buffer_len32_a1584",
            ),
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_b_4x",
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_len36_dense_shift1024",
            description="4x count bucket with dense nonzero branch pressure and +1024 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "branch_density_shift", "numeric_precision_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=1600,
            program=count_nonzero_i32_buffer_program(
                input_values=_dense_nonzero_count_values(36),
                input_base_address=1704,
                output_address=1776,
                name="bytecode_count_nonzero_i32_buffer_len36_a1704",
            ),
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_b_4x",
            kernel_id="histogram16_u8",
            variant_id="histogram_len32_lowbin_shift1024",
            description="4x histogram bucket with low-bin skew and +1024 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "histogram_low_bin_skew", "numeric_precision_gate"),
            comparison_mode="long_exact_final_state",
            max_steps=1600,
            program=histogram16_u8_program(
                input_values=_low_bin_histogram_values(32),
                input_base_address=1824,
                bin_base_address=1888,
                name="bytecode_histogram16_u8_len32_a1824",
            ),
            precision_reference_sampled=True,
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_c_8x",
            kernel_id="sum_i32_buffer",
            variant_id="sum_len64_shift4096",
            description="8x sum bucket with longer fixed buffer and +4096 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "numeric_precision_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=4000,
            program=sum_i32_buffer_program(
                input_values=_scaled_sum_values(64),
                input_base_address=4656,
                output_address=4784,
                name="bytecode_sum_i32_buffer_len64_a4656",
            ),
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_c_8x",
            kernel_id="count_nonzero_i32_buffer",
            variant_id="count_len72_dense_shift4096",
            description="8x count bucket with dense nonzero branch pressure and +4096 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "branch_density_shift", "numeric_precision_gate"),
            comparison_mode="medium_exact_trace",
            max_steps=4000,
            program=count_nonzero_i32_buffer_program(
                input_values=_dense_nonzero_count_values(72),
                input_base_address=4776,
                output_address=4920,
                name="bytecode_count_nonzero_i32_buffer_len72_a4776",
            ),
        ),
        UsefulCaseNumericScalingCase(
            bucket_id="bucket_c_8x",
            kernel_id="histogram16_u8",
            variant_id="histogram_len64_lowbin_shift4096",
            description="8x histogram bucket with low-bin skew and +4096 preserved-base shift.",
            axis_tags=("buffer_length_scale", "base_address_scale", "histogram_low_bin_skew", "numeric_precision_gate"),
            comparison_mode="long_exact_final_state",
            max_steps=4000,
            program=histogram16_u8_program(
                input_values=_low_bin_histogram_values(64),
                input_base_address=4896,
                bin_base_address=5024,
                name="bytecode_histogram16_u8_len64_a4896",
            ),
            precision_reference_sampled=True,
        ),
    )


def bounded_scalar_family_negative_programs() -> tuple[BytecodeProgram, ...]:
    return (
        invalid_bounded_scalar_flag_branch_program(base_address=352),
        invalid_bounded_scalar_flag_layout_program(base_address=360),
        invalid_bounded_scalar_heap_escape_program(base_address=368),
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


def r3_d0_exact_execution_stress_cases() -> tuple[StressReferenceCase, ...]:
    return (
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="medium_exact_trace",
            max_steps=256,
            program=helper_checkpoint_braid_program(6, base_address=280, selector_seed=0),
            diagnostic_surface=True,
        ),
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="medium_exact_trace",
            max_steps=512,
            program=subroutine_braid_program(8, base_address=96),
        ),
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=helper_checkpoint_braid_long_program(18, base_address=312, selector_seed=0),
            diagnostic_surface=True,
        ),
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=subroutine_braid_long_program(14, base_address=176),
        ),
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=iterated_helper_accumulator_program(24, counter_address=144, accumulator_address=145),
        ),
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="long_exact_final_state",
            max_steps=1024,
            program=stack_memory_braid_program(10, base_address=112),
            diagnostic_surface=True,
        ),
        StressReferenceCase(
            suite="r3_exact_execution",
            comparison_mode="long_exact_final_state",
            max_steps=1280,
            program=checkpoint_replay_long_program(10, base_address=128),
        ),
    )


def r6_d0_long_horizon_scaling_cases() -> tuple[LongHorizonScalingCase, ...]:
    registry = (
        {
            "family": "indirect_counter_bank",
            "baseline_stage": "M6_typed_bytecode_harness",
            "baseline_start": 12,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 512,
            "diagnostic_surface": False,
            "builder": lambda start: indirect_counter_bank_program(start, counter_address=32, accumulator_address=33),
        },
        {
            "family": "helper_checkpoint_braid",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 6,
            "comparison_mode": "medium_exact_trace",
            "baseline_max_steps": 256,
            "diagnostic_surface": True,
            "builder": lambda start: helper_checkpoint_braid_program(start, base_address=280, selector_seed=0),
        },
        {
            "family": "subroutine_braid",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 8,
            "comparison_mode": "medium_exact_trace",
            "baseline_max_steps": 512,
            "diagnostic_surface": False,
            "builder": lambda start: subroutine_braid_program(start, base_address=96),
        },
        {
            "family": "helper_checkpoint_braid_long",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 18,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024,
            "diagnostic_surface": True,
            "builder": lambda start: helper_checkpoint_braid_long_program(start, base_address=312, selector_seed=0),
        },
        {
            "family": "subroutine_braid_long",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 14,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024,
            "diagnostic_surface": False,
            "builder": lambda start: subroutine_braid_long_program(start, base_address=176),
        },
        {
            "family": "iterated_helper_accumulator",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 24,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024,
            "diagnostic_surface": False,
            "builder": lambda start: iterated_helper_accumulator_program(start, counter_address=144, accumulator_address=145),
        },
        {
            "family": "stack_memory_braid",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 10,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024,
            "diagnostic_surface": True,
            "builder": lambda start: stack_memory_braid_program(start, base_address=112),
        },
        {
            "family": "checkpoint_replay_long",
            "baseline_stage": "R3_d0_exact_execution_stress_gate",
            "baseline_start": 10,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1280,
            "diagnostic_surface": False,
            "builder": lambda start: checkpoint_replay_long_program(start, base_address=128),
        },
    )

    cases: list[LongHorizonScalingCase] = []
    for entry in registry:
        builder = entry["builder"]
        baseline_start = int(entry["baseline_start"])
        baseline_program_name = builder(baseline_start).name
        for multiplier in (2, 4, 8):
            scaled_start = baseline_start * multiplier
            cases.append(
                LongHorizonScalingCase(
                    family=str(entry["family"]),
                    baseline_stage=str(entry["baseline_stage"]),
                    baseline_program_name=baseline_program_name,
                    baseline_start=baseline_start,
                    horizon_multiplier=multiplier,
                    scaled_start=scaled_start,
                    suite="r6_long_horizon_scaling",
                    comparison_mode=str(entry["comparison_mode"]),
                    max_steps=int(entry["baseline_max_steps"]) * multiplier,
                    program=builder(scaled_start),
                    diagnostic_surface=bool(entry["diagnostic_surface"]),
                )
            )
    return tuple(cases)


def r8_d0_retrieval_pressure_cases() -> tuple[RetrievalPressureCase, ...]:
    registry = (
        {
            "family": "helper_checkpoint_braid_long",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 18 * 8,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024 * 8,
            "diagnostic_surface": True,
            "builder": lambda start: helper_checkpoint_braid_long_program(start, base_address=312, selector_seed=0),
        },
        {
            "family": "subroutine_braid_long",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 14 * 8,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024 * 8,
            "diagnostic_surface": False,
            "builder": lambda start: subroutine_braid_long_program(start, base_address=176),
        },
        {
            "family": "iterated_helper_accumulator",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 24 * 8,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024 * 8,
            "diagnostic_surface": False,
            "builder": lambda start: iterated_helper_accumulator_program(
                start,
                counter_address=144,
                accumulator_address=145,
            ),
        },
        {
            "family": "checkpoint_replay_long",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 10 * 8,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1280 * 8,
            "diagnostic_surface": False,
            "builder": lambda start: checkpoint_replay_long_program(start, base_address=128),
        },
    )

    cases: list[RetrievalPressureCase] = []
    for entry in registry:
        builder = entry["builder"]
        baseline_start = int(entry["baseline_start"])
        baseline_program_name = builder(baseline_start).name
        for multiplier in (10,):
            scaled_start = (baseline_start // 8) * multiplier
            cases.append(
                RetrievalPressureCase(
                    family=str(entry["family"]),
                    baseline_stage=str(entry["baseline_stage"]),
                    baseline_program_name=baseline_program_name,
                    baseline_horizon_multiplier=8,
                    baseline_start=baseline_start,
                    retrieval_horizon_multiplier=multiplier,
                    scaled_start=scaled_start,
                    suite="r8_retrieval_pressure",
                    comparison_mode=str(entry["comparison_mode"]),
                    max_steps=(int(entry["baseline_max_steps"]) // 8) * multiplier,
                    program=builder(scaled_start),
                    diagnostic_surface=bool(entry["diagnostic_surface"]),
                )
            )
    return tuple(cases)


def r15_d0_remaining_family_retrieval_pressure_cases() -> tuple[RetrievalPressureCase, ...]:
    registry = (
        {
            "family": "indirect_counter_bank",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 12 * 8,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 512 * 8,
            "diagnostic_surface": False,
            "builder": lambda start: indirect_counter_bank_program(
                start,
                counter_address=32,
                accumulator_address=33,
            ),
        },
        {
            "family": "helper_checkpoint_braid",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 6 * 8,
            "comparison_mode": "medium_exact_trace",
            "baseline_max_steps": 256 * 8,
            "diagnostic_surface": True,
            "builder": lambda start: helper_checkpoint_braid_program(
                start,
                base_address=280,
                selector_seed=0,
            ),
        },
        {
            "family": "subroutine_braid",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 8 * 8,
            "comparison_mode": "medium_exact_trace",
            "baseline_max_steps": 512 * 8,
            "diagnostic_surface": False,
            "builder": lambda start: subroutine_braid_program(start, base_address=96),
        },
        {
            "family": "stack_memory_braid",
            "baseline_stage": "R6_d0_long_horizon_scaling_gate",
            "baseline_start": 10 * 8,
            "comparison_mode": "long_exact_final_state",
            "baseline_max_steps": 1024 * 8,
            "diagnostic_surface": True,
            "builder": lambda start: stack_memory_braid_program(start, base_address=112),
        },
    )

    cases: list[RetrievalPressureCase] = []
    for entry in registry:
        builder = entry["builder"]
        baseline_start = int(entry["baseline_start"])
        baseline_program_name = builder(baseline_start).name
        for multiplier in (10,):
            scaled_start = (baseline_start // 8) * multiplier
            cases.append(
                RetrievalPressureCase(
                    family=str(entry["family"]),
                    baseline_stage=str(entry["baseline_stage"]),
                    baseline_program_name=baseline_program_name,
                    baseline_horizon_multiplier=8,
                    baseline_start=baseline_start,
                    retrieval_horizon_multiplier=multiplier,
                    scaled_start=scaled_start,
                    suite="r15_remaining_family_retrieval_pressure",
                    comparison_mode=str(entry["comparison_mode"]),
                    max_steps=(int(entry["baseline_max_steps"]) // 8) * multiplier,
                    program=builder(scaled_start),
                    diagnostic_surface=bool(entry["diagnostic_surface"]),
                )
            )
    return tuple(cases)
