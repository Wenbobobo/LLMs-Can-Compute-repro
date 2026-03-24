"""Export the post-R51 internal-vs-external executor value gate for R52."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from time import perf_counter
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    lower_program,
    normalize_event,
    normalize_final_state,
    r51_origin_memory_control_surface_sufficiency_cases,
    run_spec_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R52_origin_internal_vs_external_executor_value_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def timed_average(fn, *, repeats: int = 3) -> float:
    durations: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        fn()
        durations.append(perf_counter() - start)
    return mean(durations)


def main() -> None:
    r51_summary = json.loads(
        (ROOT / "results" / "R51_origin_memory_control_surface_sufficiency_gate" / "summary.json").read_text(encoding="utf-8")
    )["summary"]["gate"]
    if str(r51_summary["lane_verdict"]) != "memory_control_surface_supported_narrowly":
        raise RuntimeError("R52 requires a positive R51 gate before execution.")

    comparator_rows: list[dict[str, object]] = []
    accelerated_faster_than_linear = 0
    accelerated_faster_than_external = 0

    for case in r51_origin_memory_control_surface_sufficiency_cases():
        spec_result = run_spec_program(case.program, max_steps=case.max_steps)
        external_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        lowered_program = lower_program(case.program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(case.max_steps, external_result.final_state.steps + 8)

        accelerated = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        linear = run_free_running_exact(lowered_program, decode_mode="linear", max_steps=max_steps)
        accelerated_outcome = compare_execution_to_reference(
            lowered_program,
            accelerated,
            reference=reference_wrapper(lowered_program, lowered_result),
        )
        linear_outcome = compare_execution_to_reference(
            lowered_program,
            linear,
            reference=reference_wrapper(lowered_program, lowered_result),
        )

        external_exact_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in external_result.events
        )
        external_exact_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            external_result.final_state
        )

        accelerated_time = timed_average(
            lambda: run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        )
        linear_time = timed_average(
            lambda: run_free_running_exact(lowered_program, decode_mode="linear", max_steps=max_steps)
        )
        external_time = timed_average(lambda: BytecodeInterpreter().run(case.program, max_steps=case.max_steps))

        accelerated_faster_than_linear += int(accelerated_time < linear_time)
        accelerated_faster_than_external += int(accelerated_time < external_time)

        comparator_rows.append(
            {
                "family_id": case.family_id,
                "variant_id": case.variant_id,
                "description": case.description,
                "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
                "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
                "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
                "linear_exact_trace_match": linear_outcome.exact_trace_match,
                "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
                "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
                "external_exact_trace_match": external_exact_trace_match,
                "external_exact_final_state_match": external_exact_final_state_match,
                "accelerated_mean_seconds": accelerated_time,
                "linear_mean_seconds": linear_time,
                "external_mean_seconds": external_time,
                "accelerated_vs_linear_speedup": linear_time / accelerated_time if accelerated_time else None,
                "accelerated_vs_external_speedup": external_time / accelerated_time if accelerated_time else None,
                "debugging_burden_note": (
                    "internal route keeps explicit execution trace and identity diagnostics"
                    if accelerated_outcome.exact_trace_match
                    else "internal route lost exactness before value comparison"
                ),
                "operational_burden_note": (
                    "external interpreter remains simpler to operate and materially faster"
                    if external_time < accelerated_time
                    else "internal accelerated route beats the external runtime on this row"
                ),
            }
        )

    accelerated_exact = all(
        row["accelerated_exact_trace_match"] and row["accelerated_exact_final_state_match"] for row in comparator_rows
    )
    linear_exact = all(row["linear_exact_trace_match"] and row["linear_exact_final_state_match"] for row in comparator_rows)
    external_exact = all(
        row["external_exact_trace_match"] and row["external_exact_final_state_match"] for row in comparator_rows
    )
    bounded_value_positive = (
        accelerated_exact
        and linear_exact
        and external_exact
        and accelerated_faster_than_linear >= 4
        and accelerated_faster_than_external >= 3
    )

    lane_verdict = (
        "internal_route_retains_bounded_value"
        if bounded_value_positive
        else "internal_route_lacks_bounded_value"
    )

    checklist_rows = [
        {
            "item_id": "r52_requires_positive_r51_basis",
            "status": "pass"
            if str(r51_summary["lane_verdict"]) == "memory_control_surface_supported_narrowly"
            and str(r51_summary["next_required_packet"]) == "r52_origin_internal_vs_external_executor_value_gate"
            else "blocked",
            "notes": "R52 only runs after a positive R51 lane verdict.",
        },
        {
            "item_id": "accelerated_and_linear_internal_routes_keep_exactness",
            "status": "pass" if accelerated_exact and linear_exact else "blocked",
            "notes": "R52 should compare value, not hide an exactness break inside the internal route.",
        },
        {
            "item_id": "r52_establishes_bounded_value_over_simpler_baselines",
            "status": "pass" if bounded_value_positive else "blocked",
            "notes": "Accelerated internal execution must retain bounded value over internal linear and plain external baselines.",
        },
    ]

    summary_payload = {
        "experiment": "r52_origin_internal_vs_external_executor_value_gate",
        "environment": environment_payload(),
        "summary": {
            "current_active_docs_only_stage": "h49_post_r50_tinyc_lowering_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_post_h49_planning_bundle": "f26_post_h49_origin_claim_delta_and_next_question_bundle",
            "current_completed_r51_gate": "r51_origin_memory_control_surface_sufficiency_gate",
            "active_runtime_lane": "r52_origin_internal_vs_external_executor_value_gate",
            "gate": {
                "lane_verdict": lane_verdict,
                "planned_case_count": len(comparator_rows),
                "executed_case_count": len(comparator_rows),
                "accelerated_exact_case_count": sum(
                    int(row["accelerated_exact_trace_match"] and row["accelerated_exact_final_state_match"])
                    for row in comparator_rows
                ),
                "linear_exact_case_count": sum(
                    int(row["linear_exact_trace_match"] and row["linear_exact_final_state_match"])
                    for row in comparator_rows
                ),
                "external_exact_case_count": sum(
                    int(row["external_exact_trace_match"] and row["external_exact_final_state_match"])
                    for row in comparator_rows
                ),
                "accelerated_faster_than_linear_count": accelerated_faster_than_linear,
                "accelerated_faster_than_external_count": accelerated_faster_than_external,
                "next_required_packet": "h50_post_r51_r52_scope_decision_packet",
            },
            "pass_count": sum(1 for row in checklist_rows if row["status"] == "pass"),
            "blocked_count": sum(1 for row in checklist_rows if row["status"] != "pass"),
        },
    }

    claim_packet = {
        "experiment": "r52_origin_internal_vs_external_executor_value_gate",
        "supports": [
            "internal accelerated execution stays exact on the declared R51 rows"
            if accelerated_exact
            else "internal accelerated execution does not stay exact on all declared R51 rows",
            "the internal route retains bounded value over simpler baselines"
            if bounded_value_positive
            else "the internal route does not retain bounded value over simpler baselines",
        ],
        "does_not_support": [
            "broad systems-marketing claims",
            "value superiority by headline without comparator evidence",
        ],
        "next_required_packet": "h50_post_r51_r52_scope_decision_packet",
    }

    write_json(OUT_DIR / "summary.json", summary_payload)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "snapshot.json", {"comparator_rows": comparator_rows})


if __name__ == "__main__":
    main()
