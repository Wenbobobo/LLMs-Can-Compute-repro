from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from bytecode import r8_d0_retrieval_pressure_cases


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r8_d0_retrieval_pressure_gate.py"
    spec = importlib.util.spec_from_file_location("export_r8_d0_retrieval_pressure_gate", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r8_case_registry_has_expected_bounded_grid() -> None:
    cases = r8_d0_retrieval_pressure_cases()

    assert len(cases) == 4
    assert {case.retrieval_horizon_multiplier for case in cases} == {10}
    assert {case.baseline_horizon_multiplier for case in cases} == {8}
    assert len({case.family for case in cases}) == 4


def test_route_bucket_classification_keeps_only_true_execution_mismatches_for_e1c() -> None:
    module = _load_export_module()

    assert module.route_bucket_from_mismatch_class(None) == "admitted"
    assert module.route_bucket_from_mismatch_class("trace_disagreement") == "d0_contradiction_candidate"
    assert module.route_bucket_from_mismatch_class("final_state_disagreement") == "d0_contradiction_candidate"
    assert module.route_bucket_from_mismatch_class("verifier_disagreement") == "harness_or_annotation"
    assert module.route_bucket_from_mismatch_class("runtime_exception") == "harness_or_annotation"


def test_export_r8_d0_retrieval_pressure_gate_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(Path("results/R8_d0_retrieval_pressure_gate/summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]
    decode_payload = json.loads(
        Path("results/R8_d0_retrieval_pressure_gate/decode_parity_rows.json").read_text(encoding="utf-8")
    )
    decode_rows = decode_payload["rows"]

    assert summary["exact_suite"]["row_count"] == 4
    assert summary["decode_parity"]["row_count"] == 2
    assert summary["pressure"]["row_count"] == summary["exact_suite"]["exact_admitted_count"]
    assert summary["pressure"]["family_count"] == 4
    assert len(decode_rows) == 2
    assert all(row["parity_probe_mode"] == "uniform_load_probe" for row in decode_rows)
    assert all(row["parity_probe_max_loads_per_space"] == 64 for row in decode_rows)
    assert all(row["memory_sampled_observation_count"] <= row["memory_total_observation_count"] for row in decode_rows)
    assert all(row["stack_sampled_observation_count"] <= row["stack_total_observation_count"] for row in decode_rows)
    assert summary["claim_impact"]["gate_status"] in {
        "go_harder_retrieval_pressure_exact",
        "stop_harness_or_annotation_gap",
        "stop_d0_contradiction_candidate",
        "stop_no_admitted_rows",
    }
    if summary["claim_impact"]["gate_status"] == "stop_d0_contradiction_candidate":
        assert summary["claim_impact"]["e1c_status"] == "triggered"
        assert summary["claim_impact"]["next_lane"] == "E1c_compiled_boundary_patch"
    else:
        assert summary["claim_impact"]["e1c_status"] == "not_triggered"
