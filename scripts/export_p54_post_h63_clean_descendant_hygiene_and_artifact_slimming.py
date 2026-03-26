"""Export the post-H63 clean-descendant hygiene and artifact-slimming sidecar."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming"
H63_SUMMARY_PATH = ROOT / "results" / "H63_post_p50_p51_p52_f38_archive_first_closeout_packet" / "summary.json"
P52_SUMMARY_PATH = ROOT / "results" / "P52_post_h62_clean_descendant_hygiene_and_merge_prep" / "summary.json"
SOURCE_BRANCH = "wip/f38-post-h62-archive-first-closeout"
PREFERRED_WORKTREE_PREFIX = "D:/zWenbo/AI/wt/"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"
RAW_ROW_PATTERNS = [
    "results/**/probe_read_rows.json",
    "results/**/per_read_rows.json",
    "results/**/trace_rows.json",
    "results/**/step_rows.json",
]
MERGE_RULES_PATH = ROOT / "docs" / "milestones" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming" / "merge_prep_rules.md"
ARTIFACT_POLICY_PATH = ROOT / "docs" / "milestones" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming" / "artifact_policy.md"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"


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


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"]).strip()


def tracked_upstream(branch: str) -> str:
    return git_output(["for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch}"]).strip()


def branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def parse_worktree_list(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in text.splitlines():
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


def tracked_large_files() -> list[str]:
    tracked = [path for path in git_output(["ls-files", "-z"]).split("\0") if path]
    rows: list[str] = []
    for rel_path in tracked:
        candidate = ROOT / rel_path
        if candidate.exists() and candidate.is_file() and candidate.stat().st_size >= 10 * 1024 * 1024:
            rows.append(rel_path.replace("\\", "/"))
    return rows


def raw_row_ignore_rules_active() -> bool:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    return all(pattern in text for pattern in RAW_ROW_PATTERNS)


def merge_rule_text_ok(current_branch_name: str) -> bool:
    text = MERGE_RULES_PATH.read_text(encoding="utf-8")
    required = [
        SOURCE_BRANCH,
        current_branch_name,
        "clean_descendant_only_never_dirty_root_main",
    ]
    return all(pattern in text for pattern in required)


def artifact_policy_ok() -> bool:
    text = ARTIFACT_POLICY_PATH.read_text(encoding="utf-8")
    required = ["surface_report.json", "10 MiB", "summary tables"]
    return all(pattern in text for pattern in required)


def current_stage_driver_ok() -> bool:
    text = CURRENT_STAGE_DRIVER_PATH.read_text(encoding="utf-8")
    required = [
        "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
        "clean_descendant_only_never_dirty_root_main",
    ]
    return all(pattern in text for pattern in required)


def main() -> None:
    h63_summary = read_json(H63_SUMMARY_PATH)["summary"]
    p52_summary = read_json(P52_SUMMARY_PATH)["summary"]
    if h63_summary["selected_outcome"] != "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant":
        raise RuntimeError("P54 expects the landed H63 closeout posture.")
    if p52_summary["selected_outcome"] != "clean_descendant_hygiene_and_merge_prep_locked_without_dirty_root_merge":
        raise RuntimeError("P54 expects the landed P52 hygiene posture.")

    current_branch_name = current_branch()
    current_upstream = tracked_upstream(current_branch_name)
    worktrees = parse_worktree_list(git_output(["worktree", "list", "--porcelain"]))
    root_main_entry = next((row for row in worktrees if row["worktree"] == ROOT_MAIN_WORKTREE), None)
    root_main_branch = root_main_entry["branch"] if root_main_entry else ""
    root_main_quarantined = bool(root_main_branch.startswith(ROOT_MAIN_BRANCH_PREFIX))
    tracked_oversize = tracked_large_files()

    checklist_rows = [
        {
            "item_id": "p54_reads_h63",
            "status": "pass",
            "notes": "P54 runs only after H63 lands the archive-first closeout packet.",
        },
        {
            "item_id": "p54_reads_p52",
            "status": "pass",
            "notes": "P54 extends P52 rather than replacing the descendant-only hygiene posture.",
        },
        {
            "item_id": "p54_source_branch_exists",
            "status": "pass" if branch_exists(SOURCE_BRANCH) else "blocked",
            "notes": "The preserved source branch should remain available for later comparison.",
        },
        {
            "item_id": "p54_current_branch_uses_repo_local_alias_prefix",
            "status": "pass" if str(ROOT).replace("\\", "/").startswith(PREFERRED_WORKTREE_PREFIX) else "blocked",
            "notes": "The current wave should run from D:/zWenbo/AI/wt/... rather than the parked root checkout.",
        },
        {
            "item_id": "p54_root_main_is_quarantined",
            "status": "pass" if root_main_quarantined else "blocked",
            "notes": "Dirty root main should remain parked on a quarantine branch.",
        },
        {
            "item_id": "p54_raw_row_ignore_rules_active",
            "status": "pass" if raw_row_ignore_rules_active() else "blocked",
            "notes": "Raw-row ignore rules should remain active in .gitignore.",
        },
        {
            "item_id": "p54_no_tracked_oversize_artifacts",
            "status": "pass" if not tracked_oversize else "blocked",
            "notes": "The clean descendant should not track artifacts at or above roughly 10 MiB.",
        },
        {
            "item_id": "p54_merge_rules_doc_is_current",
            "status": "pass" if merge_rule_text_ok(current_branch_name) else "blocked",
            "notes": "The merge-prep rules doc should reflect the current clean-descendant posture.",
        },
        {
            "item_id": "p54_artifact_policy_doc_is_current",
            "status": "pass" if artifact_policy_ok() else "blocked",
            "notes": "The artifact policy doc should mention oversize surface-report handling explicitly.",
        },
        {
            "item_id": "p54_current_stage_driver_mentions_p54",
            "status": "pass" if current_stage_driver_ok() else "blocked",
            "notes": "The current stage driver should expose P54 as the current hygiene sidecar.",
        },
    ]
    claim_packet = {
        "supports": [
            "P54 refreshes clean-descendant-only hygiene and artifact policy without executing a merge.",
            "P54 keeps dirty root main quarantined and preserves the repo-local worktree rule.",
            "P54 keeps raw-row ignore rules active while making oversize surface-report handling explicit.",
        ],
        "does_not_support": [
            "merge execution",
            "dirty-root integration",
            "scientific claim widening",
        ],
        "distilled_result": {
            "active_stage_at_hygiene_time": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "current_repo_hygiene_sidecar": "p54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
            "preserved_prior_repo_hygiene_sidecar": "p52_post_h62_clean_descendant_hygiene_and_merge_prep",
            "source_branch": SOURCE_BRANCH,
            "current_planning_branch": current_branch_name,
            "current_planning_branch_upstream": current_upstream,
            "root_main_branch": root_main_branch,
            "root_main_quarantined": root_main_quarantined,
            "tracked_oversize_count": len(tracked_oversize),
            "raw_row_ignore_rules_active": raw_row_ignore_rules_active(),
            "surface_report_policy_declared": artifact_policy_ok(),
            "selected_outcome": "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution",
            "next_required_lane": "later_clean_descendant_promotion_prep_or_archive_freeze",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
            "tracked_oversize_artifacts": tracked_oversize,
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"field": "source_branch", "value": SOURCE_BRANCH},
            {"field": "current_planning_branch", "value": current_branch_name},
            {"field": "current_planning_branch_upstream", "value": current_upstream},
            {"field": "root_main_branch", "value": root_main_branch},
            {"field": "tracked_oversize_count", "value": len(tracked_oversize)},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
