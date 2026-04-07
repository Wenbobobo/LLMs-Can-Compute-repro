"""Export the post-R49 numeric-scaling decision packet for H48."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H48_post_r49_numeric_scaling_decision_packet"


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
        "h48_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H48_post_r49_numeric_scaling_decision_packet" / "README.md"
        ),
        "h48_status_text": read_text(
            ROOT / "docs" / "milestones" / "H48_post_r49_numeric_scaling_decision_packet" / "status.md"
        ),
        "h48_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H48_post_r49_numeric_scaling_decision_packet" / "todo.md"
        ),
        "h48_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H48_post_r49_numeric_scaling_decision_packet" / "acceptance.md"
        ),
        "h48_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H48_post_r49_numeric_scaling_decision_packet" / "artifact_index.md"
        ),
        "f25_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "README.md"
        ),
        "f25_status_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "status.md"
        ),
        "f25_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "todo.md"
        ),
        "p36_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h48_falsification_closeout_bundle" / "README.md"
        ),
        "design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-r49-h48-numeric-scaling-decision-design.md"
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
        "h47_summary": read_json(ROOT / "results" / "H47_post_r48_useful_case_bridge_refreeze" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "f23_summary": read_json(ROOT / "results" / "F23_post_h47_numeric_scaling_bundle" / "summary.json"),
        "r49_summary": read_json(ROOT / "results" / "R49_origin_useful_case_numeric_scaling_gate" / "summary.json"),
        "r49_stop_rule": read_json(ROOT / "results" / "R49_origin_useful_case_numeric_scaling_gate" / "stop_rule.json"),
        "p35_summary": read_json(ROOT / "results" / "P35_post_h47_research_record_rollup" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h47 = inputs["h47_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    f23 = inputs["f23_summary"]["summary"]
    r49 = inputs["r49_summary"]["summary"]["gate"]
    r49_stop = inputs["r49_stop_rule"]
    p35 = inputs["p35_summary"]["summary"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "h48_docs_select_f25_without_scope_widening",
            "status": "pass"
            if contains_all(
                inputs["h48_readme_text"],
                [
                    "completed docs-only numeric-scaling interpretation packet after landed exact `r49`",
                    "`authorize_f25_restricted_tinyc_lowering_bundle`",
                    "`freeze_post_h47_as_practical_falsifier_for_clean_widening`",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle`",
                    "`p36_post_h48_falsification_closeout_bundle`",
                ],
            )
            and contains_all(
                inputs["h48_status_text"],
                [
                    "completed docs-only numeric-scaling interpretation packet after exact `r49`",
                    "preserves `h47` as the preserved prior docs-only packet",
                    "selects `authorize_f25_restricted_tinyc_lowering_bundle`",
                    "hands the stack to `f25_post_h48_restricted_tinyc_lowering_bundle`",
                ],
            )
            and contains_all(
                inputs["h48_todo_text"],
                [
                    "interpret landed `r49` explicitly rather than widening by momentum",
                    "choose exactly one of the two saved `f23` outcomes",
                    "authorize only a planning bundle, not a new runtime lane",
                    "keep `p36` explicit as the non-selected falsification-closeout route",
                ],
            )
            and contains_all(
                inputs["h48_acceptance_text"],
                [
                    "`r49` is read as completed evidence rather than as a continuing active lane",
                    "exactly one of `f25` or `p36` is selected",
                    "`h47` remains visible as the preserved prior docs-only packet",
                    "`h43` remains visible as the paper-grade endpoint",
                    "`bounded_useful_cases_only`",
                ],
            )
            and contains_all(
                inputs["h48_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-r49-h48-numeric-scaling-decision-design.md",
                    "results/r49_origin_useful_case_numeric_scaling_gate/summary.json",
                    "docs/milestones/f25_post_h48_restricted_tinyc_lowering_bundle/readme.md",
                    "results/h48_post_r49_numeric_scaling_decision_packet/summary.json",
                ],
            )
            and contains_all(
                inputs["f25_readme_text"],
                [
                    "authorized next planning-only bundle after completed `h48`",
                    "`authorize_f25_restricted_tinyc_lowering_bundle`",
                    "`authorized_by_h48_not_yet_executed`",
                ],
            )
            and contains_all(
                inputs["f25_status_text"],
                [
                    "authorized by `h48_post_r49_numeric_scaling_decision_packet`",
                    "planning-only, not yet executed",
                ],
            )
            and contains_all(
                inputs["f25_todo_text"],
                [
                    "save the dedicated `f25` design",
                    "define the smallest admitted restricted tiny-`c` lowering surface",
                ],
            )
            and contains_all(
                inputs["p36_readme_text"],
                [
                    "non-selected downstream closeout bundle",
                    "selected the positive route after `r49`",
                    "`not_selected_by_h48`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`h48_post_r49_numeric_scaling_decision_packet`",
                    "`authorize_f25_restricted_tinyc_lowering_bundle`",
                    "`freeze_post_h47_as_practical_falsifier_for_clean_widening`",
                    "`next_required_lane = f25_post_h48_restricted_tinyc_lowering_bundle`",
                ],
            )
            else "blocked",
            "notes": "H48 should select F25 narrowly, keep P36 explicit but non-selected, and avoid widening scope by momentum.",
        },
        {
            "item_id": "upstream_r49_and_f23_support_the_h48_positive_route",
            "status": "pass"
            if str(h47["selected_outcome"]) == "freeze_r48_as_narrow_comparator_support_only"
            and str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(f23["only_next_runtime_candidate"]) == "r49_origin_useful_case_numeric_scaling_gate"
            and str(f23["next_required_lane"]) == "r49_origin_useful_case_numeric_scaling_gate"
            and str(r49["lane_verdict"]) == "numeric_scaling_survives_through_bucket_c"
            and bool(r49["practical_falsifier_triggered"]) is False
            and len(r49["bucket_a_admitted_float32_recovery_exact_regimes"]) >= 1
            and len(r49["bucket_b_admitted_float32_recovery_exact_regimes"]) >= 1
            and str(r49["next_required_packet"]) == "h48_post_r49_numeric_scaling_decision_packet"
            and bool(r49_stop["stop_rule_triggered"]) is False
            and len(r49_stop["kill_triggers"]) == 0
            and str(p35["current_low_priority_wave"]) == "p35_post_h47_research_record_rollup"
            and bool(p27["merge_executed"]) is False
            else "blocked",
            "notes": "H48 should authorize F25 only if R49 stayed exact, escaped the saved kill criteria, and kept admitted float32 recovery alive on bucket_a and bucket_b.",
        },
        {
            "item_id": "shared_control_surfaces_make_h48_current_and_authorize_f25",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "the current docs-only decision packet is now `h48_post_r49_numeric_scaling_decision_packet`",
                    "the preserved prior docs-only decision packet is now `h47_post_r48_useful_case_bridge_refreeze`",
                    "`r49_origin_useful_case_numeric_scaling_gate` is now the completed current numeric-scaling gate",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle` is now the next authorized planning bundle",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h48_post_r49_numeric_scaling_decision_packet`, not the preserved prior `h47` packet",
                    "`no_active_downstream_runtime_lane`",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle` is now the next authorized planning bundle",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "the canonical `active_driver` for the current `h48` docs-only numeric-scaling decision packet",
                    "`h48` as the current active docs-only stage",
                    "`h47` as the preserved prior decision packet",
                    "`r49` as the completed current numeric-scaling gate",
                    "`f25` as the next authorized planning bundle",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-r49-h48-numeric-scaling-decision-design.md",
                    "2026-03-24-post-h47-r49-useful-case-numeric-scaling-design.md",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "h48_post_r49_numeric_scaling_decision_packet/` — current active docs-only",
                    "h47_post_r48_useful_case_bridge_refreeze/` — preserved prior docs-only",
                    "f25_post_h48_restricted_tinyc_lowering_bundle/",
                    "r49_origin_useful_case_numeric_scaling_gate/",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h48 | the post-`r49` useful-case line can authorize exactly one restricted tiny-`c` lowering planning bundle",
                    "| d2d | the preserved useful-case ladder survives one more narrow numeric-scaling widening",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "`h48` is now complete as the current active docs-only numeric-scaling decision packet",
                    "`r49` is now complete as the current numeric-scaling gate",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle` is now the next authorized planning bundle",
                    "`next_required_lane = f25_post_h48_restricted_tinyc_lowering_bundle`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h48_post_r49_numeric_scaling_decision_packet` is the current active docs-only",
                    "`h47_post_r48_useful_case_bridge_refreeze` is the preserved prior docs-only decision packet",
                    "`r49_origin_useful_case_numeric_scaling_gate` is now the completed current numeric-scaling gate",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle` is now the next authorized planning bundle",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`r49` `h48` numeric-scaling decision wave",
                    "new `scripts/export_h48_post_r49_numeric_scaling_decision_packet.py`",
                    "new `tests/test_export_h48_post_r49_numeric_scaling_decision_packet.py`",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should make H48 current, preserve H47 as prior, and expose F25 as the next authorized planning bundle.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H48 lands the required explicit post-R49 docs-only interpretation packet.",
            "H48 preserves H43 as the paper-grade endpoint while preserving H47 as the prior docs-only packet.",
            "H48 authorizes exactly F25 as the next planning-only bundle after positive R49 evidence.",
        ],
        "unsupported_here": [
            "H48 does not widen the claim ceiling beyond bounded useful cases.",
            "H48 does not itself authorize a broader runtime lane, arbitrary C, or hybrid scope growth.",
            "H48 does not erase P36; it leaves the falsification-closeout route explicit but non-selected.",
        ],
        "disconfirmed_here": [
            "The idea that R49 should force either immediate tiny-C execution or a broad systems claim without an intermediate planning bundle.",
        ],
        "distilled_result": {
            "active_stage": "h48_post_r49_numeric_scaling_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h47_post_r48_useful_case_bridge_refreeze",
            "current_exact_first_planning_bundle": "f23_post_h47_numeric_scaling_bundle",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "authorize_f25_restricted_tinyc_lowering_bundle",
            "current_completed_numeric_scaling_gate": "r49_origin_useful_case_numeric_scaling_gate",
            "authorized_next_planning_bundle": "f25_post_h48_restricted_tinyc_lowering_bundle",
            "non_selected_closeout_bundle": "p36_post_h48_falsification_closeout_bundle",
            "current_low_priority_wave": "p35_post_h47_research_record_rollup",
            "merge_executed": False,
            "later_explicit_packet_required_before_scope_widening": True,
            "next_required_lane": "f25_post_h48_restricted_tinyc_lowering_bundle",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-r49-h48-numeric-scaling-decision-design.md": (
            "design_text",
            ["`authorize_f25_restricted_tinyc_lowering_bundle`", "`freeze_post_h47_as_practical_falsifier_for_clean_widening`"],
        ),
        "docs/milestones/H48_post_r49_numeric_scaling_decision_packet/README.md": (
            "h48_readme_text",
            ["`authorize_f25_restricted_tinyc_lowering_bundle`", "`p36_post_h48_falsification_closeout_bundle`"],
        ),
        "docs/milestones/F25_post_h48_restricted_tinyc_lowering_bundle/README.md": (
            "f25_readme_text",
            ["authorized next planning-only bundle", "`authorized_by_h48_not_yet_executed`"],
        ),
        "docs/milestones/P36_post_h48_falsification_closeout_bundle/README.md": (
            "p36_readme_text",
            ["non-selected downstream closeout bundle", "`not_selected_by_h48`"],
        ),
        "docs/claims_matrix.md": (
            "claims_matrix_text",
            ["| h48 |", "| d2d |"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["`h48` is now complete as the current active docs-only numeric-scaling decision packet", "`f25_post_h48_restricted_tinyc_lowering_bundle`"],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            ["post-`r49` `h48` numeric-scaling decision wave", "export_h48_post_r49_numeric_scaling_decision_packet.py"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "h48_post_r49_numeric_scaling_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h47_post_r48_useful_case_bridge_refreeze",
        "current_exact_first_planning_bundle": "f23_post_h47_numeric_scaling_bundle",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "authorize_f25_restricted_tinyc_lowering_bundle",
        "current_completed_numeric_scaling_gate": "r49_origin_useful_case_numeric_scaling_gate",
        "authorized_next_planning_bundle": "f25_post_h48_restricted_tinyc_lowering_bundle",
        "non_selected_closeout_bundle": "p36_post_h48_falsification_closeout_bundle",
        "current_low_priority_wave": "p35_post_h47_research_record_rollup",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "f25_post_h48_restricted_tinyc_lowering_bundle",
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
            "experiment": "h48_post_r49_numeric_scaling_decision_packet",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
