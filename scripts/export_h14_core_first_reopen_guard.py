"""Export a machine-readable guard for the preserved H14 core-first reopen packet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H14_core_first_reopen_guard"


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
        "h14_readme_text": ROOT / "docs" / "milestones" / "H14_core_first_reopen_and_scope_lock" / "README.md",
        "h14_status_text": ROOT / "docs" / "milestones" / "H14_core_first_reopen_and_scope_lock" / "status.md",
        "h14_artifact_index_text": ROOT / "docs" / "milestones" / "H14_core_first_reopen_and_scope_lock" / "artifact_index.md",
        "h13_result_digest_text": ROOT / "docs" / "milestones" / "H13_post_h12_rollover_and_next_stage_staging" / "result_digest.md",
        "h13_stage_health_summary_text": ROOT / "results" / "H13_post_h12_governance_stage_health" / "summary.json",
        "v1_timing_summary_text": ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup" / "summary.json",
        "h10_summary_text": ROOT / "results" / "H10_r7_reconciliation_guard" / "summary.json",
        "h11_summary_text": ROOT / "results" / "H11_post_h9_mainline_rollover_guard" / "summary.json",
        "h8_summary_text": ROOT / "results" / "H8_driver_replacement_guard" / "summary.json",
        "h6_summary_text": ROOT / "results" / "H6_mainline_rollover_guard" / "summary.json",
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
    h14_readme_text: str,
    h14_status_text: str,
    h14_artifact_index_text: str,
    h13_result_digest_text: str,
    h13_stage_health_summary_text: str,
    h13_stage_health_summary: dict[str, Any],
    v1_timing_summary_text: str,
    v1_timing_summary: dict[str, Any],
    h10_summary_text: str,
    h10_summary: dict[str, Any],
    h11_summary_text: str,
    h11_summary: dict[str, Any],
    h8_summary_text: str,
    h8_summary: dict[str, Any],
    h6_summary_text: str,
    h6_summary: dict[str, Any],
    worktree_summary_text: str,
    worktree_summary: dict[str, Any],
    m7_decision_text: str,
    m7_decision: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "current_stage_driver_exposes_h14_core_first_order",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`r11_geometry_fastpath_reaudit`",
                    "`r12_append_only_executor_long_horizon`",
                    "`r14_bounded_compiled_probe`",
                    "`h13_post_h12_rollover_and_next_stage_staging`",
                    "`v1_full_suite_validation_runtime_audit`",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint follow-up packet",
                ],
            )
            else "blocked",
            "notes": "The canonical driver should expose current H15 plus the preserved H14 packet and the required R11/R12-before-R14 ordering.",
        },
        {
            "item_id": "root_and_public_docs_expose_h14_without_widening",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "| `h13-v1` | completed governance/runtime handoff preserved as a control baseline",
                    "| `h14-h15` | completed bounded core-first reopen/refreeze packet",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "v1 remains a standing operational reference under the preserved `h13`",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`v1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`healthy_but_slow`",
                    "`h14 -> r11 -> r12 -> conditional r13 -> bounded r14 -> h15`",
                ],
            )
            and contains_all(
                publication_readme_text,
                [
                    "`h15` refreeze-and-decision-sync",
                    "`h14` / `r11` / `r12` remain the completed reopen packet",
                    "`h13` / `v1` remain the completed governance/runtime handoff",
                    "`h10` / `h11` / `r8` / `r9` / `r10` / `h12` remain the latest completed",
                ],
            )
            and contains_all(
                release_summary_text,
                [
                    "`h13/v1` is now the preserved governance/runtime handoff",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "`r11_geometry_fastpath_reaudit`",
                    "`r12_append_only_executor_long_horizon`",
                ],
            )
            else "blocked",
            "notes": "Root and publication-facing docs should agree on current H15 and preserved H14/H13 semantics.",
        },
        {
            "item_id": "h14_milestone_docs_track_scope_lock",
            "status": "pass"
            if contains_all(
                h14_readme_text,
                ["append-only trace semantics", "exact latest-write retrieval", "free-running executor closure"],
            )
            and contains_all(
                h14_status_text,
                [
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`h13_post_h12_rollover_and_next_stage_staging`",
                    "`r11_geometry_fastpath_reaudit`",
                    "`r12_append_only_executor_long_horizon`",
                    "`r13_small_model_executor_reactivation`",
                    "`r14_bounded_compiled_probe`",
                    "`h15_refreeze_and_decision_sync`",
                ],
            )
            and contains_all(
                h14_artifact_index_text,
                [
                    "2026-03-20-h14-core-first-reopen-design.md",
                    "2026-03-20-r11-geometry-fastpath-reaudit-design.md",
                    "2026-03-20-r12-append-only-executor-long-horizon-design.md",
                    "results/h14_core_first_reopen_guard/summary.json",
                    "results/h13_post_h12_governance_stage_health/summary.json",
                ],
            )
            else "blocked",
            "notes": "The H14 milestone docs should keep the completed scope lock explicit and machine-readable.",
        },
        {
            "item_id": "preserved_h13_handoff_remains_green",
            "status": "pass"
            if h13_stage_health_summary["summary"]["stage_health_state"] == "preserved_handoff_green"
            and blocked_count_from_summary(h13_stage_health_summary) == 0
            and contains_all(
                h13_result_digest_text,
                ["governance-only post-`h12` handoff", "did not authorize `r11`, `r12`, `r13`, or `r14`"],
            )
            and contains_all(
                h13_stage_health_summary_text,
                ["\"preserved_stage\": \"h13_post_h12_rollover_and_next_stage_staging\"", "\"blocked_count\": 0"],
            )
            else "blocked",
            "notes": "H14 should treat H13/V1 as preserved handoff state, not reopen it implicitly.",
        },
        {
            "item_id": "preserved_baseline_guards_are_green",
            "status": "pass"
            if blocked_count_from_summary(h10_summary) == 0
            and blocked_count_from_summary(h11_summary) == 0
            and blocked_count_from_summary(h8_summary) == 0
            and blocked_count_from_summary(h6_summary) == 0
            and contains_all(h11_summary_text, ["\"current_paper_phase\": \"h15_refreeze_and_decision_sync_complete\"", "\"blocked_count\": 0"])
            and contains_all(h10_summary_text, ["\"current_paper_phase\": \"h15_refreeze_and_decision_sync_complete\"", "\"blocked_count\": 0"])
            else "blocked",
            "notes": "The latest checkpoint plus the older direct/deeper baselines should stay green under H15.",
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
            "notes": "The preserved V1 runtime reference should remain operationally bounded while H15 remains the current refrozen stage.",
        },
        {
            "item_id": "release_worktree_and_no_widening_constraints_remain_explicit",
            "status": "pass"
            if release_commit_state_from_summary(worktree_summary)
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and diff_check_state_from_summary(worktree_summary) != "content_issues_present"
            and contains_all(
                worktree_summary_text,
                [
                    "\"release_commit_state\":",
                    "\"git_diff_check_state\":",
                ],
            )
            and m7_decision["summary"]["frontend_widening_authorized"] is False
            and m7_decision["summary"]["public_demo_authorized"] is False
            and str(m7_decision["summary"]["selected_candidate_id"]) == "stay_on_tiny_typed_bytecode"
            and contains_all(
                m7_decision_text,
                [
                    "\"frontend_widening_authorized\": false",
                    "\"public_demo_authorized\": false",
                    "\"selected_candidate_id\": \"stay_on_tiny_typed_bytecode\"",
                ],
            )
            else "blocked",
            "notes": "H14 should keep the runtime issue operationally bounded and the no-widening decision intact.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["`H15_refreeze_and_decision_sync`", "`H14_core_first_reopen_and_scope_lock`", "`R11_geometry_fastpath_reaudit`", "`R12_append_only_executor_long_horizon`"],
        ),
        "README.md": (
            "readme_text",
            ["| `H14-H15` | completed bounded core-first reopen/refreeze packet", "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`"],
        ),
        "STATUS.md": (
            "status_text",
            ["`H15_refreeze_and_decision_sync`", "`H14_core_first_reopen_and_scope_lock`", "`H14 -> R11 -> R12 -> conditional R13 -> bounded R14 -> H15`"],
        ),
        "docs/milestones/H14_core_first_reopen_and_scope_lock/status.md": (
            "h14_status_text",
            [
                "`R11_geometry_fastpath_reaudit`",
                "`R12_append_only_executor_long_horizon`",
                "`R13_small_model_executor_reactivation`",
                "`R14_bounded_compiled_probe`",
                "`H15_refreeze_and_decision_sync`",
            ],
        ),
        "docs/milestones/H14_core_first_reopen_and_scope_lock/artifact_index.md": (
            "h14_artifact_index_text",
            ["2026-03-20-h14-core-first-reopen-design.md", "results/H14_core_first_reopen_guard/summary.json"],
        ),
        "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/result_digest.md": (
            "h13_result_digest_text",
            ["governance-only post-`H12` handoff", "did not authorize `R11`, `R12`, `R13`, or `R14`"],
        ),
    }
    return [
        {"path": path, "matched_lines": extract_matching_lines(inputs[key], needles=needles)}
        for path, (key, needles) in lookup.items()
    ]


def build_summary(
    checklist_rows: list[dict[str, object]], worktree_summary: dict[str, Any]
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "active_stage": "h15_refreeze_and_decision_sync",
        "guarded_reopen_stage": "h14_core_first_reopen_and_scope_lock",
        "handoff_stage": "h13_post_h12_rollover_and_next_stage_staging_preserved",
        "stage_guard_state": "preserved_core_first_reopen_guard_green" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_summary),
        "prior_completed_checkpoint": "h10_h11_r8_r9_r10_h12",
        "lane_order": "preserve_h12_and_h13_then_preserve_completed_h14_packet_then_hold_h15_refrozen",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use this summary as the preserved H14 packet entrypoint; keep H10/H11/R8/R9/R10/H12 frozen as the latest completed checkpoint, keep H13/V1 preserved as handoff state, preserve R11 and R12 as landed reopen outputs, and treat H15 as the current refrozen stage until a later explicit plan changes it"
            if not blocked_items
            else "resolve the blocked H14 driver-alignment items before treating the current core-first reopen as canonical"
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
        {"experiment": "h14_core_first_reopen_guard_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h14_core_first_reopen_guard_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h14_core_first_reopen_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/milestones/H14_core_first_reopen_and_scope_lock/README.md",
                "docs/milestones/H14_core_first_reopen_and_scope_lock/status.md",
                "docs/milestones/H14_core_first_reopen_and_scope_lock/artifact_index.md",
                "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/result_digest.md",
                "results/H13_post_h12_governance_stage_health/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
                "results/H10_r7_reconciliation_guard/summary.json",
                "results/H11_post_h9_mainline_rollover_guard/summary.json",
                "results/H8_driver_replacement_guard/summary.json",
                "results/H6_mainline_rollover_guard/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H14 Core-First Reopen Guard\n\n"
        "Machine-readable guard for the preserved H14 core-first reopen packet.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
