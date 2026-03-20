from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h13_post_h12_governance_stage_health.py"
    spec = importlib.util.spec_from_file_location("export_h13_post_h12_governance_stage_health", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta H13_post_h12_governance_stage_health\ngamma H13_post_h12_governance_stage_health\n",
        needles=["H13_post_h12_governance_stage_health"],
    )

    assert lines == ["beta H13_post_h12_governance_stage_health", "gamma H13_post_h12_governance_stage_health"]


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)
    assert any(row["item_id"] == "current_stage_driver_preserves_h13_handoff" for row in rows)


def test_build_summary_reports_preserved_handoff_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["worktree_hygiene_summary"])

    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["active_stage"] == "h15_refreeze_and_decision_sync"
    assert summary["preserved_stage"] == "h13_post_h12_rollover_and_next_stage_staging"
    assert summary["entrypoint_role"] == "preserved_governance_handoff_reference"
    assert summary["stage_health_state"] == "preserved_handoff_green"
    assert summary["release_commit_state"] in {
        "dirty_worktree_release_commit_blocked",
        "clean_worktree_ready_if_other_gates_green",
    }
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "use this summary as the preserved H13/V1 handoff reference while H15 keeps the repo refrozen; keep H14/R11/R12 preserved as the completed reopen packet, keep H10/H11/R8/R9/R10/H12 frozen, consult release_worktree_hygiene_snapshot before any release-facing commit, and do not treat H13/V1 as an active science lane"
    )
