from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r21_d0_exact_executor_boundary_break_map.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r21_d0_exact_executor_boundary_break_map",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r21_builds_expected_branch_grid() -> None:
    module = _load_export_module()

    admitted_rows = module.load_r19_admitted_runtime_rows()
    templates = module.build_template_registry(admitted_rows)
    branch_specs = module.build_branch_specs(templates)

    assert len(templates) == 4
    assert len(branch_specs) == 96

    branch_ids = {spec.branch_id for spec in branch_specs}
    assert len(branch_ids) == 48

    branch_counts: dict[str, int] = {}
    for spec in branch_specs:
        branch_counts[spec.branch_id] = branch_counts.get(spec.branch_id, 0) + 1
    assert set(branch_counts.values()) == {2}

    target_to_family = {
        template.unique_address_target: template.family for template in templates
    }
    assert target_to_family == {
        6: "subroutine_braid",
        8: "helper_checkpoint_braid",
        12: "checkpoint_replay_long",
        16: "checkpoint_replay_long",
    }

    target_to_padding = {
        spec.unique_address_target: spec.padding_unique_count for spec in branch_specs if spec.seed_id == 0
    }
    assert target_to_padding == {6: 2, 8: 2, 12: 3, 16: 7}


def test_r21_prunes_branch_after_two_failures(monkeypatch) -> None:
    module = _load_export_module()

    monkeypatch.setattr(module, "SEED_IDS", (0, 1, 2))
    admitted_rows = module.load_r19_admitted_runtime_rows()
    templates = module.build_template_registry(admitted_rows)
    branch_specs = [
        spec
        for spec in module.build_branch_specs(templates)
        if spec.branch_id in {"u6_h1p0_cbaseline_kbaseline", "u8_h1p0_cbaseline_kbaseline"}
    ]

    measured: list[str] = []

    def fake_measure(spec):
        measured.append(spec.candidate_id)
        exact = not (
            spec.branch_id == "u6_h1p0_cbaseline_kbaseline" and spec.seed_id in {0, 1}
        )
        row = {
            **module.branch_spec_to_row(spec),
            "branch_id": spec.branch_id,
            "candidate_id": spec.candidate_id,
            "program_name": f"fake_{spec.candidate_id}",
            "exact": exact,
            "first_mismatch_step": None if exact else 5,
            "failure_reason": None if exact else "fake mismatch",
            "failure_class": None if exact else "exactness_mismatch",
            "unique_address_count": spec.unique_address_target,
            "hottest_address_share": 0.25,
        }
        profile = {
            **module.branch_spec_to_row(spec),
            "program_name": f"fake_{spec.candidate_id}",
            "reference_step_count": 10,
            "memory_operation_count": 10,
            "memory_load_count": 4,
            "memory_store_count": 6,
            "unique_address_count": spec.unique_address_target,
            "hottest_address": 1,
            "hottest_address_loads": 2,
            "hottest_address_stores": 2,
            "hottest_address_share": 0.25,
            "address_rows": [],
        }
        return row, profile

    monkeypatch.setattr(module, "measure_branch_spec", fake_measure)

    rows, _profiles, skipped_count = module.execute_boundary_scan(branch_specs)

    assert skipped_count == 1
    assert "u6_h1p0_cbaseline_kbaseline_seed2" not in measured
    assert len([row for row in rows if row["branch_id"] == "u6_h1p0_cbaseline_kbaseline"]) == 2
    assert len([row for row in rows if row["branch_id"] == "u8_h1p0_cbaseline_kbaseline"]) == 3


def test_export_r21_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R21_d0_exact_executor_boundary_break_map"
    module.OUT_DIR = temp_out_dir

    def fake_measure(spec):
        exact = not (
            spec.unique_address_target == 16
            and spec.horizon_multiplier == 2.0
            and spec.checkpoint_depth == "plus_one"
            and spec.hot_address_skew == "flattened"
        )
        row = {
            **module.branch_spec_to_row(spec),
            "source_runtime_stage": "r20_d0_runtime_mechanism_ablation_matrix",
            "base_runtime_stage": "r19_d0_pointer_like_surface_generalization_gate",
            "program_name": f"fake_{spec.candidate_id}",
            "base_variant_program_name": f"base_{spec.seed_variant}",
            "runtime_seconds": 0.01,
            "ns_per_step": 100.0,
            "exact_trace_match": exact,
            "exact_final_state_match": exact,
            "first_mismatch_step": None if exact else 9,
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
            "hottest_address_share": 0.22 if spec.hot_address_skew == "flattened" else 0.41,
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
            "hottest_address_share": 0.22 if spec.hot_address_skew == "flattened" else 0.41,
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

    summary = payload["summary"]
    gate = summary["gate"]

    assert summary["status"] == "r21_boundary_map_complete"
    assert gate["lane_verdict"] == "mixed_boundary_detected"
    assert gate["planned_branch_count"] == 48
    assert gate["planned_candidate_count"] == 96
    assert gate["executed_candidate_count"] == 96
    assert gate["failure_candidate_count"] == 2
    assert gate["next_priority_lane"] == "h19_refreeze_and_next_scope_decision"
    assert len(branch_payload["rows"]) == 48
    assert len(fail_payload["rows"]) == 2
    assert len(first_fail_payload["rows"]) == 1
