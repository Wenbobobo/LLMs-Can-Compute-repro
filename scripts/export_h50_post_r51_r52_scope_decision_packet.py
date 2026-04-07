"""Export the post-R51/R52 scope-decision packet for H50."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H50_post_r51_r52_scope_decision_packet"


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
        "h50_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H50_post_r51_r52_scope_decision_packet" / "README.md"
        ),
        "h50_status_text": read_text(
            ROOT / "docs" / "milestones" / "H50_post_r51_r52_scope_decision_packet" / "status.md"
        ),
        "h50_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H50_post_r51_r52_scope_decision_packet" / "todo.md"
        ),
        "h50_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H50_post_r51_r52_scope_decision_packet" / "acceptance.md"
        ),
        "h50_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H50_post_r51_r52_scope_decision_packet" / "artifact_index.md"
        ),
        "f27_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle" / "README.md"
        ),
        "f27_status_text": read_text(
            ROOT / "docs" / "milestones" / "F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle" / "status.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h49_summary": read_json(ROOT / "results" / "H49_post_r50_tinyc_lowering_decision_packet" / "summary.json"),
        "r51_summary": read_json(ROOT / "results" / "R51_origin_memory_control_surface_sufficiency_gate" / "summary.json"),
        "r52_summary": read_json(ROOT / "results" / "R52_origin_internal_vs_external_executor_value_gate" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h49 = inputs["h49_summary"]["summary"]
    r51 = inputs["r51_summary"]["summary"]["gate"]
    r52 = inputs["r52_summary"]["summary"]["gate"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "h50_docs_record_negative_closeout_explicitly",
            "status": "pass"
            if contains_all(
                inputs["h50_readme_text"],
                [
                    "completed docs-only scope decision packet after landed `r51` and `r52`",
                    "`stop_as_exact_without_system_value`",
                    "`freeze_as_narrow_specialized_executor_only`",
                    "`allow_planning_only_f27_entry_bundle`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h50_status_text"],
                [
                    "completed docs-only post-`r51/r52` decision packet",
                    "preserves `h49` as the preserved prior docs-only packet",
                    "preserves `h43` as the paper-grade endpoint",
                    "selects `stop_as_exact_without_system_value`",
                ],
            )
            and contains_all(
                inputs["h50_todo_text"],
                [
                    "[x] interpret landed `r51` and `r52` explicitly",
                    "[x] decide whether to freeze as a narrow specialized executor",
                    "[x] keep broader trainable/transformed entry blocked",
                ],
            )
            and contains_all(
                inputs["h50_acceptance_text"],
                [
                    "`h50` remains docs-only",
                    "exactly one decision outcome is selected",
                    "`h49` remains visible as the current upstream docs-only packet",
                    "`h43` remains visible as the paper-grade endpoint",
                    "`no_active_downstream_runtime_lane` is restored",
                ],
            )
            and contains_all(
                inputs["h50_artifact_index_text"],
                [
                    "results/r51_origin_memory_control_surface_sufficiency_gate/summary.json",
                    "results/r52_origin_internal_vs_external_executor_value_gate/summary.json",
                    "results/h50_post_r51_r52_scope_decision_packet/summary.json",
                    "scripts/export_h50_post_r51_r52_scope_decision_packet.py",
                ],
            )
            else "blocked",
            "notes": "H50 must be an explicit negative closeout packet rather than an implied consequence of R52 alone.",
        },
        {
            "item_id": "r51_positive_and_r52_negative_support_h50",
            "status": "pass"
            if str(h49["selected_outcome"]) == "freeze_r50_as_narrow_exact_tinyc_support_only"
            and str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(r51["lane_verdict"]) == "memory_control_surface_supported_narrowly"
            and int(r51["planned_case_count"]) == 5
            and int(r51["exact_case_count"]) == 5
            and int(r51["maximizer_identity_exact_count"]) == 5
            and int(r51["budget_clean_case_count"]) == 5
            and str(r52["lane_verdict"]) == "internal_route_lacks_bounded_value"
            and int(r52["executed_case_count"]) == 5
            and int(r52["accelerated_exact_case_count"]) == 5
            and int(r52["linear_exact_case_count"]) == 5
            and int(r52["external_exact_case_count"]) == 5
            and int(r52["accelerated_faster_than_linear_count"]) == 3
            and int(r52["accelerated_faster_than_external_count"]) == 0
            else "blocked",
            "notes": "H50 should close the lane only because R51 stayed narrow-positive while R52 stayed exact but failed the bounded-value test.",
        },
        {
            "item_id": "shared_control_surfaces_make_h50_current",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h50_post_r51_r52_scope_decision_packet`",
                    "`r51_origin_memory_control_surface_sufficiency_gate` is now the completed post-`h49` runtime gate",
                    "`r52_origin_internal_vs_external_executor_value_gate` is now the completed post-`h49` comparator gate",
                    "`stop_as_exact_without_system_value`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`r51_origin_memory_control_surface_sufficiency_gate` is now the completed",
                    "`r52_origin_internal_vs_external_executor_value_gate` is now the completed",
                    "`stop_as_exact_without_system_value`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`r51_origin_memory_control_surface_sufficiency_gate`",
                    "`r52_origin_internal_vs_external_executor_value_gate`",
                    "the current downstream scientific lane after `h50`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h50_post_r51_r52_scope_decision_packet` is now the current active docs-only",
                    "`r51_origin_memory_control_surface_sufficiency_gate` completed with",
                    "`r52_origin_internal_vs_external_executor_value_gate` completed with",
                    "`stop_as_exact_without_system_value`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| d2f |",
                    "| d2g |",
                    "| h50 |",
                    "stop as exact without system value",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h50_post_r51_r52_scope_decision_packet/` — current active docs-only",
                    "r52_origin_internal_vs_external_executor_value_gate/` — completed",
                    "r51_origin_memory_control_surface_sufficiency_gate/` — completed",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`f26` `r51/r52/h50` substrate-sufficiency and bounded-value closeout wave",
                    "new `scripts/export_h50_post_r51_r52_scope_decision_packet.py`",
                    "new `results/h50_post_r51_r52_scope_decision_packet/summary.json`",
                ],
            )
            else "blocked",
            "notes": "The shared control surfaces should make H50 current so unattended work starts from the real closeout state.",
        },
        {
            "item_id": "f27_remains_saved_but_blocked_after_negative_h50",
            "status": "pass"
            if contains_all(
                inputs["f27_readme_text"],
                [
                    "saved future planning-only bundle",
                    "`saved_but_blocked_after_negative_h50`",
                    "does not authorize `f27`",
                ],
            )
            and contains_all(
                inputs["f27_status_text"],
                [
                    "not active here",
                    "explicitly non-selected by landed negative `h50`",
                    "blocked unless a later explicit packet reopens the question",
                ],
            )
            else "blocked",
            "notes": "Future executor-entry planning remains stored but inactive after the negative H50 closeout.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "The append-only exact substrate remains sufficient on one bounded richer memory/control surface.",
            "R51 is a narrow positive result, not an empty failure-to-falsify.",
            "H50 lands an explicit negative closeout packet instead of widening by momentum from R51 alone.",
        ],
        "unsupported_here": [
            "The internal exact route does not show bounded system value over simpler baselines on the landed R51 rows.",
            "F27 is not authorized from the landed H50 state.",
            "Trainable or transformed executor growth is not active on this branch.",
        ],
        "disconfirmed_here": [
            "The idea that a positive narrow substrate-extension result is enough to justify broader executor investment without a bounded-value win.",
        ],
        "distilled_result": {
            "active_stage": "h50_post_r51_r52_scope_decision_packet",
            "preserved_prior_docs_only_decision_packet": "h49_post_r50_tinyc_lowering_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_post_h49_planning_bundle": "f26_post_h49_origin_claim_delta_and_next_question_bundle",
            "current_completed_post_h49_runtime_gate": "r51_origin_memory_control_surface_sufficiency_gate",
            "current_completed_post_h49_comparator_gate": "r52_origin_internal_vs_external_executor_value_gate",
            "selected_outcome": "stop_as_exact_without_system_value",
            "future_bundle_state": "f27_saved_but_blocked_after_negative_h50",
            "current_low_priority_wave": "p36_post_h49_cleanline_hygiene_and_artifact_policy",
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h49 = inputs["h49_summary"]["summary"]
    r51 = inputs["r51_summary"]["summary"]["gate"]
    r52 = inputs["r52_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H49_post_r50_tinyc_lowering_decision_packet/summary.json",
            "fields": {
                "active_stage": h49["active_stage"],
                "selected_outcome": h49["selected_outcome"],
                "next_required_lane": h49["next_required_lane"],
            },
        },
        {
            "source": "results/R51_origin_memory_control_surface_sufficiency_gate/summary.json",
            "fields": {
                "lane_verdict": r51["lane_verdict"],
                "exact_case_count": r51["exact_case_count"],
                "maximizer_identity_exact_count": r51["maximizer_identity_exact_count"],
                "budget_clean_case_count": r51["budget_clean_case_count"],
            },
        },
        {
            "source": "results/R52_origin_internal_vs_external_executor_value_gate/summary.json",
            "fields": {
                "lane_verdict": r52["lane_verdict"],
                "executed_case_count": r52["executed_case_count"],
                "accelerated_faster_than_linear_count": r52["accelerated_faster_than_linear_count"],
                "accelerated_faster_than_external_count": r52["accelerated_faster_than_external_count"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "preserved_prior_docs_only_decision_packet": distilled["preserved_prior_docs_only_decision_packet"],
        "current_active_routing_stage": distilled["current_active_routing_stage"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "current_post_h49_planning_bundle": distilled["current_post_h49_planning_bundle"],
        "current_completed_post_h49_runtime_gate": distilled["current_completed_post_h49_runtime_gate"],
        "current_completed_post_h49_comparator_gate": distilled["current_completed_post_h49_comparator_gate"],
        "selected_outcome": distilled["selected_outcome"],
        "future_bundle_state": distilled["future_bundle_state"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "next_required_lane": distilled["next_required_lane"],
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
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet)

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
