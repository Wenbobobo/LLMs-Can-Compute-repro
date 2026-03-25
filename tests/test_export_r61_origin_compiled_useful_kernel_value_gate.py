from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r61_origin_compiled_useful_kernel_value_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r61_origin_compiled_useful_kernel_value_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_r60_module():
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


def test_export_r61_writes_actual_value_gate(tmp_path: Path) -> None:
    r60_module = _load_r60_module()
    original_r60_out_dir = r60_module.OUT_DIR
    temp_r60_out_dir = tmp_path / "R60_origin_compiled_useful_kernel_carryover_gate"
    r60_module.OUT_DIR = temp_r60_out_dir
    try:
        r60_module.main()
    finally:
        r60_module.OUT_DIR = original_r60_out_dir

    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    original_r60_summary_path = module.R60_SUMMARY_PATH
    temp_out_dir = tmp_path / "R61_origin_compiled_useful_kernel_value_gate"
    module.OUT_DIR = temp_out_dir
    module.R60_SUMMARY_PATH = temp_r60_out_dir / "summary.json"

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.R60_SUMMARY_PATH = original_r60_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))

    gate = payload["summary"]["gate"]
    comparator_rows = snapshot["rows"]

    assert payload["summary"]["current_completed_r60_gate"] == (
        "r60_origin_compiled_useful_kernel_carryover_gate"
    )
    assert payload["summary"]["active_runtime_lane"] == "r61_origin_compiled_useful_kernel_value_gate"
    assert gate["lane_verdict"] == "compiled_useful_kernel_route_lacks_bounded_value"
    assert gate["planned_case_count"] == 5
    assert gate["executed_case_count"] == 5
    assert gate["exact_case_count"] == 5
    assert gate["external_exact_case_count"] == 5
    assert gate["selected_h56_outcome"] == (
        "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value"
    )
    assert gate["next_required_packet"] == "h56_post_r60_r61_useful_kernel_decision_packet"
    assert payload["summary"]["pass_count"] == len(checklist_rows) - 1
    assert payload["summary"]["blocked_count"] == 1
    assert len(comparator_rows) == 5
    assert all(row["source_spec_trace_match"] for row in comparator_rows)
    assert all(row["source_spec_final_state_match"] for row in comparator_rows)
    assert all(row["source_to_lowered_trace_match"] for row in comparator_rows)
    assert all(row["source_to_lowered_final_state_match"] for row in comparator_rows)
    assert all(row["linear_exact_trace_match"] for row in comparator_rows)
    assert all(row["linear_exact_final_state_match"] for row in comparator_rows)
    assert all(row["accelerated_exact_trace_match"] for row in comparator_rows)
    assert all(row["accelerated_exact_final_state_match"] for row in comparator_rows)
    assert all(row["external_exact_final_value_match"] for row in comparator_rows)
    assert all(row["compile_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["trace_lower_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["source_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["linear_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["accelerated_mean_seconds"] > 0.0 for row in comparator_rows)
    assert all(row["external_mean_seconds"] > 0.0 for row in comparator_rows)
    assert gate["accelerated_end_to_end_faster_than_external_count"] == 0
    assert claim_packet["distilled_result"]["selected_outcome"] == (
        "compiled_useful_kernel_route_lacks_bounded_value"
    )
    assert claim_packet["distilled_result"]["selected_h56_outcome"] == (
        "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value"
    )
