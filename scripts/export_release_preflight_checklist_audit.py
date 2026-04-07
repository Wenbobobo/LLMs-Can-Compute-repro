"""Export a machine-readable audit for the release preflight checklist."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "release_preflight_checklist_audit"

CURRENT_PAPER_PHASE = "h65_p80_archive_facing_stack_with_preserved_p74_p76_h64_h58_h43_endpoints"
PREFLIGHT_SCOPE = "outward_release_surface_and_followthrough_bundle"
GREEN_ACTION = (
    "use this audit together with release_worktree_hygiene_snapshot as the outward-sync control reference while "
    "P77/P78/P79/P80 remain the current archive-facing control stack above the active H65 packet, "
    "P72/P69/P70/P71 remain hygiene-only archive/control sidecars beneath that archive-facing stack, "
    "H65 remains the current active docs-only packet, P56/P57/P58/P59 remain the landed follow-through "
    "foundation, P74/P75/P76 remain the preserved immediate publication lineage on "
    "wip/p75-post-p74-published-successor-freeze, P66/P67/P68 remain the preserved prior successor stack, "
    "P63/P64/P65 remain the preserved deeper successor stack, "
    "H64 remains the preserved prior active packet, F38 remains the dormant non-runtime future dossier, H58 "
    "remains the strongest executor-value closeout, H43 remains the preserved paper-grade endpoint, explicit stop "
    "or no further action is now the recommended downstream route, and no dirty-root-main merge or runtime reopen "
    "is implied"
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


def blocked_count(summary_doc: dict[str, Any]) -> int:
    summary = summary_doc["summary"]
    return int(summary["blocked_count"] if "blocked_count" in summary else summary["blocked_rows"])


def ready_count(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def load_inputs() -> dict[str, Any]:
    text_files = {
        "readme_text": "README.md",
        "status_text": "STATUS.md",
        "docs_readme_text": "docs/README.md",
        "publication_readme_text": "docs/publication_record/README.md",
        "current_stage_driver_text": "docs/publication_record/current_stage_driver.md",
        "plans_readme_text": "docs/plans/README.md",
        "release_summary_text": "docs/publication_record/release_summary_draft.md",
        "release_preflight_text": "docs/publication_record/release_preflight_checklist.md",
        "release_candidate_text": "docs/publication_record/release_candidate_checklist.md",
        "submission_candidate_text": "docs/publication_record/submission_candidate_criteria.md",
        "claim_ladder_text": "docs/publication_record/claim_ladder.md",
        "archival_manifest_text": "docs/publication_record/archival_repro_manifest.md",
        "paper_bundle_status_text": "docs/publication_record/paper_bundle_status.md",
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
        "p5_summary": "results/P5_public_surface_sync/summary.json",
        "p5_callout_summary": "results/P5_callout_alignment/summary.json",
        "h2_summary": "results/H2_bundle_lock_audit/summary.json",
        "worktree_hygiene_summary": "results/release_worktree_hygiene_snapshot/summary.json",
        "v1_timing_summary": "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
    }
    data = {key: read_text(ROOT / rel) for key, rel in text_files.items()}
    data.update({key: read_json(ROOT / rel) for key, rel in json_files.items()})
    return data


def build_checklist_rows(**inputs: Any) -> list[dict[str, object]]:
    text_checks = [
        (
            "top_level_release_surface_stays_narrow_and_h65_terminal_freeze_explicit",
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
                            "`wip/p75-post-p74-published-successor-freeze`",
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
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                        ],
                    ),
                    contains_all(
                        inputs["release_summary_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P72`",
                            "`P56/P57/P58/P59`",
                            "`P66/P67/P68`",
                            "`wip/p75-post-p74-published-successor-freeze`",
                            "archive-first terminal freeze",
                            "R63 remains dormant, non-runtime",
                        ],
                    ),
                )
            ),
            "README, STATUS, and release summary should expose H65 plus the current archive-facing control stack.",
        ),
        (
            "publication_and_plan_indexes_expose_current_h65_route",
            all(
                (
                    contains_all(
                        inputs["docs_readme_text"],
                        [
                            "publication_record/current_stage_driver.md",
                            "branch_worktree_registry.md",
                            "F38_post_h62_r63_dormant_eligibility_profile_dossier",
                            "live",
                            "historical",
                            "dormant",
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
                            "partial_falsification_boundary.md",
                            "future_reopen_screen.md",
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
                            "`P74_post_p73_successor_publication_review`",
                            "`wip/p75-post-p74-published-successor-freeze`",
                            "`explicit_stop_or_no_further_action_archive_first`",
                        ],
                    ),
                    contains_all(
                        inputs["plans_readme_text"],
                        [
                            "2026-04-05-post-p76-hygiene-first-convergence-design.md",
                            "2026-04-05-post-p80-next-planmode-handoff.md",
                            "2026-04-05-post-p80-next-planmode-startup-prompt.md",
                            "2026-04-05-post-p80-next-planmode-brief-prompt.md",
                            "P77_post_p76_keep_set_and_provenance_normalization",
                            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
                            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
                            "P80_post_p79_next_planmode_handoff_sync",
                        ],
                    ),
                )
            ),
            "Publication, control, and planning indexes should expose the current archive-facing control route.",
        ),
        (
            "release_candidate_submission_claim_and_archive_ledgers_align",
            all(
                (
                    contains_all(
                        inputs["release_preflight_text"],
                        [
                            "`H65/P77/P78/P79/P80`",
                            "`P72` hygiene-only archive-polish and explicit-stop handoff sidecar",
                            "`P69/P70/P71` hygiene-only cleanup sidecars",
                            "`P74/P75/P76` as the immediate publication lineage",
                            "`H64/P56/P57/P58/P59/F38` foundation",
                            "`H58` as the value-negative closeout",
                            "`H43` as the preserved paper-grade endpoint",
                            "explicit stop or no further action",
                        ],
                    ),
                    contains_all(
                        inputs["release_candidate_text"],
                        [
                            "`H65/P56/P57/P58/P59/P77/P78/P79/P80/F38`",
                            "`P74/P75/P76` remain preserved immediate publication lineage",
                            "`P72` remains the current archive-polish explicit-stop handoff sidecar",
                            "`P69/P70/P71` remain hygiene-only cleanup sidecars",
                            "preserved `H64/H58/H43`",
                            "no outward wording implies a new runtime lane",
                            "explicit stop or no further action",
                        ],
                    ),
                    contains_all(
                        inputs["submission_candidate_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P77_post_p76_keep_set_and_provenance_normalization`",
                            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
                            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
                            "`P80_post_p79_next_planmode_handoff_sync`",
                            "`P71_post_p70_clean_descendant_merge_prep_readiness_sync`",
                            "`P70_post_p69_archive_index_and_artifact_policy_sync`",
                            "`P69_post_h65_repo_graph_hygiene_inventory`",
                            "`P76_post_p75_release_hygiene_and_control_rebaseline`",
                            "`H58_post_r62_origin_value_boundary_closeout_packet`",
                            "`H43_post_r44_useful_case_refreeze`",
                            "do not authorize a runtime reopen",
                            "explicit stop or no further action",
                        ],
                    ),
                    contains_all(
                        inputs["claim_ladder_text"],
                        [
                            "| P79 Archive claim boundary and reopen screen |",
                            "| P80 Next-planmode handoff sync |",
                            "| P74/P75/P76 Immediate publication lineage |",
                        ],
                    ),
                    contains_all(
                        inputs["archival_manifest_text"],
                        [
                            "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
                            "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
                            "results/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/summary.json",
                            "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json",
                            "results/P72_post_p71_archive_polish_and_explicit_stop_handoff/summary.json",
                            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
                            "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
                            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                        ],
                    ),
                )
            ),
            "Release, submission, claim, and archive ledgers should expose the same current archive-facing stack and preserved publication lineage.",
        ),
        (
            "paper_bundle_ledgers_stay_downstream_of_archive_first_partial_falsification",
            all(
                (
                    contains_all(
                        inputs["paper_bundle_status_text"],
                        [
                            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
                            "`P80_post_p79_next_planmode_handoff_sync`",
                            "`P74_post_p73_successor_publication_review`",
                            "`P76_post_p75_release_hygiene_and_control_rebaseline`",
                            "archive-first terminal-freeze and explicit-stop framing",
                        ],
                    ),
                    contains_all(
                        inputs["review_boundary_text"],
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P79/P80`",
                            "`P56/P57/P58/P59`",
                            "narrow positive mechanism support survives",
                            "the only remaining future route is a dormant no-go dossier at `F38` unless a",
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
                )
            ),
            "Paper bundle and outward helper notes must stay downstream of archive-first terminal freeze.",
        ),
        (
            "blog_rules_keep_restrained_release_surface",
            contains_all(
                read_text(ROOT / "docs" / "publication_record" / "blog_release_rules.md"),
                [
                    "release_candidate_checklist.md",
                    "blog stays blocked unless all of the following are true",
                    "no arbitrary C",
                    "no broad “LLMs are computers” framing",
                ],
            ),
            "Blocked-blog rules should remain explicit and downstream.",
        ),
    ]
    summary_checks = [
        (
            "release_worktree_hygiene_snapshot_classifies_commit_state",
            inputs["worktree_hygiene_summary"]["summary"]["release_commit_state"]
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            and inputs["worktree_hygiene_summary"]["summary"]["git_diff_check_state"] != "content_issues_present"
            and contains_all(inputs["worktree_hygiene_summary_text"], ['"release_commit_state":', '"git_diff_check_state":']),
            "The worktree hygiene snapshot should classify current release-commit readiness.",
        ),
        (
            "standing_h65_followthrough_audits_remain_green",
            ready_count(inputs["p1_summary"]) == 10
            and not inputs["p1_summary"]["blocked_or_partial_items"]
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
            "Standing release-preflight state depends on H65, the landed P56/P57/P58/P59 foundation, and the current archive-facing control stack.",
        ),
    ]
    return [
        {"item_id": item_id, "status": "pass" if ok else "blocked", "notes": notes}
        for item_id, ok, notes in [*text_checks, *summary_checks]
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": ("readme_text", ["`P77_post_p76_keep_set_and_provenance_normalization`", "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`"]),
        "STATUS.md": ("status_text", ["`P80_post_p79_next_planmode_handoff_sync`", "`explicit_stop_or_no_further_action_archive_first`"]),
        "docs/README.md": ("docs_readme_text", ["current_stage_driver.md", "branch_worktree_registry.md", "Dormant Future"]),
        "docs/publication_record/current_stage_driver.md": ("current_stage_driver_text", ["`P80_post_p79_next_planmode_handoff_sync`", "`wip/p75-post-p74-published-successor-freeze`"]),
        "docs/plans/README.md": ("plans_readme_text", ["2026-04-05-post-p80-next-planmode-handoff.md", "P80_post_p79_next_planmode_handoff_sync"]),
        "docs/publication_record/release_preflight_checklist.md": ("release_preflight_text", ["`P72` hygiene-only archive-polish and explicit-stop handoff sidecar", "dirty root `main`"]),
        "docs/publication_record/release_candidate_checklist.md": ("release_candidate_text", ["`H65/P56/P57/P58/P59/P77/P78/P79/P80/F38`", "preserved `H64/H58/H43`"]),
        "docs/publication_record/claim_ladder.md": ("claim_ladder_text", ["| P79 Archive claim boundary and reopen screen |", "| P74/P75/P76 Immediate publication lineage |"]),
        "docs/publication_record/archival_repro_manifest.md": ("archival_manifest_text", ["results/P80_post_p79_next_planmode_handoff_sync/summary.json", "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json"]),
        "results/release_worktree_hygiene_snapshot/summary.json": ("worktree_hygiene_summary_text", ['"release_commit_state":', '"git_diff_check_state":']),
    }
    return [{"path": path, "matched_lines": extract_matching_lines(inputs[key], needles=needles)} for path, (key, needles) in lookup.items()]


def build_summary(checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": CURRENT_PAPER_PHASE,
        "preflight_scope": PREFLIGHT_SCOPE,
        "preflight_state": "docs_and_audits_green" if not blocked_items else "blocked",
        "release_commit_state": worktree_hygiene_summary["summary"]["release_commit_state"],
        "git_diff_check_state": worktree_hygiene_summary["summary"]["git_diff_check_state"],
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": GREEN_ACTION if not blocked_items else "resolve the blocked release-preflight items before treating outward-sync docs as stable",
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    summary = build_summary(checklist_rows, inputs["worktree_hygiene_summary"])
    write_json(OUT_DIR / "checklist.json", {"experiment": "release_preflight_checklist_audit_checklist", "environment": environment.as_dict(), "rows": checklist_rows})
    write_json(OUT_DIR / "snapshot.json", {"experiment": "release_preflight_checklist_audit_snapshot", "environment": environment.as_dict(), "rows": build_snapshot(inputs)})
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "release_preflight_checklist_audit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/README.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/plans/README.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/release_preflight_checklist.md",
                "docs/publication_record/release_candidate_checklist.md",
                "docs/publication_record/submission_candidate_criteria.md",
                "docs/publication_record/claim_ladder.md",
                "docs/publication_record/archival_repro_manifest.md",
                "docs/publication_record/paper_bundle_status.md",
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
                "results/release_worktree_hygiene_snapshot/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# Release Preflight Checklist Audit\n\n"
        "Machine-readable audit of whether outward release-facing docs and the frozen paper bundle remain aligned on "
        "the H65 published frozen successor posture while preserving H64 as the prior active packet, P63/P64/P65 as "
        "the prior successor stack, H58 as the value-negative closeout, and H43 as the paper-grade "
        "endpoint.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()



