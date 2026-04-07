"""Export the post-H21 dual-track reopen-control summary for H22."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H22_post_h21_boundary_reopen_and_dual_track_lock"


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
    paths = {
        "h22_readme_text": ROOT / "docs" / "milestones" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "README.md",
        "h22_status_text": ROOT / "docs" / "milestones" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "status.md",
        "h22_todo_text": ROOT / "docs" / "milestones" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "todo.md",
        "h22_acceptance_text": ROOT / "docs" / "milestones" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "acceptance.md",
        "h22_artifact_index_text": ROOT / "docs" / "milestones" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "artifact_index.md",
        "h22_decision_log_text": ROOT / "docs" / "milestones" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "decision_log.md",
        "r26_todo_text": ROOT / "docs" / "milestones" / "R26_d0_boundary_localization_execution_gate" / "todo.md",
        "r27_status_text": ROOT / "docs" / "milestones" / "R27_d0_boundary_localization_extension_gate" / "status.md",
        "r28_todo_text": ROOT / "docs" / "milestones" / "R28_d0_trace_retrieval_contract_audit" / "todo.md",
        "h23_todo_text": ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "todo.md",
        "r29_status_text": ROOT / "docs" / "milestones" / "R29_d0_same_endpoint_systems_recovery_execution_gate" / "status.md",
        "f3_status_text": ROOT / "docs" / "milestones" / "F3_post_h23_scope_lift_decision_bundle" / "status.md",
        "h21_summary_text": ROOT / "results" / "H21_refreeze_after_r22_r23" / "summary.json",
        "r24_matrix_text": ROOT / "docs" / "milestones" / "R24_d0_boundary_localization_zoom_followup" / "boundary_zoom_matrix.md",
        "r25_thresholds_text": ROOT / "docs" / "milestones" / "R25_d0_same_endpoint_systems_recovery_hypotheses" / "thresholds_and_disconfirmers.md",
    }
    inputs: dict[str, Any] = {key: read_text(path) for key, path in paths.items()}
    inputs["h21_summary"] = read_json(paths["h21_summary_text"])
    return inputs


def build_checklist_rows(
    *,
    h22_readme_text: str,
    h22_status_text: str,
    h22_todo_text: str,
    h22_acceptance_text: str,
    h22_artifact_index_text: str,
    h22_decision_log_text: str,
    r26_todo_text: str,
    r27_status_text: str,
    r28_todo_text: str,
    h23_todo_text: str,
    r29_status_text: str,
    f3_status_text: str,
    h21_summary_text: str,
    h21_summary: dict[str, Any],
    r24_matrix_text: str,
    r25_thresholds_text: str,
) -> list[dict[str, object]]:
    h21_state = h21_summary["summary"]
    return [
        {
            "item_id": "h22_docs_lock_one_dual_track_reopen_contract",
            "status": "pass"
            if contains_all(
                h22_readme_text,
                ["dual-track", "`R26`", "`R28`", "`R27`", "`H23`"],
            )
            and contains_all(
                h22_status_text,
                ["bounded same-endpoint reopen packet", "`R26`", "`R28`", "`R29`", "`F3`"],
            )
            and contains_all(
                h22_todo_text,
                ["`R26`", "`R27`", "`R28`", "machine-readable `H22` control summary"],
            )
            and contains_all(
                h22_acceptance_text,
                ["`R26` manifest", "`R27` trigger", "`R28`", "widened runtime"],
            )
            and contains_all(
                h22_decision_log_text,
                ["`H21`", "`R26`", "`R28`", "`R27`", "`P14`"],
            )
            else "blocked",
            "notes": "H22 should define the reopen packet before any new runtime execution is treated as active.",
        },
        {
            "item_id": "h22_keeps_h21_as_the_frozen_input",
            "status": "pass"
            if h21_state["active_stage"] == "h21_refreeze_after_r22_r23"
            and h21_state["boundary_verdict"] == "extended_grid_no_break_still_not_localized"
            and h21_state["systems_verdict"] == "systems_still_mixed"
            and contains_all(
                h21_summary_text,
                [
                    '"active_stage": "h21_refreeze_after_r22_r23"',
                    '"future_frontier_review_state": "planning_only_conditionally_reviewable"',
                ],
            )
            else "blocked",
            "notes": "H22 is a reopen-control stage on top of H21, not a replacement of the frozen H21 state.",
        },
        {
            "item_id": "r26_and_r28_are_actionable_before_runtime_starts",
            "status": "pass"
            if contains_all(
                r26_todo_text,
                ["exact `R26` manifest", "`22`-candidate", "`first_fail_digest`", "`R27`"],
            )
            and contains_all(
                r28_todo_text,
                ["claim-layer map", "`latest_write`", "`stack`", "cost-breakdown"],
            )
            and contains_all(
                h23_todo_text,
                ["`R26`", "`R27`", "`R28`", "machine-readable packet"],
            )
            else "blocked",
            "notes": "H22 should only activate lanes that already have explicit acceptance and handoff targets.",
        },
        {
            "item_id": "r27_is_conditional_and_future_lanes_remain_blocked",
            "status": "pass"
            if contains_all(
                r27_status_text,
                ["Blocked by default", "confirmation mode", "extension mode", "no `plus_three`"],
            )
            and contains_all(
                r29_status_text,
                ["Blocked by default", "same-endpoint", "explicit reopen plan"],
            )
            and contains_all(
                f3_status_text,
                ["Blocked by default", "planning surface only", "broader demos or headlines"],
            )
            else "blocked",
            "notes": "Only R26 and R28 should be active by default under H22.",
        },
        {
            "item_id": "h22_stays_downstream_of_r24_and_r25_planning_packets",
            "status": "pass"
            if contains_all(
                r24_matrix_text,
                ["candidate core", "Stop Rules", "Predeclared Verdict Vocabulary"],
            )
            and contains_all(
                r25_thresholds_text,
                ["systems_materially_positive", "systems_still_mixed", "Kill Criteria"],
            )
            and contains_all(
                h22_artifact_index_text,
                ["R26_d0_boundary_localization_execution_gate", "R28_d0_trace_retrieval_contract_audit"],
            )
            else "blocked",
            "notes": "H22 should treat R24/R25 as bounded inputs rather than reopening scope from scratch.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h21_summary = inputs["h21_summary"]["summary"]
    return [
        {
            "source": "results/H21_refreeze_after_r22_r23/summary.json",
            "active_stage": h21_summary["active_stage"],
            "boundary_verdict": h21_summary["boundary_verdict"],
            "systems_verdict": h21_summary["systems_verdict"],
            "future_frontier_review_state": h21_summary.get("future_frontier_review_state"),
        },
        {
            "source": "docs/milestones/R24_d0_boundary_localization_zoom_followup/boundary_zoom_matrix.md",
            "planned_role": "bounded_boundary_input",
        },
        {
            "source": "docs/milestones/R25_d0_same_endpoint_systems_recovery_hypotheses/thresholds_and_disconfirmers.md",
            "planned_role": "same_endpoint_systems_limits_input",
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "h22_post_h21_boundary_reopen_and_dual_track_lock",
        "current_frozen_stage": "h21_refreeze_after_r22_r23",
        "decision_state": "post_h21_dual_track_reopen_contract_complete",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "active_runtime_lane": "r26_d0_boundary_localization_execution_gate",
        "active_support_lane": "r28_d0_trace_retrieval_contract_audit",
        "conditional_runtime_lane": "r27_d0_boundary_localization_extension_gate",
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "next_priority_lane": "r26_d0_boundary_localization_execution_gate",
        "check_count": len(checklist_rows),
        "pass_count": len(checklist_rows) - len(blocked_items),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Advance to R26 and R28 in parallel, keep R27 conditional, and refreeze the packet in H23 before any outward sync."
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "h22_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "h22_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h22_post_h21_boundary_reopen_and_dual_track_lock",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/README.md",
                "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/status.md",
                "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/todo.md",
                "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/acceptance.md",
                "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/artifact_index.md",
                "docs/milestones/H22_post_h21_boundary_reopen_and_dual_track_lock/decision_log.md",
                "docs/milestones/R26_d0_boundary_localization_execution_gate/todo.md",
                "docs/milestones/R27_d0_boundary_localization_extension_gate/status.md",
                "docs/milestones/R28_d0_trace_retrieval_contract_audit/todo.md",
                "docs/milestones/H23_refreeze_after_r26_r27_r28/todo.md",
                "docs/milestones/R29_d0_same_endpoint_systems_recovery_execution_gate/status.md",
                "docs/milestones/F3_post_h23_scope_lift_decision_bundle/status.md",
                "results/H21_refreeze_after_r22_r23/summary.json",
                "docs/milestones/R24_d0_boundary_localization_zoom_followup/boundary_zoom_matrix.md",
                "docs/milestones/R25_d0_same_endpoint_systems_recovery_hypotheses/thresholds_and_disconfirmers.md",
            ],
            "summary": summary,
        },
    )


if __name__ == "__main__":
    main()
