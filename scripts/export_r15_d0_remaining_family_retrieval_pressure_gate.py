"""Export the remaining-family R15 retrieval-pressure gate on the same D0 endpoint."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from statistics import median

from bytecode import (
    RetrievalPressureCase,
    StressReferenceCase,
    helper_checkpoint_braid_program,
    indirect_counter_bank_program,
    lower_program,
    r15_d0_remaining_family_retrieval_pressure_cases,
    run_stress_reference_harness,
    stack_memory_braid_program,
    subroutine_braid_program,
)
from exec_trace import TraceInterpreter
from model import (
    config_for_operations,
    extract_memory_operations,
    extract_stack_slot_operations,
    run_latest_write_decode,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R15_d0_remaining_family_retrieval_pressure_gate"
PARITY_TOP_CASES = 2
PARITY_MAX_LOADS_PER_SPACE = 64


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def median_or_none(values: list[float]) -> float | None:
    return median(values) if values else None


def ratio_or_none(numerator: int | float, denominator: int | float) -> float | None:
    if denominator == 0:
        return None
    return float(numerator) / float(denominator)


def route_bucket_from_mismatch_class(mismatch_class: str | None) -> str:
    if mismatch_class is None:
        return "admitted"
    if mismatch_class in {
        "trace_disagreement",
        "final_state_disagreement",
        "linear_reference_mismatch",
        "accelerated_reference_mismatch",
        "decode_parity_mismatch",
    }:
        return "d0_contradiction_candidate"
    return "harness_or_annotation"


def _first_decode_mismatch_step(observations) -> int | None:
    for observation in observations:
        if not (
            observation.expected_value == observation.linear_value == observation.accelerated_value
        ):
            return observation.step
    return None


def _sample_operations_for_decode_parity(
    operations,
    *,
    max_loads: int,
):
    load_count = sum(operation.kind == "load" for operation in operations)
    if load_count <= max_loads:
        return tuple(operations), load_count, load_count
    if max_loads <= 0:
        raise ValueError("max_loads must be positive for decode parity sampling.")

    if max_loads == 1:
        selected_load_ordinals = {load_count - 1}
    else:
        selected_load_ordinals = {
            (index * (load_count - 1)) // (max_loads - 1)
            for index in range(max_loads)
        }

    sampled_operations = []
    load_ordinal = 0
    for operation in operations:
        if operation.kind == "store":
            sampled_operations.append(operation)
            continue
        if load_ordinal in selected_load_ordinals:
            sampled_operations.append(operation)
        load_ordinal += 1
    return tuple(sampled_operations), len(selected_load_ordinals), load_count


def _run_sampled_decode_parity(operations):
    sampled_operations, sampled_load_count, total_load_count = _sample_operations_for_decode_parity(
        operations,
        max_loads=PARITY_MAX_LOADS_PER_SPACE,
    )
    decode = run_latest_write_decode(
        sampled_operations,
        config_for_operations(sampled_operations),
    )
    return decode, sampled_load_count, total_load_count


def _case_metadata(case: RetrievalPressureCase) -> dict[str, object]:
    return {
        "family": case.family,
        "baseline_stage": case.baseline_stage,
        "baseline_program_name": case.baseline_program_name,
        "baseline_horizon_multiplier": case.baseline_horizon_multiplier,
        "baseline_start": case.baseline_start,
        "retrieval_horizon_multiplier": case.retrieval_horizon_multiplier,
        "scaled_start": case.scaled_start,
    }


def _as_stress_reference_cases(cases: tuple[RetrievalPressureCase, ...]) -> tuple[StressReferenceCase, ...]:
    return tuple(
        StressReferenceCase(
            suite=case.suite,
            comparison_mode=case.comparison_mode,
            max_steps=case.max_steps,
            program=case.program,
            diagnostic_surface=case.diagnostic_surface,
        )
        for case in cases
    )


def build_baseline_program(case: RetrievalPressureCase):
    match case.family:
        case "indirect_counter_bank":
            return indirect_counter_bank_program(case.baseline_start, counter_address=32, accumulator_address=33)
        case "helper_checkpoint_braid":
            return helper_checkpoint_braid_program(case.baseline_start, base_address=280, selector_seed=0)
        case "subroutine_braid":
            return subroutine_braid_program(case.baseline_start, base_address=96)
        case "stack_memory_braid":
            return stack_memory_braid_program(case.baseline_start, base_address=112)
        case _:
            raise ValueError(f"Unsupported R15 family: {case.family}")


def build_exact_rows(cases: tuple[RetrievalPressureCase, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case, row in zip(cases, run_stress_reference_harness(_as_stress_reference_cases(cases)), strict=True):
        payload = dict(row)
        payload.update(_case_metadata(case))
        payload["route_bucket"] = route_bucket_from_mismatch_class(payload["mismatch_class"])
        rows.append(payload)
    return rows


def exact_admitted_names(exact_rows: list[dict[str, object]]) -> set[str]:
    return {
        str(row["program_name"])
        for row in exact_rows
        if str(row["route_bucket"]) == "admitted"
    }


def build_decode_parity_rows(
    cases: tuple[RetrievalPressureCase, ...],
    exact_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    admitted_names = exact_admitted_names(exact_rows)
    focus_cases = sorted(
        (case for case in cases if case.program.name in admitted_names),
        key=lambda item: (item.max_steps, item.scaled_start, item.program.name),
        reverse=True,
    )[:PARITY_TOP_CASES]
    rows: list[dict[str, object]] = []

    for case in sorted(focus_cases, key=lambda item: (item.family, item.program.name)):
        lowered_program = lower_program(case.program)
        try:
            reference = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
            memory_decode, memory_sampled_load_count, memory_total_load_count = _run_sampled_decode_parity(
                extract_memory_operations(reference.events)
            )
            stack_decode, stack_sampled_load_count, stack_total_load_count = _run_sampled_decode_parity(
                extract_stack_slot_operations(reference.events)
            )
            memory_mismatch_count = sum(
                not (
                    observation.expected_value == observation.linear_value == observation.accelerated_value
                )
                for observation in memory_decode.observations
            )
            stack_mismatch_count = sum(
                not (
                    observation.expected_value == observation.linear_value == observation.accelerated_value
                )
                for observation in stack_decode.observations
            )

            mismatch_class: str | None = None
            failure_reason: str | None = None
            if memory_mismatch_count or stack_mismatch_count:
                mismatch_class = "decode_parity_mismatch"
                failure_reason = "Linear and accelerated latest-write decode do not agree on the extracted retrieval traces."

            row = {
                **_case_metadata(case),
                "program_name": case.program.name,
                "comparison_mode": case.comparison_mode,
                "max_steps": case.max_steps,
                "lowered_program_name": lowered_program.name,
                "reference_step_count": reference.final_state.steps,
                "parity_probe_mode": "uniform_load_probe",
                "parity_probe_max_loads_per_space": PARITY_MAX_LOADS_PER_SPACE,
                "memory_observation_count": len(memory_decode.observations),
                "memory_sampled_observation_count": memory_sampled_load_count,
                "memory_total_observation_count": memory_total_load_count,
                "stack_observation_count": len(stack_decode.observations),
                "stack_sampled_observation_count": stack_sampled_load_count,
                "stack_total_observation_count": stack_total_load_count,
                "memory_exact_read_agreement": memory_mismatch_count == 0,
                "stack_exact_read_agreement": stack_mismatch_count == 0,
                "memory_first_mismatch_step": _first_decode_mismatch_step(memory_decode.observations),
                "stack_first_mismatch_step": _first_decode_mismatch_step(stack_decode.observations),
                "mismatch_class": mismatch_class,
                "failure_reason": failure_reason,
            }
        except Exception as exc:  # pragma: no cover - defensive export guard
            row = {
                **_case_metadata(case),
                "program_name": case.program.name,
                "comparison_mode": case.comparison_mode,
                "max_steps": case.max_steps,
                "lowered_program_name": lowered_program.name,
                "reference_step_count": None,
                "parity_probe_mode": "uniform_load_probe",
                "parity_probe_max_loads_per_space": PARITY_MAX_LOADS_PER_SPACE,
                "memory_observation_count": 0,
                "memory_sampled_observation_count": 0,
                "memory_total_observation_count": 0,
                "stack_observation_count": 0,
                "stack_sampled_observation_count": 0,
                "stack_total_observation_count": 0,
                "memory_exact_read_agreement": False,
                "stack_exact_read_agreement": False,
                "memory_first_mismatch_step": None,
                "stack_first_mismatch_step": None,
                "mismatch_class": "runtime_exception",
                "failure_reason": f"{type(exc).__name__}: {exc}",
            }

        row["route_bucket"] = route_bucket_from_mismatch_class(row["mismatch_class"])
        rows.append(row)
    return rows


def _space_metrics(operations, *, include_default: bool, prefix: str) -> dict[str, int]:
    write_counts: defaultdict[int, int] = defaultdict(int)
    read_candidate_depths: list[int] = []
    read_addresses: set[int] = set()
    write_addresses: set[int] = set()

    for operation in operations:
        if operation.kind == "store":
            write_counts[operation.address] += 1
            write_addresses.add(operation.address)
            continue

        base_depth = 1 if include_default else 0
        read_candidate_depths.append(write_counts[operation.address] + base_depth)
        read_addresses.add(operation.address)

    history_depths = list(write_counts.values())
    return {
        f"{prefix}_operation_count": len(operations),
        f"{prefix}_read_count": sum(operation.kind == "load" for operation in operations),
        f"{prefix}_write_count": sum(operation.kind == "store" for operation in operations),
        f"{prefix}_unique_address_count": len({operation.address for operation in operations}),
        f"{prefix}_unique_read_address_count": len(read_addresses),
        f"{prefix}_unique_write_address_count": len(write_addresses),
        f"{prefix}_reused_write_address_count": sum(depth > 1 for depth in history_depths),
        f"{prefix}_max_history_depth": max(history_depths, default=0),
        f"{prefix}_max_candidate_depth": max(read_candidate_depths, default=0),
        f"{prefix}_total_candidate_depth": sum(read_candidate_depths),
    }


def build_pressure_metrics(program, *, max_steps: int) -> dict[str, object]:
    lowered_program = lower_program(program)
    reference = TraceInterpreter().run(lowered_program, max_steps=max_steps)
    events = reference.events
    memory_ops = extract_memory_operations(events)
    stack_ops = extract_stack_slot_operations(events)
    branch_event_count = sum(event.branch_taken is not None for event in events)
    taken_branch_count = sum(event.branch_taken is True for event in events)
    control_transfer_count = sum(
        getattr(event.opcode, "name", str(event.opcode)) in {"JMP", "JZ", "CALL", "RET"}
        for event in events
    )
    max_stack_depth = max((event.stack_depth_after for event in events), default=0)

    metrics: dict[str, object] = {
        "program_name": program.name,
        "event_count": len(events),
        "step_count": reference.final_state.steps,
        "branch_event_count": branch_event_count,
        "taken_branch_count": taken_branch_count,
        "control_transfer_count": control_transfer_count,
        "max_stack_depth": max_stack_depth,
    }
    metrics.update(_space_metrics(memory_ops, include_default=True, prefix="memory"))
    metrics.update(_space_metrics(stack_ops, include_default=False, prefix="stack"))
    metrics["total_read_count"] = int(metrics["memory_read_count"]) + int(metrics["stack_read_count"])
    metrics["total_write_count"] = int(metrics["memory_write_count"]) + int(metrics["stack_write_count"])
    metrics["total_candidate_depth"] = int(metrics["memory_total_candidate_depth"]) + int(
        metrics["stack_total_candidate_depth"]
    )
    return metrics


def build_pressure_rows(
    cases: tuple[RetrievalPressureCase, ...],
    exact_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    admitted_names = exact_admitted_names(exact_rows)
    rows: list[dict[str, object]] = []
    growth_fields = (
        "event_count",
        "total_read_count",
        "total_write_count",
        "total_candidate_depth",
        "memory_max_candidate_depth",
        "stack_max_candidate_depth",
        "branch_event_count",
        "control_transfer_count",
        "max_stack_depth",
    )

    for case in cases:
        if case.program.name not in admitted_names:
            continue

        source_program = build_baseline_program(case)
        source_max_steps = int(
            case.max_steps * case.baseline_horizon_multiplier / case.retrieval_horizon_multiplier
        )
        source_metrics = build_pressure_metrics(source_program, max_steps=source_max_steps)
        current_metrics = build_pressure_metrics(case.program, max_steps=case.max_steps)
        row: dict[str, object] = {
            **_case_metadata(case),
            "program_name": case.program.name,
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            **current_metrics,
        }
        for key, value in source_metrics.items():
            row[f"source_{key}"] = value
        for field in growth_fields:
            row[f"{field}_growth_vs_source"] = ratio_or_none(
                int(current_metrics[field]),
                int(source_metrics[field]),
            )
        rows.append(row)
    return rows


def build_family_pressure_summary(pressure_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for row in pressure_rows:
        grouped[str(row["family"])].append(row)

    rows: list[dict[str, object]] = []
    for family, family_rows in sorted(grouped.items()):
        rows.append(
            {
                "family": family,
                "row_count": len(family_rows),
                "max_retrieval_horizon_multiplier": max(
                    int(row["retrieval_horizon_multiplier"]) for row in family_rows
                ),
                "median_event_growth_vs_source": median(
                    float(row["event_count_growth_vs_source"]) for row in family_rows
                ),
                "median_total_candidate_growth_vs_source": median(
                    float(row["total_candidate_depth_growth_vs_source"]) for row in family_rows
                ),
                "max_memory_candidate_depth": max(int(row["memory_max_candidate_depth"]) for row in family_rows),
                "max_stack_candidate_depth": max(int(row["stack_max_candidate_depth"]) for row in family_rows),
            }
        )
    return rows


def build_summary(
    exact_rows: list[dict[str, object]],
    decode_parity_rows: list[dict[str, object]],
    pressure_rows: list[dict[str, object]],
    family_rows: list[dict[str, object]],
) -> dict[str, object]:
    exact_admitted_count = sum(str(row["route_bucket"]) == "admitted" for row in exact_rows)
    exact_harness_gap_count = sum(str(row["route_bucket"]) == "harness_or_annotation" for row in exact_rows)
    exact_contradiction_count = sum(
        str(row["route_bucket"]) == "d0_contradiction_candidate" for row in exact_rows
    )
    parity_harness_gap_count = sum(
        str(row["route_bucket"]) == "harness_or_annotation" for row in decode_parity_rows
    )
    parity_contradiction_count = sum(
        str(row["route_bucket"]) == "d0_contradiction_candidate" for row in decode_parity_rows
    )
    contradiction_candidate_count = exact_contradiction_count + parity_contradiction_count
    harness_gap_count = exact_harness_gap_count + parity_harness_gap_count

    if contradiction_candidate_count:
        gate_status = "stop_d0_contradiction_candidate"
        next_lane = "E1c_compiled_boundary_patch"
    elif harness_gap_count:
        gate_status = "stop_harness_or_annotation_gap"
        next_lane = "R15_d0_remaining_family_retrieval_pressure_gate"
    elif pressure_rows:
        gate_status = "go_remaining_family_retrieval_pressure_exact"
        next_lane = "R16_d0_real_trace_precision_boundary_saturation"
    else:
        gate_status = "stop_no_admitted_rows"
        next_lane = "R15_d0_remaining_family_retrieval_pressure_gate"

    return {
        "exact_suite": {
            "row_count": len(exact_rows),
            "exact_admitted_count": exact_admitted_count,
            "harness_or_annotation_count": exact_harness_gap_count,
            "contradiction_candidate_count": exact_contradiction_count,
        },
        "decode_parity": {
            "row_count": len(decode_parity_rows),
            "parity_match_count": 0,
            "exact_admitted_row_count": sum(str(row["route_bucket"]) == "admitted" for row in decode_parity_rows),
            "harness_or_annotation_count": parity_harness_gap_count,
            "contradiction_candidate_count": parity_contradiction_count,
        },
        "pressure": {
            "row_count": len(pressure_rows),
            "family_count": len(family_rows),
            "max_event_growth_vs_source": max(
                (float(row["event_count_growth_vs_source"]) for row in pressure_rows),
                default=0.0,
            ),
            "median_event_growth_vs_source": median_or_none(
                [float(row["event_count_growth_vs_source"]) for row in pressure_rows]
            ),
            "max_total_candidate_growth_vs_source": max(
                (float(row["total_candidate_depth_growth_vs_source"]) for row in pressure_rows),
                default=0.0,
            ),
            "median_total_candidate_growth_vs_source": median_or_none(
                [float(row["total_candidate_depth_growth_vs_source"]) for row in pressure_rows]
            ),
            "max_memory_candidate_depth": max(
                (int(row["memory_max_candidate_depth"]) for row in pressure_rows),
                default=0,
            ),
            "max_stack_candidate_depth": max(
                (int(row["stack_max_candidate_depth"]) for row in pressure_rows),
                default=0,
            ),
        },
        "claim_impact": {
            "gate_status": gate_status,
            "target_claims": ["D0"],
            "e1c_status": "triggered" if contradiction_candidate_count else "not_triggered",
            "next_lane": next_lane,
            "supported_here": [
                "R15 keeps the same direct-baseline endpoint fixed while filling the four remaining R6 family gaps under bounded retrieval pressure.",
                "Admitted rows export event, read/write, candidate-depth, stack-depth, and control-transfer growth explicitly rather than implying remaining-family pressure qualitatively.",
            ],
            "unsupported_here": [
                "R15 does not widen semantics, reopen arbitrary compiled-language claims, or justify a broader systems-superiority statement.",
                "Any contradiction-only route to E1c remains narrower than a general endpoint expansion.",
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = r15_d0_remaining_family_retrieval_pressure_cases()
    exact_rows = build_exact_rows(cases)
    decode_parity_rows = build_decode_parity_rows(cases, exact_rows)
    pressure_rows = build_pressure_rows(cases, exact_rows)
    family_rows = build_family_pressure_summary(pressure_rows)
    summary = build_summary(exact_rows, decode_parity_rows, pressure_rows, family_rows)

    summary["decode_parity"]["parity_match_count"] = sum(
        row["mismatch_class"] is None for row in decode_parity_rows
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "exact_suite_rows.json",
        {
            "experiment": "r15_d0_remaining_family_retrieval_pressure_exact_suite",
            "environment": environment.as_dict(),
            "rows": exact_rows,
        },
    )
    write_json(
        OUT_DIR / "decode_parity_rows.json",
        {
            "experiment": "r15_d0_remaining_family_retrieval_pressure_decode_parity",
            "environment": environment.as_dict(),
            "rows": decode_parity_rows,
        },
    )
    write_json(
        OUT_DIR / "pressure_rows.json",
        {
            "experiment": "r15_d0_remaining_family_retrieval_pressure_rows",
            "environment": environment.as_dict(),
            "rows": pressure_rows,
        },
    )
    write_json(
        OUT_DIR / "family_pressure_summary.json",
        {
            "experiment": "r15_d0_remaining_family_retrieval_pressure_family_summary",
            "environment": environment.as_dict(),
            "rows": family_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r15_d0_remaining_family_retrieval_pressure_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r15_d0_remaining_family_retrieval_pressure_gate",
            "environment": environment.as_dict(),
            "notes": [
                "R15 keeps the same endpoint fixed and raises retrieval pressure only on the four R6 families that R8 did not previously cover.",
                "The remaining-family suite is limited to one 10x retrieval-horizon row from each admitted R6 family that was missing from R8.",
                "Linear-vs-Hull decode parity stays bounded to a uniform-load probe on the top two heaviest admitted remaining-family rows so the gate remains executable under unattended runs.",
                "Pressure is exported quantitatively as event, read/write, candidate-depth, stack-depth, and control-transfer growth relative to the admitted R6 8x rows.",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R15 D0 Remaining-Family Retrieval-Pressure Gate",
                "",
                "Machine-readable export for the bounded remaining-family same-endpoint",
                "retrieval-pressure gate on the current D0 endpoint.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `exact_suite_rows.json`",
                "- `decode_parity_rows.json`",
                "- `pressure_rows.json`",
                "- `family_pressure_summary.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
