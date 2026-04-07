from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r49_origin_useful_case_numeric_scaling_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r49_origin_useful_case_numeric_scaling_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r49_writes_useful_case_numeric_scaling_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R49_origin_useful_case_numeric_scaling_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "case_manifest.json").read_text(encoding="utf-8"))["rows"]
    exactness_report = json.loads((temp_out_dir / "exactness_report.json").read_text(encoding="utf-8"))
    precision_report = json.loads((temp_out_dir / "precision_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    exactness_rows = exactness_report["exactness_rows"]
    exactness_bucket_rows = exactness_report["exactness_bucket_rows"]
    kernel_rows = exactness_report["kernel_rows"]
    screening_rows = precision_report["screening_rows"]
    case_summary_rows = precision_report["case_summary_rows"]
    bucket_summary_rows = precision_report["bucket_summary_rows"]
    gate = payload["summary"]["gate"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h47_post_r48_useful_case_bridge_refreeze"
    assert payload["summary"]["active_runtime_lane"] == "r49_origin_useful_case_numeric_scaling_gate"
    assert payload["summary"]["activation_packet"] == "h47_post_r48_useful_case_bridge_refreeze"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_exact_first_planning_bundle"] == "f23_post_h47_numeric_scaling_bundle"
    assert gate["lane_verdict"] == "numeric_scaling_survives_through_bucket_c"
    assert gate["planned_case_count"] == 9
    assert gate["exact_case_count"] == 9
    assert gate["failed_case_count"] == 0
    assert gate["bucket_count"] == 3
    assert gate["kernel_count"] == 3
    assert gate["precision_row_count"] == 30
    assert gate["sampled_float64_reference_case_count"] == 3
    assert gate["single_head_failure_case_count"] == 7
    assert gate["decomposition_recovery_case_count"] == 7
    assert gate["bucket_a_admitted_float32_recovery_exact_regimes"] == [
        "float32_radix2",
        "float32_block_recentered",
    ]
    assert gate["bucket_b_admitted_float32_recovery_exact_regimes"] == [
        "float32_radix2",
        "float32_block_recentered",
    ]
    assert gate["bucket_c_admitted_float32_recovery_exact_regimes"] == [
        "float32_radix2",
        "float32_block_recentered",
    ]
    assert gate["next_required_packet"] == "h48_post_r49_numeric_scaling_decision_packet"
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 9
    assert len(exactness_rows) == 9
    assert len(exactness_bucket_rows) == 3
    assert len(kernel_rows) == 3
    assert len(screening_rows) == 30
    assert len(case_summary_rows) == 9
    assert len(bucket_summary_rows) == 3

    verdict_by_variant = {row["variant_id"]: row["verdict"] for row in exactness_rows}
    assert verdict_by_variant["sum_len64_shift4096"] == "exact"
    assert verdict_by_variant["count_len72_dense_shift4096"] == "exact"
    assert verdict_by_variant["histogram_len64_lowbin_shift4096"] == "exact"

    sum_row = next(row for row in exactness_rows if row["variant_id"] == "sum_len64_shift4096")
    assert sum_row["free_running_declared_memory"]["sum_output"] == 96

    count_row = next(row for row in exactness_rows if row["variant_id"] == "count_len72_dense_shift4096")
    assert count_row["free_running_declared_memory"]["count_nonzero_output"] == 72

    histogram_row = next(row for row in exactness_rows if row["variant_id"] == "histogram_len64_lowbin_shift4096")
    assert histogram_row["free_running_declared_memory"]["histogram_bin_0"] == 16
    assert histogram_row["free_running_declared_memory"]["histogram_bin_1"] == 16
    assert histogram_row["free_running_declared_memory"]["histogram_bin_2"] == 16
    assert histogram_row["free_running_declared_memory"]["histogram_bin_3"] == 16

    count_case_summary = next(row for row in case_summary_rows if row["variant_id"] == "count_len18_dense_shift256")
    assert count_case_summary["float32_single_head_passed"] is False
    assert count_case_summary["float32_radix2_passed"] is True
    assert count_case_summary["float32_block_recentered_passed"] is True
    assert count_case_summary["float64_reference_sampled"] is True
    assert count_case_summary["float64_reference_passed"] is True

    histogram_case_summary = next(row for row in case_summary_rows if row["variant_id"] == "histogram_len16_lowbin_shift256")
    assert histogram_case_summary["float32_single_head_passed"] is True
    assert histogram_case_summary["admitted_float32_recovery_regimes"] == [
        "float32_radix2",
        "float32_block_recentered",
    ]

    bucket_b_summary = next(row for row in bucket_summary_rows if row["bucket_id"] == "bucket_b_4x")
    assert bucket_b_summary["single_head_failed_case_count"] == 3
    assert bucket_b_summary["bucket_verdict"] == "admitted_float32_survives"
