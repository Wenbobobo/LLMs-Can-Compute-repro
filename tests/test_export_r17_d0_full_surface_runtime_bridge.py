from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r17_d0_full_surface_runtime_bridge.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r17_d0_full_surface_runtime_bridge",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r17_loads_full_surface_from_r16_handoff() -> None:
    module = _load_export_module()

    surface_cases, metadata = module.load_admitted_surface_cases()

    assert metadata["exact_suite_row_count"] == 8
    assert metadata["admitted_program_count"] == 8
    assert metadata["precision_handoff"]["screened_stream_count"] == 8
    assert len(surface_cases) == 8
    assert {surface_case.source_lane for surface_case in surface_cases} == {
        "R8_d0_retrieval_pressure_gate",
        "R15_d0_remaining_family_retrieval_pressure_gate",
    }
    assert {surface_case.case.family for surface_case in surface_cases} == {
        "checkpoint_replay_long",
        "helper_checkpoint_braid",
        "helper_checkpoint_braid_long",
        "indirect_counter_bank",
        "iterated_helper_accumulator",
        "stack_memory_braid",
        "subroutine_braid",
        "subroutine_braid_long",
    }
    assert sum(surface_case.boundary_bearing_stream for surface_case in surface_cases) == 1


def test_r17_focus_selection_uses_boundary_and_heaviest_r15_rows() -> None:
    module = _load_export_module()
    surface_cases, _ = module.load_admitted_surface_cases()

    focused_cases, selection_rows = module.select_focused_attribution_cases(surface_cases)

    assert len(focused_cases) == 2
    assert len(selection_rows) == 2
    assert {case.focus_reason for case in focused_cases} == {
        "unique_boundary_bearing_precision_stream",
        "heaviest_r15_admitted_by_bytecode_step_count",
    }
    assert {case.program_name for case in focused_cases} == {
        "bytecode_helper_checkpoint_braid_long_180_a312_s0",
        "bytecode_stack_memory_braid_100_a112",
    }
    assert selection_rows[0]["selection_rule"] == (
        "unique_boundary_bearing_precision_stream_plus_heaviest_r15_admitted_by_bytecode_step_count"
    )


def test_r17_r18_trigger_requires_sharp_local_outlier() -> None:
    module = _load_export_module()

    runtime_rows = [
        {
            "program_name": "row_a",
            "family": "family_a",
            "reference_step_count": 100,
            "accelerated_ratio_vs_lowered": 2.8,
            "accelerated_speedup_vs_linear": 1.2,
            "linear_exact_trace_match": True,
            "linear_exact_final_state_match": True,
            "accelerated_exact_trace_match": True,
            "accelerated_exact_final_state_match": True,
            "linear_accelerated_trace_match": True,
            "linear_accelerated_final_state_match": True,
            "exact_read_agreement": True,
        },
        {
            "program_name": "row_b",
            "family": "family_b",
            "reference_step_count": 90,
            "accelerated_ratio_vs_lowered": 1.6,
            "accelerated_speedup_vs_linear": 1.15,
            "linear_exact_trace_match": True,
            "linear_exact_final_state_match": True,
            "accelerated_exact_trace_match": True,
            "accelerated_exact_final_state_match": True,
            "linear_accelerated_trace_match": True,
            "linear_accelerated_final_state_match": True,
            "exact_read_agreement": True,
        },
    ]
    focused_rows = [
        {
            "program_name": "row_a",
            "family": "family_a",
            "focus_reason": "unique_boundary_bearing_precision_stream",
            "retrieval_total_seconds": 3.0,
            "exact_vs_lowered_ratio": 3.2,
            "dominant_exact_component": "retrieval_total",
            "dominant_component_share": 0.72,
        },
        {
            "program_name": "row_b",
            "family": "family_b",
            "focus_reason": "heaviest_r15_admitted_by_bytecode_step_count",
            "retrieval_total_seconds": 1.2,
            "exact_vs_lowered_ratio": 1.8,
            "dominant_exact_component": "retrieval_total",
            "dominant_component_share": 0.58,
        },
    ]

    assessment = module.assess_r18_trigger(runtime_rows, focused_rows)

    assert assessment["triggered"] is True
    assert assessment["next_lane"] == "R18_d0_same_endpoint_runtime_repair_counterfactual"
    assert assessment["repair_target"]["program_name"] == "row_a"
    assert assessment["repair_target"]["component"] == "retrieval_total"


