"""Export the post-H32 conditional next-question packet for H33."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H33_post_h32_conditional_next_question_packet"


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
        "h33_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H33_post_h32_conditional_next_question_packet" / "README.md"
        ),
        "h33_status_text": read_text(
            ROOT / "docs" / "milestones" / "H33_post_h32_conditional_next_question_packet" / "status.md"
        ),
        "h33_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H33_post_h32_conditional_next_question_packet" / "todo.md"
        ),
        "h33_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H33_post_h32_conditional_next_question_packet" / "acceptance.md"
        ),
        "h33_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H33_post_h32_conditional_next_question_packet" / "artifact_index.md"
        ),
        "post_h32_plan_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-h32-conditional-next-packet-design.md"),
        "r39_plan_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-23-post-h33-r39-origin-core-substrate-question-design.md"
        ),
        "r39_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R39_origin_compiler_control_surface_dependency_audit" / "README.md"
        ),
        "r39_status_text": read_text(
            ROOT / "docs" / "milestones" / "R39_origin_compiler_control_surface_dependency_audit" / "status.md"
        ),
        "r39_todo_text": read_text(
            ROOT / "docs" / "milestones" / "R39_origin_compiler_control_surface_dependency_audit" / "todo.md"
        ),
        "r39_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R39_origin_compiler_control_surface_dependency_audit" / "acceptance.md"
        ),
        "r39_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "R39_origin_compiler_control_surface_dependency_audit" / "artifact_index.md"
        ),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "f2_activation_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F2_future_frontier_recheck_activation_matrix" / "activation_matrix.md"
        ),
        "h32_summary": read_json(ROOT / "results" / "H32_post_r38_compiled_boundary_refreeze" / "summary.json"),
        "r38_summary": read_json(ROOT / "results" / "R38_origin_compiler_control_surface_extension_gate" / "summary.json"),
        "h31_summary": read_json(ROOT / "results" / "H31_post_h30_later_explicit_boundary_decision_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h32 = inputs["h32_summary"]["summary"]
    r38_gate = inputs["r38_summary"]["summary"]["gate"]
    h31 = inputs["h31_summary"]["summary"]
    return [
        {
            "item_id": "h33_docs_select_one_explicit_post_h32_outcome_and_keep_h32_active",
            "status": "pass"
            if contains_all(
                inputs["h33_readme_text"],
                [
                    "executed docs-only conditional packet",
                    "authorize_one_origin_core_substrate_question",
                    "h32",
                    "r39_origin_compiler_control_surface_dependency_audit",
                ],
            )
            and contains_all(
                inputs["h33_status_text"],
                [
                    "completed docs-only conditional next-question packet",
                    "h32",
                    "authorize_one_origin_core_substrate_question",
                    "r39_origin_compiler_control_surface_dependency_audit",
                ],
            )
            and contains_all(
                inputs["h33_todo_text"],
                ["freeze_compiled_boundary_as_complete_for_now", "authorize_one_origin_core_substrate_question", "r39", "r29", "f3"],
            )
            and contains_all(
                inputs["h33_acceptance_text"],
                ["docs-only", "h32", "r39_origin_compiler_control_surface_dependency_audit"],
            )
            and contains_all(
                inputs["h33_artifact_index_text"],
                [
                    "results/h33_post_h32_conditional_next_question_packet/summary.json",
                    "docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md",
                    "docs/milestones/r39_origin_compiler_control_surface_dependency_audit/",
                ],
            )
            else "blocked",
            "notes": "H33 should formalize the post-H32 fork, keep H32 active, and select exactly one narrow next-question outcome.",
        },
        {
            "item_id": "upstream_h32_and_post_h32_plan_require_an_explicit_new_question_packet",
            "status": "pass"
            if str(h32["active_stage"]) == "h32_post_r38_compiled_boundary_refreeze"
            and str(h32["decision_state"]) == "origin_core_one_richer_compiled_control_family_refrozen"
            and str(h32["next_required_lane"]) == "new_plan_required_before_any_further_compiled_boundary_or_scope_lift"
            and str(r38_gate["lane_verdict"]) == "origin_compiler_control_surface_extension_supported_narrowly"
            and str(h31["authorization_outcome"]) == "execute_one_more_tiny_extension"
            and contains_all(
                inputs["post_h32_plan_text"],
                [
                    "h33_post_h32_conditional_next_question_packet",
                    "freeze_compiled_boundary_as_complete_for_now",
                    "authorize_one_origin_core_substrate_question",
                    "r39_origin_compiler_control_surface_dependency_audit",
                ],
            )
            else "blocked",
            "notes": "H33 is only justified if H32 still ends at a new-plan-required state and the saved post-H32 design narrows the next question explicitly.",
        },
        {
            "item_id": "r39_candidate_stays_same_substrate_same_opcode_and_no_widening",
            "status": "pass"
            if contains_all(
                inputs["r39_plan_text"],
                [
                    "same opcode surface as `r37` and `r38`",
                    "no new opcode",
                    "no new hidden host evaluator",
                    "no new program-family breadth",
                    "subroutine_braid_program(6, base_address=80)",
                    "subroutine_braid_long_program(12, base_address=160)",
                ],
            )
            and contains_all(
                inputs["r39_readme_text"],
                ["same opcode surface", "r37/r38", "current origin-core substrate fixed"],
            )
            and contains_all(
                inputs["r39_status_text"],
                ["planning-only", "same opcode surface", "current active routing/refreeze packet"],
            )
            and contains_all(
                inputs["r39_todo_text"],
                ["new opcode", "hidden host evaluator", "new program-family breadth"],
            )
            and contains_all(
                inputs["r39_acceptance_text"],
                ["same-substrate and same-opcode", "exact trace", "exact final-state"],
            )
            and contains_all(
                inputs["r39_artifact_index_text"],
                [
                    "docs/plans/2026-03-23-post-h33-r39-origin-core-substrate-question-design.md",
                    "results/h33_post_h32_conditional_next_question_packet/summary.json",
                    "results/h32_post_r38_compiled_boundary_refreeze/summary.json",
                ],
            )
            else "blocked",
            "notes": "The only lane named by H33 must remain a same-substrate audit, not a backdoor widening packet.",
        },
        {
            "item_id": "driver_active_wave_and_f2_preserve_h32_routing_h33_control_and_r39_as_next_candidate",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h32_post_r38_compiled_boundary_refreeze",
                    "h33_post_h32_conditional_next_question_packet",
                    "authorize_one_origin_core_substrate_question",
                    "r39_origin_compiler_control_surface_dependency_audit",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h32_post_r38_compiled_boundary_refreeze",
                    "h33_post_h32_conditional_next_question_packet",
                    "r39_origin_compiler_control_surface_dependency_audit",
                ],
            )
            and contains_all(
                inputs["f2_activation_matrix_text"],
                [
                    "isolates one narrow same-substrate question",
                    "r39_origin_compiler_control_surface_dependency_audit",
                    "must stay downstream",
                ],
            )
            else "blocked",
            "notes": "Project entrypoints should show that H32 stays active, H33 is the current docs-only control packet, and R39 is the only named next candidate.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H33 lands the post-H32 question-selection packet as docs-only control rather than new runtime evidence.",
            "H32 remains the current active routing/refreeze packet after H33 lands.",
            "The selected outcome is `authorize_one_origin_core_substrate_question`, not automatic freeze or automatic widening.",
            "R39 is the only future runtime candidate named here, and it stays same-substrate and same-opcode by contract.",
        ],
        "unsupported_here": [
            "H33 does not execute R39.",
            "H33 does not authorize arbitrary `C`, broader Wasm/compiler support, or a general LLM-computer claim.",
            "H33 does not reopen same-endpoint systems recovery, frontier review, or scope lift.",
        ],
        "disconfirmed_here": [
            "The expectation that post-H32 work should continue by automatic broader compiled-family momentum rather than one explicit new question packet.",
        ],
        "distilled_result": {
            "active_stage": "h33_post_h32_conditional_next_question_packet",
            "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
            "decision_state": "one_origin_core_substrate_question_authorized_docs_only",
            "selected_outcome": "authorize_one_origin_core_substrate_question",
            "authorized_next_runtime_candidate": "r39_origin_compiler_control_surface_dependency_audit",
            "authorized_runtime_scope": "same_substrate_same_opcode_same_admitted_and_boundary_rows_only",
            "blocked_lanes_preserved": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
            "future_frontier_review_state": "planning_only_f2_preserved",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h32 = inputs["h32_summary"]["summary"]
    h31 = inputs["h31_summary"]["summary"]
    r38_gate = inputs["r38_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H32_post_r38_compiled_boundary_refreeze/summary.json",
            "fields": {
                "active_stage": h32["active_stage"],
                "decision_state": h32["decision_state"],
                "compiled_boundary_state": h32["compiled_boundary_state"],
                "next_required_lane": h32["next_required_lane"],
            },
        },
        {
            "source": "results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json",
            "fields": {
                "authorization_outcome": h31["authorization_outcome"],
                "admitted_extension_case": h31["admitted_extension_case"],
                "boundary_probe_case": h31["boundary_probe_case"],
            },
        },
        {
            "source": "results/R38_origin_compiler_control_surface_extension_gate/summary.json",
            "fields": {
                "lane_verdict": r38_gate["lane_verdict"],
                "admitted_case_count": r38_gate["admitted_case_count"],
                "boundary_stress_case_count": r38_gate["boundary_stress_case_count"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h33_post_h32_conditional_next_question_packet_complete",
        "active_stage": "h33_post_h32_conditional_next_question_packet",
        "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
        "decision_state": "one_origin_core_substrate_question_authorized_docs_only",
        "selected_outcome": "authorize_one_origin_core_substrate_question",
        "authorized_next_runtime_candidate": "r39_origin_compiler_control_surface_dependency_audit",
        "authorized_runtime_scope": "same_substrate_same_opcode_same_admitted_and_boundary_rows_only",
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "future_frontier_review_state": "planning_only_f2_preserved",
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
