from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p61_post_p60_release_hygiene_rebaseline.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p61_post_p60_release_hygiene_rebaseline",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p61_writes_preserved_prior_release_hygiene_summary(tmp_path: Path) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p60_summary = _write_json(
        "p60_summary.json",
        {"summary": {"selected_outcome": "published_clean_descendant_promotion_prep_locked_after_p59"}},
    )
    temp_worktree_hygiene_summary = _write_json(
        "release_worktree_hygiene_snapshot.json",
        {
            "summary": {
                "branch": "wip/p63-post-p62-tight-core-hygiene",
                "release_commit_state": "clean_worktree_ready_if_other_gates_green",
                "git_diff_check_state": "clean",
            }
        },
    )
    temp_preflight_summary = _write_json(
        "release_preflight_checklist_audit.json",
        {"summary": {"preflight_state": "docs_and_audits_green"}},
    )
    temp_p10_summary = _write_json(
        "p10_submission_archive_ready.json",
        {"summary": {"packet_state": "archive_ready"}},
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P64_post_p63_release_hygiene_rebaseline",
            "wip/p63-post-p62-tight-core-hygiene",
            "clean_worktree_ready_if_other_gates_green",
        ],
    )
    temp_branch_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p63-post-p62-tight-core-hygiene",
            "wip/p64-post-p63-successor-stack",
            "successor",
            "wip/p60-post-p59-published-clean-descendant-prep",
            "preserved prior published clean descendant",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p60 = module.P60_SUMMARY_PATH
    original_worktree_hygiene = module.WORKTREE_HYGIENE_SUMMARY_PATH
    original_preflight = module.PREFLIGHT_SUMMARY_PATH
    original_p10 = module.P10_SUMMARY_PATH
    original_current_stage_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_branch_registry = module.BRANCH_REGISTRY_PATH
    original_current_branch = module.current_branch
    temp_out_dir = tmp_path / "P61_post_p60_release_hygiene_rebaseline"
    module.OUT_DIR = temp_out_dir
    module.P60_SUMMARY_PATH = temp_p60_summary
    module.WORKTREE_HYGIENE_SUMMARY_PATH = temp_worktree_hygiene_summary
    module.PREFLIGHT_SUMMARY_PATH = temp_preflight_summary
    module.P10_SUMMARY_PATH = temp_p10_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.BRANCH_REGISTRY_PATH = temp_branch_registry
    module.current_branch = lambda: "wip/p64-post-p63-successor-stack"
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P60_SUMMARY_PATH = original_p60
        module.WORKTREE_HYGIENE_SUMMARY_PATH = original_worktree_hygiene
        module.PREFLIGHT_SUMMARY_PATH = original_preflight
        module.P10_SUMMARY_PATH = original_p10
        module.CURRENT_STAGE_DRIVER_PATH = original_current_stage_driver
        module.BRANCH_REGISTRY_PATH = original_branch_registry
        module.current_branch = original_current_branch

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "published_clean_descendant_release_hygiene_rebaselined"
    assert payload["summary"]["current_published_clean_descendant_branch"] == "wip/p63-post-p62-tight-core-hygiene"
    assert payload["summary"]["current_execution_branch"] == "wip/p64-post-p63-successor-stack"
    assert payload["summary"]["worktree_hygiene_branch"] == "wip/p63-post-p62-tight-core-hygiene"
    assert payload["summary"]["blocked_count"] == 0
