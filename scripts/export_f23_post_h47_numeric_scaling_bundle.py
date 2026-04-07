"""Export the post-H47 numeric-scaling planning bundle for F23."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F23_post_h47_numeric_scaling_bundle"


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
        "master_plan_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-h47-p35-f23-mainline-extension-master-plan.md"
        ),
        "design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-h47-f23-numeric-scaling-bundle-design.md"
        ),
        "f23_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "README.md"
        ),
        "f23_status_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "status.md"
        ),
        "f23_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "todo.md"
        ),
        "f23_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "acceptance.md"
        ),
        "f23_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "artifact_index.md"
        ),
        "precision_regime_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "precision_regime_matrix.md"
        ),
        "addressability_strategy_table_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "addressability_strategy_table.md"
        ),
        "length_bucket_plan_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "length_bucket_plan.md"
        ),
        "kill_criteria_text": read_text(
            ROOT / "docs" / "milestones" / "F23_post_h47_numeric_scaling_bundle" / "kill_criteria.md"
        ),
        "f25_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "README.md"
        ),
        "p36_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h48_falsification_closeout_bundle" / "README.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h47_summary": read_json(ROOT / "results" / "H47_post_r48_useful_case_bridge_refreeze" / "summary.json"),
        "p35_summary": read_json(ROOT / "results" / "P35_post_h47_research_record_rollup" / "summary.json"),
        "r46_summary": read_json(ROOT / "results" / "R46_origin_useful_case_surface_generalization_gate" / "summary.json"),
        "r47_summary": read_json(ROOT / "results" / "R47_origin_restricted_frontend_translation_gate" / "summary.json"),
        "r48_summary": read_json(ROOT / "results" / "R48_origin_dual_mode_useful_case_model_gate" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h47 = inputs["h47_summary"]["summary"]
    p35 = inputs["p35_summary"]["summary"]
    r46 = inputs["r46_summary"]["summary"]["gate"]
    r47 = inputs["r47_summary"]["summary"]["gate"]
    r48 = inputs["r48_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "f23_docs_define_planning_only_numeric_scaling_bundle",
            "status": "pass"
            if contains_all(
                inputs["master_plan_text"],
                [
                    "wave 2: `f23_post_h47_numeric_scaling_bundle`",
                    "wave 3: `r49_origin_useful_case_numeric_scaling_gate`",
                    "wave 4: `h48_post_r49_numeric_scaling_decision_packet`",
                    "`f24_post_h47_hybrid_executor_growth_bundle` remains dormant",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`f23_post_h47_numeric_scaling_bundle`",
                    "`h47_post_r48_useful_case_bridge_refreeze`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r49_origin_useful_case_numeric_scaling_gate`",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle`",
                    "`p36_post_h48_falsification_closeout_bundle`",
                ],
            )
            and contains_all(
                inputs["f23_readme_text"],
                [
                    "planning-only future bundle",
                    "`h47` as the active docs-only packet",
                    "`h43` as the",
                    "`r49_origin_useful_case_numeric_scaling_gate`",
                ],
            )
            and contains_all(
                inputs["f23_status_text"],
                [
                    "completed planning-only future numeric-scaling bundle after landed `p35`",
                    "preserves `h47` as the current active docs-only packet",
                    "preserves `h43` as the current paper-grade endpoint",
                    "`r49_origin_useful_case_numeric_scaling_gate` as the only next runtime candidate",
                    "`f24_post_h47_hybrid_executor_growth_bundle` dormant",
                ],
            )
            and contains_all(
                inputs["f23_todo_text"],
                [
                    "define one allowed precision regime matrix for `r49`",
                    "define one allowed addressability strategy table for `r49`",
                    "define one explicit length-bucket plan for `r49`",
                    "define one explicit kill-criteria sheet for early stop",
                ],
            )
            and contains_all(
                inputs["f23_acceptance_text"],
                [
                    "the bundle remains planning-only",
                    "`h47` remains the active docs-only packet",
                    "`h43` remains the current paper-grade endpoint",
                    "`r49_origin_useful_case_numeric_scaling_gate` is the only next runtime candidate fixed here",
                    "`f24` remains dormant",
                    "`f25/p36` remain placeholders only",
                ],
            )
            and contains_all(
                inputs["f23_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-h47-f23-numeric-scaling-bundle-design.md",
                    "docs/milestones/f25_post_h48_restricted_tinyc_lowering_bundle/readme.md",
                    "docs/milestones/p36_post_h48_falsification_closeout_bundle/readme.md",
                    "results/f23_post_h47_numeric_scaling_bundle/summary.json",
                ],
            )
            else "blocked",
            "notes": "F23 should stay planning-only, preserve H47/H43, and fix R49 as the only next runtime candidate.",
        },
        {
            "item_id": "f23_tables_fix_precision_addressability_length_and_stop_rules",
            "status": "pass"
            if contains_all(
                inputs["precision_regime_matrix_text"],
                [
                    "`float64_reference`",
                    "`float32_single_head`",
                    "`float32_radix2`",
                    "`float32_block_recentered`",
                    "`float32_segment_rescaled`",
                    "`bfloat16_single_head`",
                    "`float16_single_head`",
                ],
            )
            and contains_all(
                inputs["addressability_strategy_table_text"],
                [
                    "`preserved_absolute_base`",
                    "`radix2_address_split`",
                    "`block_recentered_window`",
                    "`segment_rescaled_window`",
                ],
            )
            and contains_all(
                inputs["length_bucket_plan_text"],
                [
                    "`bucket_a_2x`",
                    "`bucket_b_4x`",
                    "`bucket_c_8x`",
                    "up to `+4096` base-span shift",
                ],
            )
            and contains_all(
                inputs["kill_criteria_text"],
                [
                    "no admitted float32 recovery regime stays exact on `bucket_a_2x`",
                    "only `float64_reference` survives while all admitted float32 regimes fail",
                    "exactness requires a new kernel, heap, alias-heavy pointers, recursion",
                    "success requires treating comparator/model evidence as a substitute for exact `r46/r47` evidence",
                    "`h48` may authorize `f25` as the next planning bundle",
                ],
            )
            and contains_all(
                inputs["f25_readme_text"],
                [
                    "placeholder only",
                    "restricted tiny-`c` lowering question",
                    "`not_authorized_yet`",
                ],
            )
            and contains_all(
                inputs["p36_readme_text"],
                [
                    "placeholder only",
                    "practical falsifier of clean useful-case widening",
                    "`not_authorized_yet`",
                ],
            )
            else "blocked",
            "notes": "F23 must save the four planning tables plus positive and negative downstream placeholders.",
        },
        {
            "item_id": "shared_control_surfaces_record_f23_without_changing_h47",
            "status": "pass"
            if str(h47["active_stage"]) == "h47_post_r48_useful_case_bridge_refreeze"
            and str(h47["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(p35["next_required_lane"]) == "f23_post_h47_numeric_scaling_bundle"
            and str(r46["lane_verdict"]) == "surface_generalizes_narrowly"
            and str(r47["lane_verdict"]) == "restricted_frontend_supported_narrowly"
            and str(r48["lane_verdict"]) == "useful_case_model_lane_supported_without_replacing_exact"
            and contains_all(
                inputs["readme_text"],
                [
                    "`f23` is now the current",
                    "`r49_origin_useful_case_numeric_scaling_gate` as the only next runtime",
                    "`f24` dormant",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`f23_post_h47_numeric_scaling_bundle` is now complete as the current",
                    "`r49_origin_useful_case_numeric_scaling_gate` as the only next runtime candidate",
                    "`f24` dormant",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/plans/2026-03-24-post-h47-f23-numeric-scaling-bundle-design.md",
                    "docs/milestones/f23_post_h47_numeric_scaling_bundle/",
                    "results/f23_post_h47_numeric_scaling_bundle/summary.json",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| f23 |",
                    "`f23_post_h47_numeric_scaling_bundle`",
                    "`r49` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h47-f23-numeric-scaling-bundle-design.md",
                    "../milestones/f23_post_h47_numeric_scaling_bundle/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "f23_post_h47_numeric_scaling_bundle/",
                    "`r49` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current post-`h47` numeric-scaling planning bundle is:",
                    "f23_post_h47_numeric_scaling_bundle",
                    "r49_origin_useful_case_numeric_scaling_gate",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`f23_post_h47_numeric_scaling_bundle` is now the current post-`h47`",
                    "`r49_origin_useful_case_numeric_scaling_gate` as the only next runtime",
                    "`h47` is the current active docs-only packet",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h47` `f23` numeric-scaling bundle wave",
                    "scripts/export_f23_post_h47_numeric_scaling_bundle.py",
                    "results/f23_post_h47_numeric_scaling_bundle/summary.json",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should keep H47 current while exposing F23 as the current post-H47 planning bundle.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F23 saves the only admissible post-H47 numeric-scaling planning bundle without authorizing execution by itself.",
            "F23 preserves H47 as the active docs-only packet and H43 as the current paper-grade endpoint.",
            "F23 fixes R49 as the only next runtime candidate while keeping exact R46/R47 evidence decisive relative to comparator-only R48.",
        ],
        "unsupported_here": [
            "F23 does not itself authorize runtime execution.",
            "F23 does not widen frontend/runtime scope beyond structured i32 plus static memory on the preserved useful-case kernels.",
            "F23 does not authorize F24, broader Wasm/C, arbitrary C, or model substitution for exact evidence.",
        ],
        "disconfirmed_here": [
            "The idea that the post-H47 line should jump directly into broader useful-case widening or hybrid growth without first testing one narrow numeric-scaling gate.",
        ],
        "distilled_result": {
            "active_stage": "f23_post_h47_numeric_scaling_bundle",
            "current_active_docs_only_stage": "h47_post_r48_useful_case_bridge_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "post_h47_numeric_scaling_bundle_saved",
            "current_low_priority_wave": "p35_post_h47_research_record_rollup",
            "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
            "only_next_runtime_candidate": "r49_origin_useful_case_numeric_scaling_gate",
            "dormant_parallel_bundle": "f24_post_h47_hybrid_executor_growth_bundle",
            "positive_downstream_placeholder": "f25_post_h48_restricted_tinyc_lowering_bundle",
            "negative_downstream_placeholder": "p36_post_h48_falsification_closeout_bundle",
            "next_required_lane": "r49_origin_useful_case_numeric_scaling_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h47-f23-numeric-scaling-bundle-design.md": (
            "design_text",
            ["`f23_post_h47_numeric_scaling_bundle`", "`r49_origin_useful_case_numeric_scaling_gate`"],
        ),
        "docs/milestones/F23_post_h47_numeric_scaling_bundle/precision_regime_matrix.md": (
            "precision_regime_matrix_text",
            ["`float32_radix2`", "`float32_block_recentered`"],
        ),
        "docs/milestones/F23_post_h47_numeric_scaling_bundle/addressability_strategy_table.md": (
            "addressability_strategy_table_text",
            ["`radix2_address_split`", "`block_recentered_window`"],
        ),
        "docs/milestones/F23_post_h47_numeric_scaling_bundle/length_bucket_plan.md": (
            "length_bucket_plan_text",
            ["`bucket_a_2x`", "`bucket_c_8x`"],
        ),
        "docs/milestones/F23_post_h47_numeric_scaling_bundle/kill_criteria.md": (
            "kill_criteria_text",
            ["`h48` must freeze", "`f25` as the next planning bundle"],
        ),
        "docs/claims_matrix.md": (
            "claims_matrix_text",
            ["| f23 |", "`f23_post_h47_numeric_scaling_bundle`"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["the current post-`h47` numeric-scaling planning bundle is:", "`f23_post_h47_numeric_scaling_bundle`"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`f23_post_h47_numeric_scaling_bundle` is now the current post-`h47`", "`r49_origin_useful_case_numeric_scaling_gate`"],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            ["post-`h47` `f23` numeric-scaling bundle wave", "scripts/export_f23_post_h47_numeric_scaling_bundle.py"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "f23_post_h47_numeric_scaling_bundle",
        "current_active_docs_only_stage": "h47_post_r48_useful_case_bridge_refreeze",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "post_h47_numeric_scaling_bundle_saved",
        "current_low_priority_wave": "p35_post_h47_research_record_rollup",
        "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
        "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
        "only_next_runtime_candidate": "r49_origin_useful_case_numeric_scaling_gate",
        "dormant_parallel_bundle": "f24_post_h47_hybrid_executor_growth_bundle",
        "positive_downstream_placeholder": "f25_post_h48_restricted_tinyc_lowering_bundle",
        "negative_downstream_placeholder": "p36_post_h48_falsification_closeout_bundle",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "r49_origin_useful_case_numeric_scaling_gate",
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
            "experiment": "f23_post_h47_numeric_scaling_bundle",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
