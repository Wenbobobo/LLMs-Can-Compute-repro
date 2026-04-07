"""Export the post-R43 route-selection packet for H42."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H42_post_r43_route_selection_packet"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
        "h42_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H42_post_r43_route_selection_packet" / "README.md"
        ),
        "h42_status_text": read_text(
            ROOT / "docs" / "milestones" / "H42_post_r43_route_selection_packet" / "status.md"
        ),
        "h42_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H42_post_r43_route_selection_packet" / "todo.md"
        ),
        "h42_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H42_post_r43_route_selection_packet" / "acceptance.md"
        ),
        "h42_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H42_post_r43_route_selection_packet" / "artifact_index.md"
        ),
        "r44_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "README.md"
        ),
        "r44_status_text": read_text(
            ROOT / "docs" / "milestones" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "status.md"
        ),
        "r44_todo_text": read_text(
            ROOT / "docs" / "milestones" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "todo.md"
        ),
        "r44_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "acceptance.md"
        ),
        "r44_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "artifact_index.md"
        ),
        "f19_future_gate_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F19_post_f18_restricted_wasm_useful_case_roadmap" / "future_gate_matrix.md"
        ),
        "f20_boundary_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F20_post_r42_dual_mode_model_mainline_bundle"
            / "exact_model_evidence_boundary.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r43-h42-route-selection-design.md"),
        "h41_summary": read_json(ROOT / "results" / "H41_post_r42_aggressive_long_arc_decision_packet" / "summary.json"),
        "r43_summary": read_json(ROOT / "results" / "R43_origin_bounded_memory_small_vm_execution_gate" / "summary.json"),
        "r45_summary": read_json(ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h41 = inputs["h41_summary"]["summary"]
    r43_gate = inputs["r43_summary"]["summary"]["gate"]
    r45_gate = inputs["r45_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h42_docs_authorize_r44_while_preserving_h41_h36_r43_r45_f20_p27",
            "status": "pass"
            if contains_all(
                inputs["h42_readme_text"],
                [
                    "completed docs-only route-selection packet downstream of exact `r43` and coequal model `r45`",
                    "`h41` as the preserved prior docs-only aggressive-long-arc packet",
                    "`h36` as the preserved active routing/refreeze packet underneath the stack",
                    "`authorize_r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`hold_at_r43_and_continue_bounded_consolidation`",
                    "`keep_h41_r43_r45_state_and_continue_planning_only`",
                ],
            )
            and contains_all(
                inputs["h42_status_text"],
                [
                    "completed docs-only route-selection packet after exact `r43` and coequal model `r45`",
                    "preserves `h41` as the prior docs-only decision packet and `h36` as the active routing/refreeze packet underneath the stack",
                    "authorizes exactly `r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "keeps `r41` deferred and keeps merge explicit through `p27`",
                ],
            )
            and contains_all(
                inputs["h42_todo_text"],
                [
                    "`authorize_r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`hold_at_r43_and_continue_bounded_consolidation`",
                    "`keep_h41_r43_r45_state_and_continue_planning_only`",
                    "keep `h41`, `h36`, completed exact `r43`, completed coequal `r45`, and `f20` explicit",
                    "keep merge explicit through `p27`",
                ],
            )
            and contains_all(
                inputs["h42_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h41` remains visible as the preserved prior docs-only decision packet",
                    "`h36` remains the preserved active routing/refreeze packet underneath `h42`",
                    "exact `r43` and coequal `r45` are named explicitly as the upstream evidence basis",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                ],
            )
            else "blocked",
            "notes": "H42 should make the next useful-case lane explicit while preserving the exact/model evidence boundary and merge posture.",
        },
        {
            "item_id": "r43_r45_f19_and_p27_fix_the_narrow_decision_basis",
            "status": "pass"
            if str(h41["selected_outcome"]) == "authorize_r43_exact_mainline_and_coequal_r45_model_lane"
            and str(r43_gate["lane_verdict"]) == "keep_semantic_boundary_route"
            and int(r43_gate["exact_family_count"]) == 5
            and int(r43_gate["exact_core_family_count"]) == 4
            and bool(r43_gate["optional_call_family_exact"])
            and str(r45_gate["lane_verdict"]) == "coequal_model_lane_supported_without_replacing_exact"
            and int(r45_gate["exact_mode_count"]) == 2
            and int(r45_gate["exact_family_mode_row_count"]) == 10
            and bool(r45_gate["trainable_heldout_family_exact"])
            and bool(r45_gate["exact_r43_dependency_satisfied"])
            and bool(p27["merge_executed"]) is False
            and contains_all(
                inputs["f19_future_gate_matrix_text"],
                [
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "validate restricted wasm / tiny-`c` useful kernels on the same substrate",
                    "`r43` positive and the surface in `restricted_wasm_surface.md` still holds",
                ],
            )
            and contains_all(
                inputs["f20_boundary_text"],
                [
                    "exact `r43` evidence can directly support the bounded-memory small-vm claim",
                    "model-only positives cannot stand in for exact `r43`",
                    "model-only failures do not invalidate a positive exact `r43`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h42_post_r43_route_selection_packet`",
                    "authorize exactly `r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "hold at `r43` while strengthening bounded kernels",
                    "freeze again and continue planning-only work",
                    "`merge_executed = false`",
                ],
            )
            else "blocked",
            "notes": "H42 should only authorize R44 because F19 fixed the ladder, R43 stayed exact, R45 stayed coequal, and P27 still keeps merge posture operational rather than scientific.",
        },
        {
            "item_id": "driver_wave_plan_and_r44_surface_promote_h42_as_current_and_r44_as_next",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "h42_post_r43_route_selection_packet",
                    "selected_outcome = authorize_r44_origin_restricted_wasm_useful_case_execution_gate",
                    "the next required order is now:",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h42_post_r43_route_selection_packet",
                    "r44_origin_restricted_wasm_useful_case_execution_gate",
                    "authorize `r44` as the next exact useful-case gate",
                    "current active wave is now `r44` preparation",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r43-h42-route-selection-design.md",
                    "../milestones/h42_post_r43_route_selection_packet/",
                    "../milestones/r44_origin_restricted_wasm_useful_case_execution_gate/",
                ],
            )
            and contains_all(
                inputs["r44_readme_text"],
                [
                    "authorized next restricted-wasm / tiny-`c` useful-case gate after completed `h42`",
                    "`h42` as the current active docs-only route-selection packet",
                    "`r43` as the required upstream exact bounded-memory execution gate",
                    "`r45` as a coequal comparator lane that does not replace exact evidence",
                ],
            )
            and contains_all(
                inputs["r44_status_text"],
                [
                    "authorized next restricted-wasm / tiny-`c` useful-case execution gate after completed `h42`",
                    "still requires exact `r43` to remain the decisive upstream evidence",
                    "keeps any trainable or translated variant comparator-only until exact lowering survives",
                ],
            )
            and contains_all(
                inputs["r44_acceptance_text"],
                [
                    "kernel suite and order are fixed before execution",
                    "authorized by completed `h42`",
                ],
            )
            and contains_all(
                inputs["r44_artifact_index_text"],
                [
                    "docs/milestones/h42_post_r43_route_selection_packet/readme.md",
                    "results/h42_post_r43_route_selection_packet/summary.json",
                ],
            )
            and contains_all(
                inputs["h42_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-r43-h42-route-selection-design.md",
                    "results/h42_post_r43_route_selection_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "The public control surfaces should treat H42 as current and R44 as the next required exact useful-case lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H42 lands the later explicit post-R43 route-selection packet as a completed docs-only control artifact.",
            "H42 preserves H41 as the prior docs-only packet, H36 as the routing/refreeze packet underneath the stack, and F20 as the exact-versus-model evidence boundary.",
            "H42 authorizes exactly R44 as the next exact restricted useful-case gate.",
            "H42 keeps R41 deferred, keeps merge explicit through P27, and does not let model evidence replace exact R43.",
        ],
        "unsupported_here": [
            "H42 does not authorize arbitrary C, unrestricted Wasm, or general LLM-computer rhetoric.",
            "H42 does not reactivate same-substrate R41 by momentum.",
            "H42 does not treat merge execution as part of the scientific claim surface.",
        ],
        "disconfirmed_here": [
            "The idea that the post-R43 stack should remain planning-only despite exact R43 plus coequal R45 on the fixed bounded family.",
        ],
        "distilled_result": {
            "active_stage": "h42_post_r43_route_selection_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h41_post_r42_aggressive_long_arc_decision_packet",
            "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
            "current_completed_coequal_model_gate": "r45_origin_dual_mode_model_mainline_gate",
            "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
            "selected_outcome": "authorize_r44_origin_restricted_wasm_useful_case_execution_gate",
            "non_selected_outcomes": [
                "hold_at_r43_and_continue_bounded_consolidation",
                "keep_h41_r43_r45_state_and_continue_planning_only",
            ],
            "authorized_next_runtime_candidate": "r44_origin_restricted_wasm_useful_case_execution_gate",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
            "decision_basis": "r43_exact_positive_plus_r45_coequal_support_plus_f19_useful_case_ladder",
            "merge_executed": False,
            "next_required_lane": "r44_origin_restricted_wasm_useful_case_execution_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h41 = inputs["h41_summary"]["summary"]
    r43_gate = inputs["r43_summary"]["summary"]["gate"]
    r45_gate = inputs["r45_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "source": "results/H41_post_r42_aggressive_long_arc_decision_packet/summary.json",
            "fields": {
                "active_stage": h41["active_stage"],
                "selected_outcome": h41["selected_outcome"],
                "authorized_exact_runtime_candidate": h41["authorized_exact_runtime_candidate"],
                "authorized_model_runtime_candidate": h41["authorized_model_runtime_candidate"],
            },
        },
        {
            "source": "results/R43_origin_bounded_memory_small_vm_execution_gate/summary.json",
            "fields": {
                "lane_verdict": r43_gate["lane_verdict"],
                "exact_family_count": r43_gate["exact_family_count"],
                "optional_call_family_exact": r43_gate["optional_call_family_exact"],
                "later_explicit_followup_packet": r43_gate["later_explicit_followup_packet"],
            },
        },
        {
            "source": "results/R45_origin_dual_mode_model_mainline_gate/summary.json",
            "fields": {
                "lane_verdict": r45_gate["lane_verdict"],
                "exact_mode_count": r45_gate["exact_mode_count"],
                "exact_family_mode_row_count": r45_gate["exact_family_mode_row_count"],
                "conditional_useful_case_candidate": r45_gate["conditional_useful_case_candidate"],
            },
        },
        {
            "source": "results/P27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json",
            "fields": {
                "promotion_mode": p27["promotion_mode"],
                "merge_recommended": p27["merge_recommended"],
                "merge_executed": p27["merge_executed"],
                "target_branch": p27["target_branch"],
            },
        },
        {
            "source": "docs/milestones/F19_post_f18_restricted_wasm_useful_case_roadmap/future_gate_matrix.md",
            "fields": {
                "first_semantic_boundary_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
                "bounded_memory_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
                "authorized_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h42_post_r43_route_selection_packet_complete",
        "active_stage": "h42_post_r43_route_selection_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h41_post_r42_aggressive_long_arc_decision_packet",
        "preserved_prior_active_routing_packet": "h36_post_r40_bounded_scalar_family_refreeze",
        "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
        "current_completed_coequal_model_gate": "r45_origin_dual_mode_model_mainline_gate",
        "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
        "selected_outcome": "authorize_r44_origin_restricted_wasm_useful_case_execution_gate",
        "non_selected_outcome": "hold_at_r43_and_continue_bounded_consolidation",
        "secondary_non_selected_outcome": "keep_h41_r43_r45_state_and_continue_planning_only",
        "authorized_next_runtime_candidate": "r44_origin_restricted_wasm_useful_case_execution_gate",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
        "decision_basis": "r43_exact_positive_plus_r45_coequal_support_plus_f19_useful_case_ladder",
        "merge_executed": False,
        "next_required_lane": "r44_origin_restricted_wasm_useful_case_execution_gate",
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
