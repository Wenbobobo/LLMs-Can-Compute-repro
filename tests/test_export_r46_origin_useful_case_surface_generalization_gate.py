from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r46_origin_useful_case_surface_generalization_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r46_origin_useful_case_surface_generalization_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r46_writes_useful_case_surface_generalization_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R46_origin_useful_case_surface_generalization_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "case_manifest.json").read_text(encoding="utf-8"))["rows"]
    surface_report = json.loads((temp_out_dir / "surface_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    exactness_rows = surface_report["exactness_rows"]
    kernel_rollup_rows = surface_report["kernel_rollup_rows"]
    gate = payload["summary"]["gate"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h44_post_h43_route_reauthorization_packet"
    assert payload["summary"]["active_runtime_lane"] == "r46_origin_useful_case_surface_generalization_gate"
    assert payload["summary"]["activation_packet"] == "h44_post_h43_route_reauthorization_packet"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_exact_first_planning_bundle"] == "f21_post_h43_exact_useful_case_expansion_bundle"
    assert gate["lane_verdict"] == "surface_generalizes_narrowly"
    assert gate["planned_variant_count"] == 8
    assert gate["executed_variant_count"] == 8
    assert gate["exact_variant_count"] == 8
    assert gate["failed_variant_count"] == 0
    assert gate["planned_kernel_count"] == 3
    assert gate["exact_kernel_count"] == 3
    assert gate["next_required_lane"] == "h45_post_r46_surface_decision_packet"
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 8
    assert len(exactness_rows) == 8
    assert len(kernel_rollup_rows) == 3

    verdict_by_variant = {row["variant_id"]: row["verdict"] for row in exactness_rows}
    assert verdict_by_variant["sum_len6_shifted_base"] == "exact"
    assert verdict_by_variant["count_sparse_len8_shifted_base"] == "exact"
    assert verdict_by_variant["histogram_wide_len10_shifted_base"] == "exact"

    sum_row = next(row for row in exactness_rows if row["variant_id"] == "sum_len6_shifted_base")
    assert sum_row["free_running_declared_memory"]["sum_output"] == 13

    count_row = next(row for row in exactness_rows if row["variant_id"] == "count_sparse_len8_shifted_base")
    assert count_row["free_running_declared_memory"]["count_nonzero_output"] == 3

    histogram_row = next(row for row in exactness_rows if row["variant_id"] == "histogram_wide_len10_shifted_base")
    assert histogram_row["free_running_declared_memory"]["histogram_bin_0"] == 2
    assert histogram_row["free_running_declared_memory"]["histogram_bin_3"] == 2
    assert histogram_row["free_running_declared_memory"]["histogram_bin_7"] == 3
    assert histogram_row["free_running_declared_memory"]["histogram_bin_15"] == 2
