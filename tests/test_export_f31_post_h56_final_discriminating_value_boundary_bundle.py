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


def test_export_f31_writes_final_discriminating_bundle(tmp_path: Path) -> None:
    module = _load_module(
        "export_f31_post_h56_final_discriminating_value_boundary_bundle.py",
        "export_f31_post_h56_final_discriminating_value_boundary_bundle",
    )
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "F31_post_h56_final_discriminating_value_boundary_bundle"
    module.OUT_DIR = temp_out_dir
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    assert payload["summary"]["planning_bundle"] == "f31_post_h56_final_discriminating_value_boundary_bundle"
    assert payload["summary"]["only_runtime_candidate"] == "r62_origin_native_useful_kernel_value_discriminator_gate"
    assert payload["summary"]["only_later_packet"] == "h58_post_r62_origin_value_boundary_closeout_packet"
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["blocked_count"] == 0
    assert claim_packet["distilled_result"]["current_low_priority_wave"] == (
        "p40_post_h56_successor_worktree_and_artifact_hygiene_sync"
    )
