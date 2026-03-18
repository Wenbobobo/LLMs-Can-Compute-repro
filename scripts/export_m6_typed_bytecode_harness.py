"""Export verifier, lowering, and harness artifacts for the first typed-bytecode batch."""

from __future__ import annotations

import json
from pathlib import Path

from bytecode import harness_cases, lower_program, run_harness, verifier_negative_programs, verify_program
from utils import detect_runtime_environment


def encode_verifier_row(result) -> dict[str, object]:
    return {
        "program_name": result.program_name,
        "passed": result.passed,
        "first_error_pc": result.first_error_pc,
        "error_class": result.error_class,
        "expected_stack": list(result.expected_stack),
        "actual_stack": list(result.actual_stack),
        "message": result.message,
    }


def encode_harness_row(row) -> dict[str, object]:
    return {
        "program_name": row.program_name,
        "suite": row.suite,
        "comparison_mode": row.comparison_mode,
        "trace_match": row.trace_match,
        "final_state_match": row.final_state_match,
        "first_divergence_step": row.first_divergence_step,
        "failure_class": row.failure_class,
        "failure_reason": row.failure_reason,
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = harness_cases()
    harness_rows = run_harness(cases)
    verifier_rows = [verify_program(case.program) for case in cases] + [verify_program(program) for program in verifier_negative_programs()]

    lowering_rows = []
    for case, row in zip(cases, harness_rows, strict=True):
        lowered = lower_program(case.program)
        lowering_rows.append(
            {
                "program_name": case.program.name,
                "suite": case.suite,
                "comparison_mode": case.comparison_mode,
                "bytecode_instruction_count": len(case.program.instructions),
                "lowered_instruction_count": len(lowered.instructions),
                "instruction_count_match": len(case.program.instructions) == len(lowered.instructions),
                "trace_match": row.trace_match,
                "final_state_match": row.final_state_match,
                "failure_class": row.failure_class,
                "failure_reason": row.failure_reason,
            }
        )

    out_dir = Path("results/M6_typed_bytecode_harness")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "verifier_rows.json").write_text(
        json.dumps(
            {
                "experiment": "m6_typed_bytecode_verifier",
                "environment": environment.as_dict(),
                "rows": [encode_verifier_row(row) for row in verifier_rows],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "lowering_equivalence.json").write_text(
        json.dumps(
            {
                "experiment": "m6_typed_bytecode_lowering_equivalence",
                "environment": environment.as_dict(),
                "rows": lowering_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "short_exact_trace.json").write_text(
        json.dumps(
            {
                "experiment": "m6_typed_bytecode_exact_trace",
                "environment": environment.as_dict(),
                "rows": [
                    encode_harness_row(row)
                    for row in harness_rows
                    if row.comparison_mode in {"short_exact_trace", "medium_exact_trace"}
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "long_exact_final_state.json").write_text(
        json.dumps(
            {
                "experiment": "m6_typed_bytecode_long_final_state",
                "environment": environment.as_dict(),
                "rows": [encode_harness_row(row) for row in harness_rows if row.comparison_mode == "long_exact_final_state"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(out_dir.as_posix())


if __name__ == "__main__":
    main()
