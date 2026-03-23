"""Export the post-H43 blocked-blog/helper refresh packet for P31."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P31_post_h43_blog_guardrails_refresh"


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


def load_inputs() -> dict[str, Any]:
    return {
        "p31_readme_text": read_text(ROOT / "docs" / "milestones" / "P31_post_h43_blog_guardrails_refresh" / "README.md"),
        "p31_status_text": read_text(ROOT / "docs" / "milestones" / "P31_post_h43_blog_guardrails_refresh" / "status.md"),
        "p31_todo_text": read_text(ROOT / "docs" / "milestones" / "P31_post_h43_blog_guardrails_refresh" / "todo.md"),
        "p31_acceptance_text": read_text(ROOT / "docs" / "milestones" / "P31_post_h43_blog_guardrails_refresh" / "acceptance.md"),
        "p31_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P31_post_h43_blog_guardrails_refresh" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-p31-blog-guardrails-refresh-design.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "blog_outline_text": read_text(ROOT / "docs" / "publication_record" / "blog_outline.md"),
        "blog_rules_text": read_text(ROOT / "docs" / "publication_record" / "blog_release_rules.md"),
        "manuscript_stub_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_stub_notes.md"),
        "section_caption_text": read_text(ROOT / "docs" / "publication_record" / "section_caption_notes.md"),
        "caption_candidate_text": read_text(ROOT / "docs" / "publication_record" / "caption_candidate_notes.md"),
        "figure_roles_text": read_text(ROOT / "docs" / "publication_record" / "figure_table_narrative_roles.md"),
        "manuscript_section_map_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_section_map.md"),
        "appendix_boundary_map_text": read_text(ROOT / "docs" / "publication_record" / "appendix_boundary_map.md"),
        "appendix_stub_text": read_text(ROOT / "docs" / "publication_record" / "appendix_stub_notes.md"),
        "appendix_companion_text": read_text(ROOT / "docs" / "publication_record" / "appendix_companion_scope.md"),
        "freeze_candidate_text": read_text(ROOT / "docs" / "publication_record" / "freeze_candidate_criteria.md"),
        "reviewer_boundary_text": read_text(ROOT / "docs" / "publication_record" / "reviewer_boundary_note.md"),
        "claim_evidence_text": read_text(ROOT / "docs" / "publication_record" / "claim_evidence_table.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "p30_summary": read_json(ROOT / "results" / "P30_post_h43_manuscript_surface_refresh" / "summary.json"),
        "p29_summary": read_json(ROOT / "results" / "P29_post_h43_release_audit_refresh" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    current_docs_text = "\n".join(
        [
            inputs["status_text"],
            inputs["blog_outline_text"],
            inputs["blog_rules_text"],
            inputs["manuscript_stub_text"],
            inputs["section_caption_text"],
            inputs["caption_candidate_text"],
            inputs["figure_roles_text"],
            inputs["manuscript_section_map_text"],
            inputs["appendix_boundary_map_text"],
            inputs["appendix_stub_text"],
            inputs["appendix_companion_text"],
            inputs["freeze_candidate_text"],
            inputs["reviewer_boundary_text"],
            inputs["claim_evidence_text"],
            inputs["release_summary_text"],
            inputs["publication_readme_text"],
            inputs["active_wave_plan_text"],
        ]
    )
    return [
        {
            "item_id": "p31_packet_docs_define_low_priority_blog_guardrail_refresh_without_scientific_widening",
            "status": "pass"
            if contains_all(
                inputs["p31_readme_text"],
                [
                    "blocked-blog/helper guardrail refresh packet",
                    "does not unblock blog release",
                ],
            )
            and contains_all(
                inputs["p31_status_text"],
                [
                    "active scientific stage remains `h43_post_r44_useful_case_refreeze`",
                    "current operational wave is `p31_post_h43_blog_guardrails_refresh`",
                    "blog release remain blocked here",
                ],
            )
            and contains_all(
                inputs["p31_todo_text"],
                [
                    "refresh `blog_outline.md`",
                    "refresh `blog_release_rules.md`",
                    "export a focused `p31` summary/checklist/snapshot packet",
                ],
            )
            and contains_all(
                inputs["p31_acceptance_text"],
                [
                    "the packet remains operational/docs-only",
                    "`h43` remains the current active scientific stage",
                    "blog release remains blocked",
                ],
            )
            and contains_all(
                inputs["p31_artifact_index_text"],
                [
                    "docs/publication_record/blog_outline.md",
                    "docs/publication_record/blog_release_rules.md",
                    "results/p31_post_h43_blog_guardrails_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p31_post_h43_blog_guardrails_refresh`",
                    "`blocked_blog_guardrails_refreshed_to_h43`",
                    "rejected: broader public blog release",
                ],
            )
            else "blocked",
            "notes": "P31 should remain a docs-only blocked-blog/helper refresh packet and must not unblock release or widen the scientific stage.",
        },
        {
            "item_id": "blocked_blog_guardrails_treat_h43_as_current_paper_grade_endpoint",
            "status": "pass"
            if contains_all(
                inputs["blog_outline_text"],
                [
                    "landed `h43` post-`r44` useful-case refreeze packet",
                    "completed `r43/r44/r45` stack explicit",
                    "preserved first `d0` compiled boundary as earlier support rather than as the whole current finish line",
                ],
            )
            and contains_all(
                inputs["blog_rules_text"],
                [
                    "small-vm execution in `r43`",
                    "coequal `r45` model support as non-substitutive",
                    "restricted useful-case support in `r44`",
                    "preserved first `d0` compiled boundary as earlier support rather than the whole current endpoint",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/milestones/p31_post_h43_blog_guardrails_refresh/",
                    "present `h43` paper-grade endpoint",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "guardrail refresh wave `p31`",
                ],
            )
            and contains_none(
                current_docs_text,
                [
                    "landed `h34` post-`r39` scope-decision packet",
                    "`d0` as the compiled stop point",
                    "current complete-for-now compiled-boundary state",
                    "current low-priority manuscript-surface refresh wave `p30`",
                    "`p30` remains the current low-priority manuscript-surface refresh wave",
                ],
            )
            else "blocked",
            "notes": "Blocked blog/helper docs should preserve the current H43 paper-grade endpoint and treat D0 as earlier support only.",
        },
        {
            "item_id": "manuscript_and_appendix_helper_docs_treat_d0_as_preserved_first_compiled_step",
            "status": "pass"
            if contains_all(
                inputs["manuscript_stub_text"],
                [
                    "broader current `h43` paper endpoint",
                    "preserved first compiled step at tiny typed bytecode",
                ],
            )
            and contains_all(
                inputs["section_caption_text"],
                [
                    "preserved first compiled step inside the current `h43` paper-grade endpoint",
                    "broader current `h43` endpoint",
                ],
            )
            and contains_all(
                inputs["caption_candidate_text"],
                [
                    "current paper-grade endpoint covers append-only traces",
                    "preserved first tiny typed-bytecode `d0` compiled step",
                ],
            )
            and contains_all(
                inputs["figure_roles_text"],
                [
                    "preserved first compiled step inside the current `h43` endpoint",
                    "preserved-first-step `d0` starter suite",
                ],
            )
            and contains_all(
                inputs["manuscript_section_map_text"],
                [
                    "preserved first compiled step is the tiny typed-bytecode `d0` boundary inside the broader current `h43` paper endpoint",
                ],
            )
            and contains_all(
                inputs["appendix_boundary_map_text"],
                [
                    "appendix companions to the broader `h43` paper endpoint",
                    "preserved first compiled step",
                ],
            )
            and contains_all(
                inputs["appendix_stub_text"],
                [
                    "`d0` memory-surface diagnostics",
                    "preserved first `d0` compiled step",
                ],
            )
            and contains_all(
                inputs["appendix_companion_text"],
                [
                    "preserved first compiled step",
                ],
            )
            and contains_all(
                inputs["freeze_candidate_text"],
                [
                    "preserved first tiny typed-bytecode `d0` compiled step inside the broader `h43` paper-grade endpoint",
                ],
            )
            and contains_all(
                inputs["reviewer_boundary_text"],
                [
                    "narrow restricted useful-case paper endpoint",
                    "preserved first tiny typed-bytecode `d0`",
                ],
            )
            and contains_all(
                inputs["claim_evidence_text"],
                [
                    "preserved first compiled step stays on tiny",
                ],
            )
            and contains_all(
                inputs["release_summary_text"],
                [
                    "active endpoint on current evidence is the narrower origin-core semantic-boundary line",
                    "frozen by `h43`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "preserved first `d0` compiled step",
                ],
            )
            and contains_none(
                current_docs_text,
                [
                    "current compiled endpoint",
                    "current compiled claim ends at tiny typed bytecode `d0`",
                    "tiny typed bytecode is the endpoint on current evidence",
                    "current bounded `d0` packet",
                    "current endpoint stays on tiny typed bytecode",
                    "the validated scope ends at append-only traces, exact retrieval, a narrow precision boundary, and a tiny typed-bytecode `d0` endpoint",
                ],
            )
            else "blocked",
            "notes": "Helper docs should present D0 as preserved first compiled support within the broader current H43 endpoint, not as the whole current paper endpoint.",
        },
        {
            "item_id": "index_and_handoff_surfaces_record_p31_as_current_low_priority_wave",
            "status": "pass"
            if contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/milestones/p31_post_h43_blog_guardrails_refresh/",
                    "results/p31_post_h43_blog_guardrails_refresh/summary.json",
                    "docs/milestones/p30_post_h43_manuscript_surface_refresh/",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "../milestones/p31_post_h43_blog_guardrails_refresh/",
                    "../milestones/p30_post_h43_manuscript_surface_refresh/",
                    "2026-03-24-post-h43-p31-blog-guardrails-refresh-design.md",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "p31_post_h43_blog_guardrails_refresh/",
                    "p30_post_h43_manuscript_surface_refresh/",
                    "p29_post_h43_release_audit_refresh/",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`p31_post_h43_blog_guardrails_refresh` is the current low-priority",
                    "wip/p31-h43-blog-guardrails-refresh",
                    "`p30` is the completed prior manuscript-surface refresh wave",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h43` `p31` blog-guardrail refresh wave",
                    "scripts/export_p31_post_h43_blog_guardrails_refresh.py",
                    "results/p31_post_h43_blog_guardrails_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`p31` remains the current",
                    "blog/helper guardrail refresh wave",
                ],
            )
            else "blocked",
            "notes": "Indexes and handoff docs should record P31 as the current low-priority helper-doc wave downstream of H43.",
        },
        {
            "item_id": "upstream_h43_p30_and_p29_packets_remain_preserved",
            "status": "pass"
            if str(inputs["h43_summary"]["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(inputs["h43_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p30_summary"]["summary"]["selected_outcome"]) == "manuscript_surfaces_refreshed_to_h43"
            and str(inputs["p30_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p29_summary"]["summary"]["selected_outcome"]) == "release_audit_surfaces_refreshed_to_h43"
            and str(inputs["p29_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            else "blocked",
            "notes": "P31 should stay strictly downstream of the landed H43, P30, and P29 packets.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/milestones/P31_post_h43_blog_guardrails_refresh/README.md": (
            "p31_readme_text",
            ["blocked-blog/helper guardrail refresh packet", "does not unblock blog release"],
        ),
        "docs/plans/2026-03-24-post-h43-p31-blog-guardrails-refresh-design.md": (
            "design_text",
            ["`P31_post_h43_blog_guardrails_refresh`", "`blocked_blog_guardrails_refreshed_to_h43`"],
        ),
        "docs/publication_record/blog_outline.md": (
            "blog_outline_text",
            ["landed `H43` post-`R44` useful-case refreeze packet", "completed `R43/R44/R45` stack explicit"],
        ),
        "docs/publication_record/blog_release_rules.md": (
            "blog_rules_text",
            ["small-VM execution in `R43`", "coequal `R45` model support as non-substitutive"],
        ),
        "docs/publication_record/manuscript_stub_notes.md": (
            "manuscript_stub_text",
            ["broader current `H43` paper endpoint", "preserved first compiled step at tiny typed bytecode"],
        ),
        "docs/publication_record/section_caption_notes.md": (
            "section_caption_text",
            ["preserved first compiled step inside the current `H43` paper-grade endpoint", "broader current `H43` endpoint"],
        ),
        "docs/publication_record/appendix_boundary_map.md": (
            "appendix_boundary_map_text",
            ["appendix companions to the broader `H43` paper endpoint", "preserved first compiled step"],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            ["origin-core semantic-boundary line", "frozen by `H43`"],
        ),
        "STATUS.md": (
            "status_text",
            ["current low-priority blocked-blog/helper guardrail refresh wave `P31`", "completed prior low-priority sync packets `P30/P29/P28`"],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            ["docs/milestones/P31_post_h43_blog_guardrails_refresh/", "results/P31_post_h43_blog_guardrails_refresh/summary.json"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`P31_post_h43_blog_guardrails_refresh` is the current low-priority", "wip/p31-h43-blog-guardrails-refresh"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_active",
        "refresh_packet": "p31_post_h43_blog_guardrails_refresh",
        "refresh_scope": "blocked_blog_and_manuscript_helper_guardrails",
        "selected_outcome": "blocked_blog_guardrails_refreshed_to_h43",
        "refreshed_surface_count": 20,
        "next_required_lane": "no_active_downstream_runtime_lane",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p31_post_h43_blog_guardrails_refresh_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p31_post_h43_blog_guardrails_refresh_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p31_post_h43_blog_guardrails_refresh",
            "environment": environment.as_dict(),
            "summary": summary,
        },
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
