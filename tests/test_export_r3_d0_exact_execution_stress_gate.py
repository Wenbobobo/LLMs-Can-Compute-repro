from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from bytecode import r3_d0_exact_execution_stress_cases, run_stress_reference_harness


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r3_d0_exact_execution_stress_gate.py"
    spec = importlib.util.spec_from_file_location("export_r3_d0_exact_execution_stress_gate", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r3_cases_stay_exact_on_current_stress_reference_harness() -> None:
    rows = run_stress_reference_harness(r3_d0_exact_execution_stress_cases())

    assert len(rows) == 7
    assert all(row["mismatch_class"] is None for row in rows)
    assert sum(row["comparison_mode"] == "medium_exact_trace" for row in rows) == 2
    assert sum(row["comparison_mode"] == "long_exact_final_state" for row in rows) == 5


def test_build_decode_parity_rows_keeps_linear_and_hull_exact() -> None:
    module = _load_export_module()

    rows = module.build_decode_parity_rows(r3_d0_exact_execution_stress_cases())

    assert len(rows) == 7
    assert all(row["mismatch_class"] is None for row in rows)
    assert all(row["linear_exact_trace_match"] is True for row in rows)
    assert all(row["accelerated_exact_trace_match"] is True for row in rows)
    assert all(row["linear_accelerated_trace_match"] is True for row in rows)


def test_export_r3_d0_exact_execution_stress_gate_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    summary_path = Path("results/R3_d0_exact_execution_stress_gate/summary.json")
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["exact_suite"]["row_count"] == 7
    assert summary["exact_suite"]["positive_row_count"] == 7
    assert summary["exact_suite"]["exact_trace_match_count"] == 2
    assert summary["exact_suite"]["exact_final_state_match_count"] == 5
    assert summary["exact_suite"]["contradiction_candidate_count"] == 0
    assert summary["decode_parity"]["row_count"] == 7
    assert summary["decode_parity"]["parity_match_count"] == 7
    assert summary["precision_followup"]["boundary_bearing_stream_count"] == 4
    assert summary["precision_followup"]["negative_control_row_count"] == 4
    assert summary["precision_followup"]["negative_control_failure_count"] == 3
    assert summary["claim_impact"]["e1c_status"] == "not_triggered"
    assert summary["claim_impact"]["next_lane"] == "R4_mechanistic_retrieval_closure"
