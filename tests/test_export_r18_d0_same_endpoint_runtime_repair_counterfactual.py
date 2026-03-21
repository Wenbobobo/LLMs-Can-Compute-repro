from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r18_d0_same_endpoint_runtime_repair_counterfactual.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r18_d0_same_endpoint_runtime_repair_counterfactual",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r18_loads_probe_cases_from_r17_selection() -> None:
    module = _load_export_module()

    surface_records = module.load_surface_case_records()
    probe_cases = module.load_probe_cases(surface_records)

    assert len(surface_records) == 8
    assert len(probe_cases) == 2
    assert [probe_case.probe_role for probe_case in probe_cases] == ["target", "control"]
    assert {probe_case.record.program_name for probe_case in probe_cases} == {
        "bytecode_helper_checkpoint_braid_long_180_a312_s0",
        "bytecode_stack_memory_braid_100_a112",
    }


def test_r18_target_gate_requires_exact_two_x_speedup() -> None:
    module = _load_export_module()
    probe_rows = [
        {
            "probe_role": "target",
            "program_name": "target_program",
            "family": "target_family",
            "probe_exact_trace_match": True,
            "probe_exact_final_state_match": True,
            "speedup_vs_r17_accelerated": 2.4,
        },
        {
            "probe_role": "control",
            "program_name": "control_program",
            "family": "control_family",
            "probe_exact_trace_match": True,
            "probe_exact_final_state_match": True,
            "speedup_vs_r17_accelerated": 1.3,
        },
    ]

    gate = module.assess_target_gate(probe_rows)

    assert gate["gate_passed"] is True
    assert gate["target_program_name"] == "target_program"
    assert gate["required_speedup_vs_r17_accelerated"] == 2.0


