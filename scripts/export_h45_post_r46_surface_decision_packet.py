"""Export the post-R46 surface decision packet for H45."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H45_post_r46_surface_decision_packet"


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
        "h45_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H45_post_r46_surface_decision_packet" / "README.md"
        ),
        "h45_status_text": read_text(
            ROOT / "docs" / "milestones" / "H45_post_r46_surface_decision_packet" / "status.md"
        ),
        "h45_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H45_post_r46_surface_decision_packet" / "todo.md"
        ),
        "h45_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H45_post_r46_surface_decision_packet" / "acceptance.md"
        ),
        "h45_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H45_post_r46_surface_decision_packet" / "artifact_index.md"
        ),
        "h46_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "README.md"
        ),
        "f22_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "README.md"
        ),
        "f22_status_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "status.md"
        ),
        "f22_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "todo.md"
        ),
        "f22_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "acceptance.md"
        ),
        "f22_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "artifact_index.md"
        ),
        "r47_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R47_origin_restricted_frontend_translation_gate" / "README.md"
        ),
        "r47_status_text": read_text(
            ROOT / "docs" / "milestones" / "R47_origin_restricted_frontend_translation_gate" / "status.md"
        ),
        "r47_todo_text": read_text(
            ROOT / "docs" / "milestones" / "R47_origin_restricted_frontend_translation_gate" / "todo.md"
        ),
        "r47_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R47_origin_restricted_frontend_translation_gate" / "acceptance.md"
        ),
        "r47_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "R47_origin_restricted_frontend_translation_gate" / "artifact_index.md"
        ),
        "h47_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H47_post_r48_useful_case_bridge_refreeze" / "README.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r46-h45-surface-decision-design.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h44_summary": read_json(ROOT / "results" / "H44_post_h43_route_reauthorization_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "f21_summary": read_json(ROOT / "results" / "F21_post_h43_exact_useful_case_expansion_bundle" / "summary.json"),
        "r46_summary": read_json(ROOT / "results" / "R46_origin_useful_case_surface_generalization_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h44 = inputs["h44_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    f21 = inputs["f21_summary"]["summary"]
    r46 = inputs["r46_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h45_docs_authorize_r47_and_keep_later_scope_explicit",
            "status": "pass"
            if contains_all(
                inputs["h45_readme_text"],
                [
                    "`authorize_r47_origin_restricted_frontend_translation_gate`",
                    "`freeze_r46_as_mixed_inside_surface_and_stop`",
                    "`freeze_r46_as_fixed_suite_only_and_stop`",
                    "`f22_post_r46_useful_case_model_bridge_bundle`",
                    "`r48` remains conditional on later exact frontend evidence plus `h46`",
                ],
            )
            and contains_all(
                inputs["h45_status_text"],
                [
                    "completed docs-only surface decision packet after exact `r46`",
                    "authorizes exactly `r47_origin_restricted_frontend_translation_gate`",
                    "saves `f22_post_r46_useful_case_model_bridge_bundle` only as a blocked future comparator bundle",
                ],
            )
            and contains_all(
                inputs["h45_todo_text"],
                [
                    "`authorize_r47_origin_restricted_frontend_translation_gate`",
                    "`freeze_r46_as_mixed_inside_surface_and_stop`",
                    "`freeze_r46_as_fixed_suite_only_and_stop`",
                    "keep `f22` explicit as a saved but blocked future comparator bundle",
                ],
            )
            and contains_all(
                inputs["h45_acceptance_text"],
                [
                    "`h44` remains visible as the preserved prior docs-only route packet",
                    "`h43` remains visible as the preserved prior useful-case refreeze packet and current paper-grade endpoint",
                    "exact `r47` is named explicitly as the next exact runtime gate",
                    "`f22` remains a saved but blocked future comparator bundle and `r48` remains conditional",
                ],
            )
            and contains_all(
                inputs["r47_readme_text"],
                [
                    "completed exact frontend bridge gate authorized by landed `h45`",
                    "not a new runtime stack",
                    "instruction-identically onto the existing useful-case bytecode kernels",
                ],
            )
            and contains_all(
                inputs["r47_acceptance_text"],
                [
                    "the gate remains exact-first rather than demo-first",
                    "the bridge reuses the existing useful-case bytecode kernels and exactness contract",
                    "no heap, no alias-heavy pointers, no recursion, no float, no io, and no hidden mutable state",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h45_post_r46_surface_decision_packet`",
                    "`authorize_r47_origin_restricted_frontend_translation_gate`",
                    "`f22_post_r46_useful_case_model_bridge_bundle` is saved only as a blocked future comparator bundle",
                ],
            )
            else "blocked",
            "notes": "H45 should select exactly R47 while keeping any later model-side widening explicit rather than automatic.",
        },
        {
            "item_id": "upstream_h44_r46_and_h43_support_the_h45_decision",
            "status": "pass"
            if str(h44["selected_outcome"]) == "authorize_r46_origin_useful_case_surface_generalization_gate"
            and str(h44["authorized_next_runtime_candidate"]) == "r46_origin_useful_case_surface_generalization_gate"
            and str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(f21["first_admissible_next_runtime_candidate"]) == "r46_origin_useful_case_surface_generalization_gate"
            and str(r46["lane_verdict"]) == "surface_generalizes_narrowly"
            and int(r46["exact_variant_count"]) == 8
            and int(r46["exact_kernel_count"]) == 3
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "H45 is only justified if H44 authorized R46 and R46 really preserved narrow exact useful-case surface generalization.",
        },
        {
            "item_id": "shared_control_surfaces_preserve_h45_after_r48",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h46_post_r47_frontend_bridge_decision_packet`",
                    "the preserved prior docs-only decision packet is now `h45_post_r46_surface_decision_packet`",
                    "`r48` is now the completed current comparator-only useful-case model gate",
                    "`h47_post_r48_useful_case_bridge_refreeze` is now the next required docs-only refreeze packet",
                    "`f22` is now the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h46_post_r47_frontend_bridge_decision_packet`, not the preserved prior `h45` packet",
                    "`r47_origin_restricted_frontend_translation_gate`",
                    "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h46` docs-only frontend-bridge decision packet",
                    "`r48` as the completed current comparator-only useful-case model gate",
                    "`h47` as the next required docs-only useful-case bridge refreeze packet",
                    "`f22` as the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r47-h46-frontend-bridge-decision-design.md",
                    "2026-03-24-post-r46-h45-surface-decision-design.md",
                    "2026-03-24-post-h45-r47-restricted-frontend-translation-design.md",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h46_post_r47_frontend_bridge_decision_packet/",
                    "h45_post_r46_surface_decision_packet/",
                    "f22_post_r46_useful_case_model_bridge_bundle/",
                    "r48_origin_dual_mode_useful_case_model_gate/",
                    "h47_post_r48_useful_case_bridge_refreeze/",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h45 | the post-`r46` useful-case line can authorize exactly one restricted frontend bridge",
                    "authorizes exactly `r47`",
                    "keeps `r48` conditional behind later `h46`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "h46_post_r47_frontend_bridge_decision_packet",
                    "r47_origin_restricted_frontend_translation_gate",
                    "h47_post_r48_useful_case_bridge_refreeze",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h46_post_r47_frontend_bridge_decision_packet` is the current active docs-only",
                    "`r47_origin_restricted_frontend_translation_gate` is now the completed current exact frontend bridge lane",
                    "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
                    "`h47_post_r48_useful_case_bridge_refreeze` is now the next required docs-only refreeze packet",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h46` `r48` dual-mode useful-case model wave",
                    "post-`r47` `h46` frontend-bridge decision wave",
                    "refreshed `scripts/export_h45_post_r46_surface_decision_packet.py`",
                    "refreshed `results/h45_post_r46_surface_decision_packet/*`",
                ],
            )
            and contains_all(
                inputs["h47_readme_text"],
                [
                    "planned next docs-only refreeze packet after landed comparator-only `r48`",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should preserve H45 as the prior decision packet after H46 stays active, R48 lands, and H47 becomes next.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H45 lands the required explicit post-R46 docs-only interpretation packet.",
            "H45 preserves H43 as the current paper-grade endpoint while preserving H44 as the prior route packet.",
            "H45 authorizes exactly R47 and keeps F22/R48 blocked behind later explicit packets.",
        ],
        "unsupported_here": [
            "H45 does not widen the claim ceiling beyond bounded useful cases.",
            "H45 does not authorize arbitrary Wasm/C, hybrid model work, or merge-to-main.",
            "H45 does not let model-side comparison outrun exact frontend evidence.",
        ],
        "disconfirmed_here": [
            "The idea that a positive R46 result should automatically widen directly into broader frontend or model work by momentum.",
        ],
        "distilled_result": {
            "active_stage": "h45_post_r46_surface_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h44_post_h43_route_reauthorization_packet",
            "current_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "authorize_r47_origin_restricted_frontend_translation_gate",
            "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
            "authorized_next_runtime_candidate": "r47_origin_restricted_frontend_translation_gate",
            "blocked_future_comparator_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
            "deferred_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
            "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "r47_origin_restricted_frontend_translation_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-r46-h45-surface-decision-design.md": (
            "design_text",
            [
                "`authorize_r47_origin_restricted_frontend_translation_gate`",
                "`f22_post_r46_useful_case_model_bridge_bundle`",
            ],
        ),
        "docs/milestones/H45_post_r46_surface_decision_packet/README.md": (
            "h45_readme_text",
            [
                "`authorize_r47_origin_restricted_frontend_translation_gate`",
                "`freeze_r46_as_mixed_inside_surface_and_stop`",
            ],
        ),
        "docs/milestones/H46_post_r47_frontend_bridge_decision_packet/README.md": (
            "h46_readme_text",
            ["`authorize_r48_origin_dual_mode_useful_case_model_gate`", "`freeze_r47_as_frontend_only_and_stop`"],
        ),
        "docs/milestones/R47_origin_restricted_frontend_translation_gate/README.md": (
            "r47_readme_text",
            ["not a new runtime stack", "existing `r44/r46` exactness pipeline"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "h46_post_r47_frontend_bridge_decision_packet",
                "r47_origin_restricted_frontend_translation_gate",
                "h47_post_r48_useful_case_bridge_refreeze",
            ],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            [
                "`h46_post_r47_frontend_bridge_decision_packet` is the current active docs-only",
                "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
                "`h47_post_r48_useful_case_bridge_refreeze` is now the next required docs-only refreeze packet",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "h45_post_r46_surface_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h44_post_h43_route_reauthorization_packet",
        "current_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "authorize_r47_origin_restricted_frontend_translation_gate",
        "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
        "authorized_next_runtime_candidate": "r47_origin_restricted_frontend_translation_gate",
        "blocked_future_comparator_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
        "deferred_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "r47_origin_restricted_frontend_translation_gate",
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
            "experiment": "h45_post_r46_surface_decision_packet",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
