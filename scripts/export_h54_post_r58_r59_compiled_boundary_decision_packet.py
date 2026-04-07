"""Export the post-R58/R59 compiled-boundary decision packet for H54."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H54_post_r58_r59_compiled_boundary_decision_packet"


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
        "h54_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "README.md"
        ),
        "h54_status_text": read_text(
            ROOT / "docs" / "milestones" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "status.md"
        ),
        "h54_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "todo.md"
        ),
        "h54_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "acceptance.md"
        ),
        "h54_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "artifact_index.md"
        ),
        "h54_decision_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "decision_matrix.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "milestones_readme_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "r58_summary": read_json(ROOT / "results" / "R58_origin_restricted_stack_bytecode_lowering_contract_gate" / "summary.json"),
        "r59_summary": read_json(ROOT / "results" / "R59_origin_compiled_trace_vm_execution_gate" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "h52_summary": read_json(ROOT / "results" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "summary.json"),
        "h53_summary": read_json(ROOT / "results" / "H53_post_h52_compiled_boundary_reentry_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    r58 = inputs["r58_summary"]["summary"]
    r59 = inputs["r59_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    h52 = inputs["h52_summary"]["summary"]
    h53 = inputs["h53_summary"]["summary"]
    return [
        {
            "item_id": "h54_docs_record_one_completed_compiled_boundary_closeout_outcome",
            "status": "pass"
            if contains_all(
                inputs["h54_readme_text"],
                [
                    "completed docs-only compiled-boundary decision packet",
                    "selected outcome:",
                    "`freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`",
                    "`stop_before_restricted_compiled_boundary`",
                    "`stop_due_to_compiler_work_leakage`",
                ],
            )
            and contains_all(
                inputs["h54_status_text"],
                [
                    "completed docs-only compiled-boundary decision packet",
                    "preserves `h52` as the preserved prior mechanism closeout",
                    "preserves `h43` as the paper-grade endpoint",
                    "selects `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`",
                    "restores `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h54_todo_text"],
                [
                    "[x] read landed `r58` and `r59` explicitly",
                    "[x] decide whether the restricted compiled boundary is supported narrowly",
                    "[x] preserve `h43` as the paper-grade endpoint",
                    "[x] keep transformed and trainable entry blocked",
                ],
            )
            and contains_all(
                inputs["h54_acceptance_text"],
                [
                    "`h54` remains docs-only",
                    "exactly one decision outcome is selected",
                    "`r58` and `r59` are both read explicitly",
                    "`h52` remains visible as the preserved prior mechanism closeout",
                    "`h43` remains visible as the paper-grade endpoint",
                    "`f27`, `r53`, and `r54` remain blocked",
                ],
            )
            and contains_all(
                inputs["h54_decision_matrix_text"],
                [
                    "| `freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value` |",
                    "| `stop_before_restricted_compiled_boundary` |",
                    "| `stop_due_to_compiler_work_leakage` |",
                ],
            )
            and contains_all(
                inputs["h54_artifact_index_text"],
                [
                    "scripts/export_h54_post_r58_r59_compiled_boundary_decision_packet.py",
                    "tests/test_export_h54_post_r58_r59_compiled_boundary_decision_packet.py",
                    "results/h54_post_r58_r59_compiled_boundary_decision_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "H54 must land as one explicit docs-only closeout packet with one selected outcome.",
        },
        {
            "item_id": "h54_reads_r58_and_r59_explicitly_before_closing",
            "status": "pass"
            if str(r58["gate"]["lane_verdict"]) == "restricted_stack_bytecode_lowering_supported_narrowly"
            and int(r58["gate"]["exact_case_count"]) == 5
            and str(r59["gate"]["lane_verdict"]) == "compiled_trace_vm_execution_supported_exactly"
            and int(r59["gate"]["exact_case_count"]) == 5
            and str(r59["gate"]["selected_h54_outcome"]) == "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
            else "blocked",
            "notes": "H54 should read the two positive exact gates explicitly rather than infer by momentum.",
        },
        {
            "item_id": "h54_preserves_h52_h43_and_blocked_future_entry",
            "status": "pass"
            if str(h52["selected_outcome"]) == "freeze_origin_mechanism_supported_without_fastpath_value"
            and str(h52["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and str(h53["selected_outcome"]) == "authorize_compiled_boundary_reentry_through_r58_first"
            else "blocked",
            "notes": "H54 must preserve H52 as prior mechanism history, keep H43 as the paper-grade endpoint, and keep blocked future entry blocked.",
        },
        {
            "item_id": "shared_control_surfaces_make_h54_the_current_closed_state",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "no active downstream runtime lane",
                    "`r59_origin_compiled_trace_vm_execution_gate`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "`no_active_downstream_runtime_lane`",
                    "`r59_origin_compiled_trace_vm_execution_gate`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "- `h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "the current downstream scientific lane is:",
                    "- `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "`r59_origin_compiled_trace_vm_execution_gate`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| r59 |",
                    "| h54 |",
                    "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value",
                ],
            )
            and contains_all(
                inputs["milestones_readme_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet/`",
                    "`r59_origin_compiled_trace_vm_execution_gate/`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h52` restricted compiled-boundary reentry wave",
                    "new `scripts/export_h54_post_r58_r59_compiled_boundary_decision_packet.py`",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should expose H54 as the current closed state and remove any active downstream runtime lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "R58 and R59 support one narrow restricted compiled-boundary chain exactly on the fixed typed stack-bytecode suite.",
            "H54 closes the lane as narrow compiled-boundary support without fast-path value while preserving H52 and H43.",
            "The admitted support remains transparent and exact rather than broad frontend or broader executor-entry support.",
        ],
        "unsupported_here": [
            "H54 does not authorize transformed-model entry, trainable entry, arbitrary C, or broad Wasm claims.",
            "H54 does not overturn H52 or raise the claim ceiling above H43.",
            "H54 does not reopen an active downstream runtime lane.",
        ],
        "disconfirmed_here": [
            "The idea that a positive narrow compiled boundary automatically justifies broader scope reopening or a system-value claim.",
        ],
        "distilled_result": {
            "active_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "preserved_prior_docs_only_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "preserved_prior_compiled_boundary_reentry_packet": "h53_post_h52_compiled_boundary_reentry_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_planning_bundle": "f29_post_h52_restricted_compiled_boundary_bundle",
            "selected_outcome": "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value",
            "non_selected_alternatives": [
                "stop_before_restricted_compiled_boundary",
                "stop_due_to_compiler_work_leakage",
            ],
            "current_low_priority_wave": "p38_post_h52_compiled_boundary_hygiene_sync",
            "preserved_lowering_gate": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
            "preserved_execution_gate": "r59_origin_compiled_trace_vm_execution_gate",
            "blocked_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "blocked_future_gates": [
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/H54_post_r58_r59_compiled_boundary_decision_packet/README.md",
            inputs["h54_readme_text"],
            ["selected outcome:", "`freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value`", "`no_active_downstream_runtime_lane`"],
        ),
        (
            "docs/milestones/H54_post_r58_r59_compiled_boundary_decision_packet/status.md",
            inputs["h54_status_text"],
            ["restores `no_active_downstream_runtime_lane`", "preserves `H52` as the preserved prior mechanism closeout"],
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["`h54_post_r58_r59_compiled_boundary_decision_packet`", "no active downstream runtime lane"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`h54_post_r58_r59_compiled_boundary_decision_packet`", "`no_active_downstream_runtime_lane`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["the current active stage is:", "- `h54_post_r58_r59_compiled_boundary_decision_packet`"],
        ),
        (
            "docs/claims_matrix.md",
            inputs["claims_matrix_text"],
            ["| R59 |", "| H54 |"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`h54_post_r58_r59_compiled_boundary_decision_packet`", "`no_active_downstream_runtime_lane`"],
        ),
        (
            "results/R59_origin_compiled_trace_vm_execution_gate/summary.json",
            json.dumps(inputs["r59_summary"]),
            [
                "compiled_trace_vm_execution_supported_exactly",
                "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value",
            ],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "preserved_prior_docs_only_closeout": distilled["preserved_prior_docs_only_closeout"],
        "preserved_prior_compiled_boundary_reentry_packet": distilled["preserved_prior_compiled_boundary_reentry_packet"],
        "current_active_routing_stage": distilled["current_active_routing_stage"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "current_planning_bundle": distilled["current_planning_bundle"],
        "selected_outcome": distilled["selected_outcome"],
        "non_selected_alternatives": distilled["non_selected_alternatives"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "preserved_lowering_gate": distilled["preserved_lowering_gate"],
        "preserved_execution_gate": distilled["preserved_execution_gate"],
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
