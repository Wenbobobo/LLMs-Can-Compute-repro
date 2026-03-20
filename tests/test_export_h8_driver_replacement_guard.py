from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h8_driver_replacement_guard.py"
    spec = importlib.util.spec_from_file_location("export_h8_driver_replacement_guard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta h8 driver\ngamma h8 driver\n",
        needles=["h8 driver"],
    )

    assert lines == ["beta h8 driver", "gamma h8 driver"]


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_h8_active_phase() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows)

    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "preserve the completed H8/R6/R7/H9 packet as the direct baseline while H15 keeps H14/R11/R12 preserved as the completed reopen packet, H10/H11/R8/R9/R10/H12 as the latest completed checkpoint on the same fixed D0 scope, and H13/V1 as preserved handoff state"
    )
