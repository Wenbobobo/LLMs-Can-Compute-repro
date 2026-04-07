"""Export the compiled trace-VM execution gate for R59."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from time import perf_counter
from typing import Any

from bytecode import BytecodeInterpreter, lower_program, r58_restricted_compiled_boundary_cases
from model import FreeRunningExecutionResult, FreeRunningTraceExecutor, compare_execution_to_reference
from exec_trace import TraceInterpreter
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R59_origin_compiled_trace_vm_execution_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
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


def timed_average(fn, *, repeats: int = 8) -> float:
    durations: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        fn()
        durations.append(perf_counter() - start)
    return mean(durations)


def build_case_manifest() -> list[dict[str, object]]:
    return [
        {
            "case_order": index + 1,
            "case_id": case.case_id,
            "category": case.category,
            "description": case.description,
            "notes": case.notes,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
        }
        for index, case in enumerate(r58_restricted_compiled_boundary_cases())
    ]


def evaluate_case(case) -> tuple[dict[str, object], dict[str, object] | None]:
    source_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
    lowered_program = lower_program(case.program)
    lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)

    max_steps = max(source_result.final_state.steps + 8, case.max_steps)
    linear_executor = FreeRunningTraceExecutor(stack_strategy="linear", memory_strategy="linear", validate_exact_reads=False)
    accelerated_executor = FreeRunningTraceExecutor(
        stack_strategy="accelerated",
        memory_strategy="accelerated",
        validate_exact_reads=False,
    )

    linear_result = linear_executor.run(lowered_program, max_steps=max_steps)
    accelerated_result = accelerated_executor.run(lowered_program, max_steps=max_steps)
    reference_execution = reference_wrapper(lowered_program, lowered_result)
    linear_outcome = compare_execution_to_reference(lowered_program, linear_result, reference=reference_execution)
    accelerated_outcome = compare_execution_to_reference(lowered_program, accelerated_result, reference=reference_execution)

    linear_counter = Counter(observation.space for observation in linear_result.read_observations)
    accelerated_counter = Counter(observation.space for observation in accelerated_result.read_observations)
    transition_count = len(lowered_result.events)

    source_time = timed_average(lambda: BytecodeInterpreter().run(case.program, max_steps=case.max_steps))
    lowered_time = timed_average(lambda: TraceInterpreter().run(lowered_program, max_steps=case.max_steps))
    linear_time = timed_average(lambda: linear_executor.run(lowered_program, max_steps=max_steps))
    accelerated_time = timed_average(lambda: accelerated_executor.run(lowered_program, max_steps=max_steps))

    first_failure = None
    if tuple(source_result.events) != tuple(lowered_result.events) or source_result.final_state != lowered_result.final_state:
        first_failure = {
            "route": "source_vs_lowered_reference",
            "case_id": case.case_id,
            "category": case.category,
        }
    elif not linear_outcome.exact_trace_match or not linear_outcome.exact_final_state_match:
        first_failure = {
            "route": "linear_internal_trace_vm",
            "case_id": case.case_id,
            "category": case.category,
            "first_mismatch_step": linear_outcome.first_mismatch_step,
        }
    elif not accelerated_outcome.exact_trace_match or not accelerated_outcome.exact_final_state_match:
        first_failure = {
            "route": "accelerated_internal_trace_vm",
            "case_id": case.case_id,
            "category": case.category,
            "first_mismatch_step": accelerated_outcome.first_mismatch_step,
        }

    row = {
        "case_id": case.case_id,
        "category": case.category,
        "program_name": case.program.name,
        "description": case.description,
        "notes": case.notes,
        "transition_count": transition_count,
        "source_to_lowered_trace_match": tuple(source_result.events) == tuple(lowered_result.events),
        "source_to_lowered_final_state_match": source_result.final_state == lowered_result.final_state,
        "linear_exact_trace_match": linear_outcome.exact_trace_match,
        "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
        "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
        "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
        "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
        "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
        "source_interpreter_mean_seconds": source_time,
        "lowered_interpreter_mean_seconds": lowered_time,
        "linear_mean_seconds": linear_time,
        "accelerated_mean_seconds": accelerated_time,
        "linear_read_count": len(linear_result.read_observations),
        "linear_stack_read_count": linear_counter.get("stack", 0),
        "linear_memory_read_count": linear_counter.get("memory", 0),
        "linear_call_read_count": linear_counter.get("call", 0),
        "linear_retrieval_share_of_transitions": len(linear_result.read_observations) / transition_count if transition_count else 0.0,
        "accelerated_read_count": len(accelerated_result.read_observations),
        "accelerated_stack_read_count": accelerated_counter.get("stack", 0),
        "accelerated_memory_read_count": accelerated_counter.get("memory", 0),
        "accelerated_call_read_count": accelerated_counter.get("call", 0),
        "accelerated_retrieval_share_of_transitions": len(accelerated_result.read_observations) / transition_count if transition_count else 0.0,
        "accelerated_faster_than_linear": accelerated_time < linear_time,
    }
    return row, first_failure


def build_artifacts() -> tuple[list[dict[str, object]], dict[str, object], dict[str, object], dict[str, object]]:
    manifest_rows = build_case_manifest()
    comparator_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None
    for case in r58_restricted_compiled_boundary_cases():
        row, case_failure = evaluate_case(case)
        comparator_rows.append(row)
        if first_failure is None and case_failure is not None:
            first_failure = case_failure

    exact_rows = [
        row
        for row in comparator_rows
        if row["source_to_lowered_trace_match"]
        and row["source_to_lowered_final_state_match"]
        and row["linear_exact_trace_match"]
        and row["linear_exact_final_state_match"]
        and row["accelerated_exact_trace_match"]
        and row["accelerated_exact_final_state_match"]
    ]
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in comparator_rows:
        grouped[str(row["category"])].append(row)
    category_rollup_rows = [
        {
            "category": category,
            "planned_case_count": len(rows),
            "exact_case_count": sum(
                row["source_to_lowered_trace_match"]
                and row["source_to_lowered_final_state_match"]
                and row["linear_exact_trace_match"]
                and row["linear_exact_final_state_match"]
                and row["accelerated_exact_trace_match"]
                and row["accelerated_exact_final_state_match"]
                for row in rows
            ),
        }
        for category, rows in sorted(grouped.items())
    ]

    lane_verdict = (
        "compiled_trace_vm_execution_supported_exactly"
        if len(exact_rows) == len(comparator_rows)
        else "compiled_trace_vm_execution_break"
    )
    selected_h54_outcome = (
        "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
        if lane_verdict == "compiled_trace_vm_execution_supported_exactly"
        else "stop_before_restricted_compiled_boundary"
    )
    stop_rule = {
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "stop_policy": "stop at first source/lowered or free-running exactness break",
    }
    summary = {
        "summary": {
            "current_active_docs_only_stage": "h53_post_h52_compiled_boundary_reentry_packet",
            "current_post_h52_planning_bundle": "f29_post_h52_restricted_compiled_boundary_bundle",
            "active_runtime_lane": "r59_origin_compiled_trace_vm_execution_gate",
            "preserved_lowering_gate": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "gate": {
                "lane_verdict": lane_verdict,
                "planned_case_count": len(comparator_rows),
                "executed_case_count": len(comparator_rows),
                "exact_case_count": len(exact_rows),
                "failed_case_count": len(comparator_rows) - len(exact_rows),
                "exact_category_count": len({row["category"] for row in exact_rows}),
                "selected_h54_outcome": selected_h54_outcome,
                "first_failure_route": None if first_failure is None else first_failure["route"],
                "next_required_packet": "h54_post_r58_r59_compiled_boundary_decision_packet",
            },
        },
        "runtime_environment": environment_payload(),
    }
    report = {
        "runtime_environment": environment_payload(),
        "comparator_rows": comparator_rows,
        "category_rollup_rows": category_rollup_rows,
        "first_failure": first_failure,
    }
    return manifest_rows, report, stop_rule, summary


def main() -> None:
    manifest_rows, report, stop_rule, summary = build_artifacts()
    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "execution_report.json", report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
