from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r16_d0_real_trace_precision_boundary_saturation.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r16_d0_real_trace_precision_boundary_saturation",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r16_loads_admitted_r8_and_r15_surface_cases_only() -> None:
    module = _load_export_module()

    surface_cases, metadata = module.load_admitted_surface_cases()

    assert metadata["exact_suite_row_count"] == 8
    assert metadata["admitted_program_count"] == 8
    assert len(surface_cases) == 8
    assert {entry["source_lane"] for entry in surface_cases} == {
        "R8_d0_retrieval_pressure_gate",
        "R15_d0_remaining_family_retrieval_pressure_gate",
    }
    assert {entry["case"].family for entry in surface_cases} == {
        "checkpoint_replay_long",
        "helper_checkpoint_braid",
        "helper_checkpoint_braid_long",
        "indirect_counter_bank",
        "iterated_helper_accumulator",
        "stack_memory_braid",
        "subroutine_braid",
        "subroutine_braid_long",
    }


def test_r16_boundary_followup_logic_flags_precision_divergence_only() -> None:
    module = _load_export_module()

    rows = [
        {"horizon_multiplier": 1, "scheme": "single_head", "passed": True},
        {"horizon_multiplier": 1, "scheme": "radix2", "passed": True},
        {"horizon_multiplier": 1, "scheme": "block_recentered", "passed": True},
        {"horizon_multiplier": 2, "scheme": "single_head", "passed": False},
        {"horizon_multiplier": 2, "scheme": "radix2", "passed": True},
        {"horizon_multiplier": 2, "scheme": "block_recentered", "passed": True},
    ]

    assert module.enters_boundary_followup(rows) is True
    assert module.first_single_head_failure_multiplier(rows) == 2


def test_export_r16_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(
        Path("results/R16_d0_real_trace_precision_boundary_saturation/summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["source_surface"]["admitted_program_count"] == 8
    assert summary["source_surface"]["source_lane_count"] == 2
    assert summary["screening"]["candidate_stream_count"] == 8
    assert summary["screening"]["family_count"] == 8
    assert (
        summary["classification"]["effective_here_stream_count"]
        + summary["classification"]["unproven_here_stream_count"]
        + summary["classification"]["negated_here_stream_count"]
        == summary["screening"]["candidate_stream_count"]
    )
    assert summary["claim_impact"]["e1c_status"] == "not_triggered"
    assert summary["claim_impact"]["next_lane"] == "R17_d0_full_surface_runtime_bridge"
    assert summary["claim_impact"]["gate_status"] == "go_real_trace_precision_surface_saturated"
