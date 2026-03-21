from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h19_refreeze_and_next_scope_decision.py"
    )
    spec = importlib.util.spec_from_file_location("export_h19_refreeze_and_next_scope_decision", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_checklist_rows_accepts_current_h19_packet() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)
    assert any(row["item_id"] == "r19_confirms_same_endpoint_generalization_inside_the_declared_envelope" for row in rows)
    assert any(row["item_id"] == "r21_stays_exact_across_the_bounded_grid_without_a_detected_break" for row in rows)


def test_build_summary_reports_same_endpoint_refreeze_complete() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    claim_packet = module.build_claim_packet(inputs)
    summary = module.build_summary(rows, inputs, claim_packet)

    assert summary["current_paper_phase"] == "h19_refreeze_and_next_scope_decision_complete"
    assert summary["active_stage"] == "h19_refreeze_and_next_scope_decision"
    assert summary["prior_frozen_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
    assert summary["guarded_reopen_stage"] == "h18_post_h17_mainline_reopen_and_scope_lock"
    assert summary["decision_state"] == "same_endpoint_refreeze_complete"
    assert summary["runtime_generalization_verdict"] == "same_endpoint_generalization_confirmed"
    assert summary["mechanism_verdict"] == "mechanism_supported"
    assert summary["boundary_verdict"] == "no_boundary_break_detected"
    assert summary["frontier_recheck_decision"] == "conditional_plan_required"
    assert summary["next_priority_lane"] == "p13_public_surface_sync_and_repo_hygiene"
    assert summary["blocked_count"] == 0
    assert summary["disconfirmed_here_count"] == 3


def test_export_h19_writes_expected_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H19_refreeze_and_next_scope_decision"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["decision_state"] == "same_endpoint_refreeze_complete"
    assert summary["future_frontier_review_state"] == "planning_only_conditionally_reviewable"
    assert summary["next_priority_lane"] == "p13_public_surface_sync_and_repo_hygiene"
    assert summary["supported_here_count"] == 4
    assert claim_packet["summary"]["distilled_result"]["r21_executed_candidate_count"] == 96
