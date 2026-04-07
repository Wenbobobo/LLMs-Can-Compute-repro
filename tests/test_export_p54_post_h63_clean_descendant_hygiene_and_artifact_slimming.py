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


def test_export_p54_writes_hygiene_artifact_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p54_post_h63_clean_descendant_hygiene_and_artifact_slimming.py",
        "export_p54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
    )

    temp_h63_summary = tmp_path / "h63_summary.json"
    temp_h63_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_p52_summary = tmp_path / "p52_summary.json"
    temp_p52_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "clean_descendant_hygiene_and_merge_prep_locked_without_dirty_root_merge"}}, indent=2)
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
    temp_merge_rules = tmp_path / "merge_prep_rules.md"
    temp_merge_rules.write_text(
        "\n".join(
            [
                "wip/f38-post-h62-archive-first-closeout",
                "wip/h64-post-h63-archive-first-freeze",
                "clean_descendant_only_never_dirty_root_main",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    temp_artifact_policy = tmp_path / "artifact_policy.md"
    temp_artifact_policy.write_text(
        "\n".join(
            [
                "surface_report.json",
                "10 MiB",
                "summary tables",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    temp_driver = tmp_path / "current_stage_driver.md"
    temp_driver.write_text(
        "\n".join(
            [
                "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
                "clean_descendant_only_never_dirty_root_main",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_root = module.ROOT
    original_h63 = module.H63_SUMMARY_PATH
    original_p52 = module.P52_SUMMARY_PATH
    original_git_output = module.git_output
    original_branch_exists = module.branch_exists
    original_merge_rules = module.MERGE_RULES_PATH
    original_artifact_policy = module.ARTIFACT_POLICY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH

    def fake_git_output(args: list[str], *, check: bool = True) -> str:
        if args == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return "wip/h64-post-h63-archive-first-freeze\n"
        if args == ["for-each-ref", "--format=%(upstream:short)", "refs/heads/wip/h64-post-h63-archive-first-freeze"]:
            return ""
        if args == ["worktree", "list", "--porcelain"]:
            return "\n".join(
                [
                    "worktree D:/zWenbo/AI/LLMCompute",
                    "HEAD deadbeef",
                    "branch refs/heads/wip/root-main-parking-2026-03-24",
                    "",
                    "worktree D:/zWenbo/AI/wt/h64-post-h63-archive-first-freeze",
                    "HEAD cafe1234",
                    "branch refs/heads/wip/h64-post-h63-archive-first-freeze",
                    "",
                ]
            )
        if args == ["ls-files", "-z"]:
            return ""
        raise AssertionError(args)

    temp_root = tmp_path / "h64-post-h63-archive-first-freeze"
    temp_root.mkdir(parents=True, exist_ok=True)
    (temp_root / ".gitignore").write_text(temp_gitignore.read_text(encoding="utf-8"), encoding="utf-8")
    temp_out_dir = tmp_path / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming"
    module.OUT_DIR = temp_out_dir
    module.ROOT = temp_root
    module.H63_SUMMARY_PATH = temp_h63_summary
    module.P52_SUMMARY_PATH = temp_p52_summary
    module.git_output = fake_git_output
    module.branch_exists = lambda branch: branch == "wip/f38-post-h62-archive-first-closeout"
    module.MERGE_RULES_PATH = temp_merge_rules
    module.ARTIFACT_POLICY_PATH = temp_artifact_policy
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.ROOT = original_root
        module.H63_SUMMARY_PATH = original_h63
        module.P52_SUMMARY_PATH = original_p52
        module.git_output = original_git_output
        module.branch_exists = original_branch_exists
        module.MERGE_RULES_PATH = original_merge_rules
        module.ARTIFACT_POLICY_PATH = original_artifact_policy
        module.CURRENT_STAGE_DRIVER_PATH = original_driver

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution"
    assert payload["summary"]["root_main_quarantined"] is True
    assert payload["summary"]["tracked_oversize_count"] == 0
