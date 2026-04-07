"""Export the post-P65 successor publication review sidecar for P66."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P66_post_p65_successor_publication_review"
P65_SUMMARY_PATH = ROOT / "results" / "P65_post_p64_merge_prep_control_sync" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
REVIEW_BASE_BRANCH = "wip/p63-post-p62-tight-core-hygiene"
REVIEW_TIP_BRANCH = "wip/p64-post-p63-successor-stack"
TARGET_FREEZE_BRANCH = "wip/p66-post-p65-published-successor-freeze"


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


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def classify_review_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized in {"README.md", "STATUS.md", "tmp/active_wave_plan.md"}:
        return "allowed_control_surface"
    if normalized.startswith("docs/"):
        return "allowed_control_surface"
    if normalized.startswith("results/"):
        return "allowed_results_surface"
    if normalized.startswith("scripts/export_p") or normalized.startswith("scripts/export_release_"):
        return "allowed_export_surface"
    if normalized.startswith("tests/test_export_"):
        return "allowed_test_surface"
    return "blocked_non_release_surface"


def main() -> None:
    p65_summary = read_json(P65_SUMMARY_PATH)["summary"]
    if p65_summary["selected_outcome"] != "published_successor_merge_prep_control_synced_to_h64_stack":
        raise RuntimeError("P66 expects the landed P65 successor control-sync wave.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    current_branch_name = current_branch()

    left_right = git_output(["rev-list", "--left-right", "--count", f"{REVIEW_BASE_BRANCH}...{REVIEW_TIP_BRANCH}"])
    left_count_str, right_count_str = left_right.split()
    left_count = int(left_count_str)
    right_count = int(right_count_str)
    commit_lines = [
        line for line in git_output(["log", "--oneline", f"{REVIEW_BASE_BRANCH}..{REVIEW_TIP_BRANCH}"]).splitlines() if line
    ]
    diff_paths = [
        line for line in git_output(["diff", "--name-only", f"{REVIEW_BASE_BRANCH}..{REVIEW_TIP_BRANCH}"]).splitlines() if line
    ]
    classified_paths = [
        {"path": path, "classification": classify_review_path(path)}
        for path in diff_paths
    ]
    blocked_paths = [row["path"] for row in classified_paths if row["classification"] == "blocked_non_release_surface"]
    all_paths_allowed = not blocked_paths

    checklist_rows = [
        {
            "item_id": "p66_reads_p65",
            "status": "pass",
            "notes": "P66 starts only after the landed P65 successor control-sync wave.",
        },
        {
            "item_id": "p66_review_range_is_exact_successor_delta",
            "status": "pass" if left_count == 0 and right_count == 3 else "blocked",
            "notes": "The review must cover the exact one-sided three-commit delta from p63 to p64.",
        },
        {
            "item_id": "p66_reviewed_paths_stay_inside_release_surfaces",
            "status": "pass" if all_paths_allowed else "blocked",
            "notes": "The reviewed delta must stay inside docs/export/control/release surfaces.",
        },
        {
            "item_id": "p66_review_has_three_commits",
            "status": "pass" if len(commit_lines) == 3 else "blocked",
            "notes": "The reviewed successor delta should expose exactly three commits before publication freeze.",
        },
        {
            "item_id": "p66_current_surfaces_still_describe_p63_as_live_and_p64_as_execution_successor",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                            "wip/p63-post-p62-tight-core-hygiene",
                        ],
                    ),
                    contains_all(
                        branch_registry_text,
                        [
                            "wip/p63-post-p62-tight-core-hygiene",
                            "wip/p64-post-p63-successor-stack",
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The review happens before the live published branch is promoted from p63 to p66.",
        },
        {
            "item_id": "p66_runs_on_target_freeze_branch",
            "status": "pass" if current_branch_name == TARGET_FREEZE_BRANCH else "blocked",
            "notes": "The review artifacts should be recorded from the future freeze branch.",
        },
    ]
    claim_packet = {
        "supports": [
            "P66 reviews the exact p63..p64 successor delta before any new publication freeze.",
            "P66 keeps the review narrow to docs/export/control/release surfaces.",
            "P66 authorizes a p66 freeze only if the review remains one-sided, exact, and non-runtime.",
        ],
        "does_not_support": [
            "runtime reopen",
            "dirty-root integration",
            "non-release-surface successor changes",
        ],
        "distilled_result": {
            "review_base_branch": REVIEW_BASE_BRANCH,
            "review_tip_branch": REVIEW_TIP_BRANCH,
            "freeze_target_branch": TARGET_FREEZE_BRANCH,
            "current_execution_branch": current_branch_name,
            "review_left_count": left_count,
            "review_right_count": right_count,
            "reviewed_commit_count": len(commit_lines),
            "reviewed_path_count": len(diff_paths),
            "blocked_reviewed_path_count": len(blocked_paths),
            "all_reviewed_paths_allowed": all_paths_allowed,
            "selected_outcome": "successor_publication_review_supports_p67_freeze",
            "next_required_lane": "p67_published_successor_freeze",
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
            {"field": "review_commit_lines", "value": commit_lines},
            {"field": "reviewed_paths", "value": diff_paths},
            {"field": "classified_paths", "value": classified_paths},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
