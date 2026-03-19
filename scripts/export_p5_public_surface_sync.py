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
                    "active post-`p9` stage is checkpoint consolidation and archive packaging",
                    "`h3` fixes driver/gate semantics",
                    "`p10` builds a venue-agnostic submission/archive packet",
                    "`p11` prepares downstream-only derivative material",
                    "no `e1` patch lane is active",
                ],
            )
            else "blocked",
            "notes": "README should name the active post-P9 consolidation packet rather than a generic later stage.",
        },
        {
            "item_id": "status_tracks_current_active_stage",
            "status": "pass"
            if contains_all(
                status_text,
                [
                    "`p8` stage is complete on the current frozen scope",
                    "`p9` stage is complete on the same scope",
                    "current active post-`p9` operational stage is checkpoint consolidation and archive readiness",
                    "`h3`, `p10`, `p11`, and `f1`",
                    "no `e1` patch lane is active",
                ],
            )
            else "blocked",
            "notes": "STATUS should record the completed checkpoint plus the active consolidation packet.",
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
                    "paper_package_plan.md",
                    "historical_complete",
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
                    "the active post-`p9` follow-up is checkpoint consolidation rather than claim expansion",
                    "`h3` clarifies driver/gate semantics",
                    "`p10` builds a venue-agnostic submission/archive packet",
                    "`p11` prepares downstream-only derivative material",
                    "no `e1` patch lane is active",
                ],
            )
            and contains_none(release_summary_text, ["later full plan-mode stage"])
            else "blocked",
            "notes": "The release summary should stay narrow while naming the active post-P9 follow-up explicitly.",
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
                    "`h3_stage_driver_consolidation_and_plan_index`",
                    "`p10_submission_packet_and_archival_repro_bundle`",
                    "`p11_manuscript_targeting_and_derivative_controls`",
                    "`f1_future_evidence_playbooks`",
                    "no `e1` patch lane is active on the current repo state",
                ],
            )
            else "blocked",
            "notes": "The current-stage driver should expose the full active consolidation packet in one place.",
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
                "active post-`P9` stage is checkpoint consolidation and archive packaging",
                "`H3` fixes driver/gate semantics",
                "`P10` builds a venue-agnostic submission/archive packet",
                "No `E1` patch lane is active",
                "does **not** claim",
            ],
        },
        {
            "path": "STATUS.md",
            "needles": [
                "`P8` stage is complete on the current frozen scope",
                "`P9` stage is complete on the same scope",
                "checkpoint consolidation and archive readiness",
                "`H3`, `P10`, `P11`, and `F1`",
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
                "paper_package_plan.md",
            ],
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "needles": [
                "`H3_stage_driver_consolidation_and_plan_index`",
                "`P10_submission_packet_and_archival_repro_bundle`",
                "`P11_manuscript_targeting_and_derivative_controls`",
                "`F1_future_evidence_playbooks`",
            ],
        },
        {
            "path": "docs/publication_record/release_summary_draft.md",
            "needles": [
                "This repository reproduces a narrow execution-substrate claim",
                "The active post-`P9` follow-up is checkpoint consolidation rather than claim expansion",
                "`H3` clarifies driver/gate semantics",
                "`P10` builds a venue-agnostic submission/archive packet",
                "No `E1` patch lane is active",
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
        "current_paper_phase": "post_p9_checkpoint_consolidation_active",
        "release_summary_role": "approved_downstream_short_update_source",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "execute the current H3/P10/P11/F1 consolidation packet while keeping current claim and artifact boundaries fixed"
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
