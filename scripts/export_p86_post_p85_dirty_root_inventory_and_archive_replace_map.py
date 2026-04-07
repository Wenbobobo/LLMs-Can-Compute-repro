"""Export the post-P85 dirty-root inventory and archive-replace map packet for P86."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P86_post_p85_dirty_root_inventory_and_archive_replace_map"
P85_SUMMARY_PATH = ROOT / "results" / "P85_post_p84_main_rebaseline_and_control_resync" / "summary.json"
ROOT_QUARANTINE_PATH = Path("D:/zWenbo/AI/LLMCompute")
CURRENT_BRANCH = "wip/p85-post-p84-main-rebaseline"
ROOT_QUARANTINE_BRANCH = "wip/root-main-parking-2026-03-24"
DOC_REQUIREMENTS = {
    "README.md": [
        "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
        CURRENT_BRANCH,
        ROOT_QUARANTINE_BRANCH,
        "dirty-root inventory and archive-replace map",
    ],
    "STATUS.md": [
        "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
        ROOT_QUARANTINE_BRANCH,
        "quarantine-only",
        "docs consolidation",
    ],
    "docs/README.md": [
        "H65 + P86 + P85 + P84 + P83",
        "publication_record/current_stage_driver.md",
        "branch_worktree_registry.md",
        "plans/README.md",
    ],
    "docs/branch_worktree_registry.md": [
        CURRENT_BRANCH,
        ROOT_QUARANTINE_BRANCH,
        "archive-replace map",
        "salvage-only import",
    ],
    "docs/plans/README.md": [
        "2026-04-07-post-p86-next-planmode-handoff.md",
        "2026-04-07-post-p86-next-planmode-startup-prompt.md",
        "2026-04-07-post-p86-next-planmode-brief-prompt.md",
        "P86",
    ],
    "docs/milestones/README.md": [
        "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
        "P85_post_p84_main_rebaseline_and_control_resync",
        "P84_post_p83_keep_set_contraction_and_closeout",
    ],
    "docs/publication_record/README.md": [
        "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
        "current_stage_driver.md",
        "paper_bundle_status.md",
    ],
    "docs/publication_record/current_stage_driver.md": [
        "P86_post_p85_dirty_root_inventory_and_archive_replace_map",
        ROOT_QUARANTINE_BRANCH,
        "docs consolidation",
        "paper spine refresh",
    ],
    "docs/plans/2026-04-07-post-p86-next-planmode-handoff.md": [
        CURRENT_BRANCH,
        "docs consolidation",
        "paper spine refresh",
        "salvage-only import",
    ],
    "docs/plans/2026-04-07-post-p86-next-planmode-startup-prompt.md": [
        CURRENT_BRANCH,
        "docs consolidation",
        "paper spine refresh",
    ],
    "docs/plans/2026-04-07-post-p86-next-planmode-brief-prompt.md": [
        "p85-post-p84-main-rebaseline",
        "docs consolidation",
        "paper spine refresh",
    ],
}
DUPLICATE_OR_OBSOLETE_PATHS = {
    "README.md",
    "STATUS.md",
    "docs/README.md",
    "docs/branch_worktree_registry.md",
    "docs/plans/README.md",
    "docs/milestones/README.md",
    "scripts/export_p5_public_surface_sync.py",
    "tests/test_export_p5_public_surface_sync.py",
    "tests/test_export_release_preflight_checklist_audit.py",
    "tmp/active_wave_plan.md",
}
ARCHIVE_ONLY_PREFIXES = ("results/",)
SALVAGE_CANDIDATE_PREFIXES = (
    "docs/milestones/",
    "docs/plans/",
    "docs/publication_record/",
    "scripts/",
    "tests/",
)
HIGH_RISK_PATHS = {
    "README.md",
    "STATUS.md",
    "docs/README.md",
    "docs/branch_worktree_registry.md",
    "docs/publication_record/current_stage_driver.md",
    "docs/publication_record/claim_evidence_table.md",
    "docs/publication_record/paper_bundle_status.md",
    "docs/plans/README.md",
    "docs/milestones/README.md",
    "scripts/export_p5_public_surface_sync.py",
    "tests/test_export_release_preflight_checklist_audit.py",
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


def git_output(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd or ROOT),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def ahead_behind(left: str, right: str) -> dict[str, int]:
    left_only, right_only = git_output(["rev-list", "--left-right", "--count", f"{left}...{right}"]).split()
    return {"left_only": int(left_only), "right_only": int(right_only)}


def doc_sync_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative_path, needles in DOC_REQUIREMENTS.items():
        path = ROOT / relative_path
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "path": relative_path,
                "exists": exists,
                "needle_count": len(needles),
                "ok": exists and contains_all(text, needles),
            }
        )
    return rows


def parse_status_rows(raw: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in raw.splitlines():
        if line:
            rows.append({"status": line[:2], "path": line[3:]})
    return rows


def classify_path(path: str) -> str:
    if path in DUPLICATE_OR_OBSOLETE_PATHS:
        return "duplicate_or_obsolete"
    if path.startswith(ARCHIVE_ONLY_PREFIXES):
        return "archive_only"
    if path == "docs/claims_matrix.md":
        return "salvage_candidate"
    if path.startswith(SALVAGE_CANDIDATE_PREFIXES):
        return "salvage_candidate"
    return "duplicate_or_obsolete"


def risk_flag(path: str) -> bool:
    if path in HIGH_RISK_PATHS:
        return True
    return path.startswith("docs/publication_record/") or path.startswith("results/release_")


def summarize_inventory(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, int], list[str]]:
    inventory_rows: list[dict[str, object]] = []
    counts = {
        "duplicate_or_obsolete": 0,
        "salvage_candidate": 0,
        "archive_only": 0,
    }
    risky_paths: list[str] = []
    for row in rows:
        classification = classify_path(row["path"])
        counts[classification] += 1
        risky = risk_flag(row["path"])
        if risky:
            risky_paths.append(row["path"])
        inventory_rows.append(
            {
                "status": row["status"],
                "path": row["path"],
                "classification": classification,
                "merge_policy": "salvage_only_import" if classification == "salvage_candidate" else "do_not_merge_blindly",
                "risky": risky,
            }
        )
    return inventory_rows, counts, sorted(set(risky_paths))


def main() -> None:
    p85_summary = read_json(P85_SUMMARY_PATH)["summary"]
    if p85_summary["selected_outcome"] != "merged_main_rebaseline_and_control_resync_after_p84":
        raise RuntimeError("P86 expects the landed green P85 rebaseline summary.")
    if p85_summary["blocked_count"] != 0:
        raise RuntimeError("P86 expects a green P85 summary before root inventory.")

    current_branch_name = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    current_head = git_output(["rev-parse", "--short", "HEAD"])
    origin_main_head = git_output(["rev-parse", "--short", "origin/main"])
    branch_divergence = ahead_behind("origin/main", "HEAD")
    quarantine_branch_name = git_output(["rev-parse", "--abbrev-ref", "HEAD"], ROOT_QUARANTINE_PATH)
    dirty_status_rows = parse_status_rows(git_output(["status", "--porcelain=v1"], ROOT_QUARANTINE_PATH))
    inventory_rows, classification_counts, risky_paths = summarize_inventory(dirty_status_rows)
    tracked_count = sum(row["status"] != "??" for row in dirty_status_rows)
    untracked_count = sum(row["status"] == "??" for row in dirty_status_rows)
    doc_rows = doc_sync_rows()

    checklist_rows = [
        {
            "item_id": "p86_reads_green_p85_summary",
            "status": "pass",
            "notes": "P86 begins only after the landed green P85 merged-main rebaseline.",
        },
        {
            "item_id": "p86_runs_on_clean_p85_branch",
            "status": "pass" if current_branch_name == CURRENT_BRANCH else "blocked",
            "notes": "The dirty-root inventory packet must run from the dedicated clean p85 branch.",
        },
        {
            "item_id": "p86_quarantine_root_stays_parked",
            "status": "pass" if quarantine_branch_name == ROOT_QUARANTINE_BRANCH else "blocked",
            "notes": "Dirty root remains quarantine-only and is inspected read-only.",
        },
        {
            "item_id": "p86_dirty_root_inventory_is_nonempty",
            "status": "pass" if tracked_count > 0 and untracked_count > 0 else "blocked",
            "notes": "Archive/replace mapping should capture both tracked and untracked root dirt.",
        },
        {
            "item_id": "p86_live_docs_shift_current_control_to_inventory_wave",
            "status": "pass" if all(bool(row["ok"]) for row in doc_rows) else "blocked",
            "notes": "Live control docs should make P86 current while keeping dirty root quarantine-only.",
        },
    ]

    claim_packet = {
        "supports": [
            "P86 records the dirty root as a quarantine-only archive/replace target rather than an integration base.",
            "P86 classifies dirty-root paths into duplicate_or_obsolete, salvage_candidate, and archive_only buckets.",
            "P86 moves the next route from root inventory toward docs consolidation, selective salvage import, and paper spine refresh.",
        ],
        "does_not_support": [
            "dirty-root integration",
            "runtime reopen",
            "same-lane executor-value reopen",
            "broad Wasm or arbitrary C scope expansion",
        ],
        "distilled_result": {
            "current_inventory_wave": "p86_post_p85_dirty_root_inventory_and_archive_replace_map",
            "current_branch": CURRENT_BRANCH,
            "current_branch_head": current_head,
            "merged_main_head": origin_main_head,
            "quarantine_root_branch": ROOT_QUARANTINE_BRANCH,
            "origin_main_to_p86_left_right": f"{branch_divergence['left_only']}/{branch_divergence['right_only']}",
            "selected_outcome": "dirty_root_inventory_and_archive_replace_map_after_p85",
            "next_recommended_route": "docs_consolidation_selective_salvage_import_and_paper_spine_refresh",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "tracked_dirty_count": tracked_count,
            "untracked_dirty_count": untracked_count,
            "duplicate_or_obsolete_count": classification_counts["duplicate_or_obsolete"],
            "salvage_candidate_count": classification_counts["salvage_candidate"],
            "archive_only_count": classification_counts["archive_only"],
            "high_risk_path_count": len(risky_paths),
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"field": "dirty_status_rows", "value": dirty_status_rows},
            {"field": "inventory_rows", "value": inventory_rows},
            {"field": "classification_counts", "value": classification_counts},
            {"field": "risky_paths", "value": risky_paths},
            {"field": "doc_sync_rows", "value": doc_rows},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
