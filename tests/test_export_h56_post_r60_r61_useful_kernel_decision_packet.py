from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module(script_name: str, module_name: str):
    module_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h56_writes_actual_decision_packet(tmp_path: Path) -> None:
    r60_module = _load_module(
        "export_r60_origin_compiled_useful_kernel_carryover_gate.py",
        "export_r60_origin_compiled_useful_kernel_carryover_gate",
    )
    r61_module = _load_module(
        "export_r61_origin_compiled_useful_kernel_value_gate.py",
        "export_r61_origin_compiled_useful_kernel_value_gate",
    )
    h56_module = _load_module(
        "export_h56_post_r60_r61_useful_kernel_decision_packet.py",
        "export_h56_post_r60_r61_useful_kernel_decision_packet",
    )

    temp_r60_out_dir = tmp_path / "R60_origin_compiled_useful_kernel_carryover_gate"
    temp_r61_out_dir = tmp_path / "R61_origin_compiled_useful_kernel_value_gate"
    temp_h56_out_dir = tmp_path / "H56_post_r60_r61_useful_kernel_decision_packet"

    original_r60_out_dir = r60_module.OUT_DIR
    original_r61_out_dir = r61_module.OUT_DIR
    original_h56_out_dir = h56_module.OUT_DIR
    original_r61_r60_summary_path = r61_module.R60_SUMMARY_PATH
    original_h56_r60_summary_path = h56_module.R60_SUMMARY_PATH
    original_h56_r61_summary_path = h56_module.R61_SUMMARY_PATH

    r60_module.OUT_DIR = temp_r60_out_dir
    r60_module.main()

    r61_module.OUT_DIR = temp_r61_out_dir
    r61_module.R60_SUMMARY_PATH = temp_r60_out_dir / "summary.json"
    r61_module.main()

    h56_module.OUT_DIR = temp_h56_out_dir
    h56_module.R60_SUMMARY_PATH = temp_r60_out_dir / "summary.json"
    h56_module.R61_SUMMARY_PATH = temp_r61_out_dir / "summary.json"

    try:
        h56_module.main()
    finally:
        r60_module.OUT_DIR = original_r60_out_dir
        r61_module.OUT_DIR = original_r61_out_dir
        h56_module.OUT_DIR = original_h56_out_dir
        r61_module.R60_SUMMARY_PATH = original_r61_r60_summary_path
        h56_module.R60_SUMMARY_PATH = original_h56_r60_summary_path
        h56_module.R61_SUMMARY_PATH = original_h56_r61_summary_path

    payload = json.loads((temp_h56_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_h56_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_h56_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot = json.loads((temp_h56_out_dir / "snapshot.json").read_text(encoding="utf-8"))

    assert payload["summary"]["active_stage"] == "h56_post_r60_r61_useful_kernel_decision_packet"
    assert payload["summary"]["selected_outcome"] == (
        "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value"
    )
    assert payload["summary"]["current_downstream_scientific_lane"] == (
        "no_active_downstream_runtime_lane"
    )
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["blocked_count"] == 0
    assert claim_packet["distilled_result"]["preserved_prior_reentry_packet"] == (
        "h55_post_h54_useful_kernel_reentry_packet"
    )
    assert len(snapshot["rows"]) == 3
