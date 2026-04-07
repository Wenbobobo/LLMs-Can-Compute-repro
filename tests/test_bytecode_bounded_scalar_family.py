from __future__ import annotations

from bytecode import (
    BytecodeInterpreter,
    bounded_scalar_flag_loop_long_program,
    bounded_scalar_flag_loop_program,
    invalid_bounded_scalar_flag_branch_program,
    invalid_bounded_scalar_flag_layout_program,
    invalid_bounded_scalar_heap_escape_program,
    normalize_final_state,
    run_spec_program,
    validate_program_contract,
    verify_memory_surfaces,
    verify_program,
)


def test_bounded_scalar_flag_loop_program_is_exact_and_frame_only() -> None:
    program = bounded_scalar_flag_loop_program(6, base_address=320)

    verifier = verify_program(program)
    spec_contract = validate_program_contract(program)
    memory_surface = verify_memory_surfaces(program)
    source_result = BytecodeInterpreter().run(program)
    spec_result = run_spec_program(program)

    assert verifier.passed is True
    assert spec_contract.passed is True
    assert memory_surface.passed is True
    assert normalize_final_state(source_result.final_state) == normalize_final_state(spec_result.final_state)
    assert source_result.final_state.stack == (21,)
    assert source_result.final_state.memory == ((320, 0), (321, 1), (322, 21))


def test_bounded_scalar_flag_loop_long_program_tracks_two_locals() -> None:
    program = bounded_scalar_flag_loop_long_program(12, base_address=336)

    verifier = verify_program(program)
    spec_contract = validate_program_contract(program)
    memory_surface = verify_memory_surfaces(program)
    source_result = BytecodeInterpreter().run(program)

    assert verifier.passed is True
    assert spec_contract.passed is True
    assert memory_surface.passed is True
    assert source_result.final_state.stack == (156,)
    assert source_result.final_state.memory == ((336, 0), (337, 1), (338, 78), (339, 78))


def test_invalid_bounded_scalar_flag_branch_program_is_rejected_by_verifier() -> None:
    program = invalid_bounded_scalar_flag_branch_program(base_address=352)

    verifier = verify_program(program)
    spec_contract = validate_program_contract(program)
    memory_surface = verify_memory_surfaces(program)

    assert verifier.passed is False
    assert verifier.error_class == "type_mismatch"
    assert spec_contract.passed is False
    assert memory_surface.passed is False


def test_invalid_bounded_scalar_flag_layout_program_is_rejected_by_memory_surface() -> None:
    program = invalid_bounded_scalar_flag_layout_program(base_address=360)

    verifier = verify_program(program)
    spec_contract = validate_program_contract(program)
    memory_surface = verify_memory_surfaces(program)

    assert verifier.passed is True
    assert spec_contract.passed is True
    assert memory_surface.passed is False
    assert memory_surface.error_class == "layout_type_mismatch"


def test_invalid_bounded_scalar_heap_escape_program_only_fails_family_scope() -> None:
    program = invalid_bounded_scalar_heap_escape_program(base_address=368)

    verifier = verify_program(program)
    spec_contract = validate_program_contract(program)
    memory_surface = verify_memory_surfaces(program)

    assert verifier.passed is True
    assert spec_contract.passed is True
    assert memory_surface.passed is True
