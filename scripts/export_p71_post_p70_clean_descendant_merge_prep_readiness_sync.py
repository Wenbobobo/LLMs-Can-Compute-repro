"""Export the post-P70 clean-descendant merge-prep readiness sidecar for P71."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P71_post_p70_clean_descendant_merge_prep_readiness_sync"
P70_SUMMARY_PATH = ROOT / "results" / "P70_post_p69_archive_index_and_artifact_policy_sync" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ROOT_README_PATH = ROOT / "README.md"
STATUS_PATH = ROOT / "STATUS.md"
DOCS_README_PATH = ROOT / "docs" / "README.md"
MILESTONES_README_PATH = ROOT / "docs" / "milestones" / "README.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
POST_P71_HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-01-post-p71-next-planmode-handoff.md"
POST_P71_STARTUP_PATH = ROOT / "docs" / "plans" / "2026-04-01-post-p71-next-planmode-startup-prompt.md"
POST_P71_BRIEF_PATH = ROOT / "docs" / "plans" / "2026-04-01-post-p71-next-planmode-brief-prompt.md"
MERGE_PREP_READINESS_PATH = ROOT / "docs" / "milestones" / "P71_post_p70_clean_descendant_merge_prep_readiness_sync" / "merge_prep_readiness.md"
CURRENT_HYGIENE_BRANCH = "wip/p69-post-h65-hygiene-only-cleanup"
LOCAL_INTEGRATION_BRANCH = "wip/p56-main-scratch"
PUBLISHED_BRANCH = "wip/p66-post-p65-published-successor-freeze"
LOCAL_INTEGRATION_WORKTREE = "D:/zWenbo/AI/wt/p56-main-scratch"
EXPECTED_P56_TO_P66_FACT = "0/18"
EXPECTED_ORIGIN_MAIN_TO_P66_FACT = "0/159"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def git_output(args: list[str], *, cwd: Path | str | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd or ROOT),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def worktree_status(path: str) -> dict[str, object]:
    branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    dirty_lines = [line for line in git_output(["status", "--short", "--untracked-files=all"], cwd=path).splitlines() if line]
    return {"branch": branch, "dirty_count": len(dirty_lines), "clean": len(dirty_lines) == 0}


def merge_tree_probe(left: str, right: str) -> dict[str, object]:
    merge_base = git_output(["merge-base", left, right])
    result = subprocess.run(
        ["git", "merge-tree", "--write-tree", left, right],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    return {
        "merge_base": merge_base,
        "conflict_free": result.returncode == 0,
        "probe_exit_code": result.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "write_tree_oid": stdout.splitlines()[0] if result.returncode == 0 and stdout else None,
    }


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p70_summary = read_json(P70_SUMMARY_PATH)["summary"]
    if p70_summary["selected_outcome"] != "archive_indexes_and_artifact_policy_synced_to_h65_hygiene_cleanup_stack":
        raise RuntimeError("P71 expects the landed P70 archive-index sidecar.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    root_readme_text = read_text(ROOT_README_PATH)
    status_text = read_text(STATUS_PATH)
    docs_readme_text = read_text(DOCS_README_PATH)
    milestones_readme_text = read_text(MILESTONES_README_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    handoff_text = read_text(POST_P71_HANDOFF_PATH)
    startup_text = read_text(POST_P71_STARTUP_PATH)
    brief_text = read_text(POST_P71_BRIEF_PATH)
    merge_prep_readiness_text = read_text(MERGE_PREP_READINESS_PATH)
    current_branch_name = current_branch()

    p56_status = worktree_status(LOCAL_INTEGRATION_WORKTREE)
    merge_probe = merge_tree_probe(LOCAL_INTEGRATION_BRANCH, PUBLISHED_BRANCH)

    checklist_rows = [
        {"item_id": "p71_reads_p70", "status": "pass", "notes": "P71 runs only after P70 lands the archive-index and artifact-policy sync."},
        {"item_id": "p71_runs_on_current_hygiene_branch", "status": "pass" if current_branch_name == CURRENT_HYGIENE_BRANCH else "blocked", "notes": "P71 should run from the current hygiene-only cleanup branch."},
        {
            "item_id": "p71_local_integration_branch_remains_clean",
            "status": "pass" if p56_status["branch"] == LOCAL_INTEGRATION_BRANCH and bool(p56_status["clean"]) else "blocked",
            "notes": "The preserved local integration base should remain clean.",
        },
        {
            "item_id": "p71_merge_tree_probe_remains_conflict_free",
            "status": "pass" if bool(merge_probe["conflict_free"]) else "blocked",
            "notes": "The read-only merge-tree probe should remain conflict-free and non-executing.",
        },
        {
            "item_id": "p71_current_stage_driver_mentions_cleanup_stack",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "P69_post_h65_repo_graph_hygiene_inventory",
                    "P70_post_p69_archive_index_and_artifact_policy_sync",
                    "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
                    CURRENT_HYGIENE_BRANCH,
                    PUBLISHED_BRANCH,
                    LOCAL_INTEGRATION_BRANCH,
                ],
            )
            else "blocked",
            "notes": "The current stage driver should expose the current hygiene-only cleanup stack and merge-prep base.",
        },
        {
            "item_id": "p71_root_readme_and_status_mention_cleanup_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        root_readme_text,
                        [
                            "P69_post_h65_repo_graph_hygiene_inventory",
                            "P70_post_p69_archive_index_and_artifact_policy_sync",
                            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
                            CURRENT_HYGIENE_BRANCH,
                        ],
                    ),
                    contains_all(
                        status_text,
                        [
                            "P69_post_h65_repo_graph_hygiene_inventory",
                            "P70_post_p69_archive_index_and_artifact_policy_sync",
                            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
                            CURRENT_HYGIENE_BRANCH,
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "README and STATUS should expose the current hygiene-only cleanup stack explicitly.",
        },
        {
            "item_id": "p71_docs_routers_mention_cleanup_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        docs_readme_text,
                        [
                            "H65 + P69/P70/P71 + P56/P57/P58/P59 + P66/P67/P68 + F38",
                            "plans/README.md",
                            "milestones/README.md",
                        ],
                    ),
                    contains_all(
                        milestones_readme_text,
                        [
                            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
                            "P70_post_p69_archive_index_and_artifact_policy_sync",
                            "P69_post_h65_repo_graph_hygiene_inventory",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The docs and milestones routers should expose the current hygiene-only cleanup stack.",
        },
        {
            "item_id": "p71_plans_index_points_to_post_p71_handoff",
            "status": "pass"
            if contains_all(
                plans_readme_text,
                [
                    "2026-04-01-post-p71-next-planmode-handoff.md",
                    "2026-04-01-post-p71-next-planmode-startup-prompt.md",
                    "2026-04-01-post-p71-next-planmode-brief-prompt.md",
                ],
            )
            else "blocked",
            "notes": "The plans index should route the next planning round through the post-P71 handoff files.",
        },
        {
            "item_id": "p71_post_p71_handoff_surfaces_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(
                        handoff_text,
                        [
                            CURRENT_HYGIENE_BRANCH,
                            PUBLISHED_BRANCH,
                            LOCAL_INTEGRATION_BRANCH,
                            EXPECTED_P56_TO_P66_FACT,
                            EXPECTED_ORIGIN_MAIN_TO_P66_FACT,
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                    contains_all(
                        startup_text,
                        [
                            CURRENT_HYGIENE_BRANCH,
                            PUBLISHED_BRANCH,
                            LOCAL_INTEGRATION_BRANCH,
                            EXPECTED_P56_TO_P66_FACT,
                            EXPECTED_ORIGIN_MAIN_TO_P66_FACT,
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                    contains_all(
                        brief_text,
                        [
                            CURRENT_HYGIENE_BRANCH,
                            PUBLISHED_BRANCH,
                            EXPECTED_P56_TO_P66_FACT,
                            EXPECTED_ORIGIN_MAIN_TO_P66_FACT,
                            "dirty-root integration is still out of bounds",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The next plan-mode handoff and prompts should preserve the current merge-prep readiness facts.",
        },
        {
            "item_id": "p71_merge_prep_readiness_doc_is_current",
            "status": "pass"
            if contains_all(
                merge_prep_readiness_text,
                [
                    LOCAL_INTEGRATION_BRANCH,
                    PUBLISHED_BRANCH,
                    "git merge-tree",
                    "merge execution remains absent",
                    "dirty root `main` remains quarantine-only",
                ],
            )
            else "blocked",
            "notes": "The merge-prep readiness doc should keep the route non-executing and dirty-root-free.",
        },
    ]

    claim_packet = {
        "supports": [
            "P71 records the only admissible later merge-prep readiness route from p56 to p66.",
            "P71 keeps the route read-only and conflict-screened without authorizing merge execution.",
            "P71 refreshes the next planning entrypoints while leaving H65 as the active packet.",
        ],
        "does_not_support": ["merge execution", "dirty-root integration", "runtime reopening"],
        "distilled_result": {
            "active_stage_at_readiness_time": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "current_merge_prep_readiness_sidecar": "p71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "preserved_prior_archive_index_sidecar": "p70_post_p69_archive_index_and_artifact_policy_sync",
            "current_planning_branch": current_branch_name,
            "local_integration_branch": LOCAL_INTEGRATION_BRANCH,
            "published_branch": PUBLISHED_BRANCH,
            "p56_clean": bool(p56_status["clean"]),
            "merge_tree_merge_base": str(merge_probe["merge_base"]),
            "merge_tree_conflict_free": bool(merge_probe["conflict_free"]),
            "selected_outcome": "clean_descendant_merge_prep_readiness_mapped_without_merge_execution",
            "next_required_lane": "explicit_archive_stop_or_next_planmode",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {"rows": [{"field": "p56_status", "value": p56_status}, {"field": "merge_probe", "value": merge_probe}]}

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
