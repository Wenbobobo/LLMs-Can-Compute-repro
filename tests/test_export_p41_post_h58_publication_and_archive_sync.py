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


def test_export_p41_writes_publication_archive_sync_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p41_post_h58_publication_and_archive_sync.py",
        "export_p41_post_h58_publication_and_archive_sync",
    )

    temp_h59_summary = tmp_path / "h59_summary.json"
    temp_h59_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_gitignore = tmp_path / ".gitignore"
    temp_gitignore.write_text(
        "\n".join(
            [
                "results/**/probe_read_rows.json",
                "results/**/per_read_rows.json",
                "results/**/trace_rows.json",
                "results/**/step_rows.json",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h59_summary_path = module.H59_SUMMARY_PATH
    original_gitignore_path = module.GITIGNORE_PATH
    original_git_output = module.git_output
    temp_out_dir = tmp_path / "P41_post_h58_publication_and_archive_sync"
    module.OUT_DIR = temp_out_dir
    module.H59_SUMMARY_PATH = temp_h59_summary
    module.GITIGNORE_PATH = temp_gitignore
    module.git_output = lambda _args: ""
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H59_SUMMARY_PATH = original_h59_summary_path
        module.GITIGNORE_PATH = original_gitignore_path
        module.git_output = original_git_output

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "publication_archive_surfaces_synced_to_h59_gap_state"
    assert payload["summary"]["tracked_large_artifact_count"] == 0
    assert payload["summary"]["raw_row_ignore_rules_present"] is True
