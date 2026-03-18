"""Export a float32-focused real-trace horizon/base sweep for latest-write precision."""

from __future__ import annotations

import json
from pathlib import Path

from exec_trace import (
    TraceInterpreter,
    alternating_memory_loop_program,
    loop_indirect_memory_program,
    stack_memory_ping_pong_program,
)
from model import (
    check_real_trace_precision,
    extract_memory_operations,
    extract_stack_slot_operations,
)
from utils import detect_runtime_environment


HORIZON_MULTIPLIERS = (1, 4, 16, 64)
BASES = (32, 64, 128, 256)


def encode_result(result, *, horizon_multiplier: int, native_max_steps: int):
    return {
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
        "first_failure": None
        if result.first_failure is None
        else {
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


def build_streams():
    interpreter = TraceInterpreter()
    streams: list[tuple[str, tuple]] = []
    programs = [
        ("loop_offset_64", loop_indirect_memory_program(12, counter_address=64, accumulator_address=65)),
        ("loop_offset_256", loop_indirect_memory_program(12, counter_address=256, accumulator_address=257)),
        ("loop_offset_1024", loop_indirect_memory_program(12, counter_address=1024, accumulator_address=1025)),
        ("loop_offset_4096", loop_indirect_memory_program(12, counter_address=4096, accumulator_address=4097)),
        ("ping_pong_offset_128", stack_memory_ping_pong_program(base_address=128)),
        ("ping_pong_offset_512", stack_memory_ping_pong_program(base_address=512)),
        ("ping_pong_offset_2048", stack_memory_ping_pong_program(base_address=2048)),
        ("ping_pong_offset_8192", stack_memory_ping_pong_program(base_address=8192)),
        ("alternating_offset_256", alternating_memory_loop_program(12, base_address=256)),
        ("alternating_offset_2048", alternating_memory_loop_program(12, base_address=2048)),
    ]

    for name, program in programs:
        result = interpreter.run(program)
        memory_ops = extract_memory_operations(result.events)
        if memory_ops:
            streams.append((f"{name}_memory", memory_ops))
        stack_ops = extract_stack_slot_operations(result.events)
        if stack_ops:
            streams.append((f"{name}_stack", stack_ops))

    return streams


def summarize_rows(rows):
    single_head_fail = next(
        (
            row["horizon_multiplier"]
            for row in rows
            if row["scheme"] == "single_head" and row["passed"] is False
        ),
        None,
    )
    stable_configs = [
        {
            "scheme": row["scheme"],
            "base": row["base"],
            "max_horizon_multiplier": row["horizon_multiplier"],
        }
        for row in rows
        if row["horizon_multiplier"] == HORIZON_MULTIPLIERS[-1] and row["passed"] is True
    ]
    return {
        "single_head_first_failure_multiplier": single_head_fail,
        "stable_through_max_multiplier": stable_configs,
    }


def main() -> None:
    environment = detect_runtime_environment()
    streams = build_streams()
    output = {
        "experiment": "m4_real_trace_precision_sweep",
        "environment": environment.as_dict(),
        "notes": [
            "This sweep focuses on float32 because the previous real-trace summary already established the broader dtype picture.",
            "Each row reuses a real execution stream but inflates the latest-write horizon to shrink the time epsilon and stress temporal tie-breaking.",
            "The main question is whether base decomposition keeps real traces stable as the same stream is evaluated under longer effective horizons.",
        ],
        "focus_format": "float32",
        "horizon_multipliers": list(HORIZON_MULTIPLIERS),
        "base_options": list(BASES),
        "streams": {},
    }

    for name, operations in streams:
        native_max_steps = max(operation.step for operation in operations)
        rows = []

        for multiplier in HORIZON_MULTIPLIERS:
            max_steps = native_max_steps * multiplier
            rows.append(
                encode_result(
                    check_real_trace_precision(
                        operations,
                        fmt="float32",
                        scheme="single_head",
                        base=64,
                        max_steps=max_steps,
                    ),
                    horizon_multiplier=multiplier,
                    native_max_steps=native_max_steps,
                )
            )
            for scheme in ("radix2", "block_recentered"):
                for base in BASES:
                    rows.append(
                        encode_result(
                            check_real_trace_precision(
                                operations,
                                fmt="float32",
                                scheme=scheme,
                                base=base,
                                max_steps=max_steps,
                            ),
                            horizon_multiplier=multiplier,
                            native_max_steps=native_max_steps,
                        )
                    )

        output["streams"][name] = {
            "space": operations[0].space,
            "operation_count": len(operations),
            "read_count": sum(1 for operation in operations if operation.kind == "load"),
            "write_count": sum(1 for operation in operations if operation.kind == "store"),
            "native_max_steps": native_max_steps,
            "rows": rows,
            "summary": summarize_rows(rows),
        }

    out_path = Path("results/M4_precision_scaling_real_traces/horizon_base_sweep.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
