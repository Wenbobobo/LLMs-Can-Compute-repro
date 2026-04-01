"""Export the post-P69 archive-index and artifact-policy sync sidecar for P70."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P70_post_p69_archive_index_and_artifact_policy_sync"
P69_SUMMARY_PATH = ROOT / "results" / "P69_post_h65_repo_graph_hygiene_inventory" / "summary.json"
PREFLIGHT_SUMMARY_PATH = ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
P10_SUMMARY_PATH = ROOT / "results" / "P10_submission_archive_ready" / "summary.json"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
SUBMISSION_PACKET_INDEX_PATH = ROOT / "docs" / "publication_record" / "submission_packet_index.md"
ARCHIVAL_MANIFEST_PATH = ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"
ARTIFACT_POLICY_PATH = ROOT / "docs" / "milestones" / "P70_post_p69_archive_index_and_artifact_policy_sync" / "artifact_policy.md"
CURRENT_HYGIENE_BRANCH = "wip/p69-post-h65-hygiene-only-cleanup"
RAW_ROW_PATTERNS = [
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


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


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


def main() -> None:
    p69_summary = read_json(P69_SUMMARY_PATH)["summary"]
    preflight_summary = read_json(PREFLIGHT_SUMMARY_PATH)["summary"]
    p10_summary = read_json(P10_SUMMARY_PATH)["summary"]
    if p69_summary["selected_outcome"] != "repo_graph_hygiene_inventory_confirms_clean_descendant_keep_set_and_root_quarantine":
        raise RuntimeError("P70 expects the landed P69 hygiene inventory.")
    if preflight_summary["preflight_state"] != "docs_and_audits_green":
        raise RuntimeError("P70 expects standing release preflight to remain green.")
    if p10_summary["packet_state"] != "archive_ready":
        raise RuntimeError("P70 expects standing P10 archive readiness to remain green.")

    plans_readme_text = read_text(PLANS_README_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)
    submission_packet_index_text = read_text(SUBMISSION_PACKET_INDEX_PATH)
    archival_manifest_text = read_text(ARCHIVAL_MANIFEST_PATH)
    artifact_policy_text = read_text(ARTIFACT_POLICY_PATH)
    current_branch_name = current_branch()
    tracked_oversize = tracked_large_files()

    checklist_rows = [
        {"item_id": "p70_reads_p69", "status": "pass", "notes": "P70 runs only after P69 lands the repo-graph hygiene inventory."},
        {"item_id": "p70_reads_standing_release_audits", "status": "pass", "notes": "P70 preserves the current green preflight and archive-ready posture."},
        {
            "item_id": "p70_runs_on_current_hygiene_branch",
            "status": "pass" if current_branch_name == CURRENT_HYGIENE_BRANCH else "blocked",
            "notes": "P70 should run only from the current hygiene-only cleanup branch.",
        },
        {
            "item_id": "p70_plans_index_mentions_current_design_and_post_p71_handoff",
            "status": "pass"
            if contains_all(
                plans_readme_text,
                [
                    "2026-04-01-post-h65-hygiene-only-cleanup-design.md",
                    "2026-04-01-post-p71-next-planmode-handoff.md",
                    "2026-04-01-post-p71-next-planmode-startup-prompt.md",
                    "2026-04-01-post-p71-next-planmode-brief-prompt.md",
                ],
            )
            else "blocked",
            "notes": "The planning index should expose the current hygiene-only cleanup design and next handoff surfaces.",
        },
        {
            "item_id": "p70_publication_readme_mentions_hygiene_cleanup_stack",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "P69_post_h65_repo_graph_hygiene_inventory",
                    "P70_post_p69_archive_index_and_artifact_policy_sync",
                    "current hygiene-only cleanup stack",
                    "artifact policy",
                ],
            )
            else "blocked",
            "notes": "The publication router should surface the current hygiene-only cleanup stack explicitly.",
        },
        {
            "item_id": "p70_submission_packet_index_mentions_current_cleanup_stack",
            "status": "pass"
            if contains_all(
                submission_packet_index_text,
                [
                    "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                    "P70_post_p69_archive_index_and_artifact_policy_sync",
                    "P69_post_h65_repo_graph_hygiene_inventory",
                    "P68_post_p67_release_hygiene_and_control_rebaseline",
                    "P67_post_p66_published_successor_freeze",
                    "P66_post_p65_successor_publication_review",
                ],
            )
            else "blocked",
            "notes": "The submission packet index should expose the current archive-facing cleanup helpers alongside H65.",
        },
        {
            "item_id": "p70_archival_manifest_mentions_current_cleanup_results",
            "status": "pass"
            if contains_all(
                archival_manifest_text,
                [
                    "results/P70_post_p69_archive_index_and_artifact_policy_sync/summary.json",
                    "results/P69_post_h65_repo_graph_hygiene_inventory/summary.json",
                    "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
                    "results/P68_post_p67_release_hygiene_and_control_rebaseline/summary.json",
                    "results/P67_post_p66_published_successor_freeze/summary.json",
                    "results/P66_post_p65_successor_publication_review/summary.json",
                    "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                    "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                    "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
                    "results/H43_post_r44_useful_case_refreeze/summary.json",
                ],
            )
            else "blocked",
            "notes": "The archival manifest should record the current cleanup sidecars without changing the paper-facing endpoint facts.",
        },
        {
            "item_id": "p70_artifact_policy_doc_is_current",
            "status": "pass"
            if contains_all(
                artifact_policy_text,
                [
                    "probe_read_rows.json",
                    "per_read_rows.json",
                    "trace_rows.json",
                    "step_rows.json",
                    "10 MiB",
                    "surface_report.json",
                    "Git LFS remains inactive by default",
                    "review-critical packet",
                    "runtime reopening",
                    "dirty-root integration",
                ],
            )
            else "blocked",
            "notes": "The artifact policy doc should keep the standing local-only / explicit-LFS-only rule explicit.",
        },
        {"item_id": "p70_raw_row_ignore_rules_stay_active", "status": "pass" if raw_row_ignore_rules_active() else "blocked", "notes": "The raw-row ignore rules should remain active in .gitignore."},
        {"item_id": "p70_no_tracked_oversize_artifacts", "status": "pass" if not tracked_oversize else "blocked", "notes": "The current clean descendant should not track artifacts at or above roughly 10 MiB."},
    ]

    claim_packet = {
        "supports": [
            "P70 syncs archive/publication/planning indexes to the current H65 hygiene-only cleanup view.",
            "P70 keeps the standing large-artifact rule explicit without enabling default LFS.",
            "P70 preserves green release-preflight and archive-ready audits while staying non-runtime.",
        ],
        "does_not_support": ["runtime reopening", "default LFS expansion", "dirty-root integration"],
        "distilled_result": {
            "active_stage_at_archive_sync_time": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "current_archive_index_sidecar": "p70_post_p69_archive_index_and_artifact_policy_sync",
            "preserved_prior_repo_hygiene_sidecar": "p69_post_h65_repo_graph_hygiene_inventory",
            "current_planning_branch": current_branch_name,
            "preflight_state": preflight_summary["preflight_state"],
            "packet_state": p10_summary["packet_state"],
            "tracked_oversize_count": len(tracked_oversize),
            "raw_row_ignore_rules_active": raw_row_ignore_rules_active(),
            "selected_outcome": "archive_indexes_and_artifact_policy_synced_to_h65_hygiene_cleanup_stack",
            "next_required_lane": "p71_clean_descendant_merge_prep_readiness_sync",
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
            {"field": "current_planning_branch", "value": current_branch_name},
            {"field": "tracked_oversize_artifacts", "value": tracked_oversize},
            {"field": "raw_row_ignore_rules_active", "value": raw_row_ignore_rules_active()},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
