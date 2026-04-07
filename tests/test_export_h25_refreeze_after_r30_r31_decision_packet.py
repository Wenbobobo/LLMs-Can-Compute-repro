from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h25_refreeze_after_r30_r31_decision_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h25_refreeze_after_r30_r31_decision_packet",
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
        "h25_readme_text": "does not replace `H23` as the frozen scientific evidence state `R29` and `F3` one primary next science lane and one deferred audit lane",
        "h25_status_text": "`H23` remains the current frozen scientific state `R32` `R33` `R29` and `F3` remain blocked",
        "h25_todo_text": "`R30` and `R31` `supported_here`, `unsupported_here`, and `disconfirmed_here` `R29` or `F3`",
        "h25_acceptance_text": "machine-readable post-`H23` decision packet `H23` remains the frozen scientific state `next_priority_lane`",
        "h25_artifact_index_text": "results/H25_refreeze_after_r30_r31_decision_packet/summary.json R32_d0_family_local_boundary_sharp_zoom R33_d0_non_retrieval_overhead_localization_audit",
        "h25_result_digest_text": "boundary reauthorization verdict systems reauthorization verdict `H23` remains the frozen scientific state",
        "h23_summary_text": '"boundary_verdict": "bounded_grid_still_not_localized" "systems_verdict": "systems_still_mixed" "next_priority_lane": "p14_public_surface_sync_after_h23"',
        "h23_summary": {
            "summary": {
                "boundary_verdict": "bounded_grid_still_not_localized",
                "systems_verdict": "systems_still_mixed",
            }
        },
        "r30_summary_text": '"boundary_reauthorization_verdict": "execute_one_more_family_local_zoom"',
        "r30_summary": {
            "summary": {
                "boundary_reauthorization_verdict": "execute_one_more_family_local_zoom",
                "recommended_next_lane": "r32_d0_family_local_boundary_sharp_zoom",
            }
        },
        "r31_summary_text": '"systems_reauthorization_verdict": "audit_non_retrieval_overhead_first"',
        "r31_summary": {
            "summary": {
                "systems_reauthorization_verdict": "audit_non_retrieval_overhead_first",
                "recommended_next_lane": "r33_d0_non_retrieval_overhead_localization_audit",
            }
        },
    }


def test_h25_summary_freezes_the_post_h23_decision_packet() -> None:
    module = _load_export_module()

    inputs = _fake_inputs()
    checklist_rows = module.build_checklist_rows(**inputs)
    claim_packet = module.build_claim_packet()
    summary = module.build_summary(checklist_rows, claim_packet, inputs)

    assert summary["active_stage"] == "h25_refreeze_after_r30_r31_decision_packet"
    assert summary["current_frozen_stage"] == "h23_refreeze_after_r26_r27_r28"
    assert summary["next_priority_lane"] == "r32_d0_family_local_boundary_sharp_zoom"
    assert summary["deferred_audit_lane"] == "r33_d0_non_retrieval_overhead_localization_audit"
    assert summary["blocked_count"] == 0


def test_export_h25_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H25_refreeze_after_r30_r31_decision_packet"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["decision_state"] == "post_h23_reauthorization_packet_complete"
    assert summary["recommended_next_action"].startswith("Execute R32 only")
