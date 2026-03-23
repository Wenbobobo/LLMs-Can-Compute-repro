from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_p34_post_h43_live_surface_wording_guardrail.py"
    )
    spec = importlib.util.spec_from_file_location("export_p34_post_h43_live_surface_wording_guardrail", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_find_blocked_lines_allows_negated_whole_current_endpoint() -> None:
    module = _load_export_module()

    hits = module.find_blocked_lines(
        "The preserved first D0 compiled boundary is earlier support rather than the whole current endpoint.\n"
    )

    assert hits == []


def test_find_blocked_lines_blocks_affirmative_current_compiled_endpoint() -> None:
    module = _load_export_module()

    hits = module.find_blocked_lines("The current compiled endpoint remains D0.\n")

    assert hits == ["The current compiled endpoint remains D0."]


def test_find_blocked_lines_does_not_flag_following_line_after_negated_wrap() -> None:
    module = _load_export_module()

    hits = module.find_blocked_lines(
        "The preserved first D0 compiled boundary is earlier support rather than the\n"
        "whole current endpoint.\n"
        "The blog preserves the current blocked claims explicitly.\n"
    )

    assert hits == []


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    guarded_surface_rows = module.build_guarded_surface_rows(inputs)
    rows = module.build_checklist_rows(inputs, guarded_surface_rows)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_live_surface_guardrail_packet() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    guarded_surface_rows = module.build_guarded_surface_rows(inputs)
    checklist_rows = module.build_checklist_rows(inputs, guarded_surface_rows)
    snapshot_rows = module.build_snapshot(inputs, guarded_surface_rows)
    summary = module.build_summary(checklist_rows, snapshot_rows, guarded_surface_rows)

    assert summary["current_paper_phase"] == "h43_post_r44_useful_case_refreeze_active"
    assert summary["current_low_priority_wave"] == "p31_post_h43_blog_guardrails_refresh"
    assert summary["refresh_packet"] == "p34_post_h43_live_surface_wording_guardrail"
    assert summary["selected_outcome"] == "live_surface_wording_guardrail_landed"
    assert summary["guarded_surface_count"] == len(guarded_surface_rows)
    assert summary["clean_guarded_surface_count"] == len(guarded_surface_rows)
    assert summary["blocked_count"] == 0
