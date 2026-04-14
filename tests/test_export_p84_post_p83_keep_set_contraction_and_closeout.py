from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p84_post_p83_keep_set_contraction_and_closeout.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p84_post_p83_keep_set_contraction_and_closeout",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p84_writes_keep_set_closeout_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    temp_p83 = tmp_path / "p83_summary.json"
    temp_p83.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "promotion_branch_materialized_and_pr_handoff_prepared_after_p82",
                    "blocked_count": 0,
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    tmp_path / "docs"
    docs = {
        "README.md": "\n".join(
            [
                "P84_post_p83_keep_set_contraction_and_closeout",
                "P83_post_p82_promotion_branch_and_pr_handoff",
                "wip/p83-post-p82-promotion-branch-and-pr-handoff",
                "wip/p75-post-p74-published-successor-freeze",
            ]
        ),
        "STATUS.md": "\n".join(
            [
                "P84_post_p83_keep_set_contraction_and_closeout",
                "P83_post_p82_promotion_branch_and_pr_handoff",
                "p83",
                "p81",
                "p82",
            ]
        ),
        "docs/README.md": "\n".join(
            [
                "H65 + P84 + P83",
                "branch_worktree_registry.md",
                "plans/README.md",
                "milestones/README.md",
            ]
        ),
        "docs/branch_worktree_registry.md": "\n".join(
            [
                "wip/p83-post-p82-promotion-branch-and-pr-handoff",
                "wip/p81-post-p80-clean-descendant-promotion-prep",
                "wip/p82-post-p81-clean-main-promotion-probe",
                "P84",
                "P83",
            ]
        ),
        "docs/plans/README.md": "\n".join(
            [
                "2026-04-07-post-p84-next-planmode-handoff.md",
                "2026-04-07-post-p84-next-planmode-startup-prompt.md",
                "2026-04-07-post-p84-next-planmode-brief-prompt.md",
                "P84",
                "P83",
                "wip/p83-post-p82-promotion-branch-and-pr-handoff",
            ]
        ),
        "docs/milestones/README.md": "\n".join(
            [
                "P84_post_p83_keep_set_contraction_and_closeout",
                "P83_post_p82_promotion_branch_and_pr_handoff",
                "P81_post_p80_locked_fact_rebaseline_and_route_sync",
                "P82_post_p81_clean_main_promotion_probe",
            ]
        ),
        "docs/publication_record/README.md": "\n".join(
            [
                "2026-04-07-post-p84-next-planmode-handoff.md",
                "P84_post_p83_keep_set_contraction_and_closeout",
                "P83_post_p82_promotion_branch_and_pr_handoff",
            ]
        ),
        "docs/publication_record/current_stage_driver.md": "\n".join(
            [
                "P84_post_p83_keep_set_contraction_and_closeout",
                "P83_post_p82_promotion_branch_and_pr_handoff",
                "wip/p83-post-p82-promotion-branch-and-pr-handoff",
                "wip/p75-post-p74-published-successor-freeze",
            ]
        ),
        "docs/plans/2026-04-07-post-p84-next-planmode-handoff.md": "\n".join(
            [
                "wip/p83-post-p82-promotion-branch-and-pr-handoff",
                "promotion/PR finalization",
                "no further action",
                "runtime remains closed",
            ]
        ),
        "docs/plans/2026-04-07-post-p84-next-planmode-startup-prompt.md": "\n".join(
            [
                "promotion/PR finalization",
                "no further action",
                "runtime",
                "dirty-root integration",
            ]
        ),
        "docs/plans/2026-04-07-post-p84-next-planmode-brief-prompt.md": "\n".join(
            [
                "promotion/PR finalization",
                "no further action",
                "runtime closed",
            ]
        ),
    }
    for relative, body in docs.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body + "\n", encoding="utf-8")

    temp_out_dir = tmp_path / "results" / "P84_post_p83_keep_set_contraction_and_closeout"
    original_out_dir = module.OUT_DIR
    original_p83_summary_path = module.P83_SUMMARY_PATH
    original_root = module.ROOT
    module.OUT_DIR = temp_out_dir
    module.P83_SUMMARY_PATH = temp_p83
    module.ROOT = tmp_path

    monkeypatch.setattr(
        module,
        "git_output",
        lambda args: {
            ("rev-parse", "--abbrev-ref", "HEAD"): "wip/p83-post-p82-promotion-branch-and-pr-handoff",
            ("rev-parse", "--short", "HEAD"): "6f68178",
            ("rev-parse", "--short", "wip/p75-post-p74-published-successor-freeze"): "53962ca",
            ("worktree", "list", "--porcelain"): "\n".join(
                [
                    "worktree D:/zWenbo/AI/LLMCompute",
                    "HEAD 56ff106",
                    "branch refs/heads/wip/root-main-parking-2026-03-24",
                    "",
                    "worktree D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion",
                    "HEAD eaa4fb0",
                    "branch refs/heads/wip/h27-promotion",
                    "",
                    "worktree D:/zWenbo/AI/wt/p56-main-scratch",
                    "HEAD eff98f8",
                    "branch refs/heads/wip/p56-main-scratch",
                    "",
                    "worktree D:/zWenbo/AI/wt/p69-post-h65-hygiene-only-cleanup",
                    "HEAD 55c7bb7",
                    "branch refs/heads/wip/p69-post-h65-hygiene-only-cleanup",
                    "",
                    "worktree D:/zWenbo/AI/wt/p72-post-p71-archive-polish-stop-handoff",
                    "HEAD bc03069",
                    "branch refs/heads/wip/p72-post-p71-archive-polish-stop-handoff",
                    "",
                    "worktree D:/zWenbo/AI/wt/p73-post-p72-hygiene-shrink-mergeprep",
                    "HEAD b45902e",
                    "branch refs/heads/wip/p73-post-p72-hygiene-shrink-mergeprep",
                    "",
                    "worktree D:/zWenbo/AI/wt/p74-post-p73-successor-publication-review",
                    "HEAD ad03aca",
                    "branch refs/heads/wip/p74-post-p73-successor-publication-review",
                    "",
                    "worktree D:/zWenbo/AI/wt/p75-post-p74-published-successor-freeze",
                    "HEAD 53962ca",
                    "branch refs/heads/wip/p75-post-p74-published-successor-freeze",
                    "",
                    "worktree D:/zWenbo/AI/wt/p83-post-p82-promotion-branch-and-pr-handoff",
                    "HEAD 6f68178",
                    "branch refs/heads/wip/p83-post-p82-promotion-branch-and-pr-handoff",
                    "",
                ]
            ),
        }[tuple(args)],
    )
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P83_SUMMARY_PATH = original_p83_summary_path
        module.ROOT = original_root

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "keep_set_contracted_and_closeout_synced_after_p83"
    assert payload["summary"]["blocked_count"] == 0
