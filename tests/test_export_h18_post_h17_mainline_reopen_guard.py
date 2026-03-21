from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h18_post_h17_mainline_reopen_guard.py"
    )
    spec = importlib.util.spec_from_file_location("export_h18_post_h17_mainline_reopen_guard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_summary_reports_ready_h18_reopen_plan() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(
        rows,
        inputs["h17_summary"],
        inputs["m7_decision"],
        inputs["worktree_summary"],
        inputs["active_wave_plan_text"],
    )

    assert summary["current_paper_phase"] == "h18_post_h17_mainline_reopen_planned"
    assert summary["current_frozen_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
    assert summary["planned_reopen_stage"] == "h18_post_h17_mainline_reopen_and_scope_lock"
    assert summary["stage_guard_state"] == "planned_same_scope_reopen_ready"
    assert summary["scope_lock_state"] == "tiny_typed_bytecode_d0_locked"
    assert summary["frontier_recheck_state"] == "conditional_plan_required"
    assert summary["frontend_widening_authorized"] is False
    assert summary["lane_order"] == "h18_then_r19_then_r20_then_r21_then_h19_then_p13"
    assert summary["next_priority_lane"] == "h19_refreeze_and_next_scope_decision"
    assert summary["blocked_count"] == 0


def test_export_h18_writes_expected_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H18_post_h17_mainline_reopen_guard"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["current_paper_phase"] == "h18_post_h17_mainline_reopen_planned"
    assert summary["current_frozen_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
    assert summary["planned_reopen_stage"] == "h18_post_h17_mainline_reopen_and_scope_lock"
    assert summary["stage_guard_state"] == "planned_same_scope_reopen_ready"
    assert summary["next_priority_lane"] == "h19_refreeze_and_next_scope_decision"
    assert summary["frontend_widening_authorized"] is False
