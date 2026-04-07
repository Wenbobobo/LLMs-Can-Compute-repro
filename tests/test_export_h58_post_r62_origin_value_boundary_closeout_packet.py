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


def test_export_h58_writes_negative_value_boundary_closeout(tmp_path: Path) -> None:
    module = _load_module(
        "export_h58_post_r62_origin_value_boundary_closeout_packet.py",
        "export_h58_post_r62_origin_value_boundary_closeout_packet",
    )

    temp_h57_summary = tmp_path / "h57_summary.json"
    temp_h57_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "authorize_one_last_native_useful_kernel_value_discriminator_gate",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_r62_summary = tmp_path / "r62_summary.json"
    temp_r62_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "gate": {
                        "lane_verdict": "native_useful_kernel_route_lacks_bounded_value",
                        "selected_h58_outcome": "stop_as_mechanism_supported_but_no_bounded_executor_value",
                    }
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h57_summary_path = module.H57_SUMMARY_PATH
    original_r62_summary_path = module.R62_SUMMARY_PATH
    temp_out_dir = tmp_path / "H58_post_r62_origin_value_boundary_closeout_packet"

    module.OUT_DIR = temp_out_dir
    module.H57_SUMMARY_PATH = temp_h57_summary
    module.R62_SUMMARY_PATH = temp_r62_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H57_SUMMARY_PATH = original_h57_summary_path
        module.R62_SUMMARY_PATH = original_r62_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    assert payload["summary"]["active_stage"] == "h58_post_r62_origin_value_boundary_closeout_packet"
    assert payload["summary"]["selected_outcome"] == "stop_as_mechanism_supported_but_no_bounded_executor_value"
    assert payload["summary"]["current_downstream_scientific_lane"] == "no_active_downstream_runtime_lane"
    assert payload["summary"]["pass_count"] + payload["summary"]["blocked_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["completed_value_discriminator_gate"] == (
        "r62_origin_native_useful_kernel_value_discriminator_gate"
    )
