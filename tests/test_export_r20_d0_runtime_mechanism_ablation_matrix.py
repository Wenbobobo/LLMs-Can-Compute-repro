from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r20_d0_runtime_mechanism_ablation_matrix.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r20_d0_runtime_mechanism_ablation_matrix",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r20_builds_one_heldout_focus_row_per_family() -> None:
    module = _load_export_module()

    runtime_rows = module.load_r19_runtime_rows()
    sample_rows = module.build_sample_set(runtime_rows)

    admitted_rows = [row for row in sample_rows if row["cohort"] == "admitted"]
    heldout_rows = [row for row in sample_rows if row["cohort"] == "heldout"]

    assert len(sample_rows) == 16
    assert len(admitted_rows) == 8
    assert len(heldout_rows) == 8
    assert len({row["family"] for row in heldout_rows}) == 8

    by_family: dict[str, list[dict[str, object]]] = {}
    for row in runtime_rows:
        if row["cohort"] == "heldout" and row["pointer_like_exact"]:
            by_family.setdefault(str(row["family"]), []).append(row)

    for row in heldout_rows:
        family_rows = by_family[str(row["family"])]
        best_speedup = min(item["pointer_like_speedup_vs_current_accelerated"] for item in family_rows)
        assert row["pointer_like_speedup_vs_current_accelerated"] == best_speedup


def test_r20_assesses_mechanism_supported_verdict() -> None:
    module = _load_export_module()

    gate = module.assess_mechanism_gate(
        [
            {
                "strategy_id": "linear_exact",
                "exact_case_count": 16,
                "claim_relevant_failure": False,
            },
            {
                "strategy_id": "accelerated",
                "exact_case_count": 16,
                "claim_relevant_failure": False,
            },
            {
                "strategy_id": "pointer_like_exact",
                "exact_case_count": 16,
                "claim_relevant_failure": False,
                "median_speedup_vs_imported_accelerated": 10.0,
            },
            {
                "strategy_id": "pointer_like_shuffled",
                "exact_case_count": 3,
                "claim_relevant_failure": True,
            },
            {
                "strategy_id": "address_oblivious_control",
                "exact_case_count": 0,
                "claim_relevant_failure": True,
            },
        ],
        total_case_count=16,
    )

    assert gate["lane_verdict"] == "mechanism_supported"
    assert gate["pointer_like_exact_gate_passed"] is True
    assert gate["negative_controls_with_claim_relevant_failure"] == [
        "pointer_like_shuffled",
        "address_oblivious_control",
    ]
    assert gate["next_priority_lane"] == "r21_d0_exact_executor_boundary_break_map"


