from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p73_writes_legacy_worktree_shrink_inventory_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p72_summary = _write_json(
        "p72_summary.json",
        {
            "summary": {
                "selected_outcome": "archive_polish_surfaces_normalized_and_explicit_stop_handoff_frozen_without_scope_widening"
            }
        },
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
        ],
    )
    temp_readme = _write_text(
        "README.md",
        [
            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
        ],
    )
    temp_status = _write_text(
        "STATUS.md",
        [
            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
        ],
    )
    temp_docs_readme = _write_text(
        "docs_readme.md",
        [
            "H65 + P73 + P74/P75/P76 + P72 + P69/P70/P71",
            "branch_worktree_registry.md",
            "plans/README.md",
        ],
    )
    temp_milestones = _write_text(
        "milestones_readme.md",
        [
            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "P74_post_p73_successor_publication_review",
            "P75_post_p74_published_successor_freeze",
            "P76_post_p75_release_hygiene_and_control_rebaseline",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
        ],
    )
    temp_plans = _write_text(
        "plans_readme.md",
        [
            "2026-04-02-post-p72-hygiene-shrink-mergeprep-design.md",
            "2026-04-02-post-p73-next-planmode-handoff.md",
            "2026-04-02-post-p73-next-planmode-startup-prompt.md",
            "2026-04-02-post-p73-next-planmode-brief-prompt.md",
        ],
    )
    temp_publication_readme = _write_text(
        "publication_readme.md",
        [
            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "current local hygiene and shrink wave",
        ],
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            str(module.ROOT).replace("\\", "/"),
            "wip/p74-post-p73-successor-publication-review",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "D:/zWenbo/AI/wt/",
            "D:/zWenbo/AI/LLMCompute-worktrees/",
            "wip/r33-next",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_keep_set = _write_text(
        "keep_set.md",
        [
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p74-post-p73-successor-publication-review",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p75-post-p74-published-successor-freeze",
            "wip/p56-main-scratch",
            "wip/root-main-parking-2026-03-24",
            "wip/r33-next",
            "D:/zWenbo/AI/wt/",
        ],
    )
    temp_runbook = _write_text(
        "shrink_runbook.md",
        [
            "D:/zWenbo/AI/LLMCompute-worktrees/",
            "git worktree remove",
            "never touch",
            "D:/zWenbo/AI/LLMCompute",
            "do not remove dirty worktrees",
            "branch refs remain preserved",
        ],
    )
    temp_handoff = _write_text(
        "post_p73_handoff.md",
        [
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p75-post-p74-published-successor-freeze",
            "wip/p56-main-scratch",
            "legacy local worktree footprint has already been shrunk",
            "remaining legacy-path worktrees",
            "wip/h27-promotion",
            "wip/r33-next",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_startup = _write_text(
        "post_p73_startup.md",
        [
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p75-post-p74-published-successor-freeze",
            "wip/p56-main-scratch",
            "legacy-path worktree count: `2`",
            "wip/h27-promotion",
            "wip/r33-next",
            "Runtime remains closed",
        ],
    )
    temp_brief = _write_text(
        "post_p73_brief.md",
        [
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "legacy-path worktree count: `2`",
            "wip/h27-promotion",
            "wip/r33-next",
            "dirty-root integration remains out of bounds",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p72 = module.P72_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_readme = module.ROOT_README_PATH
    original_status = module.STATUS_PATH
    original_docs_readme = module.DOCS_README_PATH
    original_milestones = module.MILESTONES_README_PATH
    original_plans = module.PLANS_README_PATH
    original_publication = module.PUBLICATION_README_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    original_keep_set = module.KEEP_SET_PATH
    original_runbook = module.SHRINK_RUNBOOK_PATH
    original_handoff = module.POST_P73_HANDOFF_PATH
    original_startup = module.POST_P73_STARTUP_PATH
    original_brief = module.POST_P73_BRIEF_PATH
    original_current_branch_path = module.CURRENT_BRANCH_PATH
    temp_out_dir = tmp_path / "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync"
    module.OUT_DIR = temp_out_dir
    module.P72_SUMMARY_PATH = temp_p72_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.ROOT_README_PATH = temp_readme
    module.STATUS_PATH = temp_status
    module.DOCS_README_PATH = temp_docs_readme
    module.MILESTONES_README_PATH = temp_milestones
    module.PLANS_README_PATH = temp_plans
    module.PUBLICATION_README_PATH = temp_publication_readme
    module.BRANCH_REGISTRY_PATH = temp_registry
    module.KEEP_SET_PATH = temp_keep_set
    module.SHRINK_RUNBOOK_PATH = temp_runbook
    module.POST_P73_HANDOFF_PATH = temp_handoff
    module.POST_P73_STARTUP_PATH = temp_startup
    module.POST_P73_BRIEF_PATH = temp_brief
    module.CURRENT_BRANCH_PATH = str(module.ROOT).replace("\\", "/")

    monkeypatch.setattr(
        module,
        "listed_worktrees",
        lambda: [
            {
                "worktree": "D:/zWenbo/AI/wt/p73-post-p72-hygiene-shrink-mergeprep",
                "branch": "wip/p73-post-p72-hygiene-shrink-mergeprep",
                "upstream": "",
            },
            {
                "worktree": "D:/zWenbo/AI/wt/p72-post-p71-archive-polish-stop-handoff",
                "branch": "wip/p72-post-p71-archive-polish-stop-handoff",
                "upstream": "origin/wip/p72-post-p71-archive-polish-stop-handoff",
            },
            {
                "worktree": "D:/zWenbo/AI/LLMCompute-worktrees/r33-next",
                "branch": "wip/r33-next",
                "upstream": "",
            },
            {
                "worktree": "D:/zWenbo/AI/LLMCompute-worktrees/f18-f19-planning",
                "branch": "wip/f18-f19-planning",
                "upstream": "origin/wip/f18-f19-planning",
            },
            {
                "worktree": "D:/zWenbo/AI/LLMCompute-worktrees/h31-later-explicit",
                "branch": "wip/h31-later-explicit",
                "upstream": "",
            },
            {
                "worktree": "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion",
                "branch": "wip/h27-promotion",
                "upstream": "",
            },
        ],
    )
    monkeypatch.setattr(
        module,
        "worktree_status",
        lambda path: {
            "branch": {
                "D:/zWenbo/AI/LLMCompute-worktrees/r33-next": "wip/r33-next",
                "D:/zWenbo/AI/LLMCompute-worktrees/f18-f19-planning": "wip/f18-f19-planning",
                "D:/zWenbo/AI/LLMCompute-worktrees/h31-later-explicit": "wip/h31-later-explicit",
                "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion": "wip/h27-promotion",
            }.get(path, "unused"),
            "dirty_count": 123 if path == "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion" else 0,
            "clean": path != "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion",
        },
    )
    monkeypatch.setattr(module, "current_branch", lambda: "wip/p73-post-p72-hygiene-shrink-mergeprep")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P72_SUMMARY_PATH = original_p72
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.ROOT_README_PATH = original_readme
        module.STATUS_PATH = original_status
        module.DOCS_README_PATH = original_docs_readme
        module.MILESTONES_README_PATH = original_milestones
        module.PLANS_README_PATH = original_plans
        module.PUBLICATION_README_PATH = original_publication
        module.BRANCH_REGISTRY_PATH = original_registry
        module.KEEP_SET_PATH = original_keep_set
        module.SHRINK_RUNBOOK_PATH = original_runbook
        module.POST_P73_HANDOFF_PATH = original_handoff
        module.POST_P73_STARTUP_PATH = original_startup
        module.POST_P73_BRIEF_PATH = original_brief
        module.CURRENT_BRANCH_PATH = original_current_branch_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "legacy_worktree_inventory_and_keep_set_sync_completed_for_safe_local_shrink"
    assert payload["summary"]["legacy_keep_count"] == 1
    assert payload["summary"]["legacy_prune_with_upstream_count"] == 1
    assert payload["summary"]["legacy_prune_without_upstream_count"] == 1
    assert payload["summary"]["legacy_blocked_dirty_count"] == 1
    assert payload["summary"]["legacy_misplaced_live_count"] == 0
    assert payload["summary"]["blocked_count"] == 0

