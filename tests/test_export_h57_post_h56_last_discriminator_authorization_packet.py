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


def test_export_h57_writes_authorization_packet(tmp_path: Path) -> None:
    f31_module = _load_module(
        "export_f31_post_h56_final_discriminating_value_boundary_bundle.py",
        "export_f31_post_h56_final_discriminating_value_boundary_bundle_for_h57",
    )
    h57_module = _load_module(
        "export_h57_post_h56_last_discriminator_authorization_packet.py",
        "export_h57_post_h56_last_discriminator_authorization_packet",
    )

    temp_f31_out_dir = tmp_path / "F31_post_h56_final_discriminating_value_boundary_bundle"
    temp_h57_out_dir = tmp_path / "H57_post_h56_last_discriminator_authorization_packet"

    original_f31_out_dir = f31_module.OUT_DIR
    original_h57_out_dir = h57_module.OUT_DIR
    original_h57_f31_summary_path = h57_module.F31_SUMMARY_PATH

    f31_module.OUT_DIR = temp_f31_out_dir
    f31_module.main()

    h57_module.OUT_DIR = temp_h57_out_dir
    h57_module.F31_SUMMARY_PATH = temp_f31_out_dir / "summary.json"
    try:
        h57_module.main()
    finally:
        f31_module.OUT_DIR = original_f31_out_dir
        h57_module.OUT_DIR = original_h57_out_dir
        h57_module.F31_SUMMARY_PATH = original_h57_f31_summary_path

    payload = json.loads((temp_h57_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_h57_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_h57_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    assert payload["summary"]["active_stage"] == "h57_post_h56_last_discriminator_authorization_packet"
    assert payload["summary"]["selected_outcome"] == (
        "authorize_one_last_native_useful_kernel_value_discriminator_gate"
    )
    assert payload["summary"]["only_next_runtime_candidate"] == "r62_origin_native_useful_kernel_value_discriminator_gate"
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["blocked_count"] == 0
    assert claim_packet["distilled_result"]["only_later_packet"] == (
        "h58_post_r62_origin_value_boundary_closeout_packet"
    )
