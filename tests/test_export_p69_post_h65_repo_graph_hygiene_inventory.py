from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p69_post_h65_repo_graph_hygiene_inventory.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p69_post_h65_repo_graph_hygiene_inventory",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p69_writes_repo_graph_hygiene_inventory_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_h65_summary = _write_json(
        "h65_summary.json",
        {
            "summary": {
                "selected_outcome": "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop"
            }
        },
    )
    temp_p54_summary = _write_json(
        "p54_summary.json",
        {
            "summary": {
                "selected_outcome": "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution"
            }
        },
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p56-main-scratch",
            "wip/p63-post-p62-tight-core-hygiene",
            "wip/p64-post-p63-successor-stack",
            "wip/root-main-parking-2026-03-24",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_keep_set = _write_text(
        "keep_set.md",
        [
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p56-main-scratch",
            "wip/root-main-parking-2026-03-24",
            "0/18",
            "0/159",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_h65 = module.H65_SUMMARY_PATH
    original_p54 = module.P54_SUMMARY_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    original_keep_set = module.KEEP_SET_PATH
    temp_out_dir = tmp_path / "P69_post_h65_repo_graph_hygiene_inventory"
    module.OUT_DIR = temp_out_dir
    module.H65_SUMMARY_PATH = temp_h65_summary
    module.P54_SUMMARY_PATH = temp_p54_summary
    module.BRANCH_REGISTRY_PATH = temp_registry
    module.KEEP_SET_PATH = temp_keep_set

    monkeypatch.setattr(
        module,
        "listed_worktrees",
        lambda: [
            {
                "worktree": "D:/zWenbo/AI/wt/p69-post-h65-hygiene-only-cleanup",
                "branch": "wip/p69-post-h65-hygiene-only-cleanup",
            },
            {
                "worktree": "D:/zWenbo/AI/wt/p66-post-p65-published-successor-freeze",
                "branch": "wip/p66-post-p65-published-successor-freeze",
            },
            {"worktree": "D:/zWenbo/AI/wt/p56-main-scratch", "branch": "wip/p56-main-scratch"},
            {
                "worktree": "D:/zWenbo/AI/wt/p63-post-p62-tight-core-hygiene",
                "branch": "wip/p63-post-p62-tight-core-hygiene",
            },
            {
                "worktree": "D:/zWenbo/AI/wt/p64-post-p63-successor-stack",
                "branch": "wip/p64-post-p63-successor-stack",
            },
            {
                "worktree": "D:/zWenbo/AI/wt/h64-post-h63-archive-first-freeze",
                "branch": "wip/h64-post-h63-archive-first-freeze",
            },
            {
                "worktree": "D:/zWenbo/AI/LLMCompute",
                "branch": "wip/root-main-parking-2026-03-24",
            },
        ],
    )
    monkeypatch.setattr(
        module,
        "worktree_status",
        lambda path: {
            "branch": {
                "D:/zWenbo/AI/wt/p56-main-scratch": "wip/p56-main-scratch",
                "D:/zWenbo/AI/wt/p63-post-p62-tight-core-hygiene": "wip/p63-post-p62-tight-core-hygiene",
                "D:/zWenbo/AI/wt/p64-post-p63-successor-stack": "wip/p64-post-p63-successor-stack",
                "D:/zWenbo/AI/wt/h64-post-h63-archive-first-freeze": "wip/h64-post-h63-archive-first-freeze",
                "D:/zWenbo/AI/wt/p66-post-p65-published-successor-freeze": "wip/p66-post-p65-published-successor-freeze",
                "D:/zWenbo/AI/LLMCompute": "wip/root-main-parking-2026-03-24",
            }[path],
            "dirty_count": 5 if path == "D:/zWenbo/AI/LLMCompute" else 0,
            "clean": path != "D:/zWenbo/AI/LLMCompute",
        },
    )
    monkeypatch.setattr(module, "divergence", lambda left, right: (0, 18) if left == "wip/p56-main-scratch" else (0, 159))
    monkeypatch.setattr(module, "tracked_upstream", lambda branch: f"origin/{branch}")
    monkeypatch.setattr(module, "current_branch", lambda: "wip/p69-post-h65-hygiene-only-cleanup")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H65_SUMMARY_PATH = original_h65
        module.P54_SUMMARY_PATH = original_p54
        module.BRANCH_REGISTRY_PATH = original_registry
        module.KEEP_SET_PATH = original_keep_set

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "repo_graph_hygiene_inventory_confirms_clean_descendant_keep_set_and_root_quarantine"
    assert payload["summary"]["p56_to_p66_right_count"] == 18
    assert payload["summary"]["origin_main_to_p66_right_count"] == 159
    assert payload["summary"]["clean_keep_set_count"] == 5
    assert payload["summary"]["blocked_count"] == 0
