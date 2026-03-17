"""Core data structures for the append-only execution trace DSL."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Opcode(StrEnum):
    PUSH_CONST = "push_const"
    ADD = "add"
    SUB = "sub"
    EQ = "eq"
    DUP = "dup"
    POP = "pop"
    JMP = "jmp"
    JZ = "jz"
    HALT = "halt"


@dataclass(frozen=True, slots=True)
class Instruction:
    opcode: Opcode
    arg: int | None = None


@dataclass(frozen=True, slots=True)
class Program:
    instructions: tuple[Instruction, ...]
    name: str = "anonymous"

    def __len__(self) -> int:
        return len(self.instructions)


@dataclass(frozen=True, slots=True)
class TraceEvent:
    step: int
    pc: int
    opcode: Opcode
    arg: int | None
    popped: tuple[int, ...]
    pushed: tuple[int, ...]
    branch_taken: bool | None
    next_pc: int
    stack_depth_before: int
    stack_depth_after: int
    halted: bool


@dataclass(frozen=True, slots=True)
class ExecutionState:
    pc: int = 0
    stack: tuple[int, ...] = ()
    halted: bool = False
    steps: int = 0


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    program: Program
    events: tuple[TraceEvent, ...]
    final_state: ExecutionState
