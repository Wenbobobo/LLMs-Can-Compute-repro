from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from bytecode import r6_d0_long_horizon_scaling_cases


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r6_d0_long_horizon_scaling_gate.py"
    spec = importlib.util.spec_from_file_location("export_r6_d0_long_horizon_scaling_gate", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r6_case_registry_has_expected_fixed_scaling_grid() -> None:
    cases = r6_d0_long_horizon_scaling_cases()

    assert len(cases) == 24
    assert {case.horizon_multiplier for case in cases} == {2, 4, 8}
    assert len({case.family for case in cases}) == 8


def test_build_decode_parity_rows_keeps_linear_and_hull_exact_on_r6_grid() -> None:
    module = _load_export_module()

    rows = module.build_decode_parity_rows(r6_d0_long_horizon_scaling_cases())

    assert len(rows) == 8
    assert all(row["mismatch_class"] is None for row in rows)
    assert all(row["linear_exact_trace_match"] is True for row in rows)
    assert all(row["accelerated_exact_trace_match"] is True for row in rows)
    assert all(row["linear_accelerated_trace_match"] is True for row in rows)


def test_export_r6_d0_long_horizon_scaling_gate_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(Path("results/R6_d0_long_horizon_scaling_gate/summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["exact_suite"]["row_count"] == 24
    assert summary["exact_suite"]["positive_row_count"] == 24
    assert summary["exact_suite"]["exact_trace_match_count"] == 6
    assert summary["exact_suite"]["exact_final_state_match_count"] == 18
    assert summary["exact_suite"]["contradiction_candidate_count"] == 0
    assert summary["decode_parity"]["row_count"] == 8
    assert summary["decode_parity"]["parity_match_count"] == 8
    assert summary["growth"]["row_count"] == 24
    assert summary["precision_followup"]["candidate_stream_count"] > 0
    assert summary["claim_impact"]["e1c_status"] == "not_triggered"
    assert summary["claim_impact"]["next_lane"] == "R7_d0_same_endpoint_runtime_bridge"
