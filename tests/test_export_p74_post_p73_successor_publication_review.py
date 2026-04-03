from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p74_post_p73_successor_publication_review.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p74_post_p73_successor_publication_review",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p74_writes_successor_publication_review_summary(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p73_summary = _write_json(
        "p73_summary.json",
        {
            "summary": {
                "selected_outcome": "legacy_worktree_inventory_and_keep_set_sync_completed_for_safe_local_shrink"
            }
        },
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p66-post-p65-published-successor-freeze",
        ],
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p73-post-p72-hygiene-shrink-mergeprep",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p73 = module.P73_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    temp_out_dir = tmp_path / "P74_post_p73_successor_publication_review"
    module.OUT_DIR = temp_out_dir
    module.P73_SUMMARY_PATH = temp_p73_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.BRANCH_REGISTRY_PATH = temp_registry

    outputs = {
        (
            "rev-list",
            "--left-right",
            "--count",
            "wip/p66-post-p65-published-successor-freeze...wip/p73-post-p72-hygiene-shrink-mergeprep",
        ): "0 11",
        (
            "log",
            "--oneline",
            "wip/p66-post-p65-published-successor-freeze..wip/p73-post-p72-hygiene-shrink-mergeprep",
        ): "\n".join(
            [
                "b45902e Add post-P73 plan handoff prompts",
                "196e196 Refresh P73 shrink and standing result packets",
                "5047c05 Add P73 legacy worktree shrink inventory",
                "bc03069 Refresh P72 archive polish handoff audit results",
                "e3df2dd Normalize P72 boundary summary wording",
                "83c62d8 Align P72 release and archive machine wording",
                "bd58d44 Tighten P72 archive handoff surface wording",
                "36316d6 Add P72 archive polish explicit stop handoff sidecar",
                "55c7bb7 Refresh post-H65 hygiene-only audit results",
                "e7f25a8 Harden post-H65 hygiene-only audits",
                "64eb2aa Add post-H65 hygiene-only cleanup stack",
            ]
        ),
        (
            "diff",
            "--name-only",
            "wip/p66-post-p65-published-successor-freeze..wip/p73-post-p72-hygiene-shrink-mergeprep",
        ): "\n".join(
            [
                "README.md",
                "docs/publication_record/current_stage_driver.md",
                "results/P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync/summary.json",
                "scripts/export_p73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync.py",
                "tests/test_export_p73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync.py",
                "tmp/active_wave_plan.md",
            ]
        ),
        ("rev-parse", "--abbrev-ref", "HEAD"): "wip/p74-post-p73-successor-publication-review",
    }

    def fake_git_output(args: list[str]) -> str:
        key = tuple(args)
        assert key in outputs
        return outputs[key]

    monkeypatch.setattr(module, "git_output", fake_git_output)
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P73_SUMMARY_PATH = original_p73
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.BRANCH_REGISTRY_PATH = original_registry

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert (
        payload["summary"]["selected_outcome"]
        == "successor_publication_review_supports_p75_freeze"
    )
    assert payload["summary"]["review_left_count"] == 0
    assert payload["summary"]["review_right_count"] == 11
    assert payload["summary"]["reviewed_commit_count"] == 11
    assert payload["summary"]["blocked_reviewed_path_count"] == 0
    assert payload["summary"]["blocked_count"] == 0
