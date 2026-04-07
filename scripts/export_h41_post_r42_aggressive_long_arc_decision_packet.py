"""Export the post-R42 aggressive long-arc decision packet for H41."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H41_post_r42_aggressive_long_arc_decision_packet"


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
        "h41_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H41_post_r42_aggressive_long_arc_decision_packet" / "README.md"
        ),
        "h41_status_text": read_text(
            ROOT / "docs" / "milestones" / "H41_post_r42_aggressive_long_arc_decision_packet" / "status.md"
        ),
        "h41_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H41_post_r42_aggressive_long_arc_decision_packet" / "todo.md"
        ),
        "h41_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H41_post_r42_aggressive_long_arc_decision_packet" / "acceptance.md"
        ),
        "h41_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H41_post_r42_aggressive_long_arc_decision_packet" / "artifact_index.md"
        ),
        "f20_status_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "status.md"
        ),
        "f20_evidence_boundary_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F20_post_r42_dual_mode_model_mainline_bundle"
            / "exact_model_evidence_boundary.md"
        ),
        "f20_route_order_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "downstream_route_order.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r42-f20-h41-control-override-design.md"),
        "master_plan_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r42-aggressive-long-arc-master-plan.md"),
        "h40_summary": read_json(ROOT / "results" / "H40_post_h38_semantic_boundary_activation_packet" / "summary.json"),
        "r42_summary": read_json(ROOT / "results" / "R42_origin_append_only_memory_retrieval_contract_gate" / "summary.json"),
        "f20_summary": read_json(ROOT / "results" / "F20_post_r42_dual_mode_model_mainline_bundle" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h40 = inputs["h40_summary"]["summary"]
    r42_gate = inputs["r42_summary"]["summary"]["gate"]
    f20 = inputs["f20_summary"]["summary"]
    return [
        {
            "item_id": "h41_docs_authorize_r43_and_r45_while_preserving_h40_h36_r42",
            "status": "pass"
            if contains_all(
                inputs["h41_readme_text"],
                [
                    "executed docs-only aggressive long-arc decision packet after the completed `r42` retrieval-contract gate",
                    "does not replace `h36` as the preserved active routing/refreeze packet",
                    "`authorize_r43_exact_mainline_and_coequal_r45_model_lane`",
                    "`hold_at_r42_and_continue_planning_only`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                ],
            )
            and contains_all(
                inputs["h41_status_text"],
                [
                    "completed docs-only aggressive long-arc decision packet after `r42`",
                    "preserves `h40` as the preserved prior semantic-boundary activation packet",
                    "preserves `h36` as the active routing/refreeze packet underneath the stack",
                    "preserves `r42` as the completed first semantic-boundary gate",
                    "authorizes exactly `r43_origin_bounded_memory_small_vm_execution_gate`",
                    "authorizes exactly `r45_origin_dual_mode_model_mainline_gate`",
                ],
            )
            and contains_all(
                inputs["h41_todo_text"],
                [
                    "`authorize_r43_exact_mainline_and_coequal_r45_model_lane`",
                    "`hold_at_r42_and_continue_planning_only`",
                    "keep `h40`, `h36`, and completed `r42` explicit",
                    "keep `r41`, `r44`, `f11`, `r29`, and `f3` non-active here",
                    "merge explicit through later `p27`",
                ],
            )
            and contains_all(
                inputs["h41_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h40` remains visible as the preserved prior semantic-boundary activation packet",
                    "`h36` remains the preserved active routing/refreeze packet underneath `h41`",
                    "exact `r43` is named explicitly as the next exact runtime gate",
                    "`r45` is named explicitly as a coequal model lane",
                    "`r41` remains deferred and `r44` still requires later `h42`",
                ],
            )
            else "blocked",
            "notes": "H41 should preserve H40/H36/R42 and authorize exact R43 plus coequal model R45 without activating R41/R44.",
        },
        {
            "item_id": "f20_boundary_is_visible_inside_h41_decision_basis",
            "status": "pass"
            if str(h40["selected_outcome"]) == "authorize_r42_origin_append_only_memory_retrieval_contract_gate"
            and str(r42_gate["lane_verdict"]) == "keep_semantic_boundary_route"
            and str(f20["model_mainline_posture"]) == "coequal_mainline_exact_non_substitutive"
            and contains_all(
                inputs["f20_status_text"],
                [
                    "coequal_mainline_exact_non_substitutive",
                    "`compiled_weight_executor`",
                    "`trainable_2d_executor`",
                    "keeps exact `r43` decisive",
                ],
            )
            and contains_all(
                inputs["f20_evidence_boundary_text"],
                [
                    "model-only positives cannot stand in for exact `r43`",
                    "model-only failures do not invalidate a positive exact `r43`",
                ],
            )
            and contains_all(
                inputs["f20_route_order_text"],
                [
                    "`p27_post_h41_clean_promotion_and_explicit_merge_packet`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "`h42_post_r43_route_selection_packet`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h41_post_r42_aggressive_long_arc_decision_packet`",
                    "authorize exactly `r43_origin_bounded_memory_small_vm_execution_gate`",
                    "authorize exactly `r45_origin_dual_mode_model_mainline_gate`",
                    "keep `r41` deferred",
                    "keep `r44` deferred until a later explicit `h42_post_r43_route_selection_packet`",
                ],
            )
            and contains_all(
                inputs["master_plan_text"],
                [
                    "wave 3: exact bounded-memory mainline",
                    "wave 4: dual-mode model mainline",
                    "wave 5: post-r43 route selection",
                ],
            )
            else "blocked",
            "notes": "H41 should only admit a coequal model lane because F20 already fixed the evidence boundary and downstream order.",
        },
        {
            "item_id": "driver_wave_and_plan_index_promote_h41_as_current_active_stage",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h41_post_r42_aggressive_long_arc_decision_packet",
                    "f20_post_r42_dual_mode_model_mainline_bundle",
                    "r43_origin_bounded_memory_small_vm_execution_gate",
                    "r45_origin_dual_mode_model_mainline_gate",
                    "h42_post_r43_route_selection_packet",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h41_post_r42_aggressive_long_arc_decision_packet",
                    "f20_post_r42_dual_mode_model_mainline_bundle",
                    "r43_origin_bounded_memory_small_vm_execution_gate",
                    "r45_origin_dual_mode_model_mainline_gate",
                    "p27_post_h41_clean_promotion_and_explicit_merge_packet",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r42-aggressive-long-arc-master-plan.md",
                    "2026-03-24-post-r42-f20-h41-control-override-design.md",
                ],
            )
            and contains_all(
                inputs["h41_artifact_index_text"],
                [
                    "results/h40_post_h38_semantic_boundary_activation_packet/summary.json",
                    "results/r42_origin_append_only_memory_retrieval_contract_gate/summary.json",
                    "results/f20_post_r42_dual_mode_model_mainline_bundle/summary.json",
                    "docs/publication_record/current_stage_driver.md",
                ],
            )
            else "blocked",
            "notes": "The entry surfaces should treat H41 as current, with F20 visible and P27/R43/R45/H42 properly indexed.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H41 lands the required later explicit post-R42 docs-only decision packet.",
            "H41 preserves H40/H36 and records R42 as the completed first semantic-boundary gate.",
            "H41 authorizes exact R43 as the next decisive runtime gate and admits R45 as a coequal model lane under the F20 evidence boundary.",
            "H41 keeps R41 deferred, keeps R44 behind later H42, and keeps merge explicit through P27.",
        ],
        "unsupported_here": [
            "H41 does not treat R42 as already proving bounded-memory small-VM execution.",
            "H41 does not authorize R44, arbitrary C, unrestricted Wasm, or general-computer rhetoric.",
            "H41 does not let model-only positives replace exact R43 evidence.",
        ],
        "disconfirmed_here": [
            "The idea that the post-R42 route should stay planning-only by default once an explicit aggressive-long-arc override has been selected.",
        ],
        "distilled_result": {
            "active_stage": "h41_post_r42_aggressive_long_arc_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h40_post_h38_semantic_boundary_activation_packet",
            "current_completed_retrieval_contract_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
            "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
            "selected_outcome": "authorize_r43_exact_mainline_and_coequal_r45_model_lane",
            "non_selected_outcome": "hold_at_r42_and_continue_planning_only",
            "authorized_exact_runtime_candidate": "r43_origin_bounded_memory_small_vm_execution_gate",
            "authorized_model_runtime_candidate": "r45_origin_dual_mode_model_mainline_gate",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "deferred_future_semantic_boundary_candidate": "r44_origin_restricted_wasm_useful_case_execution_gate",
            "later_explicit_followup_packet": "h42_post_r43_route_selection_packet",
            "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
            "decision_basis": "r42_positive_plus_f20_coequal_mainline_boundary",
            "next_required_lane": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h40 = inputs["h40_summary"]["summary"]
    r42_gate = inputs["r42_summary"]["summary"]["gate"]
    f20 = inputs["f20_summary"]["summary"]
    return [
        {
            "source": "results/H40_post_h38_semantic_boundary_activation_packet/summary.json",
            "fields": {
                "active_stage": h40["active_stage"],
                "selected_outcome": h40["selected_outcome"],
                "authorized_next_runtime_candidate": h40["authorized_next_runtime_candidate"],
            },
        },
        {
            "source": "results/R42_origin_append_only_memory_retrieval_contract_gate/summary.json",
            "fields": {
                "lane_verdict": r42_gate["lane_verdict"],
                "exact_task_count": r42_gate["exact_task_count"],
                "conditional_next_runtime_candidate": r42_gate["conditional_next_runtime_candidate"],
            },
        },
        {
            "source": "results/F20_post_r42_dual_mode_model_mainline_bundle/summary.json",
            "fields": {
                "active_stage": f20["active_stage"],
                "model_mainline_posture": f20["model_mainline_posture"],
                "decisive_exact_next_gate": f20["decisive_exact_next_gate"],
                "authorized_future_model_gate": f20["authorized_future_model_gate"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h41_post_r42_aggressive_long_arc_decision_packet_complete",
        "active_stage": "h41_post_r42_aggressive_long_arc_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h40_post_h38_semantic_boundary_activation_packet",
        "preserved_prior_active_routing_packet": "h36_post_r40_bounded_scalar_family_refreeze",
        "current_completed_retrieval_contract_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
        "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
        "selected_outcome": "authorize_r43_exact_mainline_and_coequal_r45_model_lane",
        "non_selected_outcome": "hold_at_r42_and_continue_planning_only",
        "authorized_exact_runtime_candidate": "r43_origin_bounded_memory_small_vm_execution_gate",
        "authorized_model_runtime_candidate": "r45_origin_dual_mode_model_mainline_gate",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "deferred_future_semantic_boundary_candidate": "r44_origin_restricted_wasm_useful_case_execution_gate",
        "later_explicit_followup_packet": "h42_post_r43_route_selection_packet",
        "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
        "decision_basis": "r42_positive_plus_f20_coequal_mainline_boundary",
        "next_required_lane": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
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
