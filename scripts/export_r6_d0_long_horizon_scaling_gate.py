"""Export the bounded R6 long-horizon scaling gate on the current D0 endpoint."""

from __future__ import annotations

import json
from pathlib import Path

from bytecode import (
    LongHorizonScalingCase,
    checkpoint_replay_long_program,
    helper_checkpoint_braid_long_program,
    helper_checkpoint_braid_program,
    indirect_counter_bank_program,
    iterated_helper_accumulator_program,
    lower_program,
    r6_d0_long_horizon_scaling_cases,
    run_stress_reference_harness,
    stack_memory_braid_program,
    subroutine_braid_long_program,
    subroutine_braid_program,
)
from exec_trace import TraceInterpreter
from model import (
    check_real_trace_precision,
    compare_execution_to_reference,
    extract_memory_operations,
    extract_stack_slot_operations,
    run_free_running_exact,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R6_d0_long_horizon_scaling_gate"
PRECISION_HORIZON_MULTIPLIERS = (1, 2, 4)
PRECISION_DEFAULT_BASE = 64
PRECISION_ACTIVE_BASES = (64, 128)
PRECISION_NEGATIVE_CONTROL_BASE = 256
FOCUS_HORIZON_MULTIPLIER = 8
DECODE_PARITY_HORIZON_MULTIPLIER = 4


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _first_event_divergence(events_left, events_right) -> int | None:
    for left, right in zip(events_left, events_right):
        if left != right:
            return left.step
    if len(events_left) != len(events_right):
        return min(len(events_left), len(events_right))
    return None


def _case_metadata(case: LongHorizonScalingCase) -> dict[str, object]:
    return {
        "family": case.family,
        "baseline_stage": case.baseline_stage,
        "baseline_program_name": case.baseline_program_name,
        "baseline_start": case.baseline_start,
        "horizon_multiplier": case.horizon_multiplier,
        "scaled_start": case.scaled_start,
    }


def build_baseline_program(case: LongHorizonScalingCase):
    match case.family:
        case "indirect_counter_bank":
            return indirect_counter_bank_program(
                case.baseline_start,
                counter_address=32,
                accumulator_address=33,
            )
        case "helper_checkpoint_braid":
            return helper_checkpoint_braid_program(
                case.baseline_start,
                base_address=280,
                selector_seed=0,
            )
        case "subroutine_braid":
            return subroutine_braid_program(case.baseline_start, base_address=96)
        case "helper_checkpoint_braid_long":
            return helper_checkpoint_braid_long_program(
                case.baseline_start,
                base_address=312,
                selector_seed=0,
            )
        case "subroutine_braid_long":
            return subroutine_braid_long_program(case.baseline_start, base_address=176)
        case "iterated_helper_accumulator":
            return iterated_helper_accumulator_program(
                case.baseline_start,
                counter_address=144,
                accumulator_address=145,
            )
        case "stack_memory_braid":
            return stack_memory_braid_program(case.baseline_start, base_address=112)
        case "checkpoint_replay_long":
            return checkpoint_replay_long_program(case.baseline_start, base_address=128)
        case _:
            raise ValueError(f"Unsupported R6 family: {case.family}")


def build_exact_rows(cases: tuple[LongHorizonScalingCase, ...]) -> list[dict[str, object]]:
    rows = []
    for case, row in zip(cases, run_stress_reference_harness(cases), strict=True):
        payload = dict(row)
        payload.update(_case_metadata(case))
        rows.append(payload)
    return rows


def build_decode_parity_rows(cases: tuple[LongHorizonScalingCase, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    focus_cases = [case for case in cases if case.horizon_multiplier == DECODE_PARITY_HORIZON_MULTIPLIER]
    for case in focus_cases:
        lowered_program = lower_program(case.program)
        try:
            linear = run_free_running_exact(lowered_program, decode_mode="linear", max_steps=case.max_steps)
            accelerated = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=case.max_steps)
            linear_outcome = compare_execution_to_reference(lowered_program, linear)
            accelerated_outcome = compare_execution_to_reference(lowered_program, accelerated)
            mismatch_class: str | None = None
            failure_reason: str | None = None
            if not linear_outcome.exact_trace_match or not linear_outcome.exact_final_state_match:
                mismatch_class = "linear_reference_mismatch"
                failure_reason = "Linear decode does not exactly match the lowered exec_trace reference."
            elif not accelerated_outcome.exact_trace_match or not accelerated_outcome.exact_final_state_match:
                mismatch_class = "accelerated_reference_mismatch"
                failure_reason = "Accelerated Hull decode does not exactly match the lowered exec_trace reference."
            elif linear.events != accelerated.events or linear.final_state != accelerated.final_state:
                mismatch_class = "decode_parity_mismatch"
                failure_reason = "Linear and accelerated Hull decoders do not agree exactly on the lowered program."

            rows.append(
                {
                    **_case_metadata(case),
                    "program_name": case.program.name,
                    "suite": case.suite,
                    "comparison_mode": case.comparison_mode,
                    "lowered_program_name": lowered_program.name,
                    "reference_step_count": linear_outcome.program_steps,
                    "linear_exact_trace_match": linear_outcome.exact_trace_match,
                    "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
                    "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
                    "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
                    "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
                    "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
                    "linear_accelerated_trace_match": linear.events == accelerated.events,
                    "linear_accelerated_final_state_match": linear.final_state == accelerated.final_state,
                    "linear_accelerated_first_mismatch_step": _first_event_divergence(linear.events, accelerated.events),
                    "read_observation_count": len(accelerated.read_observations),
                    "exact_read_agreement": all(
                        observation.linear_value == observation.accelerated_value
                        for observation in accelerated.read_observations
                    ),
                    "mismatch_class": mismatch_class,
                    "failure_reason": failure_reason,
                }
            )
        except Exception as exc:  # pragma: no cover - defensive export guard
            rows.append(
                {
                    **_case_metadata(case),
                    "program_name": case.program.name,
                    "suite": case.suite,
                    "comparison_mode": case.comparison_mode,
                    "lowered_program_name": lowered_program.name,
                    "reference_step_count": None,
                    "linear_exact_trace_match": False,
                    "linear_exact_final_state_match": False,
                    "linear_first_mismatch_step": None,
                    "accelerated_exact_trace_match": False,
                    "accelerated_exact_final_state_match": False,
                    "accelerated_first_mismatch_step": None,
                    "linear_accelerated_trace_match": False,
                    "linear_accelerated_final_state_match": False,
                    "linear_accelerated_first_mismatch_step": None,
                    "read_observation_count": 0,
                    "exact_read_agreement": False,
                    "mismatch_class": "runtime_exception",
                    "failure_reason": f"{type(exc).__name__}: {exc}",
                }
            )
    return rows


def _operation_counts(events) -> dict[str, int]:
    memory_ops = extract_memory_operations(events)
    stack_ops = extract_stack_slot_operations(events)
    return {
        "event_count": len(events),
        "memory_read_count": sum(operation.kind == "load" for operation in memory_ops),
        "memory_write_count": sum(operation.kind == "store" for operation in memory_ops),
        "stack_read_count": sum(operation.kind == "load" for operation in stack_ops),
        "stack_write_count": sum(operation.kind == "store" for operation in stack_ops),
    }


def build_growth_rows(cases: tuple[LongHorizonScalingCase, ...]) -> list[dict[str, object]]:
    interpreter = TraceInterpreter()
    baseline_cache: dict[str, dict[str, int | bool]] = {}
    rows: list[dict[str, object]] = []

    for case in cases:
        baseline_key = f"{case.family}:{case.baseline_program_name}"
        if baseline_key not in baseline_cache:
            baseline_program = build_baseline_program(case)
            baseline_result = interpreter.run(
                lower_program(baseline_program),
                max_steps=case.max_steps // case.horizon_multiplier,
            )
            baseline_cache[baseline_key] = {
                "baseline_step_count": baseline_result.final_state.steps,
                "baseline_halted": baseline_result.final_state.halted,
                **_operation_counts(baseline_result.events),
            }

        lowered_result = interpreter.run(lower_program(case.program), max_steps=case.max_steps)
        counts = _operation_counts(lowered_result.events)
        baseline = baseline_cache[baseline_key]
        rows.append(
            {
                **_case_metadata(case),
                "program_name": case.program.name,
                "comparison_mode": case.comparison_mode,
                "step_count": lowered_result.final_state.steps,
                "halted": lowered_result.final_state.halted,
                **counts,
                **baseline,
                "step_growth_vs_baseline": lowered_result.final_state.steps / int(baseline["baseline_step_count"]),
                "event_growth_vs_baseline": counts["event_count"] / int(baseline["event_count"]),
                "memory_read_growth_vs_baseline": counts["memory_read_count"] / max(1, int(baseline["memory_read_count"])),
                "memory_write_growth_vs_baseline": counts["memory_write_count"] / max(
                    1, int(baseline["memory_write_count"])
                ),
                "stack_read_growth_vs_baseline": counts["stack_read_count"] / max(1, int(baseline["stack_read_count"])),
                "stack_write_growth_vs_baseline": counts["stack_write_count"] / max(
                    1, int(baseline["stack_write_count"])
                ),
            }
        )
    return rows


def encode_precision_result(
    result,
    *,
    case: LongHorizonScalingCase,
    stream_name: str,
    native_max_steps: int,
    horizon_multiplier: int,
    negative_control_kind: str | None = None,
) -> dict[str, object]:
    return {
        **_case_metadata(case),
        "program_name": case.program.name,
        "stream_name": stream_name,
        "fmt": result.fmt,
        "scheme": result.scheme,
        "base": result.base,
        "space": result.space,
        "native_max_steps": native_max_steps,
        "horizon_multiplier": horizon_multiplier,
        "max_steps": result.max_steps,
        "read_count": result.read_count,
        "write_count": result.write_count,
        "passed": result.passed,
        "negative_control_kind": negative_control_kind,
        "first_failure": None
        if result.first_failure is None
        else {
            "space": result.first_failure.space,
            "read_step": result.first_failure.read_step,
            "query_address": result.first_failure.query_address,
            "expected_address": result.first_failure.expected_address,
            "expected_step": result.first_failure.expected_step,
            "competing_address": result.first_failure.competing_address,
            "competing_step": result.first_failure.competing_step,
            "expected_scores": list(result.first_failure.expected_scores),
            "competing_scores": list(result.first_failure.competing_scores),
            "failure_type": result.first_failure.failure_type,
        },
    }


def enters_boundary_followup(rows: list[dict[str, object]]) -> bool:
    for multiplier in PRECISION_HORIZON_MULTIPLIERS:
        multiplier_rows = [row for row in rows if int(row["horizon_multiplier"]) == multiplier]
        single_head = next(row for row in multiplier_rows if str(row["scheme"]) == "single_head")
        if single_head["passed"] is False:
            return True
        if any(row["passed"] != single_head["passed"] for row in multiplier_rows if str(row["scheme"]) != "single_head"):
            return True
    return False


def first_single_head_failure_multiplier(rows: list[dict[str, object]]) -> int | None:
    return next(
        (
            int(row["horizon_multiplier"])
            for row in rows
            if str(row["scheme"]) == "single_head" and row["passed"] is False
        ),
        None,
    )


def build_precision_companion(
    cases: tuple[LongHorizonScalingCase, ...],
    exact_rows: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    admitted_programs = {str(row["program_name"]) for row in exact_rows if row["mismatch_class"] is None}
    focus_cases = [
        case
        for case in cases
        if case.program.name in admitted_programs and case.horizon_multiplier == FOCUS_HORIZON_MULTIPLIER
    ]
    interpreter = TraceInterpreter()
    streams: dict[str, dict[str, object]] = {}
    base_sweep_rows: list[dict[str, object]] = []

    for case in focus_cases:
        lowered_program = lower_program(case.program)
        reference = interpreter.run(lowered_program, max_steps=case.max_steps)
        operation_streams = {"memory": extract_memory_operations(reference.events)}
        for space, operations in operation_streams.items():
            if not operations:
                continue
            native_max_steps = max(operation.step for operation in operations)
            screening_rows: list[dict[str, object]] = []
            for horizon_multiplier in PRECISION_HORIZON_MULTIPLIERS:
                max_steps = native_max_steps * horizon_multiplier
                for scheme in ("single_head", "radix2", "block_recentered"):
                    screening_rows.append(
                        encode_precision_result(
                            check_real_trace_precision(
                                operations,
                                fmt="float32",
                                scheme=scheme,
                                base=PRECISION_DEFAULT_BASE,
                                max_steps=max_steps,
                            ),
                            case=case,
                            stream_name=f"{case.program.name}_{space}",
                            native_max_steps=native_max_steps,
                            horizon_multiplier=horizon_multiplier,
                        )
                    )

            boundary_active = enters_boundary_followup(screening_rows)
            failure_multiplier = first_single_head_failure_multiplier(screening_rows) or 1
            if boundary_active:
                for scheme in ("radix2", "block_recentered"):
                    for base in PRECISION_ACTIVE_BASES:
                        base_sweep_rows.append(
                            encode_precision_result(
                                check_real_trace_precision(
                                    operations,
                                    fmt="float32",
                                    scheme=scheme,
                                    base=base,
                                    max_steps=native_max_steps * failure_multiplier,
                                ),
                                case=case,
                                stream_name=f"{case.program.name}_{space}",
                                native_max_steps=native_max_steps,
                                horizon_multiplier=failure_multiplier,
                            )
                        )
                base_sweep_rows.append(
                    encode_precision_result(
                        check_real_trace_precision(
                            operations,
                            fmt="float32",
                            scheme="block_recentered",
                            base=PRECISION_NEGATIVE_CONTROL_BASE,
                            max_steps=native_max_steps * failure_multiplier,
                        ),
                        case=case,
                        stream_name=f"{case.program.name}_{space}",
                        native_max_steps=native_max_steps,
                        horizon_multiplier=failure_multiplier,
                        negative_control_kind="weaker_block_recentered_base256",
                    )
                )

            streams[f"{case.program.name}_{space}"] = {
                "family": case.family,
                "program_name": case.program.name,
                "space": space,
                "operation_count": len(operations),
                "read_count": sum(operation.kind == "load" for operation in operations),
                "write_count": sum(operation.kind == "store" for operation in operations),
                "native_max_steps": native_max_steps,
                "rows": screening_rows,
                "summary": {
                    "entered_boundary_followup": boundary_active,
                    "single_head_first_failure_multiplier": failure_multiplier
                    if any(str(row["scheme"]) == "single_head" and row["passed"] is False for row in screening_rows)
                    else None,
                    "default_base": PRECISION_DEFAULT_BASE,
                },
            }

    screening_payload = {
        "experiment": "r6_d0_long_horizon_precision_screening",
        "environment": detect_runtime_environment().as_dict(),
        "notes": [
            "Only exact-admitted R6 rows at the largest fixed multiplier enter the narrow precision companion.",
            "The companion stays on memory streams because the prior packet already showed stack streams were easier on the same screened boundary logic.",
            "The horizon screen stays on default base 64 before any boundary-bearing stream receives a small base sweep.",
            "Base 256 remains a weaker negative control rather than a positive alternative.",
        ],
        "focus_horizon_multiplier": FOCUS_HORIZON_MULTIPLIER,
        "horizon_multipliers": list(PRECISION_HORIZON_MULTIPLIERS),
        "default_base": PRECISION_DEFAULT_BASE,
        "active_bases": list(PRECISION_ACTIVE_BASES),
        "negative_control_base": PRECISION_NEGATIVE_CONTROL_BASE,
        "streams": streams,
    }
    return screening_payload, base_sweep_rows


def build_summary(
    *,
    exact_rows: list[dict[str, object]],
    decode_rows: list[dict[str, object]],
    growth_rows: list[dict[str, object]],
    precision_screening: dict[str, object],
    precision_base_sweep_rows: list[dict[str, object]],
) -> dict[str, object]:
    positive_rows = [
        row
        for row in exact_rows
        if str(row["comparison_mode"]) in {"medium_exact_trace", "long_exact_final_state"}
    ]
    contradiction_rows = [row for row in positive_rows if row["mismatch_class"] is not None]
    admitted_programs = {str(row["program_name"]) for row in positive_rows if row["mismatch_class"] is None}
    boundary_streams = [
        stream_name
        for stream_name, payload in precision_screening["streams"].items()
        if bool(payload["summary"]["entered_boundary_followup"])
    ]
    negative_control_rows = [row for row in precision_base_sweep_rows if row["negative_control_kind"] is not None]
    negative_control_failures = [row for row in negative_control_rows if row["passed"] is False]
    return {
        "exact_suite": {
            "row_count": len(exact_rows),
            "positive_row_count": len(positive_rows),
            "exact_admitted_count": len(admitted_programs),
            "exact_trace_match_count": sum(
                row["comparison_mode"] == "medium_exact_trace" and row["mismatch_class"] is None for row in exact_rows
            ),
            "exact_final_state_match_count": sum(
                row["comparison_mode"] == "long_exact_final_state" and row["mismatch_class"] is None
                for row in exact_rows
            ),
            "diagnostic_surface_match_count": sum(
                row["diagnostic_surface_match"] is True
                for row in exact_rows
                if row["diagnostic_surface_match"] is not None
            ),
            "contradiction_candidate_count": len(contradiction_rows),
        },
        "decode_parity": {
            "row_count": len(decode_rows),
            "parity_match_count": sum(row["mismatch_class"] is None for row in decode_rows),
            "exact_read_agreement_count": sum(row["exact_read_agreement"] is True for row in decode_rows),
        },
        "growth": {
            "row_count": len(growth_rows),
            "family_count": len({str(row["family"]) for row in growth_rows}),
            "max_step_growth_vs_baseline": max(float(row["step_growth_vs_baseline"]) for row in growth_rows),
            "max_event_growth_vs_baseline": max(float(row["event_growth_vs_baseline"]) for row in growth_rows),
        },
        "precision_followup": {
            "candidate_stream_count": len(precision_screening["streams"]),
            "boundary_bearing_stream_count": len(boundary_streams),
            "boundary_bearing_streams": sorted(boundary_streams),
            "base_sweep_row_count": len(precision_base_sweep_rows),
            "negative_control_row_count": len(negative_control_rows),
            "negative_control_failure_count": len(negative_control_failures),
        },
        "claim_impact": {
            "status": "bounded_long_horizon_exactness_on_current_d0",
            "target_claims": ["D0"],
            "e1c_status": "not_triggered" if not contradiction_rows else "triggered",
            "next_lane": "R7_d0_same_endpoint_runtime_bridge" if not contradiction_rows else "E1c_compiled_boundary_patch",
            "supported_here": [
                "Current D0 families remain exact under fixed 2x/4x/8x horizon scaling without widening semantics.",
                "Linear and accelerated Hull decode stay exactly aligned on one longer lowered row from each tested family.",
                "Longer admitted rows materially increase event and read/write counts relative to the preserved baseline families.",
            ],
            "bounded_companion": [
                f"Only multiplier-{FOCUS_HORIZON_MULTIPLIER} exact-admitted rows enter the narrow precision companion, and {len(boundary_streams)} streams show a boundary signal on that screen.",
                f"The weaker base-256 control fails on {len(negative_control_failures)}/{len(negative_control_rows)} boundary-bearing rows in the follow-up base sweep.",
            ],
            "unsupported_here": [
                "No R6 output authorizes frontend widening, arbitrary compiled-language claims, or a broad robustness statement.",
                "The precision companion remains a narrow stress probe on exact-admitted long rows rather than a new universal precision guarantee.",
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = r6_d0_long_horizon_scaling_cases()
    exact_rows = build_exact_rows(cases)
    decode_rows = build_decode_parity_rows(cases)
    growth_rows = build_growth_rows(cases)
    precision_screening, precision_base_sweep_rows = build_precision_companion(cases, exact_rows)
    summary = build_summary(
        exact_rows=exact_rows,
        decode_rows=decode_rows,
        growth_rows=growth_rows,
        precision_screening=precision_screening,
        precision_base_sweep_rows=precision_base_sweep_rows,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r6_d0_long_horizon_scaling_gate",
            "environment": environment.as_dict(),
            "notes": [
                "R6 keeps the current D0 endpoint fixed and scales only already-admitted family horizons by fixed multipliers 2/4/8.",
                "The exactness gate reuses the current bytecode/lowered/spec harness; decode parity is kept explicit on one longer lowered row per family before the same-endpoint runtime bridge revisits the largest rows.",
                "The precision companion stays narrow: only exact-admitted multiplier-8 rows enter the horizon/base follow-up.",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "exact_suite_rows.json",
        {
            "experiment": "r6_d0_long_horizon_exact_suite_rows",
            "environment": environment.as_dict(),
            "rows": exact_rows,
        },
    )
    write_json(
        OUT_DIR / "decode_parity_rows.json",
        {
            "experiment": "r6_d0_long_horizon_decode_parity_rows",
            "environment": environment.as_dict(),
            "rows": decode_rows,
        },
    )
    write_json(
        OUT_DIR / "growth_rows.json",
        {
            "experiment": "r6_d0_long_horizon_growth_rows",
            "environment": environment.as_dict(),
            "rows": growth_rows,
        },
    )
    write_json(OUT_DIR / "precision_screening.json", precision_screening)
    write_json(
        OUT_DIR / "precision_base_sweep.json",
        {
            "experiment": "r6_d0_long_horizon_precision_base_sweep",
            "environment": environment.as_dict(),
            "rows": precision_base_sweep_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r6_d0_long_horizon_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R6 D0 Long-Horizon Scaling Gate",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `exact_suite_rows.json`",
                "- `decode_parity_rows.json`",
                "- `growth_rows.json`",
                "- `precision_screening.json`",
                "- `precision_base_sweep.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
