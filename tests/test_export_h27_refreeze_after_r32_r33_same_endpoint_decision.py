from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h27_refreeze_after_r32_r33_same_endpoint_decision.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h27_refreeze_after_r32_r33_same_endpoint_decision",
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
        "h27_readme_text": "freeze the post-`R32/R33` same-endpoint state systems story blocked future lanes",
        "h27_status_text": "executed `R33` `R29` `F3` scope",
        "h27_todo_text": "post-`R33` systems state `R29`, `F3`, and `F2`",
        "h27_acceptance_text": "post-`R33` same-endpoint decision packet blocked future lanes does not widen scope",
        "h27_artifact_index_text": (
            "results/R33_d0_non_retrieval_overhead_localization_audit/summary.json "
            "results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json "
            "F2_future_frontier_recheck_activation_matrix"
        ),
        "h26_summary_text": '"next_priority_lane": "r33_d0_non_retrieval_overhead_localization_audit"',
        "h26_summary": {
            "summary": {
                "boundary_verdict": "family_local_sharp_zoom_still_not_localized",
                "next_priority_lane": "r33_d0_non_retrieval_overhead_localization_audit",
            }
        },
        "r33_summary_text": (
            '"status": "r33_non_retrieval_overhead_localization_complete" '
            '"next_priority_lane": "h27_refreeze_after_r32_r33_same_endpoint_decision"'
        ),
        "r33_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "suite_stable_noncompetitive_after_localization",
                    "audit_scope": "full_r23_suite_escalation",
                    "next_priority_lane": "h27_refreeze_after_r32_r33_same_endpoint_decision",
                }
            }
        },
        "r31_summary_text": '"recommended_next_lane": "r33_d0_non_retrieval_overhead_localization_audit"',
        "r31_summary": {
            "summary": {
                "systems_reauthorization_verdict": "audit_non_retrieval_overhead_first",
                "recommended_next_lane": "r33_d0_non_retrieval_overhead_localization_audit",
            }
        },
    }


def test_h27_summary_freezes_post_r33_negative_state() -> None:
    module = _load_export_module()

    inputs = _fake_inputs()
    checklist_rows = module.build_checklist_rows(**inputs)
    claim_packet = module.build_claim_packet(inputs)
    summary = module.build_summary(checklist_rows, inputs, claim_packet)

    assert summary["active_stage"] == "h27_refreeze_after_r32_r33_same_endpoint_decision"
    assert summary["systems_verdict"] == "systems_more_sharply_negative"
    assert summary["next_priority_lane"] == "later_explicit_packet_required_before_new_runtime"
    assert summary["blocked_count"] == 0


def test_export_h27_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H27_refreeze_after_r32_r33_same_endpoint_decision"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", _fake_inputs)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["decision_state"] == "post_r33_same_endpoint_decision_complete"
    assert summary["systems_verdict"] == "systems_more_sharply_negative"
    assert claim_packet["summary"]["distilled_result"]["r29_state"] == "blocked_preserved"
