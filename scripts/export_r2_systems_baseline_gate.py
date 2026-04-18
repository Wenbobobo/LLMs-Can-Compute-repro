"""Export the current systems-baseline gate for the narrow execution stack."""

from __future__ import annotations

from collections import defaultdict
import csv
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
from exec_trace import TraceInterpreter
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R2_systems_baseline_gate"
PROFILE_REPEATS = 5


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def median_or_none(values: list[float]) -> float | None:
    return median(values) if values else None


def relative_path(path: str | Path) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def profile_callable(fn: Callable[[], Any], *, repeats: int = PROFILE_REPEATS) -> tuple[float, list[float], Any]:
    fn()
    samples: list[float] = []
    last_result: Any = None
    for _ in range(repeats):
        start = time.perf_counter()
        last_result = fn()
        samples.append(time.perf_counter() - start)
    return median(samples), samples, last_result


def load_geometry_rows() -> list[dict[str, object]]:
    payload = read_json(ROOT / "results" / "M2_geometry_core" / "benchmark_geometry.json")
    rows: list[dict[str, object]] = payload["rows"]
    return rows


def build_geometry_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    speedups = [float(row["cache_speedup_vs_bruteforce"]) for row in rows]
    history_sizes = [int(row["history_size"]) for row in rows]
    cache_seconds = [float(row["cache_seconds"]) for row in rows]
    brute_force_seconds = [float(row["brute_force_seconds"]) for row in rows]
    return {
        "row_count": len(rows),
        "history_sizes": history_sizes,
        "median_cache_speedup_vs_bruteforce": median(speedups),
        "min_cache_speedup_vs_bruteforce": min(speedups),
        "max_cache_speedup_vs_bruteforce": max(speedups),
        "speedup_grows_with_history": speedups[-1] > speedups[0],
        "all_cache_rows_faster_than_bruteforce": all(speedup > 1.0 for speedup in speedups),
        "cache_seconds": cache_seconds,
        "brute_force_seconds": brute_force_seconds,
    }


def load_correctness_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    short_payload = read_json(ROOT / "results" / "M6_typed_bytecode_harness" / "short_exact_trace.json")
    long_payload = read_json(ROOT / "results" / "M6_typed_bytecode_harness" / "long_exact_final_state.json")
    stress_payload = read_json(ROOT / "results" / "M6_stress_reference_followup" / "summary.json")
    rows.extend(short_payload["rows"])
    rows.extend(long_payload["rows"])
    rows.extend(stress_payload["rows"])
    return rows


