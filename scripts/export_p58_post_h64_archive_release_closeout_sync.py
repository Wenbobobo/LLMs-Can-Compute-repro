"""Export the post-H64 archive/release closeout sync sidecar for P58."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P58_post_h64_archive_release_closeout_sync"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P56_SUMMARY_PATH = ROOT / "results" / "P56_post_h64_clean_merge_candidate_packet" / "summary.json"
P57_SUMMARY_PATH = ROOT / "results" / "P57_post_h64_paper_submission_package_sync" / "summary.json"


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
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P58 expects the landed H64 freeze packet.")
    if p56_summary["selected_outcome"] != "clean_descendant_merge_candidate_staged_without_merge_execution":
        raise RuntimeError("P58 expects the landed P56 merge-candidate packet.")
    if p57_summary["selected_outcome"] != "paper_submission_package_surfaces_synced_to_h64_followthrough_stack":
        raise RuntimeError("P58 expects the landed P57 package sync.")

    archival_manifest_text = read_text(ROOT / "docs" / "publication_record" / "archival_repro_manifest.md")
    release_preflight_text = read_text(ROOT / "docs" / "publication_record" / "release_preflight_checklist.md")
    release_candidate_text = read_text(ROOT / "docs" / "publication_record" / "release_candidate_checklist.md")
    external_release_note_text = read_text(ROOT / "docs" / "publication_record" / "external_release_note_skeleton.md")
    review_boundary_text = read_text(ROOT / "docs" / "publication_record" / "review_boundary_summary.md")

    release_preflight_matches_old_stack = contains_all(
        release_preflight_text,
        [
            "current `H64/P56/P57/P58/P59/F38` stack",
            "`H58` as the value-negative closeout",
            "`H43` as the preserved paper-grade endpoint",
            "No public release surface routes through dirty root `main`.",
        ],
    )
    release_preflight_matches_extended_stack = contains_all(
        release_preflight_text,
        [
            "`P60/P61/P62` published clean-descendant stack",
            "`P56/P57/P58/P59/F38` foundation",
            "`H58` as the value-negative closeout",
            "`H43` as the preserved paper-grade endpoint",
            "No public release surface routes through dirty root `main`.",
        ],
    )
    release_candidate_matches_old_stack = contains_all(
        release_candidate_text,
        [
            "`H64/P56/P57/P58/P59/F38`",
            "preserved `H58/H43`",
            "No outward wording implies a new runtime lane",
        ],
    )
    release_candidate_matches_extended_stack = contains_all(
        release_candidate_text,
        [
            "`H64/P56/P57/P58/P59/P60/P61/P62/F38`",
            "preserved `H58/H43`",
            "No outward wording implies a new runtime lane",
        ],
    )

    checklist_rows = [
        {
            "item_id": "p58_reads_h64_p56_p57",
            "status": "pass",
            "notes": "P58 starts only after H64, P56, and P57 stay green.",
        },
        {
            "item_id": "p58_archive_and_release_ledgers_expose_current_followthrough_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        archival_manifest_text,
                        [
                            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                            "results/P56_post_h64_clean_merge_candidate_packet/summary.json",
                            "results/P57_post_h64_paper_submission_package_sync/summary.json",
                            "results/P58_post_h64_archive_release_closeout_sync/summary.json",
                            "results/P59_post_h64_control_and_handoff_sync/summary.json",
                            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                        ],
                    ),
                    release_preflight_matches_old_stack or release_preflight_matches_extended_stack,
                    release_candidate_matches_old_stack or release_candidate_matches_extended_stack,
                )
            )
            else "blocked",
            "notes": "Archive and release ledgers should expose the same H64 follow-through stack or its later published clean-descendant extension.",
        },
        {
            "item_id": "p58_release_note_and_review_boundary_stay_restrained",
            "status": "pass"
            if all(
                (
                    contains_all(
                        external_release_note_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56/P57/P58/P59`",
                            "`H43_post_r44_useful_case_refreeze`",
                            "`H58_post_r62_origin_value_boundary_closeout_packet`",
                            "dormant non-runtime `F38` dossier",
                        ],
                    ),
                    contains_all(
                        review_boundary_text,
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`P56/P57/P58/P59`",
                            "narrow positive mechanism support survives",
                            "the only remaining future route is a dormant no-go dossier at `F38`",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Archive/release helper wording must remain downstream of archive-first partial falsification.",
        },
    ]
    claim_packet = {
        "supports": [
            "P58 synchronizes archive-facing and release-facing docs to the current H64 follow-through stack.",
            "P58 preserves H63, H58, H43, and F38 as explicit anchors beneath the current operational sidecars.",
            "P58 keeps outward wording restrained and downstream of archive-first partial falsification.",
        ],
        "does_not_support": [
            "runtime reopen",
            "dirty-root main merge",
            "broad public claim widening",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_archive_release_sync_wave": "p58_post_h64_archive_release_closeout_sync",
            "current_clean_merge_candidate_packet": "p56_post_h64_clean_merge_candidate_packet",
            "current_paper_submission_sync_wave": "p57_post_h64_paper_submission_package_sync",
            "current_control_sync_wave": "p59_post_h64_control_and_handoff_sync",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "selected_outcome": "archive_release_closeout_surfaces_synced_to_h64_followthrough_stack",
            "next_required_lane": "p59_control_and_handoff_sync",
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
            {"field": "current_archive_release_sync_wave", "value": "p58_post_h64_archive_release_closeout_sync"},
            {"field": "current_clean_merge_candidate_packet", "value": "p56_post_h64_clean_merge_candidate_packet"},
            {"field": "current_paper_submission_sync_wave", "value": "p57_post_h64_paper_submission_package_sync"},
            {"field": "current_control_sync_wave", "value": "p59_post_h64_control_and_handoff_sync"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
