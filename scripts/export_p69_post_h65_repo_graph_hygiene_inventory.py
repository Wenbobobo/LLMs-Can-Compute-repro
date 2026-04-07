"""Export the post-H65 repo-graph hygiene inventory sidecar for P69."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P69_post_h65_repo_graph_hygiene_inventory"
H65_SUMMARY_PATH = ROOT / "results" / "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet" / "summary.json"
P54_SUMMARY_PATH = ROOT / "results" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming" / "summary.json"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
KEEP_SET_PATH = ROOT / "docs" / "milestones" / "P69_post_h65_repo_graph_hygiene_inventory" / "keep_set.md"
CURRENT_HYGIENE_BRANCH = "wip/p69-post-h65-hygiene-only-cleanup"
PUBLISHED_BRANCH = "wip/p66-post-p65-published-successor-freeze"
LOCAL_INTEGRATION_BRANCH = "wip/p56-main-scratch"
PRIOR_PUBLISHED_BRANCH = "wip/p63-post-p62-tight-core-hygiene"
PRIOR_REVIEW_BRANCH = "wip/p64-post-p63-successor-stack"
PRIOR_ACTIVE_SUPPORT_BRANCH = "wip/h64-post-h63-archive-first-freeze"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
ROOT_MAIN_BRANCH = "wip/root-main-parking-2026-03-24"
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"
PREFERRED_WORKTREE_PREFIX = "D:/zWenbo/AI/wt/"
EXPECTED_P56_TO_P66_DIVERGENCE = (0, 18)
EXPECTED_ORIGIN_MAIN_TO_P66_DIVERGENCE = (0, 159)


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


def tracked_upstream(branch: str) -> str:
    return git_output(["for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch}"])


def listed_worktrees() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in git_output(["worktree", "list", "--porcelain"]).splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, value = line.split(" ", 1)
        current[key] = value.strip()
    if current:
        entries.append(current)
    return [
        {
            "worktree": entry.get("worktree", "").replace("\\", "/"),
            "branch": entry.get("branch", "").removeprefix("refs/heads/"),
        }
        for entry in entries
    ]


def worktree_status(path: str) -> dict[str, object]:
    branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    dirty_lines = [line for line in git_output(["status", "--short", "--untracked-files=all"], cwd=path).splitlines() if line]
    return {"branch": branch, "dirty_count": len(dirty_lines), "clean": len(dirty_lines) == 0}


def divergence(left: str, right: str) -> tuple[int, int]:
    left_count, right_count = git_output(["rev-list", "--left-right", "--count", f"{left}...{right}"]).split()
    return int(left_count), int(right_count)


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    h65_summary = read_json(H65_SUMMARY_PATH)["summary"]
    p54_summary = read_json(P54_SUMMARY_PATH)["summary"]
    if h65_summary["selected_outcome"] != "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop":
        raise RuntimeError("P69 expects the landed H65 terminal-freeze posture.")
    if p54_summary["selected_outcome"] != "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution":
        raise RuntimeError("P69 expects the preserved prior P54 hygiene posture.")

    current_branch_name = current_branch()
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    keep_set_text = read_text(KEEP_SET_PATH)
    worktrees = listed_worktrees()
    worktree_by_path = {entry["worktree"]: entry["branch"] for entry in worktrees}

    clean_keep_paths = {
        "D:/zWenbo/AI/wt/p56-main-scratch": LOCAL_INTEGRATION_BRANCH,
        "D:/zWenbo/AI/wt/p63-post-p62-tight-core-hygiene": PRIOR_PUBLISHED_BRANCH,
        "D:/zWenbo/AI/wt/p64-post-p63-successor-stack": PRIOR_REVIEW_BRANCH,
        "D:/zWenbo/AI/wt/h64-post-h63-archive-first-freeze": PRIOR_ACTIVE_SUPPORT_BRANCH,
        "D:/zWenbo/AI/wt/p66-post-p65-published-successor-freeze": PUBLISHED_BRANCH,
    }
    clean_status_rows = {path: worktree_status(path) for path in clean_keep_paths}
    clean_keep_set_ok = all(
        worktree_by_path.get(path) == expected_branch and status["branch"] == expected_branch and bool(status["clean"])
        for path, expected_branch in clean_keep_paths.items()
        for status in [clean_status_rows[path]]
    )

    root_main_branch = worktree_by_path.get(ROOT_MAIN_WORKTREE, "")
    root_main_status = worktree_status(ROOT_MAIN_WORKTREE)
    root_main_quarantined = root_main_branch.startswith(ROOT_MAIN_BRANCH_PREFIX) and root_main_status["branch"].startswith(
        ROOT_MAIN_BRANCH_PREFIX
    )
    p56_to_p66_left_count, p56_to_p66_right_count = divergence(LOCAL_INTEGRATION_BRANCH, PUBLISHED_BRANCH)
    origin_main_to_p66_left_count, origin_main_to_p66_right_count = divergence("origin/main", PUBLISHED_BRANCH)
    published_branch_upstream = tracked_upstream(PUBLISHED_BRANCH)

    checklist_rows = [
        {"item_id": "p69_reads_h65", "status": "pass", "notes": "P69 runs only after H65 lands the terminal archive-first freeze packet."},
        {"item_id": "p69_reads_preserved_prior_hygiene_sidecar", "status": "pass", "notes": "P69 extends the preserved P54 hygiene posture rather than reopening science."},
        {
            "item_id": "p69_runs_on_repo_local_hygiene_branch",
            "status": "pass"
            if current_branch_name == CURRENT_HYGIENE_BRANCH and str(ROOT).replace("\\", "/").startswith(PREFERRED_WORKTREE_PREFIX)
            else "blocked",
            "notes": "P69 should run from the repo-local hygiene worktree rather than dirty root main.",
        },
        {
            "item_id": "p69_branch_registry_mentions_current_keep_set",
            "status": "pass"
            if contains_all(
                branch_registry_text,
                [
                    CURRENT_HYGIENE_BRANCH,
                    PUBLISHED_BRANCH,
                    LOCAL_INTEGRATION_BRANCH,
                    PRIOR_PUBLISHED_BRANCH,
                    PRIOR_REVIEW_BRANCH,
                    ROOT_MAIN_BRANCH,
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "The branch/worktree registry should expose the current hygiene branch, live published branch, and root quarantine.",
        },
        {
            "item_id": "p69_keep_set_doc_is_current",
            "status": "pass"
            if contains_all(
                keep_set_text,
                [
                    CURRENT_HYGIENE_BRANCH,
                    PUBLISHED_BRANCH,
                    LOCAL_INTEGRATION_BRANCH,
                    ROOT_MAIN_BRANCH,
                    "0/18",
                    "0/159",
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "The keep-set doc should record the current topology and quarantine facts explicitly.",
        },
        {
            "item_id": "p69_clean_keep_set_worktrees_remain_clean",
            "status": "pass" if clean_keep_set_ok else "blocked",
            "notes": "The preserved clean descendants and active published branch should all remain clean.",
        },
        {
            "item_id": "p69_root_main_remains_quarantined",
            "status": "pass" if root_main_quarantined else "blocked",
            "notes": "Dirty root main should remain parked on a quarantine branch.",
        },
        {
            "item_id": "p69_p56_to_p66_divergence_matches_linear_successor_fact",
            "status": "pass"
            if (p56_to_p66_left_count, p56_to_p66_right_count) == EXPECTED_P56_TO_P66_DIVERGENCE
            else "blocked",
            "notes": "The current published branch should remain a one-sided 18-commit successor above p56.",
        },
        {
            "item_id": "p69_origin_main_to_p66_divergence_remains_out_of_bounds",
            "status": "pass"
            if (origin_main_to_p66_left_count, origin_main_to_p66_right_count) == EXPECTED_ORIGIN_MAIN_TO_P66_DIVERGENCE
            else "blocked",
            "notes": "The published clean descendant should remain far enough ahead of origin/main that dirty-root integration stays inadmissible.",
        },
        {
            "item_id": "p69_p66_published_branch_is_tracked",
            "status": "pass" if published_branch_upstream == f"origin/{PUBLISHED_BRANCH}" else "blocked",
            "notes": "The live published branch should remain pushed and tracked at origin.",
        },
    ]

    claim_packet = {
        "supports": [
            "P69 inventories the post-H65 tight-core keep set without reopening science.",
            "P69 preserves dirty root main as quarantine-only and keeps clean-descendant merge posture explicit.",
            "P69 records the live p56..p66 and origin/main..p66 topology facts for later readiness-only discussion.",
        ],
        "does_not_support": ["merge execution", "dirty-root integration", "runtime reopening"],
        "distilled_result": {
            "active_stage_at_hygiene_time": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "current_repo_hygiene_sidecar": "p69_post_h65_repo_graph_hygiene_inventory",
            "preserved_prior_repo_hygiene_sidecar": "p54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
            "current_planning_branch": current_branch_name,
            "current_published_branch": PUBLISHED_BRANCH,
            "current_published_branch_upstream": published_branch_upstream,
            "root_main_branch": root_main_branch,
            "root_main_dirty_count": int(root_main_status["dirty_count"]),
            "clean_keep_set_count": sum(int(status["clean"]) for status in clean_status_rows.values()),
            "p56_to_p66_left_count": p56_to_p66_left_count,
            "p56_to_p66_right_count": p56_to_p66_right_count,
            "origin_main_to_p66_left_count": origin_main_to_p66_left_count,
            "origin_main_to_p66_right_count": origin_main_to_p66_right_count,
            "selected_outcome": "repo_graph_hygiene_inventory_confirms_clean_descendant_keep_set_and_root_quarantine",
            "next_required_lane": "p70_archive_index_and_artifact_policy_sync",
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
    snapshot = {
        "rows": [
            {"field": "listed_worktrees", "value": worktrees},
            {"field": "clean_keep_status", "value": clean_status_rows},
            {"field": "root_main_status", "value": root_main_status},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
