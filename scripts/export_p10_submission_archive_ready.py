"""Export the P10 submission/archive readiness audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P10_submission_archive_ready"

CURRENT_PAPER_PHASE = "h64_archive_first_freeze_with_preserved_h63_h58_h43_endpoints"
GREEN_ACTION = (
    "use submission_packet_index.md plus archival_repro_manifest.md as the canonical handoff while H64 remains "
    "the current active docs-only packet, H63 remains the preserved prior active packet, P53 remains the current "
    "paper/archive claim-sync wave, P54 remains the current hygiene sidecar, P55 remains the current promotion-prep "
    "wave, F38 remains the dormant non-runtime dossier, H58 remains the strongest executor-value closeout, H43 "
    "remains the preserved paper-grade endpoint, archive_or_hygiene_stop remains the default downstream lane, and "
    "no dirty-root-main merge or runtime reopen is implied"
)


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def contains_none(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) not in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles) and line not in seen:
            hits.append(line)
            seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def ready_count(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def blocked_count(summary_doc: dict[str, Any]) -> int:
    summary = summary_doc["summary"]
    return int(summary["blocked_count"] if "blocked_count" in summary else summary["blocked_rows"])


def preflight_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["preflight_state"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def diff_check_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["git_diff_check_state"])


def load_inputs() -> dict[str, Any]:
    text_files = {
        "readme_text": "README.md",
        "status_text": "STATUS.md",
        "publication_readme_text": "docs/publication_record/README.md",
        "current_stage_driver_text": "docs/publication_record/current_stage_driver.md",
        "submission_packet_index_text": "docs/publication_record/submission_packet_index.md",
        "archival_manifest_text": "docs/publication_record/archival_repro_manifest.md",
        "review_boundary_text": "docs/publication_record/review_boundary_summary.md",
        "external_release_note_text": "docs/publication_record/external_release_note_skeleton.md",
        "worktree_hygiene_summary_text": "results/release_worktree_hygiene_snapshot/summary.json",
    }
    json_files = {
        "p1_summary": "results/P1_paper_readiness/summary.json",
        "h64_summary": "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
        "h63_summary": "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
        "p53_summary": "results/P53_post_h63_paper_archive_claim_sync/summary.json",
        "p54_summary": "results/P54_post_h63_clean_descendant_hygiene_and_artifact_slimming/summary.json",
        "p55_summary": "results/P55_post_h63_clean_descendant_promotion_prep/summary.json",
        "f38_summary": "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
        "h58_summary": "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
        "h43_summary": "results/H43_post_r44_useful_case_refreeze/summary.json",
        "v1_timing_summary": "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
        "worktree_hygiene_summary": "results/release_worktree_hygiene_snapshot/summary.json",
        "preflight_summary": "results/release_preflight_checklist_audit/summary.json",
        "p5_summary": "results/P5_public_surface_sync/summary.json",
        "p5_callout_summary": "results/P5_callout_alignment/summary.json",
        "h2_summary": "results/H2_bundle_lock_audit/summary.json",
    }
    data = {key: read_text(ROOT / rel) for key, rel in text_files.items()}
    data.update({key: read_json(ROOT / rel) for key, rel in json_files.items()})
    return data


def build_checklist_rows(**inputs: Any) -> list[dict[str, object]]:
    checks = [
        (
            "top_level_surfaces_and_driver_are_current_h64_control",
            all(
                (
                    contains_all(
                        inputs["readme_text"],
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P53_post_h63_paper_archive_claim_sync`",
                            "`P54_post_h63_clean_descendant_hygiene_and_artifact_slimming`",
                            "`P55_post_h63_clean_descendant_promotion_prep`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        inputs["status_text"],
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P53_post_h63_paper_archive_claim_sync`",
                            "`P54_post_h63_clean_descendant_hygiene_and_artifact_slimming`",
                            "`P55_post_h63_clean_descendant_promotion_prep`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        inputs["publication_readme_text"],
                        [
                            "current active docs-only packet",
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "P53_post_h63_paper_archive_claim_sync",
                            "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
                            "P55_post_h63_clean_descendant_promotion_prep",
                        ],
                    ),
                    contains_all(
                        inputs["current_stage_driver_text"],
                        [
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P53_post_h63_paper_archive_claim_sync`",
                            "`P54_post_h63_clean_descendant_hygiene_and_artifact_slimming`",
                            "`P55_post_h63_clean_descendant_promotion_prep`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                )
            ),
            "Top-level surfaces and the canonical driver should all expose the current H64 archive-first freeze stack.",
        ),
        (
            "submission_packet_index_and_archival_manifest_track_current_h64_bundle",
            all(
                (
                    contains_all(
                        inputs["submission_packet_index_text"],
                        [
                            "P53_post_h63_paper_archive_claim_sync",
                            "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
                            "P55_post_h63_clean_descendant_promotion_prep",
                            "F38_post_h62_r63_dormant_eligibility_profile_dossier",
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                        ],
                    ),
                    contains_all(
                        inputs["archival_manifest_text"],
                        [
                            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                            "results/P53_post_h63_paper_archive_claim_sync/summary.json",
                            "results/P54_post_h63_clean_descendant_hygiene_and_artifact_slimming/summary.json",
                            "results/P55_post_h63_clean_descendant_promotion_prep/summary.json",
                            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                            "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
                        ],
                    ),
                )
            ),
            "Submission packet index and archival manifest should point at the same H64 current-control package.",
        ),
        (
            "review_boundary_and_external_release_note_stay_downstream_of_h64_freeze",
            all(
                (
                    contains_all(
                        inputs["review_boundary_text"],
                        [
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "narrow positive mechanism support survives",
                            "broad headline reproduction did not land",
                            "executor-value on the strongest justified lane is closed negative",
                            "dormant no-go dossier at `F38`",
                        ],
                    ),
                    contains_all(
                        inputs["external_release_note_text"],
                        [
                            "archive-first partial falsification",
                            "strongest justified executor-value lane is closed negative",
                            "`H43_post_r44_useful_case_refreeze`",
                            "`H58_post_r62_origin_value_boundary_closeout_packet`",
                            "dormant non-runtime `F38` dossier",
                        ],
                    ),
                    contains_none(inputs["external_release_note_text"], ["docs/origin/", "docs/Origin/"]),
                )
            ),
            "Review and external release-note helpers should stay downstream of archive-first partial falsification.",
        ),
        (
            "standing_release_audits_remain_green",
            ready_count(inputs["p1_summary"]) == 10
            and preflight_state_from_summary(inputs["preflight_summary"]) == "docs_and_audits_green"
            and inputs["h64_summary"]["summary"]["selected_outcome"]
            == "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
            and inputs["h64_summary"]["summary"]["default_downstream_lane"] == "archive_or_hygiene_stop"
            and inputs["h64_summary"]["summary"]["runtime_authorization"] == "closed"
            and inputs["h63_summary"]["summary"]["selected_outcome"]
            == "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"
            and inputs["p53_summary"]["summary"]["selected_outcome"]
            == "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze"
            and inputs["p53_summary"]["summary"]["future_route_posture"] == "dormant_non_runtime_only"
            and inputs["p54_summary"]["summary"]["selected_outcome"]
            == "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution"
            and int(inputs["p54_summary"]["summary"]["tracked_oversize_count"]) == 0
            and bool(inputs["p54_summary"]["summary"]["raw_row_ignore_rules_active"]) is True
            and inputs["p55_summary"]["summary"]["selected_outcome"]
            == "clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze"
            and bool(inputs["p55_summary"]["summary"]["merge_execution_state"]) is False
            and inputs["f38_summary"]["summary"]["selected_outcome"]
            == "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields"
            and inputs["f38_summary"]["summary"]["runtime_authorization"] == "closed"
            and inputs["h58_summary"]["summary"]["selected_outcome"]
            == "stop_as_mechanism_supported_but_no_bounded_executor_value"
            and inputs["h43_summary"]["summary"]["claim_d_state"] == "supported_here_narrowly"
            and blocked_count(inputs["p5_summary"]) == 0
            and blocked_count(inputs["p5_callout_summary"]) == 0
            and blocked_count(inputs["h2_summary"]) == 0
            and inputs["v1_timing_summary"]["summary"]["runtime_classification"] == "healthy_but_slow"
            and int(inputs["v1_timing_summary"]["summary"]["timed_out_file_count"]) == 0,
            "Archive readiness depends on current H64-side audits plus preserved H63/H58/H43 endpoints.",
        ),
        (
            "worktree_hygiene_snapshot_classifies_commit_state",
            release_commit_state_from_summary(inputs["worktree_hygiene_summary"])
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            and diff_check_state_from_summary(inputs["worktree_hygiene_summary"]) != "content_issues_present"
            and contains_all(inputs["worktree_hygiene_summary_text"], ['\"release_commit_state\":', '\"git_diff_check_state\":']),
            "Archive readiness should inherit the current release-worktree hygiene classification.",
        ),
    ]
    return [{"item_id": item_id, "status": "pass" if ok else "blocked", "notes": notes} for item_id, ok, notes in checks]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": ("readme_text", ["`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`", "`archive_or_hygiene_stop`"]),
        "STATUS.md": ("status_text", ["`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`", "`F38_post_h62_r63_dormant_eligibility_profile_dossier`"]),
        "docs/publication_record/README.md": ("publication_readme_text", ["current active docs-only packet", "H64_post_p53_p54_p55_f38_archive_first_freeze_packet"]),
        "docs/publication_record/current_stage_driver.md": ("current_stage_driver_text", ["`P55_post_h63_clean_descendant_promotion_prep`", "`archive_or_hygiene_stop`"]),
        "docs/publication_record/submission_packet_index.md": ("submission_packet_index_text", ["H64_post_p53_p54_p55_f38_archive_first_freeze_packet", "results/P53_post_h63_paper_archive_claim_sync/summary.json"]),
        "docs/publication_record/archival_repro_manifest.md": ("archival_manifest_text", ["results/P54_post_h63_clean_descendant_hygiene_and_artifact_slimming/summary.json", "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json"]),
        "docs/publication_record/review_boundary_summary.md": ("review_boundary_text", ["narrow positive mechanism support survives", "dormant no-go dossier at `F38`"]),
        "docs/publication_record/external_release_note_skeleton.md": ("external_release_note_text", ["archive-first partial falsification", "dormant non-runtime `F38` dossier"]),
        "results/release_worktree_hygiene_snapshot/summary.json": ("worktree_hygiene_summary_text", ['\"release_commit_state\":', '\"git_diff_check_state\":']),
    }
    return [{"path": path, "matched_lines": extract_matching_lines(inputs[key], needles=needles)} for path, (key, needles) in lookup.items()]


def build_summary(checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": CURRENT_PAPER_PHASE,
        "packet_state": "archive_ready" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_hygiene_summary),
        "git_diff_check_state": diff_check_state_from_summary(worktree_hygiene_summary),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": GREEN_ACTION if not blocked_items else "resolve the blocked archive-ready items before using the submission/archive handoff",
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    summary = build_summary(checklist_rows, inputs["worktree_hygiene_summary"])
    write_json(OUT_DIR / "checklist.json", {"experiment": "p10_submission_archive_ready_checklist", "environment": environment.as_dict(), "rows": checklist_rows})
    write_json(OUT_DIR / "snapshot.json", {"experiment": "p10_submission_archive_ready_snapshot", "environment": environment.as_dict(), "rows": build_snapshot(inputs)})
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p10_submission_archive_ready",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/submission_packet_index.md",
                "docs/publication_record/archival_repro_manifest.md",
                "docs/publication_record/review_boundary_summary.md",
                "docs/publication_record/external_release_note_skeleton.md",
                "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
                "results/P53_post_h63_paper_archive_claim_sync/summary.json",
                "results/P54_post_h63_clean_descendant_hygiene_and_artifact_slimming/summary.json",
                "results/P55_post_h63_clean_descendant_promotion_prep/summary.json",
                "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "results/release_preflight_checklist_audit/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# P10 Submission Archive Ready\n\n"
        "Machine-readable audit of whether the current submission/archive handoff surfaces stay aligned with the "
        "H64 archive-first freeze posture while preserving H63 as the prior active packet, H58 as the "
        "value-negative closeout, and H43 as the paper-grade endpoint.\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
