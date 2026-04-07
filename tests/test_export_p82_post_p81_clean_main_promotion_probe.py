from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p82_post_p81_clean_main_promotion_probe.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p82_post_p81_clean_main_promotion_probe",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p82_writes_clean_main_probe_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    temp_p81_summary = tmp_path / "p81_summary.json"
    temp_p81_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "locked_facts_rebaselined_and_route_synced_after_p80", "published_branch_head": "53962ca"}}, indent=2) + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_p81 = module.P81_SUMMARY_PATH
    original_probe_worktree = module.PROBE_WORKTREE
    temp_out_dir = tmp_path / "P82_post_p81_clean_main_promotion_probe"
    module.OUT_DIR = temp_out_dir
    module.P81_SUMMARY_PATH = temp_p81_summary
    module.PROBE_WORKTREE = str(tmp_path / "probe")

    monkeypatch.setattr(module, "worktree_status", lambda path: {"branch": "wip/p82-post-p81-clean-main-promotion-probe", "dirty_count": 0, "clean": True})
    monkeypatch.setattr(
        module,
        "git_output",
        lambda args, cwd=None: {
            ("rev-parse", "--short", "HEAD"): "56ff106",
            ("rev-parse", "--short", "wip/p81-post-p80-clean-descendant-promotion-prep"): "7a9fe0b",
            ("rev-parse", "--short", "wip/p75-post-p74-published-successor-freeze"): "53962ca",
        }.get(tuple(args), "7a9fe0b"),
    )
    monkeypatch.setattr(module, "ahead_behind", lambda left, right, cwd=None: {"left_only": 0, "right_only": 180} if left == "origin/main" else {"left_only": 0, "right_only": 180})
    monkeypatch.setattr(module, "merge_base", lambda left, right, cwd=None: "56ff1066c96dbc00b1fc73e60c3503b2accec389")
    monkeypatch.setattr(module, "is_ancestor", lambda ancestor, descendant, cwd=None: True)
    monkeypatch.setattr(module, "merge_tree_probe", lambda left, right, cwd=None: {"conflict_free": True, "probe_exit_code": 0, "write_tree_oid": "bc042eeb2d536f25cb9c15b9dd1775edb65abd64", "stdout": "bc042eeb2d536f25cb9c15b9dd1775edb65abd64", "stderr": ""})
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P81_SUMMARY_PATH = original_p81
        module.PROBE_WORKTREE = original_probe_worktree

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_main_probe_confirms_fast_forward_promotion_path_after_p81"
    assert payload["summary"]["fast_forward_ready"] is True
    assert payload["summary"]["merge_tree_conflict_free"] is True
    assert payload["summary"]["blocked_count"] == 0
