from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r59_origin_compiled_trace_vm_execution_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r59_origin_compiled_trace_vm_execution_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r59_writes_compiled_trace_vm_execution_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R59_origin_compiled_trace_vm_execution_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "case_manifest.json").read_text(encoding="utf-8"))["rows"]
    execution_report = json.loads((temp_out_dir / "execution_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    gate = payload["summary"]["gate"]
    comparator_rows = execution_report["comparator_rows"]
    category_rollup_rows = execution_report["category_rollup_rows"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h53_post_h52_compiled_boundary_reentry_packet"
    assert payload["summary"]["current_post_h52_planning_bundle"] == "f29_post_h52_restricted_compiled_boundary_bundle"
    assert payload["summary"]["active_runtime_lane"] == "r59_origin_compiled_trace_vm_execution_gate"
    assert payload["summary"]["preserved_lowering_gate"] == (
        "r58_origin_restricted_stack_bytecode_lowering_contract_gate"
    )
    assert gate["lane_verdict"] == "compiled_trace_vm_execution_supported_exactly"
    assert gate["planned_case_count"] == 5
    assert gate["executed_case_count"] == 5
    assert gate["exact_case_count"] == 5
    assert gate["failed_case_count"] == 0
    assert gate["exact_category_count"] == 5
    assert gate["selected_h54_outcome"] == (
        "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
    )
    assert gate["first_failure_route"] is None
    assert gate["next_required_packet"] == "h54_post_r58_r59_compiled_boundary_decision_packet"
    assert stop_rule["stop_rule_triggered"] is False
    assert stop_rule["first_failure"] is None
    assert execution_report["first_failure"] is None
    assert len(manifest_rows) == 5
    assert len(comparator_rows) == 5
    assert len(category_rollup_rows) == 5
    assert {row["case_id"] for row in comparator_rows} == {
        "straight_line_arithmetic",
        "counted_loop_countdown",
        "latest_write_overwrite_after_gap",
        "shallow_call_return_roundtrip",
        "branch_fallthrough_revisit",
    }
    assert all(row["source_to_lowered_trace_match"] for row in comparator_rows)
    assert all(row["source_to_lowered_final_state_match"] for row in comparator_rows)
    assert all(row["linear_exact_trace_match"] for row in comparator_rows)
    assert all(row["linear_exact_final_state_match"] for row in comparator_rows)
    assert all(row["accelerated_exact_trace_match"] for row in comparator_rows)
    assert all(row["accelerated_exact_final_state_match"] for row in comparator_rows)
    assert any(row["linear_memory_read_count"] > 0 for row in comparator_rows)
    assert any(row["accelerated_call_read_count"] > 0 for row in comparator_rows)
    assert all(row["linear_read_count"] == row["accelerated_read_count"] for row in comparator_rows)
    assert all(row["source_interpreter_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["lowered_interpreter_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["linear_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["accelerated_mean_seconds"] > 0.0 for row in comparator_rows)
