"""Export the H17 post-H16 refreeze and conditional frontier recheck summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H17_refreeze_and_conditional_frontier_recheck"


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["blocked_count"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def load_inputs() -> dict[str, Any]:
    paths = {
        "h16_guard": ROOT / "results" / "H16_post_h15_same_scope_reopen_guard" / "summary.json",
        "r15_summary": ROOT / "results" / "R15_d0_remaining_family_retrieval_pressure_gate" / "summary.json",
        "r16_summary": ROOT / "results" / "R16_d0_real_trace_precision_boundary_saturation" / "summary.json",
        "r17_summary": ROOT / "results" / "R17_d0_full_surface_runtime_bridge" / "summary.json",
        "r18_summary": ROOT / "results" / "R18_d0_same_endpoint_runtime_repair_counterfactual" / "summary.json",
        "p5_summary": ROOT / "results" / "P5_public_surface_sync" / "summary.json",
        "h2_summary": ROOT / "results" / "H2_bundle_lock_audit" / "summary.json",
        "p10_summary": ROOT / "results" / "P10_submission_archive_ready" / "summary.json",
        "worktree_summary": ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json",
    }
    return {key: read_json(path) for key, path in paths.items()}


def build_checklist_rows(
    *,
    h16_guard: dict[str, Any],
    r15_summary: dict[str, Any],
    r16_summary: dict[str, Any],
    r17_summary: dict[str, Any],
    r18_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    h2_summary: dict[str, Any],
    p10_summary: dict[str, Any],
    worktree_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "h16_guard_stayed_green_until_refreeze",
            "status": "pass"
            if h16_guard["summary"]["stage_guard_state"] == "same_scope_reopen_guard_green"
            and blocked_count_from_summary(h16_guard) == 0
            else "blocked",
            "notes": "H17 should only close a green same-scope reopen packet rather than a drifting intermediate state.",
        },
        {
            "item_id": "same_scope_lanes_r15_r16_r17_remain_landed",
            "status": "pass"
            if r15_summary["summary"]["claim_impact"]["next_lane"] == "R16_d0_real_trace_precision_boundary_saturation"
            and r16_summary["summary"]["claim_impact"]["next_lane"] == "R17_d0_full_surface_runtime_bridge"
            and r17_summary["summary"]["claim_impact"]["status"] == "full_surface_same_endpoint_runtime_bridge_measured"
            else "blocked",
            "notes": "H17 preserves the landed same-scope evidence packet rather than reopening earlier lanes.",
        },
        {
            "item_id": "r18_closed_under_h17_without_extra_probe_budget",
            "status": "pass"
            if r18_summary["summary"]["status"] in {"r18b_pointer_like_complete", "r18c_staged_exact_complete"}
            and r18_summary["summary"]["claim_impact"]["next_lane"] == "H17_refreeze_and_conditional_frontier_recheck"
            and r18_summary["summary"]["claim_impact"]["next_probe"] is None
            else "blocked",
            "notes": "R18 should arrive at H17 as a closed bounded packet, not as an open-ended repair branch.",
        },
        {
            "item_id": "public_surface_and_bundle_controls_remain_green",
            "status": "pass"
            if blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            and blocked_count_from_summary(p10_summary) == 0
            else "blocked",
            "notes": "H17 inherits the standing outward-sync and bundle-lock controls instead of bypassing them.",
        },
        {
            "item_id": "release_worktree_state_is_known",
            "status": "pass"
            if release_commit_state_from_summary(worktree_summary)
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            else "blocked",
            "notes": "H17 should record the release/worktree state explicitly even when the tree remains intentionally dirty.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H16_post_h15_same_scope_reopen_guard/summary.json",
            "fields": {
                "stage_guard_state": inputs["h16_guard"]["summary"]["stage_guard_state"],
                "latest_landed_lane": inputs["h16_guard"]["summary"]["latest_landed_lane"],
                "active_comparator_lane": inputs["h16_guard"]["summary"]["active_comparator_lane"],
            },
        },
        {
            "source": "results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json",
            "fields": {
                "next_lane": inputs["r15_summary"]["summary"]["claim_impact"]["next_lane"],
            },
        },
        {
            "source": "results/R16_d0_real_trace_precision_boundary_saturation/summary.json",
            "fields": {
                "next_lane": inputs["r16_summary"]["summary"]["claim_impact"]["next_lane"],
            },
        },
        {
            "source": "results/R17_d0_full_surface_runtime_bridge/summary.json",
            "fields": {
                "status": inputs["r17_summary"]["summary"]["claim_impact"]["status"],
                "stopgo_status": inputs["r17_summary"]["summary"]["stopgo"]["stopgo_status"],
            },
        },
        {
            "source": "results/R18_d0_same_endpoint_runtime_repair_counterfactual/summary.json",
            "fields": {
                "status": inputs["r18_summary"]["summary"]["status"],
                "probe_strategy": inputs["r18_summary"]["summary"]["probe_strategy"],
                "executed_probe_ids": inputs["r18_summary"]["summary"]["executed_probe_ids"],
                "frontier_recheck_hint": inputs["r18_summary"]["summary"]["frontier_recheck_hint"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], inputs: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    r18_confirmed = bool(inputs["r18_summary"]["summary"]["confirmation"]["gate_passed"])
    frontier_recheck_decision = "conditional_plan_required" if r18_confirmed else "blocked"
    next_stage = "future_frontier_recheck_plan_required" if r18_confirmed else "same_scope_stop_and_archive"
    return {
        "current_paper_phase": "h17_refreeze_and_conditional_frontier_recheck_complete",
        "active_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "guarded_reopen_stage": "h16_post_h15_same_scope_reopen_and_scope_lock",
        "decision_state": "same_scope_refreeze_complete" if not blocked_items else "further_resolution_required",
        "r18_decision": str(inputs["r18_summary"]["summary"]["claim_impact"]["status"]),
        "frontier_recheck_decision": frontier_recheck_decision,
        "next_stage": next_stage,
        "release_commit_state": release_commit_state_from_summary(inputs["worktree_summary"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "preserve H17 as the current refrozen same-scope state, keep the D0 exact-executor evidence explicit, and require a separate conditional frontier plan before any scope lift"
            if not blocked_items and r18_confirmed
            else "preserve H17 as the negative same-scope closeout, archive the disproved repair hypotheses, and stop without widening scope"
            if not blocked_items
            else "resolve the blocked H17 refreeze inputs before treating this packet as the canonical post-H16 state"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h17_refreeze_and_conditional_frontier_recheck_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h17_refreeze_and_conditional_frontier_recheck_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h17_refreeze_and_conditional_frontier_recheck",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/H16_post_h15_same_scope_reopen_guard/summary.json",
                "results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json",
                "results/R16_d0_real_trace_precision_boundary_saturation/summary.json",
                "results/R17_d0_full_surface_runtime_bridge/summary.json",
                "results/R18_d0_same_endpoint_runtime_repair_counterfactual/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/P10_submission_archive_ready/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H17 Refreeze And Conditional Frontier Recheck\n\n"
        "Machine-readable closeout summary for the post-H16 same-scope refreeze.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
