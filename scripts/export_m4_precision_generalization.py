"""Export broader real-trace precision evidence and failure taxonomy for M4-E."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from exec_trace import (
    TraceInterpreter,
    flagged_indirect_accumulator_program,
    hotspot_memory_rewrite_program,
    selector_checkpoint_bank_program,
    stack_fanout_sum_program,
)
from model import check_real_trace_precision, extract_memory_operations, extract_stack_slot_operations
from utils import detect_runtime_environment


HORIZON_MULTIPLIERS = (1, 4, 16, 64)
SCREENING_BASE = 64
BOUNDARY_BASES = (32, 64, 128, 256)


@dataclass(frozen=True, slots=True)
class ProgramSpec:
    family: str
    program_name: str
    program: object


@dataclass(frozen=True, slots=True)
class StreamSpec:
    family: str
    program_name: str
    stream_name: str
    operations: tuple


def encode_result(
    result,
    *,
    family: str,
    program_name: str,
    stream_name: str,
    horizon_multiplier: int,
    native_steps: int,
):
    return {
        "family": family,
        "program_name": program_name,
        "stream_name": stream_name,
        "fmt": result.fmt,
        "scheme": result.scheme,
        "base": result.base,
        "space": result.space,
        "horizon_multiplier": horizon_multiplier,
        "native_max_steps": native_steps,
        "max_steps": result.max_steps,
        "read_count": result.read_count,
        "write_count": result.write_count,
        "passed": result.passed,
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


def build_program_specs() -> tuple[ProgramSpec, ...]:
    return (
        ProgramSpec(
            "hotspot_memory_rewrite",
            "hotspot_memory_rewrite_12_a2048",
            hotspot_memory_rewrite_program(12, base_address=2048),
        ),
        ProgramSpec(
            "flagged_indirect_accumulator",
            "flagged_indirect_accumulator_10_a1024",
            flagged_indirect_accumulator_program(10, base_address=1024),
        ),
        ProgramSpec(
            "selector_checkpoint_bank",
            "selector_checkpoint_bank_9_a1536",
            selector_checkpoint_bank_program(9, base_address=1536),
        ),
        ProgramSpec(
            "stack_fanout_sum",
            "stack_fanout_sum_64_v1",
            stack_fanout_sum_program(64, base_value=1),
        ),
        ProgramSpec(
            "stack_fanout_sum",
            "stack_fanout_sum_256_v1",
            stack_fanout_sum_program(256, base_value=1),
        ),
    )


def build_streams() -> tuple[StreamSpec, ...]:
    interpreter = TraceInterpreter()
    streams: list[StreamSpec] = []
    for spec in build_program_specs():
        result = interpreter.run(spec.program)
        if spec.family == "stack_fanout_sum":
            stack_ops = extract_stack_slot_operations(result.events)
            if stack_ops:
                streams.append(
                    StreamSpec(
                        family=spec.family,
                        program_name=spec.program_name,
                        stream_name=f"{spec.program_name}_stack",
                        operations=stack_ops,
                    )
                )
            continue

        memory_ops = extract_memory_operations(result.events)
        if memory_ops:
            streams.append(
                StreamSpec(
                    family=spec.family,
                    program_name=spec.program_name,
                    stream_name=f"{spec.program_name}_memory",
                    operations=memory_ops,
                )
            )
    return tuple(streams)


def native_max_steps(operations) -> int:
    return max(operation.step for operation in operations)


def summarize_screening(rows: list[dict[str, object]], native_steps: int) -> dict[str, object]:
    single_fail = next(
        (
            row["horizon_multiplier"]
            for row in rows
            if row["scheme"] == "single_head" and row["passed"] is False
        ),
        None,
    )
    failure_types = sorted(
        {
            row["first_failure"]["failure_type"]
            for row in rows
            if row["first_failure"] is not None
        }
    )
    entered_boundary_sweep = enters_boundary_sweep(rows)
    return {
        "native_max_steps": native_steps,
        "screening_base": SCREENING_BASE,
        "first_failure_multiplier": single_fail,
        "failure_types": failure_types,
        "entered_boundary_sweep": entered_boundary_sweep,
    }


def enters_boundary_sweep(rows: list[dict[str, object]]) -> bool:
    for multiplier in HORIZON_MULTIPLIERS:
        multiplier_rows = [row for row in rows if row["horizon_multiplier"] == multiplier]
        single_head = next(row for row in multiplier_rows if row["scheme"] == "single_head")
        if single_head["passed"] is False:
            return True
        if any(row["passed"] != single_head["passed"] for row in multiplier_rows if row["scheme"] != "single_head"):
            return True
    return False


def main() -> None:
    environment = detect_runtime_environment()
    streams = build_streams()
    screening = {
        "experiment": "m4_precision_generalization_screening",
        "environment": environment.as_dict(),
        "notes": [
            "This batch broadens real-trace precision evidence beyond the earlier offset-heavy core.",
            "Stage 1 holds schemes fixed to single_head, radix2, and block_recentered, with base 64 as the current default screening point.",
            "Only streams with an actual boundary signal enter the second-stage base sweep.",
        ],
        "focus_format": "float32",
        "horizon_multipliers": list(HORIZON_MULTIPLIERS),
        "screening_base": SCREENING_BASE,
        "streams": {},
    }
    boundary = {
        "experiment": "m4_precision_generalization_boundary_sweep",
        "environment": environment.as_dict(),
        "notes": [
            "Only streams selected by the screening stage enter the boundary sweep.",
            "The boundary sweep widens the base search for radix2 and block_recentered while keeping single_head as the reference row.",
        ],
        "focus_format": "float32",
        "horizon_multipliers": list(HORIZON_MULTIPLIERS),
        "boundary_bases": list(BOUNDARY_BASES),
        "streams": {},
    }
    catalog: list[dict[str, object]] = []

    for stream in streams:
        native_steps = native_max_steps(stream.operations)
        screening_rows: list[dict[str, object]] = []
        for multiplier in HORIZON_MULTIPLIERS:
            max_steps = native_steps * multiplier
            screening_rows.append(
                encode_result(
                    check_real_trace_precision(
                        stream.operations,
                        fmt="float32",
                        scheme="single_head",
                        base=SCREENING_BASE,
                        max_steps=max_steps,
                    ),
                    family=stream.family,
                    program_name=stream.program_name,
                    stream_name=stream.stream_name,
                    horizon_multiplier=multiplier,
                    native_steps=native_steps,
                )
            )
            for scheme in ("radix2", "block_recentered"):
                screening_rows.append(
                    encode_result(
                        check_real_trace_precision(
                            stream.operations,
                            fmt="float32",
                            scheme=scheme,
                            base=SCREENING_BASE,
                            max_steps=max_steps,
                        ),
                        family=stream.family,
                        program_name=stream.program_name,
                        stream_name=stream.stream_name,
                        horizon_multiplier=multiplier,
                        native_steps=native_steps,
                    )
                )

        screening_summary = summarize_screening(screening_rows, native_steps)
        screening["streams"][stream.stream_name] = {
            "family": stream.family,
            "program_name": stream.program_name,
            "space": stream.operations[0].space,
            "operation_count": len(stream.operations),
            "read_count": sum(1 for operation in stream.operations if operation.kind == "load"),
            "write_count": sum(1 for operation in stream.operations if operation.kind == "store"),
            "native_max_steps": native_steps,
            "rows": screening_rows,
            "summary": screening_summary,
        }
        catalog.append(
            {
                "family": stream.family,
                "program_name": stream.program_name,
                "stream_name": stream.stream_name,
                "space": stream.operations[0].space,
                "operation_count": len(stream.operations),
                "read_count": sum(1 for operation in stream.operations if operation.kind == "load"),
                "write_count": sum(1 for operation in stream.operations if operation.kind == "store"),
                "native_max_steps": native_steps,
                "entered_boundary_sweep": screening_summary["entered_boundary_sweep"],
            }
        )

        if screening_summary["entered_boundary_sweep"]:
            boundary_rows: list[dict[str, object]] = []
            for multiplier in HORIZON_MULTIPLIERS:
                max_steps = native_steps * multiplier
                boundary_rows.append(
                    encode_result(
                        check_real_trace_precision(
                            stream.operations,
                            fmt="float32",
                            scheme="single_head",
                            base=SCREENING_BASE,
                            max_steps=max_steps,
                        ),
                        family=stream.family,
                        program_name=stream.program_name,
                        stream_name=stream.stream_name,
                        horizon_multiplier=multiplier,
                        native_steps=native_steps,
                    )
                )
                for scheme in ("radix2", "block_recentered"):
                    for base in BOUNDARY_BASES:
                        boundary_rows.append(
                            encode_result(
                                check_real_trace_precision(
                                    stream.operations,
                                    fmt="float32",
                                    scheme=scheme,
                                    base=base,
                                    max_steps=max_steps,
                                ),
                                family=stream.family,
                                program_name=stream.program_name,
                                stream_name=stream.stream_name,
                                horizon_multiplier=multiplier,
                                native_steps=native_steps,
                            )
                        )

            boundary["streams"][stream.stream_name] = {
                "family": stream.family,
                "program_name": stream.program_name,
                "space": stream.operations[0].space,
                "native_max_steps": native_steps,
                "rows": boundary_rows,
            }

    out_dir = Path("results/M4_precision_generalization")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "screening.json").write_text(json.dumps(screening, indent=2), encoding="utf-8")
    (out_dir / "boundary_sweep.json").write_text(json.dumps(boundary, indent=2), encoding="utf-8")
    (out_dir / "stream_catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print((out_dir / "screening.json").as_posix())


if __name__ == "__main__":
    main()
