from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r45_origin_dual_mode_model_mainline_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r45_origin_dual_mode_model_mainline_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r45_writes_dual_mode_model_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R45_origin_dual_mode_model_mainline_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "execution_manifest.json").read_text(encoding="utf-8"))["rows"]
    mode_rows = json.loads((temp_out_dir / "mode_rows.json").read_text(encoding="utf-8"))["rows"]
    family_rows = json.loads((temp_out_dir / "family_rows.json").read_text(encoding="utf-8"))["rows"]
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    gate = payload["summary"]["gate"]
    assert payload["summary"]["active_runtime_lane"] == "r45_origin_dual_mode_model_mainline_gate"
    assert payload["summary"]["current_exact_dependency"] == "r43_origin_bounded_memory_small_vm_execution_gate"
    assert gate["lane_verdict"] == "coequal_model_lane_supported_without_replacing_exact"
    assert gate["mode_count"] == 2
    assert gate["exact_mode_count"] == 2
    assert gate["contract_family_count"] == 5
    assert gate["family_mode_row_count"] == 10
    assert gate["exact_family_mode_row_count"] == 10
    assert gate["trainable_heldout_family_exact"] is True
    assert gate["next_required_packet"] == "h42_post_r43_route_selection_packet"
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 5
    assert len(mode_rows) == 2
    assert len(family_rows) == 10

    mode_row_by_id = {row["mode_id"]: row for row in mode_rows}
    assert mode_row_by_id["compiled_weight_executor"]["exact_trace_accuracy"] == 1.0
    assert mode_row_by_id["compiled_weight_executor"]["exact_final_state_accuracy"] == 1.0
    assert mode_row_by_id["trainable_2d_executor"]["fit_train_sample_accuracy"] == 1.0
    assert mode_row_by_id["trainable_2d_executor"]["fit_train_exact_program_accuracy"] == 1.0
    assert mode_row_by_id["trainable_2d_executor"]["heldout_family_ids"] == ["single_call_return_accumulator"]

    trainable_optional_rows = [
        row
        for row in family_rows
        if row["mode_id"] == "trainable_2d_executor" and row["family_id"] == "single_call_return_accumulator"
    ]
    assert len(trainable_optional_rows) == 1
    assert trainable_optional_rows[0]["verdict"] == "exact"
