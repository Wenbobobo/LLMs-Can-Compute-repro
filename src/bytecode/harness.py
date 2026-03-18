from __future__ import annotations

from dataclasses import dataclass

from exec_trace import TraceInterpreter

from .datasets import BytecodeCase
from .interpreter import BytecodeInterpreter
from .lowering import lower_program
from .verifier import verify_program


@dataclass(frozen=True, slots=True)
class HarnessRow:
    program_name: str
    suite: str
    comparison_mode: str
    trace_match: bool
    final_state_match: bool
    first_divergence_step: int | None
    failure_class: str | None
    failure_reason: str | None


def _first_divergence_step(reference_events, produced_events) -> int | None:
    for produced, expected in zip(produced_events, reference_events):
        if produced != expected:
            return produced.step
    if len(produced_events) != len(reference_events):
        return min(len(produced_events), len(reference_events))
    return None


def run_harness_case(case: BytecodeCase) -> HarnessRow:
    verification = verify_program(case.program)
    if not verification.passed:
        return HarnessRow(
            program_name=case.program.name,
            suite=case.suite,
            comparison_mode=case.comparison_mode,
            trace_match=False,
            final_state_match=False,
            first_divergence_step=None,
            failure_class="verify_error",
            failure_reason=verification.message,
        )

    try:
        reference = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        lowered = TraceInterpreter().run(lower_program(case.program), max_steps=case.max_steps)
    except Exception as exc:
        return HarnessRow(
            program_name=case.program.name,
            suite=case.suite,
            comparison_mode=case.comparison_mode,
            trace_match=False,
            final_state_match=False,
            first_divergence_step=None,
            failure_class="runtime_exception",
            failure_reason=str(exc),
        )

    trace_match = reference.events == lowered.events
    final_state_match = reference.final_state == lowered.final_state
    failure_class = None
    failure_reason = None
    if not trace_match and not final_state_match:
        failure_class = "lowering_mismatch"
        failure_reason = "bytecode reference and lowered exec_trace disagree on trace and final state."
    elif not trace_match:
        failure_class = "trace_divergence"
        failure_reason = "bytecode reference and lowered exec_trace diverge before termination."
    elif not final_state_match:
        failure_class = "final_state_divergence"
        failure_reason = "bytecode reference and lowered exec_trace end in different final states."

    return HarnessRow(
        program_name=case.program.name,
        suite=case.suite,
        comparison_mode=case.comparison_mode,
        trace_match=trace_match,
        final_state_match=final_state_match,
        first_divergence_step=_first_divergence_step(reference.events, lowered.events),
        failure_class=failure_class,
        failure_reason=failure_reason,
    )


def run_harness(cases: tuple[BytecodeCase, ...]) -> tuple[HarnessRow, ...]:
    return tuple(run_harness_case(case) for case in cases)
