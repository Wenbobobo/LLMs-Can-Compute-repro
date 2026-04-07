from __future__ import annotations

from dataclasses import dataclass
import re

from .ir import BytecodeProgram
from .restricted_frontend import (
    RestrictedFrontendProgram,
    compile_restricted_frontend_program,
    count_nonzero_i32_buffer_frontend_program,
    histogram16_u8_frontend_program,
    serialize_restricted_frontend_program,
    sum_i32_buffer_frontend_program,
)


_FUNC_SIGNATURE_RE = re.compile(r"^(?P<return_type>int|void)\s+(?P<name>[A-Za-z_]\w*)\s*\(\s*\)\s*\{$")
_ARRAY_DECL_RE = re.compile(r"^int\s+(?P<name>[A-Za-z_]\w*)\[(?P<count>\d+)\]\s*=\s*\{(?P<values>[^}]*)\};$")
_SCALAR_ZERO_RE = re.compile(r"^int\s+(?P<name>[A-Za-z_]\w*)\s*=\s*0;$")
_FOR_LOOP_RE = re.compile(r"^for\s*\(\s*int\s+i\s*=\s*0;\s*i\s*<\s*(?P<count>\d+);\s*i\+\+\s*\)\s*\{$")
_CASE_RE = re.compile(
    r"^case\s+(?P<case_value>\d+)\s*:\s*hist\[(?P<target_a>\d+)\]\s*=\s*hist\[(?P<target_b>\d+)\]\s*\+\s*1;\s*break;$"
)


@dataclass(frozen=True, slots=True)
class RestrictedTinyCProgram:
    name: str
    source_text: str
    input_base_address: int
    work_base_address: int


def _normalize_lines(source_text: str) -> list[str]:
    return [line.strip() for line in source_text.strip().splitlines() if line.strip()]


def _parse_int_list(raw_values: str) -> tuple[int, ...]:
    values = [item.strip() for item in raw_values.split(",") if item.strip()]
    return tuple(int(item) for item in values)


def _parse_signature(line: str) -> tuple[str, str]:
    match = _FUNC_SIGNATURE_RE.fullmatch(line)
    if match is None:
        raise ValueError("invalid_function_signature")
    return match.group("return_type"), match.group("name")


def _parse_array_decl(line: str, *, expected_name: str) -> tuple[int, tuple[int, ...]]:
    match = _ARRAY_DECL_RE.fullmatch(line)
    if match is None or match.group("name") != expected_name:
        raise ValueError("invalid_array_declaration")
    values = _parse_int_list(match.group("values"))
    count = int(match.group("count"))
    if count != len(values):
        raise ValueError("array_initializer_length_mismatch")
    return count, values


def _parse_scalar_zero_decl(line: str, *, expected_name: str) -> None:
    match = _SCALAR_ZERO_RE.fullmatch(line)
    if match is None or match.group("name") != expected_name:
        raise ValueError("invalid_zero_scalar_declaration")


def _parse_for_loop(line: str, *, expected_count: int) -> None:
    match = _FOR_LOOP_RE.fullmatch(line)
    if match is None:
        raise ValueError("invalid_for_loop_shape")
    if int(match.group("count")) != expected_count:
        raise ValueError("loop_bound_mismatch")


def _zero_hist_initializer(count: int) -> str:
    return ", ".join("0" for _ in range(count))


def sum_i32_buffer_tinyc_program(
    *,
    input_values: tuple[int, ...] = (7, 0, -3, 5),
    input_base_address: int = 400,
    output_address: int = 404,
    name: str | None = None,
) -> RestrictedTinyCProgram:
    program_name = name or "tinyc_sum_i32_buffer_fixed4"
    source_text = "\n".join(
        [
            f"int {program_name}() {{",
            f"  int input[{len(input_values)}] = {{{', '.join(str(value) for value in input_values)}}};",
            "  int output = 0;",
            f"  for (int i = 0; i < {len(input_values)}; i++) {{",
            "    output = output + input[i];",
            "  }",
            "  return output;",
            "}",
        ]
    )
    return RestrictedTinyCProgram(
        name=program_name,
        source_text=source_text,
        input_base_address=input_base_address,
        work_base_address=output_address,
    )


