from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r19_d0_pointer_like_surface_generalization_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r19_d0_pointer_like_surface_generalization_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_runtime_row(module, record, *, pointer_like_exact: bool) -> dict[str, object]:
    return {
        "source_lane": record.source_lane,
        "family": record.family,
        "baseline_stage": record.baseline_stage,
        "baseline_program_name": record.baseline_program_name,
        "baseline_horizon_multiplier": record.baseline_horizon_multiplier,
        "baseline_start": record.baseline_start,
        "retrieval_horizon_multiplier": record.retrieval_horizon_multiplier,
        "scaled_start": record.scaled_start,
        "comparison_mode": record.comparison_mode,
        "max_steps": record.max_steps,
        "boundary_family": record.boundary_family,
        "cohort": record.cohort,
        "variant_id": record.variant_id,
        "variant_group": record.variant_group,
        "envelope_rule": record.envelope_rule,
        "program_name": record.program_name,
        "address_signature": record.address_signature,
        "reference_step_count": 100,
        "profile_repeats": module.PROFILE_REPEATS,
        "memory_operation_count": 40,
        "memory_load_count": 28,
        "memory_store_count": 12,
        "unique_address_count": 6,
        "hottest_address": 128,
        "r17_baseline_lowered_ns_per_step": 10.0 if record.cohort == "admitted" else None,
        "r17_baseline_linear_ns_per_step": 100.0 if record.cohort == "admitted" else None,
        "r17_baseline_accelerated_ns_per_step": 80.0 if record.cohort == "admitted" else None,
        "linear_strategy_id": "linear_exact",
        "linear_stack_strategy": "linear",
        "linear_memory_strategy": "linear",
        "linear_median_seconds": 0.001,
        "linear_samples": [0.001],
        "linear_ns_per_step": 100.0,
        "linear_exact_trace_match": True,
        "linear_exact_final_state_match": True,
        "linear_first_mismatch_step": None,
        "linear_failure_reason": None,
        "linear_read_observation_count": 20,
        "linear_memory_read_count": 10,
        "linear_stack_read_count": 10,
        "linear_exact": True,
        "accelerated_strategy_id": "accelerated",
        "accelerated_stack_strategy": "accelerated",
        "accelerated_memory_strategy": "accelerated",
        "accelerated_median_seconds": 0.0008,
        "accelerated_samples": [0.0008],
        "accelerated_ns_per_step": 80.0,
        "accelerated_exact_trace_match": True,
        "accelerated_exact_final_state_match": True,
        "accelerated_first_mismatch_step": None,
        "accelerated_failure_reason": None,
        "accelerated_read_observation_count": 20,
        "accelerated_memory_read_count": 10,
        "accelerated_stack_read_count": 10,
        "accelerated_exact": True,
        "pointer_like_strategy_id": "pointer_like_exact",
        "pointer_like_stack_strategy": "pointer_like_exact",
        "pointer_like_memory_strategy": "pointer_like_exact",
        "pointer_like_median_seconds": 0.00075 if pointer_like_exact else 0.00095,
        "pointer_like_samples": [0.00075 if pointer_like_exact else 0.00095],
        "pointer_like_ns_per_step": 75.0 if pointer_like_exact else 95.0,
        "pointer_like_exact_trace_match": pointer_like_exact,
        "pointer_like_exact_final_state_match": pointer_like_exact,
        "pointer_like_first_mismatch_step": None if pointer_like_exact else 37,
        "pointer_like_failure_reason": None if pointer_like_exact else "synthetic mismatch",
        "pointer_like_read_observation_count": 20,
        "pointer_like_memory_read_count": 10,
        "pointer_like_stack_read_count": 10,
        "pointer_like_exact": pointer_like_exact,
        "accelerated_speedup_vs_linear": 1.25,
        "pointer_like_speedup_vs_linear": 100.0 / (75.0 if pointer_like_exact else 95.0),
        "pointer_like_speedup_vs_current_accelerated": 80.0 / (75.0 if pointer_like_exact else 95.0),
        "pointer_like_speedup_vs_r17_accelerated": None if record.cohort == "heldout" else 80.0 / (75.0 if pointer_like_exact else 95.0),
        "current_accelerated_ratio_vs_r17_accelerated": None if record.cohort == "heldout" else 1.0,
    }


