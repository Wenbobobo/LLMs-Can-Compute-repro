"""Export the post-H60 clean-descendant integration-readiness sidecar for P45."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P45_post_h60_clean_descendant_integration_readiness"
H60_SUMMARY_PATH = ROOT / "results" / "H60_post_f34_next_lane_decision_packet" / "summary.json"
P43_SUMMARY_PATH = ROOT / "results" / "P43_post_h59_repo_graph_hygiene_and_merge_map" / "summary.json"
PREFERRED_WORKTREE_PREFIX = "D:/zWenbo/AI/wt/"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"
PREDECESSOR_BRANCH = "wip/f34-post-h59-archive-and-reopen-screen"


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


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


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
    normalized: list[dict[str, str]] = []
    for entry in entries:
        normalized.append(
            {
                "worktree": _normalize_path(entry.get("worktree", "")),
                "head": entry.get("HEAD", ""),
                "branch": entry.get("branch", "").removeprefix("refs/heads/"),
            }
        )
    return normalized


def branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def divergence_counts(base: str, target: str) -> dict[str, int]:
    output = git_output(["rev-list", "--left-right", "--count", f"{base}...{target}"]).strip()
    left_count, right_count = output.split()
    return {"base_only": int(left_count), "target_only": int(right_count)}


def main() -> None:
    h60_summary = read_json(H60_SUMMARY_PATH)["summary"]
    p43_summary = read_json(P43_SUMMARY_PATH)["summary"]
    if h60_summary["selected_outcome"] != "remain_planning_only_and_prepare_stop_or_archive":
        raise RuntimeError("P45 expects the landed H60 decision.")
    if p43_summary["merge_posture"] != "clean_descendant_only_never_dirty_root_main":
        raise RuntimeError("P45 expects the landed P43 merge posture.")

    current_root = _normalize_path(str(ROOT))
    current_branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    worktrees = parse_worktree_list(git_output(["worktree", "list", "--porcelain"]))
    root_main_entry = next((row for row in worktrees if row["worktree"] == ROOT_MAIN_WORKTREE), None)
    root_main_branch = root_main_entry["branch"] if root_main_entry is not None else ""
    predecessor_exists = branch_exists(PREDECESSOR_BRANCH)
    divergence = divergence_counts(PREDECESSOR_BRANCH, "HEAD") if predecessor_exists else {
        "base_only": -1,
        "target_only": -1,
    }

    checklist_rows = [
        {
            "item_id": "p45_reads_h60",
            "status": "pass",
            "notes": "P45 begins only after H60 leaves the repo in planning-only / archive posture.",
        },
        {
            "item_id": "p45_preserves_p43_merge_posture",
            "status": "pass",
            "notes": "P45 inherits the descendant-only merge rule from P43.",
        },
        {
            "item_id": "p45_current_worktree_uses_repo_local_alias_prefix",
            "status": "pass" if current_root.startswith(PREFERRED_WORKTREE_PREFIX) else "blocked",
            "notes": "The current successor line should live under D:/zWenbo/AI/wt/.",
        },
        {
            "item_id": "p45_root_main_is_quarantined",
            "status": "pass" if root_main_branch.startswith(ROOT_MAIN_BRANCH_PREFIX) else "blocked",
            "notes": "Dirty root main should remain parked on a quarantine branch.",
        },
        {
            "item_id": "p45_predecessor_branch_exists",
            "status": "pass" if predecessor_exists else "blocked",
            "notes": "The clean predecessor branch should remain visible for later clean-descendant integration.",
        },
        {
            "item_id": "p45_current_branch_is_successor_line",
            "status": "pass" if current_branch == "wip/f36-post-h60-archive-first-consolidation" else "blocked",
            "notes": "The active worktree should stay on the named archive-first successor branch.",
        },
    ]
    claim_packet = {
        "supports": [
            "P45 keeps the current work on a repo-local clean successor line under D:/zWenbo/AI/wt/.",
            "P45 preserves clean-descendant-only integration posture and keeps dirty root main quarantined.",
            "P45 records a concrete predecessor reference for later promotion or merge planning without executing a merge now.",
        ],
        "does_not_support": [
            "merging into dirty root main",
            "treating repo hygiene as scientific evidence",
            "claiming this sidecar itself promotes or merges branches",
        ],
        "distilled_result": {
            "active_stage_at_sidecar_time": "h60_post_f34_next_lane_decision_packet",
            "current_repo_hygiene_sidecar": "p45_post_h60_clean_descendant_integration_readiness",
            "preserved_prior_repo_hygiene_sidecar": "p43_post_h59_repo_graph_hygiene_and_merge_map",
            "current_worktree": current_root,
            "current_branch": current_branch,
            "preferred_predecessor_branch": PREDECESSOR_BRANCH,
            "predecessor_branch_exists": predecessor_exists,
            "predecessor_divergence_base_only": divergence["base_only"],
            "predecessor_divergence_target_only": divergence["target_only"],
            "registered_worktree_count": len(worktrees),
            "root_main_worktree": ROOT_MAIN_WORKTREE,
            "root_main_branch": root_main_branch,
            "merge_posture": "clean_descendant_only_never_dirty_root_main",
            "selected_outcome": "clean_descendant_successor_line_prepared_for_later_non_root_integration",
            "next_required_lane": "archive_first_active_packet_or_later_clean_descendant_promotion",
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
            {"policy": "current_worktree", "value": current_root},
            {"policy": "current_branch", "value": current_branch},
            {"policy": "preferred_predecessor_branch", "value": PREDECESSOR_BRANCH},
            {"policy": "predecessor_divergence_base_only", "value": divergence["base_only"]},
            {"policy": "predecessor_divergence_target_only", "value": divergence["target_only"]},
            {"policy": "root_main_branch", "value": root_main_branch},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
