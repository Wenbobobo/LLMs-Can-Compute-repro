"""Export the post-H63 clean-descendant promotion-prep sidecar for P55."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P55_post_h63_clean_descendant_promotion_prep"
H63_SUMMARY_PATH = ROOT / "results" / "H63_post_p50_p51_p52_f38_archive_first_closeout_packet" / "summary.json"
P53_SUMMARY_PATH = ROOT / "results" / "P53_post_h63_paper_archive_claim_sync" / "summary.json"
P54_SUMMARY_PATH = ROOT / "results" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ACTIVE_WAVE_PLAN_PATH = ROOT / "tmp" / "active_wave_plan.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-03-26-post-h64-next-planmode-handoff.md"
STARTUP_PROMPT_PATH = ROOT / "docs" / "plans" / "2026-03-26-post-h64-next-planmode-startup-prompt.md"


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


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"]).strip()


def tracked_upstream(branch: str) -> str:
    return git_output(["for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch}"]).strip()


def text_contains(path: Path, patterns: list[str]) -> bool:
    text = path.read_text(encoding="utf-8")
    return all(pattern in text for pattern in patterns)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def main() -> None:
    h63_summary = read_json(H63_SUMMARY_PATH)["summary"]
    p53_summary = read_json(P53_SUMMARY_PATH)["summary"]
    p54_summary = read_json(P54_SUMMARY_PATH)["summary"]
    if h63_summary["selected_outcome"] != "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant":
        raise RuntimeError("P55 expects the landed H63 closeout packet.")
    if p53_summary["selected_outcome"] != "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze":
        raise RuntimeError("P55 expects the landed P53 claim-sync wave.")
    if p54_summary["selected_outcome"] != "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution":
        raise RuntimeError("P55 expects the landed P54 hygiene wave.")

    current_branch_name = current_branch()
    current_upstream = tracked_upstream(current_branch_name)
    checklist_rows = [
        {
            "item_id": "p55_reads_h63",
            "status": "pass",
            "notes": "P55 starts from the landed H63 closeout packet.",
        },
        {
            "item_id": "p55_reads_p53",
            "status": "pass",
            "notes": "P55 depends on the landed P53 claim-sync wave.",
        },
        {
            "item_id": "p55_reads_p54",
            "status": "pass",
            "notes": "P55 depends on the landed P54 hygiene wave.",
        },
        {
            "item_id": "p55_current_stage_driver_mentions_h64_stack",
            "status": "pass"
            if text_contains(
                CURRENT_STAGE_DRIVER_PATH,
                [
                    "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                    "P55_post_h63_clean_descendant_promotion_prep",
                    "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
                ],
            )
            else "blocked",
            "notes": "The current stage driver should expose the H64 stack directly.",
        },
        {
            "item_id": "p55_active_wave_plan_mentions_h64_stack",
            "status": "pass"
            if text_contains(
                ACTIVE_WAVE_PLAN_PATH,
                [
                    "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                    "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant",
                ],
            )
            else "blocked",
            "notes": "The active-wave plan should expose the H64 stack directly.",
        },
        {
            "item_id": "p55_publication_readme_mentions_h64_stack",
            "status": "pass"
            if text_contains(
                PUBLICATION_README_PATH,
                [
                    "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                    "P53_post_h63_paper_archive_claim_sync",
                    "P55_post_h63_clean_descendant_promotion_prep",
                ],
            )
            else "blocked",
            "notes": "The publication README should expose the H64 stack directly.",
        },
        {
            "item_id": "p55_handoff_doc_is_current",
            "status": "pass"
            if text_contains(HANDOFF_PATH, ["H64_post_p53_p54_p55_f38_archive_first_freeze_packet", current_branch_name])
            else "blocked",
            "notes": "The next handoff should start from H64 and the current clean descendant branch.",
        },
        {
            "item_id": "p55_startup_prompt_is_current",
            "status": "pass"
            if text_contains(
                STARTUP_PROMPT_PATH,
                [
                    "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                    "P55_post_h63_clean_descendant_promotion_prep",
                    "archive_or_hygiene_stop",
                ],
            )
            else "blocked",
            "notes": "The next startup prompt should expose the H64 stack directly.",
        },
    ]
    claim_packet = {
        "supports": [
            "P55 locks promotion-prep to the H64 stack without claiming merge execution.",
            "P55 makes the next handoff and startup prompt start from H64 rather than preserved H63.",
            "P55 preserves descendant-only merge posture and keeps R63 planning-only.",
        ],
        "does_not_support": [
            "merge execution",
            "dirty-root integration",
            "runtime reopening",
        ],
        "distilled_result": {
            "active_stage_at_promotion_time": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "current_promotion_prep_wave": "p55_post_h63_clean_descendant_promotion_prep",
            "preserved_prior_promotion_prep_wave": "p48_post_h61_clean_descendant_promotion_prep",
            "current_planning_branch": current_branch_name,
            "current_planning_branch_upstream": current_upstream,
            "publication_handoff_present": True,
            "merge_execution_state": False,
            "selected_outcome": "clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze",
            "next_required_lane": "h64_docs_only_freeze_packet",
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
            {"field": "current_planning_branch", "value": current_branch_name},
            {"field": "current_planning_branch_upstream", "value": current_upstream},
            {"field": "handoff_path", "value": display_path(HANDOFF_PATH)},
            {"field": "startup_prompt_path", "value": display_path(STARTUP_PROMPT_PATH)},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
