"""Export the post-H43 route reauthorization packet for H44."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H44_post_h43_route_reauthorization_packet"


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
        "h44_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H44_post_h43_route_reauthorization_packet" / "README.md"
        ),
        "h44_status_text": read_text(
            ROOT / "docs" / "milestones" / "H44_post_h43_route_reauthorization_packet" / "status.md"
        ),
        "h44_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H44_post_h43_route_reauthorization_packet" / "todo.md"
        ),
        "h44_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H44_post_h43_route_reauthorization_packet" / "acceptance.md"
        ),
        "h44_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H44_post_h43_route_reauthorization_packet" / "artifact_index.md"
        ),
        "master_plan_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-mainline-reentry-master-plan.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "f21_summary": read_json(ROOT / "results" / "F21_post_h43_exact_useful_case_expansion_bundle" / "summary.json"),
        "r43_summary": read_json(ROOT / "results" / "R43_origin_bounded_memory_small_vm_execution_gate" / "summary.json"),
        "r44_summary": read_json(ROOT / "results" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "summary.json"),
        "r45_summary": read_json(ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h43 = inputs["h43_summary"]["summary"]
    f21 = inputs["f21_summary"]["summary"]
    r43 = inputs["r43_summary"]["summary"]["gate"]
    r44 = inputs["r44_summary"]["summary"]["gate"]
    r45 = inputs["r45_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h44_docs_reauthorize_r46_while_preserving_h43_paper_grade_endpoint",
            "status": "pass"
            if contains_all(
                inputs["h44_readme_text"],
                [
                    "executed docs-only route reauthorization packet after the preserved prior",
                    "`authorize_r46_origin_useful_case_surface_generalization_gate`",
                    "`hold_at_h43_and_continue_planning_only`",
                    "`r46_origin_useful_case_surface_generalization_gate`",
                    "`r47_origin_restricted_frontend_translation_gate`",
                    "`r48_origin_dual_mode_useful_case_model_gate`",
                ],
            )
            and contains_all(
                inputs["h44_status_text"],
                [
                    "completed docs-only route reauthorization packet after `h43`",
                    "preserves `h43` as the preserved prior useful-case refreeze packet and current paper-grade endpoint",
                    "incorporates `f21` as the current exact-first post-`h43` planning bundle",
                    "authorizes exactly `r46_origin_useful_case_surface_generalization_gate`",
                ],
            )
            and contains_all(
                inputs["h44_todo_text"],
                [
                    "`authorize_r46_origin_useful_case_surface_generalization_gate`",
                    "`hold_at_h43_and_continue_planning_only`",
                    "keep `f21` explicit as the bundle fixing the exact-first post-`h43` route",
                    "keep `r47`, `r48`, `r41`, `f11`, `r29`, and `f3` non-active here",
                ],
            )
            and contains_all(
                inputs["h44_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h43` remains visible as the preserved prior useful-case refreeze packet and current paper-grade endpoint",
                    "exact `r46` is named explicitly as the next exact runtime gate",
                    "`r47` and `r48` remain deferred until later exact-positive packets survive",
                ],
            )
            and contains_all(
                inputs["h44_artifact_index_text"],
                [
                    "docs/milestones/f21_post_h43_exact_useful_case_expansion_bundle/readme.md",
                    "results/f21_post_h43_exact_useful_case_expansion_bundle/summary.json",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                ],
            )
            and contains_all(
                inputs["master_plan_text"],
                [
                    "wave 2: `h44_post_h43_route_reauthorization_packet`",
                    "`authorize_r46_origin_useful_case_surface_generalization_gate`",
                    "`current_paper_grade_endpoint = h43_post_r44_useful_case_refreeze`",
                    "`later_explicit_packet_required_before_scope_widening = true`",
                ],
            )
            else "blocked",
            "notes": "H44 should reauthorize R46 explicitly while preserving H43 as the bounded paper-grade endpoint.",
        },
        {
            "item_id": "h43_exact_state_and_f21_bundle_justify_the_reauthorization",
            "status": "pass"
            if str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["current_completed_useful_case_gate"]) == "r44_origin_restricted_wasm_useful_case_execution_gate"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(h43["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(f21["selected_outcome"]) == "exact_first_post_h43_reentry_bundle_saved"
            and str(f21["first_admissible_next_runtime_candidate"]) == "r46_origin_useful_case_surface_generalization_gate"
            and str(r43["lane_verdict"]) == "keep_semantic_boundary_route"
            and str(r44["lane_verdict"]) == "useful_case_surface_supported_narrowly"
            and str(r45["lane_verdict"]) == "coequal_model_lane_supported_without_replacing_exact"
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "H44 is only justified if H43 preserved a real bounded useful-case result and F21 fixed the exact-first route above it.",
        },
        {
            "item_id": "shared_control_surfaces_record_h45_current_while_preserving_h44_as_prior_route_packet",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h45_post_r46_surface_decision_packet`",
                    "the preserved prior docs-only decision packet is now `h44_post_h43_route_reauthorization_packet`",
                    "the current exact post-`h43` planning bundle is `f21_post_h43_exact_useful_case_expansion_bundle`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current active docs-only decision packet is",
                    "`h45_post_r46_surface_decision_packet`",
                    "`h44_post_h43_route_reauthorization_packet` is now complete as the",
                    "`f21_post_h43_exact_useful_case_expansion_bundle` is now complete",
                    "`p31_post_h43_blog_guardrails_refresh` remains the current low-priority",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "current `h45` docs-only surface-decision packet",
                    "docs/plans/2026-03-24-post-h43-mainline-reentry-master-plan.md",
                    "docs/plans/2026-03-24-post-r46-h45-surface-decision-design.md",
                    "docs/milestones/f21_post_h43_exact_useful_case_expansion_bundle/",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h43-mainline-reentry-master-plan.md",
                    "2026-03-24-post-r46-h45-surface-decision-design.md",
                    "../milestones/f21_post_h43_exact_useful_case_expansion_bundle/",
                    "../milestones/h44_post_h43_route_reauthorization_packet/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h45_post_r46_surface_decision_packet/",
                    "h44_post_h43_route_reauthorization_packet/",
                    "f21_post_h43_exact_useful_case_expansion_bundle/",
                    "p31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| f21 | the post-`h43` useful-case line can continue only through an exact-first planning bundle",
                    "| h44 | the post-`h43` stack can reauthorize exactly `r46` without widening the paper-grade endpoint or merge posture",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "h45_post_r46_surface_decision_packet",
                    "the current exact post-`h43` planning bundle is:",
                    "f21_post_h43_exact_useful_case_expansion_bundle",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h45_post_r46_surface_decision_packet` is the current active docs-only",
                    "`h44_post_h43_route_reauthorization_packet`",
                    "`f21_post_h43_exact_useful_case_expansion_bundle` is the current planning bundle",
                    "`p31_post_h43_blog_guardrails_refresh` is the current low-priority",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h43` `f21/h44` mainline-reentry wave",
                    "results/f21_post_h43_exact_useful_case_expansion_bundle/summary.json",
                    "results/h44_post_h43_route_reauthorization_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should make H45 current while preserving H44 as the prior route packet, preserving H43, indexing F21, and keeping P31 current as the low-priority docs wave.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H44 lands the required later explicit post-H43 docs-only route packet.",
            "H44 preserves H43 as the preserved prior useful-case refreeze packet and current paper-grade endpoint.",
            "H44 authorizes exactly R46 as the next exact runtime candidate while keeping R47/R48 deferred.",
        ],
        "unsupported_here": [
            "H44 does not widen the claim ceiling beyond bounded useful cases.",
            "H44 does not authorize broader Wasm/C, hybrid work, or merge-to-main.",
            "H44 does not let model work outrun exact evidence.",
        ],
        "disconfirmed_here": [
            "The idea that the repo should stay in no-active-downstream-runtime posture once an explicit post-H43 reauthorization packet has landed.",
        ],
        "distilled_result": {
            "active_stage": "h44_post_h43_route_reauthorization_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h43_post_r44_useful_case_refreeze",
            "current_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "authorize_r46_origin_useful_case_surface_generalization_gate",
            "non_selected_outcome": "hold_at_h43_and_continue_planning_only",
            "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
            "current_completed_useful_case_gate": "r44_origin_restricted_wasm_useful_case_execution_gate",
            "current_completed_coequal_model_gate": "r45_origin_dual_mode_model_mainline_gate",
            "authorized_next_runtime_candidate": "r46_origin_useful_case_surface_generalization_gate",
            "deferred_future_runtime_candidate": "r47_origin_restricted_frontend_translation_gate",
            "deferred_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
            "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "r46_origin_useful_case_surface_generalization_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h43-mainline-reentry-master-plan.md": (
            "master_plan_text",
            ["`h44_post_h43_route_reauthorization_packet`", "`r46_origin_useful_case_surface_generalization_gate`"],
        ),
        "docs/milestones/H44_post_h43_route_reauthorization_packet/README.md": (
            "h44_readme_text",
            ["`authorize_r46_origin_useful_case_surface_generalization_gate`", "`r48_origin_dual_mode_useful_case_model_gate`"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["h44_post_h43_route_reauthorization_packet", "f21_post_h43_exact_useful_case_expansion_bundle"],
        ),
        "STATUS.md": (
            "status_text",
            ["`H44_post_h43_route_reauthorization_packet`", "`F21_post_h43_exact_useful_case_expansion_bundle`"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`H44_post_h43_route_reauthorization_packet` is the current active docs-only packet", "`P31_post_h43_blog_guardrails_refresh` is the current low-priority"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "h44_post_h43_route_reauthorization_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h43_post_r44_useful_case_refreeze",
        "current_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "authorize_r46_origin_useful_case_surface_generalization_gate",
        "authorized_next_runtime_candidate": "r46_origin_useful_case_surface_generalization_gate",
        "deferred_future_runtime_candidate": "r47_origin_restricted_frontend_translation_gate",
        "deferred_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "r46_origin_useful_case_surface_generalization_gate",
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, snapshot_rows)

    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h44_post_h43_route_reauthorization_packet",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
