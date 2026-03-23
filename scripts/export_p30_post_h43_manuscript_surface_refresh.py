"""Export the post-H43 manuscript-surface refresh packet for P30."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P30_post_h43_manuscript_surface_refresh"


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
        "p30_readme_text": read_text(ROOT / "docs" / "milestones" / "P30_post_h43_manuscript_surface_refresh" / "README.md"),
        "p30_status_text": read_text(ROOT / "docs" / "milestones" / "P30_post_h43_manuscript_surface_refresh" / "status.md"),
        "p30_todo_text": read_text(ROOT / "docs" / "milestones" / "P30_post_h43_manuscript_surface_refresh" / "todo.md"),
        "p30_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P30_post_h43_manuscript_surface_refresh" / "acceptance.md"
        ),
        "p30_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P30_post_h43_manuscript_surface_refresh" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-p30-manuscript-surface-refresh-design.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "paper_outline_text": read_text(ROOT / "docs" / "publication_record" / "paper_outline.md"),
        "manuscript_bundle_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_bundle_draft.md"),
        "paper_bundle_status_text": read_text(ROOT / "docs" / "publication_record" / "paper_bundle_status.md"),
        "derivative_pack_text": read_text(ROOT / "docs" / "publication_record" / "derivative_material_pack.md"),
        "abstract_pack_text": read_text(ROOT / "docs" / "publication_record" / "abstract_contribution_pack.md"),
        "release_note_text": read_text(ROOT / "docs" / "publication_record" / "external_release_note_skeleton.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "p28_summary": read_json(ROOT / "results" / "P28_post_h43_publication_surface_sync" / "summary.json"),
        "p29_summary": read_json(ROOT / "results" / "P29_post_h43_release_audit_refresh" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    current_docs_text = "\n".join(
        [
            inputs["status_text"],
            inputs["paper_outline_text"],
            inputs["manuscript_bundle_text"],
            inputs["paper_bundle_status_text"],
            inputs["derivative_pack_text"],
            inputs["abstract_pack_text"],
            inputs["release_note_text"],
            inputs["release_summary_text"],
        ]
    )
    return [
        {
            "item_id": "p30_packet_docs_define_low_priority_manuscript_surface_refresh_without_scientific_widening",
            "status": "pass"
            if contains_all(
                inputs["p30_readme_text"],
                [
                    "manuscript-surface refresh packet",
                    "operational/docs lane, not a scientific gate",
                ],
            )
            and contains_all(
                inputs["p30_status_text"],
                [
                    "active scientific stage remains `h43_post_r44_useful_case_refreeze`",
                    "current operational wave is `p30_post_h43_manuscript_surface_refresh`",
                    "merge_executed = false",
                ],
            )
            and contains_all(
                inputs["p30_todo_text"],
                [
                    "refresh `paper_outline.md`",
                    "refresh `manuscript_bundle_draft.md`, `paper_bundle_status.md`, and",
                    "refresh `derivative_material_pack.md`",
                    "export a focused `p30` summary/checklist/snapshot packet",
                ],
            )
            and contains_all(
                inputs["p30_acceptance_text"],
                [
                    "the packet remains operational/docs-only",
                    "`h43` remains the current active scientific stage",
                    "`p30` as the current low-priority wave",
                ],
            )
            and contains_all(
                inputs["p30_artifact_index_text"],
                [
                    "docs/publication_record/paper_outline.md",
                    "docs/publication_record/manuscript_bundle_draft.md",
                    "results/p30_post_h43_manuscript_surface_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p30_post_h43_manuscript_surface_refresh`",
                    "`manuscript_surfaces_refreshed_to_h43`",
                    "rejected: full manuscript rewrite",
                ],
            )
            else "blocked",
            "notes": "P30 should remain a docs-only operational manuscript refresh packet, not a new scientific stage.",
        },
        {
            "item_id": "refreshed_manuscript_surfaces_present_h43_as_current_endpoint",
            "status": "pass"
            if contains_all(
                inputs["paper_outline_text"],
                [
                    "current narrow no-widening scope under",
                    "active `h43`",
                    "completed `r42/r43/r44/r45` semantic-boundary",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h43_post_r44_useful_case_refreeze` under",
                    "completed prior low-priority sync packets `p30/p29/p28`",
                    "no active downstream runtime lane exists after `h43`",
                ],
            )
            and contains_all(
                inputs["derivative_pack_text"],
                [
                    "current `h43` endpoint",
                    "bounded semantic-boundary ladder",
                ],
            )
            and contains_all(
                inputs["abstract_pack_text"],
                [
                    "`h35 -> r40 -> h36 -> h37 -> h38 -> h40 -> r42 -> h41 -> p27 -> r43 -> r45 -> h42 -> r44 -> h43`",
                    "restricted useful-case surface",
                ],
            )
            and contains_all(
                inputs["release_note_text"],
                [
                    "bounded restricted-wasm / tiny-`c` useful-case ladder",
                    "preserved first `d0` compiled boundary",
                ],
            )
            and contains_all(
                inputs["paper_bundle_status_text"],
                [
                    "manuscript draft no longer terminates on the landed `h34`",
                    "`p30` aligns manuscript-facing prose baselines to landed `h43`",
                ],
            )
            and contains_all(
                inputs["manuscript_bundle_text"],
                [
                    "ending explicitly at",
                    "-> h43`",
                    "after `h43`",
                ],
            )
            and contains_all(
                inputs["release_summary_text"],
                [
                    "`p30` now refreshes the manuscript-facing bundle to the landed `h43` state",
                    "`p29` aligns release/public audit surfaces to landed `h43`",
                ],
            )
            and contains_none(
                current_docs_text,
                [
                    "active `h32` plus docs-only `h34`",
                    "current `h32/h34` endpoint",
                    "terminates on the landed `h34` state",
                    "manuscript draft still terminates on the landed `h34` narrative line",
                    "named `e1` patch lane",
                    "the current active post-`p9` operational stage is `h36_post_r40_bounded_scalar_family_refreeze`",
                    "`p24` preserved as the current docs-only sync packet",
                    "no active downstream runtime lane exists after `h36`",
                ],
            )
            else "blocked",
            "notes": "Paper-facing prose should treat H43 as the current manuscript endpoint and H32/H34 as preserved earlier support only.",
        },
        {
            "item_id": "index_and_handoff_surfaces_record_p30_as_completed_prior_wave_under_p31_current_state",
            "status": "pass"
            if contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/milestones/p31_post_h43_blog_guardrails_refresh/",
                    "docs/milestones/p30_post_h43_manuscript_surface_refresh/",
                    "results/p31_post_h43_blog_guardrails_refresh/summary.json",
                    "results/p30_post_h43_manuscript_surface_refresh/summary.json",
                    "docs/milestones/p29_post_h43_release_audit_refresh/",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "../milestones/p31_post_h43_blog_guardrails_refresh/",
                    "../milestones/p30_post_h43_manuscript_surface_refresh/",
                    "../milestones/p29_post_h43_release_audit_refresh/",
                    "../milestones/p28_post_h43_publication_surface_sync/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "p31_post_h43_blog_guardrails_refresh/",
                    "p30_post_h43_manuscript_surface_refresh/",
                    "p29_post_h43_release_audit_refresh/",
                    "p28_post_h43_publication_surface_sync/",
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
                    "post-`h43` `p30` manuscript-surface refresh wave",
                    "scripts/export_p30_post_h43_manuscript_surface_refresh.py",
                    "results/p30_post_h43_manuscript_surface_refresh/summary.json",
                ],
            )
            else "blocked",
            "notes": "Indexes and handoff docs should record P30 as the completed prior manuscript wave under current P31 state.",
        },
        {
            "item_id": "upstream_h43_p28_and_p29_packets_remain_preserved",
            "status": "pass"
            if str(inputs["h43_summary"]["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(inputs["h43_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p28_summary"]["summary"]["selected_outcome"]) == "publication_surfaces_synced_to_h43"
            and str(inputs["p29_summary"]["summary"]["selected_outcome"]) == "release_audit_surfaces_refreshed_to_h43"
            and str(inputs["p29_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            else "blocked",
            "notes": "P30 should stay strictly downstream of the landed H43, P28, and P29 packets.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/milestones/P30_post_h43_manuscript_surface_refresh/README.md": (
            "p30_readme_text",
            ["manuscript-surface refresh packet", "operational/docs lane"],
        ),
        "docs/plans/2026-03-24-post-h43-p30-manuscript-surface-refresh-design.md": (
            "design_text",
            ["`P30_post_h43_manuscript_surface_refresh`", "`manuscript_surfaces_refreshed_to_h43`"],
        ),
        "STATUS.md": (
            "status_text",
            ["`H43_post_r44_useful_case_refreeze` under", "completed prior low-priority sync packets `P30/P29/P28`"],
        ),
        "docs/publication_record/paper_outline.md": (
            "paper_outline_text",
            ["active `H43`", "`H32/H34` compiled-boundary line", "`H40 -> R42 -> F20 -> H41 -> P27 -> R43 -> R45 -> H42 -> R44 -> H43`"],
        ),
        "docs/publication_record/paper_bundle_status.md": (
            "paper_bundle_status_text",
            ["manuscript draft no longer terminates on the landed `H34`", "`P30` aligns manuscript-facing prose baselines to landed `H43`"],
        ),
        "docs/publication_record/manuscript_bundle_draft.md": (
            "manuscript_bundle_text",
            ["ending explicitly at", "after `H43`"],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            ["`P30` now refreshes the manuscript-facing bundle to the landed `H43` state", "`P29` aligns release/public audit surfaces to landed `H43`"],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            [
                "docs/milestones/P31_post_h43_blog_guardrails_refresh/",
                "docs/milestones/P30_post_h43_manuscript_surface_refresh/",
                "results/P30_post_h43_manuscript_surface_refresh/summary.json",
            ],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            [
                "`P31_post_h43_blog_guardrails_refresh` is the current low-priority",
                "`P30` is the completed prior manuscript-surface refresh wave",
                "wip/p31-h43-blog-guardrails-refresh",
            ],
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
        "refresh_packet": "p30_post_h43_manuscript_surface_refresh",
        "refresh_scope": "manuscript_and_derivative_surfaces",
        "selected_outcome": "manuscript_surfaces_refreshed_to_h43",
        "refreshed_surface_count": 8,
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
            "experiment": "p30_post_h43_manuscript_surface_refresh_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p30_post_h43_manuscript_surface_refresh_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p30_post_h43_manuscript_surface_refresh",
            "environment": environment.as_dict(),
            "summary": summary,
        },
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
