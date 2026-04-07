"""Export the post-H36 clean promotion-prep packet for P25."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P25_post_h36_clean_promotion_prep"


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
        "p25_readme_text": read_text(ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "README.md"),
        "p25_status_text": read_text(ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "status.md"),
        "p25_todo_text": read_text(ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "todo.md"),
        "p25_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "acceptance.md"
        ),
        "p25_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "artifact_index.md"
        ),
        "promotion_manifest_text": read_text(
            ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "promotion_manifest.md"
        ),
        "hygiene_summary_text": read_text(
            ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "hygiene_summary.md"
        ),
        "source_of_truth_delta_text": read_text(
            ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "source_of_truth_delta.md"
        ),
        "worktree_runbook_text": read_text(
            ROOT / "docs" / "milestones" / "P25_post_h36_clean_promotion_prep" / "worktree_runbook.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-h36-p25-f15-h37-control-design.md"),
        "h27_summary": read_json(ROOT / "results" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "summary.json"),
        "h36_summary": read_json(ROOT / "results" / "H36_post_r40_bounded_scalar_family_refreeze" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h27 = inputs["h27_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    return [
        {
            "item_id": "p25_docs_fix_source_of_truth_clean_prep_and_prepare_only_policy",
            "status": "pass"
            if contains_all(
                inputs["p25_readme_text"],
                [
                    "wip/h35-r40-p24-exec",
                    "without touching dirty `main`",
                    "not a new science lane",
                    "does not authorize a merge by momentum",
                ],
            )
            and contains_all(
                inputs["p25_status_text"],
                [
                    "completed operational promotion-prep lane",
                    "wip/h35-r40-p24-exec",
                    "wip/p25-f15-h37-exec",
                    "prepare_only",
                ],
            )
            and contains_all(
                inputs["p25_todo_text"],
                [
                    "scientific source-of-truth branch",
                    "`prepare_only` promotion policy",
                    "landed `h27 -> h36/p24` packet window",
                    "runtime execution and merge-by-momentum",
                ],
            )
            and contains_all(
                inputs["p25_acceptance_text"],
                [
                    "wip/h35-r40-p24-exec",
                    "wip/p25-f15-h37-exec",
                    "prepare_only",
                    "future promotion procedure",
                ],
            )
            and contains_all(
                inputs["p25_artifact_index_text"],
                [
                    "docs/plans/2026-03-23-post-h36-p25-f15-h37-control-design.md",
                    "docs/publication_record/current_stage_driver.md",
                    "tmp/active_wave_plan.md",
                    "results/h36_post_r40_bounded_scalar_family_refreeze/summary.json",
                ],
            )
            else "blocked",
            "notes": "P25 should stay operational-only, fix the true source branch, and keep promotion in prepare-only mode.",
        },
        {
            "item_id": "p25_manifest_delta_and_runbook_keep_main_untouched_and_inventory_only",
            "status": "pass"
            if contains_all(
                inputs["promotion_manifest_text"],
                [
                    "scientific source of truth",
                    "wip/h35-r40-p24-exec",
                    "wip/p25-f15-h37-exec",
                    "protected target branch",
                    "`prepare_only`",
                    "no direct merge inside `p25`",
                ],
            )
            and contains_all(
                inputs["hygiene_summary_text"],
                [
                    "clean scientific source of truth",
                    "`main` remains dirty and behind",
                    "inventory-only",
                    "not from the dirty integrated tree",
                ],
            )
            and contains_all(
                inputs["source_of_truth_delta_text"],
                [
                    "`main` currently lacks the landed branch window",
                    "group 1: same-endpoint closeout",
                    "group 4: family-first and bounded-scalar stack",
                    "do not treat the presence of this delta inventory as authorization to merge",
                ],
            )
            and contains_all(
                inputs["worktree_runbook_text"],
                [
                    "start from `wip/p25-f15-h37-exec`, not dirty `main`",
                    "inspect `git diff --stat main..wip/p25-f15-h37-exec`",
                    "merge only after `main` is clean enough",
                    "do not use `p25` as justification to activate `r41`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p25` is operational only",
                    "preserve `wip/h35-r40-p24-exec` as the scientific source of truth",
                    "preserve `main` as dirty and not directly touched",
                    "record a future promotion runbook, but not execute the promotion",
                ],
            )
            else "blocked",
            "notes": "The promotion manifest must encode inventory-only mechanics and keep both runtime execution and merge-by-momentum out of scope.",
        },
        {
            "item_id": "driver_wave_and_upstream_refreeze_treat_p25_as_completed_prep_not_merge_authorization",
            "status": "pass"
            if str(h27["active_stage"]) == "h27_refreeze_after_r32_r33_same_endpoint_decision"
            and str(h36["active_stage"]) == "h36_post_r40_bounded_scalar_family_refreeze"
            and str(h36["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "p25_post_h36_clean_promotion_prep",
                    "source_of_truth_branch = wip/h35-r40-p24-exec",
                    "promotion_mode = prepare_only",
                    "merge_authorized = false",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "p25_post_h36_clean_promotion_prep",
                    "wip/p25-f15-h37-exec",
                    "preserved prior clean promotion-prep lane",
                    "dirty `main` remains untouched by design in this wave",
                ],
            )
            else "blocked",
            "notes": "The repo entry surfaces should present P25 as a completed clean-prep lane above the landed H36 state, not as merge authorization.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h27 = inputs["h27_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    return [
        {
            "source": "results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json",
            "fields": {
                "active_stage": h27["active_stage"],
                "systems_verdict": h27["systems_verdict"],
                "next_priority_lane": h27["next_priority_lane"],
            },
        },
        {
            "source": "results/H36_post_r40_bounded_scalar_family_refreeze/summary.json",
            "fields": {
                "active_stage": h36["active_stage"],
                "decision_state": h36["decision_state"],
                "deferred_future_runtime_candidate": h36["deferred_future_runtime_candidate"],
                "next_required_lane": h36["next_required_lane"],
            },
        },
        {
            "source": "docs/milestones/P25_post_h36_clean_promotion_prep/promotion_manifest.md",
            "fields": {
                "source_of_truth_branch": "wip/h35-r40-p24-exec",
                "clean_prep_branch": "wip/p25-f15-h37-exec",
                "target_branch": "main",
                "promotion_mode": "prepare_only",
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "p25_post_h36_clean_promotion_prep_complete",
        "active_stage": "p25_post_h36_clean_promotion_prep",
        "source_of_truth_branch": "wip/h35-r40-p24-exec",
        "source_of_truth_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "source_of_truth_sync_packet": "p24_post_h36_bounded_scalar_runtime_sync",
        "clean_prep_branch": "wip/p25-f15-h37-exec",
        "clean_prep_worktree": "D:/zWenbo/AI/LLMCompute-worktrees/p25-f15-h37-exec",
        "target_branch": "main",
        "promotion_mode": "prepare_only",
        "merge_authorized": False,
        "scientific_lane_change_authorized": False,
        "included_packet_window": "h27_through_h36_p24_plus_saved_r41_design",
        "supported_here_count": 0,
        "unsupported_here_count": 0,
        "disconfirmed_here_count": 0,
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
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
