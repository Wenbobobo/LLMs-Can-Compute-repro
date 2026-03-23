"""Export the post-H43 live-surface wording guardrail packet for P34."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P34_post_h43_live_surface_wording_guardrail"

GUARDED_SURFACES: list[str] = [
    "docs/publication_record/current_stage_driver.md",
    "docs/publication_record/blog_outline.md",
    "docs/publication_record/blog_release_rules.md",
    "docs/publication_record/manuscript_stub_notes.md",
    "docs/publication_record/section_caption_notes.md",
    "docs/publication_record/caption_candidate_notes.md",
    "docs/publication_record/figure_table_narrative_roles.md",
    "docs/publication_record/manuscript_section_map.md",
    "docs/publication_record/appendix_boundary_map.md",
    "docs/publication_record/appendix_stub_notes.md",
    "docs/publication_record/appendix_companion_scope.md",
    "docs/publication_record/freeze_candidate_criteria.md",
    "docs/publication_record/reviewer_boundary_note.md",
    "docs/publication_record/claim_evidence_table.md",
    "docs/publication_record/release_summary_draft.md",
]

BLOCKED_SUBSTRINGS: tuple[str, ...] = (
    "current compiled endpoint",
    "current compiled boundary",
    "current d0 boundary",
    "present d0 scope",
    "current positive d0 suites",
    "whole current endpoint",
    "whole current paper endpoint",
)

ALLOWED_NEGATED_CONTEXTS: tuple[str, ...] = (
    "not the whole current endpoint",
    "not as the whole current endpoint",
    "rather than the whole current endpoint",
    "not the whole current paper endpoint",
    "not as the whole current paper endpoint",
    "rather than the whole current paper endpoint",
)


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


def find_blocked_lines(text: str) -> list[str]:
    hits: list[str] = []
    seen: set[str] = set()
    previous_line = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = normalize_text_space(line).lower()
        previous_lowered = normalize_text_space(previous_line).lower()
        combined_with_previous = normalize_text_space(f"{previous_line} {line}").lower()
        blocked_in_current = any(needle in lowered for needle in BLOCKED_SUBSTRINGS)
        blocked_across_boundary = any(
            needle in combined_with_previous and needle not in previous_lowered
            for needle in BLOCKED_SUBSTRINGS
        )
        if not blocked_in_current and not blocked_across_boundary:
            previous_line = line
            continue
        allowed_in_current = any(exception in lowered for exception in ALLOWED_NEGATED_CONTEXTS)
        allowed_across_boundary = any(
            exception in combined_with_previous and exception not in previous_lowered
            for exception in ALLOWED_NEGATED_CONTEXTS
        )
        if allowed_in_current or allowed_across_boundary:
            previous_line = line
            continue
        if line not in seen:
            hits.append(line)
            seen.add(line)
        previous_line = line
    return hits


def load_inputs() -> dict[str, Any]:
    guarded_surface_texts = {path: read_text(ROOT / path) for path in GUARDED_SURFACES}
    return {
        "p34_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P34_post_h43_live_surface_wording_guardrail" / "README.md"
        ),
        "p34_status_text": read_text(
            ROOT / "docs" / "milestones" / "P34_post_h43_live_surface_wording_guardrail" / "status.md"
        ),
        "p34_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P34_post_h43_live_surface_wording_guardrail" / "todo.md"
        ),
        "p34_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P34_post_h43_live_surface_wording_guardrail" / "acceptance.md"
        ),
        "p34_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P34_post_h43_live_surface_wording_guardrail" / "artifact_index.md"
        ),
        "design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-h43-p34-live-surface-wording-guardrail-design.md"
        ),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "guarded_surface_texts": guarded_surface_texts,
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "p31_summary": read_json(ROOT / "results" / "P31_post_h43_blog_guardrails_refresh" / "summary.json"),
        "p32_summary": read_json(ROOT / "results" / "P32_post_h43_historical_wording_refresh" / "summary.json"),
        "p33_summary": read_json(ROOT / "results" / "P33_post_h43_dormant_playbook_wording_refresh" / "summary.json"),
    }


def build_guarded_surface_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in GUARDED_SURFACES:
        blocked_lines = find_blocked_lines(inputs["guarded_surface_texts"][path])
        rows.append({"path": path, "blocked_lines": blocked_lines})
    return rows


def build_checklist_rows(inputs: dict[str, Any], guarded_surface_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked_guarded_paths = [row["path"] for row in guarded_surface_rows if row["blocked_lines"]]
    return [
        {
            "item_id": "p34_packet_docs_define_auxiliary_live_surface_guardrail",
            "status": "pass"
            if contains_all(
                inputs["p34_readme_text"],
                [
                    "completed auxiliary live-surface wording guardrail packet",
                    "does not displace `P31` as the current low-priority wave",
                ],
            )
            and contains_all(
                inputs["p34_status_text"],
                [
                    "active scientific stage remains `H43_post_r44_useful_case_refreeze`",
                    "current operational wave remains `P31_post_h43_blog_guardrails_refresh`",
                    "`P34_post_h43_live_surface_wording_guardrail` is recorded as a completed auxiliary",
                ],
            )
            and contains_all(
                inputs["p34_todo_text"],
                [
                    "machine-readable guardrail",
                    "restrict the lint scope to current live control/helper surfaces",
                    "add a focused `P34` exporter plus tests/results",
                ],
            )
            and contains_all(
                inputs["p34_acceptance_text"],
                [
                    "`P31` remains the current low-priority",
                    "`P32` and `P33` remain completed auxiliary wording packets",
                    "current live helper/control surfaces are machine-checked",
                ],
            )
            and contains_all(
                inputs["p34_artifact_index_text"],
                [
                    "docs/publication_record/current_stage_driver.md",
                    "docs/publication_record/blog_release_rules.md",
                    "results/P34_post_h43_live_surface_wording_guardrail/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`P34_post_h43_live_surface_wording_guardrail`",
                    "`live_surface_wording_guardrail_landed`",
                    "Rejected: keep relying on ad hoc manual wording sweeps",
                ],
            )
            else "blocked",
            "notes": "P34 should remain a narrow auxiliary guardrail packet and must not displace P31 or reopen any science lane.",
        },
        {
            "item_id": "guarded_live_surfaces_contain_no_affirmative_stale_current_endpoint_wording",
            "status": "pass" if not blocked_guarded_paths else "blocked",
            "notes": "Current live helper/control surfaces should not restate preserved D0 support as the whole current endpoint; only bounded negative phrasing like 'not the whole current endpoint' is allowed.",
            "blocked_paths": blocked_guarded_paths,
        },
        {
            "item_id": "indexes_and_handoff_preserve_p31_current_and_record_p34_auxiliary_completion",
            "status": "pass"
            if contains_all(
                inputs["status_text"],
                [
                    "guardrail refresh wave `P31`",
                    "`P32`",
                    "`P33`",
                    "`P34`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/plans/2026-03-24-post-h43-p34-live-surface-wording-guardrail-design.md",
                    "docs/milestones/P34_post_h43_live_surface_wording_guardrail/",
                    "results/P34_post_h43_live_surface_wording_guardrail/summary.json",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h43-p34-live-surface-wording-guardrail-design.md",
                    "../milestones/P34_post_h43_live_surface_wording_guardrail/",
                    "../milestones/P31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "P34_post_h43_live_surface_wording_guardrail/",
                    "P33_post_h43_dormant_playbook_wording_refresh/",
                    "P31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`P31_post_h43_blog_guardrails_refresh` is the current low-priority",
                    "`P34` is the completed auxiliary live-surface wording guardrail packet",
                    "wip/p34-h43-wording-guardrail-lint",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`H43` `P34` live-surface wording guardrail wave",
                    "scripts/export_p34_post_h43_live_surface_wording_guardrail.py",
                    "results/P34_post_h43_live_surface_wording_guardrail/summary.json",
                ],
            )
            else "blocked",
            "notes": "Status, index, and handoff surfaces should keep P31 current while recording P34 as a completed auxiliary wording-guardrail packet.",
        },
        {
            "item_id": "upstream_h43_p31_p32_and_p33_packets_remain_preserved",
            "status": "pass"
            if str(inputs["h43_summary"]["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(inputs["h43_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p31_summary"]["summary"]["selected_outcome"]) == "blocked_blog_guardrails_refreshed_to_h43"
            and str(inputs["p31_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and (
                str(inputs["p32_summary"]["summary"]["selected_outcome"])
                == "historical_wording_regeneration_surfaces_refreshed_to_h43"
            )
            and (
                str(inputs["p33_summary"]["summary"]["selected_outcome"])
                == "dormant_playbook_wording_surfaces_refreshed_to_h43"
            )
            else "blocked",
            "notes": "P34 should stay strictly downstream of the landed H43, P31, P32, and P33 packets while preserving their selected outcomes.",
        },
    ]


def build_snapshot(inputs: dict[str, Any], guarded_surface_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = [
        {
            "path": "docs/plans/2026-03-24-post-h43-p34-live-surface-wording-guardrail-design.md",
            "matched_lines": extract_matching_lines(
                inputs["design_text"],
                needles=["`P34_post_h43_live_surface_wording_guardrail`", "`live_surface_wording_guardrail_landed`"],
            ),
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "matched_lines": extract_matching_lines(
                inputs["guarded_surface_texts"]["docs/publication_record/current_stage_driver.md"],
                needles=["H43_post_r44_useful_case_refreeze", "no_active_downstream_runtime_lane"],
            ),
        },
        {
            "path": "docs/publication_record/blog_release_rules.md",
            "matched_lines": extract_matching_lines(
                inputs["guarded_surface_texts"]["docs/publication_record/blog_release_rules.md"],
                needles=["preserved first `D0` compiled boundary as earlier support rather than the whole current endpoint"],
            ),
        },
        {
            "path": "docs/publication_record/section_caption_notes.md",
            "matched_lines": extract_matching_lines(
                inputs["guarded_surface_texts"]["docs/publication_record/section_caption_notes.md"],
                needles=["preserved first compiled step inside the current `H43` paper-grade endpoint"],
            ),
        },
        {
            "path": "docs/publication_record/figure_table_narrative_roles.md",
            "matched_lines": extract_matching_lines(
                inputs["guarded_surface_texts"]["docs/publication_record/figure_table_narrative_roles.md"],
                needles=["preserved first compiled step inside the current `H43` endpoint, not the whole current endpoint"],
            ),
        },
        {
            "path": "docs/publication_record/release_summary_draft.md",
            "matched_lines": extract_matching_lines(
                inputs["guarded_surface_texts"]["docs/publication_record/release_summary_draft.md"],
                needles=["active endpoint on current evidence is the narrower Origin-core semantic-boundary line", "frozen by `H43`"],
            ),
        },
        {
            "path": "tmp/active_wave_plan.md",
            "matched_lines": extract_matching_lines(
                inputs["active_wave_plan_text"],
                needles=["`P34` is the completed auxiliary live-surface wording guardrail packet", "wip/p34-h43-wording-guardrail-lint"],
            ),
        },
    ]
    for row in guarded_surface_rows:
        if row["blocked_lines"]:
            rows.append({"path": row["path"], "matched_lines": row["blocked_lines"]})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]], guarded_surface_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    guarded_surface_count = len(guarded_surface_rows)
    clean_guarded_surface_count = sum(1 for row in guarded_surface_rows if not row["blocked_lines"])
    return {
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_active",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "refresh_packet": "p34_post_h43_live_surface_wording_guardrail",
        "refresh_scope": "current_live_control_and_helper_wording_guardrails",
        "selected_outcome": "live_surface_wording_guardrail_landed",
        "guarded_surface_count": guarded_surface_count,
        "clean_guarded_surface_count": clean_guarded_surface_count,
        "snapshot_surface_count": len(snapshot_rows),
        "next_required_lane": "no_active_downstream_runtime_lane",
        "check_count": len(checklist_rows),
        "pass_count": sum(1 for row in checklist_rows if row["status"] == "pass"),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    guarded_surface_rows = build_guarded_surface_rows(inputs)
    checklist_rows = build_checklist_rows(inputs, guarded_surface_rows)
    snapshot_rows = build_snapshot(inputs, guarded_surface_rows)
    summary = build_summary(checklist_rows, snapshot_rows, guarded_surface_rows)

    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p34_post_h43_live_surface_wording_guardrail",
            "environment": environment.as_dict(),
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p34_post_h43_live_surface_wording_guardrail",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p34_post_h43_live_surface_wording_guardrail",
            "environment": environment.as_dict(),
            "rows": snapshot_rows,
        },
    )


if __name__ == "__main__":
    main()
