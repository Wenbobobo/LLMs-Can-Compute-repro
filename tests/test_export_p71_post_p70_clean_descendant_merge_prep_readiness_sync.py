from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p71_post_p70_clean_descendant_merge_prep_readiness_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p71_post_p70_clean_descendant_merge_prep_readiness_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p71_writes_clean_descendant_merge_prep_readiness_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p70_summary = _write_json(
        "p70_summary.json",
        {
            "summary": {
                "selected_outcome": "archive_indexes_and_artifact_policy_synced_to_h65_hygiene_cleanup_stack"
            }
        },
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p56-main-scratch",
        ],
    )
    temp_readme = _write_text(
        "README.md",
        [
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "wip/p69-post-h65-hygiene-only-cleanup",
        ],
    )
    temp_status = _write_text(
        "STATUS.md",
        [
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "wip/p69-post-h65-hygiene-only-cleanup",
        ],
    )
    temp_docs_readme = _write_text(
        "docs_readme.md",
        [
            "H65 + P69/P70/P71 + P56/P57/P58/P59 + P66/P67/P68 + F38",
            "plans/README.md",
            "milestones/README.md",
        ],
    )
    temp_milestones = _write_text(
        "milestones_readme.md",
        [
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P69_post_h65_repo_graph_hygiene_inventory",
        ],
    )
    temp_plans = _write_text(
        "plans_readme.md",
        [
            "2026-04-01-post-p71-next-planmode-handoff.md",
            "2026-04-01-post-p71-next-planmode-startup-prompt.md",
            "2026-04-01-post-p71-next-planmode-brief-prompt.md",
        ],
    )
    temp_handoff = _write_text(
        "post_p71_handoff.md",
        [
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p56-main-scratch",
            "0/18",
            "0/159",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_startup = _write_text(
        "post_p71_startup.md",
        [
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p56-main-scratch",
            "0/18",
            "0/159",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_brief = _write_text(
        "post_p71_brief.md",
        [
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "0/18",
            "0/159",
            "dirty-root integration is still out of bounds",
        ],
    )
    temp_readiness = _write_text(
        "merge_prep_readiness.md",
        [
            "wip/p56-main-scratch",
            "wip/p66-post-p65-published-successor-freeze",
            "git merge-tree",
            "merge execution remains absent",
            "dirty root `main` remains quarantine-only",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p70 = module.P70_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_readme = module.ROOT_README_PATH
    original_status = module.STATUS_PATH
    original_docs_readme = module.DOCS_README_PATH
    original_milestones = module.MILESTONES_README_PATH
    original_plans = module.PLANS_README_PATH
    original_handoff = module.POST_P71_HANDOFF_PATH
    original_startup = module.POST_P71_STARTUP_PATH
    original_brief = module.POST_P71_BRIEF_PATH
    original_readiness = module.MERGE_PREP_READINESS_PATH
    temp_out_dir = tmp_path / "P71_post_p70_clean_descendant_merge_prep_readiness_sync"
    module.OUT_DIR = temp_out_dir
    module.P70_SUMMARY_PATH = temp_p70_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.ROOT_README_PATH = temp_readme
    module.STATUS_PATH = temp_status
    module.DOCS_README_PATH = temp_docs_readme
    module.MILESTONES_README_PATH = temp_milestones
    module.PLANS_README_PATH = temp_plans
    module.POST_P71_HANDOFF_PATH = temp_handoff
    module.POST_P71_STARTUP_PATH = temp_startup
    module.POST_P71_BRIEF_PATH = temp_brief
    module.MERGE_PREP_READINESS_PATH = temp_readiness

    monkeypatch.setattr(
        module,
        "worktree_status",
        lambda path: {"branch": "wip/p56-main-scratch", "dirty_count": 0, "clean": True},
    )
    monkeypatch.setattr(
        module,
        "merge_tree_probe",
        lambda left, right: {
            "merge_base": "eff98f8939726189af60f7d46e2fbd1b3f5409cb",
            "conflict_free": True,
            "probe_exit_code": 0,
            "stdout": "7cdd3287afca12ed3de67368516c4cd758b51c16",
            "stderr": "",
            "write_tree_oid": "7cdd3287afca12ed3de67368516c4cd758b51c16",
        },
    )
    monkeypatch.setattr(module, "current_branch", lambda: "wip/p69-post-h65-hygiene-only-cleanup")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P70_SUMMARY_PATH = original_p70
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.ROOT_README_PATH = original_readme
        module.STATUS_PATH = original_status
        module.DOCS_README_PATH = original_docs_readme
        module.MILESTONES_README_PATH = original_milestones
        module.PLANS_README_PATH = original_plans
        module.POST_P71_HANDOFF_PATH = original_handoff
        module.POST_P71_STARTUP_PATH = original_startup
        module.POST_P71_BRIEF_PATH = original_brief
        module.MERGE_PREP_READINESS_PATH = original_readiness

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_descendant_merge_prep_readiness_mapped_without_merge_execution"
    assert payload["summary"]["merge_tree_conflict_free"] is True
    assert payload["summary"]["blocked_count"] == 0


def test_merge_tree_probe_uses_exit_code_for_conflict_detection(monkeypatch) -> None:
    module = _load_module()

    class _Completed:
        def __init__(self, *, returncode: int, stdout: str, stderr: str) -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def _fake_run(args, cwd, check, capture_output, text, encoding):
        if args[:3] == ["git", "merge-tree", "--write-tree"]:
            return _Completed(returncode=1, stdout="Auto-merging foo.txt\nCONFLICT (content): Merge conflict in foo.txt\n", stderr="")
        raise AssertionError(f"unexpected subprocess call: {args}")

    monkeypatch.setattr(module, "git_output", lambda args, cwd=None: "eff98f8939726189af60f7d46e2fbd1b3f5409cb")
    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    payload = module.merge_tree_probe("wip/p56-main-scratch", "wip/p66-post-p65-published-successor-freeze")
    assert payload["merge_base"] == "eff98f8939726189af60f7d46e2fbd1b3f5409cb"
    assert payload["conflict_free"] is False
    assert payload["probe_exit_code"] == 1
    assert payload["write_tree_oid"] is None
