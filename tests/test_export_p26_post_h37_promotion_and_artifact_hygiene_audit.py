from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_p26_post_h37_promotion_and_artifact_hygiene_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p26_post_h37_promotion_and_artifact_hygiene_audit",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p26_writes_promotion_and_artifact_hygiene_audit(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P26_post_h37_promotion_and_artifact_hygiene_audit"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "p26_post_h37_promotion_and_artifact_hygiene_audit"
    assert payload["summary"]["current_clean_audit_branch"] == "wip/f16-h38-p26-exec"
    assert payload["summary"]["preserved_prior_clean_source_branch"] == "wip/p25-f15-h37-exec"
    assert payload["summary"]["target_branch"] == "main"
    assert payload["summary"]["promotion_mode"] == "audit_only"
    assert payload["summary"]["merge_recommended"] is False
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["ahead_of_main_commit_count"] >= 1
    assert payload["summary"]["artifact_state"] == "not_present_on_current_source_branch"
    assert len(snapshot_rows) == 3
