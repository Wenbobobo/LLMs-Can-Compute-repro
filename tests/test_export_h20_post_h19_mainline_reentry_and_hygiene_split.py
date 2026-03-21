from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h20_post_h19_mainline_reentry_and_hygiene_split.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h20_post_h19_mainline_reentry_and_hygiene_split",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_checklist_rows_accepts_current_h20_reentry_packet() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)
    assert any(row["item_id"] == "saved_plan_and_active_wave_describe_post_h19_reentry" for row in rows)
    assert any(row["item_id"] == "r22_r23_and_h21_scaffolds_are_actionable" for row in rows)


def test_build_summary_reports_dirty_tree_isolation_required() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["h19_summary"], inputs["worktree_summary"])

    assert summary["current_paper_phase"] == "h20_post_h19_mainline_reentry_active"
    assert summary["current_frozen_stage"] == "h19_refreeze_and_next_scope_decision"
    assert summary["reentry_state"] == "dirty_tree_isolation_required_before_next_science_commits"
    assert summary["scope_lock_state"] == "tiny_typed_bytecode_d0_locked"
    assert summary["h19_decision_state"] == "same_endpoint_refreeze_complete"
    assert summary["future_frontier_review_state"] == "planning_only_conditionally_reviewable"
    assert summary["commit_split_state"] == "pending_in_dirty_tree"
    assert summary["lane_order"] == "h20_then_r22_then_r23_then_h21_then_p13"
    assert summary["next_priority_lanes"] == [
        "r22_d0_true_boundary_localization_gate",
        "r23_d0_same_endpoint_systems_overturn_gate",
    ]
    assert summary["release_commit_state"] == "dirty_worktree_release_commit_blocked"
    assert summary["blocked_count"] == 0


def test_export_h20_writes_expected_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H20_post_h19_mainline_reentry_and_hygiene_split"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["current_paper_phase"] == "h20_post_h19_mainline_reentry_active"
    assert summary["reentry_state"] == "dirty_tree_isolation_required_before_next_science_commits"
    assert summary["next_priority_lanes"] == [
        "r22_d0_true_boundary_localization_gate",
        "r23_d0_same_endpoint_systems_overturn_gate",
    ]
    assert summary["blocked_count"] == 0
