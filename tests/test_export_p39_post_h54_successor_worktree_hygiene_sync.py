from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p39_post_h54_successor_worktree_hygiene_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p39_post_h54_successor_worktree_hygiene_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p39_writes_actual_hygiene_sidecar(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P39_post_h54_successor_worktree_hygiene_sync"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))

    assert payload["summary"]["current_active_stage"] == (
        "h56_post_r60_r61_useful_kernel_decision_packet"
    )
    assert payload["summary"]["current_low_priority_wave"] == (
        "p39_post_h54_successor_worktree_hygiene_sync"
    )
    assert payload["summary"]["selected_outcome"] == "successor_worktree_hygiene_rules_active_and_clean"
    assert payload["summary"]["tracked_large_artifact_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["blocked_count"] == 0
    assert claim_packet["distilled_result"]["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert len(snapshot["rows"]) == 3
