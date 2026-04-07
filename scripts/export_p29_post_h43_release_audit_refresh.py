"""Export the post-H43 release-audit refresh packet for P29."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P29_post_h43_release_audit_refresh"


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


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    summary = summary_doc["summary"]
    if "blocked_count" in summary:
        return int(summary["blocked_count"])
    return int(summary["blocked_rows"])


def load_inputs() -> dict[str, Any]:
    return {
        "p29_readme_text": read_text(ROOT / "docs" / "milestones" / "P29_post_h43_release_audit_refresh" / "README.md"),
        "p29_status_text": read_text(ROOT / "docs" / "milestones" / "P29_post_h43_release_audit_refresh" / "status.md"),
        "p29_todo_text": read_text(ROOT / "docs" / "milestones" / "P29_post_h43_release_audit_refresh" / "todo.md"),
        "p29_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P29_post_h43_release_audit_refresh" / "acceptance.md"
        ),
        "p29_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P29_post_h43_release_audit_refresh" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-p29-release-audit-refresh-design.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "release_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "release_candidate_checklist.md"
        ),
        "submission_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md"
        ),
        "archival_manifest_text": read_text(
            ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"
        ),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "p28_summary": read_json(ROOT / "results" / "P28_post_h43_publication_surface_sync" / "summary.json"),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "preflight_summary": read_json(ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
        "p10_summary": read_json(ROOT / "results" / "P10_submission_archive_ready" / "summary.json"),
        "hygiene_summary": read_json(ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    hygiene = inputs["hygiene_summary"]["summary"]
    return [
        {
            "item_id": "p29_packet_docs_define_low_priority_release_audit_refresh_without_scientific_widening",
            "status": "pass"
            if contains_all(
                inputs["p29_readme_text"],
                [
                    "current low-priority operational release/public audit refresh packet downstream of landed `h43`",
                    "it is an operational/docs lane, not a scientific gate",
                ],
            )
            and contains_all(
                inputs["p29_status_text"],
                [
                    "active scientific stage remains `h43_post_r44_useful_case_refreeze`",
                    "current operational wave is `p29_post_h43_release_audit_refresh`",
                    "merge_executed = false",
                ],
            )
            and contains_all(
                inputs["p29_todo_text"],
                [
                    "refresh `release_preflight_checklist_audit`",
                    "refresh `p5_public_surface_sync`",
                    "refresh `h2_bundle_lock_audit` and `p10_submission_archive_ready`",
                    "remove orphan legacy hygiene outputs",
                ],
            )
            and contains_all(
                inputs["p29_acceptance_text"],
                [
                    "the packet remains operational/docs-only",
                    "`h43` remains the current active scientific stage",
                    "orphan legacy hygiene outputs are removed or explicitly unsupported",
                ],
            )
            and contains_all(
                inputs["p29_artifact_index_text"],
                [
                    "results/release_preflight_checklist_audit/summary.json",
                    "results/p5_public_surface_sync/summary.json",
                    "results/h2_bundle_lock_audit/summary.json",
                    "results/p10_submission_archive_ready/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p29_post_h43_release_audit_refresh`",
                    "`release_audit_surfaces_refreshed_to_h43`",
                    "rejected: refresh only `p5` and `release_preflight`",
                ],
            )
            else "blocked",
            "notes": "P29 should remain a docs-only operational refresh packet, not a new scientific stage.",
        },
        {
            "item_id": "refreshed_downstream_release_audits_are_green",
            "status": "pass"
            if blocked_count_from_summary(inputs["p5_summary"]) == 0
            and blocked_count_from_summary(inputs["preflight_summary"]) == 0
            and blocked_count_from_summary(inputs["h2_summary"]) == 0
            and blocked_count_from_summary(inputs["p10_summary"]) == 0
            and str(hygiene["branch"]) == "wip/p29-h43-release-audit-refresh"
            and str(hygiene["release_commit_state"]) == "clean_worktree_ready_if_other_gates_green"
            and str(hygiene["git_diff_check_state"]) == "clean"
            else "blocked",
            "notes": "The refreshed downstream audits should all be green on the clean P29 worktree snapshot.",
        },
        {
            "item_id": "refreshed_release_ledgers_present_current_h45_h43_stack",
            "status": "pass"
            if contains_all(
                inputs["release_candidate_text"],
                [
                    "current `h45` active docs-only decision packet plus preserved prior `h44`",
                    "results/r46_origin_useful_case_surface_generalization_gate/summary.json",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                inputs["submission_candidate_text"],
                [
                    "active `h43` docs-only useful-case",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                inputs["archival_manifest_text"],
                [
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                    "the current active docs-only packet is `h43`",
                    "completed `p27/p28` operational release-control pair",
                ],
            )
            and contains_none(
                inputs["release_candidate_text"] + "\n" + inputs["submission_candidate_text"] + "\n" + inputs["archival_manifest_text"],
                [
                    "current `h40` docs-only activation",
                    "active `h32` evidence",
                    "current docs-only `h34` control packet",
                ],
            )
            else "blocked",
            "notes": "Release-facing ledgers should no longer describe H40 or H32/H34 as current control, and should expose H45 as the current internal docs-only stage.",
        },
        {
            "item_id": "index_and_handoff_surfaces_preserve_p29_as_completed_prior_wave_under_p31_current_state",
            "status": "pass"
            if contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/milestones/p31_post_h43_blog_guardrails_refresh/",
                    "docs/milestones/p30_post_h43_manuscript_surface_refresh/",
                    "docs/milestones/p29_post_h43_release_audit_refresh/",
                    "results/p31_post_h43_blog_guardrails_refresh/summary.json",
                    "results/p30_post_h43_manuscript_surface_refresh/summary.json",
                    "results/p29_post_h43_release_audit_refresh/summary.json",
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
                    "`p30` is the completed prior manuscript-surface refresh wave",
                    "`p29` is the completed earlier prior release/public audit refresh wave",
                    "`p28` is the completed earlier publication/control sync wave",
                    "wip/p31-h43-blog-guardrails-refresh",
                ],
            )
            else "blocked",
            "notes": "Publication/index/handoff surfaces should preserve P29 as the completed earlier prior release-audit wave under current P31/P30 state.",
        },
        {
            "item_id": "upstream_h43_and_p28_results_remain_preserved",
            "status": "pass"
            if str(inputs["h43_summary"]["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(inputs["h43_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p28_summary"]["summary"]["selected_outcome"]) == "publication_surfaces_synced_to_h43"
            and str(inputs["p28_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            else "blocked",
            "notes": "P29 should stay strictly downstream of the landed H43 and P28 packets.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/milestones/P29_post_h43_release_audit_refresh/README.md": (
            "p29_readme_text",
            ["release/public audit refresh packet", "operational/docs lane"],
        ),
        "docs/milestones/P29_post_h43_release_audit_refresh/status.md": (
            "p29_status_text",
            ["current operational wave is `P29_post_h43_release_audit_refresh`", "merge_executed = false"],
        ),
        "docs/plans/2026-03-24-post-h43-p29-release-audit-refresh-design.md": (
            "design_text",
            ["`P29_post_h43_release_audit_refresh`", "`release_audit_surfaces_refreshed_to_h43`"],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            [
                "docs/milestones/P31_post_h43_blog_guardrails_refresh/",
                "docs/milestones/P30_post_h43_manuscript_surface_refresh/",
                "docs/milestones/P29_post_h43_release_audit_refresh/",
                "results/P29_post_h43_release_audit_refresh/summary.json",
            ],
        ),
        "docs/plans/README.md": (
            "plans_index_text",
            [
                "../milestones/P31_post_h43_blog_guardrails_refresh/",
                "../milestones/P30_post_h43_manuscript_surface_refresh/",
                "../milestones/P29_post_h43_release_audit_refresh/",
            ],
        ),
        "docs/milestones/README.md": (
            "milestones_index_text",
            [
                "P31_post_h43_blog_guardrails_refresh/",
                "P30_post_h43_manuscript_surface_refresh/",
                "P29_post_h43_release_audit_refresh/",
                "P28_post_h43_publication_surface_sync/",
            ],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            [
                "`P31_post_h43_blog_guardrails_refresh` is the current low-priority",
                "`P29` is the completed earlier prior release/public audit refresh wave",
                "wip/p31-h43-blog-guardrails-refresh",
            ],
        ),
        "results/release_worktree_hygiene_snapshot/summary.json": (
            "hygiene_summary_text",
            ['"branch": "wip/p29-h43-release-audit-refresh"', '"release_commit_state": "clean_worktree_ready_if_other_gates_green"'],
        ),
    }
    rows: list[dict[str, object]] = []
    text_inputs = {
        **inputs,
        "hygiene_summary_text": json.dumps(inputs["hygiene_summary"], indent=2),
    }
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(text_inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_active",
        "refresh_packet": "p29_post_h43_release_audit_refresh",
        "refresh_scope": "release_public_audits_and_ledgers",
        "selected_outcome": "release_audit_surfaces_refreshed_to_h43",
        "refreshed_audit_count": 5,
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
            "experiment": "p29_post_h43_release_audit_refresh_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p29_post_h43_release_audit_refresh_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p29_post_h43_release_audit_refresh",
            "environment": environment.as_dict(),
            "summary": summary,
        },
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
