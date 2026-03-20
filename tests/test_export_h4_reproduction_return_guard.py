from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h4_reproduction_return_guard.py"
    spec = importlib.util.spec_from_file_location("export_h4_reproduction_return_guard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta reproduction-mainline return\ngamma reproduction-mainline return\n",
        needles=["reproduction-mainline return"],
    )

    assert lines == ["beta reproduction-mainline return", "gamma reproduction-mainline return"]


def test_build_checklist_rows_accept_current_repo_state_as_preserved_history() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_h4_as_historical_phase() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows)

    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["preserved_baseline_stage"] == "h4_reproduction_mainline_return"
    assert summary["blocked_count"] == 0
