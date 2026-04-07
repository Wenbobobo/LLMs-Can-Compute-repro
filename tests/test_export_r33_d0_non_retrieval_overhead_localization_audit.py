from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r33_d0_non_retrieval_overhead_localization_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r33_d0_non_retrieval_overhead_localization_audit",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_r23_runtime_rows():
    rows = []
    for suite, ratios in {
        "smoke": [2.0, 2.5, 3.5],
        "loops": [3.0, 3.5, 5.0],
        "memory": [4.0, 4.5, 5.5],
        "control_flow": [4.0, 4.2, 4.8],
        "stress_reference": [4.1, 4.4, 4.9],
    }.items():
        for index, ratio in enumerate(ratios):
            rows.append(
                {
                    "program_name": f"{suite}_case_{index}",
                    "suite": suite,
                    "comparison_mode": "medium_exact_trace",
                    "max_steps": 64,
                    "pointer_like_exact_ratio_vs_best_reference": ratio,
                    "lowered_ratio_vs_best_reference": 1.5,
                    "pointer_like_exact_memory_read_count": 20 + index * 4 if suite != "smoke" else 0,
                    "pointer_like_exact_stack_read_count": 20 + index * 6,
                }
            )
    return rows


def _fake_inputs():
    return {
        "h26_summary": {
            "summary": {
                "next_priority_lane": "r33_d0_non_retrieval_overhead_localization_audit",
            }
        },
        "h25_summary": {"summary": {}},
        "r31_summary": {"summary": {}},
        "r23_summary": {"summary": {}},
        "r23_runtime_rows": {"rows": _fake_r23_runtime_rows()},
        "r28_summary": {"summary": {}},
    }


def test_r33_builds_expected_stratified_sample_manifest() -> None:
    module = _load_export_module()

    manifest_rows = module.build_stratified_sample_manifest(_fake_r23_runtime_rows())

    assert len(manifest_rows) == 10
    assert sum(row["selection_class"] == "median_ratio" for row in manifest_rows) == 5
    assert sum(row["selection_class"] == "worst_ratio" for row in manifest_rows) == 5
    assert sum(row["selection_class"] == "control_heavy_extra" for row in manifest_rows) == 0


def test_r33_assess_gate_reports_suite_stable_noncompetitive_after_localization() -> None:
    module = _load_export_module()

    rows = [
        {
            "suite": "smoke",
            "verification_passed": True,
            "spec_reference_seconds": 1.0,
            "lowered_exec_trace_seconds": 1.2,
            "lowered_exec_trace_error": None,
            "pointer_like_exact_seconds": 2.0,
            "pointer_like_exact_exact": True,
            "component_total_matches_non_retrieval": True,
            "dominant_non_retrieval_component": "dispatch_decode_seconds",
            "pointer_like_ratio_vs_spec_reference": 2.0,
            "pointer_like_ratio_vs_lowered_exec_trace": 1.4,
            "retrieval_seconds": 0.1,
            "non_retrieval_seconds": 0.9,
            "pointer_like_non_retrieval_share": 0.9,
        },
        {
            "suite": "loops",
            "verification_passed": True,
            "spec_reference_seconds": 1.0,
            "lowered_exec_trace_seconds": 1.3,
            "lowered_exec_trace_error": None,
            "pointer_like_exact_seconds": 2.2,
            "pointer_like_exact_exact": True,
            "component_total_matches_non_retrieval": True,
            "dominant_non_retrieval_component": "dispatch_decode_seconds",
            "pointer_like_ratio_vs_spec_reference": 2.2,
            "pointer_like_ratio_vs_lowered_exec_trace": 1.5,
            "retrieval_seconds": 0.2,
            "non_retrieval_seconds": 1.0,
            "pointer_like_non_retrieval_share": 0.83,
        },
    ]
    suite_summary_rows = module.build_suite_component_summary(rows)
    comparator_summary_rows = module.build_comparator_summary(rows)
    gate = module.assess_attribution_gate(
        rows,
        suite_summary_rows=suite_summary_rows,
        comparator_summary_rows=comparator_summary_rows,
        audit_scope="stratified_first_pass",
    )

    assert gate["lane_verdict"] == "suite_stable_noncompetitive_after_localization"
    assert gate["suites_same_dominant_component"] is True
    assert gate["next_priority_lane"] == "h27_refreeze_after_r32_r33_same_endpoint_decision"


