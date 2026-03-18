from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BytecodeType(StrEnum):
    I32 = "i32"
    ADDR = "addr"
    FLAG = "flag"


class BytecodeMemoryRegion(StrEnum):
    FRAME = "frame"
    HEAP = "heap"


@dataclass(frozen=True, slots=True)
class BytecodeMemoryCell:
    address: int
    cell_type: BytecodeType
    region: BytecodeMemoryRegion
    label: str
    allowed_targets: tuple[int, ...] = ()
    alias_group: str | None = None
