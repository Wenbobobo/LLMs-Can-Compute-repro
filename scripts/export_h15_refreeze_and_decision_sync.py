"""Export the H15 completed refreeze and decision-sync bundle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H15_refreeze_and_decision_sync"


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_inputs() -> dict[str, Any]:
    return {
        "h14_guard": read_json(ROOT / "results" / "H14_core_first_reopen_guard" / "summary.json"),
        "r11_summary": read_json(ROOT / "results" / "R11_geometry_fastpath_reaudit" / "summary.json"),
        "r12_summary": read_json(ROOT / "results" / "R12_append_only_executor_long_horizon" / "summary.json"),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
        "p10_summary": read_json(ROOT / "results" / "P10_submission_archive_ready" / "summary.json"),
    }


def build_checklist_rows(
    *,
    h14_guard: dict[str, Any],
    r11_summary: dict[str, Any],
    r12_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    h2_summary: dict[str, Any],
    p10_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h14 = h14_guard["summary"]
    r11 = r11_summary["summary"]
    r12 = r12_summary["summary"]
    p5 = p5_summary["summary"]
    h2 = h2_summary["summary"]
    p10 = p10_summary["summary"]

    r11_green = bool(r11["current_exactness"]["all_cases_exact"]) and not bool(
        r11["same_endpoint_guard"]["same_endpoint_fastpath_material"]
    )
    r12_green = (
        bool(r12["free_running_baseline"]["all_modes_exact"])
        and str(r12["harder_d0_baseline"]["e1c_status"]) == "not_triggered"
        and int(r12["mechanistic_baseline"]["contradiction_candidate_count"]) == 0
    )
    standing_controls_green = (
        int(h14["blocked_count"]) == 0
        and int(p5["blocked_count"]) == 0
        and int(h2["blocked_count"]) == 0
        and int(p10["blocked_count"]) == 0
    )
    r13_needed = not r12_green
    r14_justified = False

    return [
        {
            "item_id": "h14_guard_remains_green",
            "status": "pass" if int(h14["blocked_count"]) == 0 else "blocked",
            "notes": "The completed H14 reopen packet should remain green before H15 is treated as the canonical refrozen state.",
        },
        {
            "item_id": "r11_keeps_geometry_exact_and_wording_bounded",
            "status": "pass" if r11_green else "blocked",
            "notes": "R11 must keep bounded geometry parity exact and keep same-endpoint speedup wording blocked.",
        },
        {
            "item_id": "r12_keeps_executor_evidence_exact_without_current_gap",
            "status": "pass" if r12_green else "blocked",
            "notes": "R12 must keep current executor evidence exact and avoid exposing a bounded gap that would force R13.",
        },
        {
            "item_id": "standing_public_surface_and_bundle_controls_are_green",
            "status": "pass" if standing_controls_green else "blocked",
            "notes": "P5, H2, and P10 should stay green before H15 performs doc-sync refreeze work.",
        },
        {
            "item_id": "r13_is_not_currently_needed",
            "status": "pass" if not r13_needed else "blocked",
            "notes": "No bounded stack-bridge gap is exposed by the current R12 export, so R13 remains inactive.",
        },
        {
            "item_id": "r14_is_not_currently_justified",
            "status": "pass" if not r14_justified else "blocked",
            "notes": "No compiled follow-up is justified until a later bounded contradiction or explicit need appears.",
        },
    ]


def build_snapshot(
    *,
    h14_guard: dict[str, Any],
    r11_summary: dict[str, Any],
    r12_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H14_core_first_reopen_guard/summary.json",
            "fields": {
                "stage_guard_state": h14_guard["summary"]["stage_guard_state"],
                "blocked_count": h14_guard["summary"]["blocked_count"],
                "active_stage": h14_guard["summary"]["active_stage"],
            },
        },
        {
            "source": "results/R11_geometry_fastpath_reaudit/summary.json",
            "fields": {
                "all_cases_exact": r11_summary["summary"]["current_exactness"]["all_cases_exact"],
                "median_cache_speedup_vs_bruteforce": r11_summary["summary"]["benchmark_reaudit"][
                    "median_cache_speedup_vs_bruteforce"
                ],
                "same_endpoint_fastpath_material": r11_summary["summary"]["same_endpoint_guard"][
                    "same_endpoint_fastpath_material"
                ],
            },
        },
        {
            "source": "results/R12_append_only_executor_long_horizon/summary.json",
            "fields": {
                "all_modes_exact": r12_summary["summary"]["free_running_baseline"]["all_modes_exact"],
                "max_exact_heldout_steps": r12_summary["summary"]["free_running_baseline"]["max_exact_heldout_steps"],
                "r8_row_count": r12_summary["summary"]["horizon_inventory"]["r8_row_count"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], p10_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    direct_refreeze_ready = not blocked_items
    return {
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "active_stage": "h15_refreeze_and_decision_sync",
        "guarded_reopen_stage": "h14_core_first_reopen_and_scope_lock",
        "next_stage": "next_full_plan_pending",
        "decision_state": "direct_refreeze_complete" if direct_refreeze_ready else "further_resolution_required",
        "r13_decision": "not_currently_needed" if direct_refreeze_ready else "re-evaluate_after_blockers",
        "r14_decision": "not_currently_justified" if direct_refreeze_ready else "re-evaluate_after_blockers",
        "release_commit_state": str(p10_summary["summary"]["release_commit_state"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "treat H15 as the current refrozen state, preserve H14 as the completed reopened packet, leave R13 inactive because no bounded executor gap is exposed, leave R14 unjustified because no compiled follow-up need has been shown, and require a later explicit full plan before any new active lane starts"
            if direct_refreeze_ready
            else "resolve the blocked H15 readiness items before refreeze or any optional follow-up is activated"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(
        h14_guard=inputs["h14_guard"],
        r11_summary=inputs["r11_summary"],
        r12_summary=inputs["r12_summary"],
    )
    summary = build_summary(checklist_rows, inputs["p10_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "h15_refreeze_and_decision_sync_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "h15_refreeze_and_decision_sync_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h15_refreeze_and_decision_sync",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/H14_core_first_reopen_guard/summary.json",
                "results/R11_geometry_fastpath_reaudit/summary.json",
                "results/R12_append_only_executor_long_horizon/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/P10_submission_archive_ready/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H15 Refreeze And Decision Sync\n\n"
        "Machine-readable completion summary for the direct H15 refreeze after the R11/R12 reopen outputs.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
