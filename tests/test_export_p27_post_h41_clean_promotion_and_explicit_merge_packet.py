from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p27_post_h41_clean_promotion_and_explicit_merge_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p27_post_h41_clean_promotion_and_explicit_merge_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p27_writes_clean_promotion_and_explicit_merge_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P27_post_h41_clean_promotion_and_explicit_merge_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "p27_post_h41_clean_promotion_and_explicit_merge_packet"
    assert payload["summary"]["current_clean_source_branch"] == "wip/h41-r43-mainline"
    assert payload["summary"]["explicit_merge_branch"] == "wip/p27-promotion-merge"
    assert payload["summary"]["target_branch"] == "main"
    assert payload["summary"]["promotion_mode"] == "explicit_merge_wave"
    assert payload["summary"]["merge_recommended"] is False
    assert payload["summary"]["merge_executed"] is False
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["source_branch_synced_to_origin"] is True
    assert payload["summary"]["ahead_of_main_commit_count"] >= 1
    assert payload["summary"]["artifact_state"] == "not_present_on_current_source_branch"
    assert len(snapshot_rows) == 3
