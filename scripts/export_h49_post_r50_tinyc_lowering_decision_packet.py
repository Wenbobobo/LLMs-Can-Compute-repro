"""Export the post-R50 tiny-C lowering decision packet for H49."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H49_post_r50_tinyc_lowering_decision_packet"


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
        "h49_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H49_post_r50_tinyc_lowering_decision_packet" / "README.md"
        ),
        "h49_status_text": read_text(
            ROOT / "docs" / "milestones" / "H49_post_r50_tinyc_lowering_decision_packet" / "status.md"
        ),
        "h49_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H49_post_r50_tinyc_lowering_decision_packet" / "todo.md"
        ),
        "h49_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H49_post_r50_tinyc_lowering_decision_packet" / "acceptance.md"
        ),
        "h49_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H49_post_r50_tinyc_lowering_decision_packet" / "artifact_index.md"
        ),
        "design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-r50-h49-tinyc-lowering-decision-design.md"
        ),
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
        "paper_bundle_status_text": read_text(ROOT / "docs" / "publication_record" / "paper_bundle_status.md"),
        "h48_summary": read_json(ROOT / "results" / "H48_post_r49_numeric_scaling_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "f25_summary": read_json(ROOT / "results" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "summary.json"),
        "r50_summary": read_json(ROOT / "results" / "R50_origin_restricted_tinyc_lowering_gate" / "summary.json"),
        "p35_summary": read_json(ROOT / "results" / "P35_post_h47_research_record_rollup" / "summary.json"),
        "p27_summary": read_json(
            ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"
        ),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h48 = inputs["h48_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    f25 = inputs["f25_summary"]["summary"]
    r50 = inputs["r50_summary"]["summary"]["gate"]
    p35 = inputs["p35_summary"]["summary"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h49_docs_freeze_r50_narrowly_without_scope_widening",
            "status": "pass"
            if contains_all(
                inputs["h49_readme_text"],
                [
                    "completed docs-only tiny-`c` lowering interpretation packet after landed exact `r50`",
                    "`freeze_r50_as_narrow_exact_tinyc_support_only`",
                    "`treat_r50_as_scope_widening_authorization`",
                    "`claim_ceiling = bounded_useful_cases_only`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h49_status_text"],
                [
                    "completed docs-only tiny-`c` lowering interpretation packet after exact `r50`",
                    "preserves `h48` as the preserved prior docs-only packet",
                    "selects `freeze_r50_as_narrow_exact_tinyc_support_only`",
                    "returns the stack to `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h49_todo_text"],
                [
                    "interpret landed `r50` explicitly rather than widening by momentum",
                    "record `r50` as completed evidence rather than an active lane",
                    "restore `no_active_downstream_runtime_lane` after the decision packet",
                    "keep broader wasm/`c`, arbitrary `c`, and multi-function or dynamic-surface growth non-active",
                ],
            )
            and contains_all(
                inputs["h49_acceptance_text"],
                [
                    "`r50` is read as completed evidence rather than as a continuing active lane",
                    "exactly one of the two saved `r50` outcomes is selected",
                    "`h48` remains visible as the preserved prior docs-only packet",
                    "`h43` remains visible as the paper-grade endpoint",
                    "`bounded_useful_cases_only`",
                ],
            )
            and contains_all(
                inputs["h49_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-r50-h49-tinyc-lowering-decision-design.md",
                    "results/r50_origin_restricted_tinyc_lowering_gate/summary.json",
                    "results/h49_post_r50_tinyc_lowering_decision_packet/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h49_post_r50_tinyc_lowering_decision_packet`",
                    "`freeze_r50_as_narrow_exact_tinyc_support_only`",
                    "`treat_r50_as_scope_widening_authorization`",
                    "`next_required_lane = no_active_downstream_runtime_lane`",
                ],
            )
            else "blocked",
            "notes": "H49 must freeze positive R50 evidence narrowly, reject scope widening by momentum, and restore no active downstream runtime lane.",
        },
        {
            "item_id": "upstream_h48_f25_and_r50_support_the_h49_freeze",
            "status": "pass"
            if str(h48["selected_outcome"]) == "authorize_f25_restricted_tinyc_lowering_bundle"
            and str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(f25["only_next_runtime_candidate"]) == "r50_origin_restricted_tinyc_lowering_gate"
            and str(f25["only_followup_packet"]) == "h49_post_r50_tinyc_lowering_decision_packet"
            and str(r50["lane_verdict"]) == "restricted_tinyc_lowering_supported_narrowly"
            and int(r50["planned_variant_count"]) == 8
            and int(r50["executed_variant_count"]) == 8
            and int(r50["exact_variant_count"]) == 8
            and int(r50["exact_kernel_count"]) == 3
            and int(r50["translation_identity_exact_count"]) == 8
            and str(r50["claim_ceiling"]) == "bounded_useful_cases_only"
            and bool(r50["stop_rule_triggered"]) is False
            and str(r50["next_required_packet"]) == "h49_post_r50_tinyc_lowering_decision_packet"
            and str(p35["current_low_priority_wave"]) == "p35_post_h47_research_record_rollup"
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "H49 should freeze R50 narrowly only because H48/F25 explicitly authorized it and the landed gate stayed exact on the admitted narrow surface.",
        },
        {
            "item_id": "shared_control_surfaces_make_h49_current_and_restore_no_active_lane",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h49_post_r50_tinyc_lowering_decision_packet`",
                    "the preserved prior docs-only decision packet is now `h48_post_r49_numeric_scaling_decision_packet`",
                    "`r50_origin_restricted_tinyc_lowering_gate` is now the completed current restricted tiny-`c` lowering gate",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h49_post_r50_tinyc_lowering_decision_packet`, not the preserved prior `h48` packet",
                    "`r50_origin_restricted_tinyc_lowering_gate` is now the completed current restricted tiny-`c` lowering gate",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "the canonical `active_driver` for the current `h49` docs-only tiny-`c` lowering decision packet",
                    "`h49` as the current active docs-only stage",
                    "`h48` as the preserved prior decision packet",
                    "`r50` as the completed current restricted tiny-`c` lowering gate",
                    "`no_active_downstream_runtime_lane` restored by `h49`",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r50-h49-tinyc-lowering-decision-design.md",
                    "2026-03-24-post-f25-r50-restricted-tinyc-lowering-design.md",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h49_post_r50_tinyc_lowering_decision_packet/` — current active docs-only",
                    "h48_post_r49_numeric_scaling_decision_packet/` — preserved prior docs-only",
                    "r50_origin_restricted_tinyc_lowering_gate/` — completed current restricted",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h49 | the post-`r50` useful-case line can freeze exact restricted tiny-`c` support narrowly without authorizing a broader downstream runtime lane",
                    "| d2e | one restricted tiny-`c` lowering surface can target the preserved useful-case kernels exactly",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "`h49` is now complete as the current active docs-only tiny-`c` lowering decision packet",
                    "`r50` is now complete as the current restricted tiny-`c` lowering gate",
                    "`next_required_lane = no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h49_post_r50_tinyc_lowering_decision_packet` is now the current active docs-only",
                    "`h48_post_r49_numeric_scaling_decision_packet` is the preserved prior docs-only decision packet",
                    "`r50_origin_restricted_tinyc_lowering_gate` is now the completed current restricted tiny-`c` lowering gate",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`r50` `h49` tiny-`c` lowering decision wave",
                    "new `scripts/export_h49_post_r50_tinyc_lowering_decision_packet.py`",
                    "new `tests/test_export_h49_post_r50_tinyc_lowering_decision_packet.py`",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should make H49 current, preserve H48 as prior, and show that no downstream runtime lane remains authorized.",
        },
        {
            "item_id": "publication_ledgers_record_h49_as_narrow_closeout",
            "status": "pass"
            if contains_all(
                inputs["claim_evidence_table_text"],
                [
                    "`h49` is now the current active docs-only interpretation packet",
                    "`h48` is the preserved prior docs-only interpretation packet",
                    "`r50` is now the completed current restricted tiny-`c` lowering gate",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["paper_bundle_status_text"],
                [
                    "authoritative control has moved beyond the prose baseline: `h49` is the current active docs-only tiny-`c` lowering decision packet",
                    "`h48` is the preserved prior docs-only decision packet",
                    "`r50` is the completed current restricted tiny-`c` lowering gate",
                    "`h43` remains the paper-grade endpoint",
                    "no active downstream runtime lane exists after `h49`",
                ],
            )
            else "blocked",
            "notes": "Publication ledgers should reflect H49 as narrow closeout control while preserving H43 as the paper-grade endpoint.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H49 lands the required explicit post-R50 docs-only interpretation packet.",
            "H49 freezes R50 as narrow exact tiny-C support only while preserving H43 as the paper-grade endpoint.",
            "H49 restores no active downstream runtime lane after the completed F25 -> R50 path.",
        ],
        "unsupported_here": [
            "H49 does not widen the claim ceiling beyond bounded useful cases.",
            "H49 does not authorize arbitrary C, broader Wasm, or a new downstream runtime lane.",
            "H49 does not replace H43 as the paper-grade endpoint.",
        ],
        "disconfirmed_here": [
            "The idea that positive R50 evidence should automatically authorize broader compiler scope or a new runtime lane without another explicit packet.",
        ],
        "distilled_result": {
            "active_stage": "h49_post_r50_tinyc_lowering_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h48_post_r49_numeric_scaling_decision_packet",
            "preserved_earlier_docs_only_decision_packet": "h47_post_r48_useful_case_bridge_refreeze",
            "current_exact_first_planning_bundle": "f23_post_h47_numeric_scaling_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "freeze_r50_as_narrow_exact_tinyc_support_only",
            "current_completed_numeric_scaling_gate": "r49_origin_useful_case_numeric_scaling_gate",
            "current_completed_post_h48_planning_bundle": "f25_post_h48_restricted_tinyc_lowering_bundle",
            "current_completed_tinyc_lowering_gate": "r50_origin_restricted_tinyc_lowering_gate",
            "current_low_priority_wave": "p35_post_h47_research_record_rollup",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-r50-h49-tinyc-lowering-decision-design.md": (
            "design_text",
            [
                "`freeze_r50_as_narrow_exact_tinyc_support_only`",
                "`treat_r50_as_scope_widening_authorization`",
            ],
        ),
        "docs/milestones/H49_post_r50_tinyc_lowering_decision_packet/README.md": (
            "h49_readme_text",
            [
                "`freeze_r50_as_narrow_exact_tinyc_support_only`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/claims_matrix.md": (
            "claims_matrix_text",
            ["| h49 |", "| d2e |"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`h49` is now complete as the current active docs-only tiny-`c` lowering decision packet",
                "`next_required_lane = no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            [
                "current `h49` docs-only tiny-`c` lowering decision packet",
                "`no_active_downstream_runtime_lane` restored by `h49`",
            ],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            [
                "post-`r50` `h49` tiny-`c` lowering decision wave",
                "export_h49_post_r50_tinyc_lowering_decision_packet.py",
            ],
        ),
        "docs/publication_record/claim_evidence_table.md": (
            "claim_evidence_table_text",
            [
                "`h49` is now the current active docs-only interpretation packet",
                "`r50` is now the completed current restricted tiny-`c` lowering gate",
            ],
        ),
        "docs/publication_record/paper_bundle_status.md": (
            "paper_bundle_status_text",
            [
                "authoritative control has moved beyond the prose baseline: `h49` is the current active docs-only tiny-`c` lowering decision packet",
                "no active downstream runtime lane exists after `h49`",
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
        "active_stage": "h49_post_r50_tinyc_lowering_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h48_post_r49_numeric_scaling_decision_packet",
        "preserved_earlier_docs_only_decision_packet": "h47_post_r48_useful_case_bridge_refreeze",
        "current_exact_first_planning_bundle": "f23_post_h47_numeric_scaling_bundle",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "freeze_r50_as_narrow_exact_tinyc_support_only",
        "current_completed_numeric_scaling_gate": "r49_origin_useful_case_numeric_scaling_gate",
        "current_completed_post_h48_planning_bundle": "f25_post_h48_restricted_tinyc_lowering_bundle",
        "current_completed_tinyc_lowering_gate": "r50_origin_restricted_tinyc_lowering_gate",
        "current_low_priority_wave": "p35_post_h47_research_record_rollup",
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
            "experiment": "h49_post_r50_tinyc_lowering_decision_packet",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
