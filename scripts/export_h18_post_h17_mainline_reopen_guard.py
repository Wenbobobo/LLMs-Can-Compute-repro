"""Export a machine-readable planning guard for the H18 same-scope reopen."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H18_post_h17_mainline_reopen_guard"


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


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def load_inputs() -> dict[str, Any]:
    paths = {
        "readme_text": ROOT / "README.md",
        "status_text": ROOT / "STATUS.md",
        "publication_readme_text": ROOT / "docs" / "publication_record" / "README.md",
        "current_stage_driver_text": ROOT / "docs" / "publication_record" / "current_stage_driver.md",
        "master_plan_text": ROOT / "docs" / "plans" / "2026-03-21-h18-unattended-mainline-master-plan.md",
        "active_wave_plan_text": ROOT / "tmp" / "active_wave_plan.md",
        "h18_readme_text": ROOT / "docs" / "milestones" / "H18_post_h17_mainline_reopen_and_scope_lock" / "README.md",
        "h18_status_text": ROOT / "docs" / "milestones" / "H18_post_h17_mainline_reopen_and_scope_lock" / "status.md",
        "h18_todo_text": ROOT / "docs" / "milestones" / "H18_post_h17_mainline_reopen_and_scope_lock" / "todo.md",
        "h18_acceptance_text": ROOT / "docs" / "milestones" / "H18_post_h17_mainline_reopen_and_scope_lock" / "acceptance.md",
        "h18_artifact_index_text": ROOT / "docs" / "milestones" / "H18_post_h17_mainline_reopen_and_scope_lock" / "artifact_index.md",
        "h18_decision_log_text": ROOT / "docs" / "milestones" / "H18_post_h17_mainline_reopen_and_scope_lock" / "decision_log.md",
        "r19_todo_text": ROOT / "docs" / "milestones" / "R19_d0_pointer_like_surface_generalization_gate" / "todo.md",
        "r20_todo_text": ROOT / "docs" / "milestones" / "R20_d0_runtime_mechanism_ablation_matrix" / "todo.md",
        "r21_todo_text": ROOT / "docs" / "milestones" / "R21_d0_exact_executor_boundary_break_map" / "todo.md",
        "h19_todo_text": ROOT / "docs" / "milestones" / "H19_refreeze_and_next_scope_decision" / "todo.md",
        "f2_todo_text": ROOT / "docs" / "milestones" / "F2_future_frontier_recheck_activation_matrix" / "todo.md",
        "p12_todo_text": ROOT / "docs" / "milestones" / "P12_manuscript_and_manifest_maintenance" / "todo.md",
        "p13_todo_text": ROOT / "docs" / "milestones" / "P13_public_surface_sync_and_repo_hygiene" / "todo.md",
        "h17_summary_text": ROOT / "results" / "H17_refreeze_and_conditional_frontier_recheck" / "summary.json",
        "m7_decision_text": ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json",
        "worktree_summary_text": ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json",
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
    master_plan_text: str,
    active_wave_plan_text: str,
    h18_readme_text: str,
    h18_status_text: str,
    h18_todo_text: str,
    h18_acceptance_text: str,
    h18_artifact_index_text: str,
    h18_decision_log_text: str,
    r19_todo_text: str,
    r20_todo_text: str,
    r21_todo_text: str,
    h19_todo_text: str,
    f2_todo_text: str,
    p12_todo_text: str,
    p13_todo_text: str,
    h17_summary_text: str,
    h17_summary: dict[str, Any],
    m7_decision_text: str,
    m7_decision: dict[str, Any],
    worktree_summary_text: str,
    worktree_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "root_and_public_docs_keep_h17_frozen_and_h18_planned",
            "status": "pass"
            if (
                contains_all(
                    readme_text,
                    [
                        "`h17` has now recorded the post-`h16` frozen same-scope state",
                        "`h18_post_h17_mainline_reopen_and_scope_lock`",
                    ],
                )
                or contains_all(
                    readme_text,
                    [
                        "`h17` is now preserved as the prior same-scope refreeze",
                        "`results/h18_post_h17_mainline_reopen_guard/summary.json`",
                        "`h19_refreeze_and_next_scope_decision`",
                    ],
                )
                or contains_all(
                    readme_text,
                    [
                        "`h21_refreeze_after_r22_r23`",
                        "`results/h18_post_h17_mainline_reopen_guard/summary.json`",
                        "`results/h17_refreeze_and_conditional_frontier_recheck/summary.json`",
                    ],
                )
            )
            and (
                contains_all(
                    status_text,
                    [
                        "the current active post-`p9` operational stage is `h17_refreeze_and_conditional_frontier_recheck`",
                        "the next planned same-scope operational wave is `h18_post_h17_mainline_reopen_and_scope_lock`",
                    ],
                )
                or contains_all(
                    status_text,
                    [
                        "the current active post-`p9` operational stage is `h19_refreeze_and_next_scope_decision`",
                        "`h17_refreeze_and_conditional_frontier_recheck` is now the preserved prior",
                        "`h18` has now exported a machine-readable planning guard",
                    ],
                )
                or contains_all(
                    status_text,
                    [
                        "the current active post-`p9` operational stage is `h21_refreeze_after_r22_r23`",
                        "`h17_refreeze_and_conditional_frontier_recheck` is now the preserved prior",
                        "`h18` has now exported a machine-readable planning guard",
                    ],
                )
            )
            and (
                contains_all(
                    publication_readme_text,
                    [
                        "canonical `active_driver` for the current `h17` frozen same-scope state",
                        "`docs/plans/2026-03-21-h18-unattended-mainline-master-plan.md`",
                        "`h17` still kept as the frozen scientific state",
                    ],
                )
                or contains_all(
                    publication_readme_text,
                    [
                        "canonical `active_driver` for the current `h19` frozen same-endpoint state",
                        "`docs/plans/2026-03-21-h18-unattended-mainline-master-plan.md`",
                        "`results/h18_post_h17_mainline_reopen_guard/summary.json`",
                        "`h17` is the preserved prior same-scope refreeze",
                    ],
                )
                or contains_all(
                    publication_readme_text,
                    [
                        "keeps `h21` as the current frozen same-endpoint state",
                        "`results/h18_post_h17_mainline_reopen_guard/summary.json`",
                        "keeps `h17` as the preserved prior same-scope refreeze decision",
                    ],
                )
            )
            and (
                contains_all(
                    current_stage_driver_text,
                    [
                        "the next planned operational wave is `h18_post_h17_mainline_reopen_and_scope_lock`",
                        "`h17` is still the current frozen scientific state",
                        "`r19_d0_pointer_like_surface_generalization_gate`",
                        "`p13_public_surface_sync_and_repo_hygiene`",
                    ],
                )
                or contains_all(
                    current_stage_driver_text,
                    [
                        "the current active stage is:",
                        "`h19_refreeze_and_next_scope_decision`",
                        "`h17_refreeze_and_conditional_frontier_recheck` as the prior",
                        "`h18/r19/r20/r21` as the completed same-endpoint mainline reopen",
                        "`h19_refreeze_and_next_scope_decision`",
                        "`p13_public_surface_sync_and_repo_hygiene`",
                    ],
                )
                or contains_all(
                    current_stage_driver_text,
                    [
                        "`h21_refreeze_after_r22_r23` is the current frozen same-endpoint control stage.",
                        "`h18_post_h17_mainline_reopen_and_scope_lock` is preserved as the completed same-endpoint planning guard rather than the frozen state.",
                        "`h17_refreeze_and_conditional_frontier_recheck` is preserved as the prior same-scope refreeze control stage",
                        "`p12_manuscript_and_manifest_maintenance` is the immediate next-priority manuscript / manifest lane",
                    ],
                )
            )
            else "blocked",
            "notes": "H18 should remain readable as the historical planning guard even after the current public surface advances to landed H19.",
        },
        {
            "item_id": "master_plan_and_active_wave_handoff_agree_on_lane_order",
            "status": "pass"
            if contains_all(
                master_plan_text,
                [
                    "`h18_post_h17_mainline_reopen_and_scope_lock`",
                    "`r19_d0_pointer_like_surface_generalization_gate`",
                    "`r20_d0_runtime_mechanism_ablation_matrix`",
                    "`r21_d0_exact_executor_boundary_break_map`",
                    "`h19_refreeze_and_next_scope_decision`",
                    "`p13_public_surface_sync_and_repo_hygiene`",
                ],
            )
            and (
                contains_all(
                    active_wave_plan_text,
                    [
                        "`h18_post_h17_mainline_reopen_and_scope_lock`",
                        "`wip/h18-r19`",
                        "`wt-r21`",
                        "`wt-f2`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "`r19_d0_pointer_like_surface_generalization_gate`",
                        "`wip/h18-r19`",
                        "`wt-r21`",
                        "`wt-f2`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "`r20_d0_runtime_mechanism_ablation_matrix`",
                        "`wip/h18-r19`",
                        "`wt-r21`",
                        "`wt-f2`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "`r21_d0_exact_executor_boundary_break_map`",
                        "`wip/h18-r19`",
                        "`wt-r21`",
                        "`wt-f2`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "`h19_refreeze_and_next_scope_decision`",
                        "`wip/h18-r19`",
                        "`wt-r21`",
                        "`wt-f2`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "`h20_post_h19_mainline_reentry_and_hygiene_split`",
                        "`wip/h20-hygiene`",
                        "`wt-r23`",
                        "`wt-p12`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "`p12_manuscript_and_manifest_maintenance`",
                        "`h21_refreeze_after_r22_r23` as the current frozen scientific input",
                        "`wip/p12-ledger`",
                        "`wip/f2-planning`",
                    ],
                )
            )
            else "blocked",
            "notes": "The unattended plan and the short handoff file should expose the same next-wave structure, even after the active handoff advances from H18 setup into R19 execution.",
        },
        {
            "item_id": "h18_scope_lock_and_dirty_tree_split_are_explicit",
            "status": "pass"
            if contains_all(
                h18_readme_text,
                [
                    "planned same-scope reopen lane after the `h17` frozen state",
                    "without widening beyond the current tiny typed-bytecode `d0` endpoint",
                ],
            )
            and contains_all(
                h18_status_text,
                [
                    "`h17` remains the current frozen same-scope state",
                    "dirty-tree split and worktree ownership are documented",
                ],
            )
            and contains_all(
                h18_todo_text,
                [
                    "split the current dirty tree",
                    "decision log",
                    "machine-readable `h18` reopen guard",
                ],
            )
            and contains_all(
                h18_acceptance_text,
                [
                    "`h17` remains the explicit current frozen state",
                    "`h18 -> r19 -> r20 -> r21 -> h19 -> p13`",
                ],
            )
            and contains_all(
                h18_decision_log_text,
                [
                    "prior-wave `h16/h17/r15/r16/r17/r18` closeout",
                    "next-wave runtime workspace",
                    "later `p13` public-surface and repo-hygiene sync",
                    "`wt-r19`",
                    "`wt-f2`",
                ],
            )
            else "blocked",
            "notes": "H18 should make the split and ownership explicit before the unattended runtime wave starts.",
        },
        {
            "item_id": "next_wave_scaffolds_are_actionable_and_bounded",
            "status": "pass"
            if contains_all(
                r19_todo_text,
                [
                    "held-out family and seed manifest",
                    "`linear_exact`",
                    "`pointer_like_exact`",
                ],
            )
            and contains_all(
                r20_todo_text,
                [
                    "`pointer_like_shuffled`",
                    "`address_oblivious_control`",
                    "single mechanism verdict",
                ],
            )
            and contains_all(
                r21_todo_text,
                [
                    "bounded grid",
                    "first-fail digest",
                    "boundary verdict",
                ],
            )
            and contains_all(
                h19_todo_text,
                [
                    "`r19`, `r20`, and `r21`",
                    "machine-readable `h19` summary",
                ],
            )
            and contains_all(
                f2_todo_text,
                [
                    "planning-only",
                    "minimum evidence bundle",
                ],
            )
            and contains_all(
                p12_todo_text,
                [
                    "claim ladders",
                    "negative-result ledgers",
                ],
            )
            and contains_all(
                p13_todo_text,
                [
                    "`h19`",
                    "public-surface sync remain reviewable",
                ],
            )
            and contains_all(
                h18_artifact_index_text,
                [
                    "results/h18_post_h17_mainline_reopen_guard/summary.json",
                    "scripts/export_h18_post_h17_mainline_reopen_guard.py",
                ],
            )
            else "blocked",
            "notes": "R19/R20/R21/H19 plus the background lanes should already be defined as bounded follow-ups.",
        },
        {
            "item_id": "no_widening_and_frozen_input_controls_remain_in_force",
            "status": "pass"
            if h17_summary["summary"]["decision_state"] == "same_scope_refreeze_complete"
            and h17_summary["summary"]["frontier_recheck_decision"] == "conditional_plan_required"
            and m7_decision["summary"]["frontend_widening_authorized"] is False
            and m7_decision["summary"]["public_demo_authorized"] is False
            and contains_all(
                m7_decision_text,
                [
                    "\"frontend_widening_authorized\": false",
                    "\"public_demo_authorized\": false",
                ],
            )
            else "blocked",
            "notes": "H18 must start from the frozen H17 state and preserve the M7 no-widening decision.",
        },
        {
            "item_id": "release_worktree_state_remains_explicit_before_branching",
            "status": "pass"
            if release_commit_state_from_summary(worktree_summary)
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            and contains_all(
                worktree_summary_text,
                [
                    "\"release_commit_state\": \"dirty_worktree_release_commit_blocked\"",
                    "\"git_diff_check_state\": \"warnings_only\"",
                ],
            )
            else "blocked",
            "notes": "The new wave should keep the dirty-tree constraint explicit rather than pretending the repo is clean.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H17_refreeze_and_conditional_frontier_recheck/summary.json",
            "fields": {
                "decision_state": inputs["h17_summary"]["summary"]["decision_state"],
                "frontier_recheck_decision": inputs["h17_summary"]["summary"]["frontier_recheck_decision"],
                "release_commit_state": inputs["h17_summary"]["summary"]["release_commit_state"],
            },
        },
        {
            "source": "results/M7_frontend_candidate_decision/decision_summary.json",
            "fields": {
                "frontend_widening_authorized": inputs["m7_decision"]["summary"]["frontend_widening_authorized"],
                "public_demo_authorized": inputs["m7_decision"]["summary"]["public_demo_authorized"],
                "decision_status": inputs["m7_decision"]["summary"]["decision_status"],
            },
        },
        {
            "source": "results/release_worktree_hygiene_snapshot/summary.json",
            "fields": {
                "release_commit_state": inputs["worktree_summary"]["summary"]["release_commit_state"],
                "changed_path_count": inputs["worktree_summary"]["summary"]["changed_path_count"],
                "untracked_path_count": inputs["worktree_summary"]["summary"]["untracked_path_count"],
            },
        },
        {
            "source": "tmp/active_wave_plan.md",
            "fields": {
                "current_wave_is_h18_to_r21": (
                    contains_all(
                        inputs["active_wave_plan_text"],
                        ["`h18_post_h17_mainline_reopen_and_scope_lock`"],
                    )
                    or contains_all(
                        inputs["active_wave_plan_text"],
                        ["`r19_d0_pointer_like_surface_generalization_gate`"],
                    )
                    or contains_all(
                        inputs["active_wave_plan_text"],
                        ["`r20_d0_runtime_mechanism_ablation_matrix`"],
                    )
                or contains_all(
                    inputs["active_wave_plan_text"],
                    ["`r21_d0_exact_executor_boundary_break_map`"],
                )
                    or contains_all(
                        inputs["active_wave_plan_text"],
                        ["`h19_refreeze_and_next_scope_decision`"],
                    )
                    or contains_all(
                        inputs["active_wave_plan_text"],
                        ["`h20_post_h19_mainline_reentry_and_hygiene_split`"],
                    )
                ),
                "worktree_map_present": (
                    contains_all(
                        inputs["active_wave_plan_text"],
                        ["`wip/h18-r19`", "`wip/h18-r20`", "`wip/h18-r21`", "`wip/h18-f2`"],
                    )
                    or contains_all(
                        inputs["active_wave_plan_text"],
                        ["`wip/h20-hygiene`", "`wip/r22-boundary`", "`wip/r23-systems`", "`wip/p12-ledger`"],
                    )
                ),
            },
        },
    ]


def build_summary(
    checklist_rows: list[dict[str, object]],
    h17_summary: dict[str, Any],
    m7_decision: dict[str, Any],
    worktree_summary: dict[str, Any],
    active_wave_plan_text: str,
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    current_lane = current_wave_from_active_plan(active_wave_plan_text)
    if current_lane == "h19_refreeze_and_next_scope_decision":
        next_priority_lane = "h19_refreeze_and_next_scope_decision"
    elif current_lane in {
        "h20_post_h19_mainline_reentry_and_hygiene_split",
        "r22_d0_true_boundary_localization_gate",
        "r23_d0_same_endpoint_systems_overturn_gate",
        "h21_refreeze_after_r22_r23",
        "p12_manuscript_and_manifest_maintenance",
        "p13_public_surface_sync_and_repo_hygiene",
        "f2_future_frontier_recheck_activation_matrix",
    }:
        next_priority_lane = "h19_refreeze_and_next_scope_decision"
    elif current_lane == "r21_d0_exact_executor_boundary_break_map":
        next_priority_lane = "r21_d0_exact_executor_boundary_break_map"
    elif current_lane == "r20_d0_runtime_mechanism_ablation_matrix":
        next_priority_lane = "r20_d0_runtime_mechanism_ablation_matrix"
    else:
        next_priority_lane = "r19_d0_pointer_like_surface_generalization_gate"
    return {
        "current_paper_phase": "h18_post_h17_mainline_reopen_planned",
        "current_frozen_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "planned_reopen_stage": "h18_post_h17_mainline_reopen_and_scope_lock",
        "stage_guard_state": "planned_same_scope_reopen_ready" if not blocked_items else "blocked",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "frontier_recheck_state": str(h17_summary["summary"]["frontier_recheck_decision"]),
        "frontend_widening_authorized": bool(m7_decision["summary"]["frontend_widening_authorized"]),
        "release_commit_state": release_commit_state_from_summary(worktree_summary),
        "lane_order": "h18_then_r19_then_r20_then_r21_then_h19_then_p13",
        "next_priority_lane": next_priority_lane,
        "background_lanes": [
            "f2_future_frontier_recheck_activation_matrix",
            "p12_manuscript_and_manifest_maintenance",
        ],
        "changed_path_count": int(worktree_summary["summary"]["changed_path_count"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            (
                (
                    "preserve H17 as the frozen input, advance into H19 on the landed R19/R20/R21 packet, keep F2/P12 bounded to the saved H18 plan, and avoid outward sync commits until the dirty-tree split is isolated"
                    if next_priority_lane == "h19_refreeze_and_next_scope_decision"
                    else (
                        "preserve H17 as the frozen input, advance into R21 on the landed R20 mechanism lane, keep H19/F2/P12 bounded to the saved H18 plan, and avoid outward sync commits until the dirty-tree split is isolated"
                        if next_priority_lane == "r21_d0_exact_executor_boundary_break_map"
                        else (
                            "preserve H17 as the frozen input, advance into R20 on the landed R19 runtime gate, keep R21/F2/P12 bounded to the saved H18 plan, and avoid outward sync commits until the dirty-tree split is isolated"
                            if next_priority_lane == "r20_d0_runtime_mechanism_ablation_matrix"
                            else "preserve H17 as the frozen input, start R19 on the admitted D0 runtime surface, keep R20/R21/F2/P12 bounded to the saved H18 plan, and avoid outward sync commits until the dirty-tree split is isolated"
                        )
                    )
                )
            )
            if not blocked_items
            else "resolve the blocked H18 planning inputs before treating the next same-scope wave as ready for unattended execution"
        ),
}


def current_wave_from_active_plan(active_wave_plan_text: str) -> str | None:
    capture = False
    for line in active_wave_plan_text.splitlines():
        stripped = line.strip()
        if stripped.lower() == "## current wave":
            capture = True
            continue
        if capture and stripped:
            return stripped.strip("`").lower()
    return None


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(
        checklist_rows,
        inputs["h17_summary"],
        inputs["m7_decision"],
        inputs["worktree_summary"],
        inputs["active_wave_plan_text"],
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h18_post_h17_mainline_reopen_guard_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h18_post_h17_mainline_reopen_guard_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h18_post_h17_mainline_reopen_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/plans/2026-03-21-h18-unattended-mainline-master-plan.md",
                "tmp/active_wave_plan.md",
                "docs/milestones/H18_post_h17_mainline_reopen_and_scope_lock/README.md",
                "docs/milestones/H18_post_h17_mainline_reopen_and_scope_lock/status.md",
                "docs/milestones/H18_post_h17_mainline_reopen_and_scope_lock/todo.md",
                "docs/milestones/H18_post_h17_mainline_reopen_and_scope_lock/acceptance.md",
                "docs/milestones/H18_post_h17_mainline_reopen_and_scope_lock/artifact_index.md",
                "docs/milestones/H18_post_h17_mainline_reopen_and_scope_lock/decision_log.md",
                "docs/milestones/R19_d0_pointer_like_surface_generalization_gate/todo.md",
                "docs/milestones/R20_d0_runtime_mechanism_ablation_matrix/todo.md",
                "docs/milestones/R21_d0_exact_executor_boundary_break_map/todo.md",
                "docs/milestones/H19_refreeze_and_next_scope_decision/todo.md",
                "docs/milestones/F2_future_frontier_recheck_activation_matrix/todo.md",
                "docs/milestones/P12_manuscript_and_manifest_maintenance/todo.md",
                "docs/milestones/P13_public_surface_sync_and_repo_hygiene/todo.md",
                "results/H17_refreeze_and_conditional_frontier_recheck/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H18 Post-H17 Mainline Reopen Guard\n\n"
        "Machine-readable planning guard for the next same-scope runtime wave after the frozen H17 state.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
