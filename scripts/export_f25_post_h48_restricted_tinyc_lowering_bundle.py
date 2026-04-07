"""Export the post-H48 restricted tiny-C lowering planning bundle for F25."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F25_post_h48_restricted_tinyc_lowering_bundle"


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
            ROOT / "docs" / "plans" / "2026-03-24-post-h48-f25-restricted-tinyc-lowering-design.md"
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
        "f25_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "acceptance.md"
        ),
        "f25_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "artifact_index.md"
        ),
        "admitted_surface_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "admitted_surface_matrix.md"
        ),
        "excluded_feature_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "excluded_feature_matrix.md"
        ),
        "execution_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "execution_matrix.md"
        ),
        "kill_criteria_text": read_text(
            ROOT / "docs" / "milestones" / "F25_post_h48_restricted_tinyc_lowering_bundle" / "kill_criteria.md"
        ),
        "r50_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R50_origin_restricted_tinyc_lowering_gate" / "README.md"
        ),
        "h49_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H49_post_r50_tinyc_lowering_decision_packet" / "README.md"
        ),
        "p36_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h48_falsification_closeout_bundle" / "README.md"
        ),
        "f21_boundary_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "frontend_boundary_matrix.md"
        ),
        "f19_surface_text": read_text(
            ROOT / "docs" / "milestones" / "F19_post_f18_restricted_wasm_useful_case_roadmap" / "restricted_wasm_surface.md"
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
        "h48_summary": read_json(ROOT / "results" / "H48_post_r49_numeric_scaling_decision_packet" / "summary.json"),
        "r49_summary": read_json(ROOT / "results" / "R49_origin_useful_case_numeric_scaling_gate" / "summary.json"),
        "r47_summary": read_json(ROOT / "results" / "R47_origin_restricted_frontend_translation_gate" / "summary.json"),
        "p35_summary": read_json(ROOT / "results" / "P35_post_h47_research_record_rollup" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h48 = inputs["h48_summary"]["summary"]
    r49 = inputs["r49_summary"]["summary"]["gate"]
    r47 = inputs["r47_summary"]["summary"]["gate"]
    p35 = inputs["p35_summary"]["summary"]
    return [
        {
            "item_id": "f25_docs_define_restricted_tinyc_planning_bundle",
            "status": "pass"
            if contains_all(
                inputs["master_plan_text"],
                [
                    "wave 4: `h48_post_r49_numeric_scaling_decision_packet`",
                    "`f25_post_h48_restricted_tinyc_lowering_bundle` and",
                    "`p36_post_h48_falsification_closeout_bundle`.",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`f25_post_h48_restricted_tinyc_lowering_bundle`",
                    "`h48_post_r49_numeric_scaling_decision_packet`",
                    "`r50_origin_restricted_tinyc_lowering_gate`",
                    "`h49_post_r50_tinyc_lowering_decision_packet`",
                    "`p36_post_h48_falsification_closeout_bundle`",
                ],
            )
            and contains_all(
                inputs["f25_readme_text"],
                [
                    "completed planning-only future bundle",
                    "`h48` as the current active docs-only packet",
                    "`r50_origin_restricted_tinyc_lowering_gate`",
                    "`h49_post_r50_tinyc_lowering_decision_packet`",
                ],
            )
            and contains_all(
                inputs["f25_status_text"],
                [
                    "completed planning-only restricted tiny-`c` lowering bundle after landed `h48`",
                    "`r49_origin_useful_case_numeric_scaling_gate` as completed current numeric-scaling evidence",
                    "`r50_origin_restricted_tinyc_lowering_gate` as the only next runtime candidate",
                    "`h49_post_r50_tinyc_lowering_decision_packet` as the only follow-up packet",
                    "`bounded_useful_cases_only`",
                ],
            )
            and contains_all(
                inputs["f25_todo_text"],
                [
                    "define one admitted restricted tiny-`c` surface matrix",
                    "define one explicit excluded-feature matrix",
                    "define one execution matrix",
                    "keep numeric widening, heap, recursion, floats, io, alias-heavy pointers, library calls, and arbitrary `c` out of scope",
                ],
            )
            and contains_all(
                inputs["f25_acceptance_text"],
                [
                    "the bundle remains planning-only",
                    "`r50_origin_restricted_tinyc_lowering_gate` is the only next runtime candidate fixed here",
                    "`h49_post_r50_tinyc_lowering_decision_packet` is the only explicit follow-up packet fixed here",
                    "structured loops/branches",
                    "one top-level kernel function",
                    "no new runtime lane or scope lift is authorized beyond `r50`",
                ],
            )
            and contains_all(
                inputs["f25_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-h48-f25-restricted-tinyc-lowering-design.md",
                    "docs/milestones/r50_origin_restricted_tinyc_lowering_gate/readme.md",
                    "docs/milestones/h49_post_r50_tinyc_lowering_decision_packet/readme.md",
                    "results/f25_post_h48_restricted_tinyc_lowering_bundle/summary.json",
                ],
            )
            else "blocked",
            "notes": "F25 should land as a planning-only bundle that fixes R50 and H49 without widening scope.",
        },
        {
            "item_id": "f25_scope_stays_inside_h48_r49_r47_boundaries",
            "status": "pass"
            if str(h48["selected_outcome"]) == "authorize_f25_restricted_tinyc_lowering_bundle"
            and str(h48["authorized_next_planning_bundle"]) == "f25_post_h48_restricted_tinyc_lowering_bundle"
            and str(r49["lane_verdict"]) == "numeric_scaling_survives_through_bucket_c"
            and bool(r49["practical_falsifier_triggered"]) is False
            and str(r47["lane_verdict"]) == "restricted_frontend_supported_narrowly"
            and int(r47["translation_identity_exact_count"]) == 8
            and str(p35["current_low_priority_wave"]) == "p35_post_h47_research_record_rollup"
            and contains_all(
                inputs["admitted_surface_matrix_text"],
                [
                    "bounded scalar math",
                    "static buffer access",
                    "fixed-range table updates",
                    "single-kernel entrypoint",
                ],
            )
            and contains_all(
                inputs["excluded_feature_matrix_text"],
                [
                    "heap allocation",
                    "alias-heavy pointers",
                    "float semantics",
                    "library calls or arbitrary `c` wording",
                    "multi-function program structure",
                ],
            )
            and contains_all(
                inputs["execution_matrix_text"],
                [
                    "`sum_i32_buffer`",
                    "`count_nonzero_i32_buffer`",
                    "`histogram16_u8`",
                    "preserved `r47` `8/8` useful-case variants across the fixed",
                    "avoid fusing further numeric widening",
                ],
            )
            and contains_all(
                inputs["kill_criteria_text"],
                [
                    "exact lowering requires a new evaluator, heap, alias-heavy pointers",
                    "cannot lower instruction-faithfully onto the preserved useful-case bytecode contract",
                    "the first pass cannot stay exact on the preserved `8/8` useful-case variants",
                    "arbitrary `c`, multi-function programs, or scope wording broader than `bounded_useful_cases_only`",
                ],
            )
            and contains_all(
                inputs["r50_readme_text"],
                [
                    "authorized but not yet executed runtime candidate after completed `f25`",
                    "`r50` is the only next runtime lane fixed by `f25`",
                    "`planned_by_f25_not_yet_executed`",
                ],
            )
            and contains_all(
                inputs["h49_readme_text"],
                [
                    "future docs-only interpretation packet after potential `r50`",
                    "`h49` is not active yet",
                    "`placeholder_only`",
                ],
            )
            and contains_all(
                inputs["p36_readme_text"],
                [
                    "non-selected downstream closeout bundle",
                    "`not_selected_by_h48`",
                ],
            )
            and contains_all(
                inputs["f21_boundary_text"],
                [
                    "structured loop/branch, static memory only",
                    "no heap, no alias-heavy pointers, no recursion, no float, no io, no hidden mutable state",
                ],
            )
            and contains_all(
                inputs["f19_surface_text"],
                [
                    "bounded `i32` values only",
                    "bounded static memory with explicit address ranges",
                    "arbitrary `c` wording",
                ],
            )
            else "blocked",
            "notes": "F25 should remain inside the H48-selected route and reuse the preserved R47 useful-case contract first.",
        },
        {
            "item_id": "shared_control_surfaces_make_f25_current_and_fix_r50_h49",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "`f25_post_h48_restricted_tinyc_lowering_bundle`",
                    "current post-`h48` planning bundle",
                    "`r50_origin_restricted_tinyc_lowering_gate` as the only next runtime candidate",
                    "`h49_post_r50_tinyc_lowering_decision_packet` as the only follow-up packet",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`f25_post_h48_restricted_tinyc_lowering_bundle` is now the current post-`h48`",
                    "`r50_origin_restricted_tinyc_lowering_gate` is now the only next runtime candidate",
                    "`h49_post_r50_tinyc_lowering_decision_packet` is now the only follow-up",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`f25` as the current post-`h48` planning",
                    "`r50` as the only next runtime candidate fixed by `f25`",
                    "`h49` as the only follow-up packet fixed by `f25`",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h48-f25-restricted-tinyc-lowering-design.md",
                    "the only admissible post-`h48` runtime question",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "f25_post_h48_restricted_tinyc_lowering_bundle/` — current post-`h48`",
                    "r50_origin_restricted_tinyc_lowering_gate/` — only next runtime candidate",
                    "h49_post_r50_tinyc_lowering_decision_packet/` — only explicit follow-up packet",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| f25 |",
                    "fixes `r50` as the only next runtime candidate",
                    "fixes `h49` as the only follow-up packet",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current post-`h48` planning bundle is:",
                    "r50_origin_restricted_tinyc_lowering_gate",
                    "h49_post_r50_tinyc_lowering_decision_packet",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "current post-`h48` planning bundle:",
                    "only next runtime candidate fixed by `f25`",
                    "only follow-up packet fixed by `f25`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h48` `f25` restricted tiny-`c` lowering bundle wave",
                    "scripts/export_f25_post_h48_restricted_tinyc_lowering_bundle.py",
                    "results/f25_post_h48_restricted_tinyc_lowering_bundle/summary.json",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should keep H48 current while making F25 the current planning bundle and R50/H49 the only forward chain.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F25 lands the only admissible post-H48 planning-only restricted tiny-C lowering bundle.",
            "F25 preserves H48 as the current active docs-only packet and H43 as the paper-grade endpoint.",
            "F25 fixes exactly R50 as the next runtime candidate and H49 as the only follow-up packet.",
        ],
        "unsupported_here": [
            "F25 does not itself execute a runtime lane.",
            "F25 does not authorize arbitrary C, broader Wasm, heap, float, IO, or multi-function program claims.",
            "F25 does not fuse further numeric widening into the first tiny-C lowering pass.",
        ],
        "disconfirmed_here": [
            "The idea that positive R49 evidence should immediately widen into a broader compiled-language claim without an intermediate restricted tiny-C planning bundle.",
        ],
        "distilled_result": {
            "active_stage": "f25_post_h48_restricted_tinyc_lowering_bundle",
            "current_active_docs_only_stage": "h48_post_r49_numeric_scaling_decision_packet",
            "preserved_prior_docs_only_stage": "h47_post_r48_useful_case_bridge_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_completed_numeric_scaling_gate": "r49_origin_useful_case_numeric_scaling_gate",
            "preserved_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
            "current_low_priority_wave": "p35_post_h47_research_record_rollup",
            "selected_outcome": "restricted_tinyc_lowering_bundle_saved",
            "only_next_runtime_candidate": "r50_origin_restricted_tinyc_lowering_gate",
            "only_followup_packet": "h49_post_r50_tinyc_lowering_decision_packet",
            "non_selected_closeout_bundle": "p36_post_h48_falsification_closeout_bundle",
            "next_required_lane": "r50_origin_restricted_tinyc_lowering_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h48-f25-restricted-tinyc-lowering-design.md": (
            "design_text",
            ["`r50_origin_restricted_tinyc_lowering_gate`", "`h49_post_r50_tinyc_lowering_decision_packet`"],
        ),
        "docs/milestones/F25_post_h48_restricted_tinyc_lowering_bundle/admitted_surface_matrix.md": (
            "admitted_surface_matrix_text",
            ["bounded scalar math", "single-kernel entrypoint"],
        ),
        "docs/milestones/F25_post_h48_restricted_tinyc_lowering_bundle/excluded_feature_matrix.md": (
            "excluded_feature_matrix_text",
            ["heap allocation", "multi-function program structure"],
        ),
        "docs/milestones/F25_post_h48_restricted_tinyc_lowering_bundle/execution_matrix.md": (
            "execution_matrix_text",
            ["`sum_i32_buffer`", "`histogram16_u8`"],
        ),
        "docs/milestones/F25_post_h48_restricted_tinyc_lowering_bundle/kill_criteria.md": (
            "kill_criteria_text",
            ["`h49` must freeze", "`8/8` useful-case"],
        ),
        "docs/milestones/R50_origin_restricted_tinyc_lowering_gate/README.md": (
            "r50_readme_text",
            ["authorized but not yet executed runtime candidate", "`planned_by_f25_not_yet_executed`"],
        ),
        "docs/milestones/H49_post_r50_tinyc_lowering_decision_packet/README.md": (
            "h49_readme_text",
            ["future docs-only interpretation packet", "`placeholder_only`"],
        ),
        "docs/claims_matrix.md": (
            "claims_matrix_text",
            ["| f25 |", "fixes `r50` as the only next runtime candidate"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["the current post-`h48` planning bundle is:", "r50_origin_restricted_tinyc_lowering_gate"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["current post-`h48` planning bundle:", "only next runtime candidate fixed by `f25`"],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            ["post-`h48` `f25` restricted tiny-`c` lowering bundle wave", "export_f25_post_h48_restricted_tinyc_lowering_bundle.py"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "f25_post_h48_restricted_tinyc_lowering_bundle",
        "current_active_docs_only_stage": "h48_post_r49_numeric_scaling_decision_packet",
        "preserved_prior_docs_only_stage": "h47_post_r48_useful_case_bridge_refreeze",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "current_completed_numeric_scaling_gate": "r49_origin_useful_case_numeric_scaling_gate",
        "preserved_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
        "current_low_priority_wave": "p35_post_h47_research_record_rollup",
        "selected_outcome": "restricted_tinyc_lowering_bundle_saved",
        "only_next_runtime_candidate": "r50_origin_restricted_tinyc_lowering_gate",
        "only_followup_packet": "h49_post_r50_tinyc_lowering_decision_packet",
        "non_selected_closeout_bundle": "p36_post_h48_falsification_closeout_bundle",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "r50_origin_restricted_tinyc_lowering_gate",
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
            "experiment": "f25_post_h48_restricted_tinyc_lowering_bundle",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
