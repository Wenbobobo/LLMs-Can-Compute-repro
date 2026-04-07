"""Export the bounded post-H26 non-retrieval overhead localization audit for R33."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
import sys
import time
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bytecode import lower_program, run_spec_program, verify_program
from exec_trace import Program, TraceEvent, TraceInterpreter, replay_trace
from model import compare_execution_to_reference
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadObservation,
    ReadStrategy,
    _LatestWriteSpace,
)
from utils import detect_runtime_environment

import export_r23_d0_same_endpoint_systems_overturn_gate as r23


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R33_d0_non_retrieval_overhead_localization_audit"

PROFILE_REPEATS = 3
COMPETITIVE_RATIO_THRESHOLD = 1.10
CONTROL_HEAVY_MIN_READS = 32
COMPONENT_KEYS = (
    "dispatch_decode_seconds",
    "state_update_bookkeeping_seconds",
    "tensor_python_plumbing_seconds",
    "residual_fixed_overhead_seconds",
)


@dataclass(frozen=True, slots=True)
class PointerLikeComponentProfile:
    total_seconds: float
    retrieval_seconds: float
    dispatch_decode_seconds: float
    state_update_bookkeeping_seconds: float
    tensor_python_plumbing_seconds: float
    residual_fixed_overhead_seconds: float
    read_count: int
    memory_read_count: int
    stack_read_count: int

    @property
    def non_retrieval_seconds(self) -> float:
        return (
            self.dispatch_decode_seconds
            + self.state_update_bookkeeping_seconds
            + self.tensor_python_plumbing_seconds
            + self.residual_fixed_overhead_seconds
        )


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def median_or_none(values: list[float]) -> float | None:
    return None if not values else sorted(values)[len(values) // 2]


def median_sample_index(values: list[float]) -> int | None:
    if not values:
        return None
    ordered_indices = sorted(range(len(values)), key=lambda index: (values[index], index))
    return ordered_indices[len(ordered_indices) // 2]


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in {None, 0.0}:
        return None
    return numerator / denominator


def total_pointer_like_reads(row: dict[str, object]) -> int:
    return int(row.get("pointer_like_exact_memory_read_count") or 0) + int(
        row.get("pointer_like_exact_stack_read_count") or 0
    )


def load_inputs() -> dict[str, Any]:
    return {
        "h26_summary": read_json(ROOT / "results" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "summary.json"),
        "h25_summary": read_json(ROOT / "results" / "H25_refreeze_after_r30_r31_decision_packet" / "summary.json"),
        "r31_summary": read_json(
            ROOT / "results" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "summary.json"
        ),
        "r23_summary": read_json(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "summary.json"),
        "r23_runtime_rows": read_json(
            ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "runtime_profile_rows.json"
        ),
        "r28_summary": read_json(ROOT / "results" / "R28_d0_trace_retrieval_contract_audit" / "summary.json"),
    }


def build_case_registry() -> dict[str, object]:
    return {case.program.name: case for case in r23.positive_cases()}


def build_stratified_sample_manifest(r23_runtime_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in r23_runtime_rows:
        grouped[str(row["suite"])].append(row)

    manifest_rows: list[dict[str, object]] = []
    for suite, suite_rows in sorted(grouped.items()):
        suite_rows_sorted = sorted(
            suite_rows,
            key=lambda row: (
                float(row["pointer_like_exact_ratio_vs_best_reference"]),
                str(row["program_name"]),
            ),
        )
        selected: list[tuple[dict[str, object], str, str]] = []
        median_row = suite_rows_sorted[len(suite_rows_sorted) // 2]
        worst_row = suite_rows_sorted[-1]
        selected.append((median_row, "median_ratio", "suite median pointer_like ratio vs best reference"))
        if str(worst_row["program_name"]) != str(median_row["program_name"]):
            selected.append((worst_row, "worst_ratio", "suite worst pointer_like ratio vs best reference"))

        control_candidate = max(
            suite_rows,
            key=lambda row: (
                total_pointer_like_reads(row),
                float(row["pointer_like_exact_ratio_vs_best_reference"]),
                str(row["program_name"]),
            ),
        )
        selected_programs = {str(row["program_name"]) for row, _kind, _reason in selected}
        if (
            total_pointer_like_reads(control_candidate) >= CONTROL_HEAVY_MIN_READS
            and str(control_candidate["program_name"]) not in selected_programs
        ):
            selected.append(
                (
                    control_candidate,
                    "control_heavy_extra",
                    "suite offered a higher-control row outside the median/worst pair",
                )
            )

        for selected_row, selection_class, selection_reason in selected:
            manifest_rows.append(
                {
                    "program_name": selected_row["program_name"],
                    "suite": selected_row["suite"],
                    "comparison_mode": selected_row["comparison_mode"],
                    "max_steps": selected_row["max_steps"],
                    "selection_class": selection_class,
                    "selection_reason": selection_reason,
                    "audit_scope": "stratified_first_pass",
                    "source_pointer_like_ratio_vs_best_reference": selected_row[
                        "pointer_like_exact_ratio_vs_best_reference"
                    ],
                    "source_lowered_ratio_vs_best_reference": selected_row[
                        "lowered_ratio_vs_best_reference"
                    ],
                    "source_pointer_like_read_count": total_pointer_like_reads(selected_row),
                    "source_pointer_like_memory_read_count": selected_row[
                        "pointer_like_exact_memory_read_count"
                    ],
                    "source_pointer_like_stack_read_count": selected_row[
                        "pointer_like_exact_stack_read_count"
                    ],
                    "control_heavy_candidate": total_pointer_like_reads(selected_row)
                    >= CONTROL_HEAVY_MIN_READS,
                }
            )
    return manifest_rows


def build_full_suite_manifest(
    r23_runtime_rows: list[dict[str, object]],
    sample_manifest_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sample_by_program = {str(row["program_name"]): row for row in sample_manifest_rows}
    manifest_rows: list[dict[str, object]] = []
    for row in sorted(r23_runtime_rows, key=lambda item: (str(item["suite"]), str(item["program_name"]))):
        program_name = str(row["program_name"])
        if program_name in sample_by_program:
            manifest_rows.append(
                {
                    **sample_by_program[program_name],
                    "audit_scope": "full_r23_suite_escalation",
                }
            )
            continue
        manifest_rows.append(
            {
                "program_name": row["program_name"],
                "suite": row["suite"],
                "comparison_mode": row["comparison_mode"],
                "max_steps": row["max_steps"],
                "selection_class": "full_suite_escalation",
                "selection_reason": "sample component ranking stayed unstable, so the audit escalated to the full R23 suite",
                "audit_scope": "full_r23_suite_escalation",
                "source_pointer_like_ratio_vs_best_reference": row["pointer_like_exact_ratio_vs_best_reference"],
                "source_lowered_ratio_vs_best_reference": row["lowered_ratio_vs_best_reference"],
                "source_pointer_like_read_count": total_pointer_like_reads(row),
                "source_pointer_like_memory_read_count": row["pointer_like_exact_memory_read_count"],
                "source_pointer_like_stack_read_count": row["pointer_like_exact_stack_read_count"],
                "control_heavy_candidate": total_pointer_like_reads(row) >= CONTROL_HEAVY_MIN_READS,
            }
        )
    return manifest_rows


class ComponentProfiledPointerLikeExecutor(FreeRunningTraceExecutor):
    def __init__(self) -> None:
        super().__init__(
            stack_strategy="pointer_like_exact",
            memory_strategy="pointer_like_exact",
            validate_exact_reads=False,
        )
        self.pointer_like_retrieval_seconds = 0.0

    def run_with_profile(
        self,
        program: Program,
        *,
        max_steps: int = 10_000,
    ) -> tuple[FreeRunningExecutionResult, PointerLikeComponentProfile]:
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
        self.pointer_like_retrieval_seconds = 0.0
        total_started = time.perf_counter()

        while not halted:
            if step >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= pc < len(program)):
                raise RuntimeError(f"Program counter out of range: {pc}")

            instruction = program.instructions[pc]
            dispatch_started = time.perf_counter()
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
            dispatch_seconds += time.perf_counter() - dispatch_started

            bookkeeping_started = time.perf_counter()
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
            bookkeeping_seconds += time.perf_counter() - bookkeeping_started

            step += 1
            pc = next_pc
            stack_depth = event.stack_depth_after

        replay_started = time.perf_counter()
        final_state = replay_trace(program, tuple(events))
        replay_seconds = time.perf_counter() - replay_started
        total_seconds = time.perf_counter() - total_started

        execution = FreeRunningExecutionResult(
            program=program,
            events=tuple(events),
            final_state=final_state,
            read_observations=tuple(read_observations),
            stack_strategy=self.stack_strategy,
            memory_strategy=self.memory_strategy,
        )
        retrieval_seconds = self.pointer_like_retrieval_seconds
        dispatch_decode_seconds = max(0.0, dispatch_seconds - retrieval_seconds)
        residual_fixed_overhead_seconds = max(
            0.0,
            total_seconds - dispatch_seconds - bookkeeping_seconds - replay_seconds,
        )
        profile = PointerLikeComponentProfile(
            total_seconds=total_seconds,
            retrieval_seconds=retrieval_seconds,
            dispatch_decode_seconds=dispatch_decode_seconds,
            state_update_bookkeeping_seconds=bookkeeping_seconds,
            tensor_python_plumbing_seconds=replay_seconds,
            residual_fixed_overhead_seconds=residual_fixed_overhead_seconds,
            read_count=len(read_observations),
            memory_read_count=sum(observation.space == "memory" for observation in read_observations),
            stack_read_count=sum(observation.space == "stack" for observation in read_observations),
        )
        return execution, profile

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
        del scorer
        if strategy != "pointer_like_exact":
            raise RuntimeError(f"Unsupported R33 profiled strategy: {strategy}")
        read_started = time.perf_counter()
        chosen_value = history.read_pointer_like(address)
        self.pointer_like_retrieval_seconds += time.perf_counter() - read_started
        read_observations.append(
            ReadObservation(
                step=step,
                space=space,
                address=address,
                source=strategy,
                chosen_value=chosen_value,
                linear_value=chosen_value,
                accelerated_value=chosen_value,
            )
        )
        return chosen_value


def profile_pointer_like_exact(lowered_program: Program, *, max_steps: int) -> dict[str, object]:
    reference = r23.reference_execution(lowered_program, max_steps=max_steps)
    total_seconds_samples: list[float] = []
    retrieval_seconds_samples: list[float] = []
    dispatch_decode_seconds_samples: list[float] = []
    bookkeeping_seconds_samples: list[float] = []
    plumbing_seconds_samples: list[float] = []
    residual_seconds_samples: list[float] = []
    non_retrieval_seconds_samples: list[float] = []
    read_count_samples: list[int] = []
    memory_read_samples: list[int] = []
    stack_read_samples: list[int] = []
    profile_samples: list[PointerLikeComponentProfile] = []
    execution_samples: list[FreeRunningExecutionResult] = []
    last_execution: FreeRunningExecutionResult | None = None
    error: Exception | None = None

    for _ in range(PROFILE_REPEATS):
        executor = ComponentProfiledPointerLikeExecutor()
        try:
            execution, profile = executor.run_with_profile(lowered_program, max_steps=max_steps)
        except Exception as exc:  # pragma: no cover - exporter runtime path
            error = exc
            break
        last_execution = execution
        execution_samples.append(execution)
        profile_samples.append(profile)
        total_seconds_samples.append(profile.total_seconds)
        retrieval_seconds_samples.append(profile.retrieval_seconds)
        dispatch_decode_seconds_samples.append(profile.dispatch_decode_seconds)
        bookkeeping_seconds_samples.append(profile.state_update_bookkeeping_seconds)
        plumbing_seconds_samples.append(profile.tensor_python_plumbing_seconds)
        residual_seconds_samples.append(profile.residual_fixed_overhead_seconds)
        non_retrieval_seconds_samples.append(profile.non_retrieval_seconds)
        read_count_samples.append(profile.read_count)
        memory_read_samples.append(profile.memory_read_count)
        stack_read_samples.append(profile.stack_read_count)

    if last_execution is None:
        return {
            "median_seconds": median_or_none(total_seconds_samples),
            "retrieval_seconds": median_or_none(retrieval_seconds_samples),
            "non_retrieval_seconds": median_or_none(non_retrieval_seconds_samples),
            "dispatch_decode_seconds": median_or_none(dispatch_decode_seconds_samples),
            "state_update_bookkeeping_seconds": median_or_none(bookkeeping_seconds_samples),
            "tensor_python_plumbing_seconds": median_or_none(plumbing_seconds_samples),
            "residual_fixed_overhead_seconds": median_or_none(residual_seconds_samples),
            "exact": False,
            "exact_trace_match": False,
            "exact_final_state_match": False,
            "first_mismatch_step": None,
            "failure_reason": None if error is None else f"{type(error).__name__}: {error}",
            "read_observation_count": median_or_none([float(value) for value in read_count_samples]),
            "memory_read_count": median_or_none([float(value) for value in memory_read_samples]),
            "stack_read_count": median_or_none([float(value) for value in stack_read_samples]),
            "component_total_matches_non_retrieval": False,
            "component_reconstruction_error_seconds": None,
            "dominant_non_retrieval_component": None,
        }

    representative_index = median_sample_index(non_retrieval_seconds_samples)
    if representative_index is None:
        representative_index = median_sample_index(total_seconds_samples)
    assert representative_index is not None
    representative_profile = profile_samples[representative_index]
    representative_execution = execution_samples[representative_index]

    outcome = compare_execution_to_reference(lowered_program, representative_execution, reference=reference)
    total_seconds = representative_profile.total_seconds
    retrieval_seconds = representative_profile.retrieval_seconds
    non_retrieval_seconds = representative_profile.non_retrieval_seconds
    dispatch_decode_seconds = representative_profile.dispatch_decode_seconds
    bookkeeping_seconds = representative_profile.state_update_bookkeeping_seconds
    plumbing_seconds = representative_profile.tensor_python_plumbing_seconds
    residual_seconds = representative_profile.residual_fixed_overhead_seconds
    component_rows = {
        "dispatch_decode_seconds": dispatch_decode_seconds,
        "state_update_bookkeeping_seconds": bookkeeping_seconds,
        "tensor_python_plumbing_seconds": plumbing_seconds,
        "residual_fixed_overhead_seconds": residual_seconds,
    }
    reconstructed_non_retrieval = sum(
        float(value) for value in component_rows.values() if value is not None
    )
    reconstruction_error = abs(reconstructed_non_retrieval - non_retrieval_seconds)
    component_total_matches_non_retrieval = reconstruction_error <= max(1e-12, non_retrieval_seconds * 1e-9)
    dominant_non_retrieval_component = None
    if component_rows:
        dominant_non_retrieval_component = max(
            component_rows.items(),
            key=lambda item: -1.0 if item[1] is None else float(item[1]),
        )[0]

    return {
        "median_seconds": total_seconds,
        "retrieval_seconds": retrieval_seconds,
        "non_retrieval_seconds": non_retrieval_seconds,
        "dispatch_decode_seconds": dispatch_decode_seconds,
        "state_update_bookkeeping_seconds": bookkeeping_seconds,
        "tensor_python_plumbing_seconds": plumbing_seconds,
        "residual_fixed_overhead_seconds": residual_seconds,
        "exact": bool(outcome.exact_trace_match and outcome.exact_final_state_match and outcome.failure_reason is None),
        "exact_trace_match": outcome.exact_trace_match,
        "exact_final_state_match": outcome.exact_final_state_match,
        "first_mismatch_step": outcome.first_mismatch_step,
        "failure_reason": outcome.failure_reason,
        "read_observation_count": float(representative_profile.read_count),
        "memory_read_count": float(representative_profile.memory_read_count),
        "stack_read_count": float(representative_profile.stack_read_count),
        "component_total_matches_non_retrieval": component_total_matches_non_retrieval,
        "component_reconstruction_error_seconds": reconstruction_error,
        "dominant_non_retrieval_component": dominant_non_retrieval_component,
    }


def execute_component_audit(
    manifest_rows: list[dict[str, object]],
    case_registry: dict[str, object],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for manifest_row in manifest_rows:
        program_name = str(manifest_row["program_name"])
        case = case_registry.get(program_name)
        if case is None:
            raise RuntimeError(f"R33 missing case registry entry for {program_name}.")

        verification = verify_program(case.program)
        lowered_program = lower_program(case.program)
        spec_seconds, _spec_samples, _spec_result, spec_error = r23.profile_callable(
            lambda case=case: run_spec_program(case.program, max_steps=case.max_steps),
            repeats=PROFILE_REPEATS,
        )
        lowered_seconds, _lowered_samples, _lowered_result, lowered_error = r23.profile_callable(
            lambda lowered_program=lowered_program, case=case: TraceInterpreter().run(
                lowered_program,
                max_steps=case.max_steps,
            ),
            repeats=PROFILE_REPEATS,
        )
        exact_profile = profile_pointer_like_exact(lowered_program, max_steps=case.max_steps)
        best_reference_candidates = {
            "spec_reference": spec_seconds,
            "lowered_exec_trace": lowered_seconds,
        }
        best_reference_id, best_reference_seconds = min(
            (
                (comparator_id, seconds)
                for comparator_id, seconds in best_reference_candidates.items()
                if seconds is not None
            ),
            key=lambda item: float(item[1]),
        )

        row = {
            **manifest_row,
            "verification_passed": bool(verification.passed),
            "spec_reference_seconds": spec_seconds,
            "spec_reference_error": None if spec_error is None else f"{type(spec_error).__name__}: {spec_error}",
            "lowered_exec_trace_seconds": lowered_seconds,
            "lowered_exec_trace_error": None
            if lowered_error is None
            else f"{type(lowered_error).__name__}: {lowered_error}",
            "pointer_like_exact_seconds": exact_profile["median_seconds"],
            "pointer_like_exact_exact": exact_profile["exact"],
            "pointer_like_exact_exact_trace_match": exact_profile["exact_trace_match"],
            "pointer_like_exact_exact_final_state_match": exact_profile["exact_final_state_match"],
            "pointer_like_exact_first_mismatch_step": exact_profile["first_mismatch_step"],
            "pointer_like_exact_failure_reason": exact_profile["failure_reason"],
            "pointer_like_exact_read_observation_count": int(
                exact_profile["read_observation_count"] or 0
            ),
            "pointer_like_exact_memory_read_count": int(
                exact_profile["memory_read_count"] or 0
            ),
            "pointer_like_exact_stack_read_count": int(
                exact_profile["stack_read_count"] or 0
            ),
            "retrieval_seconds": exact_profile["retrieval_seconds"],
            "non_retrieval_seconds": exact_profile["non_retrieval_seconds"],
            "dispatch_decode_seconds": exact_profile["dispatch_decode_seconds"],
            "state_update_bookkeeping_seconds": exact_profile["state_update_bookkeeping_seconds"],
            "tensor_python_plumbing_seconds": exact_profile["tensor_python_plumbing_seconds"],
            "residual_fixed_overhead_seconds": exact_profile["residual_fixed_overhead_seconds"],
            "component_total_matches_non_retrieval": exact_profile["component_total_matches_non_retrieval"],
            "component_reconstruction_error_seconds": exact_profile["component_reconstruction_error_seconds"],
            "dominant_non_retrieval_component": exact_profile["dominant_non_retrieval_component"],
            "pointer_like_non_retrieval_share": safe_ratio(
                exact_profile["non_retrieval_seconds"],
                exact_profile["median_seconds"],
            ),
            "pointer_like_retrieval_share": safe_ratio(
                exact_profile["retrieval_seconds"],
                exact_profile["median_seconds"],
            ),
            "pointer_like_ratio_vs_spec_reference": safe_ratio(
                exact_profile["median_seconds"],
                spec_seconds,
            ),
            "pointer_like_ratio_vs_lowered_exec_trace": safe_ratio(
                exact_profile["median_seconds"],
                lowered_seconds,
            ),
            "pointer_like_ratio_vs_best_reference": safe_ratio(
                exact_profile["median_seconds"],
                best_reference_seconds,
            ),
            "best_reference_id": best_reference_id,
            "best_reference_seconds": best_reference_seconds,
        }
        rows.append(row)
    return rows


def build_suite_component_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["suite"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for suite, suite_rows in sorted(grouped.items()):
        dominant_counter = Counter(str(row["dominant_non_retrieval_component"]) for row in suite_rows)
        dominant_counter.pop("None", None)
        dominant_component = None
        component_ranking_stable = False
        if dominant_counter:
            top_component, top_count = dominant_counter.most_common(1)[0]
            second_count = dominant_counter.most_common(2)[1][1] if len(dominant_counter) > 1 else 0
            dominant_component = top_component
            component_ranking_stable = top_count > second_count
        summary_rows.append(
            {
                "suite": suite,
                "case_count": len(suite_rows),
                "exact_case_count": sum(bool(row["pointer_like_exact_exact"]) for row in suite_rows),
                "component_accounting_match_count": sum(
                    bool(row["component_total_matches_non_retrieval"]) for row in suite_rows
                ),
                "median_pointer_like_ratio_vs_spec_reference": median_or_none(
                    [
                        float(row["pointer_like_ratio_vs_spec_reference"])
                        for row in suite_rows
                        if row["pointer_like_ratio_vs_spec_reference"] is not None
                    ]
                ),
                "median_pointer_like_ratio_vs_lowered_exec_trace": median_or_none(
                    [
                        float(row["pointer_like_ratio_vs_lowered_exec_trace"])
                        for row in suite_rows
                        if row["pointer_like_ratio_vs_lowered_exec_trace"] is not None
                    ]
                ),
                "median_retrieval_seconds": median_or_none(
                    [float(row["retrieval_seconds"]) for row in suite_rows if row["retrieval_seconds"] is not None]
                ),
                "median_non_retrieval_seconds": median_or_none(
                    [
                        float(row["non_retrieval_seconds"])
                        for row in suite_rows
                        if row["non_retrieval_seconds"] is not None
                    ]
                ),
                "median_pointer_like_non_retrieval_share": median_or_none(
                    [
                        float(row["pointer_like_non_retrieval_share"])
                        for row in suite_rows
                        if row["pointer_like_non_retrieval_share"] is not None
                    ]
                ),
                "component_counts": [
                    {"component": component, "count": count}
                    for component, count in sorted(dominant_counter.items())
                ],
                "suite_dominant_component": dominant_component,
                "component_ranking_stable": component_ranking_stable,
            }
        )
    return summary_rows


def build_comparator_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    dominant_counter = Counter(str(row["dominant_non_retrieval_component"]) for row in rows)
    dominant_counter.pop("None", None)
    return [
        {
            "comparator_id": "spec_reference",
            "case_count": len(rows),
            "exact_case_count": sum(bool(row.get("verification_passed")) for row in rows),
            "median_seconds": median_or_none(
                [float(row["spec_reference_seconds"]) for row in rows if row.get("spec_reference_seconds") is not None]
            ),
            "median_ratio_vs_spec_reference": 1.0,
            "median_ratio_vs_lowered_exec_trace": median_or_none(
                [
                    safe_ratio(
                        float(row["spec_reference_seconds"]),
                        float(row["lowered_exec_trace_seconds"]),
                    )
                    for row in rows
                    if row.get("spec_reference_seconds") is not None
                    and row.get("lowered_exec_trace_seconds") is not None
                ]
            ),
        },
        {
            "comparator_id": "lowered_exec_trace",
            "case_count": len(rows),
            "exact_case_count": sum(row.get("lowered_exec_trace_error") is None for row in rows),
            "median_seconds": median_or_none(
                [
                    float(row["lowered_exec_trace_seconds"])
                    for row in rows
                    if row.get("lowered_exec_trace_seconds") is not None
                ]
            ),
            "median_ratio_vs_spec_reference": median_or_none(
                [
                    safe_ratio(
                        float(row["lowered_exec_trace_seconds"]),
                        float(row["spec_reference_seconds"]),
                    )
                    for row in rows
                    if row.get("lowered_exec_trace_seconds") is not None
                    and row.get("spec_reference_seconds") is not None
                ]
            ),
            "median_ratio_vs_lowered_exec_trace": 1.0,
        },
        {
            "comparator_id": "pointer_like_exact",
            "case_count": len(rows),
            "exact_case_count": sum(bool(row["pointer_like_exact_exact"]) for row in rows),
            "median_seconds": median_or_none(
                [
                    float(row["pointer_like_exact_seconds"])
                    for row in rows
                    if row["pointer_like_exact_seconds"] is not None
                ]
            ),
            "median_ratio_vs_spec_reference": median_or_none(
                [
                    float(row["pointer_like_ratio_vs_spec_reference"])
                    for row in rows
                    if row["pointer_like_ratio_vs_spec_reference"] is not None
                ]
            ),
            "median_ratio_vs_lowered_exec_trace": median_or_none(
                [
                    float(row["pointer_like_ratio_vs_lowered_exec_trace"])
                    for row in rows
                    if row["pointer_like_ratio_vs_lowered_exec_trace"] is not None
                ]
            ),
            "median_non_retrieval_share": median_or_none(
                [
                    float(row["pointer_like_non_retrieval_share"])
                    for row in rows
                    if row["pointer_like_non_retrieval_share"] is not None
                ]
            ),
            "dominant_component_counts": [
                {"component": component, "count": count}
                for component, count in sorted(dominant_counter.items(), key=lambda item: (-item[1], item[0]))
            ],
        },
    ]


def should_escalate_to_full_suite(suite_summary_rows: list[dict[str, object]]) -> bool:
    dominant_components = {
        str(row["suite_dominant_component"])
        for row in suite_summary_rows
        if row["suite_dominant_component"] is not None
    }
    return any(not bool(row["component_ranking_stable"]) for row in suite_summary_rows) or len(
        dominant_components
    ) > 1


def assess_attribution_gate(
    rows: list[dict[str, object]],
    *,
    suite_summary_rows: list[dict[str, object]],
    comparator_summary_rows: list[dict[str, object]],
    audit_scope: str,
) -> dict[str, object]:
    exact_case_count = sum(bool(row["pointer_like_exact_exact"]) for row in rows)
    component_accounting_match_count = sum(
        bool(row["component_total_matches_non_retrieval"]) for row in rows
    )
    pointer_like_summary = next(
        row for row in comparator_summary_rows if str(row["comparator_id"]) == "pointer_like_exact"
    )
    dominant_components = {
        str(row["suite_dominant_component"])
        for row in suite_summary_rows
        if row["suite_dominant_component"] is not None
    }
    suites_same_dominant_component = len(dominant_components) == 1 and len(suite_summary_rows) > 0
    suites_noncompetitive_against_spec = all(
        row["median_pointer_like_ratio_vs_spec_reference"] is not None
        and float(row["median_pointer_like_ratio_vs_spec_reference"]) > COMPETITIVE_RATIO_THRESHOLD
        for row in suite_summary_rows
    )

    if exact_case_count != len(rows):
        lane_verdict = "instrumentation_blocked_without_scope_drift"
        reason = (
            "At least one bounded R33 row lost exactness under component profiling, so the systems audit cannot"
            " support a stronger same-endpoint recovery claim."
        )
    elif component_accounting_match_count != len(rows):
        lane_verdict = "instrumentation_blocked_without_scope_drift"
        reason = (
            "The bounded R33 component accounting did not reconstruct the current non-retrieval bucket"
            " stably enough to support a localization claim."
        )
    elif suites_same_dominant_component and suites_noncompetitive_against_spec:
        lane_verdict = "suite_stable_noncompetitive_after_localization"
        reason = (
            "One non-retrieval component now dominates every audited suite, and pointer-like exact remains"
            " noncompetitive against the fixed same-endpoint references."
        )
    elif suites_same_dominant_component:
        lane_verdict = "non_retrieval_overhead_localized"
        reason = (
            "One non-retrieval component dominates every audited suite inside the bounded R33 attribution packet."
        )
    else:
        lane_verdict = "non_retrieval_overhead_still_aggregate_only"
        reason = (
            "The bounded R33 audit preserved exactness, but component rankings remained unstable across suites."
        )

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
        "audit_scope": audit_scope,
        "planned_case_count": len(rows),
        "executed_case_count": len(rows),
        "exact_case_count": exact_case_count,
        "component_accounting_match_count": component_accounting_match_count,
        "suite_count": len(suite_summary_rows),
        "stable_suite_component_count": sum(bool(row["component_ranking_stable"]) for row in suite_summary_rows),
        "global_dominant_component": None
        if not pointer_like_summary["dominant_component_counts"]
        else pointer_like_summary["dominant_component_counts"][0]["component"],
        "suites_same_dominant_component": suites_same_dominant_component,
        "next_priority_lane": "h27_refreeze_after_r32_r33_same_endpoint_decision",
    }


def build_summary(
    inputs: dict[str, Any],
    *,
    manifest_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    suite_summary_rows: list[dict[str, object]],
    comparator_summary_rows: list[dict[str, object]],
    gate: dict[str, object],
) -> dict[str, object]:
    return {
        "status": "r33_non_retrieval_overhead_localization_complete",
        "current_frozen_stage": "h26_refreeze_after_r32_boundary_sharp_zoom",
        "prior_operational_stage": "h25_refreeze_after_r30_r31_decision_packet",
        "source_systems_reauthorization_stage": "r31_d0_same_endpoint_systems_recovery_reauthorization_packet",
        "gate": gate,
        "selected_suite_count": len({str(row["suite"]) for row in manifest_rows}),
        "executed_program_count": len(component_rows),
        "component_targets": list(COMPONENT_KEYS),
        "comparator_set": [
            "spec_reference",
            "lowered_exec_trace",
            "pointer_like_exact",
        ],
        "recommended_next_action": "Freeze the R33 outcome into H27 before considering any new plan-mode routing.",
        "supported_here": [
            "R33 stays on the current positive D0 suite and keeps the comparator set fixed.",
            f"R33 executed {gate['executed_case_count']} bounded rows under audit scope `{gate['audit_scope']}`.",
            "R33 decomposes pointer_like_exact non-retrieval time into dispatch/decode, bookkeeping, python plumbing, and residual fixed overhead.",
        ],
        "unsupported_here": [
            "R33 does not widen endpoint scope, suite scope, or comparator scope by momentum.",
            "R33 does not authorize direct R29 activation by itself.",
            "R33 does not convert a component-localization result into a broader frontier claim.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    case_registry = build_case_registry()
    sample_manifest_rows = build_stratified_sample_manifest(inputs["r23_runtime_rows"]["rows"])
    sample_component_rows = execute_component_audit(sample_manifest_rows, case_registry)
    sample_suite_summary_rows = build_suite_component_summary(sample_component_rows)
    if should_escalate_to_full_suite(sample_suite_summary_rows):
        manifest_rows = build_full_suite_manifest(inputs["r23_runtime_rows"]["rows"], sample_manifest_rows)
        component_rows = execute_component_audit(manifest_rows, case_registry)
    else:
        manifest_rows = sample_manifest_rows
        component_rows = sample_component_rows
    suite_summary_rows = build_suite_component_summary(component_rows)
    comparator_summary_rows = build_comparator_summary(component_rows)
    gate = assess_attribution_gate(
        component_rows,
        suite_summary_rows=suite_summary_rows,
        comparator_summary_rows=comparator_summary_rows,
        audit_scope=str(manifest_rows[0]["audit_scope"]) if manifest_rows else "empty",
    )
    summary = build_summary(
        inputs,
        manifest_rows=manifest_rows,
        component_rows=component_rows,
        suite_summary_rows=suite_summary_rows,
        comparator_summary_rows=comparator_summary_rows,
        gate=gate,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "sample_manifest.json",
        {"experiment": "r33_sample_manifest", "environment": environment.as_dict(), "rows": manifest_rows},
    )
    write_json(
        OUT_DIR / "component_profile_rows.json",
        {"experiment": "r33_component_profile_rows", "environment": environment.as_dict(), "rows": component_rows},
    )
    write_csv(OUT_DIR / "component_profile_rows.csv", component_rows)
    write_json(
        OUT_DIR / "suite_component_summary.json",
        {"experiment": "r33_suite_component_summary", "environment": environment.as_dict(), "rows": suite_summary_rows},
    )
    write_json(
        OUT_DIR / "comparator_summary.json",
        {"experiment": "r33_comparator_summary", "environment": environment.as_dict(), "rows": comparator_summary_rows},
    )
    write_json(
        OUT_DIR / "attribution_verdict.json",
        {"experiment": "r33_attribution_verdict", "environment": environment.as_dict(), "summary": gate},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r33_d0_non_retrieval_overhead_localization_audit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json",
                "results/H25_refreeze_after_r30_r31_decision_packet/summary.json",
                "results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json",
                "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json",
                "results/R23_d0_same_endpoint_systems_overturn_gate/runtime_profile_rows.json",
                "results/R28_d0_trace_retrieval_contract_audit/summary.json",
                "docs/milestones/R33_d0_non_retrieval_overhead_localization_audit/component_localization_manifest.md",
                "src/model/free_running_executor.py",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R33 D0 Non-Retrieval Overhead Localization Audit\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `sample_manifest.json`\n"
        "- `component_profile_rows.json`\n"
        "- `component_profile_rows.csv`\n"
        "- `suite_component_summary.json`\n"
        "- `comparator_summary.json`\n"
        "- `attribution_verdict.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