def test_export_r17_builds_expected_summary() -> None:
    module = _load_export_module()
    surface_cases, _ = module.load_admitted_surface_cases()
    focused_cases, _ = module.select_focused_attribution_cases(surface_cases)

    original_profile_surface_runtime_case = module.profile_surface_runtime_case
    original_profile_focused_attribution_case = module.profile_focused_attribution_case

    def fake_profile_surface_runtime_case(surface_case):
        index = len(fake_runtime_rows)
        fake_runtime_rows.append(surface_case.case.program.name)
        return {
            "source_lane": surface_case.source_lane,
            "family": surface_case.case.family,
            "baseline_stage": surface_case.case.baseline_stage,
            "baseline_program_name": surface_case.case.baseline_program_name,
            "baseline_horizon_multiplier": surface_case.case.baseline_horizon_multiplier,
            "retrieval_horizon_multiplier": surface_case.case.retrieval_horizon_multiplier,
            "horizon_multiplier": surface_case.case.retrieval_horizon_multiplier,
            "program_name": surface_case.case.program.name,
            "comparison_mode": surface_case.case.comparison_mode,
            "max_steps": surface_case.case.max_steps,
            "stream_name": surface_case.stream_name,
            "boundary_bearing_stream": surface_case.boundary_bearing_stream,
            "reference_step_count": int(surface_case.exact_row["bytecode_step_count"]),
            "profile_repeats": module.PROFILE_REPEATS,
            "bytecode_median_seconds": 0.01 + index * 0.001,
            "lowered_median_seconds": 0.008 + index * 0.001,
            "linear_median_seconds": 0.02 + index * 0.001,
            "accelerated_median_seconds": 0.018 + index * 0.001,
            "bytecode_samples": [0.01 + index * 0.001],
            "lowered_samples": [0.008 + index * 0.001],
            "linear_samples": [0.02 + index * 0.001],
            "accelerated_samples": [0.018 + index * 0.001],
            "bytecode_ns_per_step": 10.0 + index,
            "lowered_ns_per_step": 8.0 + index,
            "linear_ns_per_step": 20.0 + index,
            "accelerated_ns_per_step": 18.0 + index,
            "accelerated_speedup_vs_linear": (20.0 + index) / (18.0 + index),
            "accelerated_ratio_vs_lowered": (18.0 + index) / (8.0 + index),
            "accelerated_ratio_vs_bytecode": (18.0 + index) / (10.0 + index),
            "linear_exact_trace_match": True,
            "linear_exact_final_state_match": True,
            "accelerated_exact_trace_match": True,
            "accelerated_exact_final_state_match": True,
            "linear_accelerated_trace_match": True,
            "linear_accelerated_final_state_match": True,
            "linear_first_mismatch_step": None,
            "accelerated_first_mismatch_step": None,
            "read_observation_count": 100 + index,
            "exact_read_agreement": True,
        }

    def fake_profile_focused_attribution_case(case):
        index = len(fake_focused_rows)
        fake_focused_rows.append(case.program_name)
        return {
            "selection_rank": case.selection_rank,
            "focus_reason": case.focus_reason,
            "source_lane": case.source_lane,
            "family": case.family,
            "program_name": case.program_name,
            "baseline_program_name": case.baseline_program_name,
            "baseline_horizon_multiplier": case.baseline_horizon_multiplier,
            "retrieval_horizon_multiplier": case.retrieval_horizon_multiplier,
            "boundary_bearing_stream": case.boundary_bearing_stream,
            "max_steps": case.max_steps,
            "reference_step_count": case.bytecode_step_count,
            "lowering_seconds": 0.001,
            "bytecode_seconds": 0.01 + index * 0.001,
            "lowered_seconds": 0.008 + index * 0.001,
            "exact_total_seconds": 0.03 + index * 0.01,
            "retrieval_linear_seconds": 0.01 + index * 0.002,
            "retrieval_accelerated_seconds": 0.008 + index * 0.002,
            "retrieval_total_seconds": 0.018 + index * 0.004,
            "local_transition_seconds": 0.006,
            "trace_bookkeeping_seconds": 0.004,
            "executor_overhead_seconds": 0.002,
            "exact_nonretrieval_seconds": 0.012 + index * 0.006,
            "retrieval_share_of_exact": 0.60 + index * 0.05,
            "linear_validation_share_of_retrieval": 0.55,
            "accelerated_query_share_of_retrieval": 0.45,
            "exact_vs_lowered_ratio": 3.0 - index * 0.8,
            "exact_vs_bytecode_ratio": 2.0,
            "read_count": 128,
            "stack_read_count": 64,
            "memory_read_count": 64,
            "dominant_exact_component": "retrieval_total",
            "dominant_component_share": 0.7 - index * 0.15,
        }

    fake_runtime_rows: list[str] = []
    fake_focused_rows: list[str] = []
    module.profile_surface_runtime_case = fake_profile_surface_runtime_case
    module.profile_focused_attribution_case = fake_profile_focused_attribution_case

    try:
        module.main()
    finally:
        module.profile_surface_runtime_case = original_profile_surface_runtime_case
        module.profile_focused_attribution_case = original_profile_focused_attribution_case

    summary_payload = json.loads(
        Path("results/R17_d0_full_surface_runtime_bridge/summary.json").read_text(encoding="utf-8")
    )
    trigger_payload = json.loads(
        Path("results/R17_d0_full_surface_runtime_bridge/r18_trigger_assessment.json").read_text(encoding="utf-8")
    )
    summary = summary_payload["summary"]
    trigger_summary = trigger_payload["summary"]

    assert summary["overall"]["exact_suite_row_count"] == 8
    assert summary["overall"]["admitted_surface_row_count"] == 8
    assert summary["overall"]["source_lane_count"] == 2
    assert summary["overall"]["family_count"] == 8
    assert summary["overall"]["focused_attribution_row_count"] == 2
    assert summary["stopgo"]["stopgo_status"] in {
        "stop_decode_gain_not_material",
        "stop_bridge_not_yet_closed",
        "go_full_surface_bridge_positive",
    }
    assert summary["claim_impact"]["e1c_status"] == "not_triggered"
    assert summary["claim_impact"]["next_lane"] in {
        "H17_refreeze_and_conditional_frontier_recheck",
        "R18_d0_same_endpoint_runtime_repair_counterfactual",
    }
    assert summary["claim_impact"]["next_lane"] == trigger_summary["next_lane"]
    if trigger_summary["triggered"]:
        assert trigger_summary["repair_target"] is not None
    else:
        assert trigger_summary["repair_target"] is None
