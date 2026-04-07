"""Export the P10 submission/archive readiness audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P10_submission_archive_ready"

CURRENT_PAPER_PHASE = "h65_p80_archive_facing_stack_with_preserved_p74_p76_h64_h58_h43_endpoints"
GREEN_ACTION = (
    "use submission_packet_index.md plus archival_repro_manifest.md as the canonical handoff while H65 remains "
    "the current active docs-only packet, P77/P78/P79/P80 remain the current archive-facing control stack, "
    "P72/P71/P70/P69 remain hygiene-only archive/control sidecars beneath that archive-facing stack, "
    "P56/P57/P58/P59 remain the landed follow-through foundation, "
    "P74/P75/P76 remain the preserved immediate publication lineage on "
    "wip/p75-post-p74-published-successor-freeze, P66/P67/P68 remain the preserved prior successor stack, "
    "P63/P64/P65 remain the preserved deeper successor stack, "
    "H64 remains the preserved prior active packet, F38 remains the dormant non-runtime dossier, H58 remains "
    "the strongest executor-value closeout, H43 remains the preserved paper-grade endpoint, explicit stop or no "
    "further action is now the recommended downstream route, and no dirty-root-main merge or runtime reopen is implied"
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
        "h65_summary": "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
        "h64_summary": "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
        "p74_summary": "results/P74_post_p73_successor_publication_review/summary.json",
        "p75_summary": "results/P75_post_p74_published_successor_freeze/summary.json",
        "p76_summary": "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
        "p77_summary": "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json",
        "p78_summary": "results/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/summary.json",
        "p79_summary": "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
        "p80_summary": "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
        "p56_summary": "results/P56_post_h64_clean_merge_candidate_packet/summary.json",
        "p57_summary": "results/P57_post_h64_paper_submission_package_sync/summary.json",
        "p58_summary": "results/P58_post_h64_archive_release_closeout_sync/summary.json",
        "p59_summary": "results/P59_post_h64_control_and_handoff_sync/summary.json",
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
            "top_level_surfaces_and_driver_are_current_h65_frozen_successor_control",
            all(
                (
                    contains_all(
                        inputs["readme_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P77_post_p76_keep_set_and_provenance_normalization`",
                            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
                            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
                            "`P80_post_p79_next_planmode_handoff_sync`",
                            "`explicit_stop_or_no_further_action_archive_first`",
                        ],
                    ),
                    contains_all(
                        inputs["status_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P77_post_p76_keep_set_and_provenance_normalization`",
                            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
                            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
                            "`P80_post_p79_next_planmode_handoff_sync`",
                        ],
                    ),
                    contains_all(
                        inputs["publication_readme_text"],
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P77_post_p76_keep_set_and_provenance_normalization",
                            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
                            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
                            "P80_post_p79_next_planmode_handoff_sync",
                        ],
                    ),
                    contains_all(
                        inputs["current_stage_driver_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P77_post_p76_keep_set_and_provenance_normalization`",
                            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
                            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
                            "`P80_post_p79_next_planmode_handoff_sync`",
                            "`explicit_stop_or_no_further_action_archive_first`",
                        ],
                    ),
                )
            ),
            "Top-level surfaces and the canonical driver should all expose the current archive-facing control stack.",
        ),
        (
            "submission_packet_index_and_archival_manifest_track_current_bundle",
            all(
                (
                    contains_all(
                        inputs["submission_packet_index_text"],
                        [
                            "P72/P71/P70/P69 entries below are hygiene-only control sidecars",
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P80_post_p79_next_planmode_handoff_sync",
                            "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
                            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
                            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
                            "P77_post_p76_keep_set_and_provenance_normalization",
                            "do not widen the paper-facing evidence bundle",
                        ],
                    ),
                    contains_all(
                        inputs["archival_manifest_text"],
                        [
                            "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
                            "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
                            "results/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/summary.json",
                            "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json",
                            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
                            "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
                            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                            "preserved immediate publication lineage",
                        ],
                    ),
                )
            ),
            "Submission packet index and archival manifest should point at the same archive-facing control package.",
        ),
        (
            "review_boundary_and_external_release_note_stay_downstream_of_h65_terminal_freeze",
            all(
                (
                    contains_all(
                        inputs["review_boundary_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P79/P80`",
                            "`P56/P57/P58/P59`",
                            "narrow positive mechanism support survives",
                            "the only remaining future route is a dormant no-go dossier at `F38`",
                            "explicit stop",
                            "no further action",
                        ],
                    ),
                    contains_all(
                        inputs["external_release_note_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P79/P80`",
                            "`P56/P57/P58/P59`",
                            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
                            "`H43_post_r44_useful_case_refreeze`",
                            "`H58_post_r62_origin_value_boundary_closeout_packet`",
                            "dormant non-runtime `F38` dossier",
                        ],
                    ),
                    contains_all(
                        inputs["external_release_note_text"],
                        [
                            "archive-first terminal freeze",
                            "strongest justified executor-value lane is closed negative",
                            "explicit stop",
                            "no further action",
                        ],
                    ),
                )
            ),
            "Review and external release-note helpers should stay downstream of archive-first terminal freeze.",
        ),
        (
            "standing_release_audits_remain_green",
            ready_count(inputs["p1_summary"]) == 10
            and preflight_state_from_summary(inputs["preflight_summary"]) == "docs_and_audits_green"
            and inputs["h65_summary"]["summary"]["selected_outcome"]
            == "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop"
            and inputs["h64_summary"]["summary"]["selected_outcome"]
            == "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
            and inputs["p74_summary"]["summary"]["selected_outcome"]
            == "successor_publication_review_supports_p75_freeze"
            and inputs["p75_summary"]["summary"]["selected_outcome"]
            == "published_successor_freeze_locked_after_p74_review"
            and inputs["p76_summary"]["summary"]["selected_outcome"]
            == "published_successor_release_hygiene_and_control_rebaselined_after_p75"
            and inputs["p77_summary"]["summary"]["selected_outcome"]
            == "keep_set_and_provenance_normalized_after_p76"
            and inputs["p78_summary"]["summary"]["selected_outcome"]
            == "balanced_worktree_convergence_completed_with_quarantines_preserved"
            and inputs["p79_summary"]["summary"]["selected_outcome"]
            == "archive_claim_boundary_and_reopen_screen_locked_after_convergence"
            and inputs["p80_summary"]["summary"]["selected_outcome"]
            == "next_planmode_handoff_synced_to_explicit_stop_after_p79"
            and inputs["p56_summary"]["summary"]["selected_outcome"]
            == "clean_descendant_merge_candidate_staged_without_merge_execution"
            and inputs["p57_summary"]["summary"]["selected_outcome"]
            == "paper_submission_package_surfaces_synced_to_h64_followthrough_stack"
            and inputs["p58_summary"]["summary"]["selected_outcome"]
            == "archive_release_closeout_surfaces_synced_to_h64_followthrough_stack"
            and inputs["p59_summary"]["summary"]["selected_outcome"]
            == "control_and_handoff_surfaces_synced_to_h64_followthrough_stack"
            and inputs["f38_summary"]["summary"]["runtime_authorization"] == "closed"
            and inputs["h58_summary"]["summary"]["selected_outcome"]
            == "stop_as_mechanism_supported_but_no_bounded_executor_value"
            and inputs["h43_summary"]["summary"]["claim_d_state"] == "supported_here_narrowly"
            and blocked_count(inputs["p5_summary"]) == 0
            and blocked_count(inputs["p5_callout_summary"]) == 0
            and blocked_count(inputs["h2_summary"]) == 0
            and inputs["v1_timing_summary"]["summary"]["runtime_classification"] == "healthy_but_slow"
            and int(inputs["v1_timing_summary"]["summary"]["timed_out_file_count"]) == 0,
            "Archive readiness depends on H65, the current archive-facing control stack, and preserved H64/H58/H43 endpoints.",
        ),
        (
            "worktree_hygiene_snapshot_classifies_commit_state",
            release_commit_state_from_summary(inputs["worktree_hygiene_summary"])
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            and diff_check_state_from_summary(inputs["worktree_hygiene_summary"]) != "content_issues_present"
            and contains_all(inputs["worktree_hygiene_summary_text"], ['"release_commit_state":', '"git_diff_check_state":']),
            "Archive readiness should inherit the current release-worktree hygiene classification.",
        ),
    ]
    return [{"item_id": item_id, "status": "pass" if ok else "blocked", "notes": notes} for item_id, ok, notes in checks]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": ("readme_text", ["`P77_post_p76_keep_set_and_provenance_normalization`", "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`"]),
        "STATUS.md": ("status_text", ["`P80_post_p79_next_planmode_handoff_sync`", "`explicit_stop_or_no_further_action_archive_first`"]),
        "docs/publication_record/current_stage_driver.md": ("current_stage_driver_text", ["`P80_post_p79_next_planmode_handoff_sync`", "`explicit_stop_or_no_further_action_archive_first`"]),
        "docs/publication_record/submission_packet_index.md": ("submission_packet_index_text", ["H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "results/P80_post_p79_next_planmode_handoff_sync/summary.json"]),
        "docs/publication_record/archival_repro_manifest.md": ("archival_manifest_text", ["results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json", "results/P80_post_p79_next_planmode_handoff_sync/summary.json"]),
        "docs/publication_record/review_boundary_summary.md": ("review_boundary_text", ["`P56/P57/P58/P59`", "dormant no-go dossier at `F38`"]),
        "docs/publication_record/external_release_note_skeleton.md": ("external_release_note_text", ["`P56/P57/P58/P59`", "dormant non-runtime `F38` dossier"]),
        "results/release_worktree_hygiene_snapshot/summary.json": ("worktree_hygiene_summary_text", ['"release_commit_state":', '"git_diff_check_state":']),
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
                "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
                "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                "results/P74_post_p73_successor_publication_review/summary.json",
                "results/P75_post_p74_published_successor_freeze/summary.json",
                "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
                "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json",
                "results/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/summary.json",
                "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
                "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
                "results/P56_post_h64_clean_merge_candidate_packet/summary.json",
                "results/P57_post_h64_paper_submission_package_sync/summary.json",
                "results/P58_post_h64_archive_release_closeout_sync/summary.json",
                "results/P59_post_h64_control_and_handoff_sync/summary.json",
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
        "H65 published frozen successor posture while preserving H64 as the prior active packet, P63/P64/P65 as "
        "the prior successor stack, H58 as the value-negative closeout, and H43 as the paper-grade "
        "endpoint.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()



