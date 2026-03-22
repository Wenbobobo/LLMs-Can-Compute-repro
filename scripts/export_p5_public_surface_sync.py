"""Export the P5 public-surface sync audit for the current paper lane."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P5_public_surface_sync"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_inputs() -> dict[str, str]:
    return {
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "manuscript_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_bundle_draft.md"),
        "layout_log_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
        "p8_result_digest_text": read_text(
            ROOT / "docs" / "milestones" / "P8_submission_candidate_and_bundle_lock" / "result_digest.md"
        ),
        "p9_result_digest_text": read_text(
            ROOT / "docs" / "milestones" / "P9_release_candidate_and_public_surface_freeze" / "result_digest.md"
        ),
    }


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def contains_none(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() not in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 6) -> list[str]:
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


def build_sync_checklist(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    release_summary_text: str,
    manuscript_text: str,
    layout_log_text: str,
    p8_result_digest_text: str,
    p9_result_digest_text: str,
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "readme_keeps_narrow_scope",
            "status": "pass"
            if contains_all(readme_text, ["does **not** claim that general llms are computers", "arbitrary c"])
            else "blocked",
            "notes": "README keeps the narrow-scope guardrails explicit.",
        },
        {
            "item_id": "readme_tracks_current_active_stage",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "| `h13-v1` | completed governance/runtime handoff preserved as a control baseline",
                    "`h10-h12` | completed bounded `d0` retrieval-pressure packet",
                    "| `h20-h21` | completed post-`h19` reentry/refreeze packet",
                    "| `h22-h23` | completed bounded post-`h21` dual-track reopen/refreeze packet preserved as the current frozen scientific state",
                    "| `h24-h25` | completed post-`h23` reauthorization/refreeze packet",
                    "`h25_refreeze_after_r30_r31_decision_packet`. it preserves",
                    "`h23_refreeze_after_r26_r27_r28` as the frozen same-endpoint scientific state",
                    "v1 remains a standing operational reference under the preserved `h13`",
                ],
            )
            else "blocked",
            "notes": "README should keep H25 as the current active decision packet while preserving H23 as the frozen scientific state and the older same-endpoint baselines.",
        },
        {
            "item_id": "status_tracks_current_active_stage",
            "status": "pass"
            if contains_all(
                status_text,
                [
                    "`p8` stage is complete on the current frozen scope",
                    "`p9` stage is complete on the same scope",
                    "`h25_refreeze_after_r30_r31_decision_packet`",
                    "`h22/r26/r28/r27/h23` packet preserved as the current frozen narrow-endpoint scientific state",
                    "`h24/r30/r31/h25` packet preserved as the current decision/refreeze layer above it",
                    "`h21` now remains the preserved pre-reopen same-endpoint control",
                    "`h17_refreeze_and_conditional_frontier_recheck` is now the preserved prior",
                    "`h15_refreeze_and_decision_sync` remains the preserved prior refrozen state",
                    "`h14_core_first_reopen_and_scope_lock` is now the completed prior reopened",
                    "`v1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`e1c` remains conditional only",
                    "`healthy_but_slow`",
                    "`h18 -> r19 -> r20 -> r21 -> h19`",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline",
                    "`h6/r3/r4/(inactive r5)/h7` remains the deeper completed baseline",
                ],
            )
            else "blocked",
            "notes": "STATUS should record H25 as current, preserve H23 as the frozen scientific state, and keep the older same-endpoint baselines explicit.",
        },
        {
            "item_id": "publication_record_readme_tracks_driver_and_packet_docs",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "current_stage_driver.md",
                    "planning_state_taxonomy.md",
                    "submission_packet_index.md",
                    "archival_repro_manifest.md",
                    "release_summary_draft.md",
                    "release_preflight_checklist.md",
                    "release_preflight_checklist_audit",
                    "release_worktree_hygiene_snapshot",
                    "paper_package_plan.md",
                    "current `h27` active decision packet",
                    "preserving `h26` as the current same-endpoint boundary packet",
                    "`r33` as the completed bounded systems-audit lane",
                    "`h25` as the preserved prior post-`h23` decision packet",
                    "`h23` as the preserved earlier frozen same-endpoint scientific state",
                    "`results/h27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`",
                    "`results/h26_refreeze_after_r32_boundary_sharp_zoom/summary.json`",
                    "`results/r33_d0_non_retrieval_overhead_localization_audit/summary.json`",
                    "`results/h25_refreeze_after_r30_r31_decision_packet/summary.json`",
                    "`results/h23_refreeze_after_r26_r27_r28/summary.json`",
                    "`results/r30_d0_boundary_reauthorization_packet/summary.json`",
                    "`results/r31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`",
                    "`h21` as the immediate pre-reopen control",
                    "`h13/v1` preserved as the governance/runtime handoff",
                    "staged the bounded `r32 -> h26 -> r33 -> h27` wave",
                    "submission_candidate_criteria.md",
                    "release_candidate_checklist.md",
                    "conditional_reopen_protocol.md",
                ],
            )
            else "blocked",
            "notes": "Publication record README should name the H27 internal driver, the completed H26/R33/H27 packet, and the preserved control ledgers.",
        },
        {
            "item_id": "release_summary_stays_downstream",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "this repository reproduces a narrow execution-substrate claim",
                    "`h10/h11/r8/r9/r10/h12` is now the latest completed same-endpoint follow-up packet",
                    "`h13/v1` is now the preserved governance/runtime handoff",
                    "the current frozen scientific state inside the post-`p9` chain is `h23_refreeze_after_r26_r27_r28`",
                    "the downstream `p14` public-surface sync implied by `h23` is docs-only and is already complete",
                    "the current active post-`p9` stage is now `h25_refreeze_after_r30_r31_decision_packet`",
                    "`h21` is now the preserved immediate pre-reopen control",
                    "`h17` remains the preserved prior same-scope refreeze decision",
                    "`e1c` remains conditional only",
                ],
            )
            and contains_none(release_summary_text, ["later full plan-mode stage"])
            else "blocked",
            "notes": "The release summary should stay narrow while naming H25 as current, H23 as the frozen scientific state, and frontier work as still conditional.",
        },
        {
            "item_id": "manuscript_tracks_section_draft_state",
            "status": "pass"
            if contains_all(
                manuscript_text,
                [
                    "## 1. Abstract",
                    "## 10. Reproducibility Appendix",
                    "Companion appendix material stays clearly downstream",
                    "The no-widening decision is part",
                ],
            )
            and contains_none(manuscript_text, ["Status: paper-shaped manuscript section draft"])
            else "blocked",
            "notes": "The manuscript now reads as a section-ordered draft instead of carrying a phase-status preamble.",
        },
        {
            "item_id": "current_stage_driver_is_canonical",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h27_refreeze_after_r32_r33_same_endpoint_decision`",
                    "`h26_refreeze_after_r32_boundary_sharp_zoom`",
                    "`r33_d0_non_retrieval_overhead_localization_audit`",
                    "`systems_verdict = systems_more_sharply_negative`",
                    "`next_priority_lane = later_explicit_packet_required_before_new_runtime`",
                    "`h25_refreeze_after_r30_r31_decision_packet` remains the completed prior operational decision packet",
                    "`h23_refreeze_after_r26_r27_r28` remains the preserved earlier same-endpoint scientific control stage",
                    "`r29_d0_same_endpoint_systems_recovery_execution_gate` remains blocked",
                    "`f3_post_h23_scope_lift_decision_bundle` remains blocked",
                    "`f2_future_frontier_recheck_activation_matrix` remains planning-only",
                ],
            )
            else "blocked",
            "notes": "The current-stage driver should expose the H27 internal driver, the completed H26/R33 downstream packet, and the still-blocked future lanes in one place.",
        },
        {
            "item_id": "layout_log_records_post_p7_decisions",
            "status": "pass"
            if contains_all(
                layout_log_text,
                ["Release-summary reuse", "Post-`P7` next phase", "Evidence reopen discipline"],
            )
            else "blocked",
            "notes": "The layout decision log should record release-summary reuse plus the new governance choices.",
        },
        {
            "item_id": "p8_p9_checkpoint_remains_explicit",
            "status": "pass"
            if contains_all(
                p8_result_digest_text,
                [
                    "`P8` closed the submission-candidate bundle-lock pass",
                    "The milestone did not open a new evidence wave",
                    "submission-candidate ready on the current scope",
                ],
            )
            and contains_all(
                p9_result_digest_text,
                ["What `P9` closed", "Next-stage starting point", "restrained release-candidate checkpoint"],
            )
            else "blocked",
            "notes": "The completed P8/P9 digests should remain explicit as the baseline for the next plan-mode stage.",
        },
    ]


def build_surface_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    snapshots = [
        {
            "path": "README.md",
            "needles": [
                "| `H13-V1` | completed governance/runtime handoff preserved as a control baseline",
                "`H10-H12` | completed bounded `D0` retrieval-pressure packet",
                "| `H20-H21` | completed post-`H19` reentry/refreeze packet",
                "| `H22-H23` | completed bounded post-`H21` dual-track reopen/refreeze packet preserved as the current frozen scientific state",
                "| `H24-H25` | completed post-`H23` reauthorization/refreeze packet",
                "`H25_refreeze_after_r30_r31_decision_packet`. It preserves",
                "`H23_refreeze_after_r26_r27_r28` as the frozen same-endpoint scientific state",
            ],
        },
        {
            "path": "STATUS.md",
            "needles": [
                "`P8` stage is complete on the current frozen scope",
                "`P9` stage is complete on the same scope",
                "`H25_refreeze_after_r30_r31_decision_packet`",
                "`H22/R26/R28/R27/H23` packet preserved as the current frozen narrow-endpoint scientific state",
                "`H24/R30/R31/H25` packet preserved as the current decision/refreeze layer above it",
                "`H21` now remains the preserved pre-reopen same-endpoint control",
                "`H17_refreeze_and_conditional_frontier_recheck` is now the preserved prior",
                "`H15_refreeze_and_decision_sync` remains the preserved prior refrozen state",
                "`H14_core_first_reopen_and_scope_lock` is now the completed prior reopened",
                "`V1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint",
                "`healthy_but_slow`",
            ],
        },
        {
            "path": "docs/publication_record/README.md",
            "needles": [
                "current_stage_driver.md",
                "planning_state_taxonomy.md",
                "submission_packet_index.md",
                "archival_repro_manifest.md",
                "release_summary_draft.md",
                "release_preflight_checklist.md",
                "release_preflight_checklist_audit",
                "release_worktree_hygiene_snapshot",
                "paper_package_plan.md",
                "current `H27` active decision packet",
                "preserving `H26` as the current same-endpoint boundary packet",
                "`R33` as the completed bounded systems-audit lane",
                "`H25` as the preserved prior post-`H23` decision packet",
                "`H23` as the preserved earlier frozen same-endpoint scientific state",
                "`results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json`",
                "`results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json`",
                "`results/R33_d0_non_retrieval_overhead_localization_audit/summary.json`",
                "`results/H25_refreeze_after_r30_r31_decision_packet/summary.json`",
                "`results/H23_refreeze_after_r26_r27_r28/summary.json`",
                "`results/R30_d0_boundary_reauthorization_packet/summary.json`",
                "`results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json`",
                "`H21` as the immediate pre-reopen control",
                "`H13/V1` preserved as the governance/runtime handoff",
                "staged the bounded `R32 -> H26 -> R33 -> H27` wave",
            ],
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "needles": [
                "`H27_refreeze_after_r32_r33_same_endpoint_decision`",
                "`H26_refreeze_after_r32_boundary_sharp_zoom`",
                "`R33_d0_non_retrieval_overhead_localization_audit`",
                "`systems_verdict = systems_more_sharply_negative`",
                "`next_priority_lane = later_explicit_packet_required_before_new_runtime`",
                "`H25_refreeze_after_r30_r31_decision_packet` remains the completed prior operational decision packet",
                "`H23_refreeze_after_r26_r27_r28` remains the preserved earlier same-endpoint scientific control stage",
                "`R29_d0_same_endpoint_systems_recovery_execution_gate` remains blocked",
                "`F3_post_h23_scope_lift_decision_bundle` remains blocked",
                "`F2_future_frontier_recheck_activation_matrix` remains planning-only",
            ],
        },
        {
            "path": "docs/publication_record/release_summary_draft.md",
            "needles": [
                "This repository reproduces a narrow execution-substrate claim",
                "`H10/H11/R8/R9/R10/H12` is now the latest completed same-endpoint follow-up packet",
                "`H13/V1` is now the preserved governance/runtime handoff",
                "The current frozen scientific state inside the post-`P9` chain is `H23_refreeze_after_r26_r27_r28`",
                "The downstream `P14` public-surface sync implied by `H23` is docs-only and is already complete",
                "The current active post-`P9` stage is now `H25_refreeze_after_r30_r31_decision_packet`",
                "`H21` is now the preserved immediate pre-reopen control",
                "`H17` remains the preserved prior same-scope refreeze decision",
                "`E1c` remains conditional only",
            ],
        },
        {
            "path": "docs/publication_record/manuscript_bundle_draft.md",
            "needles": [
                "## 1. Abstract",
                "## 10. Reproducibility Appendix",
                "Companion appendix material stays clearly downstream",
                "The no-widening decision is part",
            ],
        },
        {
            "path": "docs/publication_record/layout_decision_log.md",
            "needles": ["Release-summary reuse", "Post-`P7` next phase", "Evidence reopen discipline"],
        },
        {
            "path": "docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md",
            "needles": ["`P8` closed the submission-candidate bundle-lock pass", "submission-candidate ready on the current scope"],
        },
        {
            "path": "docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md",
            "needles": ["What `P9` closed", "Next-stage starting point", "restrained release-candidate checkpoint"],
        },
    ]
    rows: list[dict[str, object]] = []
    for row in snapshots:
        input_key = {
            "README.md": "readme_text",
            "STATUS.md": "status_text",
            "docs/publication_record/README.md": "publication_readme_text",
            "docs/publication_record/current_stage_driver.md": "current_stage_driver_text",
            "docs/publication_record/release_summary_draft.md": "release_summary_text",
            "docs/publication_record/manuscript_bundle_draft.md": "manuscript_text",
            "docs/publication_record/layout_decision_log.md": "layout_log_text",
            "docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md": "p8_result_digest_text",
            "docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md": "p9_result_digest_text",
        }[str(row["path"])]
        rows.append(
            {
                "path": row["path"],
                "matched_lines": extract_matching_lines(inputs[input_key], needles=list(row["needles"])),
            }
        )
    return rows


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h25_refreeze_after_r30_r31_decision_packet_active_h23_frozen",
        "internal_driver_phase": "h27_refreeze_after_r32_r33_same_endpoint_decision_active",
        "release_summary_role": "approved_downstream_short_update_source",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "keep the outward-facing H25/H23 public surface aligned while treating H27 as the current internal driver, H26 as the current same-endpoint boundary packet, R33 as the completed bounded systems-audit lane, R30 and R31 as the landed reauthorization pair for the finished R32/H26/R33/H27 wave, H22/R26/R28/R27 as the completed bounded reopen packet, H21 as the preserved pre-reopen control, H19 as the earlier same-endpoint refreeze, H17 as the preserved prior same-scope refreeze, H15 as the prior refreeze decision, and H13/V1 plus H8/R6/R7/H9 and H10/H11/R8/R9/R10/H12 as preserved baselines"
            if not blocked_items
            else "resolve the blocked public-surface sync items before another outward wording update"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_sync_checklist(**inputs)
    surface_snapshot = build_surface_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p5_public_surface_sync_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "surface_snapshot.json",
        {
            "experiment": "p5_public_surface_sync_snapshot",
            "environment": environment.as_dict(),
            "rows": surface_snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p5_public_surface_sync",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/manuscript_bundle_draft.md",
                "docs/publication_record/layout_decision_log.md",
                "docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md",
                "docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P5 Public Surface Sync",
                "",
                "Machine-readable audit of whether the current public surface stays aligned with the",
                "locked checkpoint, the current outward H25/H23 surface, the internal H27 canonical",
                "driver, and the",
                "approved downstream release summary.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `surface_snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
