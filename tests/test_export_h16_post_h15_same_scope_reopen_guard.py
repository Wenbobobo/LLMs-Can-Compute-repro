from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h16_post_h15_same_scope_reopen_guard.py"
    )
    spec = importlib.util.spec_from_file_location("export_h16_post_h15_same_scope_reopen_guard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_summary_reports_green_h16_scope_lock() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["worktree_summary"])

    assert summary["current_paper_phase"] == "h16_post_h15_same_scope_reopen_active"
    assert summary["active_stage"] == "h16_post_h15_same_scope_reopen_and_scope_lock"
    assert summary["predecessor_refreeze_stage"] == "h15_refreeze_and_decision_sync"
    assert summary["first_science_lane"] == "r15_d0_remaining_family_retrieval_pressure_gate"
    assert summary["lane_order"] == "preserve_h15_then_land_r15_r16_r17_then_activate_comparator_only_r18_then_h17"
    assert summary["latest_landed_lane"] == "r17_d0_full_surface_runtime_bridge"
    assert summary["active_comparator_lane"] == "r18_d0_same_endpoint_runtime_repair_counterfactual"
    assert summary["next_priority_lane"] == "r18_d0_same_endpoint_runtime_repair_counterfactual"
    assert summary["pending_closeout_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
    assert summary["blocked_count"] == 0


def test_export_h16_writes_expected_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    module.OUT_DIR = tmp_path / "H16_post_h15_same_scope_reopen_guard"
    module.main()

    payload = json.loads(
        (module.OUT_DIR / "summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["current_paper_phase"] == "h16_post_h15_same_scope_reopen_active"
    assert summary["active_stage"] == "h16_post_h15_same_scope_reopen_and_scope_lock"
    assert summary["stage_guard_state"] == "same_scope_reopen_guard_green"
    assert summary["latest_landed_lane"] == "r17_d0_full_surface_runtime_bridge"
    assert summary["active_comparator_lane"] == "r18_d0_same_endpoint_runtime_repair_counterfactual"
    assert summary["pending_closeout_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
