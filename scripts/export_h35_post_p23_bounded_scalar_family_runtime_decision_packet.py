"""Export the post-P23 bounded-scalar runtime decision packet for H35."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet"


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
        "h35_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet" / "README.md"
        ),
        "h35_status_text": read_text(
            ROOT / "docs" / "milestones" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet" / "status.md"
        ),
        "h35_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet" / "todo.md"
        ),
        "h35_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet" / "acceptance.md"
        ),
        "h35_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-p23-h35-r40-bounded-scalar-runtime-design.md"),
        "f13_family_scope_text": read_text(
            ROOT / "docs" / "milestones" / "F13_post_f12_bounded_scalar_value_family_spec" / "family_scope.md"
        ),
        "f13_reference_semantics_text": read_text(
            ROOT / "docs" / "milestones" / "F13_post_f12_bounded_scalar_value_family_spec" / "reference_semantics.md"
        ),
        "f14_threat_model_text": read_text(
            ROOT / "docs" / "milestones" / "F14_post_f13_conditional_reopen_readiness_bundle" / "threat_model.md"
        ),
        "h34_summary": read_json(ROOT / "results" / "H34_post_r39_later_explicit_scope_decision_packet" / "summary.json"),
        "r39_summary": read_json(ROOT / "results" / "R39_origin_compiler_control_surface_dependency_audit" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h34 = inputs["h34_summary"]["summary"]
    r39_gate = inputs["r39_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h35_docs_authorize_exactly_one_bounded_scalar_runtime_gate",
            "status": "pass"
            if contains_all(
                inputs["h35_readme_text"],
                [
                    "authorize_one_bounded_scalar_family_runtime_gate",
                    "keep_no_runtime_lane_under_h34_for_now",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                    "r41_origin_runtime_relevance_threat_stress_audit",
                ],
            )
            and contains_all(
                inputs["h35_status_text"],
                [
                    "completed docs-only bounded-scalar family runtime-decision packet",
                    "h32",
                    "h34",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                ],
            )
            and contains_all(
                inputs["h35_todo_text"],
                [
                    "current opcode surface",
                    "r41_origin_runtime_relevance_threat_stress_audit",
                    "r29",
                    "f3",
                ],
            )
            and contains_all(
                inputs["h35_acceptance_text"],
                [
                    "docs-only",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                    "bounded frame locals",
                    "typed flag slots",
                ],
            )
            and contains_all(
                inputs["h35_artifact_index_text"],
                [
                    "docs/plans/2026-03-23-post-p23-h35-r40-bounded-scalar-runtime-design.md",
                    "results/h35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json",
                    "docs/milestones/r40_origin_bounded_scalar_locals_and_flags_gate/",
                ],
            )
            else "blocked",
            "notes": "H35 should authorize exactly one bounded-scalar runtime gate and keep later threat stress deferred.",
        },
        {
            "item_id": "f13_f14_and_post_p23_design_support_the_selected_runtime_scope",
            "status": "pass"
            if contains_all(
                inputs["design_text"],
                [
                    "bounded scalar locals and flags",
                    "without adding a new opcode surface",
                    "without introducing heap-like aliasing",
                    "r41_origin_runtime_relevance_threat_stress_audit",
                ],
            )
            and contains_all(
                inputs["f13_family_scope_text"],
                [
                    "bounded_scalar_locals_and_flags",
                    "exact booleans used as branch-visible flags",
                    "single-cell reads and writes",
                ],
            )
            and contains_all(
                inputs["f13_reference_semantics_text"],
                [
                    "local slots are drawn from one fixed finite set",
                    "reads recover the latest logical value of one named slot",
                    "branch behavior may depend on those slot values",
                ],
            )
            and contains_all(
                inputs["f14_threat_model_text"],
                [
                    "runtime_irrelevance_via_compiler_helper_overencoding",
                    "fast_path_only_helps_the_easy_part",
                ],
            )
            else "blocked",
            "notes": "H35 should follow the F13 family definition directly and leave the F14 threat bundle deferred.",
        },
        {
            "item_id": "h34_and_r39_are_preserved_as_upstream_context_not_broader_authorization",
            "status": "pass"
            if str(h34["selected_outcome"]) == "freeze_compiled_boundary_as_complete_for_now"
            and str(h34["authorized_next_runtime_candidate"]) == "none"
            and str(r39_gate["lane_verdict"]) == "control_surface_dependence_not_detected_on_declared_permutation"
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                ],
            )
            else "blocked",
            "notes": "H35 should sit above preserved H34/R39 context rather than pretending that H34 already authorized R40 automatically.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H35 lands the required docs-only decision packet after P23 and authorizes exactly one bounded-scalar runtime gate.",
            "The authorized runtime scope is explicit: bounded frame locals, typed flag slots, same substrate, same opcode surface only.",
            "R41 remains deferred and inactive after H35.",
        ],
        "unsupported_here": [
            "H35 does not authorize restricted-Wasm, hybrid/planner, or broader compiler widening.",
            "H35 does not reopen R29, F3, or future frontier review by wording alone.",
        ],
        "disconfirmed_here": [
            "The expectation that H34 permanently forbids any later same-substrate runtime packet once F13 exposes a sharper bounded family question.",
        ],
        "distilled_result": {
            "active_stage": "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
            "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
            "selected_outcome": "authorize_one_bounded_scalar_family_runtime_gate",
            "non_selected_outcome": "keep_no_runtime_lane_under_h34_for_now",
            "authorized_next_runtime_candidate": "r40_origin_bounded_scalar_locals_and_flags_gate",
            "authorized_runtime_scope": "same_substrate_same_opcode_frame_only_bounded_scalar_locals_and_flags",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "deferred_runtime_precondition": "new_explicit_post_r40_packet_required",
        },
    }


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h35_post_p23_bounded_scalar_family_runtime_decision_packet_complete",
        "active_stage": "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
        "current_active_routing_stage": "h32_post_r38_compiled_boundary_refreeze",
        "selected_outcome": "authorize_one_bounded_scalar_family_runtime_gate",
        "non_selected_outcome": "keep_no_runtime_lane_under_h34_for_now",
        "authorized_next_runtime_candidate": "r40_origin_bounded_scalar_locals_and_flags_gate",
        "authorized_runtime_scope": "same_substrate_same_opcode_frame_only_bounded_scalar_locals_and_flags",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "deferred_runtime_precondition": "new_explicit_post_r40_packet_required",
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
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
