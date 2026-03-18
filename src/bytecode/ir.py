from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .types import BytecodeMemoryCell, BytecodeType


class BytecodeOpcode(StrEnum):
    CONST_I32 = "const_i32"
    CONST_ADDR = "const_addr"
    DUP = "dup"
    POP = "pop"
    ADD_I32 = "add_i32"
    SUB_I32 = "sub_i32"
    EQ_I32 = "eq_i32"
    LOAD_STATIC = "load_static"
    STORE_STATIC = "store_static"
    LOAD_INDIRECT = "load_indirect"
    STORE_INDIRECT = "store_indirect"
    JMP = "jmp"
    JZ_ZERO = "jz_zero"
    CALL = "call"
    RET = "ret"
    HALT = "halt"


@dataclass(frozen=True, slots=True)
class OpcodeSignature:
    in_types: tuple[BytecodeType, ...]
    out_types: tuple[BytecodeType, ...]


OPCODE_SIGNATURES: dict[BytecodeOpcode, OpcodeSignature] = {
    BytecodeOpcode.CONST_I32: OpcodeSignature((), (BytecodeType.I32,)),
    BytecodeOpcode.CONST_ADDR: OpcodeSignature((), (BytecodeType.ADDR,)),
    BytecodeOpcode.DUP: OpcodeSignature((), ()),
    BytecodeOpcode.POP: OpcodeSignature((), ()),
    BytecodeOpcode.ADD_I32: OpcodeSignature((BytecodeType.I32, BytecodeType.I32), (BytecodeType.I32,)),
    BytecodeOpcode.SUB_I32: OpcodeSignature((BytecodeType.I32, BytecodeType.I32), (BytecodeType.I32,)),
    BytecodeOpcode.EQ_I32: OpcodeSignature((BytecodeType.I32, BytecodeType.I32), (BytecodeType.FLAG,)),
    BytecodeOpcode.LOAD_STATIC: OpcodeSignature((), (BytecodeType.I32,)),
    BytecodeOpcode.STORE_STATIC: OpcodeSignature((BytecodeType.I32,), ()),
    BytecodeOpcode.LOAD_INDIRECT: OpcodeSignature((BytecodeType.ADDR,), (BytecodeType.I32,)),
    BytecodeOpcode.STORE_INDIRECT: OpcodeSignature((BytecodeType.I32, BytecodeType.ADDR), ()),
    BytecodeOpcode.JMP: OpcodeSignature((), ()),
    BytecodeOpcode.JZ_ZERO: OpcodeSignature((BytecodeType.FLAG,), ()),
    BytecodeOpcode.CALL: OpcodeSignature((), ()),
    BytecodeOpcode.RET: OpcodeSignature((), ()),
    BytecodeOpcode.HALT: OpcodeSignature((), ()),
}


@dataclass(frozen=True, slots=True)
class BytecodeInstruction:
    opcode: BytecodeOpcode
    arg: int | None = None
    in_types: tuple[BytecodeType, ...] = ()
    out_types: tuple[BytecodeType, ...] = ()

    def __post_init__(self) -> None:
        signature = OPCODE_SIGNATURES[self.opcode]
        if not self.in_types:
            object.__setattr__(self, "in_types", signature.in_types)
        if not self.out_types:
            object.__setattr__(self, "out_types", signature.out_types)


@dataclass(frozen=True, slots=True)
class BytecodeProgram:
    instructions: tuple[BytecodeInstruction, ...]
    name: str = "anonymous"
    memory_layout: tuple[BytecodeMemoryCell, ...] = ()

    def __len__(self) -> int:
        return len(self.instructions)

    @property
    def memory_layout_map(self) -> dict[int, BytecodeMemoryCell]:
        return {cell.address: cell for cell in self.memory_layout}
