"""Export real-trace finite-precision checks for the latest-write runtime."""

from __future__ import annotations

import json
from pathlib import Path

from exec_trace import (
    TraceInterpreter,
    loop_indirect_memory_program,
    stack_memory_ping_pong_program,
)
from model import (
    check_real_trace_precision,
    extract_memory_operations,
    extract_stack_slot_operations,
)
from utils import detect_runtime_environment


FORMATS = ("float64", "float32", "bfloat16", "float16")
SCHEMES = (
    ("single_head", 64),
    ("radix2", 64),
    ("block_recentered", 64),
)


def encode_result(result):
    return {
        "fmt": result.fmt,
        "scheme": result.scheme,
        "base": result.base,
        "space": result.space,
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
        ("ping_pong_offset_128", stack_memory_ping_pong_program(base_address=128)),
        ("ping_pong_offset_512", stack_memory_ping_pong_program(base_address=512)),
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


def main() -> None:
    environment = detect_runtime_environment()
    streams = build_streams()
    output = {
        "experiment": "m4_real_trace_precision",
        "environment": environment.as_dict(),
        "notes": [
            "These checks reuse real execution traces instead of synthetic nearest-neighbor scans.",
            "Each stream compares the expected latest-write winner against all previously written candidates visible at each real read event.",
            "Address-offset program families force the same semantics to exercise larger address magnitudes without changing the underlying DSL.",
        ],
        "streams": {},
    }

    for name, operations in streams:
        output["streams"][name] = {
            "space": operations[0].space,
            "operation_count": len(operations),
            "results": {
                fmt: {
                    scheme: encode_result(
                        check_real_trace_precision(
                            operations,
                            fmt=fmt,
                            scheme=scheme,
                            base=base,
                        )
                    )
                    for scheme, base in SCHEMES
                }
                for fmt in FORMATS
            },
        }

    out_path = Path("results/M4_precision_scaling_real_traces/summary.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
