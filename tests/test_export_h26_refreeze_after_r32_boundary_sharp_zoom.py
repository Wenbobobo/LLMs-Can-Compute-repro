from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h26_refreeze_after_r32_boundary_sharp_zoom.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h26_refreeze_after_r32_boundary_sharp_zoom",
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
        "h26_readme_text": "freeze the outcome of `R32` fixed `D0` endpoint `R33`",
        "h26_status_text": "executed `R32` `R33` `R29` and `F3` remain blocked",
        "h26_todo_text": "machine-readable same-endpoint packet `supported_here` `R33` remains justified next",
        "h26_acceptance_text": "post-`R32` same-endpoint refreeze `R33` `R29` and `F3` stay blocked",
        "h26_artifact_index_text": (
            "results/R32_d0_family_local_boundary_sharp_zoom/summary.json "
            "results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json "
            "R33_d0_non_retrieval_overhead_localization_audit"
        ),
        "h23_summary_text": '"boundary_verdict": "bounded_grid_still_not_localized" "systems_verdict": "systems_still_mixed"',
        "h23_summary": {
            "summary": {
                "boundary_verdict": "bounded_grid_still_not_localized",
                "systems_verdict": "systems_still_mixed",
            }
        },
        "h25_summary_text": (
            '"next_priority_lane": "r32_d0_family_local_boundary_sharp_zoom" '
            '"deferred_audit_lane": "r33_d0_non_retrieval_overhead_localization_audit"'
        ),
        "h25_summary": {
            "summary": {
                "next_priority_lane": "r32_d0_family_local_boundary_sharp_zoom",
                "deferred_audit_lane": "r33_d0_non_retrieval_overhead_localization_audit",
            }
        },
        "r30_summary_text": '"boundary_reauthorization_verdict": "execute_one_more_family_local_zoom"',
        "r30_summary": {
            "summary": {
                "boundary_reauthorization_verdict": "execute_one_more_family_local_zoom",
                "recommended_next_lane": "r32_d0_family_local_boundary_sharp_zoom",
            }
        },
        "r32_summary_text": (
            '"status": "r32_family_local_boundary_sharp_zoom_complete" '
            '"next_priority_lane": "h26_refreeze_after_r32_boundary_sharp_zoom"'
        ),
        "r32_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "grid_extended_still_not_localized",
                    "next_priority_lane": "h26_refreeze_after_r32_boundary_sharp_zoom",
                    "executed_candidate_count": 60,
                    "planned_candidate_count": 60,
                    "failure_candidate_count": 0,
                }
            }
        },
    }


def test_h26_summary_freezes_r32_and_routes_to_r33() -> None:
    module = _load_export_module()

    inputs = _fake_inputs()
    checklist_rows = module.build_checklist_rows(**inputs)
    claim_packet = module.build_claim_packet(inputs)
    summary = module.build_summary(checklist_rows, inputs, claim_packet)

    assert summary["active_stage"] == "h26_refreeze_after_r32_boundary_sharp_zoom"
    assert summary["boundary_verdict"] == "family_local_sharp_zoom_still_not_localized"
    assert summary["next_priority_lane"] == "r33_d0_non_retrieval_overhead_localization_audit"
    assert summary["downstream_routing_decision"] == "preserve_deferred_r33_as_next_lane"
    assert summary["blocked_count"] == 0


def test_export_h26_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H26_refreeze_after_r32_boundary_sharp_zoom"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["decision_state"] == "post_r32_refreeze_complete"
    assert summary["next_priority_lane"] == "r33_d0_non_retrieval_overhead_localization_audit"
    assert summary["recommended_next_action"].startswith("Advance to deferred R33")
    assert claim_packet["summary"]["distilled_result"]["h26_boundary_verdict"] == "family_local_sharp_zoom_still_not_localized"
