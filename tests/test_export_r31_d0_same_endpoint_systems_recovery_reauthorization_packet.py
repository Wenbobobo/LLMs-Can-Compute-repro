from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r31_d0_same_endpoint_systems_recovery_reauthorization_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r31_d0_same_endpoint_systems_recovery_reauthorization_packet",
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
        "r31_readme_text": "does not execute a same-endpoint systems recovery run mixed systems story non-retrieval overhead audit",
        "r31_status_text": "mechanism support distinct from systems competitiveness non-retrieval overhead audit `R29`",
        "r31_todo_text": "dominant bottleneck hypothesis comparator set `R29` stays blocked next lane",
        "r31_acceptance_text": "`hold_r29_blocked` `audit_non_retrieval_overhead_first` `execute_one_bounded_same_endpoint_recovery_probe`",
        "r31_artifact_index_text": "results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json R25_d0_same_endpoint_systems_recovery_hypotheses R33_d0_non_retrieval_overhead_localization_audit",
        "h23_summary_text": '"systems_verdict": "systems_still_mixed" "mechanism_contract_verdict": "mechanism_contract_supported_with_partial_control_isolation"',
        "h23_summary": {
            "summary": {
                "systems_verdict": "systems_still_mixed",
                "mechanism_contract_verdict": "mechanism_contract_supported_with_partial_control_isolation",
            }
        },
        "r23_summary_text": '"lane_verdict": "systems_still_mixed" "pointer_like_median_ratio_vs_best_reference": 4.16',
        "r23_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "systems_still_mixed",
                    "pointer_like_median_ratio_vs_best_reference": 4.16,
                }
            }
        },
        "r28_summary_text": '"retrieval_bottleneck_verdict": "pointer_like_exact_non_retrieval_dominant"',
        "r28_summary": {
            "summary": {
                "gate": {
                    "retrieval_bottleneck_verdict": "pointer_like_exact_non_retrieval_dominant",
                    "mechanism_contract_verdict": "mechanism_contract_supported_with_partial_control_isolation",
                }
            }
        },
        "r25_hypothesis_text": "non_retrieval_overhead_dominates best_reference_comparator_gap_remains_the_blocker retrieval_mechanism_success_does_not_imply_systems_success",
        "r25_thresholds_text": "If a later candidate still shows `non_retrieval` overhead as the dominant component If a later candidate only looks better against imported `accelerated` If the lag remains suite-stable",
    }


def test_r31_summary_routes_systems_work_through_non_retrieval_audit() -> None:
    module = _load_export_module()

    checklist_rows = module.build_checklist_rows(**_fake_inputs())
    summary = module.build_summary(checklist_rows)

    assert summary["systems_reauthorization_verdict"] == "audit_non_retrieval_overhead_first"
    assert summary["dominant_bottleneck_hypothesis"] == "non_retrieval_overhead_dominates"
    assert summary["recommended_next_lane"] == "r33_d0_non_retrieval_overhead_localization_audit"
    assert summary["blocked_future_lane"] == "r29_d0_same_endpoint_systems_recovery_execution_gate"
    assert summary["blocked_count"] == 0


def test_export_r31_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["systems_reauthorization_verdict"] == "audit_non_retrieval_overhead_first"
    assert summary["recommended_next_action"].startswith("Keep R29 blocked")
