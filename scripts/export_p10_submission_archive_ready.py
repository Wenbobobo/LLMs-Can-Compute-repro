"""Export the P10 submission/archive packet readiness audit."""

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


def load_inputs() -> dict[str, Any]:
    return {
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "planning_state_taxonomy_text": read_text(ROOT / "docs" / "publication_record" / "planning_state_taxonomy.md"),
        "submission_packet_index_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_packet_index.md"
        ),
        "archival_repro_manifest_text": read_text(
            ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"
        ),
        "review_boundary_summary_text": read_text(
            ROOT / "docs" / "publication_record" / "review_boundary_summary.md"
        ),
        "external_release_note_skeleton_text": read_text(
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
        "release_preflight_summary": read_json(
            ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
        ),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "p5_callout_summary": read_json(ROOT / "results" / "P5_callout_alignment" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
    }


def ready_count_from_p1_summary(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["blocked_count"])


def runtime_classification_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["runtime_classification"])


def timed_out_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["timed_out_file_count"])


def preflight_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["preflight_state"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def diff_check_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["git_diff_check_state"])


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    planning_state_taxonomy_text: str,
    submission_packet_index_text: str,
    archival_repro_manifest_text: str,
    review_boundary_summary_text: str,
    external_release_note_skeleton_text: str,
    p1_summary: dict[str, Any],
    v1_timing_summary: dict[str, Any],
    release_preflight_summary: dict[str, Any],
    worktree_hygiene_summary_text: str,
    worktree_hygiene_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    p5_callout_summary: dict[str, Any],
    h2_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "active_driver_names_current_packet",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`h13_post_h12_rollover_and_next_stage_staging` remains preserved",
                    "`v1_full_suite_validation_runtime_audit` remains a standing operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint follow-up packet",
                    "`e1c_compiled_boundary_patch`",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline underneath",
                    "`h6/r3/r4/(inactive r5)/h7` remains the deeper historical baseline",
                ],
            )
            else "blocked",
            "notes": "The current-stage driver should expose current H15, preserved H14/H13/V1 state, the preserved H12 checkpoint, and the conditional compiled lane.",
        },
        {
            "item_id": "planning_taxonomy_assigns_single_active_driver",
            "status": "pass"
            if contains_all(
                planning_state_taxonomy_text,
                [
                    "`active_driver`",
                    "`standing_gate`",
                    "`historical_complete`",
                    "`dormant_protocol`",
                    "`docs/publication_record/current_stage_driver.md`",
                    "`docs/publication_record/release_candidate_checklist.md`",
                    "`docs/publication_record/paper_package_plan.md`",
                    "`docs/publication_record/conditional_reopen_protocol.md`",
                ],
            )
            else "blocked",
            "notes": "The planning taxonomy should make active-driver and gate ownership explicit.",
        },
        {
            "item_id": "submission_packet_names_canonical_bundle",
            "status": "pass"
            if contains_all(
                submission_packet_index_text,
                [
                    "`manuscript_bundle_draft.md`",
                    "`main_text_order.md`",
                    "`appendix_companion_scope.md`",
                    "`claim_ladder.md`",
                    "`claim_evidence_table.md`",
                    "`current_stage_driver.md`",
                    "`results/p1_paper_readiness/summary.json`",
                    "`results/h15_refreeze_and_decision_sync/summary.json`",
                    "`results/v1_full_suite_validation_runtime_timing_followup/summary.json`",
                    "`results/release_worktree_hygiene_snapshot/summary.json`",
                    "`results/release_preflight_checklist_audit/summary.json`",
                    "`results/p10_submission_archive_ready/summary.json`",
                ],
            )
            else "blocked",
            "notes": "The packet index should identify the canonical manuscript, appendix, control docs, and audit anchors.",
        },
        {
            "item_id": "archival_manifest_names_regeneration_and_restrictions",
            "status": "pass"
            if contains_all(
                archival_repro_manifest_text,
                [
                    "python `3.12`",
                    "`uv`",
                    "uv run python scripts/export_p1_paper_readiness.py",
                    "uv run python scripts/export_h15_refreeze_and_decision_sync.py",
                    "uv run python scripts/export_v1_full_suite_validation_runtime_audit.py",
                    "uv run python scripts/export_v1_full_suite_validation_runtime_timing_followup.py",
                    "uv run python scripts/export_p5_public_surface_sync.py",
                    "uv run python scripts/export_h2_bundle_lock_audit.py",
                    "uv run python scripts/export_release_worktree_hygiene_snapshot.py",
                    "uv run python scripts/export_release_preflight_checklist_audit.py",
                    "uv run python scripts/export_p10_submission_archive_ready.py",
                    "results/release_worktree_hygiene_snapshot/summary.json",
                    "`docs/Origin/`",
                    "`docs/origin/`",
                ],
            )
            else "blocked",
            "notes": "The archival manifest should document regeneration commands and explicit restricted-source exclusions.",
        },
        {
            "item_id": "release_worktree_snapshot_is_recorded_without_forcing_clean_tree",
            "status": "pass"
            if release_commit_state_from_summary(worktree_hygiene_summary)
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and diff_check_state_from_summary(worktree_hygiene_summary) != "content_issues_present"
            and contains_all(
                worktree_hygiene_summary_text,
                [
                    "\"release_commit_state\":",
                    "\"git_diff_check_state\":",
                ],
            )
            else "blocked",
            "notes": "The packet should carry the machine-readable worktree snapshot as an operational commit gate without treating a dirty unattended tree as a science failure.",
        },
        {
            "item_id": "review_boundary_summary_preserves_scope",
            "status": "pass"
            if contains_all(
                review_boundary_summary_text,
                [
                    "append-only execution trace",
                    "structured 2d hard-max mechanism",
                    "tiny typed-bytecode `d0`",
                    "no general “llms are computers” claim",
                    "`e1a_precision_patch`",
                    "`e1b_systems_patch`",
                    "`e1c_compiled_boundary_patch`",
                ],
            )
            else "blocked",
            "notes": "The review-boundary summary should preserve supported claims, blocked claims, and explicit reopen routing.",
        },
        {
            "item_id": "external_release_note_stays_downstream",
            "status": "pass"
            if contains_all(
                external_release_note_skeleton_text,
                [
                    "downstream-only skeleton",
                    "narrow execution-substrate claim",
                    "tiny typed-bytecode `d0`",
                    "results/p10_submission_archive_ready/summary.json",
                    "blog remains blocked",
                ],
            )
            else "blocked",
            "notes": "The release-note skeleton should remain restrained and explicitly downstream-only.",
        },
        {
            "item_id": "top_level_docs_align_with_current_driver",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "`h10-h12` | completed bounded `d0` retrieval-pressure packet",
                    "| `h13-v1` | completed governance/runtime handoff preserved as a control baseline",
                    "| `h14-h15` | completed bounded core-first reopen/refreeze packet",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "`e1c` stays conditional only",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`v1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`e1c` remains conditional only",
                    "`healthy_but_slow`",
                    "the completed reopen wave ran through",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline",
                ],
            )
            and contains_all(
                publication_readme_text,
                [
                    "`current_stage_driver.md`",
                    "`planning_state_taxonomy.md`",
                    "`submission_packet_index.md`",
                    "`archival_repro_manifest.md`",
                    "`h15` refreeze-and-decision-sync",
                    "`h14` / `r11` / `r12` remain the completed reopen packet",
                    "`h13` / `v1` remain the completed governance/runtime handoff",
                ],
            )
            else "blocked",
            "notes": "README, STATUS, and the publication index should all reflect the same current H15 driver and preserved packet docs.",
        },
        {
            "item_id": "packet_docs_keep_restricted_sources_out_of_public_bundle",
            "status": "pass"
            if contains_none(
                submission_packet_index_text + "\n" + review_boundary_summary_text + "\n" + external_release_note_skeleton_text,
                ["docs/origin/", "docs/Origin/"],
            )
            else "blocked",
            "notes": "Public packet docs other than the archive manifest should not depend on restricted-source paths.",
        },
        {
            "item_id": "standing_audits_remain_green",
            "status": "pass"
            if ready_count_from_p1_summary(p1_summary) == 10
            and not p1_summary["blocked_or_partial_items"]
            and runtime_classification_from_summary(v1_timing_summary) == "healthy_but_slow"
            and timed_out_count_from_summary(v1_timing_summary) == 0
            and preflight_state_from_summary(release_preflight_summary) == "docs_and_audits_green"
            and blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(p5_callout_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            else "blocked",
            "notes": "The existing standing audits must stay green before the packet is called archive-ready.",
        },
    ]


def build_packet_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "`H10-H12` | completed bounded `D0` retrieval-pressure packet",
                "| `H13-V1` | completed governance/runtime handoff preserved as a control baseline",
                "| `H14-H15` | completed bounded core-first reopen/refreeze packet",
                "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`V1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint",
                "`healthy_but_slow`",
                "`E1c` remains conditional only",
            ],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`H13_post_h12_rollover_and_next_stage_staging` remains preserved",
                "`V1_full_suite_validation_runtime_audit` remains a standing operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint follow-up packet",
                "`H8/R6/R7/H9` remains the completed direct same-endpoint baseline underneath",
            ],
        ),
        "docs/publication_record/submission_packet_index.md": (
            "submission_packet_index_text",
            [
                "`manuscript_bundle_draft.md`",
                "`appendix_companion_scope.md`",
                "`current_stage_driver.md`",
                "`results/H15_refreeze_and_decision_sync/summary.json`",
                "`results/V1_full_suite_validation_runtime_timing_followup/summary.json`",
                "`results/release_worktree_hygiene_snapshot/summary.json`",
                "`results/release_preflight_checklist_audit/summary.json`",
                "`results/P10_submission_archive_ready/summary.json`",
            ],
        ),
        "docs/publication_record/archival_repro_manifest.md": (
            "archival_repro_manifest_text",
            [
                "Python `3.12`",
                "`uv`",
                "uv run python scripts/export_v1_full_suite_validation_runtime_timing_followup.py",
                "uv run python scripts/export_release_worktree_hygiene_snapshot.py",
                "uv run python scripts/export_release_preflight_checklist_audit.py",
                "uv run python scripts/export_p10_submission_archive_ready.py",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "`docs/Origin/`",
            ],
        ),
        "results/release_worktree_hygiene_snapshot/summary.json": (
            "worktree_hygiene_summary_text",
            [
                "\"release_commit_state\":",
                "\"git_diff_check_state\":",
            ],
        ),
        "docs/publication_record/review_boundary_summary.md": (
            "review_boundary_summary_text",
            [
                "append-only execution trace",
                "tiny typed-bytecode `D0`",
                "no arbitrary C reproduction claim",
                "`E1a_precision_patch`",
            ],
        ),
        "docs/publication_record/external_release_note_skeleton.md": (
            "external_release_note_skeleton_text",
            [
                "downstream-only skeleton",
                "narrow execution-substrate claim",
                "tiny typed-bytecode `D0`",
                "blog remains blocked",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append(
            {
                "path": path,
                "matched_lines": extract_matching_lines(inputs[input_key], needles=needles),
            }
        )
    return rows


def build_summary(
    checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "packet_state": "archive_ready" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_hygiene_summary),
        "git_diff_check_state": diff_check_state_from_summary(worktree_hygiene_summary),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use submission_packet_index.md plus archival_repro_manifest.md as the canonical handoff while H15 stays aligned as the current refrozen stage, consult release_worktree_hygiene_snapshot before any release-facing commit, preserve H14/R11/R12 as the completed reopen packet, preserve H13/V1 as handoff state, keep H10/H11/R8/R9/R10/H12 as the latest completed checkpoint, and keep H8/R6/R7/H9 plus H6/R3/R4/(inactive R5)/H7 as preserved baselines"
            if not blocked_items
            else "resolve the blocked packet-readiness items before treating the bundle as archive-ready"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    rows = build_checklist_rows(**inputs)
    snapshot = build_packet_snapshot(inputs)
    summary = build_summary(rows, inputs["worktree_hygiene_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p10_submission_archive_ready_checklist",
            "environment": environment.as_dict(),
            "rows": rows,
        },
    )
    write_json(
        OUT_DIR / "packet_snapshot.json",
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
                "docs/publication_record/planning_state_taxonomy.md",
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
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P10 Submission Archive Ready",
                "",
                "Machine-readable audit of whether the current locked checkpoint can be",
                "handed off as a venue-agnostic submission/archive packet without widening",
                "scientific scope.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `packet_snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
