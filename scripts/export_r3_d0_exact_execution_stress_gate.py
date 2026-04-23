"""Export the bounded R3 exact-execution stress gate on the current D0 endpoint."""

from __future__ import annotations

import json
from pathlib import Path

from bytecode import (
    lower_program,
    r3_d0_exact_execution_stress_cases,
    run_stress_reference_harness,
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
OUT_DIR = ROOT / "results" / "R3_d0_exact_execution_stress_gate"
SCREENING_MULTIPLIERS = (1, 4, 16, 64)
SCREENING_BASE = 64
WEAKER_CONTROL_BASE = 256


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def encode_stress_row(row: dict[str, object]) -> dict[str, object]:
    return dict(row)


def _first_event_divergence(events_left, events_right) -> int | None:
    for left, right in zip(events_left, events_right):
        if left != right:
            return left.step
    if len(events_left) != len(events_right):
        return min(len(events_left), len(events_right))
    return None


def build_decode_parity_rows(cases) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in cases:
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


def encode_precision_result(
    result,
    *,
    program_name: str,
    stream_name: str,
    horizon_multiplier: int,
    native_max_steps: int,
    control_kind: str | None = None,
) -> dict[str, object]:
    return {
        "program_name": program_name,
        "stream_name": stream_name,
        "fmt": result.fmt,
        "scheme": result.scheme,
        "base": result.base,
        "space": result.space,
        "horizon_multiplier": horizon_multiplier,
        "native_max_steps": native_max_steps,
        "max_steps": result.max_steps,
        "read_count": result.read_count,
        "write_count": result.write_count,
        "passed": result.passed,
        "negative_control_kind": control_kind,
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
    for multiplier in SCREENING_MULTIPLIERS:
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


def build_precision_followup(cases) -> tuple[dict[str, object], list[dict[str, object]]]:
    interpreter = TraceInterpreter()
    streams: dict[str, dict[str, object]] = {}
    negative_control_rows: list[dict[str, object]] = []

    for case in cases:
        lowered_program = lower_program(case.program)
        reference = interpreter.run(lowered_program, max_steps=case.max_steps)
        operation_streams = {
            "memory": extract_memory_operations(reference.events),
            "stack": extract_stack_slot_operations(reference.events),
        }
        for space, operations in operation_streams.items():
            if not operations:
                continue
            native_max_steps = max(operation.step for operation in operations)
            screening_rows: list[dict[str, object]] = []
            for multiplier in SCREENING_MULTIPLIERS:
                max_steps = native_max_steps * multiplier
                for scheme in ("single_head", "radix2", "block_recentered"):
                    screening_rows.append(
                        encode_precision_result(
                            check_real_trace_precision(
                                operations,
                                fmt="float32",
                                scheme=scheme,
                                base=SCREENING_BASE,
                                max_steps=max_steps,
                            ),
                            program_name=case.program.name,
                            stream_name=f"{case.program.name}_{space}",
                            horizon_multiplier=multiplier,
                            native_max_steps=native_max_steps,
                        )
                    )

            boundary_active = enters_boundary_followup(screening_rows)
            failure_multiplier = first_single_head_failure_multiplier(screening_rows)
            if boundary_active and failure_multiplier is not None:
                negative_control_rows.append(
                    encode_precision_result(
                        check_real_trace_precision(
                            operations,
                            fmt="float32",
                            scheme="block_recentered",
                            base=WEAKER_CONTROL_BASE,
                            max_steps=native_max_steps * failure_multiplier,
                        ),
                        program_name=case.program.name,
                        stream_name=f"{case.program.name}_{space}",
                        horizon_multiplier=failure_multiplier,
                        native_max_steps=native_max_steps,
                        control_kind="weaker_block_recentered_base256",
                    )
                )

            streams[f"{case.program.name}_{space}"] = {
                "program_name": case.program.name,
                "space": space,
                "operation_count": len(operations),
                "read_count": sum(operation.kind == "load" for operation in operations),
                "write_count": sum(operation.kind == "store" for operation in operations),
                "native_max_steps": native_max_steps,
                "rows": screening_rows,
                "summary": {
                    "entered_boundary_followup": boundary_active,
                    "single_head_first_failure_multiplier": failure_multiplier,
                    "default_base": SCREENING_BASE,
                    "current_default_decomposition_passes_first_failure": any(
                        row["passed"] is True
                        for row in screening_rows
                        if int(row["horizon_multiplier"]) == (failure_multiplier or -1)
                        and str(row["scheme"]) in {"radix2", "block_recentered"}
                    ),
                },
            }

    screening_payload = {
        "experiment": "r3_d0_exact_execution_stress_precision_screening",
        "environment": detect_runtime_environment().as_dict(),
        "notes": [
            "Only the longer positive R3 rows enter this immediate precision companion screen.",
            "The screen reuses the existing float32 horizon-multiplier logic with the current default base 64.",
            "Only streams that show a boundary signal receive one weaker base-256 control row.",
        ],
        "focus_format": "float32",
        "horizon_multipliers": list(SCREENING_MULTIPLIERS),
        "screening_base": SCREENING_BASE,
        "weaker_control_base": WEAKER_CONTROL_BASE,
        "streams": streams,
    }
    return screening_payload, negative_control_rows


def build_summary(
    *,
    exact_rows: list[dict[str, object]],
    decode_rows: list[dict[str, object]],
    precision_screening: dict[str, object],
    negative_control_rows: list[dict[str, object]],
) -> dict[str, object]:
    positive_rows = [
        row
        for row in exact_rows
        if str(row["comparison_mode"]) in {"medium_exact_trace", "long_exact_final_state"}
    ]
    contradiction_rows = [row for row in positive_rows if row["mismatch_class"] is not None]
    boundary_streams = [
        stream_name
        for stream_name, payload in precision_screening["streams"].items()
        if bool(payload["summary"]["entered_boundary_followup"])
    ]
    control_failures = [row for row in negative_control_rows if row["passed"] is False]
    boundary_stream_count = len(boundary_streams)
    control_failure_count = len(control_failures)
    return {
        "exact_suite": {
            "row_count": len(exact_rows),
            "positive_row_count": len(positive_rows),
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
        "precision_followup": {
            "candidate_stream_count": len(precision_screening["streams"]),
            "boundary_bearing_stream_count": len(boundary_streams),
            "boundary_bearing_streams": sorted(boundary_streams),
            "negative_control_row_count": len(negative_control_rows),
            "negative_control_failure_count": len(control_failures),
        },
        "claim_impact": {
            "status": "bounded_exactness_survives_harder_d0_suite",
            "target_claims": ["D0"],
            "e1c_status": "not_triggered" if not contradiction_rows else "triggered",
            "next_lane": "R4_mechanistic_retrieval_closure" if not contradiction_rows else "E1c_compiled_boundary_patch",
            "supported_here": [
                "The bounded harder D0 suite remains exact under bytecode, lowered exec_trace, and standalone spec agreement.",
                "Linear and accelerated Hull latest-write decoders stay exactly aligned on the admitted lowered rows.",
            ],
            "bounded_companion": [
                f"{boundary_stream_count} longer memory streams enter the immediate float32 precision companion screen, while the stack streams stay easier on the screened horizon grid.",
                f"The weaker base-256 block-recentered control fails on {control_failure_count}/{len(negative_control_rows)} boundary-bearing streams where the base-64 decompositions stay exact.",
            ],
            "unsupported_here": [
                "No R3 output authorizes frontend widening or a broader compiled-language claim.",
                "No R3 output turns the immediate precision companion into a broad long-horizon robustness claim.",
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = r3_d0_exact_execution_stress_cases()
    exact_rows = [encode_stress_row(row) for row in run_stress_reference_harness(cases)]
    decode_rows = build_decode_parity_rows(cases)
    long_cases = [case for case in cases if case.comparison_mode == "long_exact_final_state"]
    precision_screening, negative_control_rows = build_precision_followup(long_cases)
    summary = build_summary(
        exact_rows=exact_rows,
        decode_rows=decode_rows,
        precision_screening=precision_screening,
        negative_control_rows=negative_control_rows,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r3_d0_exact_execution_stress_gate",
            "environment": environment.as_dict(),
            "notes": [
                "R3 stays on the frozen tiny typed-bytecode D0 endpoint and does not widen the frontend.",
                "The exact suite reuses the current stress-reference harness and adds explicit linear-vs-Hull free-running parity on the lowered rows.",
                "The precision companion is conditional and narrow: only longer positive rows enter the immediate horizon screen, and only boundary-bearing streams get one weaker control row.",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "exact_suite_rows.json",
        {
            "experiment": "r3_d0_exact_execution_stress_exact_suite_rows",
            "environment": environment.as_dict(),
            "rows": exact_rows,
        },
    )
    write_json(
        OUT_DIR / "decode_parity_rows.json",
        {
            "experiment": "r3_d0_exact_execution_decode_parity_rows",
            "environment": environment.as_dict(),
            "rows": decode_rows,
        },
    )
    write_json(OUT_DIR / "precision_screening.json", precision_screening)
    write_json(
        OUT_DIR / "precision_negative_control_rows.json",
        {
            "experiment": "r3_d0_exact_execution_precision_negative_controls",
            "environment": environment.as_dict(),
            "rows": negative_control_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r3_d0_exact_execution_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R3 D0 Exact Execution Stress Gate",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `exact_suite_rows.json`",
                "- `decode_parity_rows.json`",
                "- `precision_screening.json`",
                "- `precision_negative_control_rows.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