def test_export_r18_writes_expected_pointer_like_summary(tmp_path) -> None:
    module = _load_export_module()
    surface_records = module.load_surface_case_records()
    probe_cases = module.load_probe_cases(surface_records)
    target_program_name = next(
        probe_case.record.program_name for probe_case in probe_cases if probe_case.probe_role == "target"
    )

    original_out_dir = module.OUT_DIR
    original_profile_surface_record = module.profile_surface_record
    original_build_memory_address_profile = module.build_memory_address_profile
    temp_out_dir = tmp_path / "R18_d0_same_endpoint_runtime_repair_counterfactual"

    def fake_build_memory_address_profile(record):
        return {
            "program_name": record.program_name,
            "family": record.family,
            "source_lane": record.source_lane,
            "boundary_bearing_stream": record.boundary_bearing_stream,
            "reference_step_count": 100,
            "memory_operation_count": 60,
            "memory_load_count": 40,
            "memory_store_count": 20,
            "unique_address_count": 6,
            "hottest_address": 312 if record.program_name == target_program_name else 112,
            "hottest_address_loads": 30,
            "hottest_address_stores": 10,
            "address_rows": [],
        }

    def fake_profile_surface_record(
        record,
        probe,
        *,
        selection_rank=None,
        probe_role=None,
        focus_reason=None,
        selection_rule=None,
    ):
        speedup_vs_r17_accelerated = 2.4 if record.program_name == target_program_name else 1.35
        return {
            "probe_id": probe.probe_id,
            "probe_label": probe.probe_label,
            "probe_strategy": probe.probe_strategy,
            "stack_strategy": probe.stack_strategy,
            "memory_strategy": probe.memory_strategy,
            "selection_rank": selection_rank,
            "probe_role": probe_role,
            "focus_reason": focus_reason,
            "selection_rule": selection_rule,
            "source_lane": record.source_lane,
            "family": record.family,
            "program_name": record.program_name,
            "baseline_stage": record.baseline_stage,
            "baseline_program_name": record.baseline_program_name,
            "baseline_horizon_multiplier": record.baseline_horizon_multiplier,
            "retrieval_horizon_multiplier": record.retrieval_horizon_multiplier,
            "comparison_mode": record.comparison_mode,
            "max_steps": record.max_steps,
            "boundary_bearing_stream": record.boundary_bearing_stream,
            "reference_step_count": 100,
            "profile_repeats": module.PROFILE_REPEATS,
            "r17_baseline_accelerated_ns_per_step": 100.0,
            "r17_baseline_lowered_ns_per_step": 10.0,
            "current_lowered_ns_per_step": 10.0,
            "current_accelerated_ns_per_step": 90.0,
            "probe_ns_per_step": 100.0 / speedup_vs_r17_accelerated,
            "speedup_vs_current_accelerated": 1.2,
            "speedup_vs_r17_accelerated": speedup_vs_r17_accelerated,
            "probe_ratio_vs_current_lowered": 8.0,
            "probe_samples": [0.05],
            "probe_exact_trace_match": True,
            "probe_exact_final_state_match": True,
            "probe_first_mismatch_step": None,
            "read_observation_count": 50,
            "memory_read_count": 30,
            "stack_read_count": 20,
        }

    module.OUT_DIR = temp_out_dir
    module.profile_surface_record = fake_profile_surface_record
    module.build_memory_address_profile = fake_build_memory_address_profile
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.profile_surface_record = original_profile_surface_record
        module.build_memory_address_profile = original_build_memory_address_profile

    payload = json.loads(
        (temp_out_dir / "summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["status"] == "r18b_pointer_like_complete"
    assert summary["probe_strategy"] == "pointer_like_exact_both_spaces"
    assert summary["target_gate"]["gate_passed"] is True
    assert summary["confirmation"]["gate_passed"] is True
    assert summary["confirmation"]["row_count"] == 8
    assert summary["executed_probe_ids"] == ["r18b_pointer_like"]
    assert summary["claim_impact"]["next_lane"] == "H17_refreeze_and_conditional_frontier_recheck"
    assert summary["claim_impact"]["next_probe"] is None


def test_export_r18_runs_conditional_staged_followup(tmp_path) -> None:
    module = _load_export_module()
    surface_records = module.load_surface_case_records()
    probe_cases = module.load_probe_cases(surface_records)
    target_program_name = next(
        probe_case.record.program_name for probe_case in probe_cases if probe_case.probe_role == "target"
    )

    original_out_dir = module.OUT_DIR
    original_profile_surface_record = module.profile_surface_record
    original_build_memory_address_profile = module.build_memory_address_profile
    temp_out_dir = tmp_path / "R18_d0_same_endpoint_runtime_repair_counterfactual"

    def fake_build_memory_address_profile(record):
        return {
            "program_name": record.program_name,
            "family": record.family,
            "source_lane": record.source_lane,
            "boundary_bearing_stream": record.boundary_bearing_stream,
            "reference_step_count": 100,
            "memory_operation_count": 60,
            "memory_load_count": 40,
            "memory_store_count": 20,
            "unique_address_count": 6,
            "hottest_address": 312 if record.program_name == target_program_name else 112,
            "hottest_address_loads": 30,
            "hottest_address_stores": 10,
            "address_rows": [],
        }

    def fake_profile_surface_record(
        record,
        probe,
        *,
        selection_rank=None,
        probe_role=None,
        focus_reason=None,
        selection_rule=None,
    ):
        if probe.probe_id == "r18b_pointer_like":
            speedup_vs_r17_accelerated = 1.7 if probe_role == "target" else 1.1
        else:
            speedup_vs_r17_accelerated = 2.2 if probe_role == "target" else 1.3
            if probe_role is None:
                speedup_vs_r17_accelerated = 1.3
        return {
            "probe_id": probe.probe_id,
            "probe_label": probe.probe_label,
            "probe_strategy": probe.probe_strategy,
            "stack_strategy": probe.stack_strategy,
            "memory_strategy": probe.memory_strategy,
            "selection_rank": selection_rank,
            "probe_role": probe_role,
            "focus_reason": focus_reason,
            "selection_rule": selection_rule,
            "source_lane": record.source_lane,
            "family": record.family,
            "program_name": record.program_name,
            "baseline_stage": record.baseline_stage,
            "baseline_program_name": record.baseline_program_name,
            "baseline_horizon_multiplier": record.baseline_horizon_multiplier,
            "retrieval_horizon_multiplier": record.retrieval_horizon_multiplier,
            "comparison_mode": record.comparison_mode,
            "max_steps": record.max_steps,
            "boundary_bearing_stream": record.boundary_bearing_stream,
            "reference_step_count": 100,
            "profile_repeats": module.PROFILE_REPEATS,
            "r17_baseline_accelerated_ns_per_step": 100.0,
            "r17_baseline_lowered_ns_per_step": 10.0,
            "current_lowered_ns_per_step": 10.0,
            "current_accelerated_ns_per_step": 90.0,
            "probe_ns_per_step": 100.0 / speedup_vs_r17_accelerated,
            "speedup_vs_current_accelerated": 1.2,
            "speedup_vs_r17_accelerated": speedup_vs_r17_accelerated,
            "probe_ratio_vs_current_lowered": 8.0,
            "probe_samples": [0.05],
            "probe_exact_trace_match": True,
            "probe_exact_final_state_match": True,
            "probe_first_mismatch_step": None,
            "read_observation_count": 50,
            "memory_read_count": 30,
            "stack_read_count": 20,
        }

    module.OUT_DIR = temp_out_dir
    module.profile_surface_record = fake_profile_surface_record
    module.build_memory_address_profile = fake_build_memory_address_profile
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.profile_surface_record = original_profile_surface_record
        module.build_memory_address_profile = original_build_memory_address_profile

    payload = json.loads(
        (temp_out_dir / "summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["status"] == "r18c_staged_exact_complete"
    assert summary["probe_strategy"] == "staged_exact_both_spaces"
    assert summary["executed_probe_ids"] == ["r18b_pointer_like", "r18c_staged_exact"]
    assert summary["target_gate"]["gate_passed"] is True
    assert summary["confirmation"]["gate_passed"] is True
    assert summary["claim_impact"]["next_lane"] == "H17_refreeze_and_conditional_frontier_recheck"
