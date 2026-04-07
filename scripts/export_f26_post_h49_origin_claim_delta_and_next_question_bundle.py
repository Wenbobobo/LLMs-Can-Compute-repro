"""Export the post-H49 claim-delta and next-question bundle for F26."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F26_post_h49_origin_claim_delta_and_next_question_bundle"


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
    except Exception as exc:  # pragma: no cover
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
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h49-origin-core-next-wave-design.md"),
        "f26_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "README.md"
        ),
        "f26_status_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "status.md"
        ),
        "f26_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "todo.md"
        ),
        "f26_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "acceptance.md"
        ),
        "f26_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "artifact_index.md"
        ),
        "claim_delta_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "claim_delta_matrix.md"
        ),
        "next_question_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "next_question.md"
        ),
        "route_constraints_text": read_text(
            ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "route_constraints.md"
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
        "h49_summary": read_json(ROOT / "results" / "H49_post_r50_tinyc_lowering_decision_packet" / "summary.json"),
        "r50_summary": read_json(ROOT / "results" / "R50_origin_restricted_tinyc_lowering_gate" / "summary.json"),
        "p35_summary": read_json(ROOT / "results" / "P35_post_h47_research_record_rollup" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h49 = inputs["h49_summary"]["summary"]
    r50 = inputs["r50_summary"]["summary"]["gate"]
    p35 = inputs["p35_summary"]["summary"]
    return [
        {
            "item_id": "f26_docs_define_post_h49_claim_delta_bundle",
            "status": "pass"
            if contains_all(
                inputs["design_text"],
                [
                    "`f26_post_h49_origin_claim_delta_and_next_question_bundle`",
                    "`r51_origin_memory_control_surface_sufficiency_gate`",
                    "`r52_origin_internal_vs_external_executor_value_gate`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                ],
            )
            and contains_all(inputs["f26_readme_text"], ["completed planning-only bundle", "`h49`", "`h43`", "`r51_origin_memory_control_surface_sufficiency_gate`"])
            and contains_all(inputs["claim_delta_matrix_text"], ["| `a` |", "| `d` |", "`r51`", "`r52`"])
            and contains_all(inputs["next_question_text"], ["substrate survive a materially richer memory/control surface", "`r52_origin_internal_vs_external_executor_value_gate`"])
            and contains_all(inputs["route_constraints_text"], ["`r51` is the only next runtime candidate fixed here", "`f27` is saved as planning-only"])
            else "blocked",
            "notes": "F26 should save a planning-only post-H49 claim-delta bundle that fixes exactly R51, R52, and H50.",
        },
        {
            "item_id": "upstream_h49_and_r50_support_substrate_first_requestioning",
            "status": "pass"
            if str(h49["active_stage"]) == "h49_post_r50_tinyc_lowering_decision_packet"
            and str(h49["selected_outcome"]) == "freeze_r50_as_narrow_exact_tinyc_support_only"
            and str(h49["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(r50["lane_verdict"]) == "restricted_tinyc_lowering_supported_narrowly"
            and str(r50["claim_ceiling"]) == "bounded_useful_cases_only"
            and str(p35["current_low_priority_wave"]) == "p35_post_h47_research_record_rollup"
            else "blocked",
            "notes": "F26 should start from H49's narrow freeze, not from an assumed post-R50 widening authorization.",
        },
        {
            "item_id": "shared_control_surfaces_make_f26_current_planning_bundle",
            "status": "pass"
            if contains_all(inputs["readme_text"], ["`f26_post_h49_origin_claim_delta_and_next_question_bundle` is now the current post-`h49` planning bundle", "`p36_post_h49_cleanline_hygiene_and_artifact_policy` is now the current low-priority", "`r51_origin_memory_control_surface_sufficiency_gate` as the only next runtime candidate"])
            and contains_all(inputs["status_text"], ["`f26_post_h49_origin_claim_delta_and_next_question_bundle` is now the current post-`h49` planning bundle", "`p36_post_h49_cleanline_hygiene_and_artifact_policy` is now the current low-priority", "`r51_origin_memory_control_surface_sufficiency_gate` as the only next runtime candidate"])
            and contains_all(inputs["publication_readme_text"], ["`f26` as the current post-`h49` planning bundle", "`p36` as the current low-priority operational/docs wave", "`r51` as the only next runtime candidate"])
            and contains_all(inputs["plans_index_text"], ["2026-03-24-post-h49-origin-core-next-wave-design.md", "../milestones/f26_post_h49_origin_claim_delta_and_next_question_bundle/"])
            and contains_all(inputs["milestones_index_text"], ["f26_post_h49_origin_claim_delta_and_next_question_bundle/", "p36_post_h49_cleanline_hygiene_and_artifact_policy/"])
            and contains_all(inputs["claims_matrix_text"], ["| f26 | the post-`h49` origin-core line can continue only through one planning-only claim-delta bundle"])
            and contains_all(inputs["current_stage_driver_text"], ["the current post-`h49` planning bundle is:", "- `f26_post_h49_origin_claim_delta_and_next_question_bundle`", "the current low-priority operational/docs wave is:", "- `p36_post_h49_cleanline_hygiene_and_artifact_policy`"])
            and contains_all(inputs["active_wave_plan_text"], ["`f26_post_h49_origin_claim_delta_and_next_question_bundle` is now the current post-`h49` planning bundle", "`r51_origin_memory_control_surface_sufficiency_gate` is the only next runtime candidate", "`p36_post_h49_cleanline_hygiene_and_artifact_policy` is the current low-priority"])
            and contains_all(inputs["experiment_manifest_text"], ["post-`h49` `f26/p36` next-wave planning and hygiene wave", "new `docs/plans/2026-03-24-post-h49-origin-core-next-wave-design.md`", "new `results/f26_post_h49_origin_claim_delta_and_next_question_bundle/summary.json`", "new `results/p36_post_h49_cleanline_hygiene_and_artifact_policy/summary.json`"])
            else "blocked",
            "notes": "Shared control surfaces should make F26 current while preserving H49 as the active docs-only packet.",
        },
    ]


def build_summary(inputs: dict[str, Any], checklist_rows: list[dict[str, object]]) -> dict[str, Any]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    pass_count = sum(1 for row in checklist_rows if row["status"] == "pass")
    return {
        "experiment": "f26_post_h49_origin_claim_delta_and_next_question_bundle",
        "environment": environment_payload(),
        "summary": {
            "active_stage": "f26_post_h49_origin_claim_delta_and_next_question_bundle",
            "current_active_docs_only_stage": "h49_post_r50_tinyc_lowering_decision_packet",
            "preserved_prior_docs_only_stage": "h48_post_r49_numeric_scaling_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_routing_refreeze_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_completed_tinyc_lowering_gate": "r50_origin_restricted_tinyc_lowering_gate",
            "preserved_prior_low_priority_wave": "p35_post_h47_research_record_rollup",
            "current_low_priority_wave": "p36_post_h49_cleanline_hygiene_and_artifact_policy",
            "selected_outcome": "post_h49_claim_delta_bundle_saved",
            "only_next_runtime_candidate": "r51_origin_memory_control_surface_sufficiency_gate",
            "only_followup_comparator_gate": "r52_origin_internal_vs_external_executor_value_gate",
            "only_followup_packet": "h50_post_r51_r52_scope_decision_packet",
            "saved_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "snapshot_surface_count": 8,
            "check_count": len(checklist_rows),
            "pass_count": pass_count,
            "blocked_count": len(blocked_items),
            "blocked_items": blocked_items,
            "next_required_lane": "r51_origin_memory_control_surface_sufficiency_gate",
        },
    }


def build_claim_packet(summary_payload: dict[str, Any]) -> dict[str, Any]:
    distilled = summary_payload["summary"]
    keys = [
        "active_stage",
        "current_active_docs_only_stage",
        "current_paper_grade_endpoint",
        "current_routing_refreeze_stage",
        "current_completed_tinyc_lowering_gate",
        "current_low_priority_wave",
        "selected_outcome",
        "only_next_runtime_candidate",
        "only_followup_comparator_gate",
        "only_followup_packet",
        "saved_future_bundle",
        "next_required_lane",
    ]
    return {
        "summary": {
            "supported_here": [
                "F26 saves the post-H49 claim-delta reading without widening the active scientific stage.",
                "F26 fixes exactly R51 as the next runtime candidate, R52 as the only later comparator/value gate, and H50 as the only follow-up packet.",
                "F26 preserves H49, H43, and H36 while keeping broader useful-case and trainable/transformed growth blocked.",
            ],
            "unsupported_here": [
                "F26 does not execute a runtime lane.",
                "F26 does not authorize arbitrary C, broader Wasm, demo-first widening, or direct trainable/transformed executor execution.",
                "F26 does not itself claim bounded system value for the internal route.",
            ],
            "disconfirmed_here": [
                "The idea that positive R50 evidence should automatically widen into a broader post-H49 runtime lane without a new falsification-first bundle."
            ],
            "distilled_result": {key: distilled[key] for key in keys},
        }
    }


def build_snapshot(inputs: dict[str, Any]) -> dict[str, Any]:
    rows = [
        ("docs/plans/2026-03-24-post-h49-origin-core-next-wave-design.md", inputs["design_text"], ["`F26_post_h49_origin_claim_delta_and_next_question_bundle`", "`R51_origin_memory_control_surface_sufficiency_gate`"]),
        ("docs/milestones/F26_post_h49_origin_claim_delta_and_next_question_bundle/claim_delta_matrix.md", inputs["claim_delta_matrix_text"], ["| `A` |", "| `D` |"]),
        ("docs/milestones/F26_post_h49_origin_claim_delta_and_next_question_bundle/next_question.md", inputs["next_question_text"], ["substrate survive a materially richer memory/control surface", "`R52_origin_internal_vs_external_executor_value_gate`"]),
        ("docs/milestones/F26_post_h49_origin_claim_delta_and_next_question_bundle/route_constraints.md", inputs["route_constraints_text"], ["`R51` is the only next runtime candidate fixed here", "`F27` is saved as planning-only"]),
        ("README.md", inputs["readme_text"], ["`F26_post_h49_origin_claim_delta_and_next_question_bundle` is now the current post-`H49` planning bundle"]),
        ("STATUS.md", inputs["status_text"], ["`F26_post_h49_origin_claim_delta_and_next_question_bundle` is now the current post-`H49` planning bundle"]),
        ("docs/publication_record/current_stage_driver.md", inputs["current_stage_driver_text"], ["The current post-`H49` planning bundle is:", "- `F26_post_h49_origin_claim_delta_and_next_question_bundle`"]),
        ("tmp/active_wave_plan.md", inputs["active_wave_plan_text"], ["`R51_origin_memory_control_surface_sufficiency_gate` is the only next runtime candidate"]),
    ]
    return {"rows": [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]}


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    summary_payload = build_summary(inputs, checklist_rows)
    write_json(OUT_DIR / "summary.json", summary_payload)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", build_claim_packet(summary_payload))
    write_json(OUT_DIR / "snapshot.json", build_snapshot(inputs))


if __name__ == "__main__":
    main()
