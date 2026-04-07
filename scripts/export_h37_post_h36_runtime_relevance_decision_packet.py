"""Export the post-H36 runtime-relevance decision packet for H37."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H37_post_h36_runtime_relevance_decision_packet"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    return {
        "h37_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H37_post_h36_runtime_relevance_decision_packet" / "README.md"
        ),
        "h37_status_text": read_text(
            ROOT / "docs" / "milestones" / "H37_post_h36_runtime_relevance_decision_packet" / "status.md"
        ),
        "h37_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H37_post_h36_runtime_relevance_decision_packet" / "todo.md"
        ),
        "h37_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H37_post_h36_runtime_relevance_decision_packet" / "acceptance.md"
        ),
        "h37_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H37_post_h36_runtime_relevance_decision_packet" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-h36-p25-f15-h37-control-design.md"),
        "r41_design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-23-post-h36-r41-runtime-relevance-threat-design.md"
        ),
        "f14_threat_model_text": read_text(
            ROOT / "docs" / "milestones" / "F14_post_f13_conditional_reopen_readiness_bundle" / "threat_model.md"
        ),
        "f15_status_text": read_text(
            ROOT / "docs" / "milestones" / "F15_post_h36_origin_goal_reanchor_bundle" / "status.md"
        ),
        "f15_claim_delta_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F15_post_h36_origin_goal_reanchor_bundle" / "claim_delta_matrix.md"
        ),
        "f15_scientific_goal_stack_text": read_text(
            ROOT / "docs" / "milestones" / "F15_post_h36_origin_goal_reanchor_bundle" / "scientific_goal_stack.md"
        ),
        "f15_repro_gap_ladder_text": read_text(
            ROOT / "docs" / "milestones" / "F15_post_h36_origin_goal_reanchor_bundle" / "repro_gap_ladder.md"
        ),
        "p25_summary": read_json(ROOT / "results" / "P25_post_h36_clean_promotion_prep" / "summary.json"),
        "h36_summary": read_json(ROOT / "results" / "H36_post_r40_bounded_scalar_family_refreeze" / "summary.json"),
        "r40_summary": read_json(ROOT / "results" / "R40_origin_bounded_scalar_locals_and_flags_gate" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    p25 = inputs["p25_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    r40_gate = inputs["r40_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h37_docs_select_keep_h36_freeze_and_leave_no_active_runtime_lane",
            "status": "pass"
            if contains_all(
                inputs["h37_readme_text"],
                [
                    "executed docs-only decision packet",
                    "does not replace `h36` as the preserved active routing/refreeze packet",
                    "`keep_h36_freeze`",
                    "`authorize_r41_origin_runtime_relevance_threat_stress_audit`",
                    "named future runtime candidate on the selected branch: none",
                ],
            )
            and contains_all(
                inputs["h37_status_text"],
                [
                    "completed docs-only runtime-relevance decision packet",
                    "preserves `h36` as the preserved prior active routing/refreeze packet",
                    "selects `keep_h36_freeze`",
                    "names no active runtime candidate",
                ],
            )
            and contains_all(
                inputs["h37_todo_text"],
                [
                    "`keep_h36_freeze` versus",
                    "`authorize_r41_origin_runtime_relevance_threat_stress_audit`",
                    "no uniquely isolated admissible candidate currently survives on the fixed landed `r40` row pair",
                    "require a later explicit packet",
                ],
            )
            and contains_all(
                inputs["h37_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h36` remains the preserved prior active routing/refreeze packet",
                    "no active downstream runtime lane exists after `h37`",
                    "a future `r41` activation still requires a later explicit packet",
                ],
            )
            and contains_all(
                inputs["h37_artifact_index_text"],
                [
                    "docs/milestones/p25_post_h36_clean_promotion_prep/",
                    "docs/milestones/f15_post_h36_origin_goal_reanchor_bundle/",
                    "results/h36_post_r40_bounded_scalar_family_refreeze/summary.json",
                    "results/r40_origin_bounded_scalar_locals_and_flags_gate/summary.json",
                ],
            )
            else "blocked",
            "notes": "H37 should remain docs-only, preserve H36 as the routing top, and select keep_h36_freeze rather than reopen by momentum.",
        },
        {
            "item_id": "f15_f14_p25_and_saved_r41_design_support_keep_freeze_decision_basis",
            "status": "pass"
            if str(p25["promotion_mode"]) == "prepare_only"
            and bool(p25["merge_authorized"]) is False
            and contains_all(
                inputs["f14_threat_model_text"],
                [
                    "runtime_irrelevance_via_compiler_helper_overencoding",
                    "fast_path_only_helps_the_easy_part",
                    "only two same-substrate threat families remain active here",
                ],
            )
            and contains_all(
                inputs["f15_status_text"],
                [
                    "replaces `f12` as the current canonical derivative claim-delta surface",
                    "bounded scalar locals and typed flags as `supported_here` narrowly",
                    "two surviving `f14` runtime-relevance cautions as the top unresolved same-substrate scientific gaps",
                    "does not authorize `r41` by itself",
                ],
            )
            and contains_all(
                inputs["f15_claim_delta_matrix_text"],
                [
                    "the next scientifically honest step is a contradiction-led runtime-relevance decision on the fixed landed `r40` row pair",
                    "`planning_only`",
                    "general llm has become a computer",
                    "`blocked_by_scope`",
                ],
            )
            and contains_all(
                inputs["f15_scientific_goal_stack_text"],
                [
                    "layer 4",
                    "planning_only",
                    "saved `r41` design, and `h37`",
                    "layers 5 through 7 remain blocked or require a new substrate",
                ],
            )
            and contains_all(
                inputs["f15_repro_gap_ladder_text"],
                [
                    "runtime_irrelevance_via_compiler_helper_overencoding",
                    "fast_path_only_helps_the_easy_part",
                    "planning_only_under_h37_keep_freeze",
                    "do not skip ranks 1 and 2 by momentum",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "the default is `keep_h36_freeze`",
                    "if no uniquely isolated admissible candidate exists, `h37` must keep the freeze and leave `r41` deferred",
                ],
            )
            and contains_all(
                inputs["r41_design_text"],
                [
                    "allowed future verdicts",
                    "`keep_h36_freeze`",
                    "`runtime_relevance_threat_isolated`",
                    "the future audit should also stop after the first uniquely isolated contradiction",
                ],
            )
            else "blocked",
            "notes": "The keep-freeze choice is only justified if F15 preserves the same narrow goal stack, F14 limits the threat set to two families, P25 stays operational-only, and the saved R41 design still requires later explicit authorization.",
        },
        {
            "item_id": "h36_r40_driver_and_wave_keep_r41_deferred_without_broader_scope_lift",
            "status": "pass"
            if str(h36["current_active_routing_stage"]) == "h36_post_r40_bounded_scalar_family_refreeze"
            and str(h36["authorized_next_runtime_candidate"]) == "none"
            and str(h36["deferred_future_runtime_candidate"]) == "r41_origin_runtime_relevance_threat_stress_audit"
            and str(h36["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(r40_gate["lane_verdict"]) == "origin_bounded_scalar_locals_and_flags_supported_narrowly"
            and str(r40_gate["admitted_program_name"]) == "bytecode_bounded_scalar_flag_loop_6_a320"
            and str(r40_gate["boundary_program_name"]) == "bytecode_bounded_scalar_flag_loop_long_12_a336"
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h37_post_h36_runtime_relevance_decision_packet",
                    "selected_outcome = keep_h36_freeze",
                    "authorized_next_runtime_candidate = none",
                    "decision_basis = no_uniquely_isolated_admissible_candidate_on_fixed_r40_row_pair",
                    "next_required_lane = no_active_downstream_runtime_lane",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h37_post_h36_runtime_relevance_decision_packet",
                    "r41_origin_runtime_relevance_threat_stress_audit",
                    "preserved prior docs-only runtime-relevance decision packet",
                    "no_active_downstream_runtime_lane",
                    "keep_h36_freeze",
                ],
            )
            else "blocked",
            "notes": "H37 should remain reproducible as the preserved prior post-H36 decision packet and keep R41 deferred without reopening blocked same-endpoint, scope-lift, or frontier lanes.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H37 lands the required post-H36 docs-only runtime-relevance decision packet.",
            "H36 remains the preserved prior active routing/refreeze packet after H37 lands.",
            "The selected outcome is `keep_h36_freeze`, so no active downstream runtime lane exists after H37.",
            "R41 remains deferred because no uniquely isolated admissible candidate currently survives on the fixed landed R40 row pair.",
        ],
        "unsupported_here": [
            "H37 does not authorize R41 execution by wording alone.",
            "H37 does not reopen R29, F3, frontier review, restricted-Wasm widening, hybrid work, or general-computer rhetoric.",
        ],
        "disconfirmed_here": [
            "The expectation that the existence of a saved R41 design or surviving F14 cautions is enough to reopen the runtime lane automatically after H36.",
        ],
        "distilled_result": {
            "active_stage": "h37_post_h36_runtime_relevance_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "selected_outcome": "keep_h36_freeze",
            "non_selected_outcome": "authorize_r41_origin_runtime_relevance_threat_stress_audit",
            "authorized_next_runtime_candidate": "none",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "decision_basis": "no_uniquely_isolated_admissible_candidate_on_fixed_r40_row_pair",
            "remaining_runtime_relevance_threats": [
                "runtime_irrelevance_via_compiler_helper_overencoding",
                "fast_path_only_helps_the_easy_part",
            ],
            "blocked_future_lanes": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
            "future_frontier_review_state": "planning_only_f2_preserved",
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    p25 = inputs["p25_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    r40_gate = inputs["r40_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/P25_post_h36_clean_promotion_prep/summary.json",
            "fields": {
                "source_of_truth_branch": p25["source_of_truth_branch"],
                "clean_prep_branch": p25["clean_prep_branch"],
                "promotion_mode": p25["promotion_mode"],
                "merge_authorized": p25["merge_authorized"],
            },
        },
        {
            "source": "results/H36_post_r40_bounded_scalar_family_refreeze/summary.json",
            "fields": {
                "active_stage": h36["active_stage"],
                "decision_state": h36["decision_state"],
                "deferred_future_runtime_candidate": h36["deferred_future_runtime_candidate"],
                "next_required_lane": h36["next_required_lane"],
            },
        },
        {
            "source": "results/R40_origin_bounded_scalar_locals_and_flags_gate/summary.json",
            "fields": {
                "lane_verdict": r40_gate["lane_verdict"],
                "admitted_program_name": r40_gate["admitted_program_name"],
                "boundary_program_name": r40_gate["boundary_program_name"],
                "next_priority_lane": r40_gate["next_priority_lane"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h37_post_h36_runtime_relevance_decision_packet_complete",
        "active_stage": "h37_post_h36_runtime_relevance_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_active_routing_packet": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_operational_prep_lane": "p25_post_h36_clean_promotion_prep",
        "preserved_current_derivative_bundle": "f15_post_h36_origin_goal_reanchor_bundle",
        "selected_outcome": "keep_h36_freeze",
        "non_selected_outcome": "authorize_r41_origin_runtime_relevance_threat_stress_audit",
        "authorized_next_runtime_candidate": "none",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "decision_basis": "no_uniquely_isolated_admissible_candidate_on_fixed_r40_row_pair",
        "remaining_runtime_relevance_threat_count": 2,
        "remaining_runtime_relevance_threats": [
            "runtime_irrelevance_via_compiler_helper_overencoding",
            "fast_path_only_helps_the_easy_part",
        ],
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "future_frontier_review_state": "planning_only_f2_preserved",
        "next_required_lane": "no_active_downstream_runtime_lane",
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
