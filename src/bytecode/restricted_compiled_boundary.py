from __future__ import annotations

from dataclasses import dataclass

from .datasets import (
    arithmetic_smoke_program,
    branch_then_call_false_program,
    call_frame_roundtrip_program,
    countdown_loop_program,
    dynamic_latest_write_program,
)
from .ir import BytecodeProgram


@dataclass(frozen=True, slots=True)
class RestrictedCompiledBoundaryCase:
    case_id: str
    category: str
    description: str
    notes: str
    max_steps: int
    program: BytecodeProgram


def r58_restricted_compiled_boundary_cases() -> tuple[RestrictedCompiledBoundaryCase, ...]:
    return (
        RestrictedCompiledBoundaryCase(
            case_id="straight_line_arithmetic",
            category="arithmetic",
            description="Straight-line arithmetic smoke row on the typed stack-bytecode surface.",
            notes="Keeps the smallest compiled boundary row visible before control or memory widening.",
            max_steps=32,
            program=arithmetic_smoke_program(),
        ),
        RestrictedCompiledBoundaryCase(
            case_id="counted_loop_countdown",
            category="counted_loop",
            description="Counted loop row with repeated stack updates and taken branches.",
            notes="Exercises bounded loop control without widening the opcode surface.",
            max_steps=128,
            program=countdown_loop_program(6),
        ),
        RestrictedCompiledBoundaryCase(
            case_id="latest_write_overwrite_after_gap",
            category="latest_write_memory",
            description="Indirect overwrite-after-gap row on the admitted bytecode lowering surface.",
            notes="Carries latest-write recovery into the compiled-boundary suite without reopening broad Wasm or arbitrary C.",
            max_steps=64,
            program=dynamic_latest_write_program(),
        ),
        RestrictedCompiledBoundaryCase(
            case_id="shallow_call_return_roundtrip",
            category="call_return",
            description="Single bounded call/return row with one declared frame-local slot.",
            notes="Keeps call-frame retrieval explicit on the compiled-boundary suite.",
            max_steps=64,
            program=call_frame_roundtrip_program(),
        ),
        RestrictedCompiledBoundaryCase(
            case_id="branch_fallthrough_revisit",
            category="branch_revisit",
            description="Branch-fallthrough revisit row that preserves alternate-path control without executing a broader call family.",
            notes="Separates branch control from the shallower call/return roundtrip row.",
            max_steps=64,
            program=branch_then_call_false_program(),
        ),
    )
