"""Export a machine-readable audit for the release preflight checklist."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "release_preflight_checklist_audit"

CURRENT_PAPER_PHASE = "h63_archive_first_closeout_with_preserved_h58_h43_endpoints"
PREFLIGHT_SCOPE = "outward_release_surface_and_archive_first_closeout_bundle"
GREEN_ACTION = (
    "use this audit together with release_worktree_hygiene_snapshot as the outward-sync control reference while "
    "H63 remains the current active docs-only packet, P50/P51/P52 remain the current archive-first closeout "
    "sidecars, F38 remains the only dormant non-runtime future dossier, H58 remains the strongest executor-value "
    "closeout, H43 remains the preserved paper-grade endpoint, archive_or_hygiene_stop remains the default "
    "downstream lane, and no dirty-root-main merge or runtime reopen is implied"
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
        "release_summary_text": "docs/publication_record/release_summary_draft.md",
        "release_preflight_text": "docs/publication_record/release_preflight_checklist.md",
        "release_candidate_text": "docs/publication_record/release_candidate_checklist.md",
        "submission_candidate_text": "docs/publication_record/submission_candidate_criteria.md",
        "claim_ladder_text": "docs/publication_record/claim_ladder.md",
        "archival_manifest_text": "docs/publication_record/archival_repro_manifest.md",
        "manuscript_text": "docs/publication_record/manuscript_bundle_draft.md",
        "paper_bundle_status_text": "docs/publication_record/paper_bundle_status.md",
        "layout_log_text": "docs/publication_record/layout_decision_log.md",
        "freeze_candidate_text": "docs/publication_record/freeze_candidate_criteria.md",
        "main_text_order_text": "docs/publication_record/main_text_order.md",
        "appendix_scope_text": "docs/publication_record/appendix_companion_scope.md",
        "blog_rules_text": "docs/publication_record/blog_release_rules.md",
        "worktree_hygiene_summary_text": "results/release_worktree_hygiene_snapshot/summary.json",
    }
    json_files = {
        "p1_summary": "results/P1_paper_readiness/summary.json",
        "h63_summary": "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
        "p50_summary": "results/P50_post_h62_archive_first_control_sync/summary.json",
        "p51_summary": "results/P51_post_h62_paper_facing_partial_falsification_package/summary.json",
        "p52_summary": "results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json",
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
            "top_level_release_surface_stays_narrow_and_h63_explicit",
            all(
                (
                    contains_all(
                        inputs["readme_text"],
                        [
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P50_post_h62_archive_first_control_sync`",
                            "`P51_post_h62_paper_facing_partial_falsification_package`",
                            "`P52_post_h62_clean_descendant_hygiene_and_merge_prep`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        inputs["status_text"],
                        [
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet`",
                            "`P50_post_h62_archive_first_control_sync`",
                            "`P51_post_h62_paper_facing_partial_falsification_package`",
                            "`P52_post_h62_clean_descendant_hygiene_and_merge_prep`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        inputs["release_summary_text"],
                        [
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "archive-first closeout is now the default repo meaning",
                            "paper-facing partial falsification is now the correct outward shorthand",
                            "strongest justified executor-value lane is closed negative",
                            "R63 remains dormant",
                        ],
                    ),
                )
            ),
            "README, STATUS, and release summary should all expose the H63 archive-first closeout posture.",
        ),
        (
            "release_candidate_submission_claim_and_archive_ledgers_align_on_h63_h58_h43_split",
            all(
                (
                    contains_all(
                        inputs["release_preflight_text"],
                        [
                            "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
                            "results/P50_post_h62_archive_first_control_sync/summary.json",
                            "results/P51_post_h62_paper_facing_partial_falsification_package/summary.json",
                            "results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json",
                            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                            "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
                            "results/H43_post_r44_useful_case_refreeze/summary.json",
                        ],
                    ),
                    contains_all(
                        inputs["release_candidate_text"],
                        [
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P51` as paper-facing package",
                            "`P52` as hygiene sidecar",
                            "`F38` as the dormant future dossier",
                            "preserved `H58/H43`",
                        ],
                    ),
                    contains_all(
                        inputs["submission_candidate_text"],
                        [
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P51_post_h62_paper_facing_partial_falsification_package`",
                            "`P52_post_h62_clean_descendant_hygiene_and_merge_prep`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "`H58_post_r62_origin_value_boundary_closeout_packet`",
                            "`H43_post_r44_useful_case_refreeze`",
                            "dormant and non-runtime only",
                        ],
                    ),
                    contains_all(
                        inputs["claim_ladder_text"],
                        [
                            "| H43 Post-R44 useful-case refreeze |",
                            "| H58 Value-negative closeout |",
                            "| P50 Archive-first control sync |",
                            "| P51 paper-facing partial-falsification package |",
                            "| P52 Clean-descendant hygiene and merge-prep |",
                            "| F38 dormant R63 eligibility dossier |",
                            "| H63 archive-first closeout packet |",
                        ],
                    ),
                    contains_all(
                        inputs["archival_manifest_text"],
                        [
                            "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
                            "results/P50_post_h62_archive_first_control_sync/summary.json",
                            "results/P51_post_h62_paper_facing_partial_falsification_package/summary.json",
                            "results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json",
                            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
                        ],
                    ),
                )
            ),
            "Release, submission, claim, and archive ledgers should expose the same H63 plus preserved H58/H43 split.",
        ),
        (
            "paper_bundle_ledgers_stay_downstream_of_archive_first_partial_falsification",
            all(
                (
                    contains_all(inputs["manuscript_text"], ["## 1. Abstract", "## 10. Reproducibility Appendix"]),
                    contains_all(
                        inputs["paper_bundle_status_text"],
                        [
                            "`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`",
                            "`P51_post_h62_paper_facing_partial_falsification_package`",
                            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
                            "archive-first partial-falsification closeout framing",
                        ],
                    ),
                    contains_all(inputs["layout_log_text"], ["Post-`P7` next phase", "Evidence reopen discipline"]),
                    contains_all(
                        inputs["freeze_candidate_text"],
                        [
                            "active `H43` docs-only useful-case refreeze packet",
                            "broader `H43` paper-grade endpoint",
                            "completed `R42/R43/R44/R45`",
                        ],
                    ),
                    contains_all(inputs["main_text_order_text"], ["## Fixed order", "Compiled Boundary"]),
                    contains_all(inputs["appendix_scope_text"], ["## Required companions", "## Out of scope on the current freeze candidate"]),
                )
            ),
            "Paper bundle ledgers should keep H43 explicit while H63 controls outward archive-first framing.",
        ),
        (
            "blog_rules_keep_restrained_release_surface",
            contains_all(
                inputs["blog_rules_text"],
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
            and contains_all(inputs["worktree_hygiene_summary_text"], ['\"release_commit_state\":', '\"git_diff_check_state\":']),
            "The worktree hygiene snapshot should classify current release-commit readiness.",
        ),
        (
            "standing_h63_audits_remain_green_or_honestly_dormant",
            ready_count(inputs["p1_summary"]) == 10
            and not inputs["p1_summary"]["blocked_or_partial_items"]
            and inputs["h63_summary"]["summary"]["selected_outcome"]
            == "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"
            and inputs["h63_summary"]["summary"]["default_downstream_lane"] == "archive_or_hygiene_stop"
            and inputs["h63_summary"]["summary"]["runtime_authorization"] == "closed"
            and inputs["p50_summary"]["summary"]["selected_outcome"]
            == "control_surfaces_locked_to_post_h62_archive_first_closeout"
            and inputs["p50_summary"]["summary"]["current_downstream_scientific_lane"] == "archive_or_hygiene_stop"
            and inputs["p51_summary"]["summary"]["selected_outcome"]
            == "paper_surfaces_locked_to_archive_first_partial_falsification_closeout"
            and inputs["p51_summary"]["summary"]["future_route_posture"] == "dormant_non_runtime_only"
            and inputs["p52_summary"]["summary"]["selected_outcome"]
            == "clean_descendant_hygiene_and_merge_prep_locked_without_dirty_root_merge"
            and int(inputs["p52_summary"]["summary"]["tracked_oversize_count"]) == 0
            and bool(inputs["p52_summary"]["summary"]["raw_row_ignore_rules_active"]) is True
            and inputs["f38_summary"]["summary"]["selected_outcome"]
            == "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields"
            and inputs["f38_summary"]["summary"]["runtime_authorization"] == "closed"
            and bool(inputs["f38_summary"]["summary"]["exact_target_declared"]) is True
            and bool(inputs["f38_summary"]["summary"]["cost_share_declared"]) is False
            and bool(inputs["f38_summary"]["summary"]["query_insert_declared"]) is False
            and bool(inputs["f38_summary"]["summary"]["tie_burden_declared"]) is False
            and bool(inputs["f38_summary"]["summary"]["materially_different_cost_model_shown"]) is False
            and inputs["h58_summary"]["summary"]["selected_outcome"]
            == "stop_as_mechanism_supported_but_no_bounded_executor_value"
            and inputs["h58_summary"]["summary"]["current_downstream_scientific_lane"] == "no_active_downstream_runtime_lane"
            and inputs["h43_summary"]["summary"]["selected_outcome"] == "freeze_r44_as_narrow_supported_here"
            and inputs["h43_summary"]["summary"]["claim_d_state"] == "supported_here_narrowly"
            and blocked_count(inputs["p5_summary"]) == 0
            and blocked_count(inputs["p5_callout_summary"]) == 0
            and blocked_count(inputs["h2_summary"]) == 0
            and inputs["v1_timing_summary"]["summary"]["runtime_classification"] == "healthy_but_slow"
            and int(inputs["v1_timing_summary"]["summary"]["timed_out_file_count"]) == 0,
            "Standing release-preflight state depends on H63/P50/P51/P52/F38 plus preserved H58/H43.",
        ),
    ]
    return [
        {"item_id": item_id, "status": "pass" if ok else "blocked", "notes": notes}
        for item_id, ok, notes in [*text_checks, *summary_checks]
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": ("readme_text", ["`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`", "`archive_or_hygiene_stop`"]),
        "STATUS.md": ("status_text", ["`H63_post_p50_p51_p52_f38_archive_first_closeout_packet`", "`F38_post_h62_r63_dormant_eligibility_profile_dossier`"]),
        "docs/publication_record/release_summary_draft.md": ("release_summary_text", ["archive-first closeout is now the default repo meaning", "R63 remains dormant"]),
        "docs/publication_record/release_preflight_checklist.md": ("release_preflight_text", ["results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json", "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json"]),
        "docs/publication_record/release_candidate_checklist.md": ("release_candidate_text", ["`P51` as paper-facing package", "preserved `H58/H43`"]),
        "docs/publication_record/submission_candidate_criteria.md": ("submission_candidate_text", ["`P52_post_h62_clean_descendant_hygiene_and_merge_prep`", "`H43_post_r44_useful_case_refreeze`"]),
        "docs/publication_record/claim_ladder.md": ("claim_ladder_text", ["| H58 Value-negative closeout |", "| H63 archive-first closeout packet |"]),
        "docs/publication_record/archival_repro_manifest.md": ("archival_manifest_text", ["results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json", "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json"]),
        "results/release_worktree_hygiene_snapshot/summary.json": ("worktree_hygiene_summary_text", ['\"release_commit_state\":', '\"git_diff_check_state\":']),
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
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/release_preflight_checklist.md",
                "docs/publication_record/release_candidate_checklist.md",
                "docs/publication_record/submission_candidate_criteria.md",
                "docs/publication_record/claim_ladder.md",
                "docs/publication_record/archival_repro_manifest.md",
                "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
                "results/P50_post_h62_archive_first_control_sync/summary.json",
                "results/P51_post_h62_paper_facing_partial_falsification_package/summary.json",
                "results/P52_post_h62_clean_descendant_hygiene_and_merge_prep/summary.json",
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
        "the H63 archive-first closeout posture while preserving H58 as the value-negative closeout and H43 as the "
        "paper-grade endpoint.\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
