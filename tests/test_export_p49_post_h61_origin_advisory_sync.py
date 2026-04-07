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


def test_export_p49_writes_origin_sync_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p49_post_h61_origin_advisory_sync.py",
        "export_p49_post_h61_origin_advisory_sync",
    )

    temp_h61_summary = tmp_path / "h61_summary.json"
    temp_h61_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "archive_first_consolidation_becomes_default_posture"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_p42_readme = tmp_path / "P42_README.md"
    temp_p42_readme.write_text("advisory\n", encoding="utf-8")
    required_files = []
    for name in ["Percepta.md", "Discuss1.md", "Discuss2.md", "Discuss3Pro.md", "QA1.md", "QA2.md"]:
        path = tmp_path / name
        path.write_text("ok\n", encoding="utf-8")
        required_files.append(path)

    original_out_dir = module.OUT_DIR
    original_h61_summary_path = module.H61_SUMMARY_PATH
    original_p42_readme = module.P42_MILESTONE_README
    original_required_files = module.REQUIRED_FILES
    temp_out_dir = tmp_path / "P49_post_h61_origin_advisory_sync"
    module.OUT_DIR = temp_out_dir
    module.H61_SUMMARY_PATH = temp_h61_summary
    module.P42_MILESTONE_README = temp_p42_readme
    module.REQUIRED_FILES = required_files
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H61_SUMMARY_PATH = original_h61_summary_path
        module.P42_MILESTONE_README = original_p42_readme
        module.REQUIRED_FILES = original_required_files

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "advisory_origin_materials_available_in_clean_line"
    assert payload["summary"]["synced_text_file_count"] == 6
    assert payload["summary"]["evidence_status"] == "advisory_only"
