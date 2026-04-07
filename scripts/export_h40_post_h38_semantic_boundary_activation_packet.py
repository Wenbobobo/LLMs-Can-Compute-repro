"""Export the post-H38 semantic-boundary activation packet for H40."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H40_post_h38_semantic_boundary_activation_packet"


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
        "h40_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H40_post_h38_semantic_boundary_activation_packet" / "README.md"
        ),
        "h40_status_text": read_text(
            ROOT / "docs" / "milestones" / "H40_post_h38_semantic_boundary_activation_packet" / "status.md"
        ),
        "h40_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H40_post_h38_semantic_boundary_activation_packet" / "todo.md"
        ),
        "h40_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H40_post_h38_semantic_boundary_activation_packet" / "acceptance.md"
        ),
        "h40_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H40_post_h38_semantic_boundary_activation_packet" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-h38-h40-r42-activation-design.md"),
        "f18_claim_ladder_text": read_text(
            ROOT / "docs" / "milestones" / "F18_post_h38_origin_core_long_arc_bundle" / "claim_ladder.md"
        ),
        "f19_future_gate_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F19_post_f18_restricted_wasm_useful_case_roadmap" / "future_gate_matrix.md"
        ),
        "h38_summary": read_json(ROOT / "results" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "summary.json"),
        "h36_summary": read_json(ROOT / "results" / "H36_post_r40_bounded_scalar_family_refreeze" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h38 = inputs["h38_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    return [
        {
            "item_id": "h40_docs_authorize_r42_and_preserve_h38_h36",
            "status": "pass"
            if contains_all(
                inputs["h40_readme_text"],
                [
                    "executed docs-only semantic-boundary activation packet",
                    "post-`h38` long-arc state explicitly",
                    "`authorize_r42_origin_append_only_memory_retrieval_contract_gate`",
                    "`keep_h36_freeze_and_continue_planning_only`",
                    "does not replace `h36` as the preserved active routing/refreeze packet",
                    "without reopening same-substrate `r41` by momentum",
                ],
            )
            and contains_all(
                inputs["h40_status_text"],
                [
                    "completed docs-only semantic-boundary activation packet after `f18/f19`",
                    "preserves `h38` as the prior docs-only decision packet",
                    "preserves `h36` as the active routing/refreeze packet underneath the stack",
                    "authorizes exactly `r42_origin_append_only_memory_retrieval_contract_gate`",
                ],
            )
            and contains_all(
                inputs["h40_todo_text"],
                [
                    "`authorize_r42_origin_append_only_memory_retrieval_contract_gate` versus",
                    "`keep_h36_freeze_and_continue_planning_only`",
                    "`h38` explicit as the preserved prior docs-only decision packet",
                    "`h36` explicit as the preserved active routing/refreeze packet",
                    "`r41`, `r43`, `r44`, `f11`, `r29`, and `f3` non-active here",
                ],
            )
            and contains_all(
                inputs["h40_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h38` remains visible as the preserved prior docs-only decision packet",
                    "`h36` remains the preserved active routing/refreeze packet underneath `h40`",
                    "exactly one semantic-boundary runtime gate is authorized",
                ],
            )
            else "blocked",
            "notes": "H40 should remain docs-only, preserve H38/H36, and authorize exactly R42.",
        },
        {
            "item_id": "f18_f19_and_h38_fix_the_semantic_boundary_decision_basis",
            "status": "pass"
            if str(h38["selected_outcome"]) == "keep_h36_freeze"
            and str(h36["current_active_routing_stage"]) == "h36_post_r40_bounded_scalar_family_refreeze"
            and contains_all(
                inputs["f18_claim_ladder_text"],
                [
                    "`b1`",
                    "`r42_origin_append_only_memory_retrieval_contract_gate`",
                    "`c1`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`d`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                ],
            )
            and contains_all(
                inputs["f19_future_gate_matrix_text"],
                [
                    "`r42_origin_append_only_memory_retrieval_contract_gate`",
                    "latest-write-by-address and stack-slot retrieval",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h40_post_h38_semantic_boundary_activation_packet`",
                    "`authorize_r42_origin_append_only_memory_retrieval_contract_gate`",
                    "`r42_origin_append_only_memory_retrieval_contract_gate`",
                    "later explicit post-`r42` packet",
                ],
            )
            else "blocked",
            "notes": "The decision basis should stay narrow: F18 prefers F9, F19 fixes R42 first, and H38 still preserves H36.",
        },
        {
            "item_id": "driver_and_wave_plan_promote_h40_and_record_r42",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h40_post_h38_semantic_boundary_activation_packet",
                    "r42_origin_append_only_memory_retrieval_contract_gate",
                    "h38_post_f16_runtime_relevance_reopen_decision_packet",
                    "r43_origin_bounded_memory_small_vm_execution_gate",
                    "r44_origin_restricted_wasm_useful_case_execution_gate",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h40_post_h38_semantic_boundary_activation_packet",
                    "r42_origin_append_only_memory_retrieval_contract_gate",
                    "h36_post_r40_bounded_scalar_family_refreeze",
                    "later explicit post-`r42` packet",
                ],
            )
            and contains_all(
                inputs["h40_artifact_index_text"],
                [
                    "docs/plans/2026-03-23-post-h38-h40-r42-activation-design.md",
                    "docs/milestones/h40_post_h38_semantic_boundary_activation_packet/",
                    "results/h40_post_h38_semantic_boundary_activation_packet/summary.json",
                    "docs/milestones/r42_origin_append_only_memory_retrieval_contract_gate/",
                    "results/r42_origin_append_only_memory_retrieval_contract_gate/summary.json",
                ],
            )
            else "blocked",
            "notes": "The control surfaces should treat H40 as current and R42 as the completed first semantic-boundary gate.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H40 lands the later explicit post-H38 semantic-boundary activation packet.",
            "H40 preserves H38 as the prior docs-only decision packet and H36 as the preserved routing/refreeze packet underneath the stack.",
            "H40 authorizes exactly R42 as the first semantic-boundary runtime gate.",
            "R41, R43, and R44 remain deferred behind later explicit decisions.",
        ],
        "unsupported_here": [
            "H40 does not authorize R41 by momentum.",
            "H40 does not activate R43, R44, F11, R29, or F3.",
        ],
        "disconfirmed_here": [
            "The idea that F18/F19 planning alone should activate the semantic-boundary route without a later explicit packet.",
        ],
        "distilled_result": {
            "active_stage": "h40_post_h38_semantic_boundary_activation_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h38_post_f16_runtime_relevance_reopen_decision_packet",
            "current_long_arc_planning_bundle": "f18_post_h38_origin_core_long_arc_bundle",
            "current_semantic_boundary_roadmap": "f19_post_f18_restricted_wasm_useful_case_roadmap",
            "selected_outcome": "authorize_r42_origin_append_only_memory_retrieval_contract_gate",
            "non_selected_outcome": "keep_h36_freeze_and_continue_planning_only",
            "authorized_next_runtime_candidate": "r42_origin_append_only_memory_retrieval_contract_gate",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "deferred_future_semantic_boundary_candidates": [
                "r43_origin_bounded_memory_small_vm_execution_gate",
                "r44_origin_restricted_wasm_useful_case_execution_gate",
            ],
            "decision_basis": "f18_prefers_f9_and_f19_fixes_r42_as_first_gate",
            "next_required_lane": "r42_origin_append_only_memory_retrieval_contract_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h38 = inputs["h38_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    return [
        {
            "source": "results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json",
            "fields": {
                "active_stage": h38["active_stage"],
                "selected_outcome": h38["selected_outcome"],
                "authorized_next_runtime_candidate": h38["authorized_next_runtime_candidate"],
            },
        },
        {
            "source": "docs/milestones/F18_post_h38_origin_core_long_arc_bundle/claim_ladder.md",
            "fields": {
                "preferred_forward_family": "f9_restricted_wasm_semantic_boundary",
                "same_substrate_reopen_route": "r41_only_by_later_explicit_packet",
                "merge_policy": "keep_main_unmerged_until_later_hygiene_packet",
            },
        },
        {
            "source": "docs/milestones/F19_post_f18_restricted_wasm_useful_case_roadmap/future_gate_matrix.md",
            "fields": {
                "first_semantic_boundary_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
                "downstream_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
                "useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
                "preserved_routing_stage": h36["active_stage"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h40_post_h38_semantic_boundary_activation_packet_complete",
        "active_stage": "h40_post_h38_semantic_boundary_activation_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h38_post_f16_runtime_relevance_reopen_decision_packet",
        "preserved_prior_active_routing_packet": "h36_post_r40_bounded_scalar_family_refreeze",
        "current_long_arc_planning_bundle": "f18_post_h38_origin_core_long_arc_bundle",
        "current_semantic_boundary_roadmap": "f19_post_f18_restricted_wasm_useful_case_roadmap",
        "selected_outcome": "authorize_r42_origin_append_only_memory_retrieval_contract_gate",
        "non_selected_outcome": "keep_h36_freeze_and_continue_planning_only",
        "authorized_next_runtime_candidate": "r42_origin_append_only_memory_retrieval_contract_gate",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "deferred_future_semantic_boundary_candidate_count": 2,
        "decision_basis": "f18_prefers_f9_and_f19_fixes_r42_as_first_gate",
        "next_required_lane": "r42_origin_append_only_memory_retrieval_contract_gate",
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
