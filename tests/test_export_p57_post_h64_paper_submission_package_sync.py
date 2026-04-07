from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p57_post_h64_paper_submission_package_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p57_post_h64_paper_submission_package_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p57_writes_paper_submission_sync_summary(tmp_path: Path) -> None:
    module = _load_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P57_post_h64_paper_submission_package_sync"
    module.OUT_DIR = temp_out_dir
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "paper_submission_package_surfaces_synced_to_h64_followthrough_stack"
    assert payload["summary"]["blocked_count"] == 0
