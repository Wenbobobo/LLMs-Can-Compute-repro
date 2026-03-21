"""Export a machine-readable guard for the active H16 same-scope reopen stage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H16_post_h15_same_scope_reopen_guard"


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


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["blocked_count"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def diff_check_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["git_diff_check_state"])


def load_inputs() -> dict[str, Any]:
    paths = {
        "readme_text": ROOT / "README.md",
        "status_text": ROOT / "STATUS.md",
        "publication_readme_text": ROOT / "docs" / "publication_record" / "README.md",
        "current_stage_driver_text": ROOT / "docs" / "publication_record" / "current_stage_driver.md",
        "release_summary_text": ROOT / "docs" / "publication_record" / "release_summary_draft.md",
        "h16_readme_text": ROOT / "docs" / "milestones" / "H16_post_h15_same_scope_reopen_and_scope_lock" / "README.md",
        "h16_status_text": ROOT / "docs" / "milestones" / "H16_post_h15_same_scope_reopen_and_scope_lock" / "status.md",
        "h16_artifact_index_text": ROOT / "docs" / "milestones" / "H16_post_h15_same_scope_reopen_and_scope_lock" / "artifact_index.md",
        "r18_status_text": ROOT / "docs" / "milestones" / "R18_d0_same_endpoint_runtime_repair_counterfactual" / "status.md",
        "h17_status_text": ROOT / "docs" / "milestones" / "H17_refreeze_and_conditional_frontier_recheck" / "status.md",
        "h15_summary_text": ROOT / "results" / "H15_refreeze_and_decision_sync" / "summary.json",
        "r15_summary_text": ROOT / "results" / "R15_d0_remaining_family_retrieval_pressure_gate" / "summary.json",
        "r16_summary_text": ROOT / "results" / "R16_d0_real_trace_precision_boundary_saturation" / "summary.json",
        "r17_summary_text": ROOT / "results" / "R17_d0_full_surface_runtime_bridge" / "summary.json",
        "h14_guard_text": ROOT / "results" / "H14_core_first_reopen_guard" / "summary.json",
        "h13_stage_health_summary_text": ROOT / "results" / "H13_post_h12_governance_stage_health" / "summary.json",
        "v1_timing_summary_text": ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup" / "summary.json",
        "worktree_summary_text": ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json",
        "m7_decision_text": ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json",
    }
    inputs: dict[str, Any] = {key: read_text(path) for key, path in paths.items()}
    for key, path in paths.items():
        if key.endswith("_text") and path.suffix == ".json":
            inputs[key.removesuffix("_text")] = read_json(path)
    return inputs


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    release_summary_text: str,
    h16_readme_text: str,
    h16_status_text: str,
    h16_artifact_index_text: str,
    r18_status_text: str,
    h17_status_text: str,
    h15_summary_text: str,
    h15_summary: dict[str, Any],
    r15_summary_text: str,
    r15_summary: dict[str, Any],
    r16_summary_text: str,
    r16_summary: dict[str, Any],
    r17_summary_text: str,
    r17_summary: dict[str, Any],
    h14_guard_text: str,
    h14_guard: dict[str, Any],
    h13_stage_health_summary_text: str,
    h13_stage_health_summary: dict[str, Any],
    v1_timing_summary_text: str,
    v1_timing_summary: dict[str, Any],
    worktree_summary_text: str,
    worktree_summary: dict[str, Any],
    m7_decision_text: str,
    m7_decision: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "current_stage_driver_exposes_h16_same_scope_lane_order",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h16_post_h15_same_scope_reopen_and_scope_lock`",
                    "`r15_d0_remaining_family_retrieval_pressure_gate`",
                    "`r16_d0_real_trace_precision_boundary_saturation`",
                    "`r17_d0_full_surface_runtime_bridge`",
                    "comparator-only `r18_d0_same_endpoint_runtime_repair_counterfactual`",
                    "`h17_refreeze_and_conditional_frontier_recheck`",
                    "`h15_refreeze_and_decision_sync`",
                ],
            )
            else "blocked",
            "notes": "The canonical driver should expose H16 as the active same-scope reopen and make the R15/R16/R17/activated comparator-only R18/H17 order explicit.",
        },
        {
            "item_id": "root_and_public_docs_promote_h16_without_widening",
            "status": "pass"
            if (
                contains_all(
                    readme_text,
                    [
                        "| `h16-h17` | completed bounded same-scope reopen/refreeze packet",
                        "the current active post-`p9` stage is `h17_refreeze_and_conditional_frontier_recheck`",
                        "`h15_refreeze_and_decision_sync` is now the preserved prior refreeze",
                        "`r18b` then closed the runtime repair packet",
                    ],
                )
                or contains_all(
                    readme_text,
                    [
                        "| `h16-h17` | completed bounded same-scope reopen/refreeze packet",
                        "`h21_refreeze_after_r22_r23`",
                        "`results/h17_refreeze_and_conditional_frontier_recheck/summary.json`",
                        "`h15_refreeze_and_decision_sync` is now the preserved prior refreeze",
                    ],
                )
            )
            and contains_all(
                status_text,
                [
                    "`h17_refreeze_and_conditional_frontier_recheck`",
                    "`h15_refreeze_and_decision_sync` remains the preserved prior refrozen state",
                    "`r16` has now closed the bounded real-trace precision saturation follow-up",
                    "`r17` has now closed the bounded full-surface same-endpoint runtime bridge",
                    "`h16 -> r15 -> r16 -> r17 -> comparator-only r18 -> h17`",
                ],
            )
            and (
                contains_all(
                    publication_readme_text,
                    [
                        "canonical `active_driver` for the current `h17` frozen same-scope state",
                        "`h16` / `r15` / `r16` / `r17` / comparator-only `r18` / `h17`",
                        "`r18b` recorded as the bounded runtime repair closeout",
                        "`h15` is the completed predecessor refreeze stage",
                    ],
                )
                or contains_all(
                    publication_readme_text,
                    [
                        "keeps `h21` as the current frozen same-endpoint state",
                        "keeps `h17` as the preserved prior same-scope refreeze decision",
                        "keeps `h15` as the preserved prior refreeze decision",
                        "`r18` remains the completed comparator-only repair closeout",
                    ],
                )
            )
            and (
                contains_all(
                    release_summary_text,
                    [
                        "the current active post-`p9` stage is `h17_refreeze_and_conditional_frontier_recheck`",
                        "`r15` has already landed",
                        "`r16` has now landed",
                        "`r17` has now landed as the bounded full-surface runtime bridge",
                        "`r18b` then closed the repair packet",
                        "`h17` now refreezes that completed same-scope packet",
                    ],
                )
                or contains_all(
                    release_summary_text,
                    [
                        "the current active post-`p9` stage is `h21_refreeze_after_r22_r23`",
                        "`h17` remains the preserved prior same-scope refreeze decision",
                        "`h15_refreeze_and_decision_sync` remains the completed predecessor refreeze stage",
                        "`h19` is now the preserved pre-`r22/r23` refreeze decision",
                    ],
                )
            )
            else "blocked",
            "notes": "Root and publication-facing docs should advance to H16 while keeping the scope lock and non-claims explicit.",
        },
        {
            "item_id": "h16_milestone_docs_lock_same_scope_scope_and_sequence",
            "status": "pass"
            if contains_all(
                h16_readme_text,
                [
                    "same fixed `d0` endpoint",
                    "landed `r15`, `r16`, `r17`, and closed comparator-only `r18`",
                    "`h17` as the same-scope closeout stage",
                    "`r15 -> r16 -> r17 -> comparator-only r18 -> h17`",
                ],
            )
            and contains_all(
                h16_status_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`r15_d0_remaining_family_retrieval_pressure_gate`",
                    "`r16_d0_real_trace_precision_boundary_saturation`",
                    "`r17_d0_full_surface_runtime_bridge` has landed",
                    "`r18_d0_same_endpoint_runtime_repair_counterfactual` has now closed as a comparator-only same-endpoint follow-up lane",
                    "`h17_refreeze_and_conditional_frontier_recheck` has now exported the required same-scope closeout state",
                    "frontier recheck now requires a separate conditional plan",
                ],
            )
            and contains_all(
                h16_artifact_index_text,
                [
                    "2026-03-20-h16-post-h15-same-scope-reopen-design.md",
                    "2026-03-20-r15-d0-remaining-family-retrieval-pressure-design.md",
                    "2026-03-20-r16-d0-real-trace-precision-boundary-saturation-design.md",
                    "2026-03-20-r17-d0-full-surface-runtime-bridge-design.md",
                    "2026-03-20-r18-d0-same-endpoint-runtime-repair-counterfactual-design.md",
                    "2026-03-20-h17-refreeze-and-conditional-frontier-recheck-design.md",
                    "docs/milestones/r18_d0_same_endpoint_runtime_repair_counterfactual/status.md",
                    "docs/milestones/h17_refreeze_and_conditional_frontier_recheck/status.md",
                    "results/h16_post_h15_same_scope_reopen_guard/summary.json",
                    "results/h15_refreeze_and_decision_sync/summary.json",
                    "results/r17_d0_full_surface_runtime_bridge/summary.json",
                ],
            )
            else "blocked",
            "notes": "The H16 milestone docs should keep the reopened scope lock, execution order, and artifact plan explicit.",
        },
        {
            "item_id": "r15_remaining_family_lane_landed_cleanly",
            "status": "pass"
            if r15_summary["summary"]["exact_suite"]["row_count"] == 4
            and r15_summary["summary"]["exact_suite"]["exact_admitted_count"] == 4
            and r15_summary["summary"]["exact_suite"]["contradiction_candidate_count"] == 0
            and r15_summary["summary"]["decode_parity"]["row_count"] == 2
            and r15_summary["summary"]["decode_parity"]["parity_match_count"] == 2
            and str(r15_summary["summary"]["claim_impact"]["gate_status"]) == "go_remaining_family_retrieval_pressure_exact"
            and str(r15_summary["summary"]["claim_impact"]["next_lane"]) == "R16_d0_real_trace_precision_boundary_saturation"
            and contains_all(
                r15_summary_text,
                [
                    "\"exact_admitted_count\": 4",
                    "\"parity_match_count\": 2",
                    "\"gate_status\": \"go_remaining_family_retrieval_pressure_exact\"",
                ],
            )
            else "blocked",
            "notes": "H16 should start from a landed R15 remaining-family gate rather than a placeholder lane description.",
        },
        {
            "item_id": "r16_precision_surface_lane_landed_cleanly",
            "status": "pass"
            if r16_summary["summary"]["source_surface"]["admitted_program_count"] == 8
            and r16_summary["summary"]["screening"]["candidate_stream_count"] == 8
            and r16_summary["summary"]["classification"]["effective_here_stream_count"] == 8
            and r16_summary["summary"]["classification"]["unproven_here_stream_count"] == 0
            and r16_summary["summary"]["classification"]["negated_here_stream_count"] == 0
            and str(r16_summary["summary"]["claim_impact"]["gate_status"]) == "go_real_trace_precision_surface_saturated"
            and str(r16_summary["summary"]["claim_impact"]["next_lane"]) == "R17_d0_full_surface_runtime_bridge"
            and contains_all(
                r16_summary_text,
                [
                    "\"admitted_program_count\": 8",
                    "\"effective_here_stream_count\": 8",
                    "\"gate_status\": \"go_real_trace_precision_surface_saturated\"",
                    "\"next_lane\": \"R17_d0_full_surface_runtime_bridge\"",
                ],
            )
            else "blocked",
            "notes": "H16 should reflect a landed R16 precision-saturation lane before handing the packet forward to R17.",
        },
        {
            "item_id": "r17_runtime_bridge_landed_and_r18_activation_remains_bounded",
            "status": "pass"
            if r17_summary["summary"]["overall"]["runtime_profiled_row_count"] == 8
            and r17_summary["summary"]["overall"]["contradiction_candidate_count"] == 0
            and str(r17_summary["summary"]["stopgo"]["stopgo_status"]) == "stop_decode_gain_not_material"
            and str(r17_summary["summary"]["claim_impact"]["status"]) == "full_surface_same_endpoint_runtime_bridge_measured"
            and str(r17_summary["summary"]["claim_impact"]["next_lane"]) == "H17_refreeze_and_conditional_frontier_recheck"
            and contains_all(
                r17_summary_text,
                [
                    "\"runtime_profiled_row_count\": 8",
                    "\"stopgo_status\": \"stop_decode_gain_not_material\"",
                    "\"status\": \"full_surface_same_endpoint_runtime_bridge_measured\"",
                    "\"next_lane\": \"H17_refreeze_and_conditional_frontier_recheck\"",
                ],
            )
            and contains_all(
                r18_status_text,
                [
                    "conditionally activated",
                    "comparator-only",
                    "`r18c` staged deterministic retrieval is therefore not needed",
                    "cannot be used to widen claim scope indirectly",
                ],
            )
            and contains_all(
                h17_status_text,
                [
                    "downstream of landed `r15/r16/r17` and the closed comparator-only `r18` packet",
                    "explicit post-`h16` refrozen same-scope state",
                    "separate conditional plan",
                ],
            )
            else "blocked",
            "notes": "H16 carry-over closeout should reflect a landed R17 bridge, an activated comparator-only R18 lane, and a still-pending H17 refreeze.",
        },
        {
            "item_id": "h15_h14_h13_predecessor_controls_remain_green",
            "status": "pass"
            if h15_summary["summary"]["decision_state"] == "direct_refreeze_complete"
            and blocked_count_from_summary(h15_summary) == 0
            and h14_guard["summary"]["stage_guard_state"] == "preserved_core_first_reopen_guard_green"
            and blocked_count_from_summary(h14_guard) == 0
            and h13_stage_health_summary["summary"]["stage_health_state"] == "preserved_handoff_green"
            and blocked_count_from_summary(h13_stage_health_summary) == 0
            and contains_all(h15_summary_text, ["\"decision_state\": \"direct_refreeze_complete\"", "\"blocked_count\": 0"])
            and contains_all(h14_guard_text, ["\"stage_guard_state\": \"preserved_core_first_reopen_guard_green\"", "\"blocked_count\": 0"])
            and contains_all(h13_stage_health_summary_text, ["\"stage_health_state\": \"preserved_handoff_green\"", "\"blocked_count\": 0"])
            else "blocked",
            "notes": "H16 should inherit a green predecessor chain from H15, the preserved H14 packet, and the preserved H13/V1 handoff.",
        },
        {
            "item_id": "preserved_v1_runtime_reference_remains_green",
            "status": "pass"
            if v1_timing_summary["summary"]["runtime_classification"] == "healthy_but_slow"
            and int(v1_timing_summary["summary"]["timed_out_file_count"]) == 0
            and contains_all(
                v1_timing_summary_text,
                ["\"runtime_classification\": \"healthy_but_slow\"", "\"timed_out_file_count\": 0"],
            )
            else "blocked",
            "notes": "The preserved V1 runtime reference should remain operationally bounded while H16 is active.",
        },
        {
            "item_id": "release_worktree_and_no_widening_constraints_remain_explicit",
            "status": "pass"
            if release_commit_state_from_summary(worktree_summary)
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            and diff_check_state_from_summary(worktree_summary) in {"warnings_only", "clean"}
            and m7_decision["summary"]["frontend_widening_authorized"] is False
            and m7_decision["summary"]["public_demo_authorized"] is False
            and contains_all(
                worktree_summary_text,
                [
                    "\"release_commit_state\":",
                    "\"git_diff_check_state\":",
                ],
            )
            and contains_all(
                m7_decision_text,
                [
                    "\"frontend_widening_authorized\": false",
                    "\"public_demo_authorized\": false",
                ],
            )
            else "blocked",
            "notes": "H16 may reopen same-scope science work, but release hygiene and no-widening constraints remain in force.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H15_refreeze_and_decision_sync/summary.json",
            "fields": {
                "decision_state": inputs["h15_summary"]["summary"]["decision_state"],
                "r13_decision": inputs["h15_summary"]["summary"]["r13_decision"],
                "r14_decision": inputs["h15_summary"]["summary"]["r14_decision"],
            },
        },
        {
            "source": "results/H14_core_first_reopen_guard/summary.json",
            "fields": {
                "stage_guard_state": inputs["h14_guard"]["summary"]["stage_guard_state"],
                "blocked_count": inputs["h14_guard"]["summary"]["blocked_count"],
                "guarded_reopen_stage": inputs["h14_guard"]["summary"]["guarded_reopen_stage"],
            },
        },
        {
            "source": "results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json",
            "fields": {
                "exact_admitted_count": inputs["r15_summary"]["summary"]["exact_suite"]["exact_admitted_count"],
                "parity_match_count": inputs["r15_summary"]["summary"]["decode_parity"]["parity_match_count"],
                "next_lane": inputs["r15_summary"]["summary"]["claim_impact"]["next_lane"],
            },
        },
        {
            "source": "results/R16_d0_real_trace_precision_boundary_saturation/summary.json",
            "fields": {
                "admitted_program_count": inputs["r16_summary"]["summary"]["source_surface"]["admitted_program_count"],
                "effective_here_stream_count": inputs["r16_summary"]["summary"]["classification"]["effective_here_stream_count"],
                "next_lane": inputs["r16_summary"]["summary"]["claim_impact"]["next_lane"],
            },
        },
        {
            "source": "results/R17_d0_full_surface_runtime_bridge/summary.json",
            "fields": {
                "runtime_profiled_row_count": inputs["r17_summary"]["summary"]["overall"]["runtime_profiled_row_count"],
                "stopgo_status": inputs["r17_summary"]["summary"]["stopgo"]["stopgo_status"],
                "next_lane": inputs["r17_summary"]["summary"]["claim_impact"]["next_lane"],
            },
        },
        {
            "source": "docs/milestones/R18_d0_same_endpoint_runtime_repair_counterfactual/status.md",
            "fields": {
                "activated": contains_all(
                    inputs["r18_status_text"],
                    ["conditionally activated"],
                ),
                "comparator_only": contains_all(
                    inputs["r18_status_text"],
                    ["comparator-only"],
                ),
            },
        },
        {
            "source": "docs/milestones/H17_refreeze_and_conditional_frontier_recheck/status.md",
            "fields": {
                "pending_refreeze": contains_all(
                    inputs["h17_status_text"],
                    ["refreeze the same-scope packet"],
                ),
                "frontier_recheck_unauthorized": contains_all(
                    inputs["h17_status_text"],
                    ["frontier recheck remains conditional and unauthorized"],
                ),
            },
        },
        {
            "source": "results/H13_post_h12_governance_stage_health/summary.json",
            "fields": {
                "stage_health_state": inputs["h13_stage_health_summary"]["summary"]["stage_health_state"],
                "blocked_count": inputs["h13_stage_health_summary"]["summary"]["blocked_count"],
            },
        },
        {
            "source": "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
            "fields": {
                "runtime_classification": inputs["v1_timing_summary"]["summary"]["runtime_classification"],
                "timed_out_file_count": inputs["v1_timing_summary"]["summary"]["timed_out_file_count"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], worktree_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h16_post_h15_same_scope_reopen_active",
        "active_stage": "h16_post_h15_same_scope_reopen_and_scope_lock",
        "prior_refreeze_stage": "h15_refreeze_and_decision_sync",
        "predecessor_refreeze_stage": "h15_refreeze_and_decision_sync",
        "prior_completed_reopen_stage": "h14_core_first_reopen_and_scope_lock",
        "handoff_stage": "h13_post_h12_rollover_and_next_stage_staging_preserved",
        "stage_guard_state": "same_scope_reopen_guard_green" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_summary),
        "lane_order": "preserve_h15_then_land_r15_r16_r17_then_activate_comparator_only_r18_then_h17",
        "lane_progression": "h16_then_r15_then_r16_then_r17_then_activated_comparator_only_r18_then_h17",
        "first_landed_lane": "r15_d0_remaining_family_retrieval_pressure_gate",
        "first_science_lane": "r15_d0_remaining_family_retrieval_pressure_gate",
        "latest_landed_lane": "r17_d0_full_surface_runtime_bridge",
        "active_comparator_lane": "r18_d0_same_endpoint_runtime_repair_counterfactual",
        "comparator_lane_state": "activated_comparator_only",
        "next_priority_lane": "r18_d0_same_endpoint_runtime_repair_counterfactual",
        "next_stage": "r18_d0_same_endpoint_runtime_repair_counterfactual",
        "pending_closeout_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use this summary as the H16 carry-over closeout entrypoint; preserve H15 as the completed predecessor refreeze, treat R15/R16/R17 as landed on the same fixed D0 scope, keep R18 active only as a comparator-only same-endpoint lane, and close under H17 rather than widening by narrative"
            if not blocked_items
            else "resolve the blocked H16 scope-lock items before treating the reopened same-scope lane as canonical"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs["worktree_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h16_post_h15_same_scope_reopen_guard_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h16_post_h15_same_scope_reopen_guard_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h16_post_h15_same_scope_reopen_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/milestones/H16_post_h15_same_scope_reopen_and_scope_lock/README.md",
                "docs/milestones/H16_post_h15_same_scope_reopen_and_scope_lock/status.md",
                "docs/milestones/H16_post_h15_same_scope_reopen_and_scope_lock/artifact_index.md",
                "results/H15_refreeze_and_decision_sync/summary.json",
                "results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json",
                "results/R16_d0_real_trace_precision_boundary_saturation/summary.json",
                "results/R17_d0_full_surface_runtime_bridge/summary.json",
                "docs/milestones/R18_d0_same_endpoint_runtime_repair_counterfactual/status.md",
                "docs/milestones/H17_refreeze_and_conditional_frontier_recheck/status.md",
                "results/H14_core_first_reopen_guard/summary.json",
                "results/H13_post_h12_governance_stage_health/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H16 Post-H15 Same-Scope Reopen Guard\n\n"
        "Machine-readable guard for the active H16 same-scope reopen and scope lock.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
