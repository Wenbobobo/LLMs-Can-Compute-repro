"""Append-only trace DSL and reference execution semantics."""

from .datasets import (
    countdown_program,
    equality_branch_program,
    latest_write_program,
    memory_accumulator_program,
)
from .dsl import ExecutionResult, ExecutionState, Instruction, Opcode, Program, TraceEvent
from .interpreter import TraceInterpreter
from .memory import latest_memory_value, reconstruct_memory
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
    "latest_memory_value",
    "latest_write_program",
    "memory_accumulator_program",
    "replay_trace",
    "reconstruct_memory",
]
