"""Export the post-R47 frontend-bridge decision packet for H46."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H46_post_r47_frontend_bridge_decision_packet"


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
        "h46_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "README.md"
        ),
        "h46_status_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "status.md"
        ),
        "h46_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "todo.md"
        ),
        "h46_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "acceptance.md"
        ),
        "f22_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "README.md"
        ),
        "f22_status_text": read_text(
            ROOT / "docs" / "milestones" / "F22_post_r46_useful_case_model_bridge_bundle" / "status.md"
        ),
        "r48_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R48_origin_dual_mode_useful_case_model_gate" / "README.md"
        ),
        "r48_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R48_origin_dual_mode_useful_case_model_gate" / "acceptance.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r47-h46-frontend-bridge-decision-design.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h45_summary": read_json(ROOT / "results" / "H45_post_r46_surface_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "r46_summary": read_json(ROOT / "results" / "R46_origin_useful_case_surface_generalization_gate" / "summary.json"),
        "r47_summary": read_json(ROOT / "results" / "R47_origin_restricted_frontend_translation_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h45 = inputs["h45_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    r46 = inputs["r46_summary"]["summary"]["gate"]
    r47 = inputs["r47_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h46_docs_authorize_r48_and_promote_f22",
            "status": "pass"
            if contains_all(
                inputs["h46_readme_text"],
                [
                    "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                    "`freeze_r47_as_frontend_only_and_stop`",
                    "`f22_post_r46_useful_case_model_bridge_bundle` becomes the current comparator-planning bundle",
                    "broader wasm/c or hybrid model work remains non-active",
                ],
            )
            and contains_all(
                inputs["h46_status_text"],
                [
                    "completed docs-only frontend-bridge decision packet after exact `r47`",
                    "preserves `h45` as the preserved prior docs-only decision packet",
                    "authorizes exactly `r48_origin_dual_mode_useful_case_model_gate` as the next comparator-only model candidate",
                    "promotes `f22_post_r46_useful_case_model_bridge_bundle` into the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["h46_todo_text"],
                [
                    "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                    "`freeze_r47_as_frontend_only_and_stop`",
                    "keep `f22` explicit as the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["h46_acceptance_text"],
                [
                    "`h45` remains visible as the preserved prior docs-only decision packet",
                    "`h43` remains visible as the preserved prior useful-case refreeze packet and current paper-grade endpoint",
                    "comparator-only `r48` is named explicitly as the next authorized model lane",
                    "`f22` becomes the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["f22_readme_text"],
                [
                    "current minimal comparator-only planning bundle after positive `r47` and executed `h46`",
                    "after `h46` selected `authorize_r48_origin_dual_mode_useful_case_model_gate`",
                    "does not let model positives replace exact failures",
                ],
            )
            and contains_all(
                inputs["f22_status_text"],
                [
                    "current comparator-only planning bundle after completed `h46`",
                    "supports the now-authorized `r48_origin_dual_mode_useful_case_model_gate`",
                ],
            )
            and contains_all(
                inputs["r48_readme_text"],
                [
                    "authorized next comparator-only model gate after exact `r47` and executed `h46`",
                    "`compiled_weight_executor` and `trainable_2d_executor`",
                    "exact evidence remains decisive",
                    "first-error position plus failure class are mandatory outputs",
                ],
            )
            and contains_all(
                inputs["r48_acceptance_text"],
                [
                    "the gate remains comparator-only rather than substitutive",
                    "exact evidence remains decisive and model positives do not replace exact failures",
                    "first-error position and failure class are mandatory outputs",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h46_post_r47_frontend_bridge_decision_packet`",
                    "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                    "`f22` into the current comparator-planning bundle",
                ],
            )
            else "blocked",
            "notes": "H46 should authorize exactly R48 while turning F22 into the current comparator-planning bundle.",
        },
        {
            "item_id": "upstream_h45_r47_and_h43_support_the_h46_decision",
            "status": "pass"
            if str(h45["selected_outcome"]) == "authorize_r47_origin_restricted_frontend_translation_gate"
            and str(h45["authorized_next_runtime_candidate"]) == "r47_origin_restricted_frontend_translation_gate"
            and str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(r46["lane_verdict"]) == "surface_generalizes_narrowly"
            and int(r46["exact_variant_count"]) == 8
            and int(r46["exact_kernel_count"]) == 3
            and str(r47["lane_verdict"]) == "restricted_frontend_supported_narrowly"
            and int(r47["exact_variant_count"]) == 8
            and int(r47["exact_kernel_count"]) == 3
            and int(r47["translation_identity_exact_count"]) == 8
            and str(r47["next_required_lane"]) == "h46_post_r47_frontend_bridge_decision_packet"
            and str(r47["blocked_future_model_candidate"]) == "r48_origin_dual_mode_useful_case_model_gate"
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "H46 is only justified if H45 authorized R47 and R47 really preserved narrow exact frontend support on the fixed useful-case ladder.",
        },
        {
            "item_id": "shared_control_surfaces_make_h46_current_with_r48_next",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h46_post_r47_frontend_bridge_decision_packet`",
                    "the preserved prior docs-only decision packet is now `h45_post_r46_surface_decision_packet`",
                    "`r48` is now the next required comparator-only model gate",
                    "`f22` is now the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h46_post_r47_frontend_bridge_decision_packet`, not the preserved prior `h45` packet",
                    "`r48_origin_dual_mode_useful_case_model_gate`",
                    "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h46` docs-only frontend-bridge decision packet",
                    "`r48` as the next required comparator-only model gate",
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
                    "f22_post_r46_useful_case_model_bridge_bundle/",
                    "r48_origin_dual_mode_useful_case_model_gate/",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h46 | the post-`r47` useful-case line can authorize exactly one comparator-only model gate",
                    "authorizes exactly `r48`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "h46_post_r47_frontend_bridge_decision_packet",
                    "r48_origin_dual_mode_useful_case_model_gate",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h46_post_r47_frontend_bridge_decision_packet` is the current active docs-only",
                    "`r48_origin_dual_mode_useful_case_model_gate` is now the next required comparator-only model lane",
                    "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`r47` `h46` frontend-bridge decision wave",
                    "new `scripts/export_h46_post_r47_frontend_bridge_decision_packet.py`",
                    "new `results/h46_post_r47_frontend_bridge_decision_packet/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should make H46 current, preserve H45 as prior, and fix R48 as the only authorized next comparator-only model lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H46 lands the required explicit post-R47 docs-only interpretation packet.",
            "H46 preserves H43 as the current paper-grade endpoint while preserving H45 as the prior decision packet.",
            "H46 authorizes exactly R48 and turns F22 into the current comparator-planning bundle.",
        ],
        "unsupported_here": [
            "H46 does not widen the claim ceiling beyond bounded useful cases.",
            "H46 does not authorize arbitrary Wasm/C, broader hybrid model work, or merge-to-main.",
            "H46 does not let model-side comparison outrun or replace exact frontend evidence.",
        ],
        "disconfirmed_here": [
            "The idea that a positive R47 result should automatically widen directly into broader frontend or systems claims by momentum.",
        ],
        "distilled_result": {
            "active_stage": "h46_post_r47_frontend_bridge_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h45_post_r46_surface_decision_packet",
            "preserved_route_reauthorization_packet": "h44_post_h43_route_reauthorization_packet",
            "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "authorize_r48_origin_dual_mode_useful_case_model_gate",
            "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
            "current_completed_exact_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
            "authorized_next_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
            "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "r48_origin_dual_mode_useful_case_model_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-r47-h46-frontend-bridge-decision-design.md": (
            "design_text",
            [
                "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                "`f22` into the current comparator-planning bundle",
            ],
        ),
        "docs/milestones/H46_post_r47_frontend_bridge_decision_packet/README.md": (
            "h46_readme_text",
            [
                "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                "`freeze_r47_as_frontend_only_and_stop`",
            ],
        ),
        "docs/milestones/F22_post_r46_useful_case_model_bridge_bundle/README.md": (
            "f22_readme_text",
            ["current minimal comparator-only planning bundle", "does not let model positives replace exact failures"],
        ),
        "docs/milestones/R48_origin_dual_mode_useful_case_model_gate/README.md": (
            "r48_readme_text",
            ["exact evidence remains decisive", "first-error position plus failure class are mandatory outputs"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["h46_post_r47_frontend_bridge_decision_packet", "r48_origin_dual_mode_useful_case_model_gate"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            [
                "`h46_post_r47_frontend_bridge_decision_packet` is the current active docs-only",
                "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
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
        "active_stage": "h46_post_r47_frontend_bridge_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h45_post_r46_surface_decision_packet",
        "preserved_route_reauthorization_packet": "h44_post_h43_route_reauthorization_packet",
        "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
        "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "authorize_r48_origin_dual_mode_useful_case_model_gate",
        "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
        "current_completed_exact_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
        "authorized_next_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "r48_origin_dual_mode_useful_case_model_gate",
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
            "experiment": "h46_post_r47_frontend_bridge_decision_packet",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
