from __future__ import annotations

from bytecode import (
    compile_restricted_frontend_program,
    count_nonzero_i32_buffer_frontend_program,
    count_nonzero_i32_buffer_program,
    histogram16_u8_frontend_program,
    histogram16_u8_program,
    sum_i32_buffer_frontend_program,
    sum_i32_buffer_program,
    validate_restricted_frontend_program,
)


def test_sum_restricted_frontend_compiles_to_canonical_kernel() -> None:
    frontend = sum_i32_buffer_frontend_program(
        input_values=(4, -1, 9, 0, 3, -2),
        input_base_address=520,
        output_address=532,
        name="frontend_sum_i32_buffer_len6_a520",
    )
    compiled = compile_restricted_frontend_program(frontend)
    canonical = sum_i32_buffer_program(
        input_values=(4, -1, 9, 0, 3, -2),
        input_base_address=520,
        output_address=532,
        name="frontend_sum_i32_buffer_len6_a520",
    )

    assert validate_restricted_frontend_program(frontend) == (True, None)
    assert compiled.instructions == canonical.instructions
    assert compiled.memory_layout == canonical.memory_layout


def test_count_nonzero_restricted_frontend_compiles_to_canonical_kernel() -> None:
    frontend = count_nonzero_i32_buffer_frontend_program(
        input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
        input_base_address=680,
        output_address=700,
        name="frontend_count_nonzero_i32_buffer_mixed_len9_a680",
    )
    compiled = compile_restricted_frontend_program(frontend)
    canonical = count_nonzero_i32_buffer_program(
        input_values=(0, 0, 5, 0, 6, 7, 0, -2, 3),
        input_base_address=680,
        output_address=700,
        name="frontend_count_nonzero_i32_buffer_mixed_len9_a680",
    )

    assert compiled.instructions == canonical.instructions
    assert compiled.memory_layout == canonical.memory_layout


def test_histogram_restricted_frontend_compiles_to_canonical_kernel() -> None:
    frontend = histogram16_u8_frontend_program(
        input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
        input_base_address=800,
        bin_base_address=816,
        name="frontend_histogram16_u8_wide_len10_a800",
    )
    compiled = compile_restricted_frontend_program(frontend)
    canonical = histogram16_u8_program(
        input_values=(0, 3, 15, 7, 3, 0, 12, 15, 7, 7),
        input_base_address=800,
        bin_base_address=816,
        name="frontend_histogram16_u8_wide_len10_a800",
    )

    assert compiled.instructions == canonical.instructions
    assert compiled.memory_layout == canonical.memory_layout
