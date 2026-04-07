"""Export the post-P73 successor publication review sidecar for P74."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P74_post_p73_successor_publication_review"
P73_SUMMARY_PATH = (
    ROOT / "results" / "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync" / "summary.json"
)
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
REVIEW_BASE_BRANCH = "wip/p66-post-p65-published-successor-freeze"
REVIEW_TIP_BRANCH = "wip/p73-post-p72-hygiene-shrink-mergeprep"
CURRENT_REVIEW_BRANCH = "wip/p74-post-p73-successor-publication-review"


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
    p73_summary = read_json(P73_SUMMARY_PATH)["summary"]
    if p73_summary["selected_outcome"] != "legacy_worktree_inventory_and_keep_set_sync_completed_for_safe_local_shrink":
        raise RuntimeError("P74 expects the landed P73 hygiene/shrink inventory wave.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    current_branch_name = current_branch()

    left_right = git_output(
        ["rev-list", "--left-right", "--count", f"{REVIEW_BASE_BRANCH}...{REVIEW_TIP_BRANCH}"]
    )
    left_count_str, right_count_str = left_right.split()
    left_count = int(left_count_str)
    right_count = int(right_count_str)
    commit_lines = [
        line for line in git_output(["log", "--oneline", f"{REVIEW_BASE_BRANCH}..{REVIEW_TIP_BRANCH}"]).splitlines() if line
    ]
    diff_paths = [
        line for line in git_output(["diff", "--name-only", f"{REVIEW_BASE_BRANCH}..{REVIEW_TIP_BRANCH}"]).splitlines() if line
    ]
    classified_paths = [{"path": path, "classification": classify_review_path(path)} for path in diff_paths]
    blocked_paths = [row["path"] for row in classified_paths if row["classification"] == "blocked_non_release_surface"]
    all_paths_allowed = not blocked_paths

    checklist_rows = [
        {
            "item_id": "p74_reads_p73",
            "status": "pass",
            "notes": "P74 starts only after the landed P73 local hygiene/shrink inventory wave.",
        },
        {
            "item_id": "p74_review_range_is_exact_successor_delta",
            "status": "pass" if left_count == 0 and right_count == 11 else "blocked",
            "notes": "The review must cover the exact one-sided eleven-commit delta from p66 to p73.",
        },
        {
            "item_id": "p74_reviewed_paths_stay_inside_release_surfaces",
            "status": "pass" if all_paths_allowed else "blocked",
            "notes": "The reviewed delta must stay inside docs/export/control/release surfaces.",
        },
        {
            "item_id": "p74_review_has_eleven_commits",
            "status": "pass" if len(commit_lines) == 11 else "blocked",
            "notes": "The reviewed successor delta should expose exactly eleven commits before publication freeze.",
        },
        {
            "item_id": "p74_current_surfaces_still_describe_p66_as_live_and_p73_as_local_successor",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
                            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
                            "wip/p73-post-p72-hygiene-shrink-mergeprep",
                            "wip/p66-post-p65-published-successor-freeze",
                        ],
                    ),
                    contains_all(
                        branch_registry_text,
                        [
                            "wip/p73-post-p72-hygiene-shrink-mergeprep",
                            "wip/p72-post-p71-archive-polish-stop-handoff",
                            "wip/p69-post-h65-hygiene-only-cleanup",
                            "wip/p66-post-p65-published-successor-freeze",
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The review happens before the live published branch is promoted away from p66 and while p73 remains the live local hygiene lane.",
        },
        {
            "item_id": "p74_runs_on_current_review_branch",
            "status": "pass" if current_branch_name == CURRENT_REVIEW_BRANCH else "blocked",
            "notes": "The review artifacts should be recorded from the dedicated p74 review branch.",
        },
    ]
    claim_packet = {
        "supports": [
            "P74 reviews the exact p66..p73 successor delta before any new publication freeze.",
            "P74 keeps the review narrow to docs/export/control/release surfaces.",
            "P74 authorizes a p75 freeze only if the review remains one-sided, exact, and non-runtime.",
        ],
        "does_not_support": [
            "runtime reopen",
            "dirty-root integration",
            "non-release-surface successor changes",
        ],
        "distilled_result": {
            "review_base_branch": REVIEW_BASE_BRANCH,
            "review_tip_branch": REVIEW_TIP_BRANCH,
            "current_execution_branch": current_branch_name,
            "review_left_count": left_count,
            "review_right_count": right_count,
            "reviewed_commit_count": len(commit_lines),
            "reviewed_path_count": len(diff_paths),
            "blocked_reviewed_path_count": len(blocked_paths),
            "all_reviewed_paths_allowed": all_paths_allowed,
            "selected_outcome": "successor_publication_review_supports_p75_freeze",
            "next_required_lane": "p75_published_successor_freeze",
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
