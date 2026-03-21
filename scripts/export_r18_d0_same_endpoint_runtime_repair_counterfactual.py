"""Export the bounded R18 runtime repair counterfactual packet."""

from __future__ import annotations

from collections import defaultdict
import csv
from dataclasses import dataclass
import json
from pathlib import Path
from statistics import median
import time
from typing import Any, Iterable

from bytecode import lower_program, r8_d0_retrieval_pressure_cases, r15_d0_remaining_family_retrieval_pressure_cases
from exec_trace import TraceInterpreter
from model import compare_execution_to_reference
from model.exact_hardmax import extract_memory_operations
from model.free_running_executor import FreeRunningExecutionResult, FreeRunningTraceExecutor
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R18_d0_same_endpoint_runtime_repair_counterfactual"
R17_OUT_DIR = ROOT / "results" / "R17_d0_full_surface_runtime_bridge"
PROFILE_REPEATS = 1
TARGET_SPEEDUP_GATE = 2.0
CONFIRMATION_MEDIAN_SPEEDUP_GATE = 1.25
STAGED_RETRY_MIN_SPEEDUP = 1.5


@dataclass(frozen=True, slots=True)
class SurfaceCaseRecord:
    source_lane: str
    family: str
    baseline_stage: str
    baseline_program_name: str
    baseline_horizon_multiplier: int
    retrieval_horizon_multiplier: int
    comparison_mode: str
    program_name: str
    max_steps: int
    boundary_bearing_stream: bool
    case: Any
    r17_lowered_ns_per_step: float
    r17_accelerated_ns_per_step: float


@dataclass(frozen=True, slots=True)
class ProbeCase:
    selection_rank: int
    probe_role: str
    focus_reason: str
    selection_rule: str
    record: SurfaceCaseRecord


@dataclass(frozen=True, slots=True)
class ProbeImplementation:
    probe_id: str
    probe_label: str
    status: str
    probe_strategy: str
    stack_strategy: str
    memory_strategy: str


R18B_POINTER_LIKE = ProbeImplementation(
    probe_id="r18b_pointer_like",
    probe_label="R18b",
    status="r18b_pointer_like_complete",
    probe_strategy="pointer_like_exact_both_spaces",
    stack_strategy="pointer_like_exact",
    memory_strategy="pointer_like_exact",
)
R18C_STAGED_EXACT = ProbeImplementation(
    probe_id="r18c_staged_exact",
    probe_label="R18c",
    status="r18c_staged_exact_complete",
    probe_strategy="staged_exact_both_spaces",
    stack_strategy="staged_exact",
    memory_strategy="staged_exact",
)


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def median_or_none(values: Iterable[float]) -> float | None:
    values = list(values)
    return median(values) if values else None


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def profile_callable(fn):
    samples: list[float] = []
    result = None
    for _ in range(PROFILE_REPEATS):
        start = time.perf_counter()
        result = fn()
        samples.append(time.perf_counter() - start)
    return median(samples), samples, result


