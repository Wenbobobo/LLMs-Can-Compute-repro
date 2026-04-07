from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p78_post_p77_legacy_worktree_convergence_and_quarantine_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p78_writes_worktree_convergence_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p77_summary = _write_json(
        "p77_summary.json",
        {"summary": {"selected_outcome": "keep_set_and_provenance_normalized_after_p76"}},
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
            "wip/h27-promotion",
            "wip/root-main-parking-2026-03-24",
            "balanced mounted keep set",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p77 = module.P77_SUMMARY_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    temp_out_dir = tmp_path / "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync"
    module.OUT_DIR = temp_out_dir
    module.P77_SUMMARY_PATH = temp_p77_summary
    module.BRANCH_REGISTRY_PATH = temp_registry
    monkeypatch.setattr(
        module,
        "listed_worktrees",
        lambda: [
            {"worktree": "D:/zWenbo/AI/LLMCompute", "branch": "wip/root-main-parking-2026-03-24"},
            {"worktree": "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion", "branch": "wip/h27-promotion"},
            {"worktree": "D:/zWenbo/AI/wt/p56-main-scratch", "branch": "wip/p56-main-scratch"},
            {"worktree": "D:/zWenbo/AI/wt/p69-post-h65-hygiene-only-cleanup", "branch": "wip/p69-post-h65-hygiene-only-cleanup"},
            {"worktree": "D:/zWenbo/AI/wt/p72-post-p71-archive-polish-stop-handoff", "branch": "wip/p72-post-p71-archive-polish-stop-handoff"},
            {"worktree": "D:/zWenbo/AI/wt/p73-post-p72-hygiene-shrink-mergeprep", "branch": "wip/p73-post-p72-hygiene-shrink-mergeprep"},
            {"worktree": "D:/zWenbo/AI/wt/p74-post-p73-successor-publication-review", "branch": "wip/p74-post-p73-successor-publication-review"},
            {"worktree": "D:/zWenbo/AI/wt/p75-post-p74-published-successor-freeze", "branch": "wip/p75-post-p74-published-successor-freeze"},
        ],
    )
    monkeypatch.setattr(
        module,
        "dirty_count_for_worktree",
        lambda path: {
            "D:/zWenbo/AI/LLMCompute": 325,
            "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion": 123,
        }.get(path, 0),
    )
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P77_SUMMARY_PATH = original_p77
        module.BRANCH_REGISTRY_PATH = original_registry

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "balanced_worktree_convergence_completed_with_quarantines_preserved"
    assert payload["summary"]["mounted_keep_branch_count"] == 6
    assert payload["summary"]["dirty_quarantine_count"] == 2
    assert payload["summary"]["blocked_count"] == 0
