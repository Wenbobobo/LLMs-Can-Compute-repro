from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r44_origin_restricted_wasm_useful_case_execution_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r44_origin_restricted_wasm_useful_case_execution_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r44_writes_restricted_useful_case_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R44_origin_restricted_wasm_useful_case_execution_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "lowering_manifest.json").read_text(encoding="utf-8"))["rows"]
    kernel_suite_report = json.loads((temp_out_dir / "kernel_suite_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    exactness_rows = kernel_suite_report["exactness_rows"]
    cost_rows = kernel_suite_report["cost_rows"]
    gate = payload["summary"]["gate"]

    assert payload["summary"]["active_runtime_lane"] == "r44_origin_restricted_wasm_useful_case_execution_gate"
    assert payload["summary"]["activation_packet"] == "h42_post_r43_route_selection_packet"
    assert payload["summary"]["current_completed_exact_runtime_gate"] == (
        "r43_origin_bounded_memory_small_vm_execution_gate"
    )
    assert gate["lane_verdict"] == "useful_case_surface_supported_narrowly"
    assert gate["route_posture"] == "keep_semantic_boundary_route"
    assert gate["planned_kernel_count"] == 3
    assert gate["executed_kernel_count"] == 3
    assert gate["exact_kernel_count"] == 3
    assert gate["exact_prefix_count"] == 3
    assert gate["article_level_substrate_evidence_exceeded_narrowly"] is True
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 3
    assert len(exactness_rows) == 3
    assert len(cost_rows) == 3

    verdict_by_kernel = {row["kernel_id"]: row["verdict"] for row in exactness_rows}
    assert verdict_by_kernel["sum_i32_buffer"] == "exact"
    assert verdict_by_kernel["count_nonzero_i32_buffer"] == "exact"
    assert verdict_by_kernel["histogram16_u8"] == "exact"

    histogram_row = next(row for row in exactness_rows if row["kernel_id"] == "histogram16_u8")
    assert histogram_row["free_running_declared_memory"]["histogram_bin_1"] == 1
    assert histogram_row["free_running_declared_memory"]["histogram_bin_3"] == 2
    assert histogram_row["free_running_declared_memory"]["histogram_bin_15"] == 1
