from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h21_refreeze_after_r22_r23.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h21_refreeze_after_r22_r23",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_inputs(*, systems_verdict: str = "systems_materially_positive"):
    return {
        "h21_readme_text": "refreeze stage after `R22` and `R23` with machine-readable packet",
        "h21_status_text": "`supported_here` `unsupported_here` `disconfirmed_here` `F2`",
        "h21_todo_text": "`R22` `R23` `supported_here` `F2` activation conditions",
        "h21_acceptance_text": "`R22` and `R23` machine-readable `F2` trigger matrix",
        "h21_artifact_index_text": "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json results/R22_d0_true_boundary_localization_gate/summary.json",
        "f2_matrix_text": "`F2` is planning-only Do not use `F2` to backdoor a broader Scope-lift thesis is explicitly re-authorized",
        "h19_summary_text": '"decision_state": "same_endpoint_refreeze_complete" "next_priority_lane": "p13_public_surface_sync_and_repo_hygiene"',
        "h19_summary": {"summary": {"decision_state": "same_endpoint_refreeze_complete"}},
        "h20_summary_text": '"lane_order": "h20_then_r22_then_r23_then_h21_then_p13" "current_frozen_stage": "h19_refreeze_and_next_scope_decision"',
        "h20_summary": {"summary": {"current_frozen_stage": "h19_refreeze_and_next_scope_decision", "lane_order": "h20_then_r22_then_r23_then_h21_then_p13"}},
        "r2_summary_text": '"gate_status": "asymptotic_positive_but_end_to_end_not_yet_competitive"',
        "r2_summary": {"gate_summary": {"gate_status": "asymptotic_positive_but_end_to_end_not_yet_competitive"}},
        "e1b_summary_text": '"gate_status_after_patch": "asymptotic_positive_but_end_to_end_not_yet_competitive"',
        "e1b_summary": {"summary": {"gate_status_after_patch": "asymptotic_positive_but_end_to_end_not_yet_competitive"}},
        "r22_summary_text": '"next_priority_lane": "r23_d0_same_endpoint_systems_overturn_gate"',
        "r22_summary": {"summary": {"gate": {"lane_verdict": "no_failure_in_extended_grid", "executed_candidate_count": 102, "planned_candidate_count": 102, "failure_candidate_count": 0}}},
        "r23_summary_text": '"r2_systems_baseline_gate" "e1b_systems_patch" "next_priority_lane": "h21_refreeze_after_r22_r23"',
        "r23_summary": {"summary": {"gate": {"lane_verdict": systems_verdict, "pointer_like_exact_case_count": 25, "total_case_count": 25, "pointer_like_median_ratio_vs_best_reference": 0.8}}},
    }


def test_build_summary_narrows_unsatisfied_conditions_when_r23_is_positive() -> None:
    module = _load_export_module()

    inputs = _fake_inputs()
    checklist_rows = module.build_checklist_rows(**inputs)
    claim_packet = module.build_claim_packet(inputs)
    summary = module.build_summary(checklist_rows, inputs, claim_packet)

    assert summary["active_stage"] == "h21_refreeze_after_r22_r23"
    assert summary["boundary_verdict"] == "extended_grid_no_break_still_not_localized"
    assert summary["systems_verdict"] == "systems_materially_positive"
    assert summary["unsatisfied_frontier_activation_conditions"] == [
        "true_executor_boundary_localization",
        "scope_lift_thesis_explicitly_reauthorized",
    ]
    assert summary["next_priority_lane"] == "p13_public_surface_sync_and_repo_hygiene"


def test_export_h21_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H21_refreeze_after_r22_r23"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["current_paper_phase"] == "h21_refreeze_after_r22_r23_complete"
    assert summary["decision_state"] == "post_r22_r23_refreeze_complete"
    assert summary["next_priority_lane"] == "p13_public_surface_sync_and_repo_hygiene"
    assert summary["blocked_count"] == 0
    assert claim_packet["summary"]["distilled_result"]["r23_lane_verdict"] == "systems_materially_positive"
