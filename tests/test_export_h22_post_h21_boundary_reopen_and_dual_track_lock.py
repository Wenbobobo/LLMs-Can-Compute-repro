from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h22_post_h21_boundary_reopen_and_dual_track_lock.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h22_post_h21_boundary_reopen_and_dual_track_lock",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_inputs():
    return {
        "h22_readme_text": "dual-track `R26` `R28` `R27` `H23`",
        "h22_status_text": "bounded same-endpoint reopen packet `R26` `R28` `R29` `F3`",
        "h22_todo_text": "`R26` `R27` `R28` machine-readable `H22` control summary",
        "h22_acceptance_text": "`R26` manifest `R27` trigger `R28` widened runtime",
        "h22_artifact_index_text": "R26_d0_boundary_localization_execution_gate R28_d0_trace_retrieval_contract_audit",
        "h22_decision_log_text": "`H21` `R26` `R28` `R27` `P14`",
        "r26_todo_text": "exact `R26` manifest `22`-candidate `first_fail_digest` `R27`",
        "r27_status_text": "Blocked by default confirmation mode extension mode no `plus_three`",
        "r28_todo_text": "claim-layer map `latest_write` `stack` cost-breakdown",
        "h23_todo_text": "`R26` `R27` `R28` machine-readable packet",
        "r29_status_text": "Blocked by default same-endpoint explicit reopen plan",
        "f3_status_text": "Blocked by default planning surface only broader demos or headlines",
        "h21_summary_text": '"active_stage": "h21_refreeze_after_r22_r23" "future_frontier_review_state": "planning_only_conditionally_reviewable"',
        "h21_summary": {
            "summary": {
                "active_stage": "h21_refreeze_after_r22_r23",
                "boundary_verdict": "extended_grid_no_break_still_not_localized",
                "systems_verdict": "systems_still_mixed",
            }
        },
        "r24_matrix_text": "candidate core Stop Rules Predeclared Verdict Vocabulary",
        "r25_thresholds_text": "systems_materially_positive systems_still_mixed Kill Criteria",
    }


def test_build_summary_marks_r26_and_r28_active() -> None:
    module = _load_export_module()

    checklist_rows = module.build_checklist_rows(**_fake_inputs())
    summary = module.build_summary(checklist_rows)

    assert summary["active_stage"] == "h22_post_h21_boundary_reopen_and_dual_track_lock"
    assert summary["active_runtime_lane"] == "r26_d0_boundary_localization_execution_gate"
    assert summary["active_support_lane"] == "r28_d0_trace_retrieval_contract_audit"
    assert summary["conditional_runtime_lane"] == "r27_d0_boundary_localization_extension_gate"
    assert summary["blocked_count"] == 0


def test_export_h22_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H22_post_h21_boundary_reopen_and_dual_track_lock"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["decision_state"] == "post_h21_dual_track_reopen_contract_complete"
    assert summary["next_priority_lane"] == "r26_d0_boundary_localization_execution_gate"
    assert summary["blocked_count"] == 0
