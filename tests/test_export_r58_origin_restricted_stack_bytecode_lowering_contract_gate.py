from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r58_origin_restricted_stack_bytecode_lowering_contract_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r58_origin_restricted_stack_bytecode_lowering_contract_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r58_writes_restricted_stack_bytecode_lowering_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R58_origin_restricted_stack_bytecode_lowering_contract_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "case_manifest.json").read_text(encoding="utf-8"))["rows"]
    lowering_report = json.loads((temp_out_dir / "lowering_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    exactness_rows = lowering_report["exactness_rows"]
    category_rollup_rows = lowering_report["category_rollup_rows"]
    gate = payload["summary"]["gate"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h53_post_h52_compiled_boundary_reentry_packet"
    assert payload["summary"]["current_post_h52_planning_bundle"] == "f29_post_h52_restricted_compiled_boundary_bundle"
    assert payload["summary"]["active_runtime_lane"] == (
        "r58_origin_restricted_stack_bytecode_lowering_contract_gate"
    )
    assert gate["lane_verdict"] == "restricted_stack_bytecode_lowering_supported_narrowly"
    assert gate["restricted_surface"] == "typed_stack_bytecode_subset_only"
    assert gate["planned_case_count"] == 5
    assert gate["executed_case_count"] == 5
    assert gate["exact_case_count"] == 5
    assert gate["failed_case_count"] == 0
    assert gate["planned_category_count"] == 5
    assert gate["exact_category_count"] == 5
    assert gate["claim_ceiling"] == "bounded_useful_cases_only"
    assert gate["stop_rule_triggered"] is False
    assert gate["next_required_packet"] == "r59_origin_compiled_trace_vm_execution_gate"
    assert stop_rule["stop_rule_triggered"] is False
    assert stop_rule["first_failure"] is None
    assert len(manifest_rows) == 5
    assert len(exactness_rows) == 5
    assert len(category_rollup_rows) == 5
    assert {row["case_id"] for row in exactness_rows} == {
        "straight_line_arithmetic",
        "counted_loop_countdown",
        "latest_write_overwrite_after_gap",
        "shallow_call_return_roundtrip",
        "branch_fallthrough_revisit",
    }
    assert all(row["verdict"] == "exact" for row in exactness_rows)
    assert all(row["compiled_scope_passed"] for row in exactness_rows)
    assert all(row["verifier_passed"] for row in exactness_rows)
    assert all(row["spec_contract_passed"] for row in exactness_rows)
    assert all(row["surface_literal_passed"] for row in exactness_rows)

    arithmetic_row = next(row for row in exactness_rows if row["case_id"] == "straight_line_arithmetic")
    assert arithmetic_row["source_final_state"]["stack"] == [12]
    assert arithmetic_row["source_final_state"]["steps"] == 4

    latest_write_row = next(row for row in exactness_rows if row["case_id"] == "latest_write_overwrite_after_gap")
    assert latest_write_row["source_final_state"]["memory"] == [[4, 17]]

    call_row = next(row for row in exactness_rows if row["case_id"] == "shallow_call_return_roundtrip")
    assert call_row["source_final_state"]["memory"] == [[192, 10]]
