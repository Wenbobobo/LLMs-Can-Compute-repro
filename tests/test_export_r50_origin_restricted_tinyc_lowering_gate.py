from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r50_origin_restricted_tinyc_lowering_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r50_origin_restricted_tinyc_lowering_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r50_writes_restricted_tinyc_lowering_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R50_origin_restricted_tinyc_lowering_gate"
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
    kernel_rollup_rows = lowering_report["kernel_rollup_rows"]
    gate = payload["summary"]["gate"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h48_post_r49_numeric_scaling_decision_packet"
    assert payload["summary"]["current_post_h48_planning_bundle"] == (
        "f25_post_h48_restricted_tinyc_lowering_bundle"
    )
    assert payload["summary"]["active_runtime_lane"] == "r50_origin_restricted_tinyc_lowering_gate"
    assert gate["lane_verdict"] == "restricted_tinyc_lowering_supported_narrowly"
    assert gate["planned_variant_count"] == 8
    assert gate["executed_variant_count"] == 8
    assert gate["exact_variant_count"] == 8
    assert gate["failed_variant_count"] == 0
    assert gate["planned_kernel_count"] == 3
    assert gate["exact_kernel_count"] == 3
    assert gate["translation_identity_exact_count"] == 8
    assert gate["next_required_packet"] == "h49_post_r50_tinyc_lowering_decision_packet"
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 8
    assert len(exactness_rows) == 8
    assert len(kernel_rollup_rows) == 3

    sum_row = next(row for row in exactness_rows if row["variant_id"] == "sum_len6_shifted_base")
    assert sum_row["compiled_declared_memory"]["sum_output"] == 13

    count_row = next(row for row in exactness_rows if row["variant_id"] == "count_mixed_len9_shifted_base")
    assert count_row["compiled_declared_memory"]["count_nonzero_output"] == 5

    histogram_row = next(row for row in exactness_rows if row["variant_id"] == "histogram_wide_len10_shifted_base")
    assert histogram_row["compiled_declared_memory"]["histogram_bin_0"] == 2
    assert histogram_row["compiled_declared_memory"]["histogram_bin_3"] == 2
    assert histogram_row["compiled_declared_memory"]["histogram_bin_7"] == 3
    assert histogram_row["compiled_declared_memory"]["histogram_bin_12"] == 1
    assert histogram_row["compiled_declared_memory"]["histogram_bin_15"] == 2
