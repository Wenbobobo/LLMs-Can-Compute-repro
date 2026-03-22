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

    assert summary["current_paper_phase"] == "h25_refreeze_after_r30_r31_decision_packet_active_h23_frozen"
    assert summary["internal_driver_phase"] == "h27_refreeze_after_r32_r33_same_endpoint_decision_active"
    assert summary["release_summary_role"] == "approved_downstream_short_update_source"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "keep the outward-facing H25/H23 public surface aligned while treating H27 as the current internal driver, H26 as the current same-endpoint boundary packet, R33 as the completed bounded systems-audit lane, R30 and R31 as the landed reauthorization pair for the finished R32/H26/R33/H27 wave, H22/R26/R28/R27 as the completed bounded reopen packet, H21 as the preserved pre-reopen control, H19 as the earlier same-endpoint refreeze, H17 as the preserved prior same-scope refreeze, H15 as the prior refreeze decision, and H13/V1 plus H8/R6/R7/H9 and H10/H11/R8/R9/R10/H12 as preserved baselines"
    )
