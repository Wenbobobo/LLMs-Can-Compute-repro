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


def test_export_r62_writes_negative_native_value_discriminator(tmp_path: Path) -> None:
    f31_module = _load_module(
        "export_f31_post_h56_final_discriminating_value_boundary_bundle.py",
        "export_f31_post_h56_final_discriminating_value_boundary_bundle_for_r62",
    )
    h57_module = _load_module(
        "export_h57_post_h56_last_discriminator_authorization_packet.py",
        "export_h57_post_h56_last_discriminator_authorization_packet_for_r62",
    )
    r62_module = _load_module(
        "export_r62_origin_native_useful_kernel_value_discriminator_gate.py",
        "export_r62_origin_native_useful_kernel_value_discriminator_gate",
    )

    temp_f31_out_dir = tmp_path / "F31_post_h56_final_discriminating_value_boundary_bundle"
    temp_h57_out_dir = tmp_path / "H57_post_h56_last_discriminator_authorization_packet"
    temp_r62_out_dir = tmp_path / "R62_origin_native_useful_kernel_value_discriminator_gate"

    original_f31_out_dir = f31_module.OUT_DIR
    original_h57_out_dir = h57_module.OUT_DIR
    original_h57_f31_summary_path = h57_module.F31_SUMMARY_PATH
    original_r62_out_dir = r62_module.OUT_DIR
    original_r62_h57_summary_path = r62_module.H57_SUMMARY_PATH
    original_r62_warmup = r62_module.WARMUP_REPEATS
    original_r62_repeats = r62_module.TIMING_REPEATS

    f31_module.OUT_DIR = temp_f31_out_dir
    f31_module.main()

    h57_module.OUT_DIR = temp_h57_out_dir
    h57_module.F31_SUMMARY_PATH = temp_f31_out_dir / "summary.json"
    h57_module.main()

    r62_module.OUT_DIR = temp_r62_out_dir
    r62_module.H57_SUMMARY_PATH = temp_h57_out_dir / "summary.json"
    r62_module.WARMUP_REPEATS = 0
    r62_module.TIMING_REPEATS = 1
    try:
        r62_module.main()
    finally:
        f31_module.OUT_DIR = original_f31_out_dir
        h57_module.OUT_DIR = original_h57_out_dir
        h57_module.F31_SUMMARY_PATH = original_h57_f31_summary_path
        r62_module.OUT_DIR = original_r62_out_dir
        r62_module.H57_SUMMARY_PATH = original_r62_h57_summary_path
        r62_module.WARMUP_REPEATS = original_r62_warmup
        r62_module.TIMING_REPEATS = original_r62_repeats

    payload = json.loads((temp_r62_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_r62_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    leakage_rows = json.loads((temp_r62_out_dir / "leakage_checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_r62_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot = json.loads((temp_r62_out_dir / "snapshot.json").read_text(encoding="utf-8"))

    assert payload["summary"]["gate"]["lane_verdict"] == "native_useful_kernel_route_lacks_bounded_value"
    assert payload["summary"]["gate"]["executed_case_count"] == 4
    assert payload["summary"]["gate"]["exact_case_count"] == 4
    assert payload["summary"]["gate"]["selected_h58_outcome"] == (
        "stop_as_mechanism_supported_but_no_bounded_executor_value"
    )
    assert payload["summary"]["pass_count"] + payload["summary"]["blocked_count"] == len(checklist_rows)
    assert len(leakage_rows) == 4
    assert claim_packet["distilled_result"]["next_required_packet"] == (
        "h58_post_r62_origin_value_boundary_closeout_packet"
    )
    assert len(snapshot["execution_report"]["comparator_rows"]) == 4
