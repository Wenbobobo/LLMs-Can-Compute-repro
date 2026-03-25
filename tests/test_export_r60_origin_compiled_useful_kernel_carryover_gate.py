from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r60_origin_compiled_useful_kernel_carryover_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r60_origin_compiled_useful_kernel_carryover_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r60_writes_actual_carryover_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R60_origin_compiled_useful_kernel_carryover_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "case_manifest.json").read_text(encoding="utf-8"))["rows"]
    report = json.loads((temp_out_dir / "carryover_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    gate = payload["summary"]["gate"]
    exactness_rows = report["exactness_rows"]
    coverage_rows = report["coverage_rows"]
    kernel_rollup_rows = report["kernel_rollup_rows"]

    assert payload["summary"]["current_active_docs_only_stage"] == (
        "h55_post_h54_useful_kernel_reentry_packet"
    )
    assert payload["summary"]["current_post_h54_planning_bundle"] == (
        "f30_post_h54_useful_kernel_bridge_bundle"
    )
    assert payload["summary"]["active_runtime_lane"] == "r60_origin_compiled_useful_kernel_carryover_gate"
    assert gate["lane_verdict"] == "compiled_useful_kernel_carryover_supported_exactly"
    assert gate["planned_variant_count"] == 5
    assert gate["executed_variant_count"] == 5
    assert gate["exact_variant_count"] == 5
    assert gate["failed_variant_count"] == 0
    assert gate["planned_kernel_count"] == 2
    assert gate["exact_kernel_count"] == 2
    assert gate["exact_kernel_ids"] == ["count_nonzero_i32_buffer", "sum_i32_buffer"]
    assert gate["translation_identity_exact_count"] == 5
    assert gate["linear_exact_variant_count"] == 5
    assert gate["accelerated_exact_variant_count"] == 5
    assert gate["compiler_work_leakage_break_count"] == 0
    assert gate["next_required_packet"] == "r61_origin_compiled_useful_kernel_value_gate"
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["blocked_count"] == 0
    assert stop_rule["stop_rule_triggered"] is False
    assert stop_rule["first_failure"] is None
    assert report["first_failure"] is None
    assert len(manifest_rows) == 5
    assert len(exactness_rows) == 5
    assert len(coverage_rows) == 5
    assert len(kernel_rollup_rows) == 2
    assert {row["kernel_id"] for row in exactness_rows} == {
        "sum_i32_buffer",
        "count_nonzero_i32_buffer",
    }
    assert all(row["translation_identity_match"] for row in exactness_rows)
    assert all(row["compiled_spec_trace_match"] for row in exactness_rows)
    assert all(row["compiled_spec_final_state_match"] for row in exactness_rows)
    assert all(row["compiled_to_canonical_trace_match"] for row in exactness_rows)
    assert all(row["compiled_to_canonical_final_state_match"] for row in exactness_rows)
    assert all(row["compiled_to_lowered_trace_match"] for row in exactness_rows)
    assert all(row["compiled_to_lowered_final_state_match"] for row in exactness_rows)
    assert all(row["linear_exact_trace_match"] for row in exactness_rows)
    assert all(row["linear_exact_final_state_match"] for row in exactness_rows)
    assert all(row["accelerated_exact_trace_match"] for row in exactness_rows)
    assert all(row["accelerated_exact_final_state_match"] for row in exactness_rows)

    sum_row = next(row for row in exactness_rows if row["variant_id"] == "sum_len6_shifted_base")
    assert sum_row["compiled_declared_memory"]["sum_output"] == 13

    count_row = next(row for row in exactness_rows if row["variant_id"] == "count_mixed_len9_shifted_base")
    assert count_row["compiled_declared_memory"]["count_nonzero_output"] == 5

    assert claim_packet["distilled_result"]["selected_outcome"] == (
        "compiled_useful_kernel_carryover_supported_exactly"
    )
    assert claim_packet["distilled_result"]["admitted_kernel_suite"] == [
        "sum_i32_buffer",
        "count_nonzero_i32_buffer",
    ]
