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


def test_export_p45_writes_clean_descendant_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p45_post_h60_clean_descendant_integration_readiness.py",
        "export_p45_post_h60_clean_descendant_integration_readiness",
    )

    temp_h60_summary = tmp_path / "h60_summary.json"
    temp_h60_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "remain_planning_only_and_prepare_stop_or_archive"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_p43_summary = tmp_path / "p43_summary.json"
    temp_p43_summary.write_text(
        json.dumps(
            {"summary": {"merge_posture": "clean_descendant_only_never_dirty_root_main"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h60_summary_path = module.H60_SUMMARY_PATH
    original_p43_summary_path = module.P43_SUMMARY_PATH
    original_git_output = module.git_output
    original_branch_exists = module.branch_exists
    original_divergence_counts = module.divergence_counts

    def fake_git_output(args: list[str], *, check: bool = True) -> str:
        if args == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return "wip/f36-post-h60-archive-first-consolidation\n"
        if args == ["worktree", "list", "--porcelain"]:
            return (
                "worktree D:/zWenbo/AI/LLMCompute\n"
                "HEAD 1111111111111111111111111111111111111111\n"
                "branch refs/heads/wip/root-main-parking-2026-03-24\n\n"
                "worktree D:/zWenbo/AI/wt/f36-post-h60-archive-first-consolidation\n"
                "HEAD 2222222222222222222222222222222222222222\n"
                "branch refs/heads/wip/f36-post-h60-archive-first-consolidation\n"
            )
        raise AssertionError(args)

    temp_out_dir = tmp_path / "P45_post_h60_clean_descendant_integration_readiness"
    module.OUT_DIR = temp_out_dir
    module.H60_SUMMARY_PATH = temp_h60_summary
    module.P43_SUMMARY_PATH = temp_p43_summary
    module.git_output = fake_git_output
    module.branch_exists = lambda branch: branch == "wip/f34-post-h59-archive-and-reopen-screen"
    module.divergence_counts = lambda base, target: {"base_only": 0, "target_only": 3}
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H60_SUMMARY_PATH = original_h60_summary_path
        module.P43_SUMMARY_PATH = original_p43_summary_path
        module.git_output = original_git_output
        module.branch_exists = original_branch_exists
        module.divergence_counts = original_divergence_counts

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_descendant_successor_line_prepared_for_later_non_root_integration"
    assert payload["summary"]["current_branch"] == "wip/f36-post-h60-archive-first-consolidation"
    assert payload["summary"]["predecessor_divergence_target_only"] == 3