def reference_execution(lowered_program, *, max_steps: int) -> FreeRunningExecutionResult:
    reference = TraceInterpreter().run(lowered_program, max_steps=max_steps)
    return FreeRunningExecutionResult(
        program=lowered_program,
        events=reference.events,
        final_state=reference.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def build_case_registry() -> dict[str, tuple[str, Any]]:
    registry: dict[str, tuple[str, Any]] = {}
    for case in r8_d0_retrieval_pressure_cases():
        registry[case.program.name] = ("R8_d0_retrieval_pressure_gate", case)
    for case in r15_d0_remaining_family_retrieval_pressure_cases():
        registry[case.program.name] = ("R15_d0_remaining_family_retrieval_pressure_gate", case)
    return registry


def load_surface_case_records() -> tuple[SurfaceCaseRecord, ...]:
    registry = build_case_registry()
    rows: list[SurfaceCaseRecord] = []
    with (R17_OUT_DIR / "runtime_bridge_rows.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            program_name = str(row["program_name"])
            source_lane, case = registry[program_name]
            rows.append(
                SurfaceCaseRecord(
                    source_lane=source_lane,
                    family=str(row["family"]),
                    baseline_stage=str(row["baseline_stage"]),
                    baseline_program_name=str(row["baseline_program_name"]),
                    baseline_horizon_multiplier=int(row["baseline_horizon_multiplier"]),
                    retrieval_horizon_multiplier=int(row["retrieval_horizon_multiplier"]),
                    comparison_mode=str(row["comparison_mode"]),
                    program_name=program_name,
                    max_steps=int(row["max_steps"]),
                    boundary_bearing_stream=parse_bool(row["boundary_bearing_stream"]),
                    case=case,
                    r17_lowered_ns_per_step=float(row["lowered_ns_per_step"]),
                    r17_accelerated_ns_per_step=float(row["accelerated_ns_per_step"]),
                )
            )
    if len(rows) != 8:
        raise RuntimeError(f"R18 expected 8 admitted R17 rows, found {len(rows)}.")
    return tuple(rows)


def load_probe_cases(surface_records: tuple[SurfaceCaseRecord, ...]) -> tuple[ProbeCase, ...]:
    by_program_name = {record.program_name: record for record in surface_records}
    payload = read_json(R17_OUT_DIR / "focused_attribution_selection.json")
    probe_cases: list[ProbeCase] = []
    for row in payload["rows"]:
        program_name = str(row["program_name"])
        selection_rank = int(row["selection_rank"])
        probe_cases.append(
            ProbeCase(
                selection_rank=selection_rank,
                probe_role="target" if selection_rank == 1 else "control",
                focus_reason=str(row["focus_reason"]),
                selection_rule=str(row["selection_rule"]),
                record=by_program_name[program_name],
            )
        )
    if len(probe_cases) != 2:
        raise RuntimeError(f"R18 expected 2 focused probe cases, found {len(probe_cases)}.")
    return tuple(sorted(probe_cases, key=lambda item: item.selection_rank))


def build_memory_address_profile(record: SurfaceCaseRecord) -> dict[str, object]:
    lowered_program = lower_program(record.case.program)
    reference = TraceInterpreter().run(lowered_program, max_steps=record.max_steps)
    operations = extract_memory_operations(reference.events)
    by_address: dict[int, dict[str, int]] = defaultdict(lambda: {"loads": 0, "stores": 0})
    load_count = 0
    store_count = 0
    for operation in operations:
        if operation.kind == "load":
            by_address[operation.address]["loads"] += 1
            load_count += 1
        elif operation.kind == "store":
            by_address[operation.address]["stores"] += 1
            store_count += 1
    address_rows = [
        {
            "address": address,
            "loads": counts["loads"],
            "stores": counts["stores"],
            "total_ops": counts["loads"] + counts["stores"],
        }
        for address, counts in sorted(by_address.items())
    ]
    hottest_address_row = max(
        address_rows,
        key=lambda row: (int(row["total_ops"]), int(row["loads"]), -int(row["address"])),
    )
    return {
        "program_name": record.program_name,
        "family": record.family,
        "source_lane": record.source_lane,
        "boundary_bearing_stream": record.boundary_bearing_stream,
        "reference_step_count": int(reference.final_state.steps),
        "memory_operation_count": len(operations),
        "memory_load_count": load_count,
        "memory_store_count": store_count,
        "unique_address_count": len(address_rows),
        "hottest_address": hottest_address_row["address"],
        "hottest_address_loads": hottest_address_row["loads"],
        "hottest_address_stores": hottest_address_row["stores"],
        "address_rows": address_rows,
    }


def profile_surface_record(
    record: SurfaceCaseRecord,
    probe: ProbeImplementation,
    *,
    selection_rank: int | None = None,
    probe_role: str | None = None,
    focus_reason: str | None = None,
    selection_rule: str | None = None,
) -> dict[str, object]:
    lowered_program = lower_program(record.case.program)
    reference = reference_execution(lowered_program, max_steps=record.max_steps)
    probe_median, probe_samples, probe_result = profile_callable(
        lambda: FreeRunningTraceExecutor(
            stack_strategy=probe.stack_strategy,
            memory_strategy=probe.memory_strategy,
            validate_exact_reads=False,
        ).run(lowered_program, max_steps=record.max_steps)
    )

    probe_outcome = compare_execution_to_reference(lowered_program, probe_result, reference=reference)
    step_count = int(reference.final_state.steps)
    probe_ns_per_step = (probe_median / step_count) * 1e9
    lowered_ns_per_step = record.r17_lowered_ns_per_step
    accelerated_ns_per_step = record.r17_accelerated_ns_per_step
    memory_read_count = sum(observation.space == "memory" for observation in probe_result.read_observations)
    stack_read_count = sum(observation.space == "stack" for observation in probe_result.read_observations)

    return {
        "probe_id": probe.probe_id,
        "probe_label": probe.probe_label,
        "probe_strategy": probe.probe_strategy,
        "stack_strategy": probe.stack_strategy,
        "memory_strategy": probe.memory_strategy,
        "selection_rank": selection_rank,
        "probe_role": probe_role,
        "focus_reason": focus_reason,
        "selection_rule": selection_rule,
        "source_lane": record.source_lane,
        "family": record.family,
        "program_name": record.program_name,
        "baseline_stage": record.baseline_stage,
        "baseline_program_name": record.baseline_program_name,
        "baseline_horizon_multiplier": record.baseline_horizon_multiplier,
        "retrieval_horizon_multiplier": record.retrieval_horizon_multiplier,
        "comparison_mode": record.comparison_mode,
        "max_steps": record.max_steps,
        "boundary_bearing_stream": record.boundary_bearing_stream,
        "reference_step_count": step_count,
        "profile_repeats": PROFILE_REPEATS,
        "r17_baseline_accelerated_ns_per_step": accelerated_ns_per_step,
        "r17_baseline_lowered_ns_per_step": lowered_ns_per_step,
        "current_lowered_ns_per_step": lowered_ns_per_step,
        "current_accelerated_ns_per_step": accelerated_ns_per_step,
        "probe_ns_per_step": probe_ns_per_step,
        "speedup_vs_current_accelerated": accelerated_ns_per_step / probe_ns_per_step,
        "speedup_vs_r17_accelerated": record.r17_accelerated_ns_per_step / probe_ns_per_step,
        "probe_ratio_vs_current_lowered": probe_ns_per_step / lowered_ns_per_step,
        "probe_samples": probe_samples,
        "probe_exact_trace_match": probe_outcome.exact_trace_match,
        "probe_exact_final_state_match": probe_outcome.exact_final_state_match,
        "probe_first_mismatch_step": probe_outcome.first_mismatch_step,
        "read_observation_count": len(probe_result.read_observations),
        "memory_read_count": memory_read_count,
        "stack_read_count": stack_read_count,
    }


def probe_row_is_exact(row: dict[str, object]) -> bool:
    return bool(row["probe_exact_trace_match"]) and bool(row["probe_exact_final_state_match"])


def assess_target_gate(probe_rows: list[dict[str, object]]) -> dict[str, object]:
    target_row = next(row for row in probe_rows if row["probe_role"] == "target")
    control_row = next(row for row in probe_rows if row["probe_role"] == "control")
    target_exact = probe_row_is_exact(target_row)
    control_exact = probe_row_is_exact(control_row)
    target_speedup = float(target_row["speedup_vs_r17_accelerated"])
    gate_passed = target_exact and target_speedup >= TARGET_SPEEDUP_GATE
    retry_eligible = target_exact and control_exact and STAGED_RETRY_MIN_SPEEDUP <= target_speedup < TARGET_SPEEDUP_GATE
    return {
        "target_program_name": target_row["program_name"],
        "target_family": target_row["family"],
        "control_program_name": control_row["program_name"],
        "control_family": control_row["family"],
        "target_exact": target_exact,
        "control_exact": control_exact,
        "target_speedup_vs_r17_accelerated": target_speedup,
        "required_speedup_vs_r17_accelerated": TARGET_SPEEDUP_GATE,
        "staged_retry_min_speedup_vs_r17_accelerated": STAGED_RETRY_MIN_SPEEDUP,
        "gate_passed": gate_passed,
        "retry_eligible": retry_eligible,
        "reason": (
            "The focused target stayed exact and cleared the 2.0x same-semantics speedup gate."
            if gate_passed
            else "The focused target did not yet clear the exactness-plus-2.0x target gate."
        ),
    }


def assess_confirmation(confirmation_rows: list[dict[str, object]]) -> dict[str, object]:
    exact_count = sum(probe_row_is_exact(row) for row in confirmation_rows)
    median_speedup = median_or_none(float(row["speedup_vs_r17_accelerated"]) for row in confirmation_rows)
    gate_passed = (
        bool(confirmation_rows)
        and exact_count == len(confirmation_rows)
        and median_speedup is not None
        and median_speedup >= CONFIRMATION_MEDIAN_SPEEDUP_GATE
    )
    return {
        "row_count": len(confirmation_rows),
        "exact_row_count": exact_count,
        "median_speedup_vs_r17_accelerated": median_speedup,
        "required_median_speedup_vs_r17_accelerated": CONFIRMATION_MEDIAN_SPEEDUP_GATE,
        "gate_passed": gate_passed,
        "reason": (
            "The full admitted surface stayed exact and cleared the confirmation median gate."
            if gate_passed
            else "The full-surface confirmation sweep did not yet clear the exactness-plus-median gate."
        ),
    }


def execute_probe(
    *,
    probe: ProbeImplementation,
    surface_records: tuple[SurfaceCaseRecord, ...],
    probe_cases: tuple[ProbeCase, ...],
) -> dict[str, object]:
    probe_rows = [
        profile_surface_record(
            probe_case.record,
            probe,
            selection_rank=probe_case.selection_rank,
            probe_role=probe_case.probe_role,
            focus_reason=probe_case.focus_reason,
            selection_rule=probe_case.selection_rule,
        )
        for probe_case in probe_cases
    ]
    target_gate = assess_target_gate(probe_rows)
    confirmation_rows: list[dict[str, object]] = []
    if target_gate["gate_passed"]:
        confirmation_rows = [profile_surface_record(record, probe) for record in surface_records]
    confirmation_summary = assess_confirmation(confirmation_rows)
    return {
        "probe_id": probe.probe_id,
        "probe_label": probe.probe_label,
        "status": probe.status,
        "probe_strategy": probe.probe_strategy,
        "stack_strategy": probe.stack_strategy,
        "memory_strategy": probe.memory_strategy,
        "probe_rows": probe_rows,
        "target_gate": target_gate,
        "confirmation_rows": confirmation_rows,
        "confirmation": confirmation_summary,
    }


def should_run_staged_followup(run: dict[str, object]) -> bool:
    target_gate = run["target_gate"]
    confirmation = run["confirmation"]
    return bool(target_gate["retry_eligible"]) or (
        bool(target_gate["gate_passed"]) and not bool(confirmation["gate_passed"])
    )


def build_probe_history_rows(probe_runs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for run in probe_runs:
        target_gate = run["target_gate"]
        confirmation = run["confirmation"]
        rows.append(
            {
                "probe_id": run["probe_id"],
                "probe_strategy": run["probe_strategy"],
                "status": run["status"],
                "target_exact": target_gate["target_exact"],
                "control_exact": target_gate["control_exact"],
                "target_speedup_vs_r17_accelerated": target_gate["target_speedup_vs_r17_accelerated"],
                "target_gate_passed": target_gate["gate_passed"],
                "retry_eligible": target_gate["retry_eligible"],
                "confirmation_ran": bool(confirmation["row_count"]),
                "confirmation_row_count": confirmation["row_count"],
                "confirmation_exact_row_count": confirmation["exact_row_count"],
                "confirmation_median_speedup_vs_r17_accelerated": confirmation["median_speedup_vs_r17_accelerated"],
                "confirmation_gate_passed": confirmation["gate_passed"],
            }
        )
    return rows


def build_summary(
    *,
    probe_cases: tuple[ProbeCase, ...],
    address_profiles: list[dict[str, object]],
    probe_runs: list[dict[str, object]],
) -> dict[str, object]:
    final_run = probe_runs[-1]
    target_row = next(row for row in final_run["probe_rows"] if row["probe_role"] == "target")
    control_row = next(row for row in final_run["probe_rows"] if row["probe_role"] == "control")
    target_gate = final_run["target_gate"]
    confirmation = final_run["confirmation"]
    probe_history = build_probe_history_rows(probe_runs)
    confirmed = bool(confirmation["gate_passed"])

    supported_here = [
        "R18 stays comparator-only on the same lowered D0 endpoint and only changes the exact runtime retrieval implementation.",
        f"The focused probe remains bounded to `{target_row['program_name']}` plus matched control `{control_row['program_name']}`.",
        f"Executed probes: {', '.join(run['probe_id'] for run in probe_runs)}.",
    ]
    if confirmed:
        supported_here.append(
            f"The final probe kept {confirmation['exact_row_count']}/{confirmation['row_count']} admitted rows exact and improved the median accelerated baseline by {confirmation['median_speedup_vs_r17_accelerated']:.3f}x."
        )
    elif len(probe_runs) == 1 and bool(target_gate["retry_eligible"]):
        supported_here.append("The pointer-like probe stayed exact enough to justify one deterministic staged retry.")
    elif len(probe_runs) == 2:
        supported_here.append("The staged deterministic retry was exercised as the final bounded closeout probe before refreeze.")

    unsupported_here = [
        "R18 does not widen beyond the admitted D0 surface or convert the runtime repair packet into a broader headline claim.",
        "The exact runtime probes do not by themselves prove arbitrary compiled-language execution or a general softmax/MHA replacement.",
    ]
    if not confirmed:
        unsupported_here.append("The current R18 packet did not close as a confirmed full-surface runtime repair win.")

    return {
        "status": final_run["status"],
        "probe_strategy": final_run["probe_strategy"],
        "executed_probe_ids": [run["probe_id"] for run in probe_runs],
        "probe_case_count": len(probe_cases),
        "full_surface_case_count": 8,
        "target_program_name": target_row["program_name"],
        "control_program_name": control_row["program_name"],
        "target_gate": target_gate,
        "confirmation_ran": bool(confirmation["row_count"]),
        "confirmation": confirmation,
        "frontier_recheck_hint": "conditional_plan_required" if confirmed else "blocked",
        "address_profiles": [
            {
                "program_name": profile["program_name"],
                "family": profile["family"],
                "memory_operation_count": profile["memory_operation_count"],
                "unique_address_count": profile["unique_address_count"],
                "hottest_address": profile["hottest_address"],
            }
            for profile in address_profiles
        ],
        "probe_history": probe_history,
        "claim_impact": {
            "status": "r18_runtime_repair_confirmed" if confirmed else "r18_runtime_repair_not_confirmed",
            "next_lane": "H17_refreeze_and_conditional_frontier_recheck",
            "next_probe": None,
            "supported_here": supported_here,
            "unsupported_here": unsupported_here,
            "distilled_result": {
                "executed_probe_count": len(probe_runs),
                "final_target_speedup_vs_r17_accelerated": target_gate["target_speedup_vs_r17_accelerated"],
                "final_confirmation_median_speedup_vs_r17_accelerated": confirmation[
                    "median_speedup_vs_r17_accelerated"
                ],
                "final_confirmation_exact_row_count": confirmation["exact_row_count"],
                "final_confirmation_row_count": confirmation["row_count"],
            },
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    surface_records = load_surface_case_records()
    probe_cases = load_probe_cases(surface_records)
    address_profiles = [build_memory_address_profile(probe_case.record) for probe_case in probe_cases]

    probe_runs = [
        execute_probe(
            probe=R18B_POINTER_LIKE,
            surface_records=surface_records,
            probe_cases=probe_cases,
        )
    ]
    if should_run_staged_followup(probe_runs[0]):
        probe_runs.append(
            execute_probe(
                probe=R18C_STAGED_EXACT,
                surface_records=surface_records,
                probe_cases=probe_cases,
            )
        )

    summary = build_summary(
        probe_cases=probe_cases,
        address_profiles=address_profiles,
        probe_runs=probe_runs,
    )
    all_probe_rows = [row for run in probe_runs for row in run["probe_rows"]]
    all_confirmation_rows = [row for run in probe_runs for row in run["confirmation_rows"]]
    probe_history = build_probe_history_rows(probe_runs)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "probe_selection.json",
        {
            "experiment": "r18_probe_selection",
            "environment": environment.as_dict(),
            "rows": [
                {
                    "selection_rank": probe_case.selection_rank,
                    "probe_role": probe_case.probe_role,
                    "focus_reason": probe_case.focus_reason,
                    "selection_rule": probe_case.selection_rule,
                    "program_name": probe_case.record.program_name,
                    "family": probe_case.record.family,
                    "source_lane": probe_case.record.source_lane,
                    "boundary_bearing_stream": probe_case.record.boundary_bearing_stream,
                }
                for probe_case in probe_cases
            ],
        },
    )
    write_json(
        OUT_DIR / "trace_address_profiles.json",
        {
            "experiment": "r18_trace_address_profiles",
            "environment": environment.as_dict(),
            "rows": address_profiles,
        },
    )
    write_json(
        OUT_DIR / "probe_history.json",
        {
            "experiment": "r18_probe_history",
            "environment": environment.as_dict(),
            "rows": probe_history,
        },
    )
    write_json(
        OUT_DIR / "probe_rows.json",
        {
            "experiment": "r18_probe_rows",
            "environment": environment.as_dict(),
            "rows": all_probe_rows,
        },
    )
    write_csv(OUT_DIR / "probe_rows.csv", all_probe_rows)
    write_json(
        OUT_DIR / "confirmation_rows.json",
        {
            "experiment": "r18_confirmation_rows",
            "environment": environment.as_dict(),
            "rows": all_confirmation_rows,
        },
    )
    write_csv(OUT_DIR / "confirmation_rows.csv", all_confirmation_rows)
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r18_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r18_d0_same_endpoint_runtime_repair_counterfactual",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R17_d0_full_surface_runtime_bridge/summary.json",
                "results/R17_d0_full_surface_runtime_bridge/runtime_bridge_rows.csv",
                "results/R17_d0_full_surface_runtime_bridge/focused_attribution_selection.json",
            ],
            "notes": [
                "R18 stays comparator-only and changes only the exact runtime retrieval implementation.",
                "R18b is the pointer-like exact probe; R18c is activated only if the pointer-like result leaves one bounded retry signal.",
                "After the final bounded probe, the packet closes under H17 rather than widening by narrative.",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R18 D0 Same-Endpoint Runtime Repair Counterfactual\n\n"
        "Comparator-only counterfactual outputs for the bounded R18 runtime repair packet.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `probe_selection.json`\n"
        "- `trace_address_profiles.json`\n"
        "- `probe_history.json`\n"
        "- `probe_rows.json`\n"
        "- `probe_rows.csv`\n"
        "- `confirmation_rows.json`\n"
        "- `confirmation_rows.csv`\n"
        "- `claim_impact.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
