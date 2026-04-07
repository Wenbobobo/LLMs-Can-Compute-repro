"""Export the post-H61 root quarantine and merge-main planning sidecar for P47."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P47_post_h61_root_quarantine_and_main_merge_planning"
H61_SUMMARY_PATH = ROOT / "results" / "H61_post_h60_archive_first_position_packet" / "summary.json"
ROOT_MAIN_WORKTREE = Path("D:/zWenbo/AI/LLMCompute")
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"
CLEAN_SOURCE_BRANCH = "wip/f36-post-h60-archive-first-consolidation"


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


def git_output(args: list[str], cwd: Path, *, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def current_branch(cwd: Path) -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"], cwd).strip()


def status_rows(cwd: Path) -> list[str]:
    return [line for line in git_output(["status", "--porcelain=v1"], cwd).splitlines() if line.strip()]


def main() -> None:
    h61_summary = read_json(H61_SUMMARY_PATH)["summary"]
    if h61_summary["selected_outcome"] != "archive_first_consolidation_becomes_default_posture":
        raise RuntimeError("P47 expects the landed H61 packet.")

    current_branch_name = current_branch(ROOT)
    root_branch_name = current_branch(ROOT_MAIN_WORKTREE)
    root_rows = status_rows(ROOT_MAIN_WORKTREE)
    merge_base = git_output(["merge-base", root_branch_name, CLEAN_SOURCE_BRANCH], ROOT).strip()
    dirty_count = len(root_rows)
    untracked_count = sum(row.startswith("??") for row in root_rows)

    checklist_rows = [
        {
            "item_id": "p47_reads_h61",
            "status": "pass",
            "notes": "P47 begins only after H61 locks archive-first as the live posture.",
        },
        {
            "item_id": "p47_current_branch_is_planning_descendant",
            "status": "pass" if current_branch_name == "wip/f37-post-h61-hygiene-first-reauth-prep" else "blocked",
            "notes": "The wave should run from the dedicated post-H61 hygiene-first clean descendant.",
        },
        {
            "item_id": "p47_root_branch_is_quarantine_parking",
            "status": "pass" if root_branch_name.startswith(ROOT_MAIN_BRANCH_PREFIX) else "blocked",
            "notes": "The parked root checkout should stay on a quarantine branch.",
        },
        {
            "item_id": "p47_root_dirty_surface_is_explicit",
            "status": "pass" if dirty_count > 0 else "blocked",
            "notes": "The parked root checkout should be recorded as dirty/untracked rather than silently treated as clean.",
        },
        {
            "item_id": "p47_merge_main_stays_planning_only",
            "status": "pass",
            "notes": "This packet records merge-main constraints but does not execute a merge.",
        },
    ]
    claim_packet = {
        "supports": [
            "P47 records the parked root checkout as quarantine-only rather than as a clean integration base.",
            "P47 keeps merge-main discussion explicit but planning-only.",
            "P47 preserves the clean source branch as the later integration candidate instead of routing through the parked root checkout.",
        ],
        "does_not_support": [
            "cleaning the parked root checkout in-place",
            "using root main as the scientific source of truth",
            "executing a merge in this packet",
        ],
        "distilled_result": {
            "active_stage_at_sidecar_time": "h61_post_h60_archive_first_position_packet",
            "current_repo_hygiene_sidecar": "p47_post_h61_root_quarantine_and_main_merge_planning",
            "current_worktree": normalize_path(str(ROOT)),
            "current_branch": current_branch_name,
            "root_parking_worktree": normalize_path(str(ROOT_MAIN_WORKTREE)),
            "root_parking_branch": root_branch_name,
            "root_dirty_entry_count": dirty_count,
            "root_untracked_entry_count": untracked_count,
            "root_has_untracked_entries": untracked_count > 0,
            "merge_base_with_f36": merge_base,
            "main_is_clean_integration_base": False,
            "selected_outcome": "quarantine_root_and_plan_main_merge_only",
            "next_required_lane": "clean_descendant_promotion_prep_or_h62_scope_decision",
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
            {"field": "root_parking_branch", "value": root_branch_name},
            {"field": "root_dirty_entry_count", "value": dirty_count},
            {"field": "root_untracked_entry_count", "value": untracked_count},
            {"field": "merge_base_with_f36", "value": merge_base},
            {"field": "main_is_clean_integration_base", "value": False},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
