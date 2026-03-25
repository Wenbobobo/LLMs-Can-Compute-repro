from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h55_post_h54_useful_kernel_reentry_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h55_post_h54_useful_kernel_reentry_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h55_writes_actual_reentry_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H55_post_h54_useful_kernel_reentry_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))

    assert payload["summary"]["active_stage"] == "h55_post_h54_useful_kernel_reentry_packet"
    assert payload["summary"]["selected_outcome"] == "authorize_useful_kernel_carryover_through_r60_first"
    assert payload["summary"]["only_next_runtime_candidate_if_activated"] == (
        "r60_origin_compiled_useful_kernel_carryover_gate"
    )
    assert payload["summary"]["next_required_lane_if_activated"] == (
        "r60_origin_compiled_useful_kernel_carryover_gate"
    )
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["blocked_count"] == 0
    assert claim_packet["distilled_result"]["current_low_priority_wave"] == (
        "p39_post_h54_successor_worktree_hygiene_sync"
    )
    assert len(snapshot["rows"]) == 2
