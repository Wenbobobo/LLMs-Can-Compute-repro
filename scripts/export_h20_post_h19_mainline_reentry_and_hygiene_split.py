"""Export the H20 post-H19 reentry and hygiene split summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H20_post_h19_mainline_reentry_and_hygiene_split"


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


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles):
            if line not in seen:
                hits.append(line)
                seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def load_inputs() -> dict[str, Any]:
    paths = {
        "master_plan_text": ROOT / "docs" / "plans" / "2026-03-21-post-h19-mainline-reentry-design.md",
        "active_wave_plan_text": ROOT / "tmp" / "active_wave_plan.md",
        "h20_readme_text": ROOT / "docs" / "milestones" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "README.md",
        "h20_status_text": ROOT / "docs" / "milestones" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "status.md",
        "h20_todo_text": ROOT / "docs" / "milestones" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "todo.md",
        "h20_acceptance_text": ROOT / "docs" / "milestones" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "acceptance.md",
        "h20_artifact_index_text": ROOT / "docs" / "milestones" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "artifact_index.md",
        "h20_decision_log_text": ROOT / "docs" / "milestones" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "decision_log.md",
        "r22_todo_text": ROOT / "docs" / "milestones" / "R22_d0_true_boundary_localization_gate" / "todo.md",
        "r23_todo_text": ROOT / "docs" / "milestones" / "R23_d0_same_endpoint_systems_overturn_gate" / "todo.md",
        "h21_todo_text": ROOT / "docs" / "milestones" / "H21_refreeze_after_r22_r23" / "todo.md",
        "p12_status_text": ROOT / "docs" / "milestones" / "P12_manuscript_and_manifest_maintenance" / "status.md",
        "p12_todo_text": ROOT / "docs" / "milestones" / "P12_manuscript_and_manifest_maintenance" / "todo.md",
        "p13_todo_text": ROOT / "docs" / "milestones" / "P13_public_surface_sync_and_repo_hygiene" / "todo.md",
        "h19_summary_text": ROOT / "results" / "H19_refreeze_and_next_scope_decision" / "summary.json",
        "worktree_summary_text": ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json",
    }
    inputs: dict[str, Any] = {key: read_text(path) for key, path in paths.items()}
    for key, path in paths.items():
        if key.endswith("_text") and path.suffix == ".json":
            inputs[key.removesuffix("_text")] = read_json(path)
    return inputs


def build_checklist_rows(
    *,
    master_plan_text: str,
    active_wave_plan_text: str,
    h20_readme_text: str,
    h20_status_text: str,
    h20_todo_text: str,
    h20_acceptance_text: str,
    h20_artifact_index_text: str,
    h20_decision_log_text: str,
    r22_todo_text: str,
    r23_todo_text: str,
    h21_todo_text: str,
    p12_status_text: str,
    p12_todo_text: str,
    p13_todo_text: str,
    h19_summary_text: str,
    h19_summary: dict[str, Any],
    worktree_summary_text: str,
    worktree_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h19 = h19_summary["summary"]
    worktree = worktree_summary["summary"]

    return [
        {
            "item_id": "saved_plan_and_active_wave_describe_post_h19_reentry",
            "status": "pass"
            if contains_all(
                master_plan_text,
                [
                    "two frontier-activation conditions remain unsatisfied",
                    "`h20_post_h19_mainline_reentry_and_hygiene_split`",
                    "`r22_d0_true_boundary_localization_gate`",
                    "`r23_d0_same_endpoint_systems_overturn_gate`",
                    "`h21_refreeze_after_r22_r23`",
                ],
            )
            and (
                contains_all(
                    active_wave_plan_text,
                    [
                        "## current wave",
                        "`h20_post_h19_mainline_reentry_and_hygiene_split`",
                        "`h19_refreeze_and_next_scope_decision` as the frozen scientific input",
                        "`r22` and `r23`",
                    ],
                )
                or contains_all(
                    active_wave_plan_text,
                    [
                        "## current wave",
                        "`p12_manuscript_and_manifest_maintenance`",
                        "`h21_refreeze_after_r22_r23` as the current frozen scientific input",
                        "`r22/r23/h21` packet",
                    ],
                )
            )
            else "blocked",
            "notes": "H20 should begin from one saved plan plus one refreshed active-wave handoff.",
        },
        {
            "item_id": "h20_docs_define_tree_isolation_without_scope_widening",
            "status": "pass"
            if contains_all(
                h20_readme_text,
                [
                    "operational reentry stage after `h19`",
                    "machine-readable split",
                    "mixed workspace",
                ],
            )
            and contains_all(
                h20_status_text,
                [
                    "`h19_refreeze_and_next_scope_decision` remains the current frozen scientific input",
                    "prior-wave closeout, next-wave runtime science, and downstream public-surface sync",
                    "must not widen the endpoint",
                ],
            )
            and contains_all(
                h20_todo_text,
                [
                    "save the post-`h19` mainline reentry design",
                    "`r22_d0_true_boundary_localization_gate`",
                    "`r23_d0_same_endpoint_systems_overturn_gate`",
                    "`h21_refreeze_after_r22_r23`",
                    "machine-readable `h20` reentry/hygiene guard",
                ],
            )
            and contains_all(
                h20_acceptance_text,
                [
                    "`h19` is still the frozen current stage",
                    "`h20 -> r22 -> r23 -> h21 -> p13`",
                    "no widened endpoint",
                ],
            )
            and contains_all(
                h20_artifact_index_text,
                [
                    "scripts/export_h20_post_h19_mainline_reentry_and_hygiene_split.py",
                    "results/h20_post_h19_mainline_reentry_and_hygiene_split/summary.json",
                ],
            )
            and contains_all(
                h20_decision_log_text,
                [
                    "`wt-h20`",
                    "`wt-r22`",
                    "`wt-r23`",
                    "`wt-p12`",
                    "root/publication outward wording downstream until `h21` lands",
                ],
            )
            else "blocked",
            "notes": "H20 should be an operational split stage, not a hidden scope lift.",
        },
        {
            "item_id": "h19_is_preserved_and_the_dirty_tree_blocker_is_machine_readable",
            "status": "pass"
            if h19["current_paper_phase"] == "h19_refreeze_and_next_scope_decision_complete"
            and h19["active_stage"] == "h19_refreeze_and_next_scope_decision"
            and h19["decision_state"] == "same_endpoint_refreeze_complete"
            and h19["next_priority_lane"] == "p13_public_surface_sync_and_repo_hygiene"
            and h19["release_commit_state"] == "dirty_worktree_release_commit_blocked"
            and worktree["release_commit_state"] == "dirty_worktree_release_commit_blocked"
            and int(worktree["changed_path_count"]) > 0
            and contains_all(
                p13_todo_text,
                [
                    "[ ] split staged commits",
                    "mixed dirty tree",
                ],
            )
            and contains_all(
                h19_summary_text,
                [
                    "\"decision_state\": \"same_endpoint_refreeze_complete\"",
                    "\"next_priority_lane\": \"p13_public_surface_sync_and_repo_hygiene\"",
                ],
            )
            and contains_all(
                worktree_summary_text,
                [
                    "\"release_commit_state\": \"dirty_worktree_release_commit_blocked\"",
                    "\"changed_path_count\":",
                ],
            )
            else "blocked",
            "notes": "The current blocker is an explicit hygiene problem, not a contradiction in the H19 evidence state.",
        },
        {
            "item_id": "r22_r23_and_h21_scaffolds_are_actionable",
            "status": "pass"
            if contains_all(
                r22_todo_text,
                [
                    "extend the `r21` grid",
                    "first-fail diagnostics",
                    "`first_boundary_failure_localized`",
                    "`no_failure_in_extended_grid`",
                ],
            )
            and contains_all(
                r23_todo_text,
                [
                    "`pointer_like_exact`",
                    "current best reference/spec",
                    "component attribution",
                    "`systems_materially_positive`",
                    "`systems_still_mixed`",
                ],
            )
            and contains_all(
                h21_todo_text,
                [
                    "`r22`",
                    "`r23`",
                    "`supported_here`, `unsupported_here`, and `disconfirmed_here`",
                    "`f2` activation conditions",
                ],
            )
            else "blocked",
            "notes": "The next science and refreeze lanes should be decision-complete before implementation begins.",
        },
        {
            "item_id": "p12_and_p13_remain_downstream_control_lanes",
            "status": "pass"
            if contains_all(
                p12_status_text,
                [
                    "downstream-only",
                    "publishable evidence assets",
                    "blog-style outward prose remains blocked here",
                ],
            )
            and contains_all(
                p12_todo_text,
                [
                    "claim ladders and evidence tables",
                    "experiment manifests and negative-result ledgers",
                    "keep readme and publication-facing wording downstream of evidence",
                ],
            )
            and contains_all(
                p13_todo_text,
                [
                    "[ ] split staged commits",
                    "public-surface sync remain reviewable",
                ],
            )
            else "blocked",
            "notes": "Background lanes should stay subordinate to landed evidence and tree hygiene.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-21-post-h19-mainline-reentry-design.md": (
            "master_plan_text",
            [
                "two frontier-activation conditions remain unsatisfied",
                "h20_post_h19_mainline_reentry_and_hygiene_split",
                "r22_d0_true_boundary_localization_gate",
                "r23_d0_same_endpoint_systems_overturn_gate",
            ],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            [
                "H20_post_h19_mainline_reentry_and_hygiene_split",
                "H19_refreeze_and_next_scope_decision",
                "R22",
                "R23",
            ],
        ),
        "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/decision_log.md": (
            "h20_decision_log_text",
            [
                "wt-h20",
                "wt-r22",
                "wt-r23",
                "wt-p12",
            ],
        ),
        "docs/milestones/P13_public_surface_sync_and_repo_hygiene/todo.md": (
            "p13_todo_text",
            [
                "[ ] Split staged commits",
                "mixed dirty tree",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    rows.append(
        {
            "path": "results/H19_refreeze_and_next_scope_decision/summary.json",
            "summary_digest": {
                "current_paper_phase": inputs["h19_summary"]["summary"]["current_paper_phase"],
                "decision_state": inputs["h19_summary"]["summary"]["decision_state"],
                "next_priority_lane": inputs["h19_summary"]["summary"]["next_priority_lane"],
            },
        }
    )
    rows.append(
        {
            "path": "results/release_worktree_hygiene_snapshot/summary.json",
            "summary_digest": {
                "changed_path_count": inputs["worktree_summary"]["summary"]["changed_path_count"],
                "release_commit_state": inputs["worktree_summary"]["summary"]["release_commit_state"],
            },
        }
    )
    return rows


def build_summary(
    checklist_rows: list[dict[str, object]],
    h19_summary: dict[str, Any],
    worktree_summary: dict[str, Any],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    h19 = h19_summary["summary"]
    worktree = worktree_summary["summary"]
    return {
        "current_paper_phase": "h20_post_h19_mainline_reentry_active",
        "current_frozen_stage": "h19_refreeze_and_next_scope_decision",
        "reentry_state": (
            "dirty_tree_isolation_required_before_next_science_commits" if not blocked_items else "blocked"
        ),
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "h19_decision_state": str(h19["decision_state"]),
        "future_frontier_review_state": str(h19["future_frontier_review_state"]),
        "unsatisfied_frontier_activation_conditions": [
            "true_executor_boundary_localization",
            "current_scope_systems_story_materially_positive",
        ],
        "commit_split_state": "pending_in_dirty_tree",
        "lane_order": "h20_then_r22_then_r23_then_h21_then_p13",
        "next_priority_lanes": [
            "r22_d0_true_boundary_localization_gate",
            "r23_d0_same_endpoint_systems_overturn_gate",
        ],
        "background_lanes": [
            "p12_manuscript_and_manifest_maintenance",
            "f2_future_frontier_recheck_activation_matrix",
        ],
        "release_commit_state": str(worktree["release_commit_state"]),
        "changed_path_count": int(worktree["changed_path_count"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "finish isolating the dirty tree into the H20 buckets, land the H20 guard, then run R22 and R23 in parallel on separate write sets while keeping H19 frozen and outward docs downstream"
            if not blocked_items
            else "resolve the blocked H20 planning inputs before treating the next same-endpoint wave as ready to execute"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs["h19_summary"], inputs["worktree_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h20_post_h19_mainline_reentry_and_hygiene_split_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h20_post_h19_mainline_reentry_and_hygiene_split_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h20_post_h19_mainline_reentry_and_hygiene_split",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/plans/2026-03-21-post-h19-mainline-reentry-design.md",
                "tmp/active_wave_plan.md",
                "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/README.md",
                "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/status.md",
                "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/todo.md",
                "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/acceptance.md",
                "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/artifact_index.md",
                "docs/milestones/H20_post_h19_mainline_reentry_and_hygiene_split/decision_log.md",
                "docs/milestones/R22_d0_true_boundary_localization_gate/todo.md",
                "docs/milestones/R23_d0_same_endpoint_systems_overturn_gate/todo.md",
                "docs/milestones/H21_refreeze_after_r22_r23/todo.md",
                "docs/milestones/P12_manuscript_and_manifest_maintenance/status.md",
                "docs/milestones/P12_manuscript_and_manifest_maintenance/todo.md",
                "docs/milestones/P13_public_surface_sync_and_repo_hygiene/todo.md",
                "results/H19_refreeze_and_next_scope_decision/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H20 Post-H19 Mainline Reentry And Hygiene Split\n\n"
        "Machine-readable reentry guard for the post-H19 dirty-tree split before the next same-endpoint science lanes.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
