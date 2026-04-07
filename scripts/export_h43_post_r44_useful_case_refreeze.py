"""Export the post-R44 useful-case refreeze packet for H43."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H43_post_r44_useful_case_refreeze"


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
        "h43_readme_text": read_text(ROOT / "docs" / "milestones" / "H43_post_r44_useful_case_refreeze" / "README.md"),
        "h43_status_text": read_text(ROOT / "docs" / "milestones" / "H43_post_r44_useful_case_refreeze" / "status.md"),
        "h43_todo_text": read_text(ROOT / "docs" / "milestones" / "H43_post_r44_useful_case_refreeze" / "todo.md"),
        "h43_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H43_post_r44_useful_case_refreeze" / "acceptance.md"
        ),
        "h43_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H43_post_r44_useful_case_refreeze" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r44-h43-refreeze-design.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "claim_ladder_text": read_text(
            ROOT / "docs" / "milestones" / "F18_post_h38_origin_core_long_arc_bundle" / "claim_ladder.md"
        ),
        "driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h42_summary": read_json(ROOT / "results" / "H42_post_r43_route_selection_packet" / "summary.json"),
        "r43_summary": read_json(ROOT / "results" / "R43_origin_bounded_memory_small_vm_execution_gate" / "summary.json"),
        "r44_summary": read_json(ROOT / "results" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "summary.json"),
        "r45_summary": read_json(ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
        "f20_boundary_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F20_post_r42_dual_mode_model_mainline_bundle"
            / "exact_model_evidence_boundary.md"
        ),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h42 = inputs["h42_summary"]["summary"]
    r43_gate = inputs["r43_summary"]["summary"]["gate"]
    r44_gate = inputs["r44_summary"]["summary"]["gate"]
    r45_gate = inputs["r45_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h43_docs_refreeze_r44_and_return_to_no_active_downstream_runtime_lane",
            "status": "pass"
            if contains_all(
                inputs["h43_readme_text"],
                [
                    "completed docs-only useful-case refreeze packet downstream of exact `r44`",
                    "`h42` as the preserved prior docs-only route-selection packet",
                    "`h36` as the preserved active routing/refreeze packet underneath the stack",
                    "`freeze_r44_as_narrow_supported_here`",
                    "`continue_to_broader_semantic_boundary_execution_immediately`",
                    "`reopen_deferred_runtime_or_merge_routes_after_r44`",
                ],
            )
            and contains_all(
                inputs["h43_status_text"],
                [
                    "completed docs-only useful-case refreeze packet after exact `r44`",
                    "claim `d` as `supported_here_narrowly`",
                    "completed current useful-case gate",
                    "no_active_downstream_runtime_lane",
                    "keeps `r41` deferred",
                ],
            )
            and contains_all(
                inputs["h43_todo_text"],
                [
                    "update claim `d` in the long-arc claim ladder",
                    "return the stack to `no_active_downstream_runtime_lane`",
                    "completed useful-case `r44`",
                    "`r41`, `f11`, `r29`, `f3`",
                ],
            )
            and contains_all(
                inputs["h43_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h42` remains visible as the preserved prior docs-only route-selection packet",
                    "claim `d` is updated to `supported_here_narrowly`",
                    "no active downstream runtime lane exists after `h43`",
                ],
            )
            and contains_all(
                inputs["h43_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-r44-h43-refreeze-design.md",
                    "results/r44_origin_restricted_wasm_useful_case_execution_gate/summary.json",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h43_post_r44_useful_case_refreeze`",
                    "`supported_here_narrowly`",
                    "`no_active_downstream_runtime_lane`",
                    "rejected: direct top-level doc sync only",
                ],
            )
            else "blocked",
            "notes": "H43 should interpret R44 explicitly and refreeze the stack without inventing a broader runtime successor.",
        },
        {
            "item_id": "r44_exact_r43_exact_r45_coequal_and_p27_merge_posture_justify_the_freeze",
            "status": "pass"
            if str(h42["selected_outcome"]) == "authorize_r44_origin_restricted_wasm_useful_case_execution_gate"
            and str(r43_gate["lane_verdict"]) == "keep_semantic_boundary_route"
            and int(r43_gate["exact_family_count"]) == 5
            and str(r44_gate["lane_verdict"]) == "useful_case_surface_supported_narrowly"
            and int(r44_gate["exact_kernel_count"]) == 3
            and int(r44_gate["exact_prefix_count"]) == 3
            and bool(r44_gate["article_level_substrate_evidence_exceeded_narrowly"])
            and str(r45_gate["lane_verdict"]) == "coequal_model_lane_supported_without_replacing_exact"
            and bool(p27["merge_executed"]) is False
            and contains_all(
                inputs["f20_boundary_text"],
                [
                    "model-only positives cannot stand in for exact `r43`",
                    "model-only failures do not invalidate a positive exact `r43`",
                ],
            )
            else "blocked",
            "notes": "The post-R44 freeze is only justified if exact useful-case evidence is real, exact R43 remains decisive, model evidence remains non-substitutive, and merge posture stays operational.",
        },
        {
            "item_id": "claim_ladder_and_shared_control_surfaces_promote_h43_to_current_and_r44_to_completed",
            "status": "pass"
            if contains_all(
                inputs["claim_ladder_text"],
                [
                    "| `d` | a restricted wasm / tiny-`c` lowering can run useful kernels exactly on the same append-only substrate | `supported_here_narrowly`",
                    "preserve as bounded useful-case support only until a later explicit packet selects any broader route",
                ],
            )
            and contains_all(
                inputs["driver_text"],
                [
                    "the current active stage is:",
                    "h43_post_r44_useful_case_refreeze",
                    "claim `d` is now supported_here_narrowly",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h43_post_r44_useful_case_refreeze",
                    "r44_origin_restricted_wasm_useful_case_execution_gate",
                    "no_active_downstream_runtime_lane",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r44-h43-refreeze-design.md",
                    "../milestones/h43_post_r44_useful_case_refreeze/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h43_post_r44_useful_case_refreeze/",
                    "r44_origin_restricted_wasm_useful_case_execution_gate/` — completed current restricted-wasm / tiny-`c` useful-case gate",
                ],
            )
            else "blocked",
            "notes": "The repo should clearly move from H42-authorizes-R44 to H43-refreezes-R44 as completed narrow useful-case evidence.",
        },
        {
            "item_id": "top_level_readme_status_and_claim_matrix_reflect_h43_current_and_no_further_runtime_lane",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h43_post_r44_useful_case_refreeze`",
                    "the preserved prior docs-only decision packet is `h42_post_r43_route_selection_packet`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate` is now the completed current restricted-wasm / tiny-`c` useful-case gate",
                    "no active downstream runtime lane now follows `h43`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current active docs-only decision packet is `h43_post_r44_useful_case_refreeze`",
                    "`h43_post_r44_useful_case_refreeze` is now complete as the current active docs-only useful-case refreeze packet",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate` is now complete as the current restricted useful-case gate",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h43 | the post-`r44` semantic-boundary line can be refrozen as narrow useful-case support without authorizing a broader runtime successor",
                    "validated as a docs-only packet; preserves `h42/h36`, records claim `d` as `supported_here_narrowly`, keeps `r41` deferred, and restores `no_active_downstream_runtime_lane`",
                ],
            )
            else "blocked",
            "notes": "The public control surfaces should agree that H43 is current and that R44 is completed rather than merely next.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "Exact R44 validates the fixed three-kernel restricted useful-case ladder on the same append-only substrate.",
            "Claim D is now supported_here_narrowly for bounded useful kernels only.",
            "H43 returns the stack to no_active_downstream_runtime_lane while preserving H42, H36, exact R43, and coequal R45.",
        ],
        "unsupported_here": [
            "H43 does not authorize arbitrary C, unrestricted Wasm, or general-computer rhetoric.",
            "H43 does not authorize a broader semantic-boundary runtime successor by momentum.",
            "H43 does not treat model evidence as a substitute for exact lowering.",
        ],
        "disconfirmed_here": [
            "The expectation that bounded useful-case exactness must remain planning-only after R44 completes.",
        ],
        "distilled_result": {
            "active_stage": "h43_post_r44_useful_case_refreeze",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h42_post_r43_route_selection_packet",
            "selected_outcome": "freeze_r44_as_narrow_supported_here",
            "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
            "current_completed_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
            "current_completed_coequal_model_gate": "r45_origin_dual_mode_model_mainline_gate",
            "claim_d_state": "supported_here_narrowly",
            "claim_ceiling": "bounded_useful_cases_only",
            "authorized_next_runtime_candidate": "none",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_complete",
        "active_stage": "h43_post_r44_useful_case_refreeze",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h42_post_r43_route_selection_packet",
        "selected_outcome": "freeze_r44_as_narrow_supported_here",
        "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
        "current_completed_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
        "current_completed_coequal_model_gate": "r45_origin_dual_mode_model_mainline_gate",
        "claim_d_state": "supported_here_narrowly",
        "claim_ceiling": "bounded_useful_cases_only",
        "authorized_next_runtime_candidate": "none",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
        "merge_executed": False,
        "later_explicit_packet_required_before_scope_widening": True,
        "next_required_lane": "no_active_downstream_runtime_lane",
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def build_snapshot_rows() -> list[dict[str, object]]:
    return [
        {
            "snapshot_id": "prior_route_selection_packet",
            "lane": "H42_post_r43_route_selection_packet",
            "state": "preserved_prior_docs_only_decision_packet",
        },
        {
            "snapshot_id": "exact_runtime_gate",
            "lane": "R43_origin_bounded_memory_small_vm_execution_gate",
            "state": "completed_upstream_exact_gate",
        },
        {
            "snapshot_id": "useful_case_gate",
            "lane": "R44_origin_restricted_wasm_useful_case_execution_gate",
            "state": "completed_current_useful_case_gate",
        },
        {
            "snapshot_id": "coequal_model_gate",
            "lane": "R45_origin_dual_mode_model_mainline_gate",
            "state": "completed_coequal_model_gate",
        },
        {
            "snapshot_id": "post_r44_stack_state",
            "lane": "H43_post_r44_useful_case_refreeze",
            "state": "no_active_downstream_runtime_lane",
        },
    ]


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    summary = build_summary(checklist_rows, claim_packet)
    snapshot_rows = build_snapshot_rows()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
