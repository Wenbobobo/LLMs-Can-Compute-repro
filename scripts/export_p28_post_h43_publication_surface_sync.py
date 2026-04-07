"""Export the post-H43 publication-surface sync packet for P28."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P28_post_h43_publication_surface_sync"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    return {
        "p28_readme_text": read_text(ROOT / "docs" / "milestones" / "P28_post_h43_publication_surface_sync" / "README.md"),
        "p28_status_text": read_text(ROOT / "docs" / "milestones" / "P28_post_h43_publication_surface_sync" / "status.md"),
        "p28_todo_text": read_text(ROOT / "docs" / "milestones" / "P28_post_h43_publication_surface_sync" / "todo.md"),
        "p28_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P28_post_h43_publication_surface_sync" / "acceptance.md"
        ),
        "p28_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P28_post_h43_publication_surface_sync" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-p28-publication-surface-sync-design.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "claim_evidence_text": read_text(ROOT / "docs" / "publication_record" / "claim_evidence_table.md"),
        "paper_bundle_status_text": read_text(ROOT / "docs" / "publication_record" / "paper_bundle_status.md"),
        "release_preflight_text": read_text(ROOT / "docs" / "publication_record" / "release_preflight_checklist.md"),
        "release_summary_draft_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "release_summary_outline_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_outline.md"),
        "review_boundary_text": read_text(ROOT / "docs" / "publication_record" / "review_boundary_summary.md"),
        "submission_packet_index_text": read_text(ROOT / "docs" / "publication_record" / "submission_packet_index.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "r44_summary": read_json(ROOT / "results" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "summary.json"),
        "r45_summary": read_json(ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate" / "summary.json"),
        "r43_summary": read_json(ROOT / "results" / "R43_origin_bounded_memory_small_vm_execution_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h43 = inputs["h43_summary"]["summary"]
    r44 = inputs["r44_summary"]["summary"]["gate"]
    r45 = inputs["r45_summary"]["summary"]["gate"]
    r43 = inputs["r43_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "p28_packet_docs_define_low_priority_publication_sync_without_scientific_widening",
            "status": "pass"
            if contains_all(
                inputs["p28_readme_text"],
                [
                    "completed low-priority publication/control sync packet downstream of landed `h43`",
                    "it is an operational/docs lane, not a scientific gate",
                ],
            )
            and contains_all(
                inputs["p28_status_text"],
                [
                    "active scientific stage remains `h43_post_r44_useful_case_refreeze`",
                    "current completed exact gate remains",
                    "`next_required_lane = no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["p28_todo_text"],
                [
                    "stop describing `r43` and `r44` as deferred",
                    "keep `r41`, `r29`, `f3`, arbitrary `c`, and merge-to-`main` blocked here",
                    "preserve `h43` as the active scientific stage",
                ],
            )
            and contains_all(
                inputs["p28_acceptance_text"],
                [
                    "the packet remains operational/docs-only",
                    "`h43` remains the current active scientific stage",
                    "no active downstream runtime lane is created after `h43`",
                ],
            )
            and contains_all(
                inputs["p28_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-h43-p28-publication-surface-sync-design.md",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p28_post_h43_publication_surface_sync`",
                    "`publication_surfaces_synced_to_h43`",
                    "`next_required_lane = no_active_downstream_runtime_lane`",
                    "rejected: merge review now",
                ],
            )
            else "blocked",
            "notes": "P28 should remain a docs-only publication sync packet, not a new scientific stage.",
        },
        {
            "item_id": "upstream_h43_r44_r45_r43_and_p27_results_justify_the_synced_surface",
            "status": "pass"
            if str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(h43["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(r44["lane_verdict"]) == "useful_case_surface_supported_narrowly"
            and int(r44["exact_kernel_count"]) == 3
            and str(r45["lane_verdict"]) == "coequal_model_lane_supported_without_replacing_exact"
            and int(r45["exact_mode_count"]) == 2
            and str(r43["lane_verdict"]) == "keep_semantic_boundary_route"
            and int(r43["exact_family_count"]) == 5
            and str(p27["promotion_mode"]) == "explicit_merge_wave"
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "The synced publication surface must stay grounded in the landed H43/R44/R45/R43/P27 result stack.",
        },
        {
            "item_id": "publication_ledgers_now_preserve_h43_as_paper_endpoint_under_h45_r47_current_stack",
            "status": "pass"
            if contains_all(
                inputs["publication_readme_text"],
                [
                    "`h45` as the current active docs-only stage",
                    "`r47` as the next required exact runtime candidate",
                    "`f22` as a saved blocked comparator bundle",
                    "`no_active_downstream_runtime_lane` as the landed paper-grade closeout",
                ],
            )
            and contains_all(
                inputs["claim_evidence_text"],
                [
                    "`h45` is the current active docs-only decision packet",
                    "`h44` is the preserved prior docs-only route packet",
                    "`h43` is the preserved prior useful-case refreeze packet and current",
                    "`r46` is the completed preserved prior post-`h44` exact runtime gate",
                ],
            )
            and contains_all(
                inputs["paper_bundle_status_text"],
                [
                    "`h43` is the current docs-only useful-case refreeze packet",
                    "`p28` aligns publication-facing ledgers to landed `h43`",
                ],
            )
            else "blocked",
            "notes": "The paper-facing ledgers should preserve H43 as the paper endpoint while current internal control moves through H45/R47 above preserved H44/R46.",
        },
        {
            "item_id": "release_review_submission_indexes_and_wave_handoff_preserve_p28_under_p31_h45_current_state",
            "status": "pass"
            if contains_all(
                inputs["release_preflight_text"],
                [
                    "`h45` as the active docs-only decision",
                    "preserved prior `h44` as the route packet",
                    "preserved `h43` as the paper-grade endpoint",
                    "`merge_executed = false`",
                    "`results/h43_post_r44_useful_case_refreeze/summary.json` reports",
                ],
            )
            and contains_all(
                inputs["release_summary_draft_text"],
                [
                    "`h43_post_r44_useful_case_refreeze`",
                    "completed current semantic-boundary gate stack",
                    "no active downstream runtime lane exists after `h43`",
                ],
            )
            and contains_all(
                inputs["release_summary_outline_text"],
                [
                    "`h43` is the current docs-only useful-case refreeze packet",
                    "`merge_executed = false`",
                ],
            )
            and contains_all(
                inputs["review_boundary_text"],
                [
                    "routing/decision state is `h43_post_r44_useful_case_refreeze`",
                    "`h43` refreezes that landed `r44` result",
                    "no active downstream runtime lane exists after `h43`",
                ],
            )
            and contains_all(
                inputs["submission_packet_index_text"],
                [
                    "../milestones/h43_post_r44_useful_case_refreeze/",
                    "../milestones/p28_post_h43_publication_surface_sync/",
                    "the current packet is anchored on `h43` as the current docs-only useful-case refreeze packet",
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
                    "publication/control sync packet aligning paper-facing ledgers to the landed `h43` state",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h43` `p31` blog-guardrail refresh wave",
                    "post-`h43` `p30` manuscript-surface refresh wave",
                    "post-`h43` `p29` release-audit refresh wave",
                    "post-`h43` `p28` publication-surface sync wave",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h45_post_r46_surface_decision_packet` is the current active docs-only",
                    "`h43` remains the current paper-grade endpoint",
                    "`p31_post_h43_blog_guardrails_refresh` is the current low-priority",
                    "`p30` is the completed prior manuscript-surface refresh wave",
                    "`p29` is the completed earlier prior release/public audit refresh wave",
                    "`p28` is the completed earlier publication/control sync wave",
                    "wip/p31-h43-blog-guardrails-refresh",
                ],
            )
            and contains_all(
                inputs["driver_text"],
                [
                    "the current active stage is:",
                    "h45_post_r46_surface_decision_packet",
                    "h43_post_r44_useful_case_refreeze",
                    "r47_origin_restricted_frontend_translation_gate",
                ],
            )
            else "blocked",
            "notes": "Release/review/submission helpers should preserve P28 as completed prior publication sync under current H45/R47 plus P31/P30/P29 state.",
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "p28_post_h43_publication_surface_sync_complete",
        "active_scientific_stage": "h43_post_r44_useful_case_refreeze",
        "sync_packet": "p28_post_h43_publication_surface_sync",
        "sync_scope": "publication_record_follow_on_ledgers",
        "preserved_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "current_completed_retrieval_contract_gate": "r42_origin_append_only_memory_retrieval_contract_gate",
        "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
        "current_completed_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
        "current_completed_coequal_model_gate": "r45_origin_dual_mode_model_mainline_gate",
        "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
        "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
        "merge_executed": False,
        "selected_outcome": "publication_surfaces_synced_to_h43",
        "next_required_lane": "no_active_downstream_runtime_lane",
        "synced_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def build_surface_snapshot_rows() -> list[dict[str, object]]:
    return [
        {
            "surface_id": "publication_readme",
            "path": "docs/publication_record/README.md",
            "role": "paper_first_control_index",
        },
        {
            "surface_id": "claim_evidence_table",
            "path": "docs/publication_record/claim_evidence_table.md",
            "role": "claim_to_artifact_mapping",
        },
        {
            "surface_id": "paper_bundle_status",
            "path": "docs/publication_record/paper_bundle_status.md",
            "role": "paper_facing_bundle_readiness",
        },
        {
            "surface_id": "release_preflight_checklist",
            "path": "docs/publication_record/release_preflight_checklist.md",
            "role": "outward_sync_guard",
        },
        {
            "surface_id": "release_summary_draft",
            "path": "docs/publication_record/release_summary_draft.md",
            "role": "short_public_surface_draft",
        },
        {
            "surface_id": "release_summary_outline",
            "path": "docs/publication_record/release_summary_outline.md",
            "role": "short_public_surface_outline",
        },
        {
            "surface_id": "review_boundary_summary",
            "path": "docs/publication_record/review_boundary_summary.md",
            "role": "reviewer_boundary_packet",
        },
        {
            "surface_id": "submission_packet_index",
            "path": "docs/publication_record/submission_packet_index.md",
            "role": "submission_archive_handoff",
        },
        {
            "surface_id": "experiment_manifest",
            "path": "docs/publication_record/experiment_manifest.md",
            "role": "unattended_batch_ledger",
        },
        {
            "surface_id": "plans_index",
            "path": "docs/plans/README.md",
            "role": "design_navigation_index",
        },
        {
            "surface_id": "milestones_index",
            "path": "docs/milestones/README.md",
            "role": "milestone_navigation_index",
        },
        {
            "surface_id": "active_wave_plan",
            "path": "tmp/active_wave_plan.md",
            "role": "current_wave_handoff",
        },
    ]


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    snapshot_rows = build_surface_snapshot_rows()
    summary = build_summary(checklist_rows, snapshot_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "surface_snapshot.json", {"rows": snapshot_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
