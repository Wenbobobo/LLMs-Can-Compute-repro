"""Export the full-surface R17 same-endpoint runtime bridge on the admitted R8/R15 surface."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from statistics import median
import time
from typing import Any, Callable

from bytecode import (
    BytecodeInterpreter,
    lower_program,
    r8_d0_retrieval_pressure_cases,
    r15_d0_remaining_family_retrieval_pressure_cases,
)
from exec_trace import Program, TraceEvent, replay_trace, TraceInterpreter
from geometry import brute_force_hardmax_2d
from model import compare_execution_to_reference, run_free_running_exact
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
OUT_DIR = ROOT / "results" / "R17_d0_full_surface_runtime_bridge"
R8_OUT_DIR = ROOT / "results" / "R8_d0_retrieval_pressure_gate"
R15_OUT_DIR = ROOT / "results" / "R15_d0_remaining_family_retrieval_pressure_gate"
R16_OUT_DIR = ROOT / "results" / "R16_d0_real_trace_precision_boundary_saturation"
PROFILE_REPEATS = 1
MATERIAL_DECODE_SPEEDUP = 1.10
BRIDGE_RATIO_THRESHOLD = 1.50
R18_OUTLIER_RATIO_THRESHOLD = 1.50
R18_DOMINANT_COMPONENT_SHARE_THRESHOLD = 0.60
R18_NAMED_COMPONENTS = frozenset({"retrieval_total", "local_transition", "trace_bookkeeping"})


@dataclass(frozen=True, slots=True)
class AdmittedSurfaceCase:
    source_lane: str
    case: Any
    exact_row: dict[str, object]
    stream_name: str
    boundary_bearing_stream: bool


@dataclass(frozen=True, slots=True)
class FocusedAttributionCase:
    selection_rank: int
    focus_reason: str
    source_lane: str
    family: str
    program_name: str
    baseline_program_name: str
    baseline_horizon_multiplier: int
    retrieval_horizon_multiplier: int
    bytecode_step_count: int
    boundary_bearing_stream: bool
    program: Any
    max_steps: int


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


class ProfiledFreeRunningTraceExecutor(FreeRunningTraceExecutor):
    def run_with_profile(
        self,
        program: Program,
        *,
        max_steps: int = 10_000,
    ) -> tuple[FreeRunningExecutionResult, RuntimeProfile]:
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


def read_json(path: Path) -> dict[str, Any]:
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


def profile_callable(
    fn: Callable[[], Any],
    *,
    repeats: int = PROFILE_REPEATS,
) -> tuple[float, list[float], Any]:
    samples: list[float] = []
    last_result: Any = None
    for _ in range(repeats):
        start = time.perf_counter()
        last_result = fn()
        samples.append(time.perf_counter() - start)
    return median(samples), samples, last_result


def runtime_row_is_exact(row: dict[str, object]) -> bool:
    return bool(
        row["linear_exact_trace_match"]
        and row["linear_exact_final_state_match"]
        and row["accelerated_exact_trace_match"]
        and row["accelerated_exact_final_state_match"]
        and row["linear_accelerated_trace_match"]
        and row["linear_accelerated_final_state_match"]
        and row["exact_read_agreement"]
    )


def load_admitted_surface_cases() -> tuple[tuple[AdmittedSurfaceCase, ...], dict[str, object]]:
    handoff_payload = read_json(R16_OUT_DIR / "runtime_bridge_handoff.json")
    handoff_summary = dict(handoff_payload["summary"])
    representative_streams = {str(name) for name in handoff_summary["representative_precision_streams"]}
    boundary_bearing_streams = {str(name) for name in handoff_summary["boundary_bearing_streams"]}

    case_specs = (
        (
            "R8_d0_retrieval_pressure_gate",
            R8_OUT_DIR / "exact_suite_rows.json",
            r8_d0_retrieval_pressure_cases(),
        ),
        (
            "R15_d0_remaining_family_retrieval_pressure_gate",
            R15_OUT_DIR / "exact_suite_rows.json",
            r15_d0_remaining_family_retrieval_pressure_cases(),
        ),
    )

    surface_cases: list[AdmittedSurfaceCase] = []
    source_rows: list[dict[str, object]] = []
    exact_suite_row_count = 0

    for source_lane, exact_suite_path, cases in case_specs:
        exact_payload = read_json(exact_suite_path)
        exact_rows = [row for row in exact_payload["rows"] if str(row["route_bucket"]) == "admitted"]
        exact_suite_row_count += len(exact_payload["rows"])
        case_by_name = {case.program.name: case for case in cases}

        lane_surface_cases: list[AdmittedSurfaceCase] = []
        for exact_row in exact_rows:
            program_name = str(exact_row["program_name"])
            case = case_by_name[program_name]
            stream_name = f"{program_name}_memory"
            if stream_name not in representative_streams:
                raise RuntimeError(f"R17 missing R16 handoff stream for {stream_name}.")
            lane_surface_cases.append(
                AdmittedSurfaceCase(
                    source_lane=source_lane,
                    case=case,
                    exact_row=exact_row,
                    stream_name=stream_name,
                    boundary_bearing_stream=stream_name in boundary_bearing_streams,
                )
            )

        source_rows.append(
            {
                "source_lane": source_lane,
                "exact_suite_row_count": len(exact_payload["rows"]),
                "admitted_program_count": len(lane_surface_cases),
                "families": sorted(surface_case.case.family for surface_case in lane_surface_cases),
                "program_names": sorted(surface_case.case.program.name for surface_case in lane_surface_cases),
                "boundary_bearing_stream_count": sum(
                    surface_case.boundary_bearing_stream for surface_case in lane_surface_cases
                ),
            }
        )
        surface_cases.extend(lane_surface_cases)

    if len(surface_cases) != int(handoff_summary["screened_stream_count"]):
        raise RuntimeError(
            "R17 admitted surface does not match the R16 runtime bridge handoff stream count."
        )

    metadata = {
        "precision_handoff": handoff_summary,
        "source_rows": source_rows,
        "exact_suite_row_count": exact_suite_row_count,
        "admitted_program_count": len(surface_cases),
    }
    ordered_cases = tuple(
        sorted(
            surface_cases,
            key=lambda item: (item.source_lane, item.case.family, item.case.program.name),
        )
    )
    return ordered_cases, metadata


def build_runtime_surface_index(surface_cases: tuple[AdmittedSurfaceCase, ...]) -> list[dict[str, object]]:
    return [
        {
            "source_lane": surface_case.source_lane,
            "family": surface_case.case.family,
            "baseline_stage": surface_case.case.baseline_stage,
            "baseline_program_name": surface_case.case.baseline_program_name,
            "baseline_horizon_multiplier": surface_case.case.baseline_horizon_multiplier,
            "baseline_start": surface_case.case.baseline_start,
            "retrieval_horizon_multiplier": surface_case.case.retrieval_horizon_multiplier,
            "scaled_start": surface_case.case.scaled_start,
            "program_name": surface_case.case.program.name,
            "comparison_mode": surface_case.case.comparison_mode,
            "max_steps": surface_case.case.max_steps,
            "stream_name": surface_case.stream_name,
            "boundary_bearing_stream": surface_case.boundary_bearing_stream,
            "bytecode_step_count": int(surface_case.exact_row["bytecode_step_count"]),
        }
        for surface_case in surface_cases
    ]


def select_focused_attribution_cases(
    surface_cases: tuple[AdmittedSurfaceCase, ...],
) -> tuple[tuple[FocusedAttributionCase, ...], list[dict[str, object]]]:
    boundary_cases = [surface_case for surface_case in surface_cases if surface_case.boundary_bearing_stream]
    if len(boundary_cases) != 1:
        raise RuntimeError(
            f"R17 expected exactly one boundary-bearing admitted stream from R16, got {len(boundary_cases)}."
        )
    boundary_case = boundary_cases[0]

    r15_cases = [
        surface_case
        for surface_case in surface_cases
        if surface_case.source_lane == "R15_d0_remaining_family_retrieval_pressure_gate"
    ]
    heaviest_r15_case = max(
        r15_cases,
        key=lambda surface_case: (
            int(surface_case.exact_row["bytecode_step_count"]),
            surface_case.case.program.name,
        ),
    )

    selected_cases = (
        FocusedAttributionCase(
            selection_rank=1,
            focus_reason="unique_boundary_bearing_precision_stream",
            source_lane=boundary_case.source_lane,
            family=boundary_case.case.family,
            program_name=boundary_case.case.program.name,
            baseline_program_name=boundary_case.case.baseline_program_name,
            baseline_horizon_multiplier=boundary_case.case.baseline_horizon_multiplier,
            retrieval_horizon_multiplier=boundary_case.case.retrieval_horizon_multiplier,
            bytecode_step_count=int(boundary_case.exact_row["bytecode_step_count"]),
            boundary_bearing_stream=boundary_case.boundary_bearing_stream,
            program=boundary_case.case.program,
            max_steps=boundary_case.case.max_steps,
        ),
        FocusedAttributionCase(
            selection_rank=2,
            focus_reason="heaviest_r15_admitted_by_bytecode_step_count",
            source_lane=heaviest_r15_case.source_lane,
            family=heaviest_r15_case.case.family,
            program_name=heaviest_r15_case.case.program.name,
            baseline_program_name=heaviest_r15_case.case.baseline_program_name,
            baseline_horizon_multiplier=heaviest_r15_case.case.baseline_horizon_multiplier,
            retrieval_horizon_multiplier=heaviest_r15_case.case.retrieval_horizon_multiplier,
            bytecode_step_count=int(heaviest_r15_case.exact_row["bytecode_step_count"]),
            boundary_bearing_stream=heaviest_r15_case.boundary_bearing_stream,
            program=heaviest_r15_case.case.program,
            max_steps=heaviest_r15_case.case.max_steps,
        ),
    )

    selection_rows = [
        {
            "selection_rank": case.selection_rank,
            "focus_reason": case.focus_reason,
            "selection_rule": "unique_boundary_bearing_precision_stream_plus_heaviest_r15_admitted_by_bytecode_step_count",
            "source_lane": case.source_lane,
            "family": case.family,
            "program_name": case.program_name,
            "baseline_program_name": case.baseline_program_name,
            "baseline_horizon_multiplier": case.baseline_horizon_multiplier,
            "retrieval_horizon_multiplier": case.retrieval_horizon_multiplier,
            "bytecode_step_count": case.bytecode_step_count,
            "boundary_bearing_stream": case.boundary_bearing_stream,
        }
        for case in selected_cases
    ]
    return selected_cases, selection_rows


def profile_surface_runtime_case(surface_case: AdmittedSurfaceCase) -> dict[str, object]:
    lowered_program = lower_program(surface_case.case.program)

    bytecode_median, bytecode_samples, bytecode_result = profile_callable(
        lambda: BytecodeInterpreter().run(surface_case.case.program, max_steps=surface_case.case.max_steps)
    )
    lowered_median, lowered_samples, lowered_result = profile_callable(
        lambda: TraceInterpreter().run(lowered_program, max_steps=surface_case.case.max_steps)
    )
    linear_median, linear_samples, linear_result = profile_callable(
        lambda: run_free_running_exact(
            lowered_program,
            decode_mode="linear",
            max_steps=surface_case.case.max_steps,
        )
    )
    accelerated_median, accelerated_samples, accelerated_result = profile_callable(
        lambda: run_free_running_exact(
            lowered_program,
            decode_mode="accelerated",
            max_steps=surface_case.case.max_steps,
        )
    )

    linear_outcome = compare_execution_to_reference(lowered_program, linear_result, reference=lowered_result)
    accelerated_outcome = compare_execution_to_reference(
        lowered_program,
        accelerated_result,
        reference=lowered_result,
    )
    step_count = max(
        int(bytecode_result.final_state.steps),
        int(lowered_result.final_state.steps),
        int(linear_outcome.program_steps),
        int(accelerated_outcome.program_steps),
    )
    bytecode_ns_per_step = (bytecode_median / bytecode_result.final_state.steps) * 1e9
    lowered_ns_per_step = (lowered_median / lowered_result.final_state.steps) * 1e9
    linear_ns_per_step = (linear_median / linear_outcome.program_steps) * 1e9
    accelerated_ns_per_step = (accelerated_median / accelerated_outcome.program_steps) * 1e9

    return {
        "source_lane": surface_case.source_lane,
        "family": surface_case.case.family,
        "baseline_stage": surface_case.case.baseline_stage,
        "baseline_program_name": surface_case.case.baseline_program_name,
        "baseline_horizon_multiplier": surface_case.case.baseline_horizon_multiplier,
        "retrieval_horizon_multiplier": surface_case.case.retrieval_horizon_multiplier,
        "horizon_multiplier": surface_case.case.retrieval_horizon_multiplier,
        "program_name": surface_case.case.program.name,
        "comparison_mode": surface_case.case.comparison_mode,
        "max_steps": surface_case.case.max_steps,
        "stream_name": surface_case.stream_name,
        "boundary_bearing_stream": surface_case.boundary_bearing_stream,
        "reference_step_count": step_count,
        "profile_repeats": PROFILE_REPEATS,
        "bytecode_median_seconds": bytecode_median,
        "lowered_median_seconds": lowered_median,
        "linear_median_seconds": linear_median,
        "accelerated_median_seconds": accelerated_median,
        "bytecode_samples": bytecode_samples,
        "lowered_samples": lowered_samples,
        "linear_samples": linear_samples,
        "accelerated_samples": accelerated_samples,
        "bytecode_ns_per_step": bytecode_ns_per_step,
        "lowered_ns_per_step": lowered_ns_per_step,
        "linear_ns_per_step": linear_ns_per_step,
        "accelerated_ns_per_step": accelerated_ns_per_step,
        "accelerated_speedup_vs_linear": linear_ns_per_step / accelerated_ns_per_step,
        "accelerated_ratio_vs_lowered": accelerated_ns_per_step / lowered_ns_per_step,
        "accelerated_ratio_vs_bytecode": accelerated_ns_per_step / bytecode_ns_per_step,
        "linear_exact_trace_match": linear_outcome.exact_trace_match,
        "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
        "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
        "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
        "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
        "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
        "linear_accelerated_trace_match": linear_result.events == accelerated_result.events,
        "linear_accelerated_final_state_match": linear_result.final_state == accelerated_result.final_state,
        "read_observation_count": len(accelerated_result.read_observations),
        "exact_read_agreement": all(
            observation.linear_value == observation.accelerated_value
            for observation in accelerated_result.read_observations
        ),
    }


def build_family_bridge_summary(runtime_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for row in runtime_rows:
        grouped[str(row["family"])].append(row)

    family_rows: list[dict[str, object]] = []
    for family, family_runtime_rows in sorted(grouped.items()):
        family_rows.append(
            {
                "family": family,
                "source_lanes": sorted({str(row["source_lane"]) for row in family_runtime_rows}),
                "row_count": len(family_runtime_rows),
                "program_names": sorted(str(row["program_name"]) for row in family_runtime_rows),
                "boundary_bearing_stream_count": sum(bool(row["boundary_bearing_stream"]) for row in family_runtime_rows),
                "median_accelerated_speedup_vs_linear": median(
                    float(row["accelerated_speedup_vs_linear"]) for row in family_runtime_rows
                ),
                "median_accelerated_ratio_vs_lowered": median(
                    float(row["accelerated_ratio_vs_lowered"]) for row in family_runtime_rows
                ),
                "median_accelerated_ratio_vs_bytecode": median(
                    float(row["accelerated_ratio_vs_bytecode"]) for row in family_runtime_rows
                ),
                "max_reference_step_count": max(int(row["reference_step_count"]) for row in family_runtime_rows),
                "all_rows_exact": all(runtime_row_is_exact(row) for row in family_runtime_rows),
            }
        )
    return family_rows


def build_source_surface_runtime_summary(runtime_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for row in runtime_rows:
        grouped[str(row["source_lane"])].append(row)

    source_rows: list[dict[str, object]] = []
    for source_lane, source_runtime_rows in sorted(grouped.items()):
        source_rows.append(
            {
                "source_lane": source_lane,
                "row_count": len(source_runtime_rows),
                "family_count": len({str(row["family"]) for row in source_runtime_rows}),
                "boundary_bearing_stream_count": sum(bool(row["boundary_bearing_stream"]) for row in source_runtime_rows),
                "median_accelerated_speedup_vs_linear": median(
                    float(row["accelerated_speedup_vs_linear"]) for row in source_runtime_rows
                ),
                "median_accelerated_ratio_vs_lowered": median(
                    float(row["accelerated_ratio_vs_lowered"]) for row in source_runtime_rows
                ),
                "median_accelerated_ratio_vs_bytecode": median(
                    float(row["accelerated_ratio_vs_bytecode"]) for row in source_runtime_rows
                ),
                "all_rows_exact": all(runtime_row_is_exact(row) for row in source_runtime_rows),
            }
        )
    return source_rows


def profile_focused_attribution_case(case: FocusedAttributionCase) -> dict[str, object]:
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
    component_durations = {
        "retrieval_total": retrieval_total_seconds,
        "local_transition": exact_profile.local_transition_seconds,
        "trace_bookkeeping": exact_profile.bookkeeping_seconds + exact_profile.replay_seconds,
        "executor_overhead": exact_profile.executor_overhead_seconds,
    }
    dominant_component, dominant_component_seconds = max(
        component_durations.items(),
        key=lambda item: item[1],
    )

    return {
        "selection_rank": case.selection_rank,
        "focus_reason": case.focus_reason,
        "source_lane": case.source_lane,
        "family": case.family,
        "program_name": case.program_name,
        "baseline_program_name": case.baseline_program_name,
        "baseline_horizon_multiplier": case.baseline_horizon_multiplier,
        "retrieval_horizon_multiplier": case.retrieval_horizon_multiplier,
        "boundary_bearing_stream": case.boundary_bearing_stream,
        "max_steps": case.max_steps,
        "reference_step_count": step_count,
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
        "exact_nonretrieval_seconds": max(0.0, exact_total_seconds - retrieval_total_seconds),
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
        "read_count": exact_profile.read_count,
        "stack_read_count": exact_profile.stack_read_count,
        "memory_read_count": exact_profile.memory_read_count,
        "dominant_exact_component": dominant_component,
        "dominant_component_share": (
            dominant_component_seconds / exact_total_seconds if exact_total_seconds else None
        ),
    }


def build_focused_attribution_summary(focused_rows: list[dict[str, object]]) -> dict[str, object]:
    dominant_counter = Counter(str(row["dominant_exact_component"]) for row in focused_rows)
    return {
        "row_count": len(focused_rows),
        "selection_rule": "unique_boundary_bearing_precision_stream_plus_heaviest_r15_admitted_by_bytecode_step_count",
        "median_exact_vs_lowered_ratio": median_or_none(
            [float(row["exact_vs_lowered_ratio"]) for row in focused_rows if row["exact_vs_lowered_ratio"] is not None]
        ),
        "median_retrieval_share_of_exact": median_or_none(
            [float(row["retrieval_share_of_exact"]) for row in focused_rows if row["retrieval_share_of_exact"] is not None]
        ),
        "dominant_component_counts": [
            {"component": component, "count": count}
            for component, count in sorted(dominant_counter.items())
        ],
        "rows": [
            {
                "selection_rank": row["selection_rank"],
                "focus_reason": row["focus_reason"],
                "source_lane": row["source_lane"],
                "family": row["family"],
                "program_name": row["program_name"],
                "boundary_bearing_stream": row["boundary_bearing_stream"],
                "exact_vs_lowered_ratio": row["exact_vs_lowered_ratio"],
                "retrieval_share_of_exact": row["retrieval_share_of_exact"],
                "dominant_exact_component": row["dominant_exact_component"],
                "dominant_component_share": row["dominant_component_share"],
            }
            for row in focused_rows
        ],
    }


def assess_surface_stopgo(runtime_rows: list[dict[str, object]]) -> dict[str, object]:
    contradiction_candidate_count = sum(not runtime_row_is_exact(row) for row in runtime_rows)
    median_speedup = median(float(row["accelerated_speedup_vs_linear"]) for row in runtime_rows)
    median_ratio_vs_lowered = median(float(row["accelerated_ratio_vs_lowered"]) for row in runtime_rows)

    if contradiction_candidate_count:
        status = "stop_exactness_contradiction"
        reason = "Full-surface exact runtime diverged on at least one admitted R8/R15 program."
    elif median_speedup < MATERIAL_DECODE_SPEEDUP:
        status = "stop_decode_gain_not_material"
        reason = "Accelerated decode does not provide a material same-endpoint speedup over linear decode on the admitted full surface."
    elif median_ratio_vs_lowered > BRIDGE_RATIO_THRESHOLD:
        status = "stop_bridge_not_yet_closed"
        reason = "Accelerated exact execution remains materially farther from the lowered endpoint than the current bridge threshold allows."
    else:
        status = "go_full_surface_bridge_positive"
        reason = "Accelerated exact execution remains exact on the full admitted surface and closes the lowered-endpoint bridge."

    worst_row = max(
        runtime_rows,
        key=lambda row: (float(row["accelerated_ratio_vs_lowered"]), float(row["reference_step_count"])),
    )
    return {
        "stopgo_status": status,
        "median_accelerated_speedup_vs_linear": median_speedup,
        "median_accelerated_ratio_vs_lowered": median_ratio_vs_lowered,
        "contradiction_candidate_count": contradiction_candidate_count,
        "worst_bridge_program_name": worst_row["program_name"],
        "worst_bridge_family": worst_row["family"],
        "worst_bridge_ratio_vs_lowered": worst_row["accelerated_ratio_vs_lowered"],
        "reason": reason,
        "thresholds": {
            "material_decode_speedup": MATERIAL_DECODE_SPEEDUP,
            "bridge_ratio_vs_lowered": BRIDGE_RATIO_THRESHOLD,
        },
    }


def assess_r18_trigger(
    runtime_rows: list[dict[str, object]],
    focused_rows: list[dict[str, object]],
) -> dict[str, object]:
    contradiction_candidate_count = sum(not runtime_row_is_exact(row) for row in runtime_rows)
    if contradiction_candidate_count:
        return {
            "triggered": False,
            "repair_target": None,
            "next_lane": "E1c_compiled_boundary_patch",
            "reason": "Full-surface runtime exactness contradicted the admitted baseline, so repair escalation is blocked behind E1c.",
            "bridge_open": None,
            "sharp_local_outlier": None,
            "candidate_matches_surface_worst": None,
            "thresholds": {
                "bridge_ratio_vs_lowered": BRIDGE_RATIO_THRESHOLD,
                "focused_outlier_ratio": R18_OUTLIER_RATIO_THRESHOLD,
                "dominant_component_share": R18_DOMINANT_COMPONENT_SHARE_THRESHOLD,
            },
        }

    stopgo = assess_surface_stopgo(runtime_rows)
    bridge_open = float(stopgo["median_accelerated_ratio_vs_lowered"]) > BRIDGE_RATIO_THRESHOLD
    worst_surface_row = max(
        runtime_rows,
        key=lambda row: (float(row["accelerated_ratio_vs_lowered"]), float(row["reference_step_count"])),
    )
    ordered_focused_rows = sorted(
        focused_rows,
        key=lambda row: (
            float(row["exact_vs_lowered_ratio"] or 0.0),
            float(row["retrieval_total_seconds"]),
        ),
        reverse=True,
    )
    worst_focused_row = ordered_focused_rows[0]
    other_focused_row = ordered_focused_rows[1] if len(ordered_focused_rows) > 1 else None

    worst_focus_ratio = float(worst_focused_row["exact_vs_lowered_ratio"] or 0.0)
    other_focus_ratio = float(other_focused_row["exact_vs_lowered_ratio"] or 0.0) if other_focused_row else 0.0
    outlier_ratio = worst_focus_ratio / other_focus_ratio if other_focus_ratio else None
    sharp_local_outlier = (
        other_focused_row is not None
        and outlier_ratio is not None
        and worst_focus_ratio > BRIDGE_RATIO_THRESHOLD
        and outlier_ratio >= R18_OUTLIER_RATIO_THRESHOLD
    )
    dominant_component = str(worst_focused_row["dominant_exact_component"])
    dominant_component_share = float(worst_focused_row["dominant_component_share"] or 0.0)
    candidate_matches_surface_worst = str(worst_surface_row["program_name"]) == str(worst_focused_row["program_name"])
    repair_target_named = bool(
        bridge_open
        and sharp_local_outlier
        and candidate_matches_surface_worst
        and dominant_component in R18_NAMED_COMPONENTS
        and dominant_component_share >= R18_DOMINANT_COMPONENT_SHARE_THRESHOLD
    )

    repair_target = (
        {
            "program_name": worst_focused_row["program_name"],
            "family": worst_focused_row["family"],
            "component": dominant_component,
            "focus_reason": worst_focused_row["focus_reason"],
            "exact_vs_lowered_ratio": worst_focused_row["exact_vs_lowered_ratio"],
            "dominant_component_share": worst_focused_row["dominant_component_share"],
            "repair_scope": "same_endpoint_runtime_counterfactual_only",
        }
        if repair_target_named
        else None
    )
    if repair_target_named:
        next_lane = "R18_d0_same_endpoint_runtime_repair_counterfactual"
        reason = (
            "One focused attribution row is a sharp full-surface runtime outlier and names a bounded same-endpoint component target."
        )
    else:
        next_lane = "H17_refreeze_and_conditional_frontier_recheck"
        reason = (
            "The full-surface bridge can be recorded without opening R18 because the focused attribution subset did not isolate one bounded runtime repair target."
        )

    return {
        "triggered": repair_target_named,
        "repair_target": repair_target,
        "next_lane": next_lane,
        "reason": reason,
        "bridge_open": bridge_open,
        "sharp_local_outlier": sharp_local_outlier,
        "candidate_matches_surface_worst": candidate_matches_surface_worst,
        "surface_worst_program_name": worst_surface_row["program_name"],
        "surface_worst_family": worst_surface_row["family"],
        "focused_worst_program_name": worst_focused_row["program_name"],
        "focused_worst_family": worst_focused_row["family"],
        "focused_outlier_ratio": outlier_ratio,
        "thresholds": {
            "bridge_ratio_vs_lowered": BRIDGE_RATIO_THRESHOLD,
            "focused_outlier_ratio": R18_OUTLIER_RATIO_THRESHOLD,
            "dominant_component_share": R18_DOMINANT_COMPONENT_SHARE_THRESHOLD,
        },
    }


def build_summary(
    runtime_rows: list[dict[str, object]],
    family_rows: list[dict[str, object]],
    source_surface_rows: list[dict[str, object]],
    focused_attribution_summary: dict[str, object],
    *,
    surface_metadata: dict[str, object],
    r18_trigger_assessment: dict[str, object],
) -> dict[str, object]:
    stopgo = assess_surface_stopgo(runtime_rows)
    contradiction_candidate_count = int(stopgo["contradiction_candidate_count"])

    if contradiction_candidate_count:
        next_lane = "E1c_compiled_boundary_patch"
        e1c_status = "triggered"
    elif bool(r18_trigger_assessment["triggered"]):
        next_lane = "R18_d0_same_endpoint_runtime_repair_counterfactual"
        e1c_status = "not_triggered"
    else:
        next_lane = "H17_refreeze_and_conditional_frontier_recheck"
        e1c_status = "not_triggered"

    return {
        "overall": {
            "exact_suite_row_count": int(surface_metadata["exact_suite_row_count"]),
            "admitted_surface_row_count": int(surface_metadata["admitted_program_count"]),
            "source_lane_count": len(source_surface_rows),
            "family_count": len(family_rows),
            "boundary_bearing_stream_count": sum(bool(row["boundary_bearing_stream"]) for row in runtime_rows),
            "runtime_profiled_row_count": len(runtime_rows),
            "focused_attribution_row_count": int(focused_attribution_summary["row_count"]),
            "profile_repeats": PROFILE_REPEATS,
            "median_bytecode_ns_per_step": median_or_none(
                [float(row["bytecode_ns_per_step"]) for row in runtime_rows]
            ),
            "median_lowered_ns_per_step": median_or_none(
                [float(row["lowered_ns_per_step"]) for row in runtime_rows]
            ),
            "median_linear_ns_per_step": median_or_none(
                [float(row["linear_ns_per_step"]) for row in runtime_rows]
            ),
            "median_accelerated_ns_per_step": median_or_none(
                [float(row["accelerated_ns_per_step"]) for row in runtime_rows]
            ),
            "median_accelerated_speedup_vs_linear": stopgo["median_accelerated_speedup_vs_linear"],
            "median_accelerated_ratio_vs_lowered": stopgo["median_accelerated_ratio_vs_lowered"],
            "contradiction_candidate_count": contradiction_candidate_count,
        },
        "source_surface": {
            "rows": source_surface_rows,
        },
        "stopgo": stopgo,
        "focused_attribution": focused_attribution_summary,
        "claim_impact": {
            "status": "full_surface_same_endpoint_runtime_bridge_measured",
            "target_claims": ["D0"],
            "e1c_status": e1c_status,
            "next_lane": next_lane,
            "supported_here": [
                "R17 returns to same-endpoint runtime only after R16 screened the full admitted same-scope R8/R15 precision surface.",
                "All 8 admitted surface rows are profiled for runtime bridge cost instead of leaving post-R15 runtime coverage implicit.",
                "Focused attribution stays bounded to the unique boundary-bearing stream and the heaviest admitted R15 row, so any repair follow-up remains optional and local.",
            ],
            "unsupported_here": [
                "R17 does not reopen a broader systems packet, arbitrary compiled-language claims, or unseen-family runtime generalization.",
                "A negative or mixed bridge result is still a bounded runtime measurement rather than proof of a wider impossibility claim.",
                "R18 remains inactive unless this export names a bounded same-endpoint repair target explicitly.",
            ],
            "distilled_result": {
                "stopgo_status": stopgo["stopgo_status"],
                "median_accelerated_speedup_vs_linear": stopgo["median_accelerated_speedup_vs_linear"],
                "median_accelerated_ratio_vs_lowered": stopgo["median_accelerated_ratio_vs_lowered"],
                "r18_triggered": bool(r18_trigger_assessment["triggered"]),
            },
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    surface_cases, surface_metadata = load_admitted_surface_cases()
    runtime_surface_index = build_runtime_surface_index(surface_cases)
    focused_cases, focused_selection_rows = select_focused_attribution_cases(surface_cases)

    runtime_rows = [profile_surface_runtime_case(surface_case) for surface_case in surface_cases]
    family_rows = build_family_bridge_summary(runtime_rows)
    source_surface_rows = build_source_surface_runtime_summary(runtime_rows)
    focused_rows = [profile_focused_attribution_case(case) for case in focused_cases]
    focused_attribution_summary = build_focused_attribution_summary(focused_rows)
    r18_trigger_assessment = assess_r18_trigger(runtime_rows, focused_rows)
    summary = build_summary(
        runtime_rows,
        family_rows,
        source_surface_rows,
        focused_attribution_summary,
        surface_metadata=surface_metadata,
        r18_trigger_assessment=r18_trigger_assessment,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r17_d0_full_surface_runtime_bridge",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R7_d0_same_endpoint_runtime_bridge/summary.json",
                "results/R10_d0_same_endpoint_cost_attribution/summary.json",
                "results/R15_d0_remaining_family_retrieval_pressure_gate/summary.json",
                "results/R15_d0_remaining_family_retrieval_pressure_gate/exact_suite_rows.json",
                "results/R16_d0_real_trace_precision_boundary_saturation/summary.json",
                "results/R16_d0_real_trace_precision_boundary_saturation/runtime_bridge_handoff.json",
                "results/R8_d0_retrieval_pressure_gate/summary.json",
                "results/R8_d0_retrieval_pressure_gate/exact_suite_rows.json",
            ],
            "notes": [
                "R17 profiles the full admitted same-scope R8/R15 surface instead of reusing the representative-only R7 subset.",
                "Runtime rows stay on the same lowered endpoint and keep linear-versus-accelerated exact execution explicit on every admitted program.",
                "Focused attribution stays limited to the unique R16 boundary-bearing stream and the heaviest admitted R15 row so R18 can remain optional unless a local repair target is actually isolated.",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "runtime_surface_index.json",
        {
            "experiment": "r17_runtime_surface_index",
            "environment": environment.as_dict(),
            "rows": runtime_surface_index,
        },
    )
    write_json(
        OUT_DIR / "source_surface_runtime_summary.json",
        {
            "experiment": "r17_source_surface_runtime_summary",
            "environment": environment.as_dict(),
            "rows": source_surface_rows,
        },
    )
    write_json(
        OUT_DIR / "family_bridge_summary.json",
        {
            "experiment": "r17_family_bridge_summary",
            "environment": environment.as_dict(),
            "rows": family_rows,
        },
    )
    write_json(
        OUT_DIR / "focused_attribution_selection.json",
        {
            "experiment": "r17_focused_attribution_selection",
            "environment": environment.as_dict(),
            "rows": focused_selection_rows,
        },
    )
    write_json(
        OUT_DIR / "focused_attribution_summary.json",
        {
            "experiment": "r17_focused_attribution_summary",
            "environment": environment.as_dict(),
            "summary": focused_attribution_summary,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r17_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    write_json(
        OUT_DIR / "r18_trigger_assessment.json",
        {
            "experiment": "r17_r18_trigger_assessment",
            "environment": environment.as_dict(),
            "summary": r18_trigger_assessment,
        },
    )
    write_csv(
        OUT_DIR / "runtime_bridge_rows.csv",
        runtime_rows,
        [
            "source_lane",
            "family",
            "baseline_stage",
            "baseline_program_name",
            "baseline_horizon_multiplier",
            "retrieval_horizon_multiplier",
            "program_name",
            "comparison_mode",
            "max_steps",
            "stream_name",
            "boundary_bearing_stream",
            "reference_step_count",
            "profile_repeats",
            "bytecode_ns_per_step",
            "lowered_ns_per_step",
            "linear_ns_per_step",
            "accelerated_ns_per_step",
            "accelerated_speedup_vs_linear",
            "accelerated_ratio_vs_lowered",
            "accelerated_ratio_vs_bytecode",
            "linear_exact_trace_match",
            "linear_exact_final_state_match",
            "accelerated_exact_trace_match",
            "accelerated_exact_final_state_match",
            "linear_accelerated_trace_match",
            "linear_accelerated_final_state_match",
            "read_observation_count",
            "exact_read_agreement",
        ],
    )
    write_csv(
        OUT_DIR / "focused_cost_breakdown_rows.csv",
        focused_rows,
        [
            "selection_rank",
            "focus_reason",
            "source_lane",
            "family",
            "program_name",
            "baseline_program_name",
            "baseline_horizon_multiplier",
            "retrieval_horizon_multiplier",
            "boundary_bearing_stream",
            "max_steps",
            "reference_step_count",
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
            "retrieval_share_of_exact",
            "linear_validation_share_of_retrieval",
            "accelerated_query_share_of_retrieval",
            "exact_vs_lowered_ratio",
            "exact_vs_bytecode_ratio",
            "read_count",
            "stack_read_count",
            "memory_read_count",
            "dominant_exact_component",
            "dominant_component_share",
        ],
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R17 D0 Full-Surface Runtime Bridge",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `runtime_surface_index.json`",
                "- `source_surface_runtime_summary.json`",
                "- `family_bridge_summary.json`",
                "- `runtime_bridge_rows.csv`",
                "- `focused_attribution_selection.json`",
                "- `focused_attribution_summary.json`",
                "- `focused_cost_breakdown_rows.csv`",
                "- `claim_impact.json`",
                "- `r18_trigger_assessment.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
