"""Export the post-H57 native useful-kernel value discriminator gate for R62."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import geometric_mean, median
from time import perf_counter
from typing import Any, Callable

from exec_trace import (
    Program,
    TraceInterpreter,
    native_count_nonzero_i32_buffer_program,
    native_sum_i32_buffer_program,
)
from model import FreeRunningExecutionResult, FreeRunningTraceExecutor, compare_execution_to_reference
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R62_origin_native_useful_kernel_value_discriminator_gate"
H57_SUMMARY_PATH = ROOT / "results" / "H57_post_h56_last_discriminator_authorization_packet" / "summary.json"
WARMUP_REPEATS = 1
TIMING_REPEATS = 3

SUM_PATTERN = (4, -1, 9, -5, 3, -2, 8, -4)
COUNT_PATTERN = (1, 2, 3, 4, 5)


@dataclass(frozen=True, slots=True)
class NativeUsefulKernelCase:
    case_id: str
    kernel_id: str
    variant_id: str
    description: str
    input_length: int
    input_base_address: int
    values: tuple[int, ...]
    builder: Callable[[tuple[int, ...], int, str], Program]

    def build_program(self) -> Program:
        return self.builder(self.values, self.input_base_address, self.variant_id)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def reference_wrapper(program: Program, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def timed_median(
    fn: Callable[[], object],
    *,
    warmup_repeats: int = WARMUP_REPEATS,
    repeats: int = TIMING_REPEATS,
) -> float:
    for _ in range(warmup_repeats):
        fn()
    durations: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        fn()
        durations.append(perf_counter() - start)
    return median(durations)


def scaled_sum_values(length: int) -> tuple[int, ...]:
    return tuple(SUM_PATTERN[index % len(SUM_PATTERN)] for index in range(length))


def dense_count_values(length: int) -> tuple[int, ...]:
    return tuple(COUNT_PATTERN[index % len(COUNT_PATTERN)] for index in range(length))


def build_sum_program(values: tuple[int, ...], base_address: int, variant_id: str) -> Program:
    return native_sum_i32_buffer_program(
        values,
        input_base_address=base_address,
        name=f"native_sum_i32_buffer_{variant_id}",
    )


def build_count_program(values: tuple[int, ...], base_address: int, variant_id: str) -> Program:
    return native_count_nonzero_i32_buffer_program(
        values,
        input_base_address=base_address,
        name=f"native_count_nonzero_i32_buffer_{variant_id}",
    )


def build_case_manifest() -> tuple[NativeUsefulKernelCase, ...]:
    return (
        NativeUsefulKernelCase(
            case_id="sum_native_len16_shift1024",
            kernel_id="sum_i32_buffer",
            variant_id="len16_shift1024",
            description="First native sum row that is retrieval-heavy and beyond the prior exact compiled horizon.",
            input_length=16,
            input_base_address=1024,
            values=scaled_sum_values(16),
            builder=build_sum_program,
        ),
        NativeUsefulKernelCase(
            case_id="sum_native_len64_shift4096",
            kernel_id="sum_i32_buffer",
            variant_id="len64_shift4096",
            description="Longer native sum extension row for the final post-H56 value discriminator.",
            input_length=64,
            input_base_address=4096,
            values=scaled_sum_values(64),
            builder=build_sum_program,
        ),
        NativeUsefulKernelCase(
            case_id="count_native_len32_dense_shift2048",
            kernel_id="count_nonzero_i32_buffer",
            variant_id="len32_dense_shift2048",
            description="First native count row that reaches beyond the prior exact compiled horizon on dense branch pressure.",
            input_length=32,
            input_base_address=2048,
            values=dense_count_values(32),
            builder=build_count_program,
        ),
        NativeUsefulKernelCase(
            case_id="count_native_len64_dense_shift8192",
            kernel_id="count_nonzero_i32_buffer",
            variant_id="len64_dense_shift8192",
            description="Longer native count extension row for the final post-H56 value discriminator.",
            input_length=64,
            input_base_address=8192,
            values=dense_count_values(64),
            builder=build_count_program,
        ),
    )


def external_scalar_reference(case: NativeUsefulKernelCase) -> int:
    if case.kernel_id == "sum_i32_buffer":
        return sum(case.values)
    if case.kernel_id == "count_nonzero_i32_buffer":
        return sum(1 for value in case.values if value != 0)
    raise RuntimeError(f"Unsupported kernel: {case.kernel_id}")


def final_scalar(state: object) -> int:
    stack = getattr(state, "stack")
    if not stack:
        raise RuntimeError("Expected final stack to contain a scalar result.")
    return int(stack[-1])


def safe_scaling_exponent(short_time: float, long_time: float, short_steps: int, long_steps: int) -> float | None:
    if short_time <= 0.0 or long_time <= 0.0 or short_steps <= 0 or long_steps <= short_steps:
        return None
    return math.log(long_time / short_time) / math.log(long_steps / short_steps)


def projected_parity_length_multiplier(
    current_ratio: float,
    accelerated_exponent: float | None,
    linear_exponent: float | None,
) -> float | None:
    if current_ratio <= 1.0:
        return 1.0
    if accelerated_exponent is None or linear_exponent is None:
        return None
    exponent_gap = accelerated_exponent - linear_exponent
    if exponent_gap >= 0.0:
        return None
    return (1.0 / current_ratio) ** (1.0 / exponent_gap)


def build_artifacts() -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    h57_summary = read_json(H57_SUMMARY_PATH)["summary"]
    if h57_summary["selected_outcome"] != "authorize_one_last_native_useful_kernel_value_discriminator_gate":
        raise RuntimeError("R62 requires the landed H57 authorization outcome.")

    comparator_rows: list[dict[str, object]] = []
    kernel_groups: dict[str, list[dict[str, object]]] = {}
    exact_case_count = 0

    for case in build_case_manifest():
        build_time = timed_median(case.build_program)
        program = case.build_program()
        reference_result = TraceInterpreter().run(program)
        max_steps = reference_result.final_state.steps + 8

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

        linear_result = linear_executor.run(program, max_steps=max_steps)
        accelerated_result = accelerated_executor.run(program, max_steps=max_steps)
        reference_execution = reference_wrapper(program, reference_result)
        linear_outcome = compare_execution_to_reference(program, linear_result, reference=reference_execution)
        accelerated_outcome = compare_execution_to_reference(program, accelerated_result, reference=reference_execution)

        external_scalar_value = external_scalar_reference(case)
        reference_scalar_value = final_scalar(reference_result.final_state)
        external_scalar_exact_match = external_scalar_value == reference_scalar_value

        linear_time = timed_median(lambda: linear_executor.run(program, max_steps=max_steps))
        accelerated_time = timed_median(lambda: accelerated_executor.run(program, max_steps=max_steps))
        external_trace_time = timed_median(lambda: TraceInterpreter().run(program))
        external_scalar_time = timed_median(lambda: external_scalar_reference(case))

        exact_row = (
            linear_outcome.exact_trace_match
            and linear_outcome.exact_final_state_match
            and accelerated_outcome.exact_trace_match
            and accelerated_outcome.exact_final_state_match
            and external_scalar_exact_match
        )
        exact_case_count += int(exact_row)
        transition_count = len(reference_result.events)
        row = {
            "case_id": case.case_id,
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "input_length": case.input_length,
            "transition_count": transition_count,
            "native_program_build_mean_seconds": build_time,
            "linear_exact_trace_match": linear_outcome.exact_trace_match,
            "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
            "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
            "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
            "external_scalar_exact_final_value_match": external_scalar_exact_match,
            "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
            "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
            "reference_return_value": reference_scalar_value,
            "external_scalar_return_value": external_scalar_value,
            "linear_mean_seconds": linear_time,
            "accelerated_mean_seconds": accelerated_time,
            "external_trace_mean_seconds": external_trace_time,
            "external_scalar_mean_seconds": external_scalar_time,
            "linear_over_accelerated_speedup": linear_time / accelerated_time if accelerated_time else None,
            "external_trace_over_accelerated_speedup": external_trace_time / accelerated_time if accelerated_time else None,
            "external_scalar_over_accelerated_speedup": external_scalar_time / accelerated_time if accelerated_time else None,
            "accelerated_over_linear_ratio": accelerated_time / linear_time if linear_time else None,
            "accelerated_over_external_scalar_ratio": accelerated_time / external_scalar_time if external_scalar_time else None,
            "linear_read_count": len(linear_result.read_observations),
            "accelerated_read_count": len(accelerated_result.read_observations),
            "linear_retrieval_share_of_transitions": len(linear_result.read_observations) / transition_count if transition_count else 0.0,
            "accelerated_retrieval_share_of_transitions": len(accelerated_result.read_observations) / transition_count if transition_count else 0.0,
            "accelerated_faster_than_linear": accelerated_time < linear_time,
            "accelerated_within_one_order_of_external_scalar": accelerated_time <= (external_scalar_time * 10.0),
            "exact_row": exact_row,
            "timing_repeats": TIMING_REPEATS,
            "warmup_repeats": WARMUP_REPEATS,
        }
        comparator_rows.append(row)
        kernel_groups.setdefault(case.kernel_id, []).append(row)

    kernel_scaling_rows: list[dict[str, object]] = []
    longest_row_accelerated_faster_than_linear_count = 0
    longest_row_within_external_order_count = 0
    exact_kernel_count = 0
    for kernel_id, rows in sorted(kernel_groups.items()):
        ordered_rows = sorted(rows, key=lambda row: int(row["transition_count"]))
        shortest = ordered_rows[0]
        longest = ordered_rows[-1]
        linear_exp = safe_scaling_exponent(
            float(shortest["linear_mean_seconds"]),
            float(longest["linear_mean_seconds"]),
            int(shortest["transition_count"]),
            int(longest["transition_count"]),
        )
        accelerated_exp = safe_scaling_exponent(
            float(shortest["accelerated_mean_seconds"]),
            float(longest["accelerated_mean_seconds"]),
            int(shortest["transition_count"]),
            int(longest["transition_count"]),
        )
        current_ratio = float(longest["accelerated_over_linear_ratio"])
        parity_multiplier = projected_parity_length_multiplier(current_ratio, accelerated_exp, linear_exp)
        longest_row_accelerated_faster_than_linear_count += int(bool(longest["accelerated_faster_than_linear"]))
        longest_row_within_external_order_count += int(bool(longest["accelerated_within_one_order_of_external_scalar"]))
        exact_kernel_count += int(all(bool(row["exact_row"]) for row in rows))
        kernel_scaling_rows.append(
            {
                "kernel_id": kernel_id,
                "shortest_case_id": shortest["case_id"],
                "longest_case_id": longest["case_id"],
                "shortest_transition_count": shortest["transition_count"],
                "longest_transition_count": longest["transition_count"],
                "shortest_retrieval_share": shortest["accelerated_retrieval_share_of_transitions"],
                "longest_retrieval_share": longest["accelerated_retrieval_share_of_transitions"],
                "longest_linear_over_accelerated_speedup": longest["linear_over_accelerated_speedup"],
                "longest_accelerated_over_external_scalar_ratio": longest["accelerated_over_external_scalar_ratio"],
                "linear_scaling_exponent": linear_exp,
                "accelerated_scaling_exponent": accelerated_exp,
                "projected_parity_length_multiplier_vs_linear": parity_multiplier,
            }
        )

    all_exact = exact_case_count == len(comparator_rows)
    geomean_linear_over_accelerated_speedup = geometric_mean(
        [float(row["linear_over_accelerated_speedup"]) for row in comparator_rows]
    )
    bounded_value_positive = (
        all_exact
        and exact_kernel_count == len(kernel_groups)
        and longest_row_accelerated_faster_than_linear_count == len(kernel_groups)
        and geomean_linear_over_accelerated_speedup >= 1.5
        and longest_row_within_external_order_count >= 1
    )

    if not all_exact:
        lane_verdict = "native_useful_kernel_discriminator_exactness_broke"
        selected_h58_outcome = "stop_due_to_native_discriminator_break"
    elif bounded_value_positive:
        lane_verdict = "native_useful_kernel_route_retains_bounded_value"
        selected_h58_outcome = "authorize_one_later_narrow_coprocessor_packet"
    else:
        lane_verdict = "native_useful_kernel_route_lacks_bounded_value"
        selected_h58_outcome = "stop_as_mechanism_supported_but_no_bounded_executor_value"

    leakage_rows = [
        {
            "item_id": "r62_uses_native_trace_programs_not_tinyc_or_bytecode_compilation",
            "status": "pass",
            "notes": "All measured programs are constructed directly in the append-only trace DSL.",
        },
        {
            "item_id": "r62_excludes_compiler_and_lowering_time_from_measured_executor_values",
            "status": "pass",
            "notes": "Program-construction time is exported separately and excluded from the runtime comparators.",
        },
        {
            "item_id": "r62_keeps_runtime_free_of_teacher_forcing_or_reference_replay",
            "status": "pass",
            "notes": "All measured executor rows run free-running against the native trace programs.",
        },
        {
            "item_id": "r62_keeps_external_scalar_reference_as_audit_only_comparator",
            "status": "pass",
            "notes": "The external scalar reference produces audit values and timing only.",
        },
    ]
    checklist_rows = [
        {
            "item_id": "r62_requires_h57_authorization",
            "status": "pass",
            "notes": "R62 runs only after the landed H57 authorization outcome.",
        },
        {
            "item_id": "r62_keeps_exactness_on_all_declared_rows",
            "status": "pass" if all_exact else "blocked",
            "notes": "Native linear, native accelerated, and external scalar final values must stay exact on every declared row.",
        },
        {
            "item_id": "r62_exports_native_build_time_separately_from_measured_runtime",
            "status": "pass",
            "notes": "Native program-construction cost is reported but not folded into executor timings.",
        },
        {
            "item_id": "r62_longest_rows_test_bounded_value_directly",
            "status": "pass" if bounded_value_positive else "blocked",
            "notes": "A positive result requires accelerated to beat linear on the longest row of each kernel and approach the external scalar comparator on at least one kernel.",
        },
    ]
    claim_packet = {
        "supports": [
            "R62 measures native useful-kernel programs directly on the append-only trace substrate with retrieval-heavy rows and no compiler/lowering timing in the executor comparators.",
            (
                "The native useful-kernel route retains bounded value on the declared native rows."
                if lane_verdict == "native_useful_kernel_route_retains_bounded_value"
                else "The native useful-kernel route does not retain bounded value on the declared native rows."
            ),
            "R62 exports exactness, timing, retrieval share, and per-kernel scaling summaries for the final discriminator.",
        ],
        "does_not_support": [
            "broad compiled or language-level scope lift",
            "any claim that native trace construction alone erases the current executor-value gap",
            "automatic reopening of transformed or trainable entry",
        ],
        "distilled_result": {
            "current_active_docs_only_stage": "h57_post_h56_last_discriminator_authorization_packet",
            "preserved_prior_docs_only_closeout": "h56_post_r60_r61_useful_kernel_decision_packet",
            "current_planning_bundle": "f31_post_h56_final_discriminating_value_boundary_bundle",
            "current_low_priority_wave": "p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "active_runtime_lane": "r62_origin_native_useful_kernel_value_discriminator_gate",
            "lane_verdict": lane_verdict,
            "planned_case_count": len(comparator_rows),
            "executed_case_count": len(comparator_rows),
            "exact_case_count": exact_case_count,
            "exact_kernel_count": exact_kernel_count,
            "longest_row_accelerated_faster_than_linear_count": longest_row_accelerated_faster_than_linear_count,
            "longest_row_within_external_order_count": longest_row_within_external_order_count,
            "geomean_linear_over_accelerated_speedup": geomean_linear_over_accelerated_speedup,
            "selected_h58_outcome": selected_h58_outcome,
            "next_required_packet": "h58_post_r62_origin_value_boundary_closeout_packet",
        },
    }
    summary = {
        "summary": {
            "current_active_docs_only_stage": "h57_post_h56_last_discriminator_authorization_packet",
            "preserved_prior_docs_only_closeout": "h56_post_r60_r61_useful_kernel_decision_packet",
            "current_planning_bundle": "f31_post_h56_final_discriminating_value_boundary_bundle",
            "current_low_priority_wave": "p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "active_runtime_lane": "r62_origin_native_useful_kernel_value_discriminator_gate",
            "gate": {
                "lane_verdict": lane_verdict,
                "planned_case_count": len(comparator_rows),
                "executed_case_count": len(comparator_rows),
                "exact_case_count": exact_case_count,
                "exact_kernel_count": exact_kernel_count,
                "longest_row_accelerated_faster_than_linear_count": longest_row_accelerated_faster_than_linear_count,
                "longest_row_within_external_order_count": longest_row_within_external_order_count,
                "geomean_linear_over_accelerated_speedup": geomean_linear_over_accelerated_speedup,
                "selected_h58_outcome": selected_h58_outcome,
                "next_required_packet": "h58_post_r62_origin_value_boundary_closeout_packet",
            },
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {
                "source": "h57",
                "selected_outcome": h57_summary["selected_outcome"],
                "only_next_runtime_candidate": h57_summary["only_next_runtime_candidate"],
            },
            *[
                {
                    "kernel_id": row["kernel_id"],
                    "shortest_case_id": row["shortest_case_id"],
                    "longest_case_id": row["longest_case_id"],
                    "longest_linear_over_accelerated_speedup": row["longest_linear_over_accelerated_speedup"],
                }
                for row in kernel_scaling_rows
            ],
        ],
        "execution_report": {
            "comparator_rows": comparator_rows,
            "kernel_scaling_rows": kernel_scaling_rows,
        },
    }

    return (
        summary,
        {"rows": checklist_rows},
        {"rows": leakage_rows},
        {"summary": claim_packet},
        snapshot,
    )


def main() -> None:
    summary, checklist, leakage, claim_packet, snapshot = build_artifacts()
    write_json(OUT_DIR / "summary.json", summary)
    write_json(OUT_DIR / "checklist.json", checklist)
    write_json(OUT_DIR / "leakage_checklist.json", leakage)
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "snapshot.json", snapshot)


if __name__ == "__main__":
    main()
