"""Export the P10 submission/archive readiness audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P10_submission_archive_ready"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def contains_none(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() not in lowered for needle in needles)


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


def preflight_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["preflight_state"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def diff_check_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["git_diff_check_state"])


def ready_count_from_p1_summary(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    summary = summary_doc["summary"]
    if "blocked_count" in summary:
        return int(summary["blocked_count"])
    return int(summary["blocked_rows"])


def runtime_classification_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["runtime_classification"])


def timed_out_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["timed_out_file_count"])


def load_inputs() -> dict[str, Any]:
    return {
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "submission_packet_index_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_packet_index.md"
        ),
        "archival_manifest_text": read_text(ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"),
        "review_boundary_text": read_text(ROOT / "docs" / "publication_record" / "review_boundary_summary.md"),
        "external_release_note_text": read_text(
            ROOT / "docs" / "publication_record" / "external_release_note_skeleton.md"
        ),
        "p1_summary": read_json(ROOT / "results" / "P1_paper_readiness" / "summary.json"),
        "v1_timing_summary": read_json(
            ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup" / "summary.json"
        ),
        "worktree_hygiene_summary_text": read_text(
            ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
        ),
        "worktree_hygiene_summary": read_json(
            ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
        ),
        "preflight_summary": read_json(ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "p5_callout_summary": read_json(ROOT / "results" / "P5_callout_alignment" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
    }


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    submission_packet_index_text: str,
    archival_manifest_text: str,
    review_boundary_text: str,
    external_release_note_text: str,
    p1_summary: dict[str, Any],
    v1_timing_summary: dict[str, Any],
    worktree_hygiene_summary_text: str,
    worktree_hygiene_summary: dict[str, Any],
    preflight_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    p5_callout_summary: dict[str, Any],
    h2_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "top_level_surfaces_and_driver_are_current_h52_control",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "`merge_executed = false`",
                ],
            )
            and contains_all(
                publication_readme_text,
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "current active packet",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                current_stage_driver_text,
                [
                    "the current active stage is:",
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            else "blocked",
            "notes": "Top-level surfaces and the canonical driver should all expose the current H52/H50/H51 control stack while preserving H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "submission_packet_index_and_archival_manifest_track_current_h52_h43_bundle",
            "status": "pass"
            if contains_all(
                submission_packet_index_text,
                [
                    "current repo control state is `h52` as the active docs-only",
                    "`h50` preserved as the broader-route value closeout",
                    "`h51` preserved as the prior mechanism-reentry packet",
                    "`h43` preserved as the paper-grade useful-case refreeze packet",
                    "`r55` and `r56` remain exact mechanism evidence only",
                    "`r57` remains negative fast-path comparator",
                    "`p26/p27/p37` preserve the current audit-plus-explicit-merge operational",
                ],
            )
            and contains_all(
                archival_manifest_text,
                [
                    "results/h52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                    "current active docs-only control packet is `h52`",
                    "`r55/r56` remain exact mechanism support only",
                    "`r57` remains negative fast-path comparator evidence",
                    "`p27/p37` preserve the current operational release-control posture",
                ],
            )
            else "blocked",
            "notes": "Submission packet index and archival manifest should point at the same H52 current-control plus preserved H43 paper-grade bundle.",
        },
        {
            "item_id": "review_boundary_and_external_release_note_stay_downstream_of_h52_control",
            "status": "pass"
            if contains_all(
                review_boundary_text,
                [
                    "routing/decision state is `h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                    "`r56_origin_append_only_trace_vm_semantics_gate`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                    "`supported_here_narrowly`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                external_release_note_text,
                [
                    "narrow execution-substrate claim",
                    "general “llms are computers”",
                    "arbitrary c reproduction",
                    "docs/publication_record/submission_packet_index.md",
                    "docs/publication_record/claim_ladder.md",
                ],
            )
            and contains_none(
                external_release_note_text,
                ["docs/origin/", "docs/Origin/"],
            )
            else "blocked",
            "notes": "Review and release-note helpers should stay downstream of the current H52 control state and preserved H43 paper bundle.",
        },
        {
            "item_id": "standing_release_audits_remain_green",
            "status": "pass"
            if ready_count_from_p1_summary(p1_summary) == 10
            and preflight_state_from_summary(preflight_summary) == "docs_and_audits_green"
            and blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(p5_callout_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            and runtime_classification_from_summary(v1_timing_summary) == "healthy_but_slow"
            and timed_out_count_from_summary(v1_timing_summary) == 0
            else "blocked",
            "notes": "Archive readiness depends on the standing P1, release-preflight, P5, H2, and V1 audits remaining green.",
        },
        {
            "item_id": "worktree_hygiene_snapshot_classifies_commit_state",
            "status": "pass"
            if release_commit_state_from_summary(worktree_hygiene_summary)
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and diff_check_state_from_summary(worktree_hygiene_summary) != "content_issues_present"
            and contains_all(
                worktree_hygiene_summary_text,
                ['"release_commit_state":', '"git_diff_check_state":'],
            )
            else "blocked",
            "notes": "Archive readiness should inherit the current release-worktree hygiene classification.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H50_post_r51_r52_scope_decision_packet`",
                "`R57_origin_accelerated_trace_vm_comparator_gate`",
                "`H43_post_r44_useful_case_refreeze`",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H50_post_r51_r52_scope_decision_packet`",
                "`H51_post_h50_origin_mechanism_reentry_packet`",
                "`merge_executed = false`",
            ],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H43_post_r44_useful_case_refreeze`",
                "`R57_origin_accelerated_trace_vm_comparator_gate`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H50_post_r51_r52_scope_decision_packet`",
                "`H51_post_h50_origin_mechanism_reentry_packet`",
                "`P37_post_h50_narrow_executor_closeout_sync`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/publication_record/submission_packet_index.md": (
            "submission_packet_index_text",
            [
                "The current repo control state is `H52` as the active docs-only",
                "`H43` preserved as the paper-grade useful-case refreeze packet",
                "`P26/P27/P37` preserve the current audit-plus-explicit-merge operational",
            ],
        ),
        "docs/publication_record/archival_repro_manifest.md": (
            "archival_manifest_text",
            [
                "results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json",
                "results/H43_post_r44_useful_case_refreeze/summary.json",
                "The current active docs-only control packet is `H52`",
            ],
        ),
        "docs/publication_record/review_boundary_summary.md": (
            "review_boundary_text",
            [
                "routing/decision state is `H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`R57_origin_accelerated_trace_vm_comparator_gate`",
                "`supported_here_narrowly`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/publication_record/external_release_note_skeleton.md": (
            "external_release_note_text",
            [
                "narrow execution-substrate claim",
                "general “llms are computers”",
                "arbitrary C reproduction",
                "docs/publication_record/submission_packet_index.md",
            ],
        ),
        "results/release_worktree_hygiene_snapshot/summary.json": (
            "worktree_hygiene_summary_text",
            ['"release_commit_state":', '"git_diff_check_state":'],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h52_current_control_with_h43_paper_endpoint",
        "packet_state": "archive_ready" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_hygiene_summary),
        "git_diff_check_state": diff_check_state_from_summary(worktree_hygiene_summary),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use submission_packet_index.md plus archival_repro_manifest.md as the canonical handoff while H52 remains the current docs-only mechanism closeout packet, preserve H50 as the broader-route value closeout, preserve H51 as the prior mechanism-reentry packet, preserve H43 as the paper-grade endpoint, keep R55/R56 as exact mechanism evidence, keep R57 as negative fast-path comparator evidence, preserve H36 as the routing/refreeze packet, keep R42/R43/R44/R45 as the completed semantic-boundary gate stack, preserve P28 as publication alignment to H43, preserve P27/P37 as operational release-control context, and keep no_active_downstream_runtime_lane as the current follow-on state"
            if not blocked_items
            else "resolve the blocked archive-ready items before using the submission/archive handoff"
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
        {
            "experiment": "p10_submission_archive_ready_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p10_submission_archive_ready_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p10_submission_archive_ready",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/submission_packet_index.md",
                "docs/publication_record/archival_repro_manifest.md",
                "docs/publication_record/review_boundary_summary.md",
                "docs/publication_record/external_release_note_skeleton.md",
                "results/P1_paper_readiness/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/release_preflight_checklist_audit/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/P5_callout_alignment/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/H52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json",
                "results/H50_post_r51_r52_scope_decision_packet/summary.json",
                "results/H51_post_h50_origin_mechanism_reentry_packet/summary.json",
                "results/P37_post_h50_narrow_executor_closeout_sync/summary.json",
                "results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json",
                "results/R56_origin_append_only_trace_vm_semantics_gate/summary.json",
                "results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json",
                "results/H43_post_r44_useful_case_refreeze/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P10 Submission Archive Ready",
                "",
                "Machine-readable audit of whether the current submission/archive handoff",
                "surfaces stay aligned with the current H52 control stack while preserving",
                "H43 as the paper-grade endpoint.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
