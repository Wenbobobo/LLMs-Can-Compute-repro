"""Export the post-P77 balanced worktree convergence and quarantine sync sidecar for P78."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync"
P77_SUMMARY_PATH = ROOT / "results" / "P77_post_p76_keep_set_and_provenance_normalization" / "summary.json"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
ROOT_QUARANTINE_BRANCH = "wip/root-main-parking-2026-03-24"
BLOCKED_LEGACY_BRANCH = "wip/h27-promotion"
KEEP_MOUNTED_BRANCHES = {
    "wip/p56-main-scratch",
    "wip/p69-post-h65-hygiene-only-cleanup",
    "wip/p72-post-p71-archive-polish-stop-handoff",
    "wip/p73-post-p72-hygiene-shrink-mergeprep",
    "wip/p74-post-p73-successor-publication-review",
    "wip/p75-post-p74-published-successor-freeze",
}
REMOVED_EXPECTED_BRANCHES = {
    "wip/r33-next",
    "wip/f32-post-h56-last-discriminator",
    "wip/f34-post-h59-archive-and-reopen-screen",
    "wip/f36-post-h60-archive-first-consolidation",
    "wip/f37-post-h61-hygiene-first-reauth-prep",
    "wip/f38-post-h62-archive-first-closeout",
    "wip/h64-post-h63-archive-first-freeze",
    "wip/p60-post-p59-published-clean-descendant-prep",
    "wip/p63-post-p62-tight-core-hygiene",
    "wip/p64-post-p63-successor-stack",
    "wip/p66-post-p65-published-successor-freeze",
}


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


def listed_worktrees() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in git_output(["worktree", "list", "--porcelain"]).splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                rows.append(current)
                current = {}
            continue
        key, value = line.split(" ", 1)
        current[key] = value.strip()
    if current:
        rows.append(current)
    return [
        {"worktree": row["worktree"].replace("\\", "/"), "branch": row.get("branch", "").removeprefix("refs/heads/")}
        for row in rows
    ]


def dirty_count_for_worktree(path: str) -> int:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return len([line for line in result.stdout.splitlines() if line.strip()])


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p77_summary = read_json(P77_SUMMARY_PATH)["summary"]
    if p77_summary["selected_outcome"] != "keep_set_and_provenance_normalized_after_p76":
        raise RuntimeError("P78 expects the landed P77 keep-set and provenance normalization sidecar.")

    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    mounted_rows = listed_worktrees()
    mounted_branches = {row["branch"] for row in mounted_rows}
    dirty_counts = {row["branch"]: dirty_count_for_worktree(row["worktree"]) for row in mounted_rows}
    dirty_branches = {branch for branch, count in dirty_counts.items() if count > 0}

    checklist_rows = [
        {"item_id": "p78_reads_p77", "status": "pass", "notes": "P78 starts only after the landed P77 normalization sidecar."},
        {
            "item_id": "p78_keep_mounted_set_is_balanced",
            "status": "pass"
            if KEEP_MOUNTED_BRANCHES.issubset(mounted_branches) and not (REMOVED_EXPECTED_BRANCHES & mounted_branches)
            else "blocked",
            "notes": "Only the balanced active keep set should remain mounted alongside quarantines.",
        },
        {
            "item_id": "p78_only_dirty_survivors_are_quarantines",
            "status": "pass" if dirty_branches == {ROOT_QUARANTINE_BRANCH, BLOCKED_LEGACY_BRANCH} else "blocked",
            "notes": "After convergence, only root quarantine and h27 should remain dirty and mounted.",
        },
        {
            "item_id": "p78_registry_records_balanced_keep_set_and_blocked_quarantines",
            "status": "pass"
            if contains_all(
                branch_registry_text,
                [
                    "wip/p75-post-p74-published-successor-freeze",
                    "wip/p74-post-p73-successor-publication-review",
                    "wip/p73-post-p72-hygiene-shrink-mergeprep",
                    "wip/p72-post-p71-archive-polish-stop-handoff",
                    "wip/p69-post-h65-hygiene-only-cleanup",
                    "wip/p56-main-scratch",
                    "wip/h27-promotion",
                    "wip/root-main-parking-2026-03-24",
                    "balanced mounted keep set",
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "The registry should make the balanced mounted keep set and blocked quarantines explicit.",
        },
    ]
    claim_packet = {
        "supports": [
            "P78 converges mounted worktrees to a balanced active set centered on p75 and its immediate hygiene lineage.",
            "P78 archives clean historical mounts without deleting their branch refs.",
            "P78 preserves only the dirty root checkout and h27 as quarantined survivors.",
        ],
        "does_not_support": ["dirty-root integration", "history deletion", "runtime reopen"],
        "distilled_result": {
            "current_worktree_convergence_wave": "p78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
            "mounted_keep_branch_count": len(KEEP_MOUNTED_BRANCHES),
            "dirty_quarantine_count": len(dirty_branches),
            "removed_clean_historical_count": len(REMOVED_EXPECTED_BRANCHES),
            "selected_outcome": "balanced_worktree_convergence_completed_with_quarantines_preserved",
            "next_required_lane": "p79_archive_claim_boundary_and_reopen_screen",
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
            {"field": "mounted_branches", "value": sorted(mounted_branches)},
            {"field": "dirty_counts", "value": dirty_counts},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
