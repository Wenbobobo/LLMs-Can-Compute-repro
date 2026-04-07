"""Export the post-R42 dual-mode model mainline bundle for F20."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F20_post_r42_dual_mode_model_mainline_bundle"


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
        "f20_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "README.md"
        ),
        "f20_status_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "status.md"
        ),
        "f20_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "todo.md"
        ),
        "f20_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "acceptance.md"
        ),
        "f20_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "artifact_index.md"
        ),
        "coequal_mainline_posture_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "coequal_mainline_posture.md"
        ),
        "exact_model_evidence_boundary_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F20_post_r42_dual_mode_model_mainline_bundle"
            / "exact_model_evidence_boundary.md"
        ),
        "dual_mode_implementation_contract_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F20_post_r42_dual_mode_model_mainline_bundle"
            / "dual_mode_implementation_contract.md"
        ),
        "downstream_route_order_text": read_text(
            ROOT / "docs" / "milestones" / "F20_post_r42_dual_mode_model_mainline_bundle" / "downstream_route_order.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r42-f20-h41-control-override-design.md"),
        "master_plan_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r42-aggressive-long-arc-master-plan.md"),
        "h40_summary": read_json(ROOT / "results" / "H40_post_h38_semantic_boundary_activation_packet" / "summary.json"),
        "r42_summary": read_json(ROOT / "results" / "R42_origin_append_only_memory_retrieval_contract_gate" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h40 = inputs["h40_summary"]["summary"]
    r42_gate = inputs["r42_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "f20_docs_fix_coequal_mainline_without_replacing_exact_evidence",
            "status": "pass"
            if contains_all(
                inputs["f20_readme_text"],
                [
                    "planning-only coequal-mainline model bundle",
                    "`h40` as the preserved prior semantic-boundary activation packet",
                    "`r42` as the completed first semantic-boundary retrieval-contract gate",
                    "`r43` as the decisive next exact gate",
                    "`r45` as a coequal model lane",
                ],
            )
            and contains_all(
                inputs["f20_status_text"],
                [
                    "completed planning-only dual-mode model mainline bundle after `r42`",
                    "`coequal_mainline_exact_non_substitutive`",
                    "`compiled_weight_executor`",
                    "`trainable_2d_executor`",
                    "keeps exact `r43` decisive",
                ],
            )
            and contains_all(
                inputs["f20_todo_text"],
                [
                    "`coequal mainline`",
                    "exact execution evidence",
                    "`r43` explicit as the decisive next exact gate",
                    "`r45` explicit as a coequal comparator/operator lane",
                    "`r41`, `f11`, `r29`, and `f3` non-active here",
                ],
            )
            and contains_all(
                inputs["f20_acceptance_text"],
                [
                    "the bundle remains planning-only",
                    "exact evidence remains scientifically decisive",
                    "both admitted model implementations are fixed by name and role",
                    "`r45` is downstream of the exact `r43` contract surface",
                    "`r44` remains deferred",
                ],
            )
            else "blocked",
            "notes": "F20 should fix the coequal-mainline posture without turning model positives into exact evidence.",
        },
        {
            "item_id": "f20_bundle_defines_dual_mode_contract_and_downstream_order",
            "status": "pass"
            if contains_all(
                inputs["coequal_mainline_posture_text"],
                [
                    "`coequal mainline`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "does not replace exact evidence",
                ],
            )
            and contains_all(
                inputs["exact_model_evidence_boundary_text"],
                [
                    "exact `r43` evidence can directly support",
                    "model `r45` evidence can support comparator",
                    "model-only positives cannot stand in for exact `r43`",
                    "model-only failures do not invalidate a positive exact `r43`",
                ],
            )
            and contains_all(
                inputs["dual_mode_implementation_contract_text"],
                [
                    "`compiled_weight_executor`",
                    "`trainable_2d_executor`",
                    "both modes must target the same bounded task families",
                    "evaluated against exact baselines",
                ],
            )
            and contains_all(
                inputs["downstream_route_order_text"],
                [
                    "`p27_post_h41_clean_promotion_and_explicit_merge_packet`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "`h42_post_r43_route_selection_packet`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`f20_post_r42_dual_mode_model_mainline_bundle`",
                    "exact-versus-model evidence boundary",
                    "`r45` is a coequal comparator/operator lane",
                    "`r44` deferred until a later post-`r43` route-selection packet",
                ],
            )
            and contains_all(
                inputs["master_plan_text"],
                [
                    "model posture: `coequal mainline`",
                    "implementation posture: `dual mode`",
                    "`trainable_2d_executor`",
                    "`compiled_weight_executor`",
                    "wave 4: dual-mode model mainline",
                ],
            )
            else "blocked",
            "notes": "F20 must define both the model contract and the route ordering that keeps exact evidence primary.",
        },
        {
            "item_id": "driver_and_wave_plan_record_f20_inside_the_post_r42_override_stack",
            "status": "pass"
            if str(h40["active_stage"]) == "h40_post_h38_semantic_boundary_activation_packet"
            and str(r42_gate["lane_verdict"]) == "keep_semantic_boundary_route"
            and str(r42_gate["conditional_next_runtime_candidate"]) == "r43_origin_bounded_memory_small_vm_execution_gate"
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "f20_post_r42_dual_mode_model_mainline_bundle",
                    "coequal-mainline model bundle",
                    "r45_origin_dual_mode_model_mainline_gate",
                    "h41_post_r42_aggressive_long_arc_decision_packet",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "f20_post_r42_dual_mode_model_mainline_bundle",
                    "h41_post_r42_aggressive_long_arc_decision_packet",
                    "r43_origin_bounded_memory_small_vm_execution_gate",
                    "r45_origin_dual_mode_model_mainline_gate",
                    "h42_post_r43_route_selection_packet",
                ],
            )
            and contains_all(
                inputs["f20_artifact_index_text"],
                [
                    "docs/milestones/r43_origin_bounded_memory_small_vm_execution_gate/readme.md",
                    "docs/milestones/r44_origin_restricted_wasm_useful_case_execution_gate/readme.md",
                    "docs/plans/2026-03-24-post-r42-f20-h41-control-override-design.md",
                    "docs/publication_record/current_stage_driver.md",
                ],
            )
            else "blocked",
            "notes": "The control surfaces should expose F20 as the new model-mainline bundle inside the post-R42 override stack.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F20 records a coequal-mainline model posture without replacing exact evidence.",
            "F20 fixes a dual-mode model implementation contract: compiled-weight plus trainable-2D executors.",
            "F20 keeps exact R43 decisive for the bounded-memory scientific claim while preserving R45 as a coequal comparator/operator lane.",
            "F20 fixes the downstream route order so R44 still requires later H42 routing.",
        ],
        "unsupported_here": [
            "F20 does not authorize execution by itself.",
            "F20 does not let model-only positives substitute for exact R43 evidence.",
        ],
        "disconfirmed_here": [
            "The idea that model-mainline promotion alone should count as bounded-memory execution evidence without an exact gate.",
        ],
        "distilled_result": {
            "active_stage": "f20_post_r42_dual_mode_model_mainline_bundle",
            "preserved_prior_docs_only_decision_packet": "h40_post_h38_semantic_boundary_activation_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_completed_retrieval_contract_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
            "current_long_arc_planning_bundle": "f18_post_h38_origin_core_long_arc_bundle",
            "current_semantic_boundary_roadmap": "f19_post_f18_restricted_wasm_useful_case_roadmap",
            "model_mainline_posture": "coequal_mainline_exact_non_substitutive",
            "implementation_posture": "dual_mode_trainable_2d_and_compiled_weight",
            "decisive_exact_next_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
            "authorized_future_model_gate": "r45_origin_dual_mode_model_mainline_gate",
            "later_route_selection_packet": "h42_post_r43_route_selection_packet",
            "deferred_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
            "next_required_lane": "h41_post_r42_aggressive_long_arc_decision_packet",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h40 = inputs["h40_summary"]["summary"]
    r42_gate = inputs["r42_summary"]["summary"]["gate"]
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
                "active_runtime_lane": "r42_origin_append_only_memory_retrieval_contract_gate",
                "lane_verdict": r42_gate["lane_verdict"],
                "conditional_next_runtime_candidate": r42_gate["conditional_next_runtime_candidate"],
            },
        },
        {
            "source": "docs/milestones/F20_post_r42_dual_mode_model_mainline_bundle/downstream_route_order.md",
            "fields": {
                "promotion_wave": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
                "exact_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
                "model_gate": "r45_origin_dual_mode_model_mainline_gate",
                "followup_packet": "h42_post_r43_route_selection_packet",
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "f20_post_r42_dual_mode_model_mainline_bundle_complete",
        "active_stage": "f20_post_r42_dual_mode_model_mainline_bundle",
        "preserved_prior_docs_only_decision_packet": "h40_post_h38_semantic_boundary_activation_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "current_completed_retrieval_contract_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
        "current_long_arc_planning_bundle": "f18_post_h38_origin_core_long_arc_bundle",
        "current_semantic_boundary_roadmap": "f19_post_f18_restricted_wasm_useful_case_roadmap",
        "model_mainline_posture": "coequal_mainline_exact_non_substitutive",
        "implementation_posture": "dual_mode_trainable_2d_and_compiled_weight",
        "admitted_model_implementation_count": 2,
        "decisive_exact_next_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
        "authorized_future_model_gate": "r45_origin_dual_mode_model_mainline_gate",
        "later_route_selection_packet": "h42_post_r43_route_selection_packet",
        "deferred_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
        "next_required_lane": "h41_post_r42_aggressive_long_arc_decision_packet",
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