def test_export_r20_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R20_d0_runtime_mechanism_ablation_matrix"
    module.OUT_DIR = temp_out_dir

    strategy_meta = {
        "pointer_like_exact": ("target_mechanism", "must_stay_exact", True, True, True),
        "pointer_like_shuffled": ("negative_control", "should_break_speed_or_exactness", False, False, False),
        "address_oblivious_control": ("negative_control", "should_break_speed_or_exactness", False, False, False),
    }

    def fake_execute(sample_rows):
        runtime_rows = []
        probe_rows = []
        for sample_row in sample_rows:
            for strategy_id, (control_class, expected_behavior, exact, retrieval_correct, address_match) in strategy_meta.items():
                runtime_rows.append(
                    {
                        "source_runtime_stage": "r20_d0_runtime_mechanism_ablation_matrix",
                        "family": sample_row["family"],
                        "cohort": sample_row["cohort"],
                        "variant_id": sample_row["variant_id"],
                        "variant_group": sample_row["variant_group"],
                        "program_name": sample_row["program_name"],
                        "selection_bucket": sample_row["selection_bucket"],
                        "selection_reason": sample_row["selection_reason"],
                        "comparison_mode": sample_row["comparison_mode"],
                        "max_steps": sample_row["max_steps"],
                        "boundary_family": sample_row["boundary_family"],
                        "memory_operation_count": sample_row["memory_operation_count"],
                        "unique_address_count": sample_row["unique_address_count"],
                        "hottest_address": sample_row["hottest_address"],
                        "strategy_id": strategy_id,
                        "control_class": control_class,
                        "implementation_state": "implemented",
                        "runtime_mode": "measured_r20",
                        "expected_behavior": expected_behavior,
                        "profile_repeats": 1,
                        "median_seconds": 0.01,
                        "samples": [0.01],
                        "ns_per_step": 100.0 if strategy_id == "pointer_like_exact" else 140.0,
                        "exact_trace_match": exact,
                        "exact_final_state_match": exact,
                        "first_mismatch_step": None if exact else 3,
                        "failure_reason": None if exact else "fake mismatch",
                        "read_observation_count": 2,
                        "memory_read_count": 1,
                        "stack_read_count": 1,
                        "exact": exact,
                        "retrieval_seconds": 0.005,
                        "non_retrieval_seconds": 0.005,
                        "retrieval_share": 0.5,
                        "ns_per_read": 2_500_000.0,
                    }
                )
                probe_rows.extend(
                    [
                        {
                            "strategy_id": strategy_id,
                            "family": sample_row["family"],
                            "cohort": sample_row["cohort"],
                            "variant_id": sample_row["variant_id"],
                            "variant_group": sample_row["variant_group"],
                            "program_name": sample_row["program_name"],
                            "selection_bucket": sample_row["selection_bucket"],
                            "comparison_mode": sample_row["comparison_mode"],
                            "boundary_family": sample_row["boundary_family"],
                            "step": 0,
                            "space": "memory",
                            "query_address": 1,
                            "selected_address": 1 if address_match else 2,
                            "linear_value": 7,
                            "accelerated_value": 7,
                            "pointer_value": 7,
                            "chosen_value": 7 if retrieval_correct else 9,
                            "retrieval_correct": retrieval_correct,
                            "address_match": address_match,
                            "hottest_address": sample_row["hottest_address"],
                            "hottest_address_hit": address_match,
                            "selected_candidate_step": 0,
                            "correct_candidate_step": 0,
                            "selected_step_gap": 0,
                            "correct_step_gap": 0,
                            "step_gap_delta": 0,
                            "selected_candidate_is_default": False,
                            "correct_candidate_is_default": False,
                            "control_note": "fake",
                        },
                        {
                            "strategy_id": strategy_id,
                            "family": sample_row["family"],
                            "cohort": sample_row["cohort"],
                            "variant_id": sample_row["variant_id"],
                            "variant_group": sample_row["variant_group"],
                            "program_name": sample_row["program_name"],
                            "selection_bucket": sample_row["selection_bucket"],
                            "comparison_mode": sample_row["comparison_mode"],
                            "boundary_family": sample_row["boundary_family"],
                            "step": 1,
                            "space": "stack",
                            "query_address": 0,
                            "selected_address": 0 if address_match else 1,
                            "linear_value": 3,
                            "accelerated_value": 3,
                            "pointer_value": 3,
                            "chosen_value": 3 if retrieval_correct else 5,
                            "retrieval_correct": retrieval_correct,
                            "address_match": address_match,
                            "hottest_address": sample_row["hottest_address"],
                            "hottest_address_hit": address_match,
                            "selected_candidate_step": 1,
                            "correct_candidate_step": 1,
                            "selected_step_gap": 0,
                            "correct_step_gap": 0,
                            "step_gap_delta": 0,
                            "selected_candidate_is_default": False,
                            "correct_candidate_is_default": False,
                            "control_note": "fake",
                        },
                    ]
                )
        return runtime_rows, probe_rows

    monkeypatch.setattr(module, "execute_mechanism_rows", fake_execute)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    runtime_payload = json.loads((temp_out_dir / "runtime_matrix_rows.json").read_text(encoding="utf-8"))
    strategy_payload = json.loads((temp_out_dir / "strategy_summary.json").read_text(encoding="utf-8"))

    summary = payload["summary"]
    gate = summary["gate"]

    assert summary["status"] == "r20_runtime_ablation_complete"
    assert summary["selected_case_count"] == 16
    assert gate["lane_verdict"] == "mechanism_supported"
    assert gate["pointer_like_exact_case_count"] == 16
    assert gate["next_priority_lane"] == "r21_d0_exact_executor_boundary_break_map"
    assert len(runtime_payload["rows"]) == 80
    assert len(strategy_payload["rows"]) == 5
    assert not (temp_out_dir / "probe_read_rows.json").exists()
