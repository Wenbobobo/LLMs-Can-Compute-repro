"""Export the post-H64 paper/submission package sync sidecar for P57."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P57_post_h64_paper_submission_package_sync"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P56_SUMMARY_PATH = ROOT / "results" / "P56_post_h64_clean_merge_candidate_packet" / "summary.json"


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
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P57 expects the landed H64 freeze packet.")
    if p56_summary["selected_outcome"] != "clean_descendant_merge_candidate_staged_without_merge_execution":
        raise RuntimeError("P57 expects the landed P56 merge-candidate packet.")

    readme_text = read_text(ROOT / "README.md")
    status_text = read_text(ROOT / "STATUS.md")
    publication_readme_text = read_text(ROOT / "docs" / "publication_record" / "README.md")
    submission_index_text = read_text(ROOT / "docs" / "publication_record" / "submission_packet_index.md")
    submission_criteria_text = read_text(ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md")
    claim_ladder_text = read_text(ROOT / "docs" / "publication_record" / "claim_ladder.md")
    paper_bundle_status_text = read_text(ROOT / "docs" / "publication_record" / "paper_bundle_status.md")
    review_boundary_text = read_text(ROOT / "docs" / "publication_record" / "review_boundary_summary.md")
    release_summary_text = read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md")

    checklist_rows = [
        {
            "item_id": "p57_reads_h64_and_p56",
            "status": "pass",
            "notes": "P57 starts only after H64 and P56 land cleanly.",
        },
        {
            "item_id": "p57_root_and_publication_surfaces_expose_current_followthrough_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        readme_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56_post_h64_clean_merge_candidate_packet`",
                            "`P57_post_h64_paper_submission_package_sync`",
                            "`P58_post_h64_archive_release_closeout_sync`",
                            "`P59_post_h64_control_and_handoff_sync`",
                        ],
                    ),
                    contains_all(
                        status_text,
                        [
                            "`P56_post_h64_clean_merge_candidate_packet`",
                            "`P57_post_h64_paper_submission_package_sync`",
                            "`P58_post_h64_archive_release_closeout_sync`",
                            "`P59_post_h64_control_and_handoff_sync`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        publication_readme_text,
                        [
                            "P56_post_h64_clean_merge_candidate_packet",
                            "P57_post_h64_paper_submission_package_sync",
                            "P58_post_h64_archive_release_closeout_sync",
                            "P59_post_h64_control_and_handoff_sync",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Top-level and publication surfaces should expose the current H64 follow-through stack.",
        },
        {
            "item_id": "p57_submission_and_paper_ledgers_stay_downstream_of_h64_h58_h43_f38_split",
            "status": "pass"
            if all(
                (
                    contains_all(
                        submission_index_text,
                        [
                            "P56_post_h64_clean_merge_candidate_packet",
                            "P57_post_h64_paper_submission_package_sync",
                            "P58_post_h64_archive_release_closeout_sync",
                            "P59_post_h64_control_and_handoff_sync",
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                        ],
                    ),
                    contains_all(
                        submission_criteria_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56_post_h64_clean_merge_candidate_packet`",
                            "`P57_post_h64_paper_submission_package_sync`",
                            "`P58_post_h64_archive_release_closeout_sync`",
                            "`P59_post_h64_control_and_handoff_sync`",
                            "`H58_post_r62_origin_value_boundary_closeout_packet`",
                            "`H43_post_r44_useful_case_refreeze`",
                        ],
                    ),
                    contains_all(
                        claim_ladder_text,
                        [
                            "| P56 Clean merge-candidate packet |",
                            "| P57 Paper/submission package sync |",
                            "| P58 Archive/release closeout sync |",
                            "| P59 Control and handoff sync |",
                        ],
                    ),
                    contains_all(
                        paper_bundle_status_text,
                        [
                            "`P56_post_h64_clean_merge_candidate_packet`",
                            "`P57_post_h64_paper_submission_package_sync`",
                            "`P58_post_h64_archive_release_closeout_sync`",
                            "`P59_post_h64_control_and_handoff_sync`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                        ],
                    ),
                    contains_all(
                        review_boundary_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56/P57/P58/P59`",
                            "narrow positive mechanism support survives",
                            "executor-value on the strongest justified lane is closed negative",
                        ],
                    ),
                    contains_all(
                        release_summary_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56/P57/P58/P59`",
                            "archive-first partial falsification",
                            "R63 remains dormant, non-runtime",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Submission and paper-facing ledgers must stay downstream of archive-first partial falsification.",
        },
    ]
    claim_packet = {
        "supports": [
            "P57 synchronizes paper-facing and submission-facing docs to the current H64 follow-through stack.",
            "P57 keeps H58 and H43 preserved rather than current.",
            "P57 keeps F38 dormant and non-runtime only.",
        ],
        "does_not_support": [
            "runtime reopen",
            "broad claim widening",
            "dirty-root main merge",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_paper_submission_sync_wave": "p57_post_h64_paper_submission_package_sync",
            "current_clean_merge_candidate_packet": "p56_post_h64_clean_merge_candidate_packet",
            "current_archive_release_sync_wave": "p58_post_h64_archive_release_closeout_sync",
            "current_control_sync_wave": "p59_post_h64_control_and_handoff_sync",
            "preserved_prior_active_packet": "h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "preserved_executor_value_closeout": "h58_post_r62_origin_value_boundary_closeout_packet",
            "preserved_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "selected_outcome": "paper_submission_package_surfaces_synced_to_h64_followthrough_stack",
            "next_required_lane": "p58_archive_release_sync_and_p59_control_sync",
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
            {"field": "preserved_executor_value_closeout", "value": "h58_post_r62_origin_value_boundary_closeout_packet"},
            {"field": "preserved_paper_grade_endpoint", "value": "h43_post_r44_useful_case_refreeze"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
