from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_f30_post_h54_useful_kernel_bridge_bundle.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_f30_post_h54_useful_kernel_bridge_bundle",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f30_writes_saved_successor_bundle(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "F30_post_h54_useful_kernel_bridge_bundle"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "f30_post_h54_useful_kernel_bridge_bundle"
    assert payload["summary"]["current_active_docs_only_stage"] == (
        "h54_post_r58_r59_compiled_boundary_decision_packet"
    )
    assert payload["summary"]["selected_outcome"] == "post_h54_useful_kernel_stopgo_bundle_saved"
    assert payload["summary"]["only_followup_packet"] == "h55_post_h54_useful_kernel_reentry_packet"
    assert payload["summary"]["only_next_runtime_candidate"] == (
        "r60_origin_compiled_useful_kernel_carryover_gate"
    )
    assert payload["summary"]["saved_successor_low_priority_wave"] == (
        "p39_post_h54_successor_worktree_hygiene_sync"
    )
    assert payload["summary"]["next_required_lane_if_activated"] == (
        "r60_origin_compiled_useful_kernel_carryover_gate"
    )
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert len(payload["summary"]["only_conditional_later_sequence"]) == 2
    assert claim_packet["distilled_result"]["selected_outcome"] == (
        "post_h54_useful_kernel_stopgo_bundle_saved"
    )
    assert len(snapshot_rows) == 7

