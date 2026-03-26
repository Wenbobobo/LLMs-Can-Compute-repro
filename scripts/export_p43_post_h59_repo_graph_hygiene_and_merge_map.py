"""Export the post-H59 repo-graph hygiene and merge-map sidecar for P43."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P43_post_h59_repo_graph_hygiene_and_merge_map"
PREFERRED_WORKTREE_PREFIX = "D:/zWenbo/AI/wt/"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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


def build_summary_rows(worktrees: list[dict[str, str]], *, current_root: str, current_branch: str) -> dict[str, Any]:
    root_main_entry = next((row for row in worktrees if row["worktree"] == ROOT_MAIN_WORKTREE), None)
    repo_local_aliases = [
        row["worktree"]
        for row in worktrees
        if row["worktree"].startswith(PREFERRED_WORKTREE_PREFIX)
    ]
    root_main_branch = root_main_entry["branch"] if root_main_entry is not None else ""
    root_main_quarantined = bool(root_main_branch.startswith(ROOT_MAIN_BRANCH_PREFIX))
    current_registered = any(
        row["worktree"] == current_root and row["branch"] == current_branch for row in worktrees
    )
    return {
        "root_main_branch": root_main_branch,
        "root_main_quarantined": root_main_quarantined,
        "repo_local_aliases": sorted(repo_local_aliases),
        "repo_local_alias_count": len(repo_local_aliases),
        "current_registered": current_registered,
        "registered_worktree_count": len(worktrees),
    }


def main() -> None:
    current_root = _normalize_path(str(ROOT))
    current_branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    worktrees = parse_worktree_list(git_output(["worktree", "list", "--porcelain"]))
    derived = build_summary_rows(worktrees, current_root=current_root, current_branch=current_branch)

    checklist_rows = [
        {
            "item_id": "p43_reads_git_worktree_graph",
            "status": "pass" if worktrees else "blocked",
            "notes": "P43 should read the registered git worktree graph successfully.",
        },
        {
            "item_id": "p43_current_worktree_uses_repo_local_alias_prefix",
            "status": "pass" if current_root.startswith(PREFERRED_WORKTREE_PREFIX) else "blocked",
            "notes": "The current wave should live on D:/zWenbo/AI/wt/... rather than on the root checkout.",
        },
        {
            "item_id": "p43_root_main_is_quarantined",
            "status": "pass" if derived["root_main_quarantined"] else "blocked",
            "notes": "Dirty root main should remain parked on a quarantine branch.",
        },
        {
            "item_id": "p43_current_worktree_is_registered",
            "status": "pass" if derived["current_registered"] else "blocked",
            "notes": "The active f34 worktree should be a registered descendant worktree, not an ad hoc clone.",
        },
        {
            "item_id": "p43_merge_posture_is_descendant_only",
            "status": "pass" if derived["root_main_quarantined"] else "blocked",
            "notes": "Merge posture stays clean-descendant-only and never targets dirty root main directly.",
        },
    ]
    claim_packet = {
        "supports": [
            "P43 records the preferred repo-local worktree graph rooted at D:/zWenbo/AI/wt/.",
            "P43 keeps dirty root main quarantined and preserves explicit no-merge posture.",
            "P43 makes the current branch/worktree identity machine-readable for later hygiene work.",
        ],
        "does_not_support": [
            "merging into dirty root main during this wave",
            "scientific execution from the root checkout",
            "treating merge posture as scientific evidence",
        ],
        "distilled_result": {
            "active_stage_at_sidecar_time": "h59_post_h58_reproduction_gap_decision_packet",
            "current_repo_hygiene_sidecar": "p43_post_h59_repo_graph_hygiene_and_merge_map",
            "preferred_worktree_prefix": PREFERRED_WORKTREE_PREFIX,
            "current_worktree": current_root,
            "current_branch": current_branch,
            "registered_worktree_count": derived["registered_worktree_count"],
            "repo_local_alias_count": derived["repo_local_alias_count"],
            "root_main_worktree": ROOT_MAIN_WORKTREE,
            "root_main_branch": derived["root_main_branch"],
            "root_main_quarantined": derived["root_main_quarantined"],
            "merge_posture": "clean_descendant_only_never_dirty_root_main",
            "next_required_lane": "docs_only_decision_or_archive",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
            "repo_local_aliases": derived["repo_local_aliases"],
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"policy": "current_worktree", "value": current_root},
            {"policy": "current_branch", "value": current_branch},
            {"policy": "registered_worktree_count", "value": derived["registered_worktree_count"]},
            {"policy": "repo_local_alias_count", "value": derived["repo_local_alias_count"]},
            {"policy": "root_main_branch", "value": derived["root_main_branch"]},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
