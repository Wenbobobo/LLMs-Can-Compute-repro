from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r23_d0_same_endpoint_systems_overturn_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r23_d0_same_endpoint_systems_overturn_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_positive_cases_match_r2_systems_universe() -> None:
    module = _load_export_module()

    cases = module.positive_cases()

    assert len(cases) == 25
    assert sum(case.suite == "stress_reference" for case in cases) == 3
    assert all(case.comparison_mode != "verifier_negative" for case in cases)


def test_assess_gate_reports_materially_positive_when_pointer_like_is_exact_and_competitive() -> None:
    module = _load_export_module()

    rows = [
        {
            "verification_passed": True,
            "linear_exact_exact": True,
            "accelerated_exact": True,
            "pointer_like_exact_exact": True,
            "pointer_like_exact_ratio_vs_best_reference": 0.8,
            "accelerated_ratio_vs_best_reference": 1.6,
            "lowered_ratio_vs_best_reference": 1.8,
            "pointer_like_speedup_vs_accelerated": 2.0,
            "pointer_like_speedup_vs_lowered": 5.0,
        },
        {
            "verification_passed": True,
            "linear_exact_exact": True,
            "accelerated_exact": True,
            "pointer_like_exact_exact": True,
            "pointer_like_exact_ratio_vs_best_reference": 0.9,
            "accelerated_ratio_vs_best_reference": 1.7,
            "lowered_ratio_vs_best_reference": 1.9,
            "pointer_like_speedup_vs_accelerated": 2.1,
            "pointer_like_speedup_vs_lowered": 5.2,
        },
    ]
    r2_summary = {
        "gate_summary": {
            "geometry_positive": True,
            "lowered_ratio_vs_best_reference": 1.8242260729438198,
        }
    }

    gate = module.assess_gate(rows, r2_summary=r2_summary)

    assert gate["lane_verdict"] == "systems_materially_positive"
    assert gate["exact_designated_paths_all_exact"] is True
    assert gate["pointer_like_median_ratio_vs_best_reference"] < 1.0
    assert gate["next_priority_lane"] == "h21_refreeze_after_r22_r23"


def test_export_r23_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R23_d0_same_endpoint_systems_overturn_gate"
    module.OUT_DIR = temp_out_dir

    class FakeCase:
        def __init__(self, suite: str, name: str) -> None:
            self.suite = suite
            self.comparison_mode = "medium_exact_trace"
            self.max_steps = 32
            self.program = type("Program", (), {"name": name})()

    def fake_positive_cases():
        return [FakeCase("smoke", "case_a"), FakeCase("loops", "case_b")]

    def fake_measure_case(case):
        base = 80.0 if case.program.name == "case_a" else 90.0
        return {
            "program_name": case.program.name,
            "suite": case.suite,
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "verification_passed": True,
            "verification_seconds": 0.001,
            "lowering_seconds": 0.001,
            "profile_step_count": 16,
            "bytecode_median_seconds": 0.002,
            "bytecode_samples": [0.002],
            "bytecode_ns_per_step": base,
            "bytecode_error": None,
            "lowered_median_seconds": 0.01,
            "lowered_samples": [0.01],
            "lowered_ns_per_step": 180.0,
            "lowered_error": None,
            "spec_median_seconds": 0.0025,
            "spec_samples": [0.0025],
            "spec_ns_per_step": base + 10.0,
            "spec_error": None,
            "best_reference_path": "bytecode_reference",
            "best_reference_ns_per_step": base,
            "bytecode_exact": True,
            "lowered_exact": True,
            "spec_exact": True,
            "lowered_ratio_vs_best_reference": 180.0 / base,
            "linear_exact_median_seconds": 0.004,
            "linear_exact_samples": [0.004],
            "linear_exact_ns_per_step": 120.0,
            "linear_exact_exact": True,
            "linear_exact_exact_trace_match": True,
            "linear_exact_exact_final_state_match": True,
            "linear_exact_first_mismatch_step": None,
            "linear_exact_failure_reason": None,
            "linear_exact_read_observation_count": 8,
            "linear_exact_memory_read_count": 4,
            "linear_exact_stack_read_count": 4,
            "linear_exact_retrieval_seconds": 0.002,
            "linear_exact_non_retrieval_seconds": 0.002,
            "linear_exact_retrieval_share": 0.5,
            "linear_exact_ns_per_read": 250_000.0,
            "linear_exact_dominant_component": "retrieval_total",
            "linear_exact_ratio_vs_best_reference": 120.0 / base,
            "accelerated_median_seconds": 0.003,
            "accelerated_samples": [0.003],
            "accelerated_ns_per_step": 110.0,
            "accelerated_exact": True,
            "accelerated_exact_trace_match": True,
            "accelerated_exact_final_state_match": True,
            "accelerated_first_mismatch_step": None,
            "accelerated_failure_reason": None,
            "accelerated_read_observation_count": 8,
            "accelerated_memory_read_count": 4,
            "accelerated_stack_read_count": 4,
            "accelerated_retrieval_seconds": 0.0015,
            "accelerated_non_retrieval_seconds": 0.0015,
            "accelerated_retrieval_share": 0.5,
            "accelerated_ns_per_read": 187_500.0,
            "accelerated_dominant_component": "retrieval_total",
            "accelerated_ratio_vs_best_reference": 110.0 / base,
            "pointer_like_exact_median_seconds": 0.002,
            "pointer_like_exact_samples": [0.002],
            "pointer_like_exact_ns_per_step": 70.0,
            "pointer_like_exact_exact": True,
            "pointer_like_exact_exact_trace_match": True,
            "pointer_like_exact_exact_final_state_match": True,
            "pointer_like_exact_first_mismatch_step": None,
            "pointer_like_exact_failure_reason": None,
            "pointer_like_exact_read_observation_count": 8,
            "pointer_like_exact_memory_read_count": 4,
            "pointer_like_exact_stack_read_count": 4,
            "pointer_like_exact_retrieval_seconds": 0.0008,
            "pointer_like_exact_non_retrieval_seconds": 0.0012,
            "pointer_like_exact_retrieval_share": 0.4,
            "pointer_like_exact_ns_per_read": 100_000.0,
            "pointer_like_exact_dominant_component": "non_retrieval",
            "pointer_like_exact_ratio_vs_best_reference": 70.0 / base,
            "pointer_like_speedup_vs_accelerated": 110.0 / 70.0,
            "pointer_like_speedup_vs_lowered": 180.0 / 70.0,
        }

    monkeypatch.setattr(module, "positive_cases", fake_positive_cases)
    monkeypatch.setattr(module, "measure_case", fake_measure_case)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    strategy_payload = json.loads((temp_out_dir / "strategy_summary.json").read_text(encoding="utf-8"))
    suite_payload = json.loads((temp_out_dir / "suite_summary.json").read_text(encoding="utf-8"))

    summary = payload["summary"]
    gate = summary["gate"]

    assert summary["status"] == "r23_same_endpoint_systems_overturn_complete"
    assert gate["lane_verdict"] == "systems_materially_positive"
    assert gate["pointer_like_exact_case_count"] == 2
    assert gate["next_priority_lane"] == "h21_refreeze_after_r22_r23"
    assert len(strategy_payload["rows"]) == 6
    assert len(suite_payload["rows"]) == 2
