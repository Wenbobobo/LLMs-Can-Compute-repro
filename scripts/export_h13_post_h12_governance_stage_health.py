"""Export a machine-readable preserved-handoff summary for completed H13/V1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H13_post_h12_governance_stage_health"


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


def load_inputs() -> dict[str, Any]:
    paths = {
        "current_stage_driver_text": ROOT / "docs" / "publication_record" / "current_stage_driver.md",
        "h13_readme_text": ROOT / "docs" / "milestones" / "H13_post_h12_rollover_and_next_stage_staging" / "README.md",
        "h13_status_text": ROOT / "docs" / "milestones" / "H13_post_h12_rollover_and_next_stage_staging" / "status.md",
        "h13_artifact_index_text": ROOT / "docs" / "milestones" / "H13_post_h12_rollover_and_next_stage_staging" / "artifact_index.md",
        "h13_result_digest_text": ROOT / "docs" / "milestones" / "H13_post_h12_rollover_and_next_stage_staging" / "result_digest.md",
        "v1_audit_summary_text": ROOT / "results" / "V1_full_suite_validation_runtime_audit" / "summary.json",
        "v1_timing_summary_text": ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup" / "summary.json",
        "h10_summary_text": ROOT / "results" / "H10_r7_reconciliation_guard" / "summary.json",
        "h11_summary_text": ROOT / "results" / "H11_post_h9_mainline_rollover_guard" / "summary.json",
        "h8_summary_text": ROOT / "results" / "H8_driver_replacement_guard" / "summary.json",
        "h6_summary_text": ROOT / "results" / "H6_mainline_rollover_guard" / "summary.json",
        "p5_summary_text": ROOT / "results" / "P5_public_surface_sync" / "summary.json",
        "h2_summary_text": ROOT / "results" / "H2_bundle_lock_audit" / "summary.json",
        "worktree_hygiene_summary_text": ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json",
        "release_preflight_summary_text": ROOT / "results" / "release_preflight_checklist_audit" / "summary.json",
        "p10_summary_text": ROOT / "results" / "P10_submission_archive_ready" / "summary.json",
        "m7_decision_text": ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json",
    }
    inputs: dict[str, Any] = {key: read_text(path) for key, path in paths.items()}
    for key, path in paths.items():
        if key.endswith("_text") and path.suffix == ".json":
            inputs[key.removesuffix("_text")] = read_json(path)
    return inputs


def build_checklist_rows(
    *,
    current_stage_driver_text: str,
    h13_readme_text: str,
    h13_status_text: str,
    h13_artifact_index_text: str,
    h13_result_digest_text: str,
    v1_audit_summary_text: str,
    v1_audit_summary: dict[str, Any],
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
    p5_summary_text: str,
    p5_summary: dict[str, Any],
    h2_summary_text: str,
    h2_summary: dict[str, Any],
    worktree_hygiene_summary_text: str,
    worktree_hygiene_summary: dict[str, Any],
    release_preflight_summary_text: str,
    release_preflight_summary: dict[str, Any],
    p10_summary_text: str,
    p10_summary: dict[str, Any],
    m7_decision_text: str,
    m7_decision: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "current_stage_driver_preserves_h13_handoff",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`h13_post_h12_rollover_and_next_stage_staging`",
                    "`v1_full_suite_validation_runtime_audit`",
                    "standing operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint follow-up packet",
                ],
            )
            else "blocked",
            "notes": "The canonical driver should keep H13/V1 explicit as preserved handoff while H15 remains the current refrozen stage.",
        },
        {
            "item_id": "h13_milestone_docs_track_preserved_handoff",
            "status": "pass"
            if contains_all(
                h13_readme_text,
                ["preserved governance/runtime handoff", "`h14`", "control synchronization"],
            )
            and contains_all(
                h13_status_text,
                [
                    "`v1_full_suite_validation_runtime_audit`",
                    "`healthy_but_slow`",
                    "`h14`",
                    "`r11`",
                    "`r12`",
                ],
            )
            and contains_all(
                h13_artifact_index_text,
                [
                    "result_digest.md",
                    "2026-03-20-h14-core-first-reopen-design.md",
                    "results/h13_post_h12_governance_stage_health/summary.json",
                    "results/h14_core_first_reopen_guard/summary.json",
                ],
            )
            and contains_all(
                h13_result_digest_text,
                ["governance-only post-`h12` handoff", "did not authorize `r11`, `r12`, `r13`, or `r14`"],
            )
            else "blocked",
            "notes": "The H13 milestone docs should read as a completed handoff, not as the active stage.",
        },
        {
            "item_id": "preserved_baseline_and_packet_guards_are_green",
            "status": "pass"
            if blocked_count_from_summary(h10_summary) == 0
            and blocked_count_from_summary(h11_summary) == 0
            and blocked_count_from_summary(h8_summary) == 0
            and blocked_count_from_summary(h6_summary) == 0
            and contains_all(h11_summary_text, ["\"blocked_count\": 0", "\"current_paper_phase\": \"h15_refreeze_and_decision_sync_complete\""])
            else "blocked",
            "notes": "The preserved packet wording and direct/deeper baseline guards should stay green under H15.",
        },
        {
            "item_id": "publication_and_archive_controls_are_green",
            "status": "pass"
            if blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            and release_preflight_summary["summary"]["preflight_state"] == "docs_and_audits_green"
            and blocked_count_from_summary(release_preflight_summary) == 0
            and p10_summary["summary"]["packet_state"] == "archive_ready"
            and blocked_count_from_summary(p10_summary) == 0
            and contains_all(p10_summary_text, ["\"packet_state\": \"archive_ready\"", "\"blocked_count\": 0"])
            and contains_all(p5_summary_text, ["\"current_paper_phase\": \"h15_refreeze_and_decision_sync_complete\""])
            else "blocked",
            "notes": "Public-surface sync, bundle lock, release preflight, and archive handoff should stay green together.",
        },
        {
            "item_id": "release_worktree_hygiene_snapshot_is_classified",
            "status": "pass"
            if str(worktree_hygiene_summary["summary"]["release_commit_state"])
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and str(worktree_hygiene_summary["summary"]["git_diff_check_state"]) != "content_issues_present"
            and contains_all(
                worktree_hygiene_summary_text,
                [
                    "\"release_commit_state\":",
                    "\"git_diff_check_state\":",
                ],
            )
            else "blocked",
            "notes": "The preserved handoff should still carry one machine-readable worktree snapshot for release-facing commit decisions.",
        },
        {
            "item_id": "v1_runtime_issue_remains_bounded_operationally",
            "status": "pass"
            if v1_audit_summary["summary"]["validation_gate_status"] == "needs_runtime_classification"
            and bool(v1_audit_summary["summary"]["collect_only_completed"])
            and int(v1_audit_summary["summary"]["collect_only_returncode"]) == 0
            and v1_timing_summary["summary"]["runtime_classification"] == "healthy_but_slow"
            and int(v1_timing_summary["summary"]["timed_out_file_count"]) == 0
            and contains_all(
                v1_audit_summary_text,
                ["\"validation_gate_status\": \"needs_runtime_classification\"", "\"collect_only_completed\": true"],
            )
            and contains_all(
                v1_timing_summary_text,
                ["\"runtime_classification\": \"healthy_but_slow\"", "\"timed_out_file_count\": 0"],
            )
            else "blocked",
            "notes": "V1 should remain a bounded operational reference rather than silently becoming 'passed'.",
        },
        {
            "item_id": "m7_no_widening_remains_in_force",
            "status": "pass"
            if m7_decision["summary"]["frontend_widening_authorized"] is False
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
            "notes": "The preserved handoff should not weaken the existing no-widening decision.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["`H15_refreeze_and_decision_sync`", "standing operational reference"],
        ),
        "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/status.md": (
            "h13_status_text",
            ["`H14`", "`R11`", "`healthy_but_slow`"],
        ),
        "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/result_digest.md": (
            "h13_result_digest_text",
            ["governance-only post-`H12` handoff", "did not authorize `R11`, `R12`, `R13`, or `R14`"],
        ),
        "results/V1_full_suite_validation_runtime_timing_followup/summary.json": (
            "v1_timing_summary_text",
            ["\"runtime_classification\": \"healthy_but_slow\"", "\"timed_out_file_count\": 0"],
        ),
        "results/release_preflight_checklist_audit/summary.json": (
            "release_preflight_summary_text",
            ["\"preflight_state\": \"docs_and_audits_green\"", "\"blocked_count\": 0"],
        ),
        "results/P10_submission_archive_ready/summary.json": (
            "p10_summary_text",
            ["\"packet_state\": \"archive_ready\"", "\"blocked_count\": 0"],
        ),
    }
    return [
        {"path": path, "matched_lines": extract_matching_lines(inputs[key], needles=needles)}
        for path, (key, needles) in lookup.items()
    ]


def build_summary(checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "active_stage": "h15_refreeze_and_decision_sync",
        "preserved_stage": "h13_post_h12_rollover_and_next_stage_staging",
        "entrypoint_role": "preserved_governance_handoff_reference",
        "stage_health_state": "preserved_handoff_green" if not blocked_items else "blocked",
        "release_commit_state": str(worktree_hygiene_summary["summary"]["release_commit_state"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use this summary as the preserved H13/V1 handoff reference while H15 keeps the repo refrozen; keep H14/R11/R12 preserved as the completed reopen packet, keep H10/H11/R8/R9/R10/H12 frozen, consult release_worktree_hygiene_snapshot before any release-facing commit, and do not treat H13/V1 as an active science lane"
            if not blocked_items
            else "resolve the blocked H13 handoff items before treating the preserved governance/runtime handoff as healthy"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs["worktree_hygiene_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h13_post_h12_governance_stage_health_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h13_post_h12_governance_stage_health_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h13_post_h12_governance_stage_health",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/publication_record/current_stage_driver.md",
                "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/README.md",
                "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/status.md",
                "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/artifact_index.md",
                "docs/milestones/H13_post_h12_rollover_and_next_stage_staging/result_digest.md",
                "results/V1_full_suite_validation_runtime_audit/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
                "results/H10_r7_reconciliation_guard/summary.json",
                "results/H11_post_h9_mainline_rollover_guard/summary.json",
                "results/H8_driver_replacement_guard/summary.json",
                "results/H6_mainline_rollover_guard/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/release_preflight_checklist_audit/summary.json",
                "results/P10_submission_archive_ready/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H13 Post-H12 Governance Stage Health\n\n"
        "Machine-readable preserved-handoff summary for the completed H13/V1\n"
        "governance/runtime stage.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
