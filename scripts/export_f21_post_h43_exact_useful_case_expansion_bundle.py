"""Export the post-H43 exact useful-case expansion bundle for F21."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F21_post_h43_exact_useful_case_expansion_bundle"


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
        "f21_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "README.md"
        ),
        "f21_status_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "status.md"
        ),
        "f21_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "todo.md"
        ),
        "f21_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "acceptance.md"
        ),
        "f21_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "artifact_index.md"
        ),
        "surface_extension_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "surface_extension_matrix.md"
        ),
        "frontend_boundary_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "frontend_boundary_matrix.md"
        ),
        "model_bridge_scoreboard_text": read_text(
            ROOT / "docs" / "milestones" / "F21_post_h43_exact_useful_case_expansion_bundle" / "model_bridge_scoreboard.md"
        ),
        "master_plan_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-mainline-reentry-master-plan.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "r44_summary": read_json(ROOT / "results" / "R44_origin_restricted_wasm_useful_case_execution_gate" / "summary.json"),
        "r45_summary": read_json(ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h43 = inputs["h43_summary"]["summary"]
    r44 = inputs["r44_summary"]["summary"]["gate"]
    r45 = inputs["r45_summary"]["summary"]["gate"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "f21_docs_define_exact_first_post_h43_reentry_bundle",
            "status": "pass"
            if contains_all(
                inputs["f21_readme_text"],
                [
                    "planning-only exact-first bundle after the completed",
                    "`h43` as the preserved prior useful-case refreeze packet and current paper-grade endpoint",
                    "`r46_origin_useful_case_surface_generalization_gate`",
                    "conditional `r47_origin_restricted_frontend_translation_gate`",
                    "conditional `r48_origin_dual_mode_useful_case_model_gate`",
                ],
            )
            and contains_all(
                inputs["f21_status_text"],
                [
                    "completed planning-only exact-first post-`h43` reentry bundle",
                    "`exact_first_post_h43_reentry_bundle_saved`",
                    "`r46_origin_useful_case_surface_generalization_gate` as the only first admissible next runtime candidate",
                    "keeps `r47` and `r48` conditional",
                ],
            )
            and contains_all(
                inputs["f21_todo_text"],
                [
                    "make exact-first post-`h43` reentry explicit",
                    "surface-extension matrix for `r46`",
                    "frontend-boundary matrix for `r47`",
                    "comparator scoreboard for `r48`",
                ],
            )
            and contains_all(
                inputs["f21_acceptance_text"],
                [
                    "the bundle remains planning-only",
                    "`h43` remains visible as the preserved prior useful-case refreeze packet and current paper-grade endpoint",
                    "`r46` is explicit as the only first admissible next runtime candidate",
                    "`r47` and `r48` remain conditional downstream lanes",
                ],
            )
            and contains_all(
                inputs["master_plan_text"],
                [
                    "default route choice: `exact_first_post_h43_reentry`",
                    "wave 1: `f21_post_h43_exact_useful_case_expansion_bundle`",
                    "wave 2: `h44_post_h43_route_reauthorization_packet`",
                    "rejected: jump directly from `h43` into broader wasm/c or hybrid model work",
                ],
            )
            else "blocked",
            "notes": "F21 should save the post-H43 exact-first route without turning planning into execution.",
        },
        {
            "item_id": "f21_route_matrices_fix_surface_frontend_and_model_bridge_boundaries",
            "status": "pass"
            if contains_all(
                inputs["surface_extension_text"],
                [
                    "`r46_origin_useful_case_surface_generalization_gate`",
                    "`sum_i32_buffer`",
                    "`count_nonzero_i32_buffer`",
                    "`histogram16_u8`",
                    "`fixed_suite_only`",
                ],
            )
            and contains_all(
                inputs["frontend_boundary_text"],
                [
                    "`r47_origin_restricted_frontend_translation_gate`",
                    "bounded `i32`",
                    "static memory only",
                    "no heap",
                    "no alias-heavy pointers",
                ],
            )
            and contains_all(
                inputs["model_bridge_scoreboard_text"],
                [
                    "`r48_origin_dual_mode_useful_case_model_gate`",
                    "`compiled_weight_executor`",
                    "`trainable_2d_executor`",
                    "comparator-only until exact frontend survives",
                ],
            )
            and contains_all(
                inputs["f21_artifact_index_text"],
                [
                    "surface_extension_matrix.md",
                    "frontend_boundary_matrix.md",
                    "model_bridge_scoreboard.md",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                ],
            )
            else "blocked",
            "notes": "F21 must fix the near-term route order and the exact/model boundary in machine-readable tables.",
        },
        {
            "item_id": "shared_control_surfaces_record_f21_under_h45_current_state",
            "status": "pass"
            if str(h43["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(h43["claim_d_state"]) == "supported_here_narrowly"
            and str(r44["lane_verdict"]) == "useful_case_surface_supported_narrowly"
            and str(r45["lane_verdict"]) == "coequal_model_lane_supported_without_replacing_exact"
            and bool(p27["merge_executed"]) is False
            and contains_all(
                inputs["readme_text"],
                [
                    "h45_post_r46_surface_decision_packet",
                    "h44_post_h43_route_reauthorization_packet",
                    "f21_post_h43_exact_useful_case_expansion_bundle",
                    "current paper-grade endpoint remains the preserved `h43_post_r44_useful_case_refreeze` line",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "h45_post_r46_surface_decision_packet",
                    "h44_post_h43_route_reauthorization_packet",
                    "f21_post_h43_exact_useful_case_expansion_bundle",
                    "`p31_post_h43_blog_guardrails_refresh` remains the current low-priority",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/plans/2026-03-24-post-h43-mainline-reentry-master-plan.md",
                    "docs/plans/2026-03-24-post-r46-h45-surface-decision-design.md",
                    "docs/milestones/f21_post_h43_exact_useful_case_expansion_bundle/",
                    "docs/milestones/h44_post_h43_route_reauthorization_packet/",
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
                    "f21_post_h43_exact_useful_case_expansion_bundle/",
                    "h44_post_h43_route_reauthorization_packet/",
                    "p31_post_h43_blog_guardrails_refresh/",
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
                    "scripts/export_f21_post_h43_exact_useful_case_expansion_bundle.py",
                    "scripts/export_h44_post_h43_route_reauthorization_packet.py",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should expose F21 under current H45 control while keeping H43 explicit as the preserved paper-grade endpoint.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F21 saves an exact-first post-H43 reentry route without widening claims.",
            "F21 preserves H43 as the preserved prior useful-case refreeze packet and current paper-grade endpoint.",
            "F21 fixes R46 as the first admissible next runtime candidate and keeps R47/R48 conditional.",
        ],
        "unsupported_here": [
            "F21 does not itself authorize execution.",
            "F21 does not treat model work as a substitute for later exact gates.",
            "F21 does not authorize broader Wasm/C, hybrid work, or merge-to-main.",
        ],
        "disconfirmed_here": [
            "The idea that the repo should drift directly from H43 into broader frontend or model work without a later explicit packet.",
        ],
        "distilled_result": {
            "active_stage": "f21_post_h43_exact_useful_case_expansion_bundle",
            "preserved_prior_docs_only_decision_packet": "h43_post_r44_useful_case_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "exact_first_post_h43_reentry_bundle_saved",
            "first_admissible_next_runtime_candidate": "r46_origin_useful_case_surface_generalization_gate",
            "deferred_future_runtime_candidate": "r47_origin_restricted_frontend_translation_gate",
            "deferred_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
            "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
            "merge_executed": False,
            "next_required_lane": "h44_post_h43_route_reauthorization_packet",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h43-mainline-reentry-master-plan.md": (
            "master_plan_text",
            ["`r46_origin_useful_case_surface_generalization_gate`", "`r47_origin_restricted_frontend_translation_gate`"],
        ),
        "docs/milestones/F21_post_h43_exact_useful_case_expansion_bundle/surface_extension_matrix.md": (
            "surface_extension_text",
            ["`r46_origin_useful_case_surface_generalization_gate`", "`fixed_suite_only`"],
        ),
        "docs/milestones/F21_post_h43_exact_useful_case_expansion_bundle/frontend_boundary_matrix.md": (
            "frontend_boundary_text",
            ["`r47_origin_restricted_frontend_translation_gate`", "no alias-heavy pointers"],
        ),
        "docs/milestones/F21_post_h43_exact_useful_case_expansion_bundle/model_bridge_scoreboard.md": (
            "model_bridge_scoreboard_text",
            ["`r48_origin_dual_mode_useful_case_model_gate`", "comparator-only until exact frontend survives"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["h44_post_h43_route_reauthorization_packet", "f21_post_h43_exact_useful_case_expansion_bundle"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`h44_post_h43_route_reauthorization_packet` is the current active docs-only packet", "`p31_post_h43_blog_guardrails_refresh` is the current low-priority"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "active_stage": "f21_post_h43_exact_useful_case_expansion_bundle",
        "preserved_prior_docs_only_decision_packet": "h43_post_r44_useful_case_refreeze",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "selected_outcome": "exact_first_post_h43_reentry_bundle_saved",
        "first_admissible_next_runtime_candidate": "r46_origin_useful_case_surface_generalization_gate",
        "deferred_future_runtime_candidate": "r47_origin_restricted_frontend_translation_gate",
        "deferred_future_model_candidate": "r48_origin_dual_mode_useful_case_model_gate",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "h44_post_h43_route_reauthorization_packet",
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
            "experiment": "f21_post_h43_exact_useful_case_expansion_bundle",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
