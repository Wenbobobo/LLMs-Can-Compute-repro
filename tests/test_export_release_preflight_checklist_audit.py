from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_release_preflight_checklist_audit.py"
    spec = importlib.util.spec_from_file_location("export_release_preflight_checklist_audit", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta release_preflight_checklist.md\ngamma release_preflight_checklist.md\n",
        needles=["release_preflight_checklist.md"],
    )

    assert lines == ["beta release_preflight_checklist.md", "gamma release_preflight_checklist.md"]


def test_contains_all_tolerates_wrapped_markdown_lines() -> None:
    module = _load_export_module()

    assert (
        module.contains_all(
            "The gate is healthy but multi-minute rather\nthan discovery-broken.\n",
            ["healthy but multi-minute rather than discovery-broken"],
        )
        is True
    )


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_green_preflight_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["worktree_hygiene_summary"])

    assert summary["current_paper_phase"] == "h52_current_control_with_h43_paper_endpoint"
    assert summary["preflight_scope"] == "outward_release_surface_and_frozen_paper_bundle"
    assert summary["preflight_state"] == "docs_and_audits_green"
    assert summary["release_commit_state"] in {
        "dirty_worktree_release_commit_blocked",
        "clean_worktree_ready_if_other_gates_green",
    }
    assert summary["git_diff_check_state"] in {"clean", "warnings_only"}
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "use this audit together with release_worktree_hygiene_snapshot as the outward-sync control reference while H52 remains the current docs-only mechanism closeout packet, H50 remains the preserved broader-route value closeout, H51 remains the preserved prior mechanism-reentry packet, H43 remains the paper-grade endpoint, R55/R56 remain exact mechanism evidence only, R57 remains negative fast-path comparator evidence, H36 remains the preserved routing/refreeze packet, R42/R43/R44/R45 remain the completed semantic-boundary gate stack, P28 remains publication alignment to landed H43, P27/P37 remain the explicit merge and operational sync packets, and no_active_downstream_runtime_lane remains the current follow-on state"
    )
