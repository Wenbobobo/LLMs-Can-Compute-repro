"""Export the post-R32 same-endpoint refreeze packet for H26."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H26_refreeze_after_r32_boundary_sharp_zoom"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    inputs: dict[str, Any] = {
        "h26_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "README.md"
        ),
        "h26_status_text": read_text(
            ROOT / "docs" / "milestones" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "status.md"
        ),
        "h26_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "todo.md"
        ),
        "h26_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "acceptance.md"
        ),
        "h26_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "artifact_index.md"
        ),
        "h23_summary_text": read_text(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json"),
        "h25_summary_text": read_text(ROOT / "results" / "H25_refreeze_after_r30_r31_decision_packet" / "summary.json"),
        "r30_summary_text": read_text(ROOT / "results" / "R30_d0_boundary_reauthorization_packet" / "summary.json"),
        "r32_summary_text": read_text(ROOT / "results" / "R32_d0_family_local_boundary_sharp_zoom" / "summary.json"),
    }
    inputs["h23_summary"] = read_json(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json")
    inputs["h25_summary"] = read_json(ROOT / "results" / "H25_refreeze_after_r30_r31_decision_packet" / "summary.json")
    inputs["r30_summary"] = read_json(ROOT / "results" / "R30_d0_boundary_reauthorization_packet" / "summary.json")
    inputs["r32_summary"] = read_json(ROOT / "results" / "R32_d0_family_local_boundary_sharp_zoom" / "summary.json")
    return inputs


def build_checklist_rows(
    *,
    h26_readme_text: str,
    h26_status_text: str,
    h26_todo_text: str,
    h26_acceptance_text: str,
    h26_artifact_index_text: str,
    h23_summary_text: str,
    h23_summary: dict[str, Any],
    h25_summary_text: str,
    h25_summary: dict[str, Any],
    r30_summary_text: str,
    r30_summary: dict[str, Any],
    r32_summary_text: str,
    r32_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h23 = h23_summary["summary"]
    h25 = h25_summary["summary"]
    r30 = r30_summary["summary"]
    r32 = r32_summary["summary"]
    r32_gate = r32["gate"]
    return [
        {
            "item_id": "h26_docs_describe_one_post_r32_same_endpoint_refreeze",
            "status": "pass"
            if contains_all(
                h26_readme_text,
                ["freeze the outcome of `R32`", "fixed `D0` endpoint", "`R33`"],
            )
            and contains_all(
                h26_status_text,
                ["executed", "`R32`", "`R33`", "`R29` and `F3` remain blocked"],
            )
            and contains_all(
                h26_todo_text,
                ["machine-readable same-endpoint packet", "`supported_here`", "`R33` remains justified next"],
            )
            and contains_all(
                h26_acceptance_text,
                ["post-`R32` same-endpoint refreeze", "`R33`", "`R29` and `F3` stay blocked"],
            )
            and contains_all(
                h26_artifact_index_text,
                [
                    "results/R32_d0_family_local_boundary_sharp_zoom/summary.json",
                    "results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json",
                    "R33_d0_non_retrieval_overhead_localization_audit",
                ],
            )
            else "blocked",
            "notes": "H26 should freeze R32 into one explicit same-endpoint routing packet.",
        },
        {
            "item_id": "r32_exports_one_explicit_family_local_sharp_zoom_verdict",
            "status": "pass"
            if str(r32_gate["lane_verdict"])
            in {
                "first_boundary_failure_localized",
                "near_boundary_mixed_signal_needs_confirmation",
                "grid_extended_still_not_localized",
                "resource_limited_before_localization",
            }
            and str(r32_gate["next_priority_lane"]) == "h26_refreeze_after_r32_boundary_sharp_zoom"
            and int(r32_gate["executed_candidate_count"]) > 0
            and contains_all(
                r32_summary_text,
                [
                    '"status": "r32_family_local_boundary_sharp_zoom_complete"',
                    '"next_priority_lane": "h26_refreeze_after_r32_boundary_sharp_zoom"',
                ],
            )
            else "blocked",
            "notes": "H26 must consume one explicit R32 verdict rather than a narrative summary.",
        },
        {
            "item_id": "h23_and_h25_remain_the_preserved_inputs_under_h26",
            "status": "pass"
            if str(h23["boundary_verdict"]) == "bounded_grid_still_not_localized"
            and str(h23["systems_verdict"]) == "systems_still_mixed"
            and str(h25["next_priority_lane"]) == "r32_d0_family_local_boundary_sharp_zoom"
            and str(h25["deferred_audit_lane"]) == "r33_d0_non_retrieval_overhead_localization_audit"
            and contains_all(
                h23_summary_text,
                ['"boundary_verdict": "bounded_grid_still_not_localized"', '"systems_verdict": "systems_still_mixed"'],
            )
            and contains_all(
                h25_summary_text,
                ['"next_priority_lane": "r32_d0_family_local_boundary_sharp_zoom"', '"deferred_audit_lane": "r33_d0_non_retrieval_overhead_localization_audit"'],
            )
            else "blocked",
            "notes": "H26 should preserve H23/H25 as the narrow pre-R32 controls.",
        },
        {
            "item_id": "r30_single_zoom_authorization_is_consumed_without_scope_drift",
            "status": "pass"
            if str(r30["boundary_reauthorization_verdict"]) == "execute_one_more_family_local_zoom"
            and str(r30["recommended_next_lane"]) == "r32_d0_family_local_boundary_sharp_zoom"
            and contains_all(
                r30_summary_text,
                ['"boundary_reauthorization_verdict": "execute_one_more_family_local_zoom"'],
            )
            else "blocked",
            "notes": "H26 should treat R32 as the consumed R30-authorized sharp zoom, not as an open-ended reopen.",
        },
    ]


def map_boundary_verdict(r32_verdict: str) -> str:
    if r32_verdict == "first_boundary_failure_localized":
        return "first_boundary_failure_localized"
    if r32_verdict == "near_boundary_mixed_signal_needs_confirmation":
        return "boundary_signal_not_yet_localized"
    if r32_verdict == "resource_limited_before_localization":
        return "resource_limited_without_boundary_localization"
    return "family_local_sharp_zoom_still_not_localized"


def decide_next_priority_lane(boundary_verdict: str, h25_summary: dict[str, Any]) -> tuple[str, str]:
    deferred_lane = str(h25_summary["deferred_audit_lane"])
    if deferred_lane:
        return deferred_lane, "preserve_deferred_r33_as_next_lane"
    return "later_explicit_packet_required", "require_later_explicit_packet_before_new_runtime"


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    h23 = inputs["h23_summary"]["summary"]
    h25 = inputs["h25_summary"]["summary"]
    r32 = inputs["r32_summary"]["summary"]
    r32_gate = r32["gate"]

    boundary_verdict = map_boundary_verdict(str(r32_gate["lane_verdict"]))
    next_priority_lane, downstream_routing_decision = decide_next_priority_lane(boundary_verdict, h25)
    systems_verdict = str(h23["systems_verdict"])

    supported_here = [
        (
            f"R32 executes {r32_gate['executed_candidate_count']}/"
            f"{r32_gate['planned_candidate_count']} planned candidates under the authorized family-local sharp zoom."
        ),
        "H26 keeps the fixed tiny typed-bytecode D0 endpoint and does not reopen the historical full grid.",
    ]
    if boundary_verdict == "first_boundary_failure_localized":
        supported_here.append("The R30-authorized sharp zoom now localizes one bounded same-endpoint failure.")
    elif boundary_verdict == "boundary_signal_not_yet_localized":
        supported_here.append("R32 found a bounded near-boundary signal without enough evidence to call the boundary localized.")
    elif boundary_verdict == "resource_limited_without_boundary_localization":
        supported_here.append("R32 stayed bounded but hit its resource cap before localizing a clean failure.")
    else:
        supported_here.append("R32 exhausts its first-pass family-local ladder without producing a first failing row.")
    if next_priority_lane == "r33_d0_non_retrieval_overhead_localization_audit":
        supported_here.append("Deferred R33 remains the next justified same-endpoint audit lane after H26.")

    unsupported_here = [
        "H26 does not widen beyond the fixed tiny typed-bytecode D0 endpoint.",
        "H26 does not authorize direct R29 execution or broader scope lift.",
        "H26 does not reopen the historical full grid or add a fifth execution axis.",
    ]
    if boundary_verdict != "first_boundary_failure_localized":
        unsupported_here.append("The true executor boundary is still not localized strongly enough for a broader boundary claim.")
    if systems_verdict != "systems_materially_positive":
        unsupported_here.append("The same-endpoint systems story remains mixed because H26 adds no new systems evidence.")

    disconfirmed_here: list[str] = []
    if boundary_verdict == "family_local_sharp_zoom_still_not_localized":
        disconfirmed_here.append(
            "The narrower expectation that the R30-authorized first-pass family-local sharp zoom would localize a first failure inside its saved ladder."
        )

    return {
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
        "distilled_result": {
            "h25_next_priority_lane": h25["next_priority_lane"],
            "h25_deferred_audit_lane": h25["deferred_audit_lane"],
            "r32_lane_verdict": r32_gate["lane_verdict"],
            "h26_boundary_verdict": boundary_verdict,
            "h23_systems_verdict": systems_verdict,
            "downstream_routing_decision": downstream_routing_decision,
            "next_priority_lane": next_priority_lane,
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h23 = inputs["h23_summary"]["summary"]
    h25 = inputs["h25_summary"]["summary"]
    r30 = inputs["r30_summary"]["summary"]
    r32_gate = inputs["r32_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H23_refreeze_after_r26_r27_r28/summary.json",
            "fields": {
                "boundary_verdict": h23["boundary_verdict"],
                "systems_verdict": h23["systems_verdict"],
            },
        },
        {
            "source": "results/H25_refreeze_after_r30_r31_decision_packet/summary.json",
            "fields": {
                "next_priority_lane": h25["next_priority_lane"],
                "deferred_audit_lane": h25["deferred_audit_lane"],
            },
        },
        {
            "source": "results/R30_d0_boundary_reauthorization_packet/summary.json",
            "fields": {
                "boundary_reauthorization_verdict": r30["boundary_reauthorization_verdict"],
                "recommended_next_lane": r30["recommended_next_lane"],
            },
        },
        {
            "source": "results/R32_d0_family_local_boundary_sharp_zoom/summary.json",
            "fields": {
                "lane_verdict": r32_gate["lane_verdict"],
                "executed_candidate_count": r32_gate["executed_candidate_count"],
                "failure_candidate_count": r32_gate["failure_candidate_count"],
            },
        },
    ]


def build_summary(
    checklist_rows: list[dict[str, object]],
    inputs: dict[str, Any],
    claim_packet: dict[str, object],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    h23 = inputs["h23_summary"]["summary"]
    h25 = inputs["h25_summary"]["summary"]
    r32_gate = inputs["r32_summary"]["summary"]["gate"]

    boundary_verdict = map_boundary_verdict(str(r32_gate["lane_verdict"]))
    next_priority_lane, downstream_routing_decision = decide_next_priority_lane(boundary_verdict, h25)

    unsatisfied_frontier_activation_conditions = []
    if boundary_verdict != "first_boundary_failure_localized":
        unsatisfied_frontier_activation_conditions.append("true_executor_boundary_localization")
    if str(h23["systems_verdict"]) != "systems_materially_positive":
        unsatisfied_frontier_activation_conditions.append("current_scope_systems_story_materially_positive")
    unsatisfied_frontier_activation_conditions.append("scope_lift_thesis_explicitly_reauthorized")

    return {
        "current_paper_phase": "h26_refreeze_after_r32_boundary_sharp_zoom_complete",
        "active_stage": "h26_refreeze_after_r32_boundary_sharp_zoom",
        "prior_frozen_stage": "h23_refreeze_after_r26_r27_r28",
        "prior_operational_stage": "h25_refreeze_after_r30_r31_decision_packet",
        "source_runtime_lane": "r32_d0_family_local_boundary_sharp_zoom",
        "decision_state": "post_r32_refreeze_complete",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "boundary_verdict": boundary_verdict,
        "systems_verdict": h23["systems_verdict"],
        "downstream_routing_decision": downstream_routing_decision,
        "next_priority_lane": next_priority_lane,
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "unsatisfied_frontier_activation_conditions": unsatisfied_frontier_activation_conditions,
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Advance to deferred R33 as the next same-endpoint audit lane while keeping R29 and F3 blocked."
            if next_priority_lane == "r33_d0_non_retrieval_overhead_localization_audit"
            else "Require a later explicit packet before opening any new same-endpoint runtime lane."
        ),
        "supported_here": claim_packet["supported_here"],
        "unsupported_here": claim_packet["unsupported_here"],
        "disconfirmed_here": claim_packet["disconfirmed_here"],
        "distilled_result": claim_packet["distilled_result"],
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    claim_packet = build_claim_packet(inputs)
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h26_refreeze_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h26_refreeze_snapshot", "environment": environment.as_dict(), "rows": snapshot_rows},
    )
    write_json(
        OUT_DIR / "claim_packet.json",
        {"experiment": "h26_refreeze_claim_packet", "environment": environment.as_dict(), "summary": claim_packet},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h26_refreeze_after_r32_boundary_sharp_zoom",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/README.md",
                "docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/status.md",
                "docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/todo.md",
                "docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/acceptance.md",
                "docs/milestones/H26_refreeze_after_r32_boundary_sharp_zoom/artifact_index.md",
                "results/H23_refreeze_after_r26_r27_r28/summary.json",
                "results/H25_refreeze_after_r30_r31_decision_packet/summary.json",
                "results/R30_d0_boundary_reauthorization_packet/summary.json",
                "results/R32_d0_family_local_boundary_sharp_zoom/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H26 Refreeze After R32 Boundary Sharp Zoom\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n"
        "- `claim_packet.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