def correctness_lookup(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    mapping: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        mapping[(str(row["program_name"]), str(row["comparison_mode"]))] = row
    return mapping


def profile_positive_cases() -> list[dict[str, object]]:
    correctness = correctness_lookup(load_correctness_rows())
    rows: list[dict[str, object]] = []

    harness_positive_cases = [
        case
        for case in harness_cases()
        if case.comparison_mode != "verifier_negative"
    ]
    stress_positive_cases = [
        case
        for case in stress_reference_cases()
        if case.comparison_mode in {"medium_exact_trace", "long_exact_final_state"}
    ]
    all_cases = [*harness_positive_cases, *stress_positive_cases]

    for case in all_cases:
        verification_median, verification_samples, verification_result = profile_callable(
            lambda case=case: verify_program(case.program)
        )
        bytecode_median, bytecode_samples, bytecode_result = profile_callable(
            lambda case=case: BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        )
        lowered_median, lowered_samples, lowered_result = profile_callable(
            lambda case=case: TraceInterpreter().run(lower_program(case.program), max_steps=case.max_steps)
        )
        spec_median, spec_samples, spec_result = profile_callable(
            lambda case=case: run_spec_program(case.program, max_steps=case.max_steps)
        )

        bytecode_steps = int(bytecode_result.final_state.steps)
        lowered_steps = int(lowered_result.final_state.steps)
        spec_steps = int(spec_result.final_state.steps)
        step_count = max(bytecode_steps, lowered_steps, spec_steps)
        reference = correctness.get((case.program.name, case.comparison_mode), {})

        rows.append(
            {
                "program_name": case.program.name,
                "suite": case.suite,
                "comparison_mode": case.comparison_mode,
                "max_steps": case.max_steps,
                "verification_passed": bool(verification_result.passed),
                "trace_match": reference.get("trace_match"),
                "final_state_match": reference.get("final_state_match")
                if "final_state_match" in reference
                else reference.get("all_final_state_match"),
                "verification_median_seconds": verification_median,
                "verification_samples": verification_samples,
                "bytecode_median_seconds": bytecode_median,
                "bytecode_samples": bytecode_samples,
                "lowered_median_seconds": lowered_median,
                "lowered_samples": lowered_samples,
                "spec_median_seconds": spec_median,
                "spec_samples": spec_samples,
                "bytecode_step_count": bytecode_steps,
                "lowered_step_count": lowered_steps,
                "spec_step_count": spec_steps,
                "profile_step_count": step_count,
                "bytecode_ns_per_step": (bytecode_median / bytecode_steps) * 1e9 if bytecode_steps else None,
                "lowered_ns_per_step": (lowered_median / lowered_steps) * 1e9 if lowered_steps else None,
                "spec_ns_per_step": (spec_median / spec_steps) * 1e9 if spec_steps else None,
            }
        )
    return rows


def build_runtime_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    per_path = {
        "bytecode": [float(row["bytecode_ns_per_step"]) for row in rows if row["bytecode_ns_per_step"] is not None],
        "lowered": [float(row["lowered_ns_per_step"]) for row in rows if row["lowered_ns_per_step"] is not None],
        "spec": [float(row["spec_ns_per_step"]) for row in rows if row["spec_ns_per_step"] is not None],
        "verification": [float(row["verification_median_seconds"]) * 1e6 for row in rows],
    }
    suite_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        suite_groups[str(row["suite"])].append(row)

    by_suite = []
    for suite, suite_rows in sorted(suite_groups.items()):
        by_suite.append(
            {
                "suite": suite,
                "case_count": len(suite_rows),
                "median_bytecode_ns_per_step": median_or_none(
                    [float(row["bytecode_ns_per_step"]) for row in suite_rows if row["bytecode_ns_per_step"] is not None]
                ),
                "median_lowered_ns_per_step": median_or_none(
                    [float(row["lowered_ns_per_step"]) for row in suite_rows if row["lowered_ns_per_step"] is not None]
                ),
                "median_spec_ns_per_step": median_or_none(
                    [float(row["spec_ns_per_step"]) for row in suite_rows if row["spec_ns_per_step"] is not None]
                ),
            }
        )

    return {
        "case_count": len(rows),
        "median_bytecode_ns_per_step": median_or_none(per_path["bytecode"]),
        "median_lowered_ns_per_step": median_or_none(per_path["lowered"]),
        "median_spec_ns_per_step": median_or_none(per_path["spec"]),
        "median_verification_microseconds": median_or_none(per_path["verification"]),
        "by_suite": by_suite,
    }


def assess_gate(*, geometry_summary: dict[str, object], runtime_summary: dict[str, object]) -> dict[str, object]:
    geometry_positive = bool(
        geometry_summary["all_cache_rows_faster_than_bruteforce"]
        and geometry_summary["speedup_grows_with_history"]
    )
    lowered = runtime_summary["median_lowered_ns_per_step"]
    bytecode = runtime_summary["median_bytecode_ns_per_step"]
    spec = runtime_summary["median_spec_ns_per_step"]

    reasons: list[str] = []
    if geometry_positive:
        reasons.append("Geometry benchmark still shows a clear and growing cache-vs-bruteforce speedup.")
    else:
        reasons.append("Geometry benchmark does not currently show a clean asymptotic win.")

    if lowered is None or bytecode is None or spec is None:
        return {
            "gate_status": "insufficient_measurement",
            "reasons": reasons + ["One or more runtime paths are missing profile data."],
            "what_is_missing": [
                "complete runtime profiles for bytecode, lowered exec_trace, and standalone spec oracle"
            ],
        }

    best_reference = min(bytecode, spec)
    lowered_ratio_vs_best_reference = lowered / best_reference if best_reference else None
    if lowered_ratio_vs_best_reference is None:
        gate_status = "insufficient_measurement"
    elif geometry_positive and lowered_ratio_vs_best_reference <= 1.10:
        gate_status = "positive_current_scope"
        reasons.append("Lowered exec_trace is already competitive with the best current reference path on median ns/step.")
    elif geometry_positive:
        gate_status = "asymptotic_positive_but_end_to_end_not_yet_competitive"
        reasons.append(
            "Lowered exec_trace remains slower than the best current reference/oracle path on current-scope median ns/step."
        )
    else:
        gate_status = "not_yet_justified"
        reasons.append("End-to-end runtime does not currently compensate for the missing geometry signal.")

    return {
        "gate_status": gate_status,
        "geometry_positive": geometry_positive,
        "lowered_ratio_vs_best_reference": lowered_ratio_vs_best_reference,
        "reasons": reasons,
        "what_is_missing": [
            "broader end-to-end cost comparisons against any future widened frontend",
            "cost attribution beyond the current interpreter/lowered/spec paths",
        ],
    }


def build_decision_table(geometry_summary: dict[str, object], runtime_summary: dict[str, object]) -> list[dict[str, object]]:
    decision = assess_gate(geometry_summary=geometry_summary, runtime_summary=runtime_summary)
    return [
        {
            "question": "Does specialized retrieval still buy an asymptotic advantage on the current geometry benchmark?",
            "status": "yes" if decision["geometry_positive"] else "no",
            "evidence": "results/M2_geometry_core/benchmark_geometry.json",
        },
        {
            "question": "Is the lowered exec_trace path already end-to-end competitive with the best current reference path?",
            "status": "yes"
            if decision["gate_status"] == "positive_current_scope"
            else "not_yet",
            "evidence": "results/R2_systems_baseline_gate/runtime_profile_rows.csv",
        },
        {
            "question": "Should frontend widening proceed before another systems pass?",
            "status": "no" if decision["gate_status"] != "positive_current_scope" else "revisit",
            "evidence": "results/R2_systems_baseline_gate/summary.json",
        },
    ]


def main() -> None:
    environment = detect_runtime_environment()
    geometry_rows = load_geometry_rows()
    runtime_rows = profile_positive_cases()
    geometry_summary = build_geometry_summary(geometry_rows)
    runtime_summary = build_runtime_summary(runtime_rows)
    gate_summary = assess_gate(geometry_summary=geometry_summary, runtime_summary=runtime_summary)
    decision_table = build_decision_table(geometry_summary, runtime_summary)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    write_csv(
        OUT_DIR / "geometry_speedup_rows.csv",
        geometry_rows,
        [
            "history_size",
            "query_count",
            "insert_seconds",
            "brute_force_seconds",
            "cache_seconds",
            "cache_speedup_vs_bruteforce",
        ],
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
            "trace_match",
            "final_state_match",
            "verification_median_seconds",
            "bytecode_median_seconds",
            "lowered_median_seconds",
            "spec_median_seconds",
            "bytecode_step_count",
            "lowered_step_count",
            "spec_step_count",
            "profile_step_count",
            "bytecode_ns_per_step",
            "lowered_ns_per_step",
            "spec_ns_per_step",
        ],
    )
    write_json(
        OUT_DIR / "baseline_matrix.json",
        {
            "experiment": "r2_systems_baseline_matrix",
            "environment": environment.as_dict(),
            "geometry_summary": geometry_summary,
            "runtime_summary": runtime_summary,
            "decision_table": decision_table,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r2_systems_baseline_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                relative_path(ROOT / "results" / "M2_geometry_core" / "benchmark_geometry.json"),
                relative_path(ROOT / "results" / "M6_typed_bytecode_harness" / "short_exact_trace.json"),
                relative_path(ROOT / "results" / "M6_typed_bytecode_harness" / "long_exact_final_state.json"),
                relative_path(ROOT / "results" / "M6_stress_reference_followup" / "summary.json"),
            ],
            "notes": [
                "This gate keeps the system claim narrower than the mechanism claim.",
                "Geometry speedup is evaluated from the existing M2 benchmark; bytecode/spec timings are profiled on the current positive D0 suites.",
                "A negative or mixed systems result is still evidence because it constrains any later frontend widening.",
            ],
            "geometry_summary": geometry_summary,
            "runtime_summary": runtime_summary,
            "gate_summary": gate_summary,
            "decision_table": decision_table,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R2 Systems Baseline Gate",
                "",
                "Current-scope systems gate comparing geometry asymptotics with bytecode/lowered/spec runtime profiles.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `baseline_matrix.json`",
                "- `geometry_speedup_rows.csv`",
                "- `runtime_profile_rows.csv`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
