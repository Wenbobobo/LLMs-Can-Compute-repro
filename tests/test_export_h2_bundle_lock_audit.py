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
        "alpha\nbeta paper_bundle_status.md\ngamma paper_bundle_status.md\n",
        needles=["paper_bundle_status.md"],
    )

    assert lines == ["beta paper_bundle_status.md", "gamma paper_bundle_status.md"]


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

    assert summary["current_paper_phase"] == "h52_current_control_with_h43_paper_endpoint"
    assert summary["bundle_lock_scope"] == "publication_record_bundle_and_supporting_ledgers"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "keep the H2 bundle-lock audit green while H52 stays explicit as the current docs-only mechanism closeout packet, preserve H50 as the broader-route value closeout, preserve H51 as the prior mechanism-reentry packet, preserve H43 as the paper-grade endpoint, preserve H42/H41 as the prior docs-only packets, preserve H36 as the routing/refreeze packet, keep R42/R43/R44/R45 as the completed semantic-boundary gate stack, keep R55/R56 as exact mechanism evidence, keep R57 as negative fast-path comparator evidence, preserve P27/P28/P37 as operational release-control context, and keep no_active_downstream_runtime_lane as the current follow-on state"
    )
