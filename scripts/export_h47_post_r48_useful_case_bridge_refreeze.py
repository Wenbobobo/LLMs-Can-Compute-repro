"""Export the post-R48 useful-case bridge refreeze packet for H47."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H47_post_r48_useful_case_bridge_refreeze"


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
        "h47_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H47_post_r48_useful_case_bridge_refreeze" / "README.md"
        ),
        "h47_status_text": read_text(
            ROOT / "docs" / "milestones" / "H47_post_r48_useful_case_bridge_refreeze" / "status.md"
        ),
        "h47_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H47_post_r48_useful_case_bridge_refreeze" / "todo.md"
        ),
        "h47_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H47_post_r48_useful_case_bridge_refreeze" / "acceptance.md"
        ),
        "h47_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H47_post_r48_useful_case_bridge_refreeze" / "artifact_index.md"
        ),
        "h46_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "README.md"
        ),
        "h46_status_text": read_text(
            ROOT / "docs" / "milestones" / "H46_post_r47_frontend_bridge_decision_packet" / "status.md"
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
        "r48_status_text": read_text(
            ROOT / "docs" / "milestones" / "R48_origin_dual_mode_useful_case_model_gate" / "status.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-r48-h47-useful-case-bridge-refreeze-design.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "claim_evidence_table_text": read_text(ROOT / "docs" / "publication_record" / "claim_evidence_table.md"),
        "h46_summary": read_json(ROOT / "results" / "H46_post_r47_frontend_bridge_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "r46_summary": read_json(ROOT / "results" / "R46_origin_useful_case_surface_generalization_gate" / "summary.json"),
        "r47_summary": read_json(ROOT / "results" / "R47_origin_restricted_frontend_translation_gate" / "summary.json"),
        "r48_summary": read_json(ROOT / "results" / "R48_origin_dual_mode_useful_case_model_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h46 = inputs["h46_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    r46 = inputs["r46_summary"]["summary"]["gate"]
    r47 = inputs["r47_summary"]["summary"]["gate"]
    r48 = inputs["r48_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h47_docs_refreeze_r48_without_scope_widening",
            "status": "pass"
            if contains_all(
                inputs["h47_readme_text"],
                [
                    "completed docs-only useful-case bridge refreeze packet after landed comparator-only `r48`",
                    "`freeze_r48_as_narrow_comparator_support_only`",
                    "`treat_r48_as_scope_widening_authorization`",
                    "`no_active_downstream_runtime_lane`",
                    "keep exact `r46/r47` evidence decisive",
                ],
            )
            and contains_all(
                inputs["h47_status_text"],
                [
                    "completed docs-only useful-case bridge refreeze packet after comparator-only `r48`",
                    "preserves `h46` as the preserved prior docs-only decision packet",
                    "freezes `r48` as narrow comparator-only useful-case support",
                    "returns the stack to `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h47_todo_text"],
                [
                    "interpret `r48` explicitly rather than widening by momentum",
                    "keep `f21` explicit as the landed exact-first post-`h43` planning bundle",
                    "keep `f22` explicit as the current comparator-planning bundle",
                    "return the stack to `no_active_downstream_runtime_lane`",
                    "keep `p35/f23/f24` low-priority or planning-only",
                ],
            )
            and contains_all(
                inputs["h47_acceptance_text"],
                [
                    "`h46` remains visible as the preserved prior docs-only decision packet",
                    "`h43` remains visible as the current paper-grade endpoint",
                    "`next_required_lane = no_active_downstream_runtime_lane`",
                    "claim ceilings do not move beyond bounded useful cases here",
                ],
            )
            and contains_all(
                inputs["h47_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-r48-h47-useful-case-bridge-refreeze-design.md",
                    "results/h46_post_r47_frontend_bridge_decision_packet/summary.json",
                    "results/r48_origin_dual_mode_useful_case_model_gate/summary.json",
                    "results/h47_post_r48_useful_case_bridge_refreeze/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h47_post_r48_useful_case_bridge_refreeze`",
                    "`freeze_r48_as_narrow_comparator_support_only`",
                    "`no_active_downstream_runtime_lane`",
                    "rejected: momentum-based widening from comparator evidence",
                ],
            )
            else "blocked",
            "notes": "H47 should interpret R48 explicitly, freeze the comparator result narrowly, and restore no active downstream runtime lane.",
        },
        {
            "item_id": "upstream_h46_r48_and_exact_r46_r47_support_the_h47_refreeze",
            "status": "pass"
            if str(h46["selected_outcome"]) == "authorize_r48_origin_dual_mode_useful_case_model_gate"
            and str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(r46["lane_verdict"]) == "surface_generalizes_narrowly"
            and int(r46["exact_variant_count"]) == 8
            and int(r46["exact_kernel_count"]) == 3
            and str(r47["lane_verdict"]) == "restricted_frontend_supported_narrowly"
            and int(r47["exact_variant_count"]) == 8
            and int(r47["exact_kernel_count"]) == 3
            and int(r47["translation_identity_exact_count"]) == 8
            and str(r48["lane_verdict"]) == "useful_case_model_lane_supported_without_replacing_exact"
            and int(r48["exact_mode_count"]) == 2
            and int(r48["contract_variant_count"]) == 8
            and int(r48["contract_kernel_count"]) == 3
            and bool(r48["trainable_heldout_family_exact"])
            and str(r48["next_required_packet"]) == "h47_post_r48_useful_case_bridge_refreeze"
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "H47 is only justified if exact R46/R47 survived and positive R48 remained comparator-only rather than substitutive.",
        },
        {
            "item_id": "shared_control_surfaces_make_h47_current_and_restore_no_active_lane",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h47_post_r48_useful_case_bridge_refreeze`",
                    "the preserved prior docs-only decision packet is now `h46_post_r47_frontend_bridge_decision_packet`",
                    "`r48` remains the completed current comparator-only useful-case model gate",
                    "`f22` remains the current comparator-planning bundle",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h47_post_r48_useful_case_bridge_refreeze`, not the preserved prior `h46` packet",
                    "`r48_origin_dual_mode_useful_case_model_gate`",
                    "`f22_post_r46_useful_case_model_bridge_bundle` is now the current comparator-planning bundle",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h47` docs-only useful-case bridge refreeze packet",
                    "`h46` as the preserved prior docs-only decision packet",
                    "`r48` as the completed current comparator-only useful-case model gate",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r48-h47-useful-case-bridge-refreeze-design.md",
                    "2026-03-24-post-h46-r48-dual-mode-useful-case-model-design.md",
                    "2026-03-24-post-r47-h46-frontend-bridge-decision-design.md",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h47_post_r48_useful_case_bridge_refreeze/` — current active docs-only",
                    "h46_post_r47_frontend_bridge_decision_packet/` — preserved prior docs-only",
                    "f22_post_r46_useful_case_model_bridge_bundle/",
                    "r48_origin_dual_mode_useful_case_model_gate/",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h47 | the post-`r48` useful-case line can refreeze comparator-only support without authorizing a new runtime lane",
                    "freezes `r48` as narrow comparator-only support",
                    "restores `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "h47_post_r48_useful_case_bridge_refreeze",
                    "h46_post_r47_frontend_bridge_decision_packet",
                    "no_active_downstream_runtime_lane",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h47_post_r48_useful_case_bridge_refreeze` is the current active docs-only",
                    "`h46_post_r47_frontend_bridge_decision_packet` is the preserved prior docs-only decision packet",
                    "`r48_origin_dual_mode_useful_case_model_gate` is now the completed current comparator-only useful-case model lane",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`r48` `h47` useful-case bridge refreeze wave",
                    "new `scripts/export_h47_post_r48_useful_case_bridge_refreeze.py`",
                    "new `tests/test_export_h47_post_r48_useful_case_bridge_refreeze.py`",
                    "refreshed `scripts/export_h46_post_r47_frontend_bridge_decision_packet.py`",
                ],
            )
            and contains_all(
                inputs["claim_evidence_table_text"],
                [
                    "`h47` is the current active docs-only interpretation packet",
                    "`h46` is the preserved prior docs-only interpretation packet",
                    "`r48` is now the completed current comparator-only useful-case model gate",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h46_readme_text"],
                [
                    "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                    "`freeze_r47_as_frontend_only_and_stop`",
                ],
            )
            and contains_all(
                inputs["h46_status_text"],
                [
                    "completed docs-only frontend-bridge decision packet after exact `r47`",
                    "authorizes exactly `r48_origin_dual_mode_useful_case_model_gate`",
                ],
            )
            and contains_all(
                inputs["f22_readme_text"],
                [
                    "current minimal comparator-only planning bundle after positive `r47` and executed `h46`",
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
                    "completed current comparator-only model gate under active docs-only `h46`",
                    "useful_case_model_lane_supported_without_replacing_exact",
                ],
            )
            and contains_all(
                inputs["r48_status_text"],
                [
                    "completed current comparator-only model gate under active docs-only `h46`",
                    "h47_post_r48_useful_case_bridge_refreeze",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should make H47 current, preserve H46 as prior, keep R48 completed, and return the scientific lane to no_active_downstream_runtime_lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H47 lands the required explicit post-R48 docs-only refreeze packet.",
            "H47 preserves H43 as the current paper-grade endpoint while preserving H46 as the prior decision packet.",
            "H47 freezes R48 as narrow comparator-only support and restores no_active_downstream_runtime_lane.",
        ],
        "unsupported_here": [
            "H47 does not widen the claim ceiling beyond bounded useful cases.",
            "H47 does not authorize broader Wasm/C, broader hybrid model work, or merge-to-main.",
            "H47 does not let model-side positives replace exact R46/R47 evidence.",
        ],
        "disconfirmed_here": [
            "The idea that a positive R48 comparator result should automatically authorize broader runtime or hybrid growth by momentum.",
        ],
        "distilled_result": {
            "active_stage": "h47_post_r48_useful_case_bridge_refreeze",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h46_post_r47_frontend_bridge_decision_packet",
            "preserved_route_reauthorization_packet": "h44_post_h43_route_reauthorization_packet",
            "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "freeze_r48_as_narrow_comparator_support_only",
            "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
            "current_completed_exact_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
            "current_completed_comparator_only_useful_case_model_gate": "r48_origin_dual_mode_useful_case_model_gate",
            "claim_d_state": "supported_here_narrowly",
            "claim_ceiling": "bounded_useful_cases_only",
            "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
            "authorized_next_runtime_candidate": "none",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "explicit_merge_packet": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-r48-h47-useful-case-bridge-refreeze-design.md": (
            "design_text",
            [
                "`freeze_r48_as_narrow_comparator_support_only`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/milestones/H47_post_r48_useful_case_bridge_refreeze/README.md": (
            "h47_readme_text",
            [
                "`freeze_r48_as_narrow_comparator_support_only`",
                "`treat_r48_as_scope_widening_authorization`",
            ],
        ),
        "docs/milestones/H46_post_r47_frontend_bridge_decision_packet/README.md": (
            "h46_readme_text",
            [
                "`authorize_r48_origin_dual_mode_useful_case_model_gate`",
                "`freeze_r47_as_frontend_only_and_stop`",
            ],
        ),
        "docs/milestones/R48_origin_dual_mode_useful_case_model_gate/README.md": (
            "r48_readme_text",
            [
                "useful_case_model_lane_supported_without_replacing_exact",
                "histogram16_u8",
            ],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "h47_post_r48_useful_case_bridge_refreeze",
                "h46_post_r47_frontend_bridge_decision_packet",
                "no_active_downstream_runtime_lane",
            ],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            [
                "`h47_post_r48_useful_case_bridge_refreeze` is the current active docs-only",
                "`h46_post_r47_frontend_bridge_decision_packet` is the preserved prior docs-only decision packet",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/publication_record/claim_evidence_table.md": (
            "claim_evidence_table_text",
            [
                "`h47` is the current active docs-only interpretation packet",
                "`r48` is now the completed current comparator-only useful-case model gate",
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
        "active_stage": "h47_post_r48_useful_case_bridge_refreeze",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h46_post_r47_frontend_bridge_decision_packet",
        "preserved_route_reauthorization_packet": "h44_post_h43_route_reauthorization_packet",
        "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
        "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "freeze_r48_as_narrow_comparator_support_only",
        "current_completed_post_h44_exact_runtime_gate": "r46_origin_useful_case_surface_generalization_gate",
        "current_completed_exact_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
        "current_completed_comparator_only_useful_case_model_gate": "r48_origin_dual_mode_useful_case_model_gate",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "no_active_downstream_runtime_lane",
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
            "experiment": "h47_post_r48_useful_case_bridge_refreeze",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
