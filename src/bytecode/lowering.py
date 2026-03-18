from __future__ import annotations

from exec_trace.dsl import Instruction, Opcode, Program

from .ir import BytecodeInstruction, BytecodeOpcode, BytecodeProgram


LOWERING_MAP: dict[BytecodeOpcode, Opcode] = {
    BytecodeOpcode.CONST_I32: Opcode.PUSH_CONST,
    BytecodeOpcode.CONST_ADDR: Opcode.PUSH_CONST,
    BytecodeOpcode.DUP: Opcode.DUP,
    BytecodeOpcode.POP: Opcode.POP,
    BytecodeOpcode.ADD_I32: Opcode.ADD,
    BytecodeOpcode.SUB_I32: Opcode.SUB,
    BytecodeOpcode.EQ_I32: Opcode.EQ,
    BytecodeOpcode.LOAD_STATIC: Opcode.LOAD,
    BytecodeOpcode.STORE_STATIC: Opcode.STORE,
    BytecodeOpcode.LOAD_INDIRECT: Opcode.LOAD_AT,
    BytecodeOpcode.STORE_INDIRECT: Opcode.STORE_AT,
    BytecodeOpcode.JMP: Opcode.JMP,
    BytecodeOpcode.JZ_ZERO: Opcode.JZ,
    BytecodeOpcode.CALL: Opcode.CALL,
    BytecodeOpcode.RET: Opcode.RET,
    BytecodeOpcode.HALT: Opcode.HALT,
}


def lower_instruction(instruction: BytecodeInstruction) -> Instruction:
    return Instruction(LOWERING_MAP[instruction.opcode], instruction.arg)


def lower_program(program: BytecodeProgram) -> Program:
    return Program(
        instructions=tuple(lower_instruction(instruction) for instruction in program.instructions),
        name=program.name,
    )
