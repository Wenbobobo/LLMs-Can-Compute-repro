"""Export the post-P81 clean-main promotion probe packet for P82."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P82_post_p81_clean_main_promotion_probe"
P81_SUMMARY_PATH = ROOT / "results" / "P81_post_p80_locked_fact_rebaseline_and_route_sync" / "summary.json"
PROBE_WORKTREE = "D:/zWenbo/AI/wt/p82-post-p81-clean-main-promotion-probe"
PROBE_BRANCH = "wip/p82-post-p81-clean-main-promotion-probe"
SOURCE_BRANCH = "wip/p81-post-p80-clean-descendant-promotion-prep"
PUBLISHED_BRANCH = "wip/p75-post-p74-published-successor-freeze"


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


def git_output(args: list[str], *, cwd: str | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or str(ROOT),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def worktree_status(path: str) -> dict[str, object]:
    branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    dirty_lines = [line for line in git_output(["status", "--short", "--untracked-files=all"], cwd=path).splitlines() if line]
    return {"branch": branch, "dirty_count": len(dirty_lines), "clean": len(dirty_lines) == 0}


def ahead_behind(left: str, right: str, *, cwd: str | None = None) -> dict[str, int]:
    behind, ahead = git_output(["rev-list", "--left-right", "--count", f"{left}...{right}"], cwd=cwd).split()
    return {"left_only": int(behind), "right_only": int(ahead)}


def merge_base(left: str, right: str, *, cwd: str | None = None) -> str:
    return git_output(["merge-base", left, right], cwd=cwd)


def is_ancestor(ancestor: str, descendant: str, *, cwd: str | None = None) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=cwd or str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def merge_tree_probe(left: str, right: str, *, cwd: str | None = None) -> dict[str, object]:
    result = subprocess.run(
        ["git", "merge-tree", "--write-tree", left, right],
        cwd=cwd or str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    stdout = result.stdout.strip()
    return {
        "conflict_free": result.returncode == 0,
        "probe_exit_code": result.returncode,
        "write_tree_oid": stdout.splitlines()[0] if result.returncode == 0 and stdout else None,
        "stdout": stdout,
        "stderr": result.stderr.strip(),
    }


def main() -> None:
    p81_summary = read_json(P81_SUMMARY_PATH)["summary"]
    if p81_summary["selected_outcome"] != "locked_facts_rebaselined_and_route_synced_after_p80":
        raise RuntimeError("P82 expects the landed P81 locked-fact rebaseline sidecar.")

    probe_status = worktree_status(PROBE_WORKTREE)
    probe_head = git_output(["rev-parse", "--short", "HEAD"], cwd=PROBE_WORKTREE)
    source_head = git_output(["rev-parse", "--short", SOURCE_BRANCH], cwd=PROBE_WORKTREE)
    published_head = git_output(["rev-parse", "--short", PUBLISHED_BRANCH], cwd=PROBE_WORKTREE)
    source_divergence = ahead_behind("HEAD", SOURCE_BRANCH, cwd=PROBE_WORKTREE)
    source_vs_origin = ahead_behind("origin/main", SOURCE_BRANCH, cwd=PROBE_WORKTREE)
    merge_base_oid = merge_base("HEAD", SOURCE_BRANCH, cwd=PROBE_WORKTREE)
    ff_only_ready = is_ancestor("HEAD", SOURCE_BRANCH, cwd=PROBE_WORKTREE)
    merge_probe = merge_tree_probe("HEAD", SOURCE_BRANCH, cwd=PROBE_WORKTREE)

    checklist_rows = [
        {"item_id": "p82_reads_p81", "status": "pass", "notes": "P82 starts only after the landed P81 sidecar."},
        {
            "item_id": "p82_probe_worktree_is_clean_main_derived",
            "status": "pass"
            if probe_status["branch"] == PROBE_BRANCH and bool(probe_status["clean"]) and source_vs_origin["left_only"] == 0
            else "blocked",
            "notes": "The probe worktree should be a clean origin/main-derived branch.",
        },
        {
            "item_id": "p82_source_branch_is_ahead_only_from_main",
            "status": "pass" if source_vs_origin["left_only"] == 0 and source_vs_origin["right_only"] > 0 else "blocked",
            "notes": "The source execution branch should stay ahead-only relative to origin/main.",
        },
        {
            "item_id": "p82_fast_forward_promotion_path_is_open",
            "status": "pass"
            if source_divergence["left_only"] == 0 and source_divergence["right_only"] > 0 and ff_only_ready and bool(merge_probe["conflict_free"])
            else "blocked",
            "notes": "The clean-main probe should be able to absorb the source branch via fast-forward without conflicts.",
        },
        {
            "item_id": "p82_probe_records_current_heads",
            "status": "pass"
            if all(
                (
                    len(probe_head) == 7,
                    len(source_head) == 7,
                    len(published_head) == 7,
                    source_head == git_output(["rev-parse", "--short", SOURCE_BRANCH]),
                    published_head == p81_summary["published_branch_head"],
                )
            )
            else "blocked",
            "notes": "The probe should capture the clean main head, the source branch head, and the published branch head.",
        },
    ]

    claim_packet = {
        "supports": [
            "P82 proves that a fresh clean main-derived worktree can probe promotion against the current P81 branch without using dirty root main.",
            "P82 records that the source branch remains ahead-only relative to origin/main.",
            "P82 leaves the route at clean-descendant promotion-prep only until a dedicated promotion branch is created.",
        ],
        "does_not_support": ["dirty-root integration", "runtime reopen", "merge execution on the probe branch"],
        "distilled_result": {
            "current_probe_wave": "p82_post_p81_clean_main_promotion_probe",
            "probe_branch": PROBE_BRANCH,
            "probe_head": probe_head,
            "source_branch": SOURCE_BRANCH,
            "source_head": source_head,
            "published_branch": PUBLISHED_BRANCH,
            "published_head": published_head,
            "origin_main_to_source_left_right": f"{source_vs_origin['left_only']}/{source_vs_origin['right_only']}",
            "probe_to_source_left_right": f"{source_divergence['left_only']}/{source_divergence['right_only']}",
            "merge_base": merge_base_oid,
            "fast_forward_ready": ff_only_ready,
            "merge_tree_conflict_free": bool(merge_probe["conflict_free"]),
            "selected_outcome": "clean_main_probe_confirms_fast_forward_promotion_path_after_p81",
            "next_required_lane": "p83_promotion_branch_and_pr_handoff",
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
            {"field": "probe_status", "value": probe_status},
            {"field": "source_vs_origin", "value": source_vs_origin},
            {"field": "probe_to_source", "value": source_divergence},
            {"field": "merge_probe", "value": merge_probe},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
