from __future__ import annotations

from model import HELDOUT_KERNEL_ID, evaluate_r48_dual_mode_useful_case


def test_r48_dual_mode_useful_case_stays_exact_on_explicit_heldout_family() -> None:
    contract_programs, mode_evaluations = evaluate_r48_dual_mode_useful_case()

    assert len(contract_programs) == 8
    assert {program.kernel_id for program in contract_programs} == {
        "sum_i32_buffer",
        "count_nonzero_i32_buffer",
        "histogram16_u8",
    }

    mode_by_id = {mode.mode_id: mode for mode in mode_evaluations}
    assert mode_by_id["compiled_weight_executor"].evaluation.exact_trace_accuracy == 1.0
    assert mode_by_id["compiled_weight_executor"].evaluation.exact_final_state_accuracy == 1.0
    assert mode_by_id["trainable_2d_executor"].fit_result is not None
    assert mode_by_id["trainable_2d_executor"].fit_result.train_sample_accuracy == 1.0
    assert mode_by_id["trainable_2d_executor"].fit_result.train_exact_program_accuracy == 1.0
    assert mode_by_id["trainable_2d_executor"].heldout_kernel_ids == (HELDOUT_KERNEL_ID,)

    heldout_rows = [
        outcome
        for program, outcome in zip(contract_programs, mode_by_id["trainable_2d_executor"].evaluation.outcomes, strict=True)
        if program.kernel_id == HELDOUT_KERNEL_ID
    ]
    assert len(heldout_rows) == 3
    assert all(outcome.exact_trace_match and outcome.exact_final_state_match for outcome in heldout_rows)
