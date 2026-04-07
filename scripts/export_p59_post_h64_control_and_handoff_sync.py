"""Export the post-H64 control and handoff sync sidecar for P59."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P59_post_h64_control_and_handoff_sync"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P56_SUMMARY_PATH = ROOT / "results" / "P56_post_h64_clean_merge_candidate_packet" / "summary.json"
P57_SUMMARY_PATH = ROOT / "results" / "P57_post_h64_paper_submission_package_sync" / "summary.json"
P58_SUMMARY_PATH = ROOT / "results" / "P58_post_h64_archive_release_closeout_sync" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
MILESTONES_README_PATH = ROOT / "docs" / "milestones" / "README.md"
ACTIVE_WAVE_PATH = ROOT / "tmp" / "active_wave_plan.md"
HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-03-31-post-p59-next-planmode-handoff.md"
STARTUP_PROMPT_PATH = ROOT / "docs" / "plans" / "2026-03-31-post-p59-next-planmode-startup-prompt.md"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    h64_summary = read_json(H64_SUMMARY_PATH)["summary"]
    p56_summary = read_json(P56_SUMMARY_PATH)["summary"]
    p57_summary = read_json(P57_SUMMARY_PATH)["summary"]
    p58_summary = read_json(P58_SUMMARY_PATH)["summary"]
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P59 expects the landed H64 freeze packet.")
    if p56_summary["selected_outcome"] != "clean_descendant_merge_candidate_staged_without_merge_execution":
        raise RuntimeError("P59 expects the landed P56 merge-candidate packet.")
    if p57_summary["selected_outcome"] != "paper_submission_package_surfaces_synced_to_h64_followthrough_stack":
        raise RuntimeError("P59 expects the landed P57 package sync.")
    if p58_summary["selected_outcome"] != "archive_release_closeout_surfaces_synced_to_h64_followthrough_stack":
        raise RuntimeError("P59 expects the landed P58 release sync.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    milestones_readme_text = read_text(MILESTONES_README_PATH)
    active_wave_text = read_text(ACTIVE_WAVE_PATH)
    handoff_text = read_text(HANDOFF_PATH)
    startup_prompt_text = read_text(STARTUP_PROMPT_PATH)

    plans_readme_matches_original_state = contains_all(
        plans_readme_text,
        [
            "2026-03-31-post-h64-clean-merge-candidate-design.md",
            "2026-03-31-post-p59-next-planmode-handoff.md",
            "2026-03-31-post-p59-next-planmode-startup-prompt.md",
            "P56_post_h64_clean_merge_candidate_packet",
            "P57_post_h64_paper_submission_package_sync",
            "P58_post_h64_archive_release_closeout_sync",
            "P59_post_h64_control_and_handoff_sync",
        ],
    )
    plans_readme_matches_extended_state = contains_all(
        plans_readme_text,
        [
            "2026-03-31-post-p59-published-clean-descendant-merge-prep-design.md",
            "2026-03-31-post-p62-next-planmode-handoff.md",
            "2026-03-31-post-p62-next-planmode-startup-prompt.md",
            "P60_post_p59_published_clean_descendant_promotion_prep",
            "P61_post_p60_release_hygiene_rebaseline",
            "P62_post_p61_merge_prep_control_sync",
        ],
    )

    checklist_rows = [
        {
            "item_id": "p59_reads_h64_p56_p57_p58",
            "status": "pass",
            "notes": "P59 starts only after H64 and the P56/P57/P58 sidecars land.",
        },
        {
            "item_id": "p59_control_surfaces_expose_current_followthrough_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56_post_h64_clean_merge_candidate_packet`",
                            "`P57_post_h64_paper_submission_package_sync`",
                            "`P58_post_h64_archive_release_closeout_sync`",
                            "`P59_post_h64_control_and_handoff_sync`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    plans_readme_matches_original_state or plans_readme_matches_extended_state,
                    contains_all(
                        milestones_readme_text,
                        [
                            "P59_post_h64_control_and_handoff_sync/",
                            "P58_post_h64_archive_release_closeout_sync/",
                            "P57_post_h64_paper_submission_package_sync/",
                            "P56_post_h64_clean_merge_candidate_packet/",
                        ],
                    ),
                    contains_all(
                        active_wave_text,
                        [
                            "`P56_post_h64_clean_merge_candidate_packet`",
                            "`P57_post_h64_paper_submission_package_sync`",
                            "`P58_post_h64_archive_release_closeout_sync`",
                            "`P59_post_h64_control_and_handoff_sync`",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Control surfaces must expose the same H64 follow-through stack or a later published clean-descendant extension that preserves it.",
        },
        {
            "item_id": "p59_handoff_and_startup_prompt_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(
                        handoff_text,
                        [
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "P56_post_h64_clean_merge_candidate_packet",
                            "P57_post_h64_paper_submission_package_sync",
                            "P58_post_h64_archive_release_closeout_sync",
                            "P59_post_h64_control_and_handoff_sync",
                            "wip/p56-post-h64-clean-merge-candidate",
                            "D:/zWenbo/AI/wt/p56-post-h64-clean-merge-candidate",
                        ],
                    ),
                    contains_all(
                        startup_prompt_text,
                        [
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "P56_post_h64_clean_merge_candidate_packet",
                            "P57_post_h64_paper_submission_package_sync",
                            "P58_post_h64_archive_release_closeout_sync",
                            "P59_post_h64_control_and_handoff_sync",
                            "archive_or_hygiene_stop",
                            "Do not reopen same-lane executor-value work",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Next-entrypoint docs must start from the landed H64 follow-through state.",
        },
    ]
    claim_packet = {
        "supports": [
            "P59 synchronizes the current stage driver, indexes, active-wave file, and next handoff surfaces.",
            "P59 keeps H64 as the active docs-only packet and P56/P57/P58/P59 as operational follow-through sidecars.",
            "P59 keeps the default downstream lane at archive_or_hygiene_stop.",
        ],
        "does_not_support": [
            "runtime reopen",
            "merge execution",
            "dirty-root integration",
            "minting a new H65 packet",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_clean_merge_candidate_packet": "p56_post_h64_clean_merge_candidate_packet",
            "current_paper_submission_sync_wave": "p57_post_h64_paper_submission_package_sync",
            "current_archive_release_sync_wave": "p58_post_h64_archive_release_closeout_sync",
            "current_control_sync_wave": "p59_post_h64_control_and_handoff_sync",
            "preserved_prior_active_packet": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "default_downstream_lane": "archive_or_hygiene_stop",
            "selected_outcome": "control_and_handoff_surfaces_synced_to_h64_followthrough_stack",
            "next_required_lane": "later_clean_descendant_review_or_merge_prep_decision",
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
            {"field": "current_clean_merge_candidate_packet", "value": "p56_post_h64_clean_merge_candidate_packet"},
            {"field": "current_paper_submission_sync_wave", "value": "p57_post_h64_paper_submission_package_sync"},
            {"field": "current_archive_release_sync_wave", "value": "p58_post_h64_archive_release_closeout_sync"},
            {"field": "current_control_sync_wave", "value": "p59_post_h64_control_and_handoff_sync"},
            {"field": "default_downstream_lane", "value": "archive_or_hygiene_stop"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
