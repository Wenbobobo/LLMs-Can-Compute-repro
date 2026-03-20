from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h2_bundle_lock_audit.py"
    spec = importlib.util.spec_from_file_location("export_h2_bundle_lock_audit", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta paper_package_plan.md\ngamma paper_package_plan.md\n",
        needles=["paper_package_plan.md"],
    )

    assert lines == ["beta paper_package_plan.md", "gamma paper_package_plan.md"]


def test_contains_all_tolerates_wrapped_markdown_lines() -> None:
    module = _load_export_module()

    assert (
        module.contains_all(
            "The next lane keeps the post-`P7`\nstabilization package narrow.\n",
            ["post-`P7` stabilization package", "keeps the post-`P7` stabilization package narrow"],
        )
        is True
    )


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_zero_blocked_items() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows)

    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["bundle_lock_scope"] == "publication_record_bundle_and_supporting_ledgers"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "keep the H2 bundle-lock audit green while H15 stays aligned as the current refrozen stage, H14/R11/R12 remains the completed reopen packet, H13/V1 remains preserved handoff state, H10/H11/R8/R9/R10/H12 remains the latest completed checkpoint, and H8/R6/R7/H9 plus H6/R3/R4/(inactive R5)/H7 remain preserved baselines"
    )
