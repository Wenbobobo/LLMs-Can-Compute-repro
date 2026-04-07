from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r32_d0_family_local_boundary_sharp_zoom.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r32_d0_family_local_boundary_sharp_zoom",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r32_builds_expected_initial_grid() -> None:
    module = _load_export_module()

    admitted_rows = module.r22.load_r19_admitted_runtime_rows()
    templates = module.r22.build_template_registry(admitted_rows)
    branch_plans = module.build_initial_branch_plans()
    branch_specs = module.r22.build_branch_specs(templates, branch_plans)

    lane_counts: dict[str, int] = {}
    for plan in branch_plans:
        lane_counts[plan.lane_class] = lane_counts.get(plan.lane_class, 0) + 1

    assert len(branch_plans) == 30
    assert len(branch_specs) == 60
    assert lane_counts == {
        "candidate_core": 5,
        "unique_address_extension": 10,
        "horizon_extension": 10,
        "checkpoint_depth_extension": 5,
    }
    assert {spec.hot_address_skew for spec in branch_specs} == {"flattened"}
    assert "plus_three" in {spec.checkpoint_depth for spec in branch_specs}


def test_export_r32_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R32_d0_family_local_boundary_sharp_zoom"
    module.OUT_DIR = temp_out_dir

    def fake_measure(spec):
        failing = (
            spec.family == "checkpoint_replay_long"
            and spec.unique_address_target == 36
            and spec.horizon_multiplier == 3.0
            and spec.checkpoint_depth == "plus_two"
            and spec.hot_address_skew == "flattened"
            and spec.seed_id == 0
        )
        exact = not failing
        row = {
            **module.r22.branch_spec_to_row(spec),
            "source_runtime_stage": "r22_d0_true_boundary_localization_gate",
            "authorization_source_stage": "r30_d0_boundary_reauthorization_packet",
            "execution_stage": "r32_d0_family_local_boundary_sharp_zoom",
            "base_runtime_stage": "r19_d0_pointer_like_surface_generalization_gate",
            "program_name": f"fake_{spec.candidate_id}",
            "base_variant_program_name": f"base_{spec.seed_variant}",
            "runtime_seconds": 0.01,
            "ns_per_step": 100.0,
            "exact_trace_match": exact,
            "exact_final_state_match": exact,
            "first_mismatch_step": None if exact else 23,
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
            "hottest_address_share": 0.18,
            "failure_axis_tags": "fake",
        }
        profile = {
            **module.r22.branch_spec_to_row(spec),
            "authorization_source_stage": "r30_d0_boundary_reauthorization_packet",
            "execution_stage": "r32_d0_family_local_boundary_sharp_zoom",
            "program_name": f"fake_{spec.candidate_id}",
            "reference_step_count": 20,
            "memory_operation_count": 14,
            "memory_load_count": 6,
            "memory_store_count": 8,
            "unique_address_count": spec.unique_address_target,
            "hottest_address": 1,
            "hottest_address_loads": 3,
            "hottest_address_stores": 3,
            "hottest_address_share": 0.18,
            "address_rows": [],
        }
        return row, profile

    monkeypatch.setattr(module, "measure_branch_spec", fake_measure)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_payload = json.loads((temp_out_dir / "manifest_rows.json").read_text(encoding="utf-8"))
    fail_payload = json.loads((temp_out_dir / "failure_rows.json").read_text(encoding="utf-8"))
    localized_payload = json.loads((temp_out_dir / "localized_boundary.json").read_text(encoding="utf-8"))

    summary = payload["summary"]
    gate = summary["gate"]

    assert summary["status"] == "r32_family_local_boundary_sharp_zoom_complete"
    assert gate["lane_verdict"] == "first_boundary_failure_localized"
    assert gate["planned_branch_count"] == 31
    assert gate["planned_candidate_count"] == 62
    assert gate["executed_candidate_count"] == 62
    assert gate["failure_candidate_count"] == 1
    assert gate["next_priority_lane"] == "h26_refreeze_after_r32_boundary_sharp_zoom"
    assert len(manifest_payload["rows"]) == 62
    assert len(fail_payload["rows"]) == 1
    assert localized_payload["rows"][0]["supporting_exact_neighbor_count"] >= 1
