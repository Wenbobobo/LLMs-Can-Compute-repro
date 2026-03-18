from __future__ import annotations

from exec_trace import TraceInterpreter

from .datasets import BytecodeCase
from .harness import run_harness_case
from .interpreter import BytecodeInterpreter
from .lowering import lower_program
from .memory_surfaces import (
    MemorySurfaceHarnessRow,
    analyze_memory_surfaces,
    verify_memory_surfaces,
)


def run_memory_surface_case(case: BytecodeCase) -> MemorySurfaceHarnessRow:
    base_row = run_harness_case(case)
    memory_verification = verify_memory_surfaces(case.program)
    if not memory_verification.passed:
        return MemorySurfaceHarnessRow(
            program_name=case.program.name,
            suite=case.suite,
            comparison_mode=case.comparison_mode,
            base_trace_match=base_row.trace_match,
            base_final_state_match=base_row.final_state_match,
            memory_surface_verifier_passed=False,
            memory_surface_error_class=memory_verification.error_class,
            memory_surface_match=False,
            boundary_snapshot_count=0,
            max_call_depth=memory_verification.max_call_depth,
            undeclared_address_count=0,
            touched_frame_addresses=(),
            touched_heap_addresses=(),
        )

    reference = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
    lowered = TraceInterpreter().run(lower_program(case.program), max_steps=case.max_steps)
    reference_report = analyze_memory_surfaces(case.program, reference)
    lowered_report = analyze_memory_surfaces(case.program, lowered)

    return MemorySurfaceHarnessRow(
        program_name=case.program.name,
        suite=case.suite,
        comparison_mode=case.comparison_mode,
        base_trace_match=base_row.trace_match,
        base_final_state_match=base_row.final_state_match,
        memory_surface_verifier_passed=True,
        memory_surface_error_class=None,
        memory_surface_match=reference_report == lowered_report,
        boundary_snapshot_count=len(reference_report.boundary_snapshots),
        max_call_depth=reference_report.max_call_depth,
        undeclared_address_count=len(reference_report.undeclared_addresses),
        touched_frame_addresses=reference_report.touched_frame_addresses,
        touched_heap_addresses=reference_report.touched_heap_addresses,
    )


def run_memory_surface_harness(cases: tuple[BytecodeCase, ...]) -> tuple[MemorySurfaceHarnessRow, ...]:
    return tuple(run_memory_surface_case(case) for case in cases)
