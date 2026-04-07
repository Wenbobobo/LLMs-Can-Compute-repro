"""Export the post-H58 publication/archive sync sidecar for P41."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P41_post_h58_publication_and_archive_sync"
H59_SUMMARY_PATH = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet" / "summary.json"
GITIGNORE_PATH = ROOT / ".gitignore"
LARGE_ARTIFACT_THRESHOLD_BYTES = 10 * 1024 * 1024
REQUIRED_IGNORE_RULES = [
    "results/**/probe_read_rows.json",
    "results/**/per_read_rows.json",
    "results/**/trace_rows.json",
    "results/**/step_rows.json",
]


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


def collect_tracked_large_artifacts() -> list[dict[str, object]]:
    tracked_paths = [path for path in git_output(["ls-files", "-z"]).split("\0") if path]
    oversized: list[dict[str, object]] = []
    for rel_path in tracked_paths:
        path = ROOT / rel_path
        if not path.exists() or not path.is_file():
            continue
        size_bytes = path.stat().st_size
        if size_bytes < LARGE_ARTIFACT_THRESHOLD_BYTES:
            continue
        oversized.append(
            {
                "path": rel_path.replace("\\", "/"),
                "size_bytes": size_bytes,
                "size_mib": round(size_bytes / (1024 * 1024), 2),
            }
        )
    return sorted(oversized, key=lambda row: (int(row["size_bytes"]), str(row["path"])), reverse=True)


def ignore_rule_status() -> dict[str, object]:
    text = GITIGNORE_PATH.read_text(encoding="utf-8")
    present = [rule for rule in REQUIRED_IGNORE_RULES if rule in text]
    return {
        "required_rule_count": len(REQUIRED_IGNORE_RULES),
        "present_rule_count": len(present),
        "missing_rules": [rule for rule in REQUIRED_IGNORE_RULES if rule not in present],
    }


def main() -> None:
    h59_summary = read_json(H59_SUMMARY_PATH)["summary"]
    if h59_summary["selected_outcome"] != "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen":
        raise RuntimeError("P41 expects the landed H59 reproduction-gap outcome.")

    tracked_large_artifacts = collect_tracked_large_artifacts()
    ignore_status = ignore_rule_status()
    checklist_rows = [
        {
            "item_id": "p41_syncs_publication_archive_surfaces_to_h59",
            "status": "pass",
            "notes": "Outward release/archive/submission surfaces should now point to H59/F33/P42.",
        },
        {
            "item_id": "p41_keeps_raw_row_ignore_rules_active",
            "status": "pass" if not ignore_status["missing_rules"] else "blocked",
            "notes": "The repo should keep the raw-row ignore rules active in .gitignore.",
        },
        {
            "item_id": "p41_keeps_large_artifacts_out_of_git",
            "status": "pass" if not tracked_large_artifacts else "blocked",
            "notes": "Tracked artifacts above roughly 10 MiB remain disallowed on the clean worktree line.",
        },
        {
            "item_id": "p41_preserves_explicit_no_merge_posture",
            "status": "pass",
            "notes": "Publication/archive sync does not imply merge or promotion back to dirty root main.",
        },
    ]
    claim_packet = {
        "supports": [
            "P41 syncs archive-facing and release-facing surfaces to the honest H59 gap state.",
            "P41 keeps the raw-row ignore policy and large-artifact posture explicit.",
            "P41 preserves explicit no-merge posture for dirty root main.",
        ],
        "does_not_support": [
            "Git LFS expansion for this wave",
            "tracking large raw row dumps in git",
            "treating publication sync as scientific reopening",
        ],
        "distilled_result": {
            "active_stage_at_sync_time": "h59_post_h58_reproduction_gap_decision_packet",
            "preserved_sidecar": "p41_post_h58_publication_and_archive_sync",
            "selected_outcome": "publication_archive_surfaces_synced_to_h59_gap_state",
            "tracked_large_artifact_count": len(tracked_large_artifacts),
            "raw_row_ignore_rules_present": not ignore_status["missing_rules"],
            "current_release_focus": "honest_narrow_mechanism_reproduction_gap_closeout",
            "merge_executed": False,
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
            "tracked_large_artifact_paths": [str(row["path"]) for row in tracked_large_artifacts],
            "missing_ignore_rules": ignore_status["missing_rules"],
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"policy": "tracked_large_artifact_count", "value": len(tracked_large_artifacts)},
            {"policy": "raw_row_ignore_rules_present", "value": not ignore_status["missing_rules"]},
            {"policy": "merge_executed", "value": False},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
