"""Export the bounded R7 same-endpoint runtime bridge on exact-admitted R6 rows."""

from __future__ import annotations

from collections import defaultdict
import csv
import json
from pathlib import Path
from statistics import median
import time
from typing import Any, Callable

from bytecode import BytecodeInterpreter, lower_program, r6_d0_long_horizon_scaling_cases
from exec_trace import TraceInterpreter
from model import compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R7_d0_same_endpoint_runtime_bridge"
R6_EXACT_ROWS = ROOT / "results" / "R6_d0_long_horizon_scaling_gate" / "exact_suite_rows.json"
PROFILE_REPEATS = 1
PROFILE_TOP_FAMILIES = 4
MATERIAL_DECODE_SPEEDUP = 1.10
BRIDGE_RATIO_THRESHOLD = 1.50


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


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
    warmup: bool = False,
) -> tuple[float, list[float], Any]:
    if warmup:
        fn()
    samples: list[float] = []
    last_result: Any = None
    for _ in range(repeats):
        start = time.perf_counter()
        last_result = fn()
        samples.append(time.perf_counter() - start)
    return median(samples), samples, last_result


def load_exact_admitted_cases():
    payload = read_json(R6_EXACT_ROWS)
    admitted_names = {
        str(row["program_name"])
        for row in payload["rows"]
        if str(row["comparison_mode"]) in {"medium_exact_trace", "long_exact_final_state"}
        and row["mismatch_class"] is None
    }
    grouped: dict[str, list[object]] = defaultdict(list)
    for case in r6_d0_long_horizon_scaling_cases():
        if case.program.name in admitted_names:
            grouped[case.family].append(case)
    cases = [
        max(family_cases, key=lambda case: (case.horizon_multiplier, case.program.name))
        for family_cases in grouped.values()
    ]
    if not cases:
        raise RuntimeError("R7 needs exact-admitted R6 rows. Run export_r6_d0_long_horizon_scaling_gate.py first.")
    return tuple(sorted(cases, key=lambda case: (case.family, case.horizon_multiplier, case.program.name)))


def build_exact_admitted_index(cases) -> list[dict[str, object]]:
    return [
        {
            "family": case.family,
            "baseline_stage": case.baseline_stage,
            "baseline_program_name": case.baseline_program_name,
            "baseline_start": case.baseline_start,
            "horizon_multiplier": case.horizon_multiplier,
            "scaled_start": case.scaled_start,
            "program_name": case.program.name,
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
        }
        for case in cases
    ]


def select_profile_cases(cases) -> tuple[object, ...]:
    ranked = sorted(
        cases,
        key=lambda case: (
            BytecodeInterpreter().run(case.program, max_steps=case.max_steps).final_state.steps,
            case.horizon_multiplier,
            case.program.name,
        ),
        reverse=True,
    )
    return tuple(sorted(ranked[:PROFILE_TOP_FAMILIES], key=lambda case: (case.family, case.program.name)))


