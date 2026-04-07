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


def test_export_p48_writes_promotion_prep_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p48_post_h61_clean_descendant_promotion_prep.py",
        "export_p48_post_h61_clean_descendant_promotion_prep",
    )

    temp_p45_summary = tmp_path / "p45_summary.json"
    temp_p45_summary.write_text(
        json.dumps({"summary": {"merge_posture": "clean_descendant_only_never_dirty_root_main"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_p47_summary = tmp_path / "p47_summary.json"
    temp_p47_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "quarantine_root_and_plan_main_merge_only"}}, indent=2) + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_p45_summary_path = module.P45_SUMMARY_PATH
    original_p47_summary_path = module.P47_SUMMARY_PATH
    original_git_output = module.git_output
    original_branch_exists = module.branch_exists

    def fake_git_output(args: list[str], *, check: bool = True) -> str:
        if args == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return "wip/f37-post-h61-hygiene-first-reauth-prep\n"
        if args == ["for-each-ref", "--format=%(upstream:short)", "refs/heads/wip/f36-post-h60-archive-first-consolidation"]:
            return "origin/wip/f36-post-h60-archive-first-consolidation\n"
        if args == ["for-each-ref", "--format=%(upstream:short)", "refs/heads/wip/f37-post-h61-hygiene-first-reauth-prep"]:
            return ""
        if args == ["diff", "--name-only", "wip/f36-post-h60-archive-first-consolidation..HEAD"]:
            return "docs/plans/2026-03-26-post-h61-hygiene-first-reauth-prep-design.md\n"
        if args == ["rev-list", "--count", "wip/f36-post-h60-archive-first-consolidation..HEAD"]:
            return "2\n"
        if args == ["status", "--porcelain=v1"]:
            return ""
        raise AssertionError(args)

    temp_out_dir = tmp_path / "P48_post_h61_clean_descendant_promotion_prep"
    module.OUT_DIR = temp_out_dir
    module.P45_SUMMARY_PATH = temp_p45_summary
    module.P47_SUMMARY_PATH = temp_p47_summary
    module.git_output = fake_git_output
    module.branch_exists = lambda branch: branch == "wip/f36-post-h60-archive-first-consolidation"
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P45_SUMMARY_PATH = original_p45_summary_path
        module.P47_SUMMARY_PATH = original_p47_summary_path
        module.git_output = original_git_output
        module.branch_exists = original_branch_exists

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_descendant_ready_for_later_explicit_promotion"
    assert payload["summary"]["candidate_commit_count"] == 2
    assert payload["summary"]["artifact_oversize_count"] == 0

