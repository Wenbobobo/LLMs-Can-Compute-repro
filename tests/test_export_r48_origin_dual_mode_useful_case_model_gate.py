from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r48_origin_dual_mode_useful_case_model_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r48_origin_dual_mode_useful_case_model_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r48_writes_dual_mode_useful_case_model_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R48_origin_dual_mode_useful_case_model_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "execution_manifest.json").read_text(encoding="utf-8"))["rows"]
    mode_rows = json.loads((temp_out_dir / "mode_rows.json").read_text(encoding="utf-8"))["rows"]
    variant_rows = json.loads((temp_out_dir / "variant_rows.json").read_text(encoding="utf-8"))["rows"]
    kernel_rows = json.loads((temp_out_dir / "kernel_rows.json").read_text(encoding="utf-8"))["rows"]
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    gate = payload["summary"]["gate"]
    assert payload["summary"]["active_runtime_lane"] == "r48_origin_dual_mode_useful_case_model_gate"
    assert payload["summary"]["activation_packet"] == "h46_post_r47_frontend_bridge_decision_packet"
    assert payload["summary"]["current_completed_exact_frontend_bridge_gate"] == (
        "r47_origin_restricted_frontend_translation_gate"
    )
    assert gate["lane_verdict"] == "useful_case_model_lane_supported_without_replacing_exact"
    assert gate["mode_count"] == 2
    assert gate["exact_mode_count"] == 2
    assert gate["contract_variant_count"] == 8
    assert gate["contract_kernel_count"] == 3
    assert gate["variant_mode_row_count"] == 16
    assert gate["exact_variant_mode_row_count"] == 16
    assert gate["heldout_kernel_id"] == "histogram16_u8"
    assert gate["heldout_variant_count"] == 3
    assert gate["trainable_heldout_family_exact"] is True
    assert gate["next_required_packet"] == "h47_post_r48_useful_case_bridge_refreeze"
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 8
    assert len(mode_rows) == 2
    assert len(variant_rows) == 16
    assert len(kernel_rows) == 6

    mode_row_by_id = {row["mode_id"]: row for row in mode_rows}
    assert mode_row_by_id["compiled_weight_executor"]["exact_trace_accuracy"] == 1.0
    assert mode_row_by_id["compiled_weight_executor"]["exact_final_state_accuracy"] == 1.0
    assert mode_row_by_id["trainable_2d_executor"]["fit_train_sample_accuracy"] == 1.0
    assert mode_row_by_id["trainable_2d_executor"]["fit_train_exact_program_accuracy"] == 1.0
    assert mode_row_by_id["trainable_2d_executor"]["heldout_kernel_ids"] == ["histogram16_u8"]

    heldout_rows = [
        row
        for row in variant_rows
        if row["mode_id"] == "trainable_2d_executor" and row["kernel_id"] == "histogram16_u8"
    ]
    assert len(heldout_rows) == 3
    assert all(row["verdict"] == "exact" for row in heldout_rows)