def profile_exact_admitted_cases(cases) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in cases:
        lowered_program = lower_program(case.program)

        bytecode_median, bytecode_samples, bytecode_result = profile_callable(
            lambda case=case: BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        )
        lowered_median, lowered_samples, lowered_result = profile_callable(
            lambda lowered_program=lowered_program, case=case: TraceInterpreter().run(
                lowered_program, max_steps=case.max_steps
            )
        )
        linear_median, linear_samples, linear_result = profile_callable(
            lambda lowered_program=lowered_program, case=case: run_free_running_exact(
                lowered_program,
                decode_mode="linear",
                max_steps=case.max_steps,
            ),
        )
        accelerated_median, accelerated_samples, accelerated_result = profile_callable(
            lambda lowered_program=lowered_program, case=case: run_free_running_exact(
                lowered_program,
                decode_mode="accelerated",
                max_steps=case.max_steps,
            ),
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
        rows.append(
            {
                "family": case.family,
                "baseline_stage": case.baseline_stage,
                "horizon_multiplier": case.horizon_multiplier,
                "program_name": case.program.name,
                "comparison_mode": case.comparison_mode,
                "max_steps": case.max_steps,
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
        )
    return rows


def build_family_bridge_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["family"])].append(row)

    summaries: list[dict[str, object]] = []
    for family, family_rows in sorted(grouped.items()):
        summaries.append(
            {
                "family": family,
                "row_count": len(family_rows),
                "max_horizon_multiplier": max(int(row["horizon_multiplier"]) for row in family_rows),
                "median_accelerated_speedup_vs_linear": median(
                    float(row["accelerated_speedup_vs_linear"]) for row in family_rows
                ),
                "median_accelerated_ratio_vs_lowered": median(
                    float(row["accelerated_ratio_vs_lowered"]) for row in family_rows
                ),
                "all_rows_exact": all(
                    row["linear_exact_trace_match"]
                    and row["linear_exact_final_state_match"]
                    and row["accelerated_exact_trace_match"]
                    and row["accelerated_exact_final_state_match"]
                    and row["linear_accelerated_trace_match"]
                    and row["linear_accelerated_final_state_match"]
                    and row["exact_read_agreement"]
                    for row in family_rows
                ),
            }
        )
    return summaries


def assess_stopgo(rows: list[dict[str, object]]) -> dict[str, object]:
    exact_failures = [
        row
        for row in rows
        if not (
            row["linear_exact_trace_match"]
            and row["linear_exact_final_state_match"]
            and row["accelerated_exact_trace_match"]
            and row["accelerated_exact_final_state_match"]
            and row["linear_accelerated_trace_match"]
            and row["linear_accelerated_final_state_match"]
            and row["exact_read_agreement"]
        )
    ]
    median_speedup = median(float(row["accelerated_speedup_vs_linear"]) for row in rows)
    median_ratio_vs_lowered = median(float(row["accelerated_ratio_vs_lowered"]) for row in rows)

    if exact_failures:
        status = "stop_exactness_contradiction"
        reason = "Same-endpoint runtime bridge cannot proceed because exact linear/Hull behavior diverged on exact-admitted rows."
    elif median_speedup < MATERIAL_DECODE_SPEEDUP:
        status = "stop_decode_gain_not_material"
        reason = "Accelerated Hull decode does not yet provide a material same-endpoint speedup over linear decode."
    elif median_ratio_vs_lowered > BRIDGE_RATIO_THRESHOLD:
        status = "stop_bridge_not_yet_closed"
        reason = "Accelerated exact execution is faster than linear but still not close enough to the lowered endpoint path."
    else:
        status = "go_same_endpoint_bridge_positive"
        reason = "Accelerated exact execution is materially faster than linear and close enough to the lowered endpoint path."

    return {
        "stopgo_status": status,
        "median_accelerated_speedup_vs_linear": median_speedup,
        "median_accelerated_ratio_vs_lowered": median_ratio_vs_lowered,
        "reason": reason,
        "thresholds": {
            "material_decode_speedup": MATERIAL_DECODE_SPEEDUP,
            "bridge_ratio_vs_lowered": BRIDGE_RATIO_THRESHOLD,
        },
    }


