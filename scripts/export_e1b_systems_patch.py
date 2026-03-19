"""Export a bounded E1b systems patch bundle on the current D0 scope."""

from __future__ import annotations

from collections import Counter, defaultdict
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
OUT_DIR = ROOT / "results" / "E1b_systems_patch"
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


def relative_path(path: str | Path) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def median_or_none(values: list[float]) -> float | None:
    return median(values) if values else None


def profile_callable(fn: Callable[[], Any], *, repeats: int = PROFILE_REPEATS) -> tuple[float, list[float], Any]:
    fn()
    samples: list[float] = []
    last_result: Any = None
    for _ in range(repeats):
        start = time.perf_counter()
        last_result = fn()
        samples.append(time.perf_counter() - start)
    return median(samples), samples, last_result


def load_inputs() -> dict[str, Any]:
    return {
        "r2_summary": read_json(ROOT / "results" / "R2_systems_baseline_gate" / "summary.json"),
        "geometry_rows": read_json(ROOT / "results" / "M2_geometry_core" / "benchmark_geometry.json")["rows"],
        "m7_decision": read_json(ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json"),
        "m6_stress_summary": read_json(ROOT / "results" / "M6_stress_reference_followup" / "summary.json"),
        "source_artifacts": [
            relative_path(ROOT / "results" / "M2_geometry_core" / "benchmark_geometry.json"),
            relative_path(ROOT / "results" / "R2_systems_baseline_gate" / "summary.json"),
            "results/R2_systems_baseline_gate/baseline_matrix.json",
            "results/R2_systems_baseline_gate/runtime_profile_rows.csv",
            relative_path(ROOT / "results" / "M6_typed_bytecode_harness" / "short_exact_trace.json"),
            relative_path(ROOT / "results" / "M6_typed_bytecode_harness" / "long_exact_final_state.json"),
            relative_path(ROOT / "results" / "M6_stress_reference_followup" / "summary.json"),
            relative_path(ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json"),
        ],
    }


def positive_cases():
    harness_positive_cases = [case for case in harness_cases() if case.comparison_mode != "verifier_negative"]
    stress_positive_cases = [
        case
        for case in stress_reference_cases()
        if case.comparison_mode in {"medium_exact_trace", "long_exact_final_state"}
    ]
    return [*harness_positive_cases, *stress_positive_cases]


def profile_component_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in positive_cases():
        verification_median, _, verification_result = profile_callable(
            lambda case=case: verify_program(case.program)
        )
        lowering_median, _, lowered_program = profile_callable(
            lambda case=case: lower_program(case.program)
        )
        lowered_exec_median, _, lowered_exec_result = profile_callable(
            lambda lowered_program=lowered_program, case=case: TraceInterpreter().run(
                lowered_program,
                max_steps=case.max_steps,
            )
        )
        lowered_total_median, _, lowered_total_result = profile_callable(
            lambda case=case: TraceInterpreter().run(lower_program(case.program), max_steps=case.max_steps)
        )
        bytecode_median, _, bytecode_result = profile_callable(
            lambda case=case: BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        )
        spec_median, _, spec_result = profile_callable(
            lambda case=case: run_spec_program(case.program, max_steps=case.max_steps)
        )

        step_count = max(
            int(bytecode_result.final_state.steps),
            int(lowered_exec_result.final_state.steps),
            int(lowered_total_result.final_state.steps),
            int(spec_result.final_state.steps),
        )
        bytecode_ns = (bytecode_median / step_count) * 1e9 if step_count else None
        lowered_total_ns = (lowered_total_median / step_count) * 1e9 if step_count else None
        lowered_exec_ns = (lowered_exec_median / step_count) * 1e9 if step_count else None
        spec_ns = (spec_median / step_count) * 1e9 if step_count else None
        best_reference = min(value for value in (bytecode_ns, spec_ns) if value is not None)
        lowered_over_best = (lowered_total_ns / best_reference) if lowered_total_ns is not None and best_reference else None

        rows.append(
            {
                "program_name": case.program.name,
                "suite": case.suite,
                "comparison_mode": case.comparison_mode,
                "profile_step_count": step_count,
                "verification_median_seconds": verification_median,
                "lowering_only_median_seconds": lowering_median,
                "lowered_exec_only_median_seconds": lowered_exec_median,
                "lowered_total_median_seconds": lowered_total_median,
                "bytecode_median_seconds": bytecode_median,
                "spec_median_seconds": spec_median,
                "lowering_share_of_lowered_total": lowering_median / lowered_total_median if lowered_total_median else None,
                "lowered_exec_share_of_lowered_total": lowered_exec_median / lowered_total_median if lowered_total_median else None,
                "lowered_total_ns_per_step": lowered_total_ns,
                "lowered_exec_only_ns_per_step": lowered_exec_ns,
                "bytecode_ns_per_step": bytecode_ns,
                "spec_ns_per_step": spec_ns,
                "lowered_over_best_reference": lowered_over_best,
                "dominant_lowered_component": "lowering_only"
                if lowering_median >= lowered_exec_median
                else "lowered_exec_only",
                "is_lagging_vs_best_reference": bool(lowered_over_best is not None and lowered_over_best > 1.10),
                "verification_passed": bool(verification_result.passed),
            }
        )
    return rows


def build_suite_bridge_rows(component_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    suite_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in component_rows:
        suite_groups[str(row["suite"])].append(row)

    rows: list[dict[str, object]] = []
    for suite, suite_rows in sorted(suite_groups.items()):
        lowered = median(float(row["lowered_total_ns_per_step"]) for row in suite_rows if row["lowered_total_ns_per_step"] is not None)
        bytecode = median(float(row["bytecode_ns_per_step"]) for row in suite_rows if row["bytecode_ns_per_step"] is not None)
        spec = median(float(row["spec_ns_per_step"]) for row in suite_rows if row["spec_ns_per_step"] is not None)
        best_reference = min(bytecode, spec)
        ratio_vs_best = lowered / best_reference if best_reference else None
        rows.append(
            {
                "suite": suite,
                "case_count": len(suite_rows),
                "median_profile_step_count": median_or_none([int(row["profile_step_count"]) for row in suite_rows]),
                "median_lowered_total_ns_per_step": lowered,
                "median_lowered_exec_only_ns_per_step": median_or_none(
                    [float(row["lowered_exec_only_ns_per_step"]) for row in suite_rows if row["lowered_exec_only_ns_per_step"] is not None]
                ),
                "median_lowering_share_of_lowered_total": median_or_none(
                    [float(row["lowering_share_of_lowered_total"]) for row in suite_rows if row["lowering_share_of_lowered_total"] is not None]
                ),
                "median_bytecode_ns_per_step": bytecode,
                "median_spec_ns_per_step": spec,
                "lowered_vs_best_reference_ratio": ratio_vs_best,
                "lowered_vs_bytecode_ratio": lowered / bytecode if bytecode else None,
                "lowered_vs_spec_ratio": lowered / spec if spec else None,
                "bridge_status": "lagging_mixed_gate" if ratio_vs_best is not None and ratio_vs_best > 1.10 else "competitive",
            }
        )
    return rows


def build_history_bridge_rows(
    geometry_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    profile_steps = [int(row["profile_step_count"]) for row in component_rows]
    rows: list[dict[str, object]] = []
    for row in sorted(geometry_rows, key=lambda value: int(value["history_size"])):
        history_size = int(row["history_size"])
        speedup = float(row["cache_speedup_vs_bruteforce"])
        cases_at_or_above = sum(step_count >= history_size for step_count in profile_steps)
        rows.append(
            {
                "history_size": history_size,
                "query_count": int(row["query_count"]),
                "cache_speedup_vs_bruteforce": speedup,
                "cases_at_or_above_history": cases_at_or_above,
                "cases_below_history": len(profile_steps) - cases_at_or_above,
                "max_profile_step_count": max(profile_steps),
                "cache_seconds": float(row["cache_seconds"]),
                "brute_force_seconds": float(row["brute_force_seconds"]),
                "bridge_status": "beyond_current_d0_scope" if cases_at_or_above == 0 else "overlaps_current_d0_scope",
            }
        )
    return rows


def build_summary(
    *,
    r2_summary: dict[str, Any],
    m7_decision: dict[str, Any],
    m6_stress_summary: dict[str, Any],
    component_rows: list[dict[str, object]],
    suite_rows: list[dict[str, object]],
    history_rows: list[dict[str, object]],
) -> dict[str, object]:
    gate_summary = r2_summary["gate_summary"]
    lowered_over_best = [
        float(row["lowered_over_best_reference"])
        for row in component_rows
        if row["lowered_over_best_reference"] is not None
    ]
    dominant_counter = Counter(str(row["dominant_lowered_component"]) for row in component_rows)
    suite_bridge_counter = Counter(str(row["bridge_status"]) for row in suite_rows)
    history_bridge_counter = Counter(str(row["bridge_status"]) for row in history_rows)

    return {
        "target_claim": "R2 systems gate",
        "lane": "E1b_systems_patch",
        "trigger_conflict": "Current locked systems prose needs same-scope component attribution and history bridge rows without widening frontend scope.",
        "gate_question": "On current positive D0 suites, does split attribution overturn the mixed R2 gate without a frontend scope change?",
        "gate_status_after_patch": gate_summary["gate_status"],
        "geometry_positive": bool(gate_summary["geometry_positive"]),
        "lowered_ratio_vs_best_reference": float(gate_summary["lowered_ratio_vs_best_reference"]),
        "component_row_count": len(component_rows),
        "suite_bridge_row_count": len(suite_rows),
        "history_bridge_row_count": len(history_rows),
        "max_profile_step_count": max(int(row["profile_step_count"]) for row in component_rows),
        "lagging_case_count_vs_best_reference": sum(value > 1.10 for value in lowered_over_best),
        "dominant_component_counts": [{"component": component, "count": count} for component, count in sorted(dominant_counter.items())],
        "suite_bridge_status_counts": [{"bridge_status": status, "count": count} for status, count in sorted(suite_bridge_counter.items())],
        "history_bridge_status_counts": [{"bridge_status": status, "count": count} for status, count in sorted(history_bridge_counter.items())],
        "stress_reference_positive_row_count": int(m6_stress_summary["summary"]["positive_row_count"]),
        "frontend_widening_authorized": bool(m7_decision["summary"]["frontend_widening_authorized"]),
        "single_bottleneck_fixable_now": False,
        "e1c_trigger_required": False,
        "decision": "Keep the mixed systems gate wording and the no-widening boundary; this patch adds attribution and bridge accounting only.",
    }


def build_claim_impact(summary: dict[str, object]) -> dict[str, object]:
    return {
        "target_claim": "R2 systems gate",
        "status": "bounded_clarification_no_scope_change",
        "claim_update": "mixed_gate_reaffirmed_with_component_bridge",
        "supports_here": [
            "Geometry asymptotic advantage remains strongly positive on the current benchmark history sweep.",
            "Same-scope suite bridge rows still keep lowered execution slower than the best current reference path on median ns/step.",
            "Component cost rows now separate lowering-only cost from lowered-execution cost on the same D0 suites.",
        ],
        "unproven_here": [
            "Current-scope end-to-end superiority for lowered execution over the best available reference path.",
            "Any claim that geometry asymptotics alone justify frontend widening.",
        ],
        "blocked_here": [
            "Frontend widening remains blocked by the current no-go decision.",
            "No arbitrary-C or broader runtime-generalization claim is supported by this patch lane.",
        ],
        "summary_anchor": {
            "gate_status_after_patch": summary["gate_status_after_patch"],
            "lowered_ratio_vs_best_reference": summary["lowered_ratio_vs_best_reference"],
            "frontend_widening_authorized": summary["frontend_widening_authorized"],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    component_rows = profile_component_rows()
    suite_rows = build_suite_bridge_rows(component_rows)
    history_rows = build_history_bridge_rows(inputs["geometry_rows"], component_rows)
    summary = build_summary(
        r2_summary=inputs["r2_summary"],
        m7_decision=inputs["m7_decision"],
        m6_stress_summary=inputs["m6_stress_summary"],
        component_rows=component_rows,
        suite_rows=suite_rows,
        history_rows=history_rows,
    )
    claim_impact = build_claim_impact(summary)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT_DIR / "component_cost_rows.csv",
        component_rows,
        [
            "program_name",
            "suite",
            "comparison_mode",
            "profile_step_count",
            "verification_median_seconds",
            "lowering_only_median_seconds",
            "lowered_exec_only_median_seconds",
            "lowered_total_median_seconds",
            "bytecode_median_seconds",
            "spec_median_seconds",
            "lowering_share_of_lowered_total",
            "lowered_exec_share_of_lowered_total",
            "lowered_total_ns_per_step",
            "lowered_exec_only_ns_per_step",
            "bytecode_ns_per_step",
            "spec_ns_per_step",
            "lowered_over_best_reference",
            "dominant_lowered_component",
            "is_lagging_vs_best_reference",
            "verification_passed",
        ],
    )
    write_csv(
        OUT_DIR / "suite_bridge_rows.csv",
        suite_rows,
        [
            "suite",
            "case_count",
            "median_profile_step_count",
            "median_lowered_total_ns_per_step",
            "median_lowered_exec_only_ns_per_step",
            "median_lowering_share_of_lowered_total",
            "median_bytecode_ns_per_step",
            "median_spec_ns_per_step",
            "lowered_vs_best_reference_ratio",
            "lowered_vs_bytecode_ratio",
            "lowered_vs_spec_ratio",
            "bridge_status",
        ],
    )
    write_csv(
        OUT_DIR / "history_bridge_rows.csv",
        history_rows,
        [
            "history_size",
            "query_count",
            "cache_speedup_vs_bruteforce",
            "cases_at_or_above_history",
            "cases_below_history",
            "max_profile_step_count",
            "cache_seconds",
            "brute_force_seconds",
            "bridge_status",
        ],
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "e1b_systems_patch",
            "environment": environment.as_dict(),
            "source_artifacts": inputs["source_artifacts"],
            "notes": [
                "This patch lane is bounded to the current mixed R2 systems gate and does not widen frontend scope.",
                "All rows stay on the current positive D0 suites; no new runtime family is introduced.",
                "The output focuses on split component attribution and same-scope bridge accounting.",
            ],
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "claim_impact.json", claim_impact)
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# E1b Systems Patch",
                "",
                "Bounded systems patch bundle for the current mixed `R2` gate.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `component_cost_rows.csv`",
                "- `suite_bridge_rows.csv`",
                "- `history_bridge_rows.csv`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
