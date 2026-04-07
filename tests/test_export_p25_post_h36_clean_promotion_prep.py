from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p25_post_h36_clean_promotion_prep.py"
    spec = importlib.util.spec_from_file_location("export_p25_post_h36_clean_promotion_prep", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p25_writes_clean_promotion_prep_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P25_post_h36_clean_promotion_prep"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "p25_post_h36_clean_promotion_prep"
    assert payload["summary"]["source_of_truth_branch"] == "wip/h35-r40-p24-exec"
    assert payload["summary"]["clean_prep_branch"] == "wip/p25-f15-h37-exec"
    assert payload["summary"]["target_branch"] == "main"
    assert payload["summary"]["promotion_mode"] == "prepare_only"
    assert payload["summary"]["merge_authorized"] is False
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert len(snapshot_rows) == 3
