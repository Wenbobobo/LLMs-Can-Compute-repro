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


def test_export_p40_writes_successor_worktree_hygiene_sync(tmp_path: Path) -> None:
    module = _load_module(
        "export_p40_post_h56_successor_worktree_and_artifact_hygiene_sync.py",
        "export_p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
    )
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P40_post_h56_successor_worktree_and_artifact_hygiene_sync"
    module.OUT_DIR = temp_out_dir
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    assert payload["summary"]["current_low_priority_wave"] == (
        "p40_post_h56_successor_worktree_and_artifact_hygiene_sync"
    )
    assert payload["summary"]["selected_outcome"] == "successor_worktree_hygiene_rules_active_and_clean"
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["preferred_worktree_prefix"] == "D:/zWenbo/AI/wt/"
