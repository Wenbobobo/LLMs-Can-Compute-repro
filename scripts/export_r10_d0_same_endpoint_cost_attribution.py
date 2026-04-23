"""Export the bounded R10 same-endpoint cost attribution companion."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from statistics import median
import time

from bytecode import (
    BytecodeInterpreter,
    checkpoint_replay_long_program,
    helper_checkpoint_braid_long_program,
    iterated_helper_accumulator_program,
    lower_program,
    r8_d0_retrieval_pressure_cases,
    subroutine_braid_long_program,
    verify_program,
)
from exec_trace import Program, TraceEvent, replay_trace, TraceInterpreter
from geometry import brute_force_hardmax_2d
from model.exact_hardmax import encode_latest_write_query
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadObservation,
    ReadStrategy,
    _LatestWriteSpace,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R10_d0_same_endpoint_cost_attribution"
R8_OUT_DIR = ROOT / "results" / "R8_d0_retrieval_pressure_gate"
REPRESENTATIVE_TOP_FAMILY_PAIRS = 2


@dataclass(frozen=True, slots=True)
class AttributionCase:
    family: str
    variant: str
    pair_rank: int
    source_program_name: str
    target_program_name: str
    program: object
    max_steps: int
    baseline_horizon_multiplier: int
    retrieval_horizon_multiplier: int


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    total_seconds: float
    dispatch_seconds: float
    retrieval_linear_seconds: float
    retrieval_accelerated_seconds: float
    bookkeeping_seconds: float
    replay_seconds: float
    read_count: int
    stack_read_count: int
    memory_read_count: int

    @property
    def retrieval_total_seconds(self) -> float:
        return self.retrieval_linear_seconds + self.retrieval_accelerated_seconds

    @property
    def local_transition_seconds(self) -> float:
        return max(0.0, self.dispatch_seconds - self.retrieval_total_seconds)

    @property
    def executor_overhead_seconds(self) -> float:
        accounted = self.dispatch_seconds + self.bookkeeping_seconds + self.replay_seconds
        return max(0.0, self.total_seconds - accounted)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def median_or_none(values: list[float]) -> float | None:
    return median(values) if values else None


def build_baseline_program(case):
    match case.family:
        case "helper_checkpoint_braid_long":
            return helper_checkpoint_braid_long_program(case.baseline_start, base_address=312, selector_seed=0)
        case "subroutine_braid_long":
            return subroutine_braid_long_program(case.baseline_start, base_address=176)
        case "iterated_helper_accumulator":
            return iterated_helper_accumulator_program(
                case.baseline_start,
                counter_address=144,
                accumulator_address=145,
            )
        case "checkpoint_replay_long":
            return checkpoint_replay_long_program(case.baseline_start, base_address=128)
        case _:
            raise ValueError(f"Unsupported R10 family: {case.family}")


def load_representative_cases() -> tuple[list[AttributionCase], list[dict[str, object]]]:
    exact_payload = read_json(R8_OUT_DIR / "exact_suite_rows.json")
    admitted_names = {
        str(row["program_name"])
        for row in exact_payload["rows"]
        if str(row["route_bucket"]) == "admitted"
    }
    pressure_payload = read_json(R8_OUT_DIR / "pressure_rows.json")
    pressure_by_name = {str(row["program_name"]): row for row in pressure_payload["rows"]}

    harder_cases = []
    for case in r8_d0_retrieval_pressure_cases():
        if case.program.name not in admitted_names:
            continue
        step_count = BytecodeInterpreter().run(case.program, max_steps=case.max_steps).final_state.steps
        harder_cases.append((step_count, case, pressure_by_name[case.program.name]))

    selected = sorted(harder_cases, key=lambda item: (item[0], item[1].program.name), reverse=True)[
        :REPRESENTATIVE_TOP_FAMILY_PAIRS
    ]
    attribution_cases: list[AttributionCase] = []
    selection_rows: list[dict[str, object]] = []

    for pair_rank, (step_count, harder_case, pressure_row) in enumerate(selected, start=1):
        source_program = build_baseline_program(harder_case)
        source_max_steps = int(
            harder_case.max_steps
            * harder_case.baseline_horizon_multiplier
            / harder_case.retrieval_horizon_multiplier
        )
        attribution_cases.append(
            AttributionCase(
                family=harder_case.family,
                variant="source_r6_8x",
                pair_rank=pair_rank,
                source_program_name=source_program.name,
                target_program_name=harder_case.program.name,
                program=source_program,
                max_steps=source_max_steps,
                baseline_horizon_multiplier=harder_case.baseline_horizon_multiplier,
                retrieval_horizon_multiplier=harder_case.retrieval_horizon_multiplier,
            )
        )
        attribution_cases.append(
            AttributionCase(
                family=harder_case.family,
                variant="harder_r8_10x",
                pair_rank=pair_rank,
                source_program_name=source_program.name,
                target_program_name=harder_case.program.name,
                program=harder_case.program,
                max_steps=harder_case.max_steps,
                baseline_horizon_multiplier=harder_case.baseline_horizon_multiplier,
                retrieval_horizon_multiplier=harder_case.retrieval_horizon_multiplier,
            )
        )
        selection_rows.append(
            {
                "pair_rank": pair_rank,
                "family": harder_case.family,
                "selection_rule": f"top_{REPRESENTATIVE_TOP_FAMILY_PAIRS}_harder_families_by_bytecode_step_count_plus_matched_r6_source_rows",
                "harder_program_name": harder_case.program.name,
                "harder_bytecode_step_count": step_count,
                "harder_max_steps": harder_case.max_steps,
                "source_program_name": source_program.name,
                "source_max_steps": source_max_steps,
                "event_growth_vs_source": float(pressure_row["event_count_growth_vs_source"]),
                "total_candidate_depth_growth_vs_source": float(
                    pressure_row["total_candidate_depth_growth_vs_source"]
                ),
                "memory_max_candidate_depth": int(pressure_row["memory_max_candidate_depth"]),
                "stack_max_candidate_depth": int(pressure_row["stack_max_candidate_depth"]),
            }
        )
    return attribution_cases, selection_rows


class ProfiledFreeRunningTraceExecutor(FreeRunningTraceExecutor):
    def run_with_profile(self, program: Program, *, max_steps: int = 10_000) -> tuple[FreeRunningExecutionResult, RuntimeProfile]:
        epsilon = Fraction(1, max_steps + 2)
        stack_history = _LatestWriteSpace(
            epsilon=epsilon,
            default_value=0,
            allow_default_reads=False,
        )
        memory_history = _LatestWriteSpace(
            epsilon=epsilon,
            default_value=self.default_memory_value,
            allow_default_reads=True,
        )

        events: list[TraceEvent] = []
        read_observations: list[ReadObservation] = []
        step = 0
        pc = 0
        stack_depth = 0
        call_stack: list[int] = []
        halted = False

        dispatch_seconds = 0.0
        bookkeeping_seconds = 0.0
        replay_seconds = 0.0
        total_start = time.perf_counter()
        self._profile_linear_seconds = 0.0
        self._profile_accelerated_seconds = 0.0

        while not halted:
            if step >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= pc < len(program)):
                raise RuntimeError(f"Program counter out of range: {pc}")

            instruction = program.instructions[pc]
            dispatch_start = time.perf_counter()
            popped, pushed, branch_taken, memory_read, memory_write, next_pc, halted = self._execute_instruction(
                step=step,
                pc=pc,
                stack_depth=stack_depth,
                call_stack=call_stack,
                instruction=instruction.opcode,
                arg=instruction.arg,
                stack_history=stack_history,
                memory_history=memory_history,
                read_observations=read_observations,
            )
            dispatch_seconds += time.perf_counter() - dispatch_start

            bookkeeping_start = time.perf_counter()
            event = TraceEvent(
                step=step,
                pc=pc,
                opcode=instruction.opcode,
                arg=instruction.arg,
                popped=popped,
                pushed=pushed,
                branch_taken=branch_taken,
                memory_read_address=None if memory_read is None else memory_read[0],
                memory_read_value=None if memory_read is None else memory_read[1],
                memory_write=memory_write,
                next_pc=next_pc,
                stack_depth_before=stack_depth,
                stack_depth_after=stack_depth - len(popped) + len(pushed),
                halted=halted,
            )
            events.append(event)

            write_base = stack_depth - len(popped)
            for offset, value in enumerate(pushed):
                stack_history.write(write_base + offset, value, step)
            if memory_write is not None:
                memory_history.write(memory_write[0], memory_write[1], step)
            bookkeeping_seconds += time.perf_counter() - bookkeeping_start

            step += 1
            pc = next_pc
            stack_depth = event.stack_depth_after

        replay_start = time.perf_counter()
        final_state = replay_trace(program, tuple(events))
        replay_seconds = time.perf_counter() - replay_start
        total_seconds = time.perf_counter() - total_start

        result = FreeRunningExecutionResult(
            program=program,
            events=tuple(events),
            final_state=final_state,
            read_observations=tuple(read_observations),
            stack_strategy=self.stack_strategy,
            memory_strategy=self.memory_strategy,
        )
        profile = RuntimeProfile(
            total_seconds=total_seconds,
            dispatch_seconds=dispatch_seconds,
            retrieval_linear_seconds=self._profile_linear_seconds,
            retrieval_accelerated_seconds=self._profile_accelerated_seconds,
            bookkeeping_seconds=bookkeeping_seconds,
            replay_seconds=replay_seconds,
            read_count=len(read_observations),
            stack_read_count=sum(observation.space == "stack" for observation in read_observations),
            memory_read_count=sum(observation.space == "memory" for observation in read_observations),
        )
        return result, profile

    def _read_from_space(
        self,
        *,
        step: int,
        address: int,
        space,
        strategy: ReadStrategy,
        history: _LatestWriteSpace,
        scorer,
        read_observations: list[ReadObservation],
    ) -> int:
        history._ensure_readable_address(address)
        query = encode_latest_write_query(address)

        linear_start = time.perf_counter()
        linear_value = brute_force_hardmax_2d(history._linear_keys, history._linear_values, query).value
        self._profile_linear_seconds += time.perf_counter() - linear_start

        accelerated_start = time.perf_counter()
        accelerated_value = history._accelerated.query(query).value
        self._profile_accelerated_seconds += time.perf_counter() - accelerated_start

        if not isinstance(linear_value, int) or not isinstance(accelerated_value, int):
            raise TypeError("Latest-write runtime expects scalar integer values.")
        if self.validate_exact_reads and linear_value != accelerated_value:
            raise RuntimeError(
                f"Exact read mismatch at step {step} for {space}[{address}]: "
                f"{linear_value} != {accelerated_value}"
            )
        if strategy == "linear":
            chosen_value = linear_value
        elif strategy == "accelerated":
            chosen_value = accelerated_value
        else:
            raise RuntimeError(f"Unsupported read strategy: {strategy}")

        read_observations.append(
            ReadObservation(
                step=step,
                space=space,
                address=address,
                source=strategy,
                chosen_value=chosen_value,
                linear_value=linear_value,
                accelerated_value=accelerated_value,
            )
        )
        return chosen_value


def profile_case(case: AttributionCase) -> dict[str, object]:
    verify_start = time.perf_counter()
    verification = verify_program(case.program)
    verify_seconds = time.perf_counter() - verify_start

    lowering_start = time.perf_counter()
    lowered_program = lower_program(case.program)
    lowering_seconds = time.perf_counter() - lowering_start

    bytecode_start = time.perf_counter()
    bytecode_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
    bytecode_seconds = time.perf_counter() - bytecode_start

    lowered_start = time.perf_counter()
    lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
    lowered_seconds = time.perf_counter() - lowered_start

    exact_executor = ProfiledFreeRunningTraceExecutor(
        stack_strategy="accelerated",
        memory_strategy="accelerated",
    )
    exact_result, exact_profile = exact_executor.run_with_profile(lowered_program, max_steps=case.max_steps)
    step_count = max(
        int(bytecode_result.final_state.steps),
        int(lowered_result.final_state.steps),
        int(exact_result.final_state.steps),
    )
    exact_total_seconds = exact_profile.total_seconds
    retrieval_total_seconds = exact_profile.retrieval_total_seconds
    exact_nonretrieval_seconds = max(0.0, exact_total_seconds - retrieval_total_seconds)
    dominant_component = max(
        {
            "retrieval_total": retrieval_total_seconds,
            "local_transition": exact_profile.local_transition_seconds,
            "trace_bookkeeping": exact_profile.bookkeeping_seconds + exact_profile.replay_seconds,
            "executor_overhead": exact_profile.executor_overhead_seconds,
        }.items(),
        key=lambda item: item[1],
    )[0]

    return {
        "pair_rank": case.pair_rank,
        "family": case.family,
        "variant": case.variant,
        "program_name": case.program.name,
        "source_program_name": case.source_program_name,
        "target_program_name": case.target_program_name,
        "max_steps": case.max_steps,
        "baseline_horizon_multiplier": case.baseline_horizon_multiplier,
        "retrieval_horizon_multiplier": case.retrieval_horizon_multiplier,
        "verification_passed": bool(verification.passed),
        "bytecode_step_count": int(bytecode_result.final_state.steps),
        "lowered_step_count": int(lowered_result.final_state.steps),
        "exact_step_count": int(exact_result.final_state.steps),
        "reference_step_count": step_count,
        "verify_seconds": verify_seconds,
        "lowering_seconds": lowering_seconds,
        "bytecode_seconds": bytecode_seconds,
        "lowered_seconds": lowered_seconds,
        "exact_total_seconds": exact_total_seconds,
        "retrieval_linear_seconds": exact_profile.retrieval_linear_seconds,
        "retrieval_accelerated_seconds": exact_profile.retrieval_accelerated_seconds,
        "retrieval_total_seconds": retrieval_total_seconds,
        "local_transition_seconds": exact_profile.local_transition_seconds,
        "trace_bookkeeping_seconds": exact_profile.bookkeeping_seconds + exact_profile.replay_seconds,
        "executor_overhead_seconds": exact_profile.executor_overhead_seconds,
        "exact_nonretrieval_seconds": exact_nonretrieval_seconds,
        "harness_seconds": verify_seconds + lowering_seconds,
        "retrieval_share_of_exact": retrieval_total_seconds / exact_total_seconds if exact_total_seconds else None,
        "linear_validation_share_of_retrieval": (
            exact_profile.retrieval_linear_seconds / retrieval_total_seconds if retrieval_total_seconds else None
        ),
        "accelerated_query_share_of_retrieval": (
            exact_profile.retrieval_accelerated_seconds / retrieval_total_seconds
            if retrieval_total_seconds
            else None
        ),
        "exact_vs_lowered_ratio": exact_total_seconds / lowered_seconds if lowered_seconds else None,
        "exact_vs_bytecode_ratio": exact_total_seconds / bytecode_seconds if bytecode_seconds else None,
        "harness_share_of_pipeline": (
            (verify_seconds + lowering_seconds)
            / (verify_seconds + lowering_seconds + lowered_seconds + exact_total_seconds)
            if (verify_seconds + lowering_seconds + lowered_seconds + exact_total_seconds)
            else None
        ),
        "read_count": exact_profile.read_count,
        "stack_read_count": exact_profile.stack_read_count,
        "memory_read_count": exact_profile.memory_read_count,
        "dominant_exact_component": dominant_component,
    }


def build_pair_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: defaultdict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["pair_rank"])].append(row)

    summaries: list[dict[str, object]] = []
    for pair_rank, pair_rows in sorted(grouped.items()):
        source_row = next(row for row in pair_rows if str(row["variant"]) == "source_r6_8x")
        harder_row = next(row for row in pair_rows if str(row["variant"]) == "harder_r8_10x")
        summaries.append(
            {
                "pair_rank": pair_rank,
                "family": source_row["family"],
                "source_program_name": source_row["program_name"],
                "harder_program_name": harder_row["program_name"],
                "source_exact_total_seconds": source_row["exact_total_seconds"],
                "harder_exact_total_seconds": harder_row["exact_total_seconds"],
                "exact_runtime_growth_vs_source": (
                    float(harder_row["exact_total_seconds"]) / float(source_row["exact_total_seconds"])
                    if source_row["exact_total_seconds"]
                    else None
                ),
                "source_retrieval_share_of_exact": source_row["retrieval_share_of_exact"],
                "harder_retrieval_share_of_exact": harder_row["retrieval_share_of_exact"],
                "source_exact_vs_lowered_ratio": source_row["exact_vs_lowered_ratio"],
                "harder_exact_vs_lowered_ratio": harder_row["exact_vs_lowered_ratio"],
                "source_dominant_exact_component": source_row["dominant_exact_component"],
                "harder_dominant_exact_component": harder_row["dominant_exact_component"],
            }
        )
    return summaries


def build_summary(
    rows: list[dict[str, object]],
    selection_rows: list[dict[str, object]],
    pair_rows: list[dict[str, object]],
) -> dict[str, object]:
    dominant_counter = Counter(str(row["dominant_exact_component"]) for row in rows)
    nonretrieval_dominant_count = sum(
        str(row["dominant_exact_component"]) != "retrieval_total" for row in rows
    )
    median_exact_vs_lowered = median_or_none(
        [float(row["exact_vs_lowered_ratio"]) for row in rows if row["exact_vs_lowered_ratio"] is not None]
    )
    median_retrieval_share = median_or_none(
        [float(row["retrieval_share_of_exact"]) for row in rows if row["retrieval_share_of_exact"] is not None]
    )
    median_harness_share = median_or_none(
        [float(row["harness_share_of_pipeline"]) for row in rows if row["harness_share_of_pipeline"] is not None]
    )
    return {
        "overall": {
            "representative_pair_count": len(selection_rows),
            "profiled_row_count": len(rows),
            "selection_rule": f"top_{REPRESENTATIVE_TOP_FAMILY_PAIRS}_harder_families_by_bytecode_step_count_plus_matched_r6_source_rows",
            "median_exact_vs_lowered_ratio": median_exact_vs_lowered,
            "median_retrieval_share_of_exact": median_retrieval_share,
            "median_harness_share_of_pipeline": median_harness_share,
            "nonretrieval_dominant_row_count": nonretrieval_dominant_count,
            "dominant_component_counts": [
                {"component": component, "count": count}
                for component, count in sorted(dominant_counter.items())
            ],
        },
        "pair_summary": pair_rows,
        "claim_impact": {
            "status": "same_endpoint_cost_attribution_measured",
            "target_claims": ["D0"],
            "e1c_status": "not_triggered",
            "next_lane": "H12_refreeze_and_record_sync",
            "supported_here": [
                "R10 stays on representative same-endpoint admitted rows and measures where exact runtime is actually spent.",
                "Current exact execution cost can be decomposed into retrieval, local transition, trace bookkeeping, and harness-facing setup rather than left as one opaque wall-clock number.",
            ],
            "unsupported_here": [
                "R10 does not reopen a broader systems packet or claim end-to-end superiority.",
                "Representative-row attribution does not justify unseen-family runtime generalization.",
            ],
            "distilled_result": {
                "dominant_component": dominant_counter.most_common(1)[0][0] if dominant_counter else None,
                "median_exact_vs_lowered_ratio": median_exact_vs_lowered,
                "median_retrieval_share_of_exact": median_retrieval_share,
                "negative_attribution_explicit": True,
            },
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    attribution_cases, selection_rows = load_representative_cases()
    cost_rows = [profile_case(case) for case in attribution_cases]
    pair_rows = build_pair_summary(cost_rows)
    summary = build_summary(cost_rows, selection_rows, pair_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r10_d0_same_endpoint_cost_attribution",
            "environment": environment.as_dict(),
            "notes": [
                "R10 uses representative-row attribution because a full component-wise exact attribution on the heaviest R8 row exceeded 150 seconds in one local benchmark.",
                "The selected set keeps the current endpoint fixed by profiling the top two harder R8 families together with their matched admitted R6 source rows.",
                "Exact attribution is measured on the accelerated exact executor while preserving exact-read validation, so the linear query path appears explicitly as validation overhead rather than being silently hidden.",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "representative_selection.json",
        {
            "experiment": "r10_representative_selection",
            "environment": environment.as_dict(),
            "rows": selection_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r10_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    write_json(
        OUT_DIR / "pair_summary.json",
        {
            "experiment": "r10_pair_summary",
            "environment": environment.as_dict(),
            "rows": pair_rows,
        },
    )
    write_csv(
        OUT_DIR / "cost_breakdown_rows.csv",
        cost_rows,
        [
            "pair_rank",
            "family",
            "variant",
            "program_name",
            "source_program_name",
            "target_program_name",
            "max_steps",
            "reference_step_count",
            "verify_seconds",
            "lowering_seconds",
            "bytecode_seconds",
            "lowered_seconds",
            "exact_total_seconds",
            "retrieval_linear_seconds",
            "retrieval_accelerated_seconds",
            "retrieval_total_seconds",
            "local_transition_seconds",
            "trace_bookkeeping_seconds",
            "executor_overhead_seconds",
            "exact_nonretrieval_seconds",
            "harness_seconds",
            "retrieval_share_of_exact",
            "linear_validation_share_of_retrieval",
            "accelerated_query_share_of_retrieval",
            "exact_vs_lowered_ratio",
            "exact_vs_bytecode_ratio",
            "harness_share_of_pipeline",
            "read_count",
            "stack_read_count",
            "memory_read_count",
            "dominant_exact_component",
        ],
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R10 D0 Same-Endpoint Cost Attribution",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `representative_selection.json`",
                "- `pair_summary.json`",
                "- `cost_breakdown_rows.csv`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
