"""Append-only trace DSL and reference execution semantics."""

from .datasets import countdown_program, equality_branch_program
from .dsl import ExecutionResult, ExecutionState, Instruction, Opcode, Program, TraceEvent
from .interpreter import TraceInterpreter
from .replay import ReplayMismatch, replay_trace

__all__ = [
    "ExecutionResult",
    "ExecutionState",
    "Instruction",
    "Opcode",
    "Program",
    "ReplayMismatch",
    "TraceEvent",
    "TraceInterpreter",
    "countdown_program",
    "equality_branch_program",
    "replay_trace",
]
