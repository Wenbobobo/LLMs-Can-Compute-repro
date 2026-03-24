from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p5_public_surface_sync.py"
    spec = importlib.util.spec_from_file_location("export_p5_public_surface_sync", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta release_summary_draft.md\ngamma release_summary_draft.md\n",
        needles=["release_summary_draft.md"],
    )

    assert lines == ["beta release_summary_draft.md", "gamma release_summary_draft.md"]


def test_contains_all_tolerates_wrapped_markdown_lines() -> None:
    module = _load_export_module()

    assert (
        module.contains_all(
            "The remaining work is sentence-level\npolish and local figure/table callout cleanup.\n",
            ["sentence-level polish", "callout cleanup"],
        )
        is True
    )


def test_build_sync_checklist_accepts_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_sync_checklist(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_current_polish_phase() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_sync_checklist(**inputs)
    summary = module.build_summary(rows)

    assert summary["current_paper_phase"] == "h52_current_control_with_h43_paper_endpoint"
    assert summary["internal_driver_phase"] == "h52_post_r55_r56_r57_origin_mechanism_decision_packet_active"
    assert summary["release_summary_role"] == "approved_downstream_short_update_source"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "keep the outward-facing surface aligned while recording H52 as the current docs-only mechanism closeout packet, H50 as the preserved broader-route value closeout, H51 as the preserved prior mechanism-reentry packet, H43 as the paper-grade endpoint, R55/R56 as exact mechanism evidence, R57 as negative fast-path comparator evidence, P37 as the current low-priority operational/docs wave, P28 as the completed publication/control sync packet, P27 as the completed explicit merge packet with merge_executed = false, H42/H41 as preserved prior docs-only packets, H36 as the preserved routing/refreeze packet, and no_active_downstream_runtime_lane as the current follow-on state"
    )
