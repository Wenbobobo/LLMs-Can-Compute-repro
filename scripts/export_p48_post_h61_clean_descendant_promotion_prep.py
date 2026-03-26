"""Export the post-H61 clean-descendant promotion prep sidecar for P48."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P48_post_h61_clean_descendant_promotion_prep"
P45_SUMMARY_PATH = ROOT / "results" / "P45_post_h60_clean_descendant_integration_readiness" / "summary.json"
P47_SUMMARY_PATH = ROOT / "results" / "P47_post_h61_root_quarantine_and_main_merge_planning" / "summary.json"
SOURCE_BRANCH = "wip/f36-post-h60-archive-first-consolidation"
IGNORED_CLEANLINESS_PREFIXES = (
    "results/P47_post_h61_root_quarantine_and_main_merge_planning/",
    "results/P48_post_h61_clean_descendant_promotion_prep/",
    "results/P49_post_h61_origin_advisory_sync/",
    "results/F37_post_h61_compiled_online_coprocessor_reauthorization_bundle/",
    "results/H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet/",
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def git_output(args: list[str], *, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def tracked_upstream(branch: str) -> str:
    return git_output(["for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch}"]).strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"]).strip()


def tracked_status_rows() -> list[str]:
    return [line.strip() for line in git_output(["status", "--porcelain=v1"]).splitlines() if line.strip()]


def is_ignored_cleanliness_row(row: str) -> bool:
    path = row[3:].replace("\\", "/") if len(row) >= 4 else ""
    return any(path.startswith(prefix) for prefix in IGNORED_CLEANLINESS_PREFIXES)


def worktree_clean() -> bool:
    return not any(not is_ignored_cleanliness_row(row) for row in tracked_status_rows())


def changed_files(base: str, target: str) -> list[str]:
    return [line.strip() for line in git_output(["diff", "--name-only", f"{base}..{target}"]).splitlines() if line.strip()]


def oversize_count(paths: list[str]) -> int:
    count = 0
    for rel_path in paths:
        candidate = ROOT / rel_path
        if candidate.exists() and candidate.is_file() and candidate.stat().st_size >= 10 * 1024 * 1024:
            count += 1
    return count


def main() -> None:
    p45_summary = read_json(P45_SUMMARY_PATH)["summary"]
    p47_summary = read_json(P47_SUMMARY_PATH)["summary"]
    if p45_summary["merge_posture"] != "clean_descendant_only_never_dirty_root_main":
        raise RuntimeError("P48 expects the landed P45 hygiene posture.")
    if p47_summary["selected_outcome"] != "quarantine_root_and_plan_main_merge_only":
        raise RuntimeError("P48 expects the landed P47 quarantine posture.")

    current_branch_name = current_branch()
    source_exists = branch_exists(SOURCE_BRANCH)
    source_upstream = tracked_upstream(SOURCE_BRANCH) if source_exists else ""
    current_upstream = tracked_upstream(current_branch_name)
    candidate_files = changed_files(SOURCE_BRANCH, "HEAD") if source_exists else []
    commit_count = int(git_output(["rev-list", "--count", f"{SOURCE_BRANCH}..HEAD"]).strip()) if source_exists else -1

    checklist_rows = [
        {
            "item_id": "p48_reads_p45",
            "status": "pass",
            "notes": "P48 preserves the descendant-only merge posture from P45.",
        },
        {
            "item_id": "p48_reads_p47",
            "status": "pass",
            "notes": "P48 treats the parked root checkout as quarantine-only rather than as a promotion base.",
        },
        {
            "item_id": "p48_source_branch_exists",
            "status": "pass" if source_exists else "blocked",
            "notes": "The published post-H60 clean descendant should remain available as the preserved source branch.",
        },
        {
            "item_id": "p48_source_branch_is_published",
            "status": "pass" if bool(source_upstream) else "blocked",
            "notes": "The source branch should track an upstream before later promotion planning continues.",
        },
        {
            "item_id": "p48_current_worktree_is_clean",
            "status": "pass" if worktree_clean() else "blocked",
            "notes": "Promotion prep should be recorded from a clean descendant worktree state, excluding current-wave exporter outputs.",
        },
    ]
    claim_packet = {
        "supports": [
            "P48 makes the clean descendant promotion range explicit as f36..f37.",
            "P48 separates promotion prep from merge execution.",
            "P48 records oversized-artifact posture before any later explicit promotion packet.",
        ],
        "does_not_support": [
            "executing a promotion or merge in this packet",
            "routing promotion through the parked root checkout",
            "treating branch publication as scientific evidence",
        ],
        "distilled_result": {
            "active_stage_at_sidecar_time": "h61_post_h60_archive_first_position_packet",
            "current_repo_hygiene_sidecar": "p48_post_h61_clean_descendant_promotion_prep",
            "preserved_prior_repo_hygiene_sidecar": "p45_post_h60_clean_descendant_integration_readiness",
            "source_branch": SOURCE_BRANCH,
            "source_branch_upstream": source_upstream,
            "current_planning_branch": current_branch_name,
            "current_planning_branch_upstream": current_upstream,
            "candidate_commit_count": commit_count,
            "candidate_file_count": len(candidate_files),
            "artifact_oversize_count": oversize_count(candidate_files),
            "worktree_clean": worktree_clean(),
            "selected_outcome": "clean_descendant_ready_for_later_explicit_promotion",
            "next_required_lane": "later_explicit_promotion_packet_or_h62_scope_decision",
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
            {"field": "source_branch", "value": SOURCE_BRANCH},
            {"field": "current_planning_branch", "value": current_branch_name},
            {"field": "candidate_commit_count", "value": commit_count},
            {"field": "candidate_file_count", "value": len(candidate_files)},
            {"field": "artifact_oversize_count", "value": oversize_count(candidate_files)},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
