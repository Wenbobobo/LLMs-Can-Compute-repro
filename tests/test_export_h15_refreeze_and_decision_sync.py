from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h15_refreeze_and_decision_sync.py"
    spec = importlib.util.spec_from_file_location("export_h15_refreeze_and_decision_sync", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_checklist_rows_accepts_current_direct_refreeze_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)
    assert any(row["item_id"] == "r13_is_not_currently_needed" for row in rows)
    assert any(row["item_id"] == "r14_is_not_currently_justified" for row in rows)


def test_build_summary_reports_direct_refreeze_ready() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["p10_summary"])

    assert summary["decision_state"] == "direct_refreeze_complete"
    assert summary["current_paper_phase"] == "h15_refreeze_and_decision_sync_complete"
    assert summary["active_stage"] == "h15_refreeze_and_decision_sync"
    assert summary["guarded_reopen_stage"] == "h14_core_first_reopen_and_scope_lock"
    assert summary["next_stage"] == "next_full_plan_pending"
    assert summary["r13_decision"] == "not_currently_needed"
    assert summary["r14_decision"] == "not_currently_justified"
    assert summary["blocked_count"] == 0


def test_export_h15_writes_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(
        Path("results/H15_refreeze_and_decision_sync/summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["decision_state"] == "direct_refreeze_complete"
    assert summary["r13_decision"] == "not_currently_needed"
    assert summary["r14_decision"] == "not_currently_justified"
