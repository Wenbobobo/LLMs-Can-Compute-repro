"""Small deterministic programs for the trace milestone."""

from __future__ import annotations

from .dsl import Instruction, Opcode, Program


def countdown_program(start: int) -> Program:
    if start < 0:
        raise ValueError("countdown_program expects a non-negative start.")

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 6),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.JMP, 1),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name=f"countdown_{start}")


def equality_branch_program(lhs: int, rhs: int) -> Program:
    instructions = (
        Instruction(Opcode.PUSH_CONST, lhs),
        Instruction(Opcode.PUSH_CONST, rhs),
        Instruction(Opcode.EQ),
        Instruction(Opcode.JZ, 6),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.HALT),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name=f"eq_{lhs}_{rhs}")