def count_nonzero_i32_buffer_tinyc_program(
    *,
    input_values: tuple[int, ...] = (5, 0, -2, 0, 3),
    input_base_address: int = 416,
    output_address: int = 432,
    name: str | None = None,
) -> RestrictedTinyCProgram:
    program_name = name or "tinyc_count_nonzero_i32_buffer_fixed5"
    source_text = "\n".join(
        [
            f"int {program_name}() {{",
            f"  int input[{len(input_values)}] = {{{', '.join(str(value) for value in input_values)}}};",
            "  int output = 0;",
            f"  for (int i = 0; i < {len(input_values)}; i++) {{",
            "    if (input[i] != 0) {",
            "      output = output + 1;",
            "    }",
            "  }",
            "  return output;",
            "}",
        ]
    )
    return RestrictedTinyCProgram(
        name=program_name,
        source_text=source_text,
        input_base_address=input_base_address,
        work_base_address=output_address,
    )


def histogram16_u8_tinyc_program(
    *,
    input_values: tuple[int, ...] = (3, 1, 3, 15),
    input_base_address: int = 448,
    bin_base_address: int = 464,
    name: str | None = None,
) -> RestrictedTinyCProgram:
    program_name = name or "tinyc_histogram16_u8_fixed4"
    case_lines = [
        f"      case {bucket}: hist[{bucket}] = hist[{bucket}] + 1; break;"
        for bucket in range(16)
    ]
    source_text = "\n".join(
        [
            f"void {program_name}() {{",
            f"  int input[{len(input_values)}] = {{{', '.join(str(value) for value in input_values)}}};",
            f"  int hist[16] = {{{_zero_hist_initializer(16)}}};",
            f"  for (int i = 0; i < {len(input_values)}; i++) {{",
            "    switch (input[i]) {",
            *case_lines,
            "      default: return;",
            "    }",
            "  }",
            "}",
        ]
    )
    return RestrictedTinyCProgram(
        name=program_name,
        source_text=source_text,
        input_base_address=input_base_address,
        work_base_address=bin_base_address,
    )


