"""Export the post-H23 boundary reauthorization packet for R30."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R30_d0_boundary_reauthorization_packet"


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
        "r30_readme_text": read_text(ROOT / "docs" / "milestones" / "R30_d0_boundary_reauthorization_packet" / "README.md"),
        "r30_status_text": read_text(ROOT / "docs" / "milestones" / "R30_d0_boundary_reauthorization_packet" / "status.md"),
        "r30_todo_text": read_text(ROOT / "docs" / "milestones" / "R30_d0_boundary_reauthorization_packet" / "todo.md"),
        "r30_acceptance_text": read_text(ROOT / "docs" / "milestones" / "R30_d0_boundary_reauthorization_packet" / "acceptance.md"),
        "r30_artifact_index_text": read_text(ROOT / "docs" / "milestones" / "R30_d0_boundary_reauthorization_packet" / "artifact_index.md"),
        "h23_summary_text": read_text(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json"),
        "h21_summary_text": read_text(ROOT / "results" / "H21_refreeze_after_r22_r23" / "summary.json"),
        "r22_summary_text": read_text(ROOT / "results" / "R22_d0_true_boundary_localization_gate" / "summary.json"),
        "r26_summary_text": read_text(ROOT / "results" / "R26_d0_boundary_localization_execution_gate" / "summary.json"),
        "r27_summary_text": read_text(ROOT / "results" / "R27_d0_boundary_localization_extension_gate" / "summary.json"),
        "r24_matrix_text": read_text(ROOT / "docs" / "milestones" / "R24_d0_boundary_localization_zoom_followup" / "boundary_zoom_matrix.md"),
    }
    inputs["h23_summary"] = read_json(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json")
    inputs["h21_summary"] = read_json(ROOT / "results" / "H21_refreeze_after_r22_r23" / "summary.json")
    inputs["r22_summary"] = read_json(ROOT / "results" / "R22_d0_true_boundary_localization_gate" / "summary.json")
    inputs["r26_summary"] = read_json(ROOT / "results" / "R26_d0_boundary_localization_execution_gate" / "summary.json")
    inputs["r27_summary"] = read_json(ROOT / "results" / "R27_d0_boundary_localization_extension_gate" / "summary.json")
    return inputs


def build_checklist_rows(
    *,
    r30_readme_text: str,
    r30_status_text: str,
    r30_todo_text: str,
    r30_acceptance_text: str,
    r30_artifact_index_text: str,
    h23_summary_text: str,
    h23_summary: dict[str, Any],
    h21_summary_text: str,
    h21_summary: dict[str, Any],
    r22_summary_text: str,
    r22_summary: dict[str, Any],
    r26_summary_text: str,
    r26_summary: dict[str, Any],
    r27_summary_text: str,
    r27_summary: dict[str, Any],
    r24_matrix_text: str,
) -> list[dict[str, object]]:
    h23 = h23_summary["summary"]
    h21 = h21_summary["summary"]
    r22 = r22_summary["summary"]["gate"]
    r26 = r26_summary["summary"]["gate"]
    r27 = r27_summary["summary"]["gate"]
    return [
        {
            "item_id": "r30_docs_define_a_decision_packet_not_a_new_runtime_lane",
            "status": "pass"
            if contains_all(
                r30_readme_text,
                ["does not execute a new boundary scan", "`R21`", "`R22`", "`R24`", "`H23`"],
            )
            and contains_all(
                r30_status_text,
                ["authorize at most one future bounded family-local sharp zoom", "principled no-localization grounds", "`D0`"],
            )
            and contains_all(
                r30_todo_text,
                ["candidate core", "approved-axis list", "stop-rule", "next boundary lane"],
            )
            and contains_all(
                r30_acceptance_text,
                ["`execute_one_more_family_local_zoom`", "`hold_boundary_lane_closed`", "`needs_new_axis_before_more_execution`"],
            )
            and contains_all(
                r30_artifact_index_text,
                ["results/R30_d0_boundary_reauthorization_packet/summary.json", "R24_d0_boundary_localization_zoom_followup", "R32_d0_family_local_boundary_sharp_zoom"],
            )
            else "blocked",
            "notes": "R30 should remain a post-H23 decision packet rather than a hidden runtime lane.",
        },
        {
            "item_id": "current_boundary_state_still_requires_reauthorization",
            "status": "pass"
            if h23["boundary_verdict"] == "bounded_grid_still_not_localized"
            and h21["boundary_verdict"] == "extended_grid_no_break_still_not_localized"
            and contains_all(
                h23_summary_text,
                ['"boundary_verdict": "bounded_grid_still_not_localized"', '"next_priority_lane": "p14_public_surface_sync_after_h23"'],
            )
            and contains_all(
                h21_summary_text,
                ['"boundary_verdict": "extended_grid_no_break_still_not_localized"', '"systems_verdict": "systems_still_mixed"'],
            )
            else "blocked",
            "notes": "R30 only exists because both H21 and H23 still leave the true executor boundary unresolved.",
        },
        {
            "item_id": "r22_r26_r27_all_preserve_no_localized_break_inside_bounded_scans",
            "status": "pass"
            if str(r22["lane_verdict"]) == "no_failure_in_extended_grid"
            and str(r26["lane_verdict"]) == "grid_extended_still_not_localized"
            and str(r27["lane_verdict"]) == "extension_grid_still_not_localized"
            and contains_all(r22_summary_text, ['"lane_verdict": "no_failure_in_extended_grid"'])
            and contains_all(r26_summary_text, ['"lane_verdict": "grid_extended_still_not_localized"'])
            and contains_all(r27_summary_text, ['"lane_verdict": "extension_grid_still_not_localized"'])
            else "blocked",
            "notes": "R30 should be grounded in the fact that several bounded scans still stayed exact without localizing a failure.",
        },
        {
            "item_id": "r24_already_exports_a_candidate_core_and_stop_rules",
            "status": "pass"
            if contains_all(
                r24_matrix_text,
                ["Candidate Core", "Zoom Axes", "Stop Rules", "Predeclared Verdict Vocabulary", "checkpoint_replay_long"],
            )
            else "blocked",
            "notes": "R30 should reuse the R24 bounded zoom discipline instead of inventing a new open-ended scan.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H23_refreeze_after_r26_r27_r28/summary.json",
            "fields": {
                "boundary_verdict": inputs["h23_summary"]["summary"]["boundary_verdict"],
                "systems_verdict": inputs["h23_summary"]["summary"]["systems_verdict"],
            },
        },
        {
            "source": "results/R22_d0_true_boundary_localization_gate/summary.json",
            "fields": {
                "lane_verdict": inputs["r22_summary"]["summary"]["gate"]["lane_verdict"],
                "planned_candidate_count": inputs["r22_summary"]["summary"]["gate"]["planned_candidate_count"],
            },
        },
        {
            "source": "results/R26_d0_boundary_localization_execution_gate/summary.json",
            "fields": {
                "lane_verdict": inputs["r26_summary"]["summary"]["gate"]["lane_verdict"],
                "executed_candidate_count": inputs["r26_summary"]["summary"]["gate"]["executed_candidate_count"],
            },
        },
        {
            "source": "results/R27_d0_boundary_localization_extension_gate/summary.json",
            "fields": {
                "lane_verdict": inputs["r27_summary"]["summary"]["gate"]["lane_verdict"],
                "executed_candidate_count": inputs["r27_summary"]["summary"]["gate"]["executed_candidate_count"],
            },
        },
        {
            "source": "docs/milestones/R24_d0_boundary_localization_zoom_followup/boundary_zoom_matrix.md",
            "planned_role": "candidate_core_and_stop_rules",
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_frozen_stage": "h23_refreeze_after_r26_r27_r28",
        "boundary_reauthorization_verdict": "execute_one_more_family_local_zoom",
        "candidate_core": [
            "checkpoint_replay_long/u32/h3.0/plus_two/flattened",
            "helper_checkpoint_braid_long/u20/h3.0/plus_two/flattened",
            "subroutine_braid_long/u20/h3.0/plus_two/flattened",
            "helper_checkpoint_braid/u8/h2.0/plus_one/flattened",
            "subroutine_braid/u6/h2.0/plus_one/flattened",
        ],
        "approved_axes": [
            "unique_address_target",
            "horizon_multiplier",
            "checkpoint_depth",
            "hot_address_skew",
        ],
        "stop_rules": [
            "stop a branch after two reproduced exactness failures",
            "stop the whole lane if every candidate-core branch either fails cleanly or exhausts the predeclared zoom matrix without a failure",
            "require one first_fail plus at least one neighboring exact row before any claim of boundary localization",
        ],
        "recommended_next_lane": "r32_d0_family_local_boundary_sharp_zoom",
        "kill_reason_if_closed": None,
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Authorize one future family-local sharp zoom through R32 while keeping the endpoint fixed, the candidate core explicit, and the historical full-grid expansion closed."
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
        {"experiment": "r30_boundary_reauthorization_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "r30_boundary_reauthorization_snapshot", "environment": environment.as_dict(), "rows": snapshot_rows},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r30_d0_boundary_reauthorization_packet",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/R30_d0_boundary_reauthorization_packet/README.md",
                "docs/milestones/R30_d0_boundary_reauthorization_packet/status.md",
                "docs/milestones/R30_d0_boundary_reauthorization_packet/todo.md",
                "docs/milestones/R30_d0_boundary_reauthorization_packet/acceptance.md",
                "docs/milestones/R30_d0_boundary_reauthorization_packet/artifact_index.md",
                "results/H23_refreeze_after_r26_r27_r28/summary.json",
                "results/H21_refreeze_after_r22_r23/summary.json",
                "results/R22_d0_true_boundary_localization_gate/summary.json",
                "results/R26_d0_boundary_localization_execution_gate/summary.json",
                "results/R27_d0_boundary_localization_extension_gate/summary.json",
                "docs/milestones/R24_d0_boundary_localization_zoom_followup/boundary_zoom_matrix.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R30 D0 Boundary Reauthorization Packet\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
