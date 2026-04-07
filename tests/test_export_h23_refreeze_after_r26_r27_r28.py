from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h23_refreeze_after_r26_r27_r28.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h23_refreeze_after_r26_r27_r28",
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
        "h23_readme_text": "Refreeze `R26` `R27` `R28` machine-readable",
        "h23_status_text": "`boundary_verdict` `mechanism_contract_verdict` systems verdict next downstream lane",
        "h23_todo_text": "`R26` `R27` `R28` machine-readable packet",
        "h23_acceptance_text": "machine-readable unsupported claims next downstream lane",
        "h23_artifact_index_text": (
            "results/R26_d0_boundary_localization_execution_gate/summary.json "
            "results/R28_d0_trace_retrieval_contract_audit/summary.json "
            "results/H23_refreeze_after_r26_r27_r28/summary.json"
        ),
        "h23_result_digest_text": "boundary mechanism systems next lane",
        "h21_summary_text": '"active_stage": "h21_refreeze_after_r22_r23" "systems_verdict": "systems_still_mixed"',
        "h21_summary": {
            "summary": {
                "active_stage": "h21_refreeze_after_r22_r23",
                "systems_verdict": "systems_still_mixed",
                "boundary_verdict": "extended_grid_no_break_still_not_localized",
                "next_priority_lane": "p12_manuscript_and_manifest_maintenance",
            }
        },
        "h22_summary_text": (
            '"active_stage": "h22_post_h21_boundary_reopen_and_dual_track_lock" '
            '"active_support_lane": "r28_d0_trace_retrieval_contract_audit"'
        ),
        "h22_summary": {
            "summary": {
                "current_frozen_stage": "h21_refreeze_after_r22_r23",
                "active_runtime_lane": "r26_d0_boundary_localization_execution_gate",
                "active_support_lane": "r28_d0_trace_retrieval_contract_audit",
                "conditional_runtime_lane": "r27_d0_boundary_localization_extension_gate",
            }
        },
        "r26_summary_text": '"source_runtime_stage": "r22_d0_true_boundary_localization_gate"',
        "r26_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "first_boundary_failure_localized",
                    "executed_candidate_count": 22,
                    "planned_candidate_count": 22,
                    "failure_candidate_count": 1,
                }
            }
        },
        "r27_summary_text": '"next_priority_lane": "h23_refreeze_after_r26_r27_r28"',
        "r27_summary": {
            "summary": {
                "gate": {
                    "execution_mode": "skip",
                    "lane_verdict": "skipped_not_triggered",
                    "next_priority_lane": "h23_refreeze_after_r26_r27_r28",
                }
            }
        },
        "r28_summary_text": '"next_priority_lane": "h23_refreeze_after_r26_r27_r28"',
        "r28_summary": {
            "summary": {
                "gate": {
                    "mechanism_contract_verdict": "mechanism_contract_supported_with_partial_control_isolation",
                    "retrieval_bottleneck_verdict": "pointer_like_exact_non_retrieval_dominant",
                    "r23_systems_verdict": "systems_still_mixed",
                    "next_priority_lane": "h23_refreeze_after_r26_r27_r28",
                }
            }
        },
    }


def test_h23_summary_carries_systems_limit_forward() -> None:
    module = _load_export_module()

    inputs = _fake_inputs()
    checklist_rows = module.build_checklist_rows(**inputs)
    claim_packet = module.build_claim_packet(inputs)
    summary = module.build_summary(checklist_rows, inputs, claim_packet)

    assert summary["active_stage"] == "h23_refreeze_after_r26_r27_r28"
    assert summary["boundary_verdict"] == "first_boundary_failure_localized"
    assert summary["mechanism_contract_verdict"] == "mechanism_contract_supported_with_partial_control_isolation"
    assert summary["systems_verdict"] == "systems_still_mixed"
    assert summary["unsatisfied_frontier_activation_conditions"] == [
        "current_scope_systems_story_materially_positive",
        "scope_lift_thesis_explicitly_reauthorized",
    ]
    assert summary["next_priority_lane"] == "p14_public_surface_sync_after_h23"


def test_export_h23_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H23_refreeze_after_r26_r27_r28"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["decision_state"] == "post_r26_r27_r28_refreeze_complete"
    assert summary["next_priority_lane"] == "p14_public_surface_sync_after_h23"
    assert summary["blocked_count"] == 0
    assert claim_packet["summary"]["distilled_result"]["h23_boundary_verdict"] == "first_boundary_failure_localized"
