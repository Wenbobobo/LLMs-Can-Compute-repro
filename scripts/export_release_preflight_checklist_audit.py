"""Export a machine-readable audit for the release preflight checklist."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "release_preflight_checklist_audit"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles):
            if line not in seen:
                hits.append(line)
                seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def load_inputs() -> dict[str, Any]:
    return {
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "release_preflight_text": read_text(
            ROOT / "docs" / "publication_record" / "release_preflight_checklist.md"
        ),
        "release_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "release_candidate_checklist.md"
        ),
        "submission_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md"
        ),
        "claim_ladder_text": read_text(ROOT / "docs" / "publication_record" / "claim_ladder.md"),
        "archival_manifest_text": read_text(
            ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"
        ),
        "manuscript_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_bundle_draft.md"),
        "paper_bundle_status_text": read_text(
            ROOT / "docs" / "publication_record" / "paper_bundle_status.md"
        ),
        "layout_log_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
        "freeze_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "freeze_candidate_criteria.md"
        ),
        "main_text_order_text": read_text(ROOT / "docs" / "publication_record" / "main_text_order.md"),
        "appendix_scope_text": read_text(
            ROOT / "docs" / "publication_record" / "appendix_companion_scope.md"
        ),
        "blog_rules_text": read_text(ROOT / "docs" / "publication_record" / "blog_release_rules.md"),
        "p1_summary": read_json(ROOT / "results" / "P1_paper_readiness" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "r44_summary": read_json(ROOT / "results" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "summary.json"),
        "r45_summary": read_json(ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate" / "summary.json"),
        "r43_summary": read_json(ROOT / "results" / "R43_origin_bounded_memory_small_vm_execution_gate" / "summary.json"),
        "p27_summary": read_json(
            ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"
        ),
        "p28_summary": read_json(ROOT / "results" / "P28_post_h43_publication_surface_sync" / "summary.json"),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "p5_callout_summary": read_json(ROOT / "results" / "P5_callout_alignment" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
        "worktree_hygiene_summary_text": read_text(
            ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
        ),
        "worktree_hygiene_summary": read_json(
            ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
        ),
        "v1_timing_summary": read_json(
            ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup" / "summary.json"
        ),
    }


def ready_count_from_p1_summary(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    summary = summary_doc["summary"]
    if "blocked_count" in summary:
        return int(summary["blocked_count"])
    return int(summary["blocked_rows"])


def runtime_classification_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["runtime_classification"])


def timed_out_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["timed_out_file_count"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def diff_check_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["git_diff_check_state"])


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    release_summary_text: str,
    release_preflight_text: str,
    release_candidate_text: str,
    submission_candidate_text: str,
    claim_ladder_text: str,
    archival_manifest_text: str,
    manuscript_text: str,
    paper_bundle_status_text: str,
    layout_log_text: str,
    freeze_candidate_text: str,
    main_text_order_text: str,
    appendix_scope_text: str,
    blog_rules_text: str,
    p1_summary: dict[str, Any],
    h43_summary: dict[str, Any],
    r44_summary: dict[str, Any],
    r45_summary: dict[str, Any],
    r43_summary: dict[str, Any],
    p27_summary: dict[str, Any],
    p28_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    p5_callout_summary: dict[str, Any],
    h2_summary: dict[str, Any],
    worktree_hygiene_summary_text: str,
    worktree_hygiene_summary: dict[str, Any],
    v1_timing_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "top_level_release_surface_stays_narrow_and_active_stage_explicit",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "does **not** claim that general llms are computers",
                    "arbitrary c has been reproduced",
                    "the current active stage is",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "no active downstream runtime lane now follows `h43`",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h43_post_r44_useful_case_refreeze`",
                    "`h42_post_r43_route_selection_packet`",
                    "`h36_post_r40_bounded_scalar_family_refreeze`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "`merge_executed = false`",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should keep the H43 release-control stack explicit while preserving narrow non-goals.",
        },
        {
            "item_id": "release_preflight_checklist_tracks_current_machine_guards",
            "status": "pass"
            if contains_all(
                release_preflight_text,
                [
                    "results/p1_paper_readiness/summary.json",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                    "results/r44_origin_restricted_wasm_useful_case_execution_gate/summary.json",
                    "results/r45_origin_dual_mode_model_mainline_gate/summary.json",
                    "results/r43_origin_bounded_memory_small_vm_execution_gate/summary.json",
                    "results/p27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json",
                    "results/r42_origin_append_only_memory_retrieval_contract_gate/summary.json",
                    "results/h40_post_h38_semantic_boundary_activation_packet/summary.json",
                    "results/h38_post_f16_runtime_relevance_reopen_decision_packet/summary.json",
                    "results/p26_post_h37_promotion_and_artifact_hygiene_audit/summary.json",
                    "results/h37_post_h36_runtime_relevance_decision_packet/summary.json",
                    "results/h36_post_r40_bounded_scalar_family_refreeze/summary.json",
                    "results/p25_post_h36_clean_promotion_prep/summary.json",
                    "results/h35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json",
                    "results/r40_origin_bounded_scalar_locals_and_flags_gate/summary.json",
                    "results/h34_post_r39_later_explicit_scope_decision_packet/summary.json",
                    "results/h32_post_r38_compiled_boundary_refreeze/summary.json",
                    "results/p5_public_surface_sync/summary.json",
                    "results/h2_bundle_lock_audit/summary.json",
                    "results/release_worktree_hygiene_snapshot/summary.json",
                    "results/v1_full_suite_validation_runtime_timing_followup/summary.json",
                    "release_candidate_checklist.md",
                    "submission_candidate_criteria.md",
                    "claim_ladder.md",
                    "archival_repro_manifest.md",
                ],
            )
            else "blocked",
            "notes": "The human release checklist should point at the current H43-era machine guards and downstream ledgers.",
        },
        {
            "item_id": "release_summary_and_blog_rules_stay_downstream",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "`h43_post_r44_useful_case_refreeze`",
                    "completed current semantic-boundary gate stack",
                    "`p28` aligns publication-facing ledgers to landed `h43`",
                    "no active downstream runtime lane exists after `h43`",
                ],
            )
            and contains_all(
                blog_rules_text,
                [
                    "release_candidate_checklist.md",
                    "blog stays blocked unless all of the following are true",
                    "no arbitrary c",
                    "no broad “llms are computers” framing",
                ],
            )
            else "blocked",
            "notes": "Release summary and blog rules must remain downstream of the landed H43 stack.",
        },
        {
            "item_id": "manuscript_and_bundle_ledgers_stay_synchronized",
            "status": "pass"
            if contains_all(
                manuscript_text,
                [
                    "## 1. Abstract",
                    "## 10. Reproducibility Appendix",
                    "Companion appendix material stays clearly downstream",
                ],
            )
            and contains_all(
                paper_bundle_status_text,
                [
                    "`h43` is the current docs-only useful-case refreeze packet",
                    "`r42`, `r43`, `r44`, and `r45` are the completed current semantic-boundary",
                    "`p28` aligns publication-facing ledgers to landed `h43`",
                ],
            )
            and contains_all(
                layout_log_text,
                ["Post-`P7` next phase", "Release-summary reuse", "Evidence reopen discipline"],
            )
            and contains_all(
                freeze_candidate_text,
                [
                    "active `h43` docs-only useful-case refreeze packet",
                    "completed `r42/r43/r44/r45`",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                main_text_order_text,
                [
                    "## Fixed order",
                    "Introduction and Claim Ladder",
                    "Compiled Boundary",
                    "Do not promote the full `R2` runtime matrix",
                ],
            )
            and contains_all(
                appendix_scope_text,
                [
                    "## Required companions",
                    "## Allowed optional companions",
                    "## Out of scope on the current freeze candidate",
                    "Broader compiled demos or any frontend widening beyond the preserved first",
                ],
            )
            else "blocked",
            "notes": "The manuscript, bundle-status, freeze-candidate, main-text, and appendix ledgers should continue to agree.",
        },
        {
            "item_id": "release_candidate_submission_claim_and_archive_ledgers_track_current_stack",
            "status": "pass"
            if contains_all(
                release_candidate_text,
                [
                    "current `h43` docs-only useful-case refreeze",
                    "`r42-r43-r44-r45` completed semantic-boundary gate stack",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                submission_candidate_text,
                [
                    "active `h43` docs-only useful-case",
                    "completed `r42/r43/r44/r45` semantic-boundary gate stack",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                claim_ladder_text,
                [
                    "| H43 Post-R44 useful-case refreeze | validated as the current docs-only useful-case refreeze packet |",
                    "| D2 Restricted Wasm / tiny-`C` useful-case ladder |",
                    "| D1g Coequal dual-mode model lane |",
                ],
            )
            and contains_all(
                archival_manifest_text,
                [
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                    "current active docs-only packet is `h43`",
                    "completed `p27/p28` operational",
                ],
            )
            else "blocked",
            "notes": "Release-candidate, submission, claim, and archival ledgers should all expose the same current H43 release-control stack.",
        },
        {
            "item_id": "release_worktree_hygiene_snapshot_classifies_commit_state",
            "status": "pass"
            if release_commit_state_from_summary(worktree_hygiene_summary)
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and diff_check_state_from_summary(worktree_hygiene_summary) != "content_issues_present"
            and contains_all(
                worktree_hygiene_summary_text,
                [
                    '"release_commit_state":',
                    '"git_diff_check_state":',
                ],
            )
            else "blocked",
            "notes": "The worktree hygiene snapshot should classify current release-commit readiness and rule out diff-check content issues.",
        },
        {
            "item_id": "standing_audits_remain_green",
            "status": "pass"
            if ready_count_from_p1_summary(p1_summary) == 10
            and not p1_summary["blocked_or_partial_items"]
            and str(h43_summary["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43_summary["summary"]["claim_d_state"]) == "supported_here_narrowly"
            and str(h43_summary["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(r44_summary["summary"]["gate"]["lane_verdict"]) == "useful_case_surface_supported_narrowly"
            and int(r44_summary["summary"]["gate"]["exact_kernel_count"]) == 3
            and str(r45_summary["summary"]["gate"]["lane_verdict"])
            == "coequal_model_lane_supported_without_replacing_exact"
            and int(r45_summary["summary"]["gate"]["exact_mode_count"]) == 2
            and str(r43_summary["summary"]["gate"]["lane_verdict"]) == "keep_semantic_boundary_route"
            and int(r43_summary["summary"]["gate"]["exact_family_count"]) == 5
            and bool(p27_summary["summary"]["merge_executed"]) is False
            and blocked_count_from_summary(p28_summary) == 0
            and blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(p5_callout_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            and runtime_classification_from_summary(v1_timing_summary) == "healthy_but_slow"
            and timed_out_count_from_summary(v1_timing_summary) == 0
            else "blocked",
            "notes": "The current release-preflight surface depends on the landed H43/R44/R45/R43/P27/P28 stack plus the standing P5/H2 and V1 audits.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "`H43_post_r44_useful_case_refreeze`",
                "`R44_origin_restricted_wasm_useful_case_execution_gate`",
                "`R45_origin_dual_mode_model_mainline_gate`",
                "no active downstream runtime lane now follows `H43`",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "`H43_post_r44_useful_case_refreeze`",
                "`H42_post_r43_route_selection_packet`",
                "`R43_origin_bounded_memory_small_vm_execution_gate`",
                "`merge_executed = false`",
            ],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            [
                "`H43_post_r44_useful_case_refreeze`",
                "completed current semantic-boundary gate stack",
                "`P28` aligns publication-facing ledgers to landed `H43`",
            ],
        ),
        "docs/publication_record/release_preflight_checklist.md": (
            "release_preflight_text",
            [
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "results/R44_origin_restricted_wasm_useful_case_execution_gate/summary.json",
                "results/R45_origin_dual_mode_model_mainline_gate/summary.json",
                "results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json",
                "release_candidate_checklist.md",
                "claim_ladder.md",
            ],
        ),
        "docs/publication_record/release_candidate_checklist.md": (
            "release_candidate_text",
            [
                "current `H43` docs-only useful-case refreeze",
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "results/P28_post_h43_publication_surface_sync/summary.json",
            ],
        ),
        "docs/publication_record/submission_candidate_criteria.md": (
            "submission_candidate_text",
            [
                "active `H43` docs-only useful-case",
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "results/P28_post_h43_publication_surface_sync/summary.json",
            ],
        ),
        "docs/publication_record/claim_ladder.md": (
            "claim_ladder_text",
            [
                "H43 Post-R44 useful-case refreeze",
                "Restricted Wasm / tiny-`C` useful-case ladder",
                "Coequal dual-mode model lane",
            ],
        ),
        "docs/publication_record/archival_repro_manifest.md": (
            "archival_manifest_text",
            [
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "results/P28_post_h43_publication_surface_sync/summary.json",
                "The current active docs-only packet is `H43`",
            ],
        ),
        "results/release_worktree_hygiene_snapshot/summary.json": (
            "worktree_hygiene_summary_text",
            [
                '"release_commit_state":',
                '"git_diff_check_state":',
            ],
        ),
        "docs/publication_record/manuscript_bundle_draft.md": (
            "manuscript_text",
            [
                "## 1. Abstract",
                "Companion appendix material stays clearly downstream",
                "## 10. Reproducibility Appendix",
            ],
        ),
        "docs/publication_record/paper_bundle_status.md": (
            "paper_bundle_status_text",
            [
                "`H43` is the current docs-only useful-case refreeze packet",
                "`R42`, `R43`, `R44`, and `R45` are the completed current semantic-boundary",
                "`P28` aligns publication-facing ledgers to landed `H43`",
            ],
        ),
        "docs/publication_record/freeze_candidate_criteria.md": (
            "freeze_candidate_text",
            [
                "active `H43` docs-only useful-case refreeze packet",
                "results/P28_post_h43_publication_surface_sync/summary.json",
                "completed `R42/R43/R44/R45`",
            ],
        ),
        "docs/publication_record/main_text_order.md": (
            "main_text_order_text",
            [
                "## Fixed order",
                "Compiled Boundary",
                "Do not promote the full `R2` runtime matrix",
            ],
        ),
        "docs/publication_record/appendix_companion_scope.md": (
            "appendix_scope_text",
            [
                "## Required companions",
                "## Allowed optional companions",
                "## Out of scope on the current freeze candidate",
            ],
        ),
        "docs/publication_record/blog_release_rules.md": (
            "blog_rules_text",
            [
                "release_candidate_checklist.md",
                "blog stays blocked unless all of the following are true",
                "no broad “llms are computers” framing",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_active",
        "preflight_scope": "outward_release_surface_and_frozen_paper_bundle",
        "preflight_state": "docs_and_audits_green" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_hygiene_summary),
        "git_diff_check_state": diff_check_state_from_summary(worktree_hygiene_summary),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use this audit together with release_worktree_hygiene_snapshot as the outward-sync control reference while H43 remains the current active docs-only useful-case refreeze packet, H42/H41 remain the preserved prior docs-only packets, H36 remains the preserved routing/refreeze packet, R42/R43/R44/R45 remain the completed current gate stack, P27 remains the explicit merge packet with merge_executed = false, P28 remains the completed publication/control sync packet, and no_active_downstream_runtime_lane remains the current follow-on state"
            if not blocked_items
            else "resolve the blocked release-preflight items before treating outward-sync docs as stable"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs["worktree_hygiene_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "release_preflight_checklist_audit_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "release_preflight_checklist_audit_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
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
                "docs/publication_record/manuscript_bundle_draft.md",
                "docs/publication_record/paper_bundle_status.md",
                "docs/publication_record/layout_decision_log.md",
                "docs/publication_record/freeze_candidate_criteria.md",
                "docs/publication_record/main_text_order.md",
                "docs/publication_record/appendix_companion_scope.md",
                "docs/publication_record/blog_release_rules.md",
                "results/P1_paper_readiness/summary.json",
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "results/R44_origin_restricted_wasm_useful_case_execution_gate/summary.json",
                "results/R45_origin_dual_mode_model_mainline_gate/summary.json",
                "results/R43_origin_bounded_memory_small_vm_execution_gate/summary.json",
                "results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json",
                "results/P28_post_h43_publication_surface_sync/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/P5_callout_alignment/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Release Preflight Checklist Audit",
                "",
                "Machine-readable audit of whether the current outward release-facing docs,",
                "release/public ledgers, and frozen paper bundle remain aligned on the current",
                "H43 release-control stack. Current release-commit readiness is carried by the",
                "separate worktree hygiene snapshot.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
