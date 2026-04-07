from __future__ import annotations

from bytecode import (
    compile_restricted_tinyc_program,
    count_nonzero_i32_buffer_program,
    count_nonzero_i32_buffer_tinyc_program,
    histogram16_u8_program,
    histogram16_u8_tinyc_program,
    lower_restricted_tinyc_program,
    serialize_restricted_tinyc_program,
    sum_i32_buffer_program,
    sum_i32_buffer_tinyc_program,
    validate_restricted_tinyc_program,
)


def test_sum_restricted_tinyc_compiles_to_canonical_kernel() -> None:
    tinyc = sum_i32_buffer_tinyc_program(
        input_values=(4, -1, 9, 0, 3, -2),
        input_base_address=520,
        output_address=532,
        name="tinyc_sum_i32_buffer_len6_a520",
    )
    compiled = compile_restricted_tinyc_program(tinyc)
    canonical = sum_i32_buffer_program(
        input_values=(4, -1, 9, 0, 3, -2),
        input_base_address=520,
        output_address=532,
        name="tinyc_sum_i32_buffer_len6_a520",
    )

    assert validate_restricted_tinyc_program(tinyc) == (True, None)
    assert lower_restricted_tinyc_program(tinyc).name == tinyc.name
    assert compiled.instructions == canonical.instructions
    assert compiled.memory_layout == canonical.memory_layout


def test_count_nonzero_restricted_tinyc_compiles_to_canonical_kernel() -> None:
    tinyc = count_nonzero_i32_buffer_tinyc_program(
        input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
        input_base_address=680,
        output_address=700,
        name="tinyc_count_nonzero_i32_buffer_mixed_len9_a680",
    )
    compiled = compile_restricted_tinyc_program(tinyc)
    canonical = count_nonzero_i32_buffer_program(
        input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
        input_base_address=680,
        output_address=700,
        name="tinyc_count_nonzero_i32_buffer_mixed_len9_a680",
    )

    assert validate_restricted_tinyc_program(tinyc) == (True, None)
    assert compiled.instructions == canonical.instructions
    assert compiled.memory_layout == canonical.memory_layout


def test_histogram_restricted_tinyc_compiles_to_canonical_kernel() -> None:
    tinyc = histogram16_u8_tinyc_program(
        input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
        input_base_address=800,
        bin_base_address=816,
        name="tinyc_histogram16_u8_wide_len10_a800",
    )
    compiled = compile_restricted_tinyc_program(tinyc)
    canonical = histogram16_u8_program(
        input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
        input_base_address=800,
        bin_base_address=816,
        name="tinyc_histogram16_u8_wide_len10_a800",
    )
    serialized = serialize_restricted_tinyc_program(tinyc)

    assert validate_restricted_tinyc_program(tinyc) == (True, None)
    assert serialized["name"] == "tinyc_histogram16_u8_wide_len10_a800"
    assert compiled.instructions == canonical.instructions
    assert compiled.memory_layout == canonical.memory_layout
