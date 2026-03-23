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
    path.parent.mkdir(parents=True, exist_ok=True)
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
            if contains_all(
                readme_text,
                [
                    "does **not** claim that general llms are computers",
                    "arbitrary c has been reproduced",
                ],
            )
            else "blocked",
            "notes": "README keeps the narrow-scope guardrails explicit.",
        },
        {
            "item_id": "readme_tracks_current_active_stage",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "the current active stage is",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "`promotion_mode = explicit_merge_wave` and `merge_executed = false`",
                    "no active downstream runtime lane now follows `h43`",
                ],
            )
            else "blocked",
            "notes": "README should keep H43 as current while preserving the landed H42/H41/H36/R43/R44/R45/P27 stack.",
        },
        {
            "item_id": "status_tracks_current_active_stage",
            "status": "pass"
            if contains_all(
                status_text,
                [
                    "`h43_post_r44_useful_case_refreeze`",
                    "`h42_post_r43_route_selection_packet`",
                    "`h36_post_r40_bounded_scalar_family_refreeze`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "`promotion_mode = explicit_merge_wave` and `merge_executed = false`",
                ],
            )
            else "blocked",
            "notes": "STATUS should record the current H43 stack and explicit merge posture.",
        },
        {
            "item_id": "publication_record_readme_tracks_h43_and_current_p30_state",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "current `h43` docs-only useful-case refreeze packet",
                    "`r42`, `r43`, `r44`, and `r45`",
                    "`merge_executed = false`",
                    "docs/milestones/p30_post_h43_manuscript_surface_refresh/",
                    "results/p30_post_h43_manuscript_surface_refresh/summary.json",
                    "2026-03-24-post-h43-p29-release-audit-refresh-design.md",
                    "docs/milestones/p29_post_h43_release_audit_refresh/",
                    "results/p29_post_h43_release_audit_refresh/summary.json",
                    "docs/milestones/p28_post_h43_publication_surface_sync/",
                ],
            )
            else "blocked",
            "notes": "Publication record README should expose H43 as current, P30 as the current manuscript-surface wave, and P29/P28 as completed prior sync packets.",
        },
        {
            "item_id": "release_summary_stays_downstream_of_landed_h43_stack",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "`h43_post_r44_useful_case_refreeze`",
                    "completed current semantic-boundary gate stack",
                    "`p28` aligns publication-facing ledgers to landed `h43`",
                    "no active downstream runtime lane exists after `h43`",
                ],
            )
            and contains_none(release_summary_text, ["later full plan-mode stage"])
            else "blocked",
            "notes": "The release summary should remain downstream of the landed H43 stack and publication sync.",
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
                ],
            )
            and contains_none(manuscript_text, ["Status: paper-shaped manuscript section draft"])
            else "blocked",
            "notes": "The manuscript remains a section-ordered draft rather than a stage-status note.",
        },
        {
            "item_id": "current_stage_driver_is_canonical",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "the current active stage is:",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r44_origin_restricted_wasm_useful_case_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                    "`p27_post_h41_clean_promotion_and_explicit_merge_packet`",
                    "`merge_executed = false`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            else "blocked",
            "notes": "The current-stage driver should remain the canonical H43 control surface.",
        },
        {
            "item_id": "layout_log_records_post_p7_decisions",
            "status": "pass"
            if contains_all(
                layout_log_text,
                ["Release-summary reuse", "Post-`P7` next phase", "Evidence reopen discipline"],
            )
            else "blocked",
            "notes": "The layout decision log should record release-summary reuse and governance choices.",
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
            "notes": "The completed P8/P9 digests should remain explicit as the bundle-lock baseline.",
        },
    ]


def build_surface_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    snapshots = [
        {
            "path": "README.md",
            "needles": [
                "`H43_post_r44_useful_case_refreeze`",
                "`R44_origin_restricted_wasm_useful_case_execution_gate`",
                "`R45_origin_dual_mode_model_mainline_gate`",
                "`promotion_mode = explicit_merge_wave` and `merge_executed = false`",
            ],
        },
        {
            "path": "STATUS.md",
            "needles": [
                "`H43_post_r44_useful_case_refreeze`",
                "`H42_post_r43_route_selection_packet`",
                "`H36_post_r40_bounded_scalar_family_refreeze`",
                "`R43_origin_bounded_memory_small_vm_execution_gate`",
            ],
        },
        {
            "path": "docs/publication_record/README.md",
            "needles": [
                "docs/milestones/P30_post_h43_manuscript_surface_refresh/",
                "results/P30_post_h43_manuscript_surface_refresh/summary.json",
                "2026-03-24-post-h43-p29-release-audit-refresh-design.md",
                "docs/milestones/P29_post_h43_release_audit_refresh/",
                "results/P29_post_h43_release_audit_refresh/summary.json",
                "docs/milestones/P28_post_h43_publication_surface_sync/",
            ],
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "needles": [
                "`H43_post_r44_useful_case_refreeze`",
                "`R44_origin_restricted_wasm_useful_case_execution_gate`",
                "`R45_origin_dual_mode_model_mainline_gate`",
                "`no_active_downstream_runtime_lane`",
            ],
        },
        {
            "path": "docs/publication_record/release_summary_draft.md",
            "needles": [
                "`H43_post_r44_useful_case_refreeze`",
                "completed current semantic-boundary gate stack",
                "`P28` aligns publication-facing ledgers to landed `H43`",
            ],
        },
        {
            "path": "docs/publication_record/manuscript_bundle_draft.md",
            "needles": [
                "## 1. Abstract",
                "Companion appendix material stays clearly downstream",
                "## 10. Reproducibility Appendix",
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
    input_key_by_path = {
        "README.md": "readme_text",
        "STATUS.md": "status_text",
        "docs/publication_record/README.md": "publication_readme_text",
        "docs/publication_record/current_stage_driver.md": "current_stage_driver_text",
        "docs/publication_record/release_summary_draft.md": "release_summary_text",
        "docs/publication_record/manuscript_bundle_draft.md": "manuscript_text",
        "docs/publication_record/layout_decision_log.md": "layout_log_text",
        "docs/milestones/P8_submission_candidate_and_bundle_lock/result_digest.md": "p8_result_digest_text",
        "docs/milestones/P9_release_candidate_and_public_surface_freeze/result_digest.md": "p9_result_digest_text",
    }
    for row in snapshots:
        input_key = input_key_by_path[str(row["path"])]
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
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_active",
        "internal_driver_phase": "h43_post_r44_useful_case_refreeze_active",
        "release_summary_role": "approved_downstream_short_update_source",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "keep the outward-facing H43 publication surface aligned while treating P30 as the current low-priority manuscript-surface refresh wave, P29 as the completed prior release/public audit refresh wave, P28 as the completed publication/control sync packet, P27 as the completed explicit merge packet with merge_executed = false, H42/H41 as preserved prior docs-only packets, H36 as the preserved routing/refreeze packet, R42/R43/R44/R45 as the completed current gate stack, and no_active_downstream_runtime_lane as the current follow-on state"
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
                "landed H43 stack, the current outward release summary, and the current low-priority",
                "manuscript/publication follow-on packets.",
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
