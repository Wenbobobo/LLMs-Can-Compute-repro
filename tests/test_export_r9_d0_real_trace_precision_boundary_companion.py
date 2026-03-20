from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r9_d0_real_trace_precision_boundary_companion.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r9_d0_real_trace_precision_boundary_companion",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r9_loads_exact_admitted_r8_cases_only() -> None:
    module = _load_export_module()

    cases, exact_payload = module.load_r8_admitted_cases()

    assert len(exact_payload["rows"]) == 4
    assert len(cases) == 4
    assert {case.family for case in cases} == {
        "helper_checkpoint_braid_long",
        "subroutine_braid_long",
        "iterated_helper_accumulator",
        "checkpoint_replay_long",
    }


def test_r9_boundary_followup_logic_flags_only_true_precision_divergence() -> None:
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


def test_export_r9_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(
        Path("results/R9_d0_real_trace_precision_boundary_companion/summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["screening"]["candidate_stream_count"] == 4
    assert summary["screening"]["family_count"] == 4
    assert (
        summary["classification"]["effective_here_stream_count"]
        + summary["classification"]["unproven_here_stream_count"]
        + summary["classification"]["negated_here_stream_count"]
        == summary["screening"]["candidate_stream_count"]
    )
    assert summary["claim_impact"]["e1c_status"] == "not_triggered"
    assert summary["claim_impact"]["next_lane"] == "R10_d0_same_endpoint_cost_attribution"
