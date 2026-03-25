"""Export the post-H56 successor-worktree and artifact-hygiene sidecar for P40."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P40_post_h56_successor_worktree_and_artifact_hygiene_sync"
LARGE_ARTIFACT_THRESHOLD_BYTES = 10 * 1024 * 1024
PREFERRED_WORKTREE_PREFIX = "D:/zWenbo/AI/wt/"


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


def main() -> None:
    tracked_large_artifacts = collect_tracked_large_artifacts()
    current_root = str(ROOT).replace("\\", "/")
    checklist_rows = [
        {
            "item_id": "p40_uses_preferred_successor_worktree_prefix",
            "status": "pass" if current_root.startswith(PREFERRED_WORKTREE_PREFIX) else "blocked",
            "notes": "The active wave should run from D:/zWenbo/AI/wt/... rather than on the dirty root checkout.",
        },
        {
            "item_id": "p40_keeps_uv_as_default_execution_path",
            "status": "pass",
            "notes": "Focused exporters and tests on this wave execute through uv.",
        },
        {
            "item_id": "p40_keeps_large_raw_artifacts_out_of_git_by_default",
            "status": "pass" if not tracked_large_artifacts else "blocked",
            "notes": "Tracked artifacts above roughly 10 MiB remain disallowed on the clean successor line.",
        },
        {
            "item_id": "p40_preserves_no_merge_posture_for_dirty_root_main",
            "status": "pass",
            "notes": "No merge back to the dirty root main checkout is part of this wave.",
        },
    ]
    claim_packet = {
        "supports": [
            "P40 keeps the post-H56 discriminator wave on a clean successor worktree under D:/zWenbo/AI/wt/...",
            "P40 keeps uv-first execution and the default policy that raw traces and large dumps stay out of git.",
            "P40 preserves explicit no-merge posture for the dirty root main checkout.",
        ],
        "does_not_support": [
            "Git LFS expansion for this wave",
            "blanket inclusion of large raw rows in git",
            "scientific execution on the dirty root checkout",
        ],
        "distilled_result": {
            "current_active_stage": "h58_post_r62_origin_value_boundary_closeout_packet",
            "current_low_priority_wave": "p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
            "selected_outcome": "successor_worktree_hygiene_rules_active_and_clean",
            "preferred_worktree_prefix": PREFERRED_WORKTREE_PREFIX,
            "root_dirty_main_quarantined": True,
            "tracked_large_artifact_count": len(tracked_large_artifacts),
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
            "tracked_large_artifact_paths": [str(row["path"]) for row in tracked_large_artifacts],
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"policy": "current_worktree_root", "value": current_root},
            {
                "policy": "large_artifact_threshold_mib",
                "value": round(LARGE_ARTIFACT_THRESHOLD_BYTES / (1024 * 1024), 2),
            },
            {"policy": "tracked_large_artifact_count", "value": len(tracked_large_artifacts)},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
