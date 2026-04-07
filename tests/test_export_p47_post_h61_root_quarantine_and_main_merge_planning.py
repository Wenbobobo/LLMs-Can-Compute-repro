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


def test_export_p47_writes_root_quarantine_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p47_post_h61_root_quarantine_and_main_merge_planning.py",
        "export_p47_post_h61_root_quarantine_and_main_merge_planning",
    )

    temp_h61_summary = tmp_path / "h61_summary.json"
    temp_h61_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "archive_first_consolidation_becomes_default_posture"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h61_summary_path = module.H61_SUMMARY_PATH
    original_git_output = module.git_output
    original_root_worktree = module.ROOT_MAIN_WORKTREE

    def fake_git_output(args: list[str], cwd: Path, *, check: bool = True) -> str:
        if cwd == module.ROOT and args == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return "wip/f37-post-h61-hygiene-first-reauth-prep\n"
        if cwd == module.ROOT_MAIN_WORKTREE and args == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return "wip/root-main-parking-2026-03-24\n"
        if cwd == module.ROOT_MAIN_WORKTREE and args == ["status", "--porcelain=v1"]:
            return " M README.md\n?? docs/Origin/QA1.md\n"
        if cwd == module.ROOT and args == ["merge-base", "wip/root-main-parking-2026-03-24", "wip/f36-post-h60-archive-first-consolidation"]:
            return "abc123\n"
        raise AssertionError((cwd, args))

    temp_out_dir = tmp_path / "P47_post_h61_root_quarantine_and_main_merge_planning"
    module.OUT_DIR = temp_out_dir
    module.H61_SUMMARY_PATH = temp_h61_summary
    module.ROOT_MAIN_WORKTREE = Path("D:/fake/root")
    module.git_output = fake_git_output
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H61_SUMMARY_PATH = original_h61_summary_path
        module.git_output = original_git_output
        module.ROOT_MAIN_WORKTREE = original_root_worktree

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "quarantine_root_and_plan_main_merge_only"
    assert payload["summary"]["root_dirty_entry_count"] == 2
    assert payload["summary"]["root_has_untracked_entries"] is True