def lower_restricted_tinyc_program(program: RestrictedTinyCProgram) -> RestrictedFrontendProgram:
    lines = _normalize_lines(program.source_text)
    if len(lines) < 8:
        raise ValueError("source_too_short")

    return_type, function_name = _parse_signature(lines[0])
    if function_name != program.name:
        raise ValueError("function_name_mismatch")

    input_count, input_values = _parse_array_decl(lines[1], expected_name="input")

    if len(lines) == 8:
        if return_type != "int":
            raise ValueError("sum_return_type_not_admitted")
        _parse_scalar_zero_decl(lines[2], expected_name="output")
        _parse_for_loop(lines[3], expected_count=input_count)
        if lines[4] != "output = output + input[i];":
            raise ValueError("sum_body_not_admitted")
        if lines[5] != "}":
            raise ValueError("sum_loop_not_closed")
        if lines[6] != "return output;":
            raise ValueError("sum_return_not_admitted")
        if lines[7] != "}":
            raise ValueError("sum_function_not_closed")
        return sum_i32_buffer_frontend_program(
            input_values=input_values,
            input_base_address=program.input_base_address,
            output_address=program.work_base_address,
            name=program.name,
        )

    if len(lines) == 9:
        if return_type != "int":
            raise ValueError("count_return_type_not_admitted")
        _parse_scalar_zero_decl(lines[2], expected_name="output")
        _parse_for_loop(lines[3], expected_count=input_count)
        if lines[4] != "if (input[i] != 0) {":
            raise ValueError("count_if_not_admitted")
        if lines[5] != "output = output + 1;":
            raise ValueError("count_increment_not_admitted")
        if lines[6] != "}":
            raise ValueError("count_if_not_closed")
        if lines[7] != "}":
            raise ValueError("count_loop_not_closed")
        if lines[8] != "return output;":
            raise ValueError("count_return_not_admitted")
        raise ValueError("count_function_not_closed")

    if len(lines) == 10:
        if return_type != "int":
            raise ValueError("count_return_type_not_admitted")
        _parse_scalar_zero_decl(lines[2], expected_name="output")
        _parse_for_loop(lines[3], expected_count=input_count)
        if lines[4] != "if (input[i] != 0) {":
            raise ValueError("count_if_not_admitted")
        if lines[5] != "output = output + 1;":
            raise ValueError("count_increment_not_admitted")
        if lines[6] != "}":
            raise ValueError("count_if_not_closed")
        if lines[7] != "}":
            raise ValueError("count_loop_not_closed")
        if lines[8] != "return output;":
            raise ValueError("count_return_not_admitted")
        if lines[9] != "}":
            raise ValueError("count_function_not_closed")
        return count_nonzero_i32_buffer_frontend_program(
            input_values=input_values,
            input_base_address=program.input_base_address,
            output_address=program.work_base_address,
            name=program.name,
        )

    if return_type != "void":
        raise ValueError("histogram_return_type_not_admitted")
    bin_count, bin_values = _parse_array_decl(lines[2], expected_name="hist")
    if bin_count != 16 or any(value != 0 for value in bin_values):
        raise ValueError("histogram_bins_must_start_zeroed")
    _parse_for_loop(lines[3], expected_count=input_count)
    if lines[4] != "switch (input[i]) {":
        raise ValueError("histogram_switch_not_admitted")
    expected_case_start = 5
    expected_case_end = expected_case_start + 16
    if len(lines) != 25:
        raise ValueError("histogram_line_count_not_admitted")
    for bucket, line in enumerate(lines[expected_case_start:expected_case_end]):
        match = _CASE_RE.fullmatch(line)
        if match is None:
            raise ValueError("histogram_case_not_admitted")
        if int(match.group("case_value")) != bucket:
            raise ValueError("histogram_case_sequence_break")
        if int(match.group("target_a")) != bucket or int(match.group("target_b")) != bucket:
            raise ValueError("histogram_case_target_mismatch")
    if lines[21] != "default: return;":
        raise ValueError("histogram_default_not_admitted")
    if lines[22] != "}":
        raise ValueError("histogram_switch_not_closed")
    if lines[23] != "}":
        raise ValueError("histogram_loop_not_closed")
    if lines[24] != "}":
        raise ValueError("histogram_function_not_closed")
    return histogram16_u8_frontend_program(
        input_values=input_values,
        input_base_address=program.input_base_address,
        bin_base_address=program.work_base_address,
        name=program.name,
    )


def compile_restricted_tinyc_program(program: RestrictedTinyCProgram) -> BytecodeProgram:
    return compile_restricted_frontend_program(lower_restricted_tinyc_program(program))


def validate_restricted_tinyc_program(program: RestrictedTinyCProgram) -> tuple[bool, str | None]:
    try:
        lower_restricted_tinyc_program(program)
    except ValueError as exc:
        return False, str(exc)
    return True, None


def serialize_restricted_tinyc_program(program: RestrictedTinyCProgram) -> dict[str, object]:
    lowered_frontend = lower_restricted_tinyc_program(program)
    return {
        "name": program.name,
        "input_base_address": program.input_base_address,
        "work_base_address": program.work_base_address,
        "source_text": program.source_text,
        "source_lines": _normalize_lines(program.source_text),
        "lowered_frontend": serialize_restricted_frontend_program(lowered_frontend),
    }


__all__ = [
    "RestrictedTinyCProgram",
    "compile_restricted_tinyc_program",
    "count_nonzero_i32_buffer_tinyc_program",
    "histogram16_u8_tinyc_program",
    "lower_restricted_tinyc_program",
    "serialize_restricted_tinyc_program",
    "sum_i32_buffer_tinyc_program",
    "validate_restricted_tinyc_program",
]
