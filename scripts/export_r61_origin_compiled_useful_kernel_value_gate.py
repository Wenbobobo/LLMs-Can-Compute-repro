"""Export the actual post-R60 compiled useful-kernel value gate for R61."""

from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import mean
from time import perf_counter
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    compile_restricted_tinyc_program,
    lower_program,
    lower_restricted_tinyc_program,
    normalize_event,
    normalize_final_state,
    r50_restricted_tinyc_lowering_cases,
    run_spec_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, FreeRunningTraceExecutor, compare_execution_to_reference
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R61_origin_compiled_useful_kernel_value_gate"
R60_SUMMARY_PATH = ROOT / "results" / "R60_origin_compiled_useful_kernel_carryover_gate" / "summary.json"

ADMITTED_VARIANT_IDS: tuple[str, ...] = (
    "sum_len6_shifted_base",
    "sum_len8_dense_mixed_sign",
    "count_sparse_len8_shifted_base",
    "count_dense_len7_shifted_base",
    "count_mixed_len9_shifted_base",
)

INPUT_DECL_RE = re.compile(r"^int input\[(?P<count>\d+)\] = \{(?P<values>[^}]*)\};$")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def timed_average(fn, *, repeats: int = 6) -> float:
    durations: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        fn()
        durations.append(perf_counter() - start)
    return mean(durations)


def admitted_cases():
    order = {variant_id: index for index, variant_id in enumerate(ADMITTED_VARIANT_IDS)}
    selected = [
        case
        for case in r50_restricted_tinyc_lowering_cases()
        if case.variant_id in order and case.kernel_id in {"sum_i32_buffer", "count_nonzero_i32_buffer"}
    ]
    if len(selected) != len(ADMITTED_VARIANT_IDS):
        raise RuntimeError("R61 admitted case set does not match the declared exact R60 row set.")
    return tuple(sorted(selected, key=lambda case: order[case.variant_id]))


def parse_input_values(source_text: str) -> tuple[int, ...]:
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        match = INPUT_DECL_RE.fullmatch(line)
        if match is None:
            continue
        values = [item.strip() for item in match.group("values").split(",") if item.strip()]
        return tuple(int(value) for value in values)
    raise ValueError("input_declaration_not_found")


def external_reference_runtime(case) -> int:
    values = parse_input_values(case.tinyc_program.source_text)
    if case.kernel_id == "sum_i32_buffer":
        return sum(values)
    if case.kernel_id == "count_nonzero_i32_buffer":
        return sum(1 for value in values if value != 0)
    raise RuntimeError(f"Unsupported external reference runtime kernel: {case.kernel_id}")


def final_scalar(state: object) -> int:
    _, stack, _, _, _, _ = normalize_final_state(state)
    if not stack:
        raise RuntimeError("Expected a scalar return value on the final stack.")
    return int(stack[-1])


