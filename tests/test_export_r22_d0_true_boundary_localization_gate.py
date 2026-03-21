from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r22_d0_true_boundary_localization_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r22_d0_true_boundary_localization_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r22_builds_expected_branch_grid() -> None:
    module = _load_export_module()

    admitted_rows = module.load_r19_admitted_runtime_rows()
    templates = module.build_template_registry(admitted_rows)
    branch_plans = module.build_branch_plans()
    branch_specs = module.build_branch_specs(templates, branch_plans)

    assert len(branch_plans) == 51
    assert len(branch_specs) == 102

    branch_ids = {spec.branch_id for spec in branch_specs}
    assert len(branch_ids) == 51

    branch_counts: dict[str, int] = {}
    for spec in branch_specs:
        branch_counts[spec.branch_id] = branch_counts.get(spec.branch_id, 0) + 1
    assert set(branch_counts.values()) == {2}

    plan_counts: dict[str, int] = {}
    for plan in branch_plans:
        plan_counts[plan.lane_class] = plan_counts.get(plan.lane_class, 0) + 1
    assert plan_counts == {"continuity_anchor": 3, "extended_probe": 48}

    assert {spec.checkpoint_depth for spec in branch_specs} == {"plus_one", "plus_two"}
    assert {
        spec.target_wrapper_call_depth for spec in branch_specs if spec.checkpoint_depth == "plus_two"
    } == {2}


def test_export_r22_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R22_d0_true_boundary_localization_gate"
    module.OUT_DIR = temp_out_dir

    def fake_measure(spec):
        failing = (
            spec.family == "checkpoint_replay_long"
            and spec.unique_address_target == 32
            and spec.horizon_multiplier == 3.0
            and spec.checkpoint_depth == "plus_two"
            and spec.hot_address_skew == "flattened"
            and spec.seed_id == 0
        )
        exact = not failing
        row = {
            **module.branch_spec_to_row(spec),
            "source_runtime_stage": "r21_d0_exact_executor_boundary_break_map",
            "base_runtime_stage": "r19_d0_pointer_like_surface_generalization_gate",
            "program_name": f"fake_{spec.candidate_id}",
            "base_variant_program_name": f"base_{spec.seed_variant}",
            "runtime_seconds": 0.01,
            "ns_per_step": 100.0,
            "exact_trace_match": exact,
            "exact_final_state_match": exact,
            "first_mismatch_step": None if exact else 13,
            "failure_reason": None if exact else "fake mismatch",
            "failure_class": None if exact else "exactness_mismatch",
            "exact": exact,
            "read_observation_count": 8,
            "memory_read_count": 4,
            "stack_read_count": 4,
            "reference_step_count": 20,
            "memory_operation_count": 14,
            "memory_load_count": 6,
            "memory_store_count": 8,
            "unique_address_count": spec.unique_address_target,
            "hottest_address": 1,
            "hottest_address_share": 0.18 if spec.hot_address_skew == "flattened" else 0.35,
            "failure_axis_tags": "fake",
        }
        profile = {
            **module.branch_spec_to_row(spec),
            "program_name": f"fake_{spec.candidate_id}",
            "reference_step_count": 20,
            "memory_operation_count": 14,
            "memory_load_count": 6,
            "memory_store_count": 8,
            "unique_address_count": spec.unique_address_target,
            "hottest_address": 1,
            "hottest_address_loads": 3,
            "hottest_address_stores": 3,
            "hottest_address_share": 0.18 if spec.hot_address_skew == "flattened" else 0.35,
            "address_rows": [],
        }
        return row, profile

    monkeypatch.setattr(module, "measure_branch_spec", fake_measure)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    branch_payload = json.loads((temp_out_dir / "branch_summary.json").read_text(encoding="utf-8"))
    fail_payload = json.loads((temp_out_dir / "failure_rows.json").read_text(encoding="utf-8"))
    first_fail_payload = json.loads((temp_out_dir / "first_fail_digest.json").read_text(encoding="utf-8"))
    localized_payload = json.loads((temp_out_dir / "localized_boundary.json").read_text(encoding="utf-8"))
    recheck_payload = json.loads((temp_out_dir / "failure_rechecks.json").read_text(encoding="utf-8"))

    summary = payload["summary"]
    gate = summary["gate"]

    assert summary["status"] == "r22_boundary_localization_complete"
    assert gate["lane_verdict"] == "first_boundary_failure_localized"
    assert gate["planned_branch_count"] == 51
    assert gate["planned_candidate_count"] == 102
    assert gate["executed_candidate_count"] == 102
    assert gate["failure_candidate_count"] == 1
    assert gate["next_priority_lane"] == "r23_d0_same_endpoint_systems_overturn_gate"
    assert len(branch_payload["rows"]) == 51
    assert len(fail_payload["rows"]) == 1
    assert len(first_fail_payload["rows"]) == 1
    assert localized_payload["rows"][0]["supporting_exact_neighbor_count"] >= 1
    assert len(recheck_payload["rows"]) == module.FIRST_FAIL_RECHECK_REPEATS
    assert all(row["reproduced"] for row in recheck_payload["rows"])


def test_r22_resource_limited_verdict() -> None:
    module = _load_export_module()

    gate = module.assess_boundary_gate(
        [],
        [],
        [],
        pruned_count=0,
        skipped_rows=[{"skip_class": "resource_limit"}],
        first_fail_digest_rows=[],
        localized_boundary_rows=[],
        failure_rechecks=[],
    )

    assert gate["lane_verdict"] == "resource_limited_without_failure"
