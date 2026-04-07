"""Append-only trace DSL and reference execution semantics."""

from .datasets import (
    alternating_memory_loop_program,
    call_chain_program,
    countdown_program,
    dynamic_latest_write_program,
    dynamic_memory_program,
    dynamic_memory_transfer_program,
    equality_branch_program,
    flagged_indirect_accumulator_program,
    hotspot_memory_rewrite_program,
    latest_write_program,
    loop_indirect_memory_program,
    memory_accumulator_program,
    native_count_nonzero_i32_buffer_program,
    native_sum_i32_buffer_program,
    selector_checkpoint_bank_program,
    stack_fanout_sum_program,
    stack_memory_ping_pong_program,
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
    "alternating_memory_loop_program",
    "call_chain_program",
    "countdown_program",
    "dynamic_latest_write_program",
    "dynamic_memory_program",
    "dynamic_memory_transfer_program",
    "equality_branch_program",
    "flagged_indirect_accumulator_program",
    "hotspot_memory_rewrite_program",
    "latest_memory_value",
    "latest_write_program",
    "loop_indirect_memory_program",
    "memory_accumulator_program",
    "native_count_nonzero_i32_buffer_program",
    "native_sum_i32_buffer_program",
    "replay_trace",
    "reconstruct_memory",
    "selector_checkpoint_bank_program",
    "stack_fanout_sum_program",
    "stack_memory_ping_pong_program",
]