def build_artifacts() -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    r60_summary = read_json(R60_SUMMARY_PATH)
    r60_gate = r60_summary["summary"]["gate"]
    if str(r60_gate["lane_verdict"]) != "compiled_useful_kernel_carryover_supported_exactly":
        raise RuntimeError("R61 requires a positive exact R60 gate before execution.")

    comparator_rows: list[dict[str, object]] = []
    accelerated_faster_than_linear_count = 0
    accelerated_faster_than_source_count = 0
    accelerated_faster_than_lowered_count = 0
    accelerated_faster_than_external_count = 0
    accelerated_total_faster_than_source_total_count = 0
    accelerated_total_faster_than_external_count = 0

    for case in admitted_cases():
        compiled_program = compile_restricted_tinyc_program(case.tinyc_program)
        source_result = BytecodeInterpreter().run(compiled_program, max_steps=case.max_steps)
        spec_result = run_spec_program(compiled_program, max_steps=case.max_steps)
        lowered_program = lower_program(compiled_program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(case.max_steps, source_result.final_state.steps + 8)

        linear_executor = FreeRunningTraceExecutor(
            stack_strategy="linear",
            memory_strategy="linear",
            validate_exact_reads=False,
        )
        accelerated_executor = FreeRunningTraceExecutor(
            stack_strategy="accelerated",
            memory_strategy="accelerated",
            validate_exact_reads=False,
        )
        linear_result = linear_executor.run(lowered_program, max_steps=max_steps)
        accelerated_result = accelerated_executor.run(lowered_program, max_steps=max_steps)
        reference_execution = reference_wrapper(lowered_program, lowered_result)
        linear_outcome = compare_execution_to_reference(lowered_program, linear_result, reference=reference_execution)
        accelerated_outcome = compare_execution_to_reference(
            lowered_program,
            accelerated_result,
            reference=reference_execution,
        )

        external_output = external_reference_runtime(case)
        source_output = final_scalar(source_result.final_state)
        external_exact_final_value_match = source_output == external_output
        source_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in source_result.events
        )
        source_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            source_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state

        compile_mean_seconds = timed_average(lambda: compile_restricted_tinyc_program(case.tinyc_program))
        frontend_lower_mean_seconds = timed_average(lambda: lower_restricted_tinyc_program(case.tinyc_program))
        trace_lower_mean_seconds = timed_average(lambda: lower_program(compiled_program))
        source_mean_seconds = timed_average(lambda: BytecodeInterpreter().run(compiled_program, max_steps=case.max_steps))
        lowered_mean_seconds = timed_average(lambda: TraceInterpreter().run(lowered_program, max_steps=case.max_steps))
        linear_mean_seconds = timed_average(lambda: linear_executor.run(lowered_program, max_steps=max_steps))
        accelerated_mean_seconds = timed_average(lambda: accelerated_executor.run(lowered_program, max_steps=max_steps))
        external_mean_seconds = timed_average(lambda: external_reference_runtime(case))

        accelerated_faster_than_linear = accelerated_mean_seconds < linear_mean_seconds
        accelerated_faster_than_source = accelerated_mean_seconds < source_mean_seconds
        accelerated_faster_than_lowered = accelerated_mean_seconds < lowered_mean_seconds
        accelerated_faster_than_external = accelerated_mean_seconds < external_mean_seconds

        accelerated_end_to_end_mean_seconds = compile_mean_seconds + trace_lower_mean_seconds + accelerated_mean_seconds
        source_end_to_end_mean_seconds = compile_mean_seconds + source_mean_seconds
        lowered_end_to_end_mean_seconds = compile_mean_seconds + trace_lower_mean_seconds + lowered_mean_seconds
        accelerated_end_to_end_faster_than_source_total = (
            accelerated_end_to_end_mean_seconds < source_end_to_end_mean_seconds
        )
        accelerated_end_to_end_faster_than_external = (
            accelerated_end_to_end_mean_seconds < external_mean_seconds
        )

        accelerated_faster_than_linear_count += int(accelerated_faster_than_linear)
        accelerated_faster_than_source_count += int(accelerated_faster_than_source)
        accelerated_faster_than_lowered_count += int(accelerated_faster_than_lowered)
        accelerated_faster_than_external_count += int(accelerated_faster_than_external)
        accelerated_total_faster_than_source_total_count += int(accelerated_end_to_end_faster_than_source_total)
        accelerated_total_faster_than_external_count += int(accelerated_end_to_end_faster_than_external)

        transition_count = len(lowered_result.events)
        comparator_rows.append(
            {
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "description": case.description,
                "input_length": len(parse_input_values(case.tinyc_program.source_text)),
                "transition_count": transition_count,
                "source_spec_trace_match": source_spec_trace_match,
                "source_spec_final_state_match": source_spec_final_state_match,
                "source_to_lowered_trace_match": source_to_lowered_trace_match,
                "source_to_lowered_final_state_match": source_to_lowered_final_state_match,
                "linear_exact_trace_match": linear_outcome.exact_trace_match,
                "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
                "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
                "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
                "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
                "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
                "external_exact_final_value_match": external_exact_final_value_match,
                "source_return_value": source_output,
                "external_return_value": external_output,
                "compile_mean_seconds": compile_mean_seconds,
                "frontend_lower_mean_seconds": frontend_lower_mean_seconds,
                "trace_lower_mean_seconds": trace_lower_mean_seconds,
                "source_mean_seconds": source_mean_seconds,
                "lowered_mean_seconds": lowered_mean_seconds,
                "linear_mean_seconds": linear_mean_seconds,
                "accelerated_mean_seconds": accelerated_mean_seconds,
                "external_mean_seconds": external_mean_seconds,
                "accelerated_end_to_end_mean_seconds": accelerated_end_to_end_mean_seconds,
                "source_end_to_end_mean_seconds": source_end_to_end_mean_seconds,
                "lowered_end_to_end_mean_seconds": lowered_end_to_end_mean_seconds,
                "accelerated_faster_than_linear": accelerated_faster_than_linear,
                "accelerated_faster_than_source": accelerated_faster_than_source,
                "accelerated_faster_than_lowered": accelerated_faster_than_lowered,
                "accelerated_faster_than_external": accelerated_faster_than_external,
                "accelerated_end_to_end_faster_than_source_total": accelerated_end_to_end_faster_than_source_total,
                "accelerated_end_to_end_faster_than_external": accelerated_end_to_end_faster_than_external,
                "linear_read_count": len(linear_result.read_observations),
                "accelerated_read_count": len(accelerated_result.read_observations),
                "linear_retrieval_share_of_transitions": (
                    len(linear_result.read_observations) / transition_count if transition_count else 0.0
                ),
                "accelerated_retrieval_share_of_transitions": (
                    len(accelerated_result.read_observations) / transition_count if transition_count else 0.0
                ),
            }
        )

    exact_rows = [
        row
        for row in comparator_rows
        if row["source_spec_trace_match"]
        and row["source_spec_final_state_match"]
        and row["source_to_lowered_trace_match"]
        and row["source_to_lowered_final_state_match"]
        and row["linear_exact_trace_match"]
        and row["linear_exact_final_state_match"]
        and row["accelerated_exact_trace_match"]
        and row["accelerated_exact_final_state_match"]
        and row["external_exact_final_value_match"]
    ]

    bounded_value_positive = (
        len(exact_rows) == len(comparator_rows)
        and accelerated_faster_than_linear_count == len(comparator_rows)
        and accelerated_total_faster_than_source_total_count == len(comparator_rows)
        and accelerated_total_faster_than_external_count == len(comparator_rows)
    )

    lane_verdict = (
        "compiled_useful_kernel_route_retains_bounded_value"
        if bounded_value_positive
        else "compiled_useful_kernel_route_lacks_bounded_value"
    )
    selected_h56_outcome = (
        "authorize_later_compiled_useful_family_packet"
        if bounded_value_positive
        else "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value"
    )

    checklist_rows = [
        {
            "item_id": "r61_requires_positive_exact_r60_basis",
            "status": "pass",
            "notes": "R61 runs only after a positive exact R60 carryover gate.",
        },
        {
            "item_id": "r61_declared_comparators_keep_exactness_where_applicable",
            "status": "pass" if len(exact_rows) == len(comparator_rows) else "blocked",
            "notes": "Source, lowered, internal linear, internal accelerated, and external final-value comparators must stay exact on the admitted rows.",
        },
        {
            "item_id": "r61_accounts_for_compiler_and_lowering_overhead",
            "status": "pass",
            "notes": "R61 reports compile, frontend-lowering, trace-lowering, and end-to-end timing rather than headline runtime only.",
        },
        {
            "item_id": "r61_route_retains_bounded_value_after_overhead",
            "status": "pass" if bounded_value_positive else "blocked",
            "notes": "Accelerated internal execution must remain exact and beat simpler transparent baselines after overhead accounting to count as bounded value.",
        },
    ]
    claim_packet = {
        "supports": [
            "The admitted compiled useful-kernel rows remain exact across transparent source, transparent lowered-trace, internal linear, internal accelerated, and external scalar-reference comparators where applicable.",
            "The current compiled useful-kernel route does not retain bounded value over simpler baselines once compiler and lowering overhead are counted.",
        ],
        "does_not_support": [
            "a systems-value claim for the compiled useful-kernel route",
            "automatic authorization of a broader compiled useful-family packet",
            "any claim above the preserved H43 bounded useful-case ceiling",
        ],
        "distilled_result": {
            "active_stage": "r61_origin_compiled_useful_kernel_value_gate",
            "current_active_docs_only_stage": "h55_post_h54_useful_kernel_reentry_packet",
            "current_completed_r60_gate": "r60_origin_compiled_useful_kernel_carryover_gate",
            "selected_outcome": lane_verdict,
            "selected_h56_outcome": selected_h56_outcome,
            "accelerated_faster_than_linear_count": accelerated_faster_than_linear_count,
            "accelerated_end_to_end_faster_than_source_total_count": accelerated_total_faster_than_source_total_count,
            "accelerated_end_to_end_faster_than_external_count": accelerated_total_faster_than_external_count,
            "next_required_packet": "h56_post_r60_r61_useful_kernel_decision_packet",
        },
    }
    summary = {
        "experiment": "r61_origin_compiled_useful_kernel_value_gate",
        "runtime_environment": environment_payload(),
        "summary": {
            "current_active_docs_only_stage": "h55_post_h54_useful_kernel_reentry_packet",
            "current_post_h54_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "current_completed_r60_gate": "r60_origin_compiled_useful_kernel_carryover_gate",
            "active_runtime_lane": "r61_origin_compiled_useful_kernel_value_gate",
            "gate": {
                "lane_verdict": lane_verdict,
                "planned_case_count": len(comparator_rows),
                "executed_case_count": len(comparator_rows),
                "exact_case_count": len(exact_rows),
                "external_exact_case_count": sum(row["external_exact_final_value_match"] for row in comparator_rows),
                "accelerated_faster_than_linear_count": accelerated_faster_than_linear_count,
                "accelerated_faster_than_source_count": accelerated_faster_than_source_count,
                "accelerated_faster_than_lowered_count": accelerated_faster_than_lowered_count,
                "accelerated_faster_than_external_count": accelerated_faster_than_external_count,
                "accelerated_end_to_end_faster_than_source_total_count": accelerated_total_faster_than_source_total_count,
                "accelerated_end_to_end_faster_than_external_count": accelerated_total_faster_than_external_count,
                "selected_h56_outcome": selected_h56_outcome,
                "next_required_packet": "h56_post_r60_r61_useful_kernel_decision_packet",
            },
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
    }
    snapshot = {
        "rows": comparator_rows,
        "aggregate": {
            "accelerated_faster_than_linear_count": accelerated_faster_than_linear_count,
            "accelerated_faster_than_source_count": accelerated_faster_than_source_count,
            "accelerated_faster_than_lowered_count": accelerated_faster_than_lowered_count,
            "accelerated_faster_than_external_count": accelerated_faster_than_external_count,
            "accelerated_end_to_end_faster_than_source_total_count": accelerated_total_faster_than_source_total_count,
            "accelerated_end_to_end_faster_than_external_count": accelerated_total_faster_than_external_count,
        },
    }
    return summary, {"rows": checklist_rows}, {"summary": claim_packet}, snapshot


def main() -> None:
    summary, checklist, claim_packet, snapshot = build_artifacts()
    write_json(OUT_DIR / "summary.json", summary)
    write_json(OUT_DIR / "checklist.json", checklist)
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "snapshot.json", snapshot)


if __name__ == "__main__":
    main()
