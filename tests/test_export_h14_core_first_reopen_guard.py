from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h14_core_first_reopen_guard.py"
    spec = importlib.util.spec_from_file_location("export_h14_core_first_reopen_guard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta H14_core_first_reopen_guard\ngamma H14_core_first_reopen_guard\n",
        needles=["H14_core_first_reopen_guard"],
    )

    assert lines == ["beta H14_core_first_reopen_guard", "gamma H14_core_first_reopen_guard"]


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)
    assert any(row["item_id"] == "preserved_v1_runtime_reference_remains_green" for row in rows)


def test_build_summary_reports_green_reopen_guard() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["worktree_summary"])

    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["active_stage"] == "h15_refreeze_and_decision_sync"
    assert summary["guarded_reopen_stage"] == "h14_core_first_reopen_and_scope_lock"
    assert summary["handoff_stage"] == "h13_post_h12_rollover_and_next_stage_staging_preserved"
    assert summary["stage_guard_state"] == "preserved_core_first_reopen_guard_green"
    assert summary["release_commit_state"] in {
        "dirty_worktree_release_commit_blocked",
        "clean_worktree_ready_if_other_gates_green",
    }
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "use this summary as the preserved H14 packet entrypoint; keep H10/H11/R8/R9/R10/H12 frozen as the latest completed checkpoint, keep H13/V1 preserved as handoff state, preserve R11 and R12 as landed reopen outputs, and treat H15 as the current refrozen stage until a later explicit plan changes it"
    )
