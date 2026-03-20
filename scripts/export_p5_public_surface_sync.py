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
                    "| `h14-h15` | completed bounded core-first reopen/refreeze packet",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "v1 remains a standing operational reference under the preserved `h13`",
                ],
            )
            else "blocked",
            "notes": "README should keep H12 as the completed checkpoint while naming current H15 and preserved H14/H13 state.",
        },
        {
            "item_id": "status_tracks_current_active_stage",
            "status": "pass"
            if contains_all(
                status_text,
                [
                    "`p8` stage is complete on the current frozen scope",
                    "`p9` stage is complete on the same scope",
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`h13_post_h12_rollover_and_next_stage_staging` is no longer the active stage",
                    "`v1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`e1c` remains conditional only",
                    "`healthy_but_slow`",
                    "the completed reopen wave ran through",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline",
                    "`h6/r3/r4/(inactive r5)/h7` remains the deeper completed baseline",
                ],
            )
            else "blocked",
            "notes": "STATUS should record the completed checkpoint plus current H15 and preserved H14/H13/V1 state.",
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
                    "`h15` refreeze-and-decision-sync",
                    "`h14` / `r11` / `r12` remain the completed reopen packet",
                    "`h13` / `v1` remain the completed governance/runtime handoff",
                    "submission_candidate_criteria.md",
                    "release_candidate_checklist.md",
                    "conditional_reopen_protocol.md",
                ],
            )
            else "blocked",
            "notes": "Publication record README should name the active driver, packet docs, and taxonomy-labeled controls.",
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
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "`e1c` remains conditional only",
                ],
            )
            and contains_none(release_summary_text, ["later full plan-mode stage"])
            else "blocked",
            "notes": "The release summary should stay narrow while naming the completed H12 checkpoint, preserved H13/V1 handoff, and current H15 stage explicitly.",
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
            "notes": "The current-stage driver should expose current H15 plus preserved H14/H13/V1 state and the completed H12 checkpoint in one place.",
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
                "| `H14-H15` | completed bounded core-first reopen/refreeze packet",
                "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`",
                "V1 remains a standing operational reference under the preserved `H13`",
            ],
        },
        {
            "path": "STATUS.md",
            "needles": [
                "`P8` stage is complete on the current frozen scope",
                "`P9` stage is complete on the same scope",
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`H13_post_h12_rollover_and_next_stage_staging` is no longer the active stage",
                "`V1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint",
                "`healthy_but_slow`",
                "The completed reopen wave ran through",
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
                "`H15` refreeze-and-decision-sync",
                "`H14` / `R11` / `R12` remain the completed reopen packet",
                "`H13` / `V1` remain the completed governance/runtime handoff",
            ],
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "needles": [
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`H13_post_h12_rollover_and_next_stage_staging` remains preserved",
                "`V1_full_suite_validation_runtime_audit` remains a standing operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint follow-up packet",
                "`H8/R6/R7/H9` remains the completed direct same-endpoint baseline underneath",
            ],
        },
        {
            "path": "docs/publication_record/release_summary_draft.md",
            "needles": [
                "This repository reproduces a narrow execution-substrate claim",
                "`H10/H11/R8/R9/R10/H12` is now the latest completed same-endpoint follow-up packet",
                "`H13/V1` is now the preserved governance/runtime handoff",
                "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`",
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
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "release_summary_role": "approved_downstream_short_update_source",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "keep the current H15 refrozen stage aligned across public-surface docs while preserving H14/R11/R12 as the completed reopen packet, H10/H11/R8/R9/R10/H12 as the latest completed checkpoint, H13/V1 as preserved handoff state, and H8/R6/R7/H9 plus H6/R3/R4/(inactive R5)/H7 as preserved baselines"
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
                "locked checkpoint, the active consolidation packet, and the approved downstream",
                "release summary.",
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
