"""Export the post-R39 later explicit scope decision packet for H34."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H34_post_r39_later_explicit_scope_decision_packet"


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
        "h34_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H34_post_r39_later_explicit_scope_decision_packet" / "README.md"
        ),
        "h34_status_text": read_text(
            ROOT / "docs" / "milestones" / "H34_post_r39_later_explicit_scope_decision_packet" / "status.md"
        ),
        "h34_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H34_post_r39_later_explicit_scope_decision_packet" / "todo.md"
        ),
        "h34_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H34_post_r39_later_explicit_scope_decision_packet" / "acceptance.md"
        ),
        "h34_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H34_post_r39_later_explicit_scope_decision_packet" / "artifact_index.md"
        ),
        "post_r39_plan_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-23-post-r39-later-explicit-scope-decision-design.md"
        ),
        "h33_summary": read_json(ROOT / "results" / "H33_post_h32_conditional_next_question_packet" / "summary.json"),
        "r39_summary": read_json(ROOT / "results" / "R39_origin_compiler_control_surface_dependency_audit" / "summary.json"),
        "h32_summary": read_json(ROOT / "results" / "H32_post_r38_compiled_boundary_refreeze" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "f2_activation_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F2_future_frontier_recheck_activation_matrix" / "activation_matrix.md"
        ),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h33 = inputs["h33_summary"]["summary"]
    r39_gate = inputs["r39_summary"]["summary"]["gate"]
    h32 = inputs["h32_summary"]["summary"]
    return [
        {
            "item_id": "h34_docs_select_freeze_outcome_and_keep_h32_active",
            "status": "pass"
            if contains_all(
                inputs["h34_readme_text"],
                [
                    "executed docs-only later explicit packet",
                    "freeze_compiled_boundary_as_complete_for_now",
                    "authorize_one_more_origin_core_substrate_question",
                    "named future runtime candidate: none",
                    "h32",
                ],
            )
            and contains_all(
                inputs["h34_status_text"],
                [
                    "completed docs-only later explicit interpretation packet",
                    "h32",
                    "freeze_compiled_boundary_as_complete_for_now",
                    "no new runtime candidate",
                ],
            )
            and contains_all(
                inputs["h34_todo_text"],
                [
                    "freeze_compiled_boundary_as_complete_for_now",
                    "authorize_one_more_origin_core_substrate_question",
                    "new contradiction- or sharper-gap-driven explicit packet",
                    "r29",
                    "f3",
                ],
            )
            and contains_all(
                inputs["h34_acceptance_text"],
                ["docs-only", "the current active routing packet remains `h32`", "no future runtime lane is named"],
            )
            and contains_all(
                inputs["h34_artifact_index_text"],
                [
                    "docs/plans/2026-03-23-post-r39-later-explicit-scope-decision-design.md",
                    "results/h34_post_r39_later_explicit_scope_decision_packet/summary.json",
                    "results/r39_origin_compiler_control_surface_dependency_audit/summary.json",
                ],
            )
            else "blocked",
            "notes": "H34 should remain docs-only, keep H32 active, and select freeze-complete-for-now rather than a new runtime lane.",
        },
        {
            "item_id": "upstream_h33_and_r39_support_freeze_not_automatic_reopen",
            "status": "pass"
            if str(h33["selected_outcome"]) == "authorize_one_origin_core_substrate_question"
            and str(h33["authorized_next_runtime_candidate"]) == "r39_origin_compiler_control_surface_dependency_audit"
            and str(r39_gate["lane_verdict"]) == "control_surface_dependence_not_detected_on_declared_permutation"
            and str(r39_gate["next_priority_lane"]) == "later_explicit_post_r39_decision_packet_required"
            and str(h32["active_stage"]) == "h32_post_r38_compiled_boundary_refreeze"
            and str(h32["next_required_lane"]) == "new_plan_required_before_any_further_compiled_boundary_or_scope_lift"
            and contains_all(
                inputs["post_r39_plan_text"],
                [
                    "freeze_compiled_boundary_as_complete_for_now",
                    "authorize_one_more_origin_core_substrate_question",
                    "one declared helper-body permutation with target renumbering",
                    "do not reopen the compiled-boundary line unless",
                ],
            )
            else "blocked",
            "notes": "The selected freeze outcome is only justified if H33 named one question, R39 answered it narrowly, and the post-R39 plan keeps reopen conditions explicit.",
        },
        {
            "item_id": "driver_active_wave_and_f2_preserve_h32_routing_h34_control_and_no_active_downstream_runtime",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h32_post_r38_compiled_boundary_refreeze",
                    "h34_post_r39_later_explicit_scope_decision_packet",
                    "freeze_compiled_boundary_as_complete_for_now",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h34_post_r39_later_explicit_scope_decision_packet",
                    "freeze_compiled_boundary_as_complete_for_now",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["f2_activation_matrix_text"],
                [
                    "h34_post_r39_later_explicit_scope_decision_packet",
                    "r39_origin_compiler_control_surface_dependency_audit",
                    "contradiction-driven",
                ],
            )
            else "blocked",
            "notes": "After H34 lands, entrypoints should show H32 active, H34 as current docs-only control, and no active downstream runtime lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H34 lands the required later explicit interpretation packet after R39 as a docs-only control result.",
            "H32 remains the current active routing/refreeze packet after H34 lands.",
            "The selected outcome is `freeze_compiled_boundary_as_complete_for_now` rather than another automatic same-substrate runtime move.",
            "Future same-substrate reopening now requires a new explicit contradiction- or sharper-gap-driven packet.",
        ],
        "unsupported_here": [
            "H34 does not authorize a new runtime candidate.",
            "H34 does not convert the R39 positive result into arbitrary control-surface freedom or broader compiled support.",
            "H34 does not reopen same-endpoint systems recovery, frontier review, or scope lift.",
        ],
        "disconfirmed_here": [
            "The expectation that a locally positive R39 result should automatically trigger another compiled-boundary runtime lane.",
        ],
        "distilled_result": {
            "active_stage": "h34_post_r39_later_explicit_scope_decision_packet",
            "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
            "decision_state": "compiled_boundary_complete_for_now_docs_only",
            "selected_outcome": "freeze_compiled_boundary_as_complete_for_now",
            "non_selected_outcome": "authorize_one_more_origin_core_substrate_question",
            "authorized_next_runtime_candidate": "none",
            "reopen_precondition": "new_contradiction_or_sharper_same_substrate_gap_required",
            "blocked_future_lanes": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
            "future_frontier_review_state": "planning_only_f2_preserved",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h33 = inputs["h33_summary"]["summary"]
    r39_gate = inputs["r39_summary"]["summary"]["gate"]
    h32 = inputs["h32_summary"]["summary"]
    return [
        {
            "source": "results/H33_post_h32_conditional_next_question_packet/summary.json",
            "fields": {
                "active_stage": h33["active_stage"],
                "selected_outcome": h33["selected_outcome"],
                "authorized_next_runtime_candidate": h33["authorized_next_runtime_candidate"],
            },
        },
        {
            "source": "results/R39_origin_compiler_control_surface_dependency_audit/summary.json",
            "fields": {
                "lane_verdict": r39_gate["lane_verdict"],
                "declared_perturbation": r39_gate["declared_perturbation"],
                "perturbation_final_state_preserved_count": r39_gate["perturbation_final_state_preserved_count"],
                "perturbation_trace_changed_count": r39_gate["perturbation_trace_changed_count"],
                "next_priority_lane": r39_gate["next_priority_lane"],
            },
        },
        {
            "source": "results/H32_post_r38_compiled_boundary_refreeze/summary.json",
            "fields": {
                "active_stage": h32["active_stage"],
                "decision_state": h32["decision_state"],
                "next_required_lane": h32["next_required_lane"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h34_post_r39_later_explicit_scope_decision_packet_complete",
        "active_stage": "h34_post_r39_later_explicit_scope_decision_packet",
        "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
        "decision_state": "compiled_boundary_complete_for_now_docs_only",
        "selected_outcome": "freeze_compiled_boundary_as_complete_for_now",
        "non_selected_outcome": "authorize_one_more_origin_core_substrate_question",
        "authorized_next_runtime_candidate": "none",
        "reopen_precondition": "new_contradiction_or_sharper_same_substrate_gap_required",
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
