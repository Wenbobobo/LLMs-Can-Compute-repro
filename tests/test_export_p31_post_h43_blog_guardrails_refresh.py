from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p31_post_h43_blog_guardrails_refresh.py"
    spec = importlib.util.spec_from_file_location("export_p31_post_h43_blog_guardrails_refresh", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta P31_post_h43_blog_guardrails_refresh\ngamma P31_post_h43_blog_guardrails_refresh\n",
        needles=["P31_post_h43_blog_guardrails_refresh"],
    )

    assert lines == [
        "beta P31_post_h43_blog_guardrails_refresh",
        "gamma P31_post_h43_blog_guardrails_refresh",
    ]


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_blog_guardrail_refresh_packet() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(inputs)
    summary = module.build_summary(rows)

    assert summary["current_paper_phase"] == "h43_post_r44_useful_case_refreeze_active"
    assert summary["refresh_packet"] == "p31_post_h43_blog_guardrails_refresh"
    assert summary["selected_outcome"] == "blocked_blog_guardrails_refreshed_to_h43"
    assert summary["refreshed_surface_count"] == 20
    assert summary["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert summary["blocked_count"] == 0
