"""Export memory-surface diagnostics for the call/ret typed-bytecode follow-up."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from bytecode import (
    analyze_memory_surfaces,
    memory_surface_cases,
    memory_surface_negative_programs,
    run_memory_surface_harness,
    verify_memory_surfaces,
)
from bytecode.interpreter import BytecodeInterpreter
from bytecode.lowering import lower_program
from exec_trace import TraceInterpreter
from utils import detect_runtime_environment


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _encode_report(report) -> dict[str, object]:
    return {
        "program_name": report.program_name,
        "declared_frame_addresses": list(report.declared_frame_addresses),
        "declared_heap_addresses": list(report.declared_heap_addresses),
        "touched_frame_addresses": list(report.touched_frame_addresses),
        "touched_heap_addresses": list(report.touched_heap_addresses),
        "undeclared_addresses": list(report.undeclared_addresses),
        "max_call_depth": report.max_call_depth,
        "boundary_snapshots": [
            {
                "step": snapshot.step,
                "pc": snapshot.pc,
                "opcode": snapshot.opcode,
                "call_depth_before": snapshot.call_depth_before,
                "call_depth_after": snapshot.call_depth_after,
                "stack_before": list(snapshot.stack_before),
                "stack_after": list(snapshot.stack_after),
                "frame_memory": [list(item) for item in snapshot.frame_memory],
                "heap_memory": [list(item) for item in snapshot.heap_memory],
            }
            for snapshot in report.boundary_snapshots
        ],
        "accesses": [
            {
                "step": access.step,
                "pc": access.pc,
                "opcode": access.opcode,
                "access_kind": access.access_kind,
                "address": access.address,
                "region": access.region,
                "label": access.label,
                "alias_group": access.alias_group,
                "call_depth": access.call_depth,
            }
            for access in report.accesses
        ],
        "final_frame_memory": [list(item) for item in report.final_frame_memory],
        "final_heap_memory": [list(item) for item in report.final_heap_memory],
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = memory_surface_cases()
    harness_rows = run_memory_surface_harness(cases)

    detailed_reports: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    csv_rows: list[dict[str, object]] = []
    for case, row in zip(cases, harness_rows, strict=True):
        bytecode_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        lowered_result = TraceInterpreter().run(lower_program(case.program), max_steps=case.max_steps)
        reference_report = analyze_memory_surfaces(case.program, bytecode_result)
        lowered_report = analyze_memory_surfaces(case.program, lowered_result)
        summary_rows.append(
            {
                "program_name": row.program_name,
                "suite": row.suite,
                "comparison_mode": row.comparison_mode,
                "base_trace_match": row.base_trace_match,
                "base_final_state_match": row.base_final_state_match,
                "memory_surface_verifier_passed": row.memory_surface_verifier_passed,
                "memory_surface_error_class": row.memory_surface_error_class,
                "memory_surface_match": row.memory_surface_match,
                "boundary_snapshot_count": row.boundary_snapshot_count,
                "max_call_depth": row.max_call_depth,
                "undeclared_address_count": row.undeclared_address_count,
                "touched_frame_addresses": list(row.touched_frame_addresses),
                "touched_heap_addresses": list(row.touched_heap_addresses),
            }
        )
        csv_rows.append(
            {
                "program_name": row.program_name,
                "comparison_mode": row.comparison_mode,
                "base_trace_match": row.base_trace_match,
                "base_final_state_match": row.base_final_state_match,
                "memory_surface_verifier_passed": row.memory_surface_verifier_passed,
                "memory_surface_match": row.memory_surface_match,
                "boundary_snapshot_count": row.boundary_snapshot_count,
                "max_call_depth": row.max_call_depth,
                "undeclared_address_count": row.undeclared_address_count,
                "touched_frame_addresses": "|".join(str(item) for item in row.touched_frame_addresses),
                "touched_heap_addresses": "|".join(str(item) for item in row.touched_heap_addresses),
            }
        )
        detailed_reports.append(
            {
                "program_name": case.program.name,
                "reference": _encode_report(reference_report),
                "lowered": _encode_report(lowered_report),
            }
        )

    negative_rows = [
        {
            "program_name": result.program_name,
            "passed": result.passed,
            "first_error_pc": result.first_error_pc,
            "error_class": result.error_class,
            "message": result.message,
            "reachable_frame_addresses": list(result.reachable_frame_addresses),
            "reachable_heap_addresses": list(result.reachable_heap_addresses),
            "max_call_depth": result.max_call_depth,
        }
        for result in (verify_memory_surfaces(program) for program in memory_surface_negative_programs())
    ]

    out_dir = Path("results/M6_memory_surface_followup")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(
        json.dumps(
            {
                "experiment": "m6_memory_surface_followup",
                "environment": environment.as_dict(),
                "summary": {
                    "row_count": len(summary_rows),
                    "memory_surface_match_count": sum(int(row["memory_surface_match"]) for row in summary_rows),
                    "memory_surface_verifier_pass_count": sum(int(row["memory_surface_verifier_passed"]) for row in summary_rows),
                    "negative_control_count": len(negative_rows),
                },
                "rows": summary_rows,
                "negative_controls": negative_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "call_boundary_snapshots.json").write_text(
        json.dumps(
            {
                "experiment": "m6_memory_surface_boundaries",
                "environment": environment.as_dict(),
                "rows": detailed_reports,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    _write_csv(
        out_dir / "memory_surface_delta.csv",
        csv_rows,
        [
            "program_name",
            "comparison_mode",
            "base_trace_match",
            "base_final_state_match",
            "memory_surface_verifier_passed",
            "memory_surface_match",
            "boundary_snapshot_count",
            "max_call_depth",
            "undeclared_address_count",
            "touched_frame_addresses",
            "touched_heap_addresses",
        ],
    )
    (out_dir / "README.md").write_text(
        "\n".join(
            [
                "# M6 Memory Surface Follow-up",
                "",
                "Deterministic memory-surface diagnostics for the call/ret typed-bytecode slice.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `call_boundary_snapshots.json`",
                "- `memory_surface_delta.csv`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(out_dir.as_posix())


if __name__ == "__main__":
    main()
