from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _module_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p86_post_p85_dirty_root_inventory_and_archive_replace_map.py"
    )


def _load_module():
    module_path = _module_path()
    assert module_path.exists(), f"missing exporter: {module_path}"
    spec = importlib.util.spec_from_file_location(
        "export_p86_post_p85_dirty_root_inventory_and_archive_replace_map",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p86_writes_dirty_root_inventory_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    temp_p85 = tmp_path / "p85_summary.json"
    temp_p85.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "merged_main_rebaseline_and_control_resync_after_p84",
                    "blocked_count": 0,
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    docs = {
        "README.md": "\n".join(
            [
                "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
                "wip/p85-post-p84-main-rebaseline",
                "wip/root-main-parking-2026-03-24",
                "dirty-root inventory and archive-replace map",
            ]
        ),
        "STATUS.md": "\n".join(
            [
                "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
                "wip/root-main-parking-2026-03-24",
                "quarantine-only",
                "docs consolidation",
            ]
        ),
        "docs/README.md": "\n".join(
            [
                "H65 + P86 + P85 + P84 + P83",
                "publication_record/current_stage_driver.md",
                "branch_worktree_registry.md",
                "plans/README.md",
            ]
        ),
        "docs/branch_worktree_registry.md": "\n".join(
            [
                "wip/p85-post-p84-main-rebaseline",
                "wip/root-main-parking-2026-03-24",
                "archive-replace map",
                "salvage-only import",
            ]
        ),
        "docs/plans/README.md": "\n".join(
            [
                "2026-04-07-post-p86-next-planmode-handoff.md",
                "2026-04-07-post-p86-next-planmode-startup-prompt.md",
                "2026-04-07-post-p86-next-planmode-brief-prompt.md",
                "P86",
            ]
        ),
        "docs/milestones/README.md": "\n".join(
            [
                "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
                "P85_post_p84_main_rebaseline_and_control_resync",
                "P84_post_p83_keep_set_contraction_and_closeout",
            ]
        ),
        "docs/publication_record/README.md": "\n".join(
            [
                "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
                "current_stage_driver.md",
                "paper_bundle_status.md",
            ]
        ),
        "docs/publication_record/current_stage_driver.md": "\n".join(
            [
                "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
                "wip/root-main-parking-2026-03-24",
                "docs consolidation",
                "paper spine refresh",
            ]
        ),
        "docs/plans/2026-04-07-post-p86-next-planmode-handoff.md": "\n".join(
            [
                "wip/p85-post-p84-main-rebaseline",
                "docs consolidation",
                "paper spine refresh",
                "salvage-only import",
            ]
        ),
        "docs/plans/2026-04-07-post-p86-next-planmode-startup-prompt.md": "\n".join(
            [
                "wip/p85-post-p84-main-rebaseline",
                "docs consolidation",
                "paper spine refresh",
            ]
        ),
        "docs/plans/2026-04-07-post-p86-next-planmode-brief-prompt.md": "\n".join(
            [
                "p85-post-p84-main-rebaseline",
                "docs consolidation",
                "paper spine refresh",
            ]
        ),
    }
    for relative, body in docs.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body + "\n", encoding="utf-8")

    temp_out_dir = tmp_path / "results" / "P86_post_p85_dirty_root_inventory_and_archive_replace_map"
    original_out_dir = module.OUT_DIR
    original_root = module.ROOT
    original_p85_path = module.P85_SUMMARY_PATH
    original_quarantine_path = module.ROOT_QUARANTINE_PATH
    module.OUT_DIR = temp_out_dir
    module.ROOT = tmp_path
    module.P85_SUMMARY_PATH = temp_p85
    module.ROOT_QUARANTINE_PATH = Path("D:/fake/root")

    tracked_rows = [
        {"status": " M", "path": "README.md"},
        {"status": " M", "path": "docs/publication_record/current_stage_driver.md"},
        {"status": " M", "path": "results/P5_public_surface_sync/summary.json"},
        {"status": " M", "path": "scripts/export_p5_public_surface_sync.py"},
        {"status": " M", "path": "tmp/active_wave_plan.md"},
    ]
    untracked_rows = [
        "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/",
        "docs/plans/2026-03-21-post-h21-dual-track-boundary-reopen-design.md",
        "results/H22_post_h21_boundary_reopen_and_dual_track_lock/",
        "scripts/export_h22_post_h21_boundary_reopen_and_dual_track_lock.py",
        "tests/test_export_h22_post_h21_boundary_reopen_and_dual_track_lock.py",
    ]

    monkeypatch.setattr(
        module,
        "git_output",
        lambda args, cwd=None: {
            ("rev-parse", "--abbrev-ref", "HEAD"): "wip/p85-post-p84-main-rebaseline",
            ("rev-parse", "--short", "HEAD"): "d86abc1",
            ("rev-parse", "--short", "origin/main"): "b82b566",
            ("rev-list", "--left-right", "--count", "origin/main...HEAD"): "0 2",
            ("rev-parse", "--abbrev-ref", "HEAD", "D:/fake/root"): "wip/root-main-parking-2026-03-24",
            ("status", "--porcelain=v1", "D:/fake/root"): "\n".join(
                [f"{row['status']} {row['path']}" for row in tracked_rows]
                + [f"?? {path}" for path in untracked_rows]
            ),
        }[tuple(args) if cwd is None else (*args, str(cwd).replace('\\', '/'))],
    )
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.ROOT = original_root
        module.P85_SUMMARY_PATH = original_p85_path
        module.ROOT_QUARANTINE_PATH = original_quarantine_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "dirty_root_inventory_and_archive_replace_map_after_p85"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["tracked_dirty_count"] == 5
    assert payload["summary"]["untracked_dirty_count"] == 5
    assert payload["summary"]["salvage_candidate_count"] == 5
    assert payload["summary"]["archive_only_count"] == 2
    assert payload["summary"]["duplicate_or_obsolete_count"] == 3
