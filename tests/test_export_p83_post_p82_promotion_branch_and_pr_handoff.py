from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p83_post_p82_promotion_branch_and_pr_handoff.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p83_post_p82_promotion_branch_and_pr_handoff",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p83_writes_promotion_handoff_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    temp_p82 = tmp_path / "p82_summary.json"
    temp_p82.write_text(
        json.dumps({"summary": {"selected_outcome": "clean_main_probe_confirms_fast_forward_promotion_path_after_p81"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_handoff = tmp_path / "pr_handoff.md"
    temp_handoff.write_text(
        "\n".join(
            [
                "wip/p83-post-p82-promotion-branch-and-pr-handoff",
                "wip/p81-post-p80-clean-descendant-promotion-prep",
                "origin/main",
                "c9603c1",
                "uv run pytest",
                "no dirty-root integration",
                "runtime remains closed",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_p82 = module.P82_SUMMARY_PATH
    original_handoff = module.HANDOFF_PATH
    temp_out_dir = tmp_path / "P83_post_p82_promotion_branch_and_pr_handoff"
    module.OUT_DIR = temp_out_dir
    module.P82_SUMMARY_PATH = temp_p82
    module.HANDOFF_PATH = temp_handoff

    monkeypatch.setattr(module, "current_branch", lambda: "wip/p83-post-p82-promotion-branch-and-pr-handoff")
    monkeypatch.setattr(module, "worktree_clean", lambda: True)
    monkeypatch.setattr(
        module,
        "git_output",
        lambda args, cwd=None: {
            ("rev-parse", "--short", "HEAD"): "c9603c1",
            ("rev-parse", "--short", "wip/p81-post-p80-clean-descendant-promotion-prep"): "c9603c1",
        }[tuple(args)],
    )
    monkeypatch.setattr(
        module,
        "ahead_behind",
        lambda left, right: {"left_only": 0, "right_only": 181} if left == "origin/main" else {"left_only": 0, "right_only": 0},
    )
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P82_SUMMARY_PATH = original_p82
        module.HANDOFF_PATH = original_handoff

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "promotion_branch_materialized_and_pr_handoff_prepared_after_p82"
    assert payload["summary"]["blocked_count"] == 0
