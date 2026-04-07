from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p60_post_p59_published_clean_descendant_promotion_prep.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p60_post_p59_published_clean_descendant_promotion_prep",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p60_writes_published_clean_descendant_prep_summary(tmp_path: Path) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_h64_summary = _write_json(
        "h64_summary.json",
        {
            "summary": {
                "selected_outcome": "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
            }
        },
    )
    temp_p56_summary = _write_json(
        "p56_summary.json",
        {"summary": {"selected_outcome": "clean_descendant_merge_candidate_staged_without_merge_execution"}},
    )
    temp_p57_summary = _write_json(
        "p57_summary.json",
        {"summary": {"selected_outcome": "paper_submission_package_surfaces_synced_to_h64_followthrough_stack"}},
    )
    temp_p58_summary = _write_json(
        "p58_summary.json",
        {"summary": {"selected_outcome": "archive_release_closeout_surfaces_synced_to_h64_followthrough_stack"}},
    )
    temp_p59_summary = _write_json(
        "p59_summary.json",
        {"summary": {"selected_outcome": "control_and_handoff_surfaces_synced_to_h64_followthrough_stack"}},
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "wip/p63-post-p62-tight-core-hygiene",
        ],
    )
    temp_active_wave = _write_text(
        "active_wave_plan.md",
        [
            "`P63_post_p62_published_successor_promotion_prep`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P65_post_p64_merge_prep_control_sync`",
            "`wip/p63-post-p62-tight-core-hygiene`",
            "`wip/p64-post-p63-successor-stack`",
        ],
    )
    temp_publication_readme = _write_text(
        "publication_readme.md",
        [
            "P63_post_p62_published_successor_promotion_prep",
            "published successor clean-descendant promotion-prep wave",
            "P60_post_p59_published_clean_descendant_promotion_prep",
        ],
    )
    temp_plans_readme = _write_text(
        "plans_readme.md",
        [
            "2026-04-01-post-p63-successor-merge-prep-design.md",
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "P60_post_p59_published_clean_descendant_promotion_prep",
        ],
    )
    temp_branch_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p63-post-p62-tight-core-hygiene",
            "wip/p64-post-p63-successor-stack",
            "wip/p60-post-p59-published-clean-descendant-prep",
            "wip/p56-main-scratch",
            "clean_descendant_only_never_dirty_root_main",
            "preserved prior published clean descendant",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_h64 = module.H64_SUMMARY_PATH
    original_p56 = module.P56_SUMMARY_PATH
    original_p57 = module.P57_SUMMARY_PATH
    original_p58 = module.P58_SUMMARY_PATH
    original_p59 = module.P59_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_active_wave = module.ACTIVE_WAVE_PLAN_PATH
    original_publication_readme = module.PUBLICATION_README_PATH
    original_plans_readme = module.PLANS_README_PATH
    original_branch_registry = module.BRANCH_REGISTRY_PATH
    original_current_branch = module.current_branch
    original_tracked_upstream = module.tracked_upstream
    temp_out_dir = tmp_path / "P60_post_p59_published_clean_descendant_promotion_prep"
    module.OUT_DIR = temp_out_dir
    module.H64_SUMMARY_PATH = temp_h64_summary
    module.P56_SUMMARY_PATH = temp_p56_summary
    module.P57_SUMMARY_PATH = temp_p57_summary
    module.P58_SUMMARY_PATH = temp_p58_summary
    module.P59_SUMMARY_PATH = temp_p59_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.ACTIVE_WAVE_PLAN_PATH = temp_active_wave
    module.PUBLICATION_README_PATH = temp_publication_readme
    module.PLANS_README_PATH = temp_plans_readme
    module.BRANCH_REGISTRY_PATH = temp_branch_registry
    module.current_branch = lambda: "wip/p64-post-p63-successor-stack"
    module.tracked_upstream = (
        lambda branch: "origin/wip/p63-post-p62-tight-core-hygiene"
        if branch == "wip/p64-post-p63-successor-stack"
        else "origin/wip/p60-post-p59-published-clean-descendant-prep"
    )
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H64_SUMMARY_PATH = original_h64
        module.P56_SUMMARY_PATH = original_p56
        module.P57_SUMMARY_PATH = original_p57
        module.P58_SUMMARY_PATH = original_p58
        module.P59_SUMMARY_PATH = original_p59
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.ACTIVE_WAVE_PLAN_PATH = original_active_wave
        module.PUBLICATION_README_PATH = original_publication_readme
        module.PLANS_README_PATH = original_plans_readme
        module.BRANCH_REGISTRY_PATH = original_branch_registry
        module.current_branch = original_current_branch
        module.tracked_upstream = original_tracked_upstream

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "published_clean_descendant_promotion_prep_locked_after_p59"
    assert payload["summary"]["merge_execution_state"] is False
    assert payload["summary"]["current_published_clean_descendant_branch"] == "wip/p63-post-p62-tight-core-hygiene"
    assert payload["summary"]["blocked_count"] == 0