def build_summary(
    rows: list[dict[str, object]],
    family_rows: list[dict[str, object]],
    *,
    exact_admitted_family_count: int,
) -> dict[str, object]:
    stopgo = assess_stopgo(rows)
    contradiction_candidate_count = sum(
        not (
            row["linear_exact_trace_match"]
            and row["linear_exact_final_state_match"]
            and row["accelerated_exact_trace_match"]
            and row["accelerated_exact_final_state_match"]
            and row["linear_accelerated_trace_match"]
            and row["linear_accelerated_final_state_match"]
            and row["exact_read_agreement"]
        )
        for row in rows
    )
    return {
        "overall": {
            "exact_admitted_family_count": exact_admitted_family_count,
            "profiled_row_count": len(rows),
            "profiled_family_count": len(family_rows),
            "profile_selection_rule": f"top_{PROFILE_TOP_FAMILIES}_exact_admitted_families_by_bytecode_step_count",
            "median_bytecode_ns_per_step": median_or_none([float(row["bytecode_ns_per_step"]) for row in rows]),
            "median_lowered_ns_per_step": median_or_none([float(row["lowered_ns_per_step"]) for row in rows]),
            "median_linear_ns_per_step": median_or_none([float(row["linear_ns_per_step"]) for row in rows]),
            "median_accelerated_ns_per_step": median_or_none(
                [float(row["accelerated_ns_per_step"]) for row in rows]
            ),
            "profile_repeats": PROFILE_REPEATS,
            "median_accelerated_speedup_vs_linear": stopgo["median_accelerated_speedup_vs_linear"],
            "median_accelerated_ratio_vs_lowered": stopgo["median_accelerated_ratio_vs_lowered"],
            "contradiction_candidate_count": contradiction_candidate_count,
        },
        "stopgo": stopgo,
        "claim_impact": {
            "status": "same_endpoint_runtime_bridge_measured",
            "target_claims": ["D0"],
            "r5_reopen_status": "not_justified"
            if stopgo["stopgo_status"] != "go_same_endpoint_bridge_positive"
            else "still_separate_from_r5",
            "e1c_status": "not_triggered" if contradiction_candidate_count == 0 else "triggered",
            "next_lane": "H9_refreeze_and_record_sync"
            if contradiction_candidate_count == 0
            else "E1c_compiled_boundary_patch",
            "supported_here": [
                "R7 measures same-endpoint cost on the heaviest exact-admitted long-horizon D0 rows rather than reopening a broader systems lane.",
                "Accelerated-versus-linear decode costs are compared on the same exact executor and the same lowered endpoint rows.",
            ],
            "unsupported_here": [
                "R7 does not reopen R5 by itself and does not justify frontend widening or a broader systems claim.",
                "Even a positive same-endpoint decode gain would still be narrower than current-scope end-to-end systems superiority.",
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = load_exact_admitted_cases()
    exact_admitted_index = build_exact_admitted_index(cases)
    profile_cases = select_profile_cases(cases)
    runtime_rows = profile_exact_admitted_cases(profile_cases)
    family_rows = build_family_bridge_summary(runtime_rows)
    summary = build_summary(runtime_rows, family_rows, exact_admitted_family_count=len(cases))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r7_d0_same_endpoint_runtime_bridge",
            "environment": environment.as_dict(),
            "notes": [
                "R7 reads the full exact-admitted R6 index but profiles only the heaviest family representatives so the same-endpoint bridge stays inside unattended execution budget.",
                "The bridge compares linear-vs-Hull exact execution on the same lowered programs and same step budgets.",
                "Timing is recorded as one bounded profiling pass per endpoint on the selected heaviest exact-admitted rows.",
                "A stop result is still evidence because it bounds what decode acceleration currently buys on the exact endpoint.",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "exact_admitted_index.json",
        {
            "experiment": "r7_d0_same_endpoint_runtime_exact_admitted_index",
            "environment": environment.as_dict(),
            "rows": exact_admitted_index,
        },
    )
    write_json(
        OUT_DIR / "family_bridge_summary.json",
        {
            "experiment": "r7_d0_same_endpoint_runtime_family_bridge_summary",
            "environment": environment.as_dict(),
            "rows": family_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r7_d0_same_endpoint_runtime_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    write_csv(
        OUT_DIR / "runtime_bridge_rows.csv",
        runtime_rows,
        [
            "family",
            "baseline_stage",
            "horizon_multiplier",
            "program_name",
            "comparison_mode",
            "max_steps",
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
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R7 D0 Same-Endpoint Runtime Bridge",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `exact_admitted_index.json`",
                "- `family_bridge_summary.json`",
                "- `runtime_bridge_rows.csv`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
