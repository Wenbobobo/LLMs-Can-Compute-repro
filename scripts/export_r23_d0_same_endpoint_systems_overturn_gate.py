"""Export the post-R22 same-endpoint systems overturn gate for R23."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import json
from pathlib import Path
from statistics import median
import time
from typing import Any, Callable

from bytecode import (
    BytecodeInterpreter,
    harness_cases,
    lower_program,
    run_spec_program,
    stress_reference_cases,
    verify_program,
)
from exec_trace import Program, TraceInterpreter
from model import compare_execution_to_reference
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadObservation,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate"
PROFILE_REPEATS = 3
COMPETITIVE_RATIO_THRESHOLD = 1.10


@dataclass(frozen=True, slots=True)
class StrategySpec:
    strategy_id: str
    stack_strategy: str
    memory_strategy: str


LINEAR_EXACT = StrategySpec("linear_exact", "linear", "linear")
ACCELERATED = StrategySpec("accelerated", "accelerated", "accelerated")
POINTER_LIKE_EXACT = StrategySpec("pointer_like_exact", "pointer_like_exact", "pointer_like_exact")
EXACT_STRATEGIES: tuple[StrategySpec, ...] = (
    LINEAR_EXACT,
    ACCELERATED,
    POINTER_LIKE_EXACT,
)


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def relative_path(path: str | Path) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def median_or_none(values: list[float]) -> float | None:
    return median(values) if values else None


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in {None, 0.0}:
        return None
    return numerator / denominator


def positive_cases():
    harness_positive_cases = [case for case in harness_cases() if case.comparison_mode != "verifier_negative"]
    stress_positive_cases = [
        case
        for case in stress_reference_cases()
        if case.comparison_mode in {"medium_exact_trace", "long_exact_final_state"}
    ]
    return [*harness_positive_cases, *stress_positive_cases]


def profile_callable(
    fn: Callable[[], Any],
    *,
    repeats: int = PROFILE_REPEATS,
) -> tuple[float, list[float], Any, Exception | None]:
    samples: list[float] = []
    last_result: Any = None
    error: Exception | None = None
    for _ in range(repeats):
        started = time.perf_counter()
        try:
            last_result = fn()
        except Exception as exc:  # pragma: no cover - exercised in exporter runs
            error = exc
            last_result = None
        elapsed = time.perf_counter() - started
        samples.append(elapsed)
        if error is not None:
            break
    return median(samples), samples, last_result, error


def reference_execution(program: Program, *, max_steps: int) -> FreeRunningExecutionResult:
    reference = TraceInterpreter().run(program, max_steps=max_steps)
    return FreeRunningExecutionResult(
        program=program,
        events=reference.events,
        final_state=reference.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


class ProfiledStrategyExecutor(FreeRunningTraceExecutor):
    """Measure chosen retrieval time without changing shared executor behavior."""

    def __init__(self, *, strategy: StrategySpec) -> None:
        super().__init__(
            stack_strategy=strategy.stack_strategy,  # type: ignore[arg-type]
            memory_strategy=strategy.memory_strategy,  # type: ignore[arg-type]
            validate_exact_reads=False,
        )
        self.retrieval_seconds = 0.0

    def run_profiled(self, program: Program, *, max_steps: int) -> tuple[FreeRunningExecutionResult, float]:
        self.retrieval_seconds = 0.0
        started = time.perf_counter()
        execution = super().run(program, max_steps=max_steps)
        total_seconds = time.perf_counter() - started
        return execution, total_seconds

    def _read_from_space(
        self,
        *,
        step: int,
        address: int,
        space,
        strategy,
        history,
        scorer,
        read_observations: list[ReadObservation],
    ) -> int:
        del scorer
        read_started = time.perf_counter()
        if strategy == "linear":
            chosen_value = history.read_linear(address)
        elif strategy == "accelerated":
            chosen_value = history.read_accelerated(address)
        elif strategy == "pointer_like_exact":
            chosen_value = history.read_pointer_like(address)
        else:  # pragma: no cover - guarded by exporter configuration
            raise RuntimeError(f"Unsupported profiled R23 strategy: {strategy}")
        self.retrieval_seconds += time.perf_counter() - read_started
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


def profile_exact_strategy(
    lowered_program: Program,
    *,
    max_steps: int,
    strategy: StrategySpec,
    reference: FreeRunningExecutionResult,
) -> dict[str, object]:
    samples: list[float] = []
    retrieval_samples: list[float] = []
    non_retrieval_samples: list[float] = []
    last_execution: FreeRunningExecutionResult | None = None
    error: Exception | None = None

    for _ in range(PROFILE_REPEATS):
        executor = ProfiledStrategyExecutor(strategy=strategy)
        try:
            execution, total_seconds = executor.run_profiled(lowered_program, max_steps=max_steps)
            last_execution = execution
        except Exception as exc:  # pragma: no cover - exercised in exporter runs
            error = exc
            total_seconds = 0.0
        retrieval_seconds = executor.retrieval_seconds
        samples.append(total_seconds)
        retrieval_samples.append(retrieval_seconds)
        non_retrieval_samples.append(max(0.0, total_seconds - retrieval_seconds))
        if error is not None:
            break

    if last_execution is None:
        return {
            "median_seconds": median(samples) if samples else None,
            "samples": samples,
            "ns_per_step": None,
            "exact": False,
            "exact_trace_match": False,
            "exact_final_state_match": False,
            "first_mismatch_step": None,
            "failure_reason": f"{type(error).__name__}: {error}" if error is not None else None,
            "read_observation_count": 0,
            "memory_read_count": 0,
            "stack_read_count": 0,
            "retrieval_seconds": median(retrieval_samples) if retrieval_samples else None,
            "non_retrieval_seconds": median(non_retrieval_samples) if non_retrieval_samples else None,
            "retrieval_share": None,
            "ns_per_read": None,
            "dominant_component": None,
        }

    outcome = compare_execution_to_reference(lowered_program, last_execution, reference=reference)
    program_steps = max(1, int(outcome.program_steps))
    read_observation_count = len(last_execution.read_observations)
    memory_read_count = sum(observation.space == "memory" for observation in last_execution.read_observations)
    stack_read_count = sum(observation.space == "stack" for observation in last_execution.read_observations)
    median_seconds = median(samples)
    retrieval_seconds = median(retrieval_samples)
    non_retrieval_seconds = median(non_retrieval_samples)
    dominant_component = "retrieval_total" if retrieval_seconds >= non_retrieval_seconds else "non_retrieval"
    return {
        "median_seconds": median_seconds,
        "samples": samples,
        "ns_per_step": (median_seconds / program_steps) * 1e9,
        "exact": bool(outcome.exact_trace_match and outcome.exact_final_state_match and outcome.failure_reason is None),
        "exact_trace_match": outcome.exact_trace_match,
        "exact_final_state_match": outcome.exact_final_state_match,
        "first_mismatch_step": outcome.first_mismatch_step,
        "failure_reason": outcome.failure_reason,
        "read_observation_count": read_observation_count,
        "memory_read_count": memory_read_count,
        "stack_read_count": stack_read_count,
        "retrieval_seconds": retrieval_seconds,
        "non_retrieval_seconds": non_retrieval_seconds,
        "retrieval_share": safe_ratio(retrieval_seconds, median_seconds),
        "ns_per_read": None if read_observation_count == 0 else (retrieval_seconds / read_observation_count) * 1e9,
        "dominant_component": dominant_component,
    }


def load_inputs() -> dict[str, Any]:
    return {
        "r2_summary": read_json(ROOT / "results" / "R2_systems_baseline_gate" / "summary.json"),
        "e1b_summary": read_json(ROOT / "results" / "E1b_systems_patch" / "summary.json"),
        "r22_summary": read_json(ROOT / "results" / "R22_d0_true_boundary_localization_gate" / "summary.json"),
    }


def measure_case(case) -> dict[str, object]:
    verification_started = time.perf_counter()
    verification = verify_program(case.program)
    verification_seconds = time.perf_counter() - verification_started

    lowering_started = time.perf_counter()
    lowered_program = lower_program(case.program)
    lowering_seconds = time.perf_counter() - lowering_started

    bytecode_seconds, bytecode_samples, bytecode_result, bytecode_error = profile_callable(
        lambda case=case: BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
    )
    lowered_seconds, lowered_samples, lowered_result, lowered_error = profile_callable(
        lambda lowered_program=lowered_program, case=case: TraceInterpreter().run(
            lowered_program,
            max_steps=case.max_steps,
        )
    )
    spec_seconds, spec_samples, spec_result, spec_error = profile_callable(
        lambda case=case: run_spec_program(case.program, max_steps=case.max_steps)
    )

    reference = reference_execution(lowered_program, max_steps=case.max_steps)
    bytecode_step_count = None if bytecode_result is None else int(bytecode_result.final_state.steps)
    lowered_step_count = int(reference.final_state.steps)
    spec_step_count = None if spec_result is None else int(spec_result.final_state.steps)
    profile_step_count = max(
        value
        for value in (bytecode_step_count, lowered_step_count, spec_step_count)
        if value is not None
    )
    bytecode_ns_per_step = None if bytecode_step_count is None else (bytecode_seconds / bytecode_step_count) * 1e9
    lowered_ns_per_step = (lowered_seconds / lowered_step_count) * 1e9
    spec_ns_per_step = None if spec_step_count is None else (spec_seconds / spec_step_count) * 1e9

    best_reference_candidates = [
        ("bytecode_reference", bytecode_ns_per_step),
        ("spec_reference", spec_ns_per_step),
    ]
    best_reference_path, best_reference_ns_per_step = min(
        ((path, value) for path, value in best_reference_candidates if value is not None),
        key=lambda item: item[1],
    )

    exact_profiles = {
        strategy.strategy_id: profile_exact_strategy(
            lowered_program,
            max_steps=case.max_steps,
            strategy=strategy,
            reference=reference,
        )
        for strategy in EXACT_STRATEGIES
    }

    row: dict[str, object] = {
        "program_name": case.program.name,
        "suite": case.suite,
        "comparison_mode": case.comparison_mode,
        "max_steps": case.max_steps,
        "verification_passed": bool(verification.passed),
        "verification_seconds": verification_seconds,
        "lowering_seconds": lowering_seconds,
        "profile_step_count": profile_step_count,
        "bytecode_median_seconds": bytecode_seconds,
        "bytecode_samples": bytecode_samples,
        "bytecode_ns_per_step": bytecode_ns_per_step,
        "bytecode_error": None if bytecode_error is None else f"{type(bytecode_error).__name__}: {bytecode_error}",
        "lowered_median_seconds": lowered_seconds,
        "lowered_samples": lowered_samples,
        "lowered_ns_per_step": lowered_ns_per_step,
        "lowered_error": None if lowered_error is None else f"{type(lowered_error).__name__}: {lowered_error}",
        "spec_median_seconds": spec_seconds,
        "spec_samples": spec_samples,
        "spec_ns_per_step": spec_ns_per_step,
        "spec_error": None if spec_error is None else f"{type(spec_error).__name__}: {spec_error}",
        "best_reference_path": best_reference_path,
        "best_reference_ns_per_step": best_reference_ns_per_step,
        "bytecode_exact": bool(verification.passed),
        "lowered_exact": bool(verification.passed and lowered_error is None),
        "spec_exact": bool(verification.passed and spec_error is None),
        "bytecode_ratio_vs_best_reference": safe_ratio(bytecode_ns_per_step, best_reference_ns_per_step),
        "lowered_ratio_vs_best_reference": safe_ratio(lowered_ns_per_step, best_reference_ns_per_step),
        "spec_ratio_vs_best_reference": safe_ratio(spec_ns_per_step, best_reference_ns_per_step),
    }

    for strategy_id, profile in exact_profiles.items():
        prefix = strategy_id
        row[f"{prefix}_median_seconds"] = profile["median_seconds"]
        row[f"{prefix}_samples"] = profile["samples"]
        row[f"{prefix}_ns_per_step"] = profile["ns_per_step"]
        row[f"{prefix}_exact"] = profile["exact"]
        row[f"{prefix}_exact_trace_match"] = profile["exact_trace_match"]
        row[f"{prefix}_exact_final_state_match"] = profile["exact_final_state_match"]
        row[f"{prefix}_first_mismatch_step"] = profile["first_mismatch_step"]
        row[f"{prefix}_failure_reason"] = profile["failure_reason"]
        row[f"{prefix}_read_observation_count"] = profile["read_observation_count"]
        row[f"{prefix}_memory_read_count"] = profile["memory_read_count"]
        row[f"{prefix}_stack_read_count"] = profile["stack_read_count"]
        row[f"{prefix}_retrieval_seconds"] = profile["retrieval_seconds"]
        row[f"{prefix}_non_retrieval_seconds"] = profile["non_retrieval_seconds"]
        row[f"{prefix}_retrieval_share"] = profile["retrieval_share"]
        row[f"{prefix}_ns_per_read"] = profile["ns_per_read"]
        row[f"{prefix}_dominant_component"] = profile["dominant_component"]
        row[f"{prefix}_ratio_vs_best_reference"] = safe_ratio(
            profile["ns_per_step"], best_reference_ns_per_step
        )

    row["pointer_like_speedup_vs_accelerated"] = safe_ratio(
        row["accelerated_ns_per_step"],
        row["pointer_like_exact_ns_per_step"],
    )
    row["pointer_like_speedup_vs_lowered"] = safe_ratio(
        row["lowered_ns_per_step"],
        row["pointer_like_exact_ns_per_step"],
    )
    return row


def build_strategy_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    strategy_specs = [
        ("bytecode_reference", "reference_path", "bytecode"),
        ("spec_reference", "reference_path", "spec"),
        ("lowered_exec_trace", "lowered_baseline", "lowered"),
        ("linear_exact", "same_endpoint_exact_candidate", "linear_exact"),
        ("accelerated", "same_endpoint_exact_candidate", "accelerated"),
        ("pointer_like_exact", "same_endpoint_exact_candidate", "pointer_like_exact"),
    ]
    summary_rows: list[dict[str, object]] = []
    for strategy_id, control_class, prefix in strategy_specs:
        exact_key = "verification_passed" if prefix in {"bytecode", "spec", "lowered"} else f"{prefix}_exact"
        ns_key = f"{prefix}_ns_per_step"
        ratio_key = "lowered_ratio_vs_best_reference" if prefix == "lowered" else f"{prefix}_ratio_vs_best_reference"
        retrieval_key = None if prefix in {"bytecode", "spec", "lowered"} else f"{prefix}_retrieval_share"
        dominant_key = None if prefix in {"bytecode", "spec", "lowered"} else f"{prefix}_dominant_component"
        exact_case_count = sum(bool(row[exact_key]) for row in rows)
        dominant_counter: dict[str, int] = {}
        if dominant_key is not None:
            for row in rows:
                component = row[dominant_key]
                if component is None:
                    continue
                dominant_counter[str(component)] = dominant_counter.get(str(component), 0) + 1
        ratio_values: list[float] = []
        for row in rows:
            if ratio_key in row and row[ratio_key] is not None:
                ratio_values.append(float(row[ratio_key]))
                continue
            if row.get(ns_key) is not None and row.get("best_reference_ns_per_step") is not None:
                ratio = safe_ratio(float(row[ns_key]), float(row["best_reference_ns_per_step"]))
                if ratio is not None:
                    ratio_values.append(ratio)
        summary_rows.append(
            {
                "strategy_id": strategy_id,
                "control_class": control_class,
                "case_count": len(rows),
                "exact_case_count": exact_case_count,
                "median_ns_per_step": median_or_none(
                    [float(row[ns_key]) for row in rows if row[ns_key] is not None]
                ),
                "median_ratio_vs_best_reference": median_or_none(ratio_values),
                "median_retrieval_share": None
                if retrieval_key is None
                else median_or_none(
                    [float(row[retrieval_key]) for row in rows if row[retrieval_key] is not None]
                ),
                "dominant_component_counts": [
                    {"component": component, "count": count}
                    for component, count in sorted(dominant_counter.items())
                ],
            }
        )
    return summary_rows


def build_suite_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["suite"]), []).append(row)
    suite_rows: list[dict[str, object]] = []
    for suite, suite_group in sorted(grouped.items()):
        suite_rows.append(
            {
                "suite": suite,
                "case_count": len(suite_group),
                "median_best_reference_ns_per_step": median_or_none(
                    [float(row["best_reference_ns_per_step"]) for row in suite_group]
                ),
                "median_lowered_ratio_vs_best_reference": median_or_none(
                    [
                        float(row["lowered_ratio_vs_best_reference"])
                        for row in suite_group
                        if row["lowered_ratio_vs_best_reference"] is not None
                    ]
                ),
                "median_accelerated_ratio_vs_best_reference": median_or_none(
                    [
                        float(row["accelerated_ratio_vs_best_reference"])
                        for row in suite_group
                        if row["accelerated_ratio_vs_best_reference"] is not None
                    ]
                ),
                "median_pointer_like_ratio_vs_best_reference": median_or_none(
                    [
                        float(row["pointer_like_exact_ratio_vs_best_reference"])
                        for row in suite_group
                        if row["pointer_like_exact_ratio_vs_best_reference"] is not None
                    ]
                ),
                "pointer_like_exact_case_count": sum(bool(row["pointer_like_exact_exact"]) for row in suite_group),
            }
        )
    return suite_rows


def assess_gate(
    rows: list[dict[str, object]],
    *,
    r2_summary: dict[str, Any],
) -> dict[str, object]:
    total_case_count = len(rows)
    verification_passed_count = sum(bool(row["verification_passed"]) for row in rows)
    linear_exact_case_count = sum(bool(row["linear_exact_exact"]) for row in rows)
    accelerated_exact_case_count = sum(bool(row["accelerated_exact"]) for row in rows)
    pointer_like_exact_case_count = sum(bool(row["pointer_like_exact_exact"]) for row in rows)
    pointer_like_median_ratio = median_or_none(
        [
            float(row["pointer_like_exact_ratio_vs_best_reference"])
            for row in rows
            if row["pointer_like_exact_ratio_vs_best_reference"] is not None
        ]
    )
    accelerated_median_ratio = median_or_none(
        [
            float(row["accelerated_ratio_vs_best_reference"])
            for row in rows
            if row["accelerated_ratio_vs_best_reference"] is not None
        ]
    )
    lowered_median_ratio = median_or_none(
        [
            float(row["lowered_ratio_vs_best_reference"])
            for row in rows
            if row["lowered_ratio_vs_best_reference"] is not None
        ]
    )
    exact_designated_paths_all_exact = (
        verification_passed_count == total_case_count
        and linear_exact_case_count == total_case_count
        and accelerated_exact_case_count == total_case_count
        and pointer_like_exact_case_count == total_case_count
    )
    r2_gate = r2_summary["gate_summary"]
    anchor_geometry_positive = bool(r2_gate["geometry_positive"])
    anchor_lowered_ratio = float(r2_gate["lowered_ratio_vs_best_reference"])

    if not exact_designated_paths_all_exact:
        lane_verdict = "systems_negative_under_same_endpoint"
        reason = (
            "At least one exact-designated path failed on the current positive D0 suites, "
            "so the systems lane cannot overturn the mixed gate."
        )
    elif (
        anchor_geometry_positive
        and pointer_like_median_ratio is not None
        and pointer_like_median_ratio <= COMPETITIVE_RATIO_THRESHOLD
    ):
        lane_verdict = "systems_materially_positive"
        reason = (
            "Pointer-like exact stayed exact on the current positive D0 suites and is now competitive "
            "with the best current bytecode/spec reference under the R2 bounded threshold."
        )
    else:
        lane_verdict = "systems_still_mixed"
        reason = (
            "Pointer-like exact stayed exact on current positive D0 suites, but the bounded systems threshold "
            "from R2 is still not overturned."
        )

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
        "competitive_ratio_threshold": COMPETITIVE_RATIO_THRESHOLD,
        "total_case_count": total_case_count,
        "verification_passed_count": verification_passed_count,
        "linear_exact_case_count": linear_exact_case_count,
        "accelerated_exact_case_count": accelerated_exact_case_count,
        "pointer_like_exact_case_count": pointer_like_exact_case_count,
        "exact_designated_paths_all_exact": exact_designated_paths_all_exact,
        "pointer_like_median_ratio_vs_best_reference": pointer_like_median_ratio,
        "accelerated_median_ratio_vs_best_reference": accelerated_median_ratio,
        "lowered_median_ratio_vs_best_reference": lowered_median_ratio,
        "pointer_like_median_speedup_vs_accelerated": median_or_none(
            [
                float(row["pointer_like_speedup_vs_accelerated"])
                for row in rows
                if row["pointer_like_speedup_vs_accelerated"] is not None
            ]
        ),
        "pointer_like_median_speedup_vs_lowered": median_or_none(
            [
                float(row["pointer_like_speedup_vs_lowered"])
                for row in rows
                if row["pointer_like_speedup_vs_lowered"] is not None
            ]
        ),
        "r2_anchor_geometry_positive": anchor_geometry_positive,
        "r2_anchor_lowered_ratio_vs_best_reference": anchor_lowered_ratio,
        "ratio_improvement_vs_r2_lowered": safe_ratio(anchor_lowered_ratio, pointer_like_median_ratio),
        "next_priority_lane": "h21_refreeze_after_r22_r23",
    }


def build_summary(
    rows: list[dict[str, object]],
    *,
    r2_summary: dict[str, Any],
    e1b_summary: dict[str, Any],
    r22_summary: dict[str, Any],
    strategy_summary: list[dict[str, object]],
    suite_summary: list[dict[str, object]],
    gate: dict[str, object],
) -> dict[str, object]:
    supported_here = [
        "R23 stays on the same positive D0 suites used by the earlier R2/E1b systems gate rather than switching to a narrower runtime-only sample.",
        (
            f"Pointer-like exact stayed exact on {gate['pointer_like_exact_case_count']}/"
            f"{gate['total_case_count']} current positive D0 rows."
        ),
        "Fresh same-suite measurement now compares bytecode/spec, lowered exec_trace, linear exact, accelerated exact, and pointer-like exact under one bounded runtime matrix.",
    ]
    if gate["lane_verdict"] == "systems_materially_positive":
        supported_here.append(
            "The current same-endpoint systems gate is now materially positive under the bounded R2 threshold."
        )
    unsupported_here = [
        "R23 does not widen beyond the tiny typed-bytecode D0 endpoint.",
        "R23 does not by itself authorize arbitrary compiled-language claims, frontend widening, or a broader 'LLMs are computers' headline.",
        "R23 does not localize the true executor boundary; that remains a separate R22/H21 issue.",
    ]
    if gate["lane_verdict"] != "systems_materially_positive":
        unsupported_here.append(
            "The same-endpoint systems story is still not strong enough to support broader systems or frontier claims."
        )
    disconfirmed_here: list[str] = []
    if gate["lane_verdict"] == "systems_materially_positive":
        disconfirmed_here.append(
            "R23 disconfirms the narrower expectation that the current same-endpoint systems story must remain mixed after measuring pointer-like exact on the full positive D0 suite."
        )
    elif gate["lane_verdict"] == "systems_negative_under_same_endpoint":
        disconfirmed_here.append(
            "R23 disconfirms the bounded hope that pointer-like exact can be treated as a same-endpoint systems candidate on the current positive D0 suites."
        )

    return {
        "status": "r23_same_endpoint_systems_overturn_complete",
        "current_frozen_stage": "h19_refreeze_and_next_scope_decision",
        "source_boundary_stage": "r22_d0_true_boundary_localization_gate",
        "source_systems_anchors": [
            "r2_systems_baseline_gate",
            "e1b_systems_patch",
        ],
        "selected_case_count": len(rows),
        "suite_count": len({str(row['suite']) for row in rows}),
        "gate": gate,
        "historical_anchor": {
            "r2_gate_status": r2_summary["gate_summary"]["gate_status"],
            "r2_lowered_ratio_vs_best_reference": r2_summary["gate_summary"]["lowered_ratio_vs_best_reference"],
            "e1b_gate_status_after_patch": e1b_summary["summary"]["gate_status_after_patch"],
            "e1b_lowered_ratio_vs_best_reference": e1b_summary["summary"]["lowered_ratio_vs_best_reference"],
            "r22_lane_verdict": r22_summary["summary"]["gate"]["lane_verdict"],
        },
        "strategy_summary": strategy_summary,
        "suite_summary": suite_summary,
        "recommended_next_action": "Refreeze R22 and R23 together in H21 before any later outward sync or frontier-planning update.",
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    runtime_rows = [measure_case(case) for case in positive_cases()]
    strategy_summary = build_strategy_summary(runtime_rows)
    suite_summary = build_suite_summary(runtime_rows)
    gate = assess_gate(runtime_rows, r2_summary=inputs["r2_summary"])
    summary = build_summary(
        runtime_rows,
        r2_summary=inputs["r2_summary"],
        e1b_summary=inputs["e1b_summary"],
        r22_summary=inputs["r22_summary"],
        strategy_summary=strategy_summary,
        suite_summary=suite_summary,
        gate=gate,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "runtime_profile_rows.json",
        {
            "experiment": "r23_runtime_profile_rows",
            "environment": environment.as_dict(),
            "rows": runtime_rows,
        },
    )
    write_csv(
        OUT_DIR / "runtime_profile_rows.csv",
        runtime_rows,
        [
            "program_name",
            "suite",
            "comparison_mode",
            "max_steps",
            "verification_passed",
            "verification_seconds",
            "lowering_seconds",
            "profile_step_count",
            "bytecode_median_seconds",
            "bytecode_ns_per_step",
            "lowered_median_seconds",
            "lowered_ns_per_step",
            "spec_median_seconds",
            "spec_ns_per_step",
            "best_reference_path",
            "best_reference_ns_per_step",
            "lowered_ratio_vs_best_reference",
            "linear_exact_median_seconds",
            "linear_exact_ns_per_step",
            "linear_exact_exact",
            "linear_exact_read_observation_count",
            "linear_exact_retrieval_share",
            "linear_exact_ratio_vs_best_reference",
            "accelerated_median_seconds",
            "accelerated_ns_per_step",
            "accelerated_exact",
            "accelerated_read_observation_count",
            "accelerated_retrieval_share",
            "accelerated_ratio_vs_best_reference",
            "pointer_like_exact_median_seconds",
            "pointer_like_exact_ns_per_step",
            "pointer_like_exact_exact",
            "pointer_like_exact_read_observation_count",
            "pointer_like_exact_retrieval_share",
            "pointer_like_exact_ratio_vs_best_reference",
            "pointer_like_speedup_vs_accelerated",
            "pointer_like_speedup_vs_lowered",
        ],
    )
    write_json(
        OUT_DIR / "strategy_summary.json",
        {
            "experiment": "r23_strategy_summary",
            "environment": environment.as_dict(),
            "rows": strategy_summary,
        },
    )
    write_json(
        OUT_DIR / "suite_summary.json",
        {
            "experiment": "r23_suite_summary",
            "environment": environment.as_dict(),
            "rows": suite_summary,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r23_d0_same_endpoint_systems_overturn_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                relative_path(ROOT / "results" / "R2_systems_baseline_gate" / "summary.json"),
                relative_path(ROOT / "results" / "E1b_systems_patch" / "summary.json"),
                relative_path(ROOT / "results" / "R22_d0_true_boundary_localization_gate" / "summary.json"),
                relative_path(ROOT / "src" / "bytecode" / "datasets.py"),
                relative_path(ROOT / "src" / "model" / "free_running_executor.py"),
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R23 D0 Same-Endpoint Systems Overturn Gate\n\n"
        "Fresh same-endpoint systems recheck on the current positive D0 suites after R22.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `runtime_profile_rows.json`\n"
        "- `runtime_profile_rows.csv`\n"
        "- `strategy_summary.json`\n"
        "- `suite_summary.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
