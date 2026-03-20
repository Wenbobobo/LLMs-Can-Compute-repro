from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h11_post_h9_mainline_rollover_guard.py"
    spec = importlib.util.spec_from_file_location("export_h11_post_h9_mainline_rollover_guard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta retrieval-pressure\ngamma retrieval-pressure\n",
        needles=["retrieval-pressure"],
    )

    assert lines == ["beta retrieval-pressure", "gamma retrieval-pressure"]


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)
    assert any(row["item_id"] == "release_preflight_audit_is_green" for row in rows)


def test_build_summary_reports_h11_active_phase() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows)

    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["active_stage"] == "h15_refreeze_and_decision_sync"
    assert summary["lane_order"] == "preserve_h12_then_preserve_h14_then_hold_refrozen_until_next_full_plan"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "keep H10/H11/R8/R9/R10/H12 aligned as the latest completed checkpoint while H15 remains the current refrozen stage, preserve H14/R11/R12 as the completed reopen packet, preserve H13/V1 as handoff state, and use release_preflight_checklist_audit plus release_worktree_hygiene_snapshot as the outward-sync control reference"
    )
