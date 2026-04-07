from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p77_post_p76_keep_set_and_provenance_normalization.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p77_post_p76_keep_set_and_provenance_normalization",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p77_writes_keep_set_and_provenance_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p76_summary = _write_json(
        "p76_summary.json",
        {
            "summary": {
                "selected_outcome": "published_successor_release_hygiene_and_control_rebaselined_after_p75"
            }
        },
    )
    temp_readme = _write_text(
        "README.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P77_post_p76_keep_set_and_provenance_normalization",
            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
            "P80_post_p79_next_planmode_handoff_sync",
            "wip/p75-post-p74-published-successor-freeze",
        ],
    )
    temp_status = _write_text(
        "STATUS.md",
        [
            "P77_post_p76_keep_set_and_provenance_normalization",
            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
            "P80_post_p79_next_planmode_handoff_sync",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p74-post-p73-successor-publication-review",
            "wip/p75-post-p74-published-successor-freeze",
        ],
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P77_post_p76_keep_set_and_provenance_normalization",
            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
            "P80_post_p79_next_planmode_handoff_sync",
            "wip/p74-post-p73-successor-publication-review",
            "wip/p64-post-p63-successor-stack",
            "wip/p75-post-p74-published-successor-freeze",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p56-main-scratch",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p75-post-p74-published-successor-freeze",
            "wip/p74-post-p73-successor-publication-review",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p56-main-scratch",
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p64-post-p63-successor-stack",
            "wip/root-main-parking-2026-03-24",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_plans_readme = _write_text(
        "plans_readme.md",
        [
            "2026-04-05-post-p76-hygiene-first-convergence-design.md",
            "2026-04-05-post-p80-next-planmode-handoff.md",
            "2026-04-05-post-p80-next-planmode-startup-prompt.md",
            "2026-04-05-post-p80-next-planmode-brief-prompt.md",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p76 = module.P76_SUMMARY_PATH
    original_readme = module.ROOT_README_PATH
    original_status = module.STATUS_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    original_plans_readme = module.PLANS_README_PATH
    temp_out_dir = tmp_path / "P77_post_p76_keep_set_and_provenance_normalization"
    module.OUT_DIR = temp_out_dir
    module.P76_SUMMARY_PATH = temp_p76_summary
    module.ROOT_README_PATH = temp_readme
    module.STATUS_PATH = temp_status
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.BRANCH_REGISTRY_PATH = temp_registry
    module.PLANS_README_PATH = temp_plans_readme
    monkeypatch.setattr(module, "current_branch", lambda: "wip/p75-post-p74-published-successor-freeze")
    monkeypatch.setattr(
        module,
        "tracked_upstream",
        lambda branch: {
            "wip/p75-post-p74-published-successor-freeze": "origin/wip/p75-post-p74-published-successor-freeze",
            "wip/p74-post-p73-successor-publication-review": "origin/wip/p74-post-p73-successor-publication-review",
            "wip/p73-post-p72-hygiene-shrink-mergeprep": "origin/wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff": "origin/wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup": "origin/wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p56-main-scratch": "origin/main",
        }[branch],
    )
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P76_SUMMARY_PATH = original_p76
        module.ROOT_README_PATH = original_readme
        module.STATUS_PATH = original_status
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.BRANCH_REGISTRY_PATH = original_registry
        module.PLANS_README_PATH = original_plans_readme

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "keep_set_and_provenance_normalized_after_p76"
    assert payload["summary"]["tracked_keep_branch_count"] == 6
    assert payload["summary"]["blocked_count"] == 0