def _fake_address_profile(record) -> dict[str, object]:
    return {
        "source_lane": record.source_lane,
        "family": record.family,
        "cohort": record.cohort,
        "variant_id": record.variant_id,
        "variant_group": record.variant_group,
        "program_name": record.program_name,
        "boundary_family": record.boundary_family,
        "reference_step_count": 100,
        "memory_operation_count": 40,
        "memory_load_count": 28,
        "memory_store_count": 12,
        "unique_address_count": 6,
        "hottest_address": 128,
        "hottest_address_loads": 8,
        "hottest_address_stores": 4,
        "address_rows": [],
    }


def test_r19_builds_two_heldout_rows_per_admitted_family() -> None:
    module = _load_export_module()

    admitted_rows = module.load_admitted_surface_records()
    heldout_rows = module.build_heldout_surface_records(admitted_rows)
    family_rows = module.build_family_summary(admitted_rows + heldout_rows)

    assert len(admitted_rows) == 8
    assert len(heldout_rows) == 16
    assert len(family_rows) == 8
    assert all(row["admitted_count"] == 1 for row in family_rows)
    assert all(row["heldout_count"] == 2 for row in family_rows)
    helper_long = next(row for row in family_rows if row["family"] == "helper_checkpoint_braid_long")
    assert "selector_seed_flip" in helper_long["variant_ids"]


def test_r19_assess_runtime_gate_detects_admitted_regression() -> None:
    module = _load_export_module()
    admitted = module.load_admitted_surface_records()
    heldout = module.build_heldout_surface_records(admitted)
    runtime_rows = [
        _fake_runtime_row(module, record, pointer_like_exact=record.program_name != admitted[0].program_name)
        for record in admitted + heldout
    ]

    cohort_rows = module.build_cohort_runtime_summary(runtime_rows)
    gate = module.assess_runtime_gate(runtime_rows, cohort_rows)

    assert gate["lane_verdict"] == "admitted_surface_regression_detected"
    assert gate["admitted_regression_gate_passed"] is False
    assert gate["next_priority_lane"] == "h19_refreeze_and_next_scope_decision"


def test_export_r19_writes_runtime_summary_with_monkeypatched_execution(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    original_execute_runtime_rows = module.execute_runtime_rows
    temp_out_dir = tmp_path / "R19_d0_pointer_like_surface_generalization_gate"

    def fake_execute_runtime_rows(manifest_rows, _r17_runtime_baselines):
        runtime_rows = []
        address_profiles = []
        for record in manifest_rows:
            pointer_like_exact = not (
                record.cohort == "heldout"
                and record.family == "subroutine_braid_long"
                and record.variant_id == "address_shift_plus_32"
            )
            runtime_rows.append(_fake_runtime_row(module, record, pointer_like_exact=pointer_like_exact))
            address_profiles.append(_fake_address_profile(record))
        return runtime_rows, address_profiles

    module.OUT_DIR = temp_out_dir
    module.execute_runtime_rows = fake_execute_runtime_rows
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.execute_runtime_rows = original_execute_runtime_rows

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]
    runtime_payload = json.loads((temp_out_dir / "runtime_rows.json").read_text(encoding="utf-8"))

    assert summary["status"] == "r19_runtime_gate_complete"
    assert summary["gate"]["lane_verdict"] == "same_endpoint_generalization_not_confirmed"
    assert summary["gate"]["admitted_regression_gate_passed"] is True
    assert summary["gate"]["heldout_pointer_like_exact_count"] == 15
    assert summary["next_priority_lane"] == "r20_d0_runtime_mechanism_ablation_matrix"
    assert len(runtime_payload["rows"]) == 24
