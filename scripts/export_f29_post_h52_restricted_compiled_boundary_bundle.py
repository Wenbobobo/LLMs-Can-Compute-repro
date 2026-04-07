"""Export the post-H52 restricted compiled-boundary bundle for F29."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F29_post_h52_restricted_compiled_boundary_bundle"


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
        if any(needle in lowered for needle in lowered_needles) and line not in seen:
            hits.append(line)
            seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def load_inputs() -> dict[str, Any]:
    return {
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-25-post-h52-restricted-compiled-boundary-reentry-master-plan.md"),
        "f29_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "README.md"
        ),
        "f29_status_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "status.md"
        ),
        "f29_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "todo.md"
        ),
        "f29_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "acceptance.md"
        ),
        "f29_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "artifact_index.md"
        ),
        "claim_delta_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F29_post_h52_restricted_compiled_boundary_bundle"
            / "compiled_boundary_claim_delta_matrix.md"
        ),
        "question_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "compiled_boundary_question.md"
        ),
        "route_constraints_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "route_constraints.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h52_summary": read_json(ROOT / "results" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h52 = inputs["h52_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "f29_docs_define_post_h52_compiled_boundary_bundle",
            "status": "pass"
            if contains_all(
                inputs["design_text"],
                [
                    "`f29_post_h52_restricted_compiled_boundary_bundle`",
                    "`h53_post_h52_compiled_boundary_reentry_packet`",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                    "`r59_origin_compiled_trace_vm_execution_gate`",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                ],
            )
            and contains_all(
                inputs["f29_readme_text"],
                [
                    "compiled-boundary reentry",
                    "`h52`",
                    "`h43`",
                    "`h36`",
                    "`h53_post_h52_compiled_boundary_reentry_packet`",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                ],
            )
            and contains_all(
                inputs["f29_status_text"],
                [
                    "completed planning-only post-`h52` restricted compiled-boundary bundle",
                    "fixes `h53` as the only follow-up packet",
                    "fixes `r58` as the only next runtime candidate",
                    "keeps `f27`, `r53`, and `r54` blocked",
                ],
            )
            and contains_all(
                inputs["f29_todo_text"],
                [
                    "define one compiled-boundary claim-delta matrix",
                    "define one compiled-boundary question note",
                    "define one route-constraints note",
                    "keep `r58` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["f29_acceptance_text"],
                [
                    "the bundle remains planning-only",
                    "`h52` remains the preserved prior docs-only packet",
                    "`h43` remains the paper-grade endpoint",
                    "`h53` is the only follow-up packet fixed here",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate` is the only next runtime candidate fixed here",
                ],
            )
            and contains_all(
                inputs["claim_delta_text"],
                [
                    "| `a` |",
                    "| `d` |",
                    "isolate this first in `r58`",
                    "close explicitly in `h54`",
                ],
            )
            and contains_all(
                inputs["question_text"],
                [
                    "the selected question is:",
                    "`h53_post_h52_compiled_boundary_reentry_packet`",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                    "`r59_origin_compiled_trace_vm_execution_gate`",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                ],
            )
            and contains_all(
                inputs["route_constraints_text"],
                [
                    "`h53` is the only follow-up packet fixed here",
                    "`r58` is the only next runtime candidate fixed here",
                    "`r59` can run only after positive exact `r58`",
                    "`h54` is the only closeout packet fixed for this compiled-boundary lane",
                    "`f27` remains saved as planning-only blocked future storage",
                    "`r53` and `r54` remain saved future gates only",
                ],
            )
            and contains_all(
                inputs["f29_artifact_index_text"],
                [
                    "docs/milestones/f29_post_h52_restricted_compiled_boundary_bundle/compiled_boundary_claim_delta_matrix.md",
                    "docs/milestones/f29_post_h52_restricted_compiled_boundary_bundle/compiled_boundary_question.md",
                    "docs/milestones/f29_post_h52_restricted_compiled_boundary_bundle/route_constraints.md",
                    "results/f29_post_h52_restricted_compiled_boundary_bundle/summary.json",
                ],
            )
            else "blocked",
            "notes": "F29 should save one planning-only compiled-boundary bundle and fix only the narrow H53->R58->R59->H54 lane.",
        },
        {
            "item_id": "upstream_h52_and_h43_support_f29_reframing_without_overturning_h52",
            "status": "pass"
            if str(h52["selected_outcome"]) == "freeze_origin_mechanism_supported_without_fastpath_value"
            and str(h52["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and bool(h43["merge_executed"]) is False
            else "blocked",
            "notes": "F29 must preserve H52 as a negative fast-path closeout while keeping H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "shared_control_surfaces_make_f29_the_current_preserved_planning_bundle",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "active docs-only packet:",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "current planning bundle:",
                    "`f29_post_h52_restricted_compiled_boundary_bundle`",
                    "current low-priority operational/docs wave:",
                    "`p38_post_h52_compiled_boundary_hygiene_sync`",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                    "`r59_origin_compiled_trace_vm_execution_gate`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current active docs-only decision packet is",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "the current planning bundle remains",
                    "`f29_post_h52_restricted_compiled_boundary_bundle`",
                    "the current low-priority operational/docs wave remains",
                    "`p38_post_h52_compiled_boundary_hygiene_sync`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current planning bundle is:",
                    "- `f29_post_h52_restricted_compiled_boundary_bundle`",
                    "the completed lowering gate under the current compiled-boundary lane is:",
                    "- `r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "`f29_post_h52_restricted_compiled_boundary_bundle`",
                    "`p38_post_h52_compiled_boundary_hygiene_sync`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| f29 |",
                    "the post-`h52` line can reopen only through one planning-only restricted compiled-boundary bundle",
                    "fixes `r58 -> r59 -> h54` as the only admissible sequence",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`f29_post_h52_restricted_compiled_boundary_bundle` remains the preserved planning bundle",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet` is now the current active",
                    "`p38_post_h52_compiled_boundary_hygiene_sync` remains the current low-priority",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h52` restricted compiled-boundary reentry wave",
                    "new `scripts/export_f29_post_h52_restricted_compiled_boundary_bundle.py`",
                    "new `results/f29_post_h52_restricted_compiled_boundary_bundle/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared current-wave surfaces should expose F29 as the preserved planning bundle under active H54 and closed downstream routing.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F29 preserves negative H52 while reopening only a narrower compiled-boundary reading of the current Origin-facing materials.",
            "F29 fixes H53 as the only follow-up packet and R58 as the only next runtime candidate.",
            "F29 keeps R59 and H54 as the only conditional downstream sequence and leaves F27, R53, and R54 blocked.",
        ],
        "unsupported_here": [
            "F29 does not overturn H52 or reactivate transformed or trainable executor entry.",
            "F29 does not authorize arbitrary C, broad Wasm, or general 'LLMs are computers' wording.",
            "F29 does not itself execute a runtime lane or claim fast-path value.",
        ],
        "disconfirmed_here": [
            "The idea that a closed H52 mechanism wave should automatically reopen broader executor-entry work by momentum.",
        ],
        "distilled_result": {
            "active_stage": "f29_post_h52_restricted_compiled_boundary_bundle",
            "current_active_docs_only_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "preserved_prior_docs_only_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_routing_refreeze_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "selected_outcome": "post_h52_restricted_compiled_boundary_bundle_saved",
            "only_followup_packet": "h53_post_h52_compiled_boundary_reentry_packet",
            "only_next_runtime_candidate": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
            "only_conditional_later_sequence": [
                "r59_origin_compiled_trace_vm_execution_gate",
                "h54_post_r58_r59_compiled_boundary_decision_packet",
            ],
            "current_low_priority_wave": "p38_post_h52_compiled_boundary_hygiene_sync",
            "blocked_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "blocked_future_gates": [
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
            "next_required_lane": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/plans/2026-03-25-post-h52-restricted-compiled-boundary-reentry-master-plan.md",
            inputs["design_text"],
            ["compiled-boundary", "`r58`", "`r59`", "`h54`"],
        ),
        (
            "docs/milestones/F29_post_h52_restricted_compiled_boundary_bundle/compiled_boundary_claim_delta_matrix.md",
            inputs["claim_delta_text"],
            ["| `A` |", "| `D` |", "`R58`", "`R59`", "`H54`"],
        ),
        (
            "docs/milestones/F29_post_h52_restricted_compiled_boundary_bundle/compiled_boundary_question.md",
            inputs["question_text"],
            ["The selected question is:", "`H53_post_h52_compiled_boundary_reentry_packet`", "`R58_origin_restricted_stack_bytecode_lowering_contract_gate`"],
        ),
        (
            "docs/milestones/F29_post_h52_restricted_compiled_boundary_bundle/route_constraints.md",
            inputs["route_constraints_text"],
            ["`H53` is the only follow-up packet fixed here", "`R58` is the only next runtime candidate fixed here"],
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["The current planning bundle is `F29_post_h52_restricted_compiled_boundary_bundle`", "`R58_origin_restricted_stack_bytecode_lowering_contract_gate`"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`F29_post_h52_restricted_compiled_boundary_bundle`", "`R58_origin_restricted_stack_bytecode_lowering_contract_gate`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["The current planning bundle is:", "- `F29_post_h52_restricted_compiled_boundary_bundle`"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`F29_post_h52_restricted_compiled_boundary_bundle` remains the preserved planning bundle", "`no_active_downstream_runtime_lane`"],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "current_active_docs_only_stage": distilled["current_active_docs_only_stage"],
        "preserved_prior_docs_only_closeout": distilled["preserved_prior_docs_only_closeout"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "current_routing_refreeze_stage": distilled["current_routing_refreeze_stage"],
        "selected_outcome": distilled["selected_outcome"],
        "only_followup_packet": distilled["only_followup_packet"],
        "only_next_runtime_candidate": distilled["only_next_runtime_candidate"],
        "only_conditional_later_sequence": distilled["only_conditional_later_sequence"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "blocked_future_bundle": distilled["blocked_future_bundle"],
        "blocked_future_gates": distilled["blocked_future_gates"],
        "next_required_lane": distilled["next_required_lane"],
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})
    write_json(OUT_DIR / "summary.json", {"summary": summary, "runtime_environment": environment_payload()})


if __name__ == "__main__":
    main()
