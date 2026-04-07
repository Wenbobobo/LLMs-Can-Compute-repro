from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p56_post_h64_clean_merge_candidate_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p56_post_h64_clean_merge_candidate_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p56_writes_clean_merge_candidate_summary(tmp_path: Path) -> None:
    module = _load_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P56_post_h64_clean_merge_candidate_packet"
    module.OUT_DIR = temp_out_dir
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_descendant_merge_candidate_staged_without_merge_execution"
    assert payload["summary"]["merge_execution_state"] is False
    assert payload["summary"]["blocked_count"] == 0
