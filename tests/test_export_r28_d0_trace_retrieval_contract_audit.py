from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r28_d0_trace_retrieval_contract_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r28_d0_trace_retrieval_contract_audit",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_inputs():
    r20_runtime_rows = [
        {
            "strategy_id": "linear_exact",
            "family": "helper_checkpoint_braid",
            "exact": True,
            "ns_per_step": 1000.0,
            "retrieval_share": None,
            "ns_per_read": None,
            "retrieval_seconds": None,
            "non_retrieval_seconds": None,
        },
        {
            "strategy_id": "accelerated",
            "family": "helper_checkpoint_braid",
            "exact": True,
            "ns_per_step": 1200.0,
            "retrieval_share": 0.9,
            "ns_per_read": 400.0,
            "retrieval_seconds": 0.9,
            "non_retrieval_seconds": 0.1,
        },
        {
            "strategy_id": "pointer_like_exact",
            "family": "helper_checkpoint_braid",
            "exact": True,
            "ns_per_step": 100.0,
            "retrieval_share": 0.02,
            "ns_per_read": 10.0,
            "retrieval_seconds": 0.02,
            "non_retrieval_seconds": 0.98,
        },
        {
            "strategy_id": "pointer_like_shuffled",
            "family": "helper_checkpoint_braid",
            "exact": False,
            "ns_per_step": None,
            "retrieval_share": None,
            "ns_per_read": None,
            "retrieval_seconds": 0.03,
            "non_retrieval_seconds": None,
        },
        {
            "strategy_id": "address_oblivious_control",
            "family": "helper_checkpoint_braid",
            "exact": False,
            "ns_per_step": None,
            "retrieval_share": None,
            "ns_per_read": None,
            "retrieval_seconds": 0.03,
            "non_retrieval_seconds": None,
        },
    ]
    r20_mechanism_rows = [
        {
            "strategy_id": "pointer_like_exact",
            "family": "helper_checkpoint_braid",
            "memory_probe_count": 5,
            "stack_probe_count": 7,
            "memory_retrieval_correct_rate": 1.0,
            "memory_address_match_rate": 1.0,
            "stack_retrieval_correct_rate": 1.0,
            "stack_address_match_rate": 1.0,
            "median_correct_step_gap": 1.0,
            "median_step_gap_delta": 0.0,
        },
        {
            "strategy_id": "pointer_like_shuffled",
            "family": "helper_checkpoint_braid",
            "memory_probe_count": 5,
            "stack_probe_count": 7,
            "memory_retrieval_correct_rate": 0.2,
            "memory_address_match_rate": 0.0,
            "stack_retrieval_correct_rate": 0.3,
            "stack_address_match_rate": 0.1,
            "median_correct_step_gap": 1.0,
            "median_step_gap_delta": 1.0,
        },
        {
            "strategy_id": "address_oblivious_control",
            "family": "helper_checkpoint_braid",
            "memory_probe_count": 5,
            "stack_probe_count": 7,
            "memory_retrieval_correct_rate": 0.8,
            "memory_address_match_rate": 0.2,
            "stack_retrieval_correct_rate": 0.9,
            "stack_address_match_rate": 0.6,
            "median_correct_step_gap": 1.0,
            "median_step_gap_delta": 0.0,
        },
    ]
    r23_runtime_rows = [
        {
            "suite": "control_flow",
            "linear_exact_exact": True,
            "linear_exact_ns_per_step": 900.0,
            "linear_exact_retrieval_share": 0.91,
            "linear_exact_ns_per_read": 300.0,
            "linear_exact_dominant_component": "retrieval_total",
            "accelerated_exact": True,
            "accelerated_ns_per_step": 1300.0,
            "accelerated_retrieval_share": 0.95,
            "accelerated_ns_per_read": 500.0,
            "accelerated_dominant_component": "retrieval_total",
            "pointer_like_exact_exact": True,
            "pointer_like_exact_ns_per_step": 120.0,
            "pointer_like_exact_retrieval_share": 0.02,
            "pointer_like_exact_ns_per_read": 12.0,
            "pointer_like_exact_dominant_component": "non_retrieval",
        },
        {
            "suite": "stress_reference",
            "linear_exact_exact": True,
            "linear_exact_ns_per_step": 950.0,
            "linear_exact_retrieval_share": 0.9,
            "linear_exact_ns_per_read": 320.0,
            "linear_exact_dominant_component": "retrieval_total",
            "accelerated_exact": True,
            "accelerated_ns_per_step": 1400.0,
            "accelerated_retrieval_share": 0.96,
            "accelerated_ns_per_read": 520.0,
            "accelerated_dominant_component": "retrieval_total",
            "pointer_like_exact_exact": True,
            "pointer_like_exact_ns_per_step": 110.0,
            "pointer_like_exact_retrieval_share": 0.03,
            "pointer_like_exact_ns_per_read": 11.0,
            "pointer_like_exact_dominant_component": "non_retrieval",
        },
    ]
    return {
        "r19_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "same_endpoint_generalization_confirmed",
                    "admitted_case_count": 8,
                    "heldout_case_count": 16,
                }
            }
        },
        "r19_runtime_rows": {"rows": []},
        "r20_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "mechanism_supported",
                    "negative_controls_with_claim_relevant_failure": [
                        "pointer_like_shuffled",
                        "address_oblivious_control",
                    ],
                }
            }
        },
        "r20_runtime_rows": {"rows": r20_runtime_rows},
        "r20_mechanism_rows": {"rows": r20_mechanism_rows},
        "r23_summary": {
            "summary": {
                "gate": {
                    "exact_designated_paths_all_exact": True,
                    "pointer_like_exact_case_count": 25,
                    "total_case_count": 25,
                    "lane_verdict": "systems_still_mixed",
                    "pointer_like_median_ratio_vs_best_reference": 4.2,
                }
            }
        },
        "r23_runtime_rows": {"rows": r23_runtime_rows},
    }


def test_r28_builds_supported_mechanism_contract_summary() -> None:
    module = _load_export_module()

    inputs = _fake_inputs()
    primitive_rows = module.build_primitive_rows(inputs)
    claim_layer_rows = module.build_claim_layer_rows(inputs, primitive_rows)
    cost_rows = module.build_cost_breakdown_rows(inputs)
    gate = module.assess_gate(
        inputs,
        primitive_rows=primitive_rows,
        claim_layer_rows=claim_layer_rows,
        cost_rows=cost_rows,
    )

    assert primitive_rows[0]["verdict"] == "supported"
    assert primitive_rows[1]["verdict"] == "supported"
    assert primitive_rows[2]["verdict"] == "supported_but_not_directly_isolated"
    assert gate["mechanism_contract_verdict"] == "mechanism_contract_supported_with_partial_control_isolation"
    assert gate["retrieval_bottleneck_verdict"] == "pointer_like_exact_non_retrieval_dominant"


def test_export_r28_writes_expected_artifacts(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R28_d0_trace_retrieval_contract_audit"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    primitive_payload = json.loads((temp_out_dir / "primitive_rows.json").read_text(encoding="utf-8"))
    claim_map = (temp_out_dir / "claim_layer_map.md").read_text(encoding="utf-8")

    assert payload["summary"]["gate"]["mechanism_contract_verdict"] == "mechanism_contract_supported_with_partial_control_isolation"
    assert len(primitive_payload["rows"]) == 3
    assert "| Layer | Claim | Status |" in claim_map