def test_r33_profile_uses_coherent_representative_sample(monkeypatch) -> None:
    module = _load_export_module()

    profiles = [
        module.PointerLikeComponentProfile(
            total_seconds=1.1,
            retrieval_seconds=0.1,
            dispatch_decode_seconds=0.0,
            state_update_bookkeeping_seconds=1.0,
            tensor_python_plumbing_seconds=0.0,
            residual_fixed_overhead_seconds=0.0,
            read_count=1,
            memory_read_count=0,
            stack_read_count=1,
        ),
        module.PointerLikeComponentProfile(
            total_seconds=3.1,
            retrieval_seconds=0.1,
            dispatch_decode_seconds=1.0,
            state_update_bookkeeping_seconds=2.0,
            tensor_python_plumbing_seconds=0.0,
            residual_fixed_overhead_seconds=0.0,
            read_count=3,
            memory_read_count=1,
            stack_read_count=2,
        ),
        module.PointerLikeComponentProfile(
            total_seconds=4.1,
            retrieval_seconds=0.1,
            dispatch_decode_seconds=4.0,
            state_update_bookkeeping_seconds=0.0,
            tensor_python_plumbing_seconds=0.0,
            residual_fixed_overhead_seconds=0.0,
            read_count=4,
            memory_read_count=2,
            stack_read_count=2,
        ),
    ]
    executions = ["exec_0", "exec_1", "exec_2"]

    class FakeExecutor:
        call_index = 0

        def run_with_profile(self, lowered_program, *, max_steps):
            del lowered_program, max_steps
            index = FakeExecutor.call_index
            FakeExecutor.call_index += 1
            return executions[index], profiles[index]

    monkeypatch.setattr(module.r23, "reference_execution", lambda lowered_program, max_steps: object())
    monkeypatch.setattr(module, "ComponentProfiledPointerLikeExecutor", FakeExecutor)
    monkeypatch.setattr(
        module,
        "compare_execution_to_reference",
        lambda lowered_program, execution, *, reference: SimpleNamespace(
            exact_trace_match=True,
            exact_final_state_match=True,
            failure_reason=None,
            first_mismatch_step=None,
        ),
    )

    profile = module.profile_pointer_like_exact(object(), max_steps=32)

    assert profile["median_seconds"] == 3.1
    assert profile["non_retrieval_seconds"] == 3.0
    assert profile["dispatch_decode_seconds"] == 1.0
    assert profile["state_update_bookkeeping_seconds"] == 2.0
    assert profile["component_total_matches_non_retrieval"] is True
    assert profile["component_reconstruction_error_seconds"] == 0.0
    assert profile["read_observation_count"] == 3.0


def test_export_r33_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R33_d0_non_retrieval_overhead_localization_audit"
    module.OUT_DIR = temp_out_dir

    def fake_execute_component_audit(manifest_rows, case_registry):
        del case_registry
        return [
            {
                **row,
                "verification_passed": True,
                "spec_reference_seconds": 1.0,
                "spec_reference_error": None,
                "lowered_exec_trace_seconds": 1.5,
                "lowered_exec_trace_error": None,
                "pointer_like_exact_seconds": 2.5,
                "pointer_like_exact_exact": True,
                "pointer_like_exact_exact_trace_match": True,
                "pointer_like_exact_exact_final_state_match": True,
                "pointer_like_exact_first_mismatch_step": None,
                "pointer_like_exact_failure_reason": None,
                "pointer_like_exact_read_observation_count": 40,
                "pointer_like_exact_memory_read_count": 16,
                "pointer_like_exact_stack_read_count": 24,
                "retrieval_seconds": 0.1,
                "non_retrieval_seconds": 2.4,
                "dispatch_decode_seconds": 1.6,
                "state_update_bookkeeping_seconds": 0.4,
                "tensor_python_plumbing_seconds": 0.2,
                "residual_fixed_overhead_seconds": 0.2,
                "component_total_matches_non_retrieval": True,
                "component_reconstruction_error_seconds": 0.0,
                "dominant_non_retrieval_component": "dispatch_decode_seconds",
                "pointer_like_non_retrieval_share": 0.96,
                "pointer_like_retrieval_share": 0.04,
                "pointer_like_ratio_vs_spec_reference": 2.5,
                "pointer_like_ratio_vs_lowered_exec_trace": 1.6666666667,
                "pointer_like_ratio_vs_best_reference": 2.5,
                "best_reference_id": "spec_reference",
                "best_reference_seconds": 1.0,
            }
            for row in manifest_rows
        ]

    monkeypatch.setattr(module, "load_inputs", _fake_inputs)
    monkeypatch.setattr(module, "build_case_registry", lambda: {})
    monkeypatch.setattr(module, "execute_component_audit", fake_execute_component_audit)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    verdict_payload = json.loads((temp_out_dir / "attribution_verdict.json").read_text(encoding="utf-8"))
    summary = payload["summary"]
    gate = summary["gate"]

    assert summary["status"] == "r33_non_retrieval_overhead_localization_complete"
    assert gate["lane_verdict"] == "suite_stable_noncompetitive_after_localization"
    assert gate["next_priority_lane"] == "h27_refreeze_after_r32_r33_same_endpoint_decision"
    assert verdict_payload["summary"]["audit_scope"] == "stratified_first_pass"
