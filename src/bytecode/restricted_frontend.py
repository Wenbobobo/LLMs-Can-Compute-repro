from __future__ import annotations

from dataclasses import dataclass, field

from .ir import BytecodeInstruction, BytecodeOpcode, BytecodeProgram
from .types import BytecodeMemoryCell, BytecodeMemoryRegion, BytecodeType


AssemblyRow = str | tuple[BytecodeOpcode, int | str | None] | tuple[
    BytecodeOpcode,
    int | str | None,
    tuple[BytecodeType, ...],
    tuple[BytecodeType, ...],
]


@dataclass(frozen=True, slots=True)
class FrontendCell:
    name: str
    address: int
    cell_type: BytecodeType = BytecodeType.I32


@dataclass(frozen=True, slots=True)
class FrontendBuffer:
    name: str
    item_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FrontendExpr:
    pass


@dataclass(frozen=True, slots=True)
class FrontendConst(FrontendExpr):
    value: int


@dataclass(frozen=True, slots=True)
class FrontendLoad(FrontendExpr):
    cell_name: str


@dataclass(frozen=True, slots=True)
class FrontendStmt:
    pass


@dataclass(frozen=True, slots=True)
class FrontendAssign(FrontendStmt):
    cell_name: str
    expr: FrontendExpr


@dataclass(frozen=True, slots=True)
class FrontendIncrement(FrontendStmt):
    cell_name: str


@dataclass(frozen=True, slots=True)
class FrontendFoldAdd(FrontendStmt):
    target_name: str
    buffer_name: str


@dataclass(frozen=True, slots=True)
class FrontendIfEq(FrontendStmt):
    left: FrontendExpr
    right: FrontendExpr
    then_body: tuple[FrontendStmt, ...]
    else_body: tuple[FrontendStmt, ...] = ()


@dataclass(frozen=True, slots=True)
class FrontendForEachStatic(FrontendStmt):
    buffer_name: str
    item_name: str
    body: tuple[FrontendStmt, ...]


@dataclass(frozen=True, slots=True)
class FrontendSwitchEq(FrontendStmt):
    expr: FrontendExpr
    cases: tuple[tuple[int, tuple[FrontendStmt, ...]], ...]
    default_body: tuple[FrontendStmt, ...] = ()


@dataclass(frozen=True, slots=True)
class FrontendReturn(FrontendStmt):
    expr: FrontendExpr


@dataclass(frozen=True, slots=True)
class FrontendHalt(FrontendStmt):
    pass


@dataclass(frozen=True, slots=True)
class RestrictedFrontendProgram:
    name: str
    cells: tuple[FrontendCell, ...]
    buffers: tuple[FrontendBuffer, ...]
    statements: tuple[FrontendStmt, ...]

    @property
    def cell_map(self) -> dict[str, FrontendCell]:
        return {cell.name: cell for cell in self.cells}

    @property
    def buffer_map(self) -> dict[str, FrontendBuffer]:
        return {buffer.name: buffer for buffer in self.buffers}

    @property
    def memory_layout(self) -> tuple[BytecodeMemoryCell, ...]:
        return tuple(
            BytecodeMemoryCell(
                address=cell.address,
                cell_type=cell.cell_type,
                region=BytecodeMemoryRegion.FRAME,
                label=cell.name,
            )
            for cell in sorted(self.cells, key=lambda item: item.address)
        )


def _serialize_expr(expr: FrontendExpr) -> dict[str, object]:
    if isinstance(expr, FrontendConst):
        return {"kind": "const", "value": expr.value}
    if isinstance(expr, FrontendLoad):
        return {"kind": "load", "cell_name": expr.cell_name}
    raise TypeError(f"Unsupported restricted-frontend expression: {type(expr).__name__}")


def _serialize_stmt(stmt: FrontendStmt) -> dict[str, object]:
    if isinstance(stmt, FrontendAssign):
        return {"kind": "assign", "cell_name": stmt.cell_name, "expr": _serialize_expr(stmt.expr)}
    if isinstance(stmt, FrontendIncrement):
        return {"kind": "increment", "cell_name": stmt.cell_name}
    if isinstance(stmt, FrontendFoldAdd):
        return {"kind": "fold_add", "target_name": stmt.target_name, "buffer_name": stmt.buffer_name}
    if isinstance(stmt, FrontendIfEq):
        return {
            "kind": "if_eq",
            "left": _serialize_expr(stmt.left),
            "right": _serialize_expr(stmt.right),
            "then_body": [_serialize_stmt(item) for item in stmt.then_body],
            "else_body": [_serialize_stmt(item) for item in stmt.else_body],
        }
    if isinstance(stmt, FrontendForEachStatic):
        return {
            "kind": "for_each_static",
            "buffer_name": stmt.buffer_name,
            "item_name": stmt.item_name,
            "body": [_serialize_stmt(item) for item in stmt.body],
        }
    if isinstance(stmt, FrontendSwitchEq):
        return {
            "kind": "switch_eq",
            "expr": _serialize_expr(stmt.expr),
            "cases": [
                {"value": value, "body": [_serialize_stmt(item) for item in body]}
                for value, body in stmt.cases
            ],
            "default_body": [_serialize_stmt(item) for item in stmt.default_body],
        }
    if isinstance(stmt, FrontendReturn):
        return {"kind": "return", "expr": _serialize_expr(stmt.expr)}
    if isinstance(stmt, FrontendHalt):
        return {"kind": "halt"}
    raise TypeError(f"Unsupported restricted-frontend statement: {type(stmt).__name__}")


def serialize_restricted_frontend_program(program: RestrictedFrontendProgram) -> dict[str, object]:
    return {
        "name": program.name,
        "cells": [
            {"name": cell.name, "address": cell.address, "cell_type": cell.cell_type.value}
            for cell in sorted(program.cells, key=lambda item: item.address)
        ],
        "buffers": [{"name": buffer.name, "item_names": list(buffer.item_names)} for buffer in program.buffers],
        "statements": [_serialize_stmt(stmt) for stmt in program.statements],
    }


def validate_restricted_frontend_program(program: RestrictedFrontendProgram) -> tuple[bool, str | None]:
    cell_map = program.cell_map
    if len(cell_map) != len(program.cells):
        return False, "duplicate_cell_name"
    addresses = [cell.address for cell in program.cells]
    if len(set(addresses)) != len(addresses):
        return False, "duplicate_cell_address"
    if any(cell.address < 0 for cell in program.cells):
        return False, "negative_static_address"
    if any(cell.cell_type != BytecodeType.I32 for cell in program.cells):
        return False, "non_i32_cell_not_admitted"
    buffer_map = program.buffer_map
    if len(buffer_map) != len(program.buffers):
        return False, "duplicate_buffer_name"

    def validate_expr(expr: FrontendExpr, aliases: set[str]) -> tuple[bool, str | None]:
        if isinstance(expr, FrontendConst):
            return True, None
        if isinstance(expr, FrontendLoad):
            if expr.cell_name not in cell_map and expr.cell_name not in aliases:
                return False, "unknown_cell_reference"
            return True, None
        return False, "unsupported_expr"

    def validate_stmt(stmt: FrontendStmt, aliases: set[str]) -> tuple[bool, str | None]:
        if isinstance(stmt, FrontendAssign):
            if stmt.cell_name not in cell_map:
                return False, "unknown_assignment_target"
            return validate_expr(stmt.expr, aliases)
        if isinstance(stmt, FrontendIncrement):
            if stmt.cell_name not in cell_map:
                return False, "unknown_increment_target"
            return True, None
        if isinstance(stmt, FrontendFoldAdd):
            if stmt.target_name not in cell_map:
                return False, "unknown_fold_target"
            if stmt.buffer_name not in buffer_map:
                return False, "unknown_buffer_reference"
            return True, None
        if isinstance(stmt, FrontendIfEq):
            passed, error = validate_expr(stmt.left, aliases)
            if not passed:
                return False, error
            passed, error = validate_expr(stmt.right, aliases)
            if not passed:
                return False, error
            for branch_stmt in stmt.then_body:
                passed, error = validate_stmt(branch_stmt, aliases)
                if not passed:
                    return False, error
            for branch_stmt in stmt.else_body:
                passed, error = validate_stmt(branch_stmt, aliases)
                if not passed:
                    return False, error
            return True, None
        if isinstance(stmt, FrontendForEachStatic):
            buffer = buffer_map.get(stmt.buffer_name)
            if buffer is None:
                return False, "unknown_buffer_reference"
            if len(buffer.item_names) == 0:
                return False, "empty_static_buffer"
            for item_name in buffer.item_names:
                if item_name not in cell_map:
                    return False, "unknown_buffer_item"
            nested_aliases = set(aliases)
            nested_aliases.add(stmt.item_name)
            for body_stmt in stmt.body:
                passed, error = validate_stmt(body_stmt, nested_aliases)
                if not passed:
                    return False, error
            return True, None
        if isinstance(stmt, FrontendSwitchEq):
            passed, error = validate_expr(stmt.expr, aliases)
            if not passed:
                return False, error
            case_values = [value for value, _ in stmt.cases]
            if len(set(case_values)) != len(case_values):
                return False, "duplicate_switch_case"
            for _, body in stmt.cases:
                for body_stmt in body:
                    passed, error = validate_stmt(body_stmt, aliases)
                    if not passed:
                        return False, error
            for body_stmt in stmt.default_body:
                passed, error = validate_stmt(body_stmt, aliases)
                if not passed:
                    return False, error
            return True, None
        if isinstance(stmt, FrontendReturn):
            return validate_expr(stmt.expr, aliases)
        if isinstance(stmt, FrontendHalt):
            return True, None
        return False, "unsupported_stmt"

    for stmt in program.statements:
        passed, error = validate_stmt(stmt, set())
        if not passed:
            return False, error
    return True, None


@dataclass(slots=True)
class _FrontendCompiler:
    program: RestrictedFrontendProgram
    rows: list[AssemblyRow] = field(default_factory=list)
    label_counter: int = 0
    aliases: dict[str, str] = field(default_factory=dict)

    def branch(self, **updates: str) -> _FrontendCompiler:
        next_aliases = dict(self.aliases)
        next_aliases.update(updates)
        return _FrontendCompiler(
            program=self.program,
            rows=self.rows,
            label_counter=self.label_counter,
            aliases=next_aliases,
        )

    def sync(self, other: _FrontendCompiler) -> None:
        self.label_counter = other.label_counter

    def next_label(self, stem: str) -> str:
        label = f"{stem}_{self.label_counter}"
        self.label_counter += 1
        return label

    def resolve_cell(self, name: str) -> FrontendCell:
        resolved = self.aliases.get(name, name)
        try:
            return self.program.cell_map[resolved]
        except KeyError as exc:  # pragma: no cover
            raise KeyError(f"Unknown restricted-frontend cell {name!r}.") from exc

    def resolve_buffer(self, name: str) -> FrontendBuffer:
        try:
            return self.program.buffer_map[name]
        except KeyError as exc:  # pragma: no cover
            raise KeyError(f"Unknown restricted-frontend buffer {name!r}.") from exc

    def emit(
        self,
        opcode: BytecodeOpcode,
        arg: int | str | None = None,
        *,
        in_types: tuple[BytecodeType, ...] = (),
        out_types: tuple[BytecodeType, ...] = (),
    ) -> None:
        if in_types or out_types:
            self.rows.append((opcode, arg, in_types, out_types))
        else:
            self.rows.append((opcode, arg))

    def emit_label(self, label: str) -> None:
        self.rows.append(f"{label}:")

    def compile_expr(self, expr: FrontendExpr) -> None:
        if isinstance(expr, FrontendConst):
            self.emit(BytecodeOpcode.CONST_I32, expr.value)
            return
        if isinstance(expr, FrontendLoad):
            self.emit(BytecodeOpcode.LOAD_STATIC, self.resolve_cell(expr.cell_name).address)
            return
        raise TypeError(f"Unsupported restricted-frontend expression: {type(expr).__name__}")

    def compile_stmt(self, stmt: FrontendStmt) -> None:
        if isinstance(stmt, FrontendAssign):
            self.compile_expr(stmt.expr)
            self.emit(BytecodeOpcode.STORE_STATIC, self.resolve_cell(stmt.cell_name).address)
            return
        if isinstance(stmt, FrontendIncrement):
            target = self.resolve_cell(stmt.cell_name)
            self.emit(BytecodeOpcode.LOAD_STATIC, target.address)
            self.emit(BytecodeOpcode.CONST_I32, 1)
            self.emit(BytecodeOpcode.ADD_I32)
            self.emit(BytecodeOpcode.STORE_STATIC, target.address)
            return
        if isinstance(stmt, FrontendFoldAdd):
            target = self.resolve_cell(stmt.target_name)
            buffer = self.resolve_buffer(stmt.buffer_name)
            self.emit(BytecodeOpcode.LOAD_STATIC, target.address)
            for item_name in buffer.item_names:
                self.emit(BytecodeOpcode.LOAD_STATIC, self.resolve_cell(item_name).address)
                self.emit(BytecodeOpcode.ADD_I32)
            self.emit(BytecodeOpcode.STORE_STATIC, target.address)
            return
        if isinstance(stmt, FrontendIfEq):
            else_label = self.next_label("frontend_else")
            end_label = self.next_label("frontend_end_if")
            self.compile_expr(stmt.left)
            self.compile_expr(stmt.right)
            self.emit(BytecodeOpcode.EQ_I32)
            self.emit(BytecodeOpcode.JZ_ZERO, else_label)
            for then_stmt in stmt.then_body:
                self.compile_stmt(then_stmt)
            if stmt.else_body:
                self.emit(BytecodeOpcode.JMP, end_label)
            self.emit_label(else_label)
            for else_stmt in stmt.else_body:
                self.compile_stmt(else_stmt)
            if stmt.else_body:
                self.emit_label(end_label)
            return
        if isinstance(stmt, FrontendForEachStatic):
            buffer = self.resolve_buffer(stmt.buffer_name)
            for item_name in buffer.item_names:
                nested = self.branch(**{stmt.item_name: item_name})
                for body_stmt in stmt.body:
                    nested.compile_stmt(body_stmt)
                self.sync(nested)
            return
        if isinstance(stmt, FrontendSwitchEq):
            end_label = self.next_label("frontend_switch_end")
            self.compile_expr(stmt.expr)
            for value, body in stmt.cases:
                next_check = self.next_label("frontend_switch_next")
                self.emit(BytecodeOpcode.DUP)
                self.emit(BytecodeOpcode.CONST_I32, value)
                self.emit(BytecodeOpcode.EQ_I32)
                self.emit(BytecodeOpcode.JZ_ZERO, next_check)
                self.emit(BytecodeOpcode.POP)
                for body_stmt in body:
                    self.compile_stmt(body_stmt)
                self.emit(BytecodeOpcode.JMP, end_label)
                self.emit_label(next_check)
            self.emit(BytecodeOpcode.POP)
            for default_stmt in stmt.default_body:
                self.compile_stmt(default_stmt)
            self.emit_label(end_label)
            return
        if isinstance(stmt, FrontendReturn):
            self.compile_expr(stmt.expr)
            self.emit(BytecodeOpcode.HALT)
            return
        if isinstance(stmt, FrontendHalt):
            self.emit(BytecodeOpcode.HALT)
            return
        raise TypeError(f"Unsupported restricted-frontend statement: {type(stmt).__name__}")


def _assemble_program(
    *,
    name: str,
    rows: list[AssemblyRow],
    memory_layout: tuple[BytecodeMemoryCell, ...],
) -> BytecodeProgram:
    labels: dict[str, int] = {}
    emitted_rows: list[tuple[BytecodeOpcode, int | str | None] | tuple[
        BytecodeOpcode,
        int | str | None,
        tuple[BytecodeType, ...],
        tuple[BytecodeType, ...],
    ]] = []

    for row in rows:
        if isinstance(row, str):
            if not row.endswith(":"):
                raise ValueError(f"Assembly label must end with ':'; got {row!r}.")
            labels[row[:-1]] = len(emitted_rows)
            continue
        emitted_rows.append(row)

    instructions: list[BytecodeInstruction] = []
    for row in emitted_rows:
        if len(row) == 2:
            opcode, arg = row
            in_types: tuple[BytecodeType, ...] = ()
            out_types: tuple[BytecodeType, ...] = ()
        else:
            opcode, arg, in_types, out_types = row
        if isinstance(arg, str):
            arg = labels[arg]
        instructions.append(BytecodeInstruction(opcode, arg, in_types=in_types, out_types=out_types))
    return BytecodeProgram(instructions=tuple(instructions), name=name, memory_layout=memory_layout)


def compile_restricted_frontend_program(program: RestrictedFrontendProgram) -> BytecodeProgram:
    passed, error = validate_restricted_frontend_program(program)
    if not passed:
        raise ValueError(f"Restricted frontend program is invalid: {error}")
    compiler = _FrontendCompiler(program=program)
    for stmt in program.statements:
        compiler.compile_stmt(stmt)
    return _assemble_program(name=program.name, rows=compiler.rows, memory_layout=program.memory_layout)


def sum_i32_buffer_frontend_program(
    *,
    input_values: tuple[int, ...] = (7, 0, -3, 5),
    input_base_address: int = 400,
    output_address: int = 404,
    name: str | None = None,
) -> RestrictedFrontendProgram:
    input_cells = tuple(
        FrontendCell(name=f"sum_input_{offset}", address=input_base_address + offset)
        for offset in range(len(input_values))
    )
    output_cell = FrontendCell(name="sum_output", address=output_address)
    statements: list[FrontendStmt] = [
        FrontendAssign(cell_name=cell.name, expr=FrontendConst(value))
        for cell, value in zip(input_cells, input_values, strict=True)
    ]
    statements.append(FrontendAssign(cell_name=output_cell.name, expr=FrontendConst(0)))
    statements.append(FrontendFoldAdd(target_name=output_cell.name, buffer_name="sum_input"))
    statements.append(FrontendReturn(expr=FrontendLoad(output_cell.name)))
    return RestrictedFrontendProgram(
        name=name or "frontend_sum_i32_buffer_fixed4",
        cells=input_cells + (output_cell,),
        buffers=(FrontendBuffer(name="sum_input", item_names=tuple(cell.name for cell in input_cells)),),
        statements=tuple(statements),
    )


def count_nonzero_i32_buffer_frontend_program(
    *,
    input_values: tuple[int, ...] = (5, 0, -2, 0, 3),
    input_base_address: int = 416,
    output_address: int = 432,
    name: str | None = None,
) -> RestrictedFrontendProgram:
    input_cells = tuple(
        FrontendCell(name=f"count_input_{offset}", address=input_base_address + offset)
        for offset in range(len(input_values))
    )
    output_cell = FrontendCell(name="count_nonzero_output", address=output_address)
    statements: list[FrontendStmt] = [
        FrontendAssign(cell_name=cell.name, expr=FrontendConst(value))
        for cell, value in zip(input_cells, input_values, strict=True)
    ]
    statements.append(FrontendAssign(cell_name=output_cell.name, expr=FrontendConst(0)))
    statements.append(
        FrontendForEachStatic(
            buffer_name="count_input",
            item_name="item",
            body=(
                FrontendIfEq(
                    left=FrontendLoad("item"),
                    right=FrontendConst(0),
                    then_body=(),
                    else_body=(FrontendIncrement(output_cell.name),),
                ),
            ),
        )
    )
    statements.append(FrontendReturn(expr=FrontendLoad(output_cell.name)))
    return RestrictedFrontendProgram(
        name=name or "frontend_count_nonzero_i32_buffer_fixed5",
        cells=input_cells + (output_cell,),
        buffers=(FrontendBuffer(name="count_input", item_names=tuple(cell.name for cell in input_cells)),),
        statements=tuple(statements),
    )


def histogram16_u8_frontend_program(
    *,
    input_values: tuple[int, ...] = (3, 1, 3, 15),
    input_base_address: int = 448,
    bin_base_address: int = 464,
    name: str | None = None,
) -> RestrictedFrontendProgram:
    input_cells = tuple(
        FrontendCell(name=f"histogram_input_{offset}", address=input_base_address + offset)
        for offset in range(len(input_values))
    )
    bin_cells = tuple(
        FrontendCell(name=f"histogram_bin_{bucket}", address=bin_base_address + bucket)
        for bucket in range(16)
    )
    statements: list[FrontendStmt] = [
        FrontendAssign(cell_name=cell.name, expr=FrontendConst(value))
        for cell, value in zip(input_cells, input_values, strict=True)
    ]
    statements.extend(FrontendAssign(cell_name=cell.name, expr=FrontendConst(0)) for cell in bin_cells)
    statements.append(
        FrontendForEachStatic(
            buffer_name="histogram_input",
            item_name="item",
            body=(
                FrontendSwitchEq(
                    expr=FrontendLoad("item"),
                    cases=tuple((bucket, (FrontendIncrement(f"histogram_bin_{bucket}"),)) for bucket in range(16)),
                    default_body=(FrontendHalt(),),
                ),
            ),
        )
    )
    statements.append(FrontendHalt())
    return RestrictedFrontendProgram(
        name=name or "frontend_histogram16_u8_fixed4",
        cells=input_cells + bin_cells,
        buffers=(FrontendBuffer(name="histogram_input", item_names=tuple(cell.name for cell in input_cells)),),
        statements=tuple(statements),
    )


__all__ = [
    "FrontendAssign",
    "FrontendBuffer",
    "FrontendCell",
    "FrontendConst",
    "FrontendFoldAdd",
    "FrontendForEachStatic",
    "FrontendHalt",
    "FrontendIfEq",
    "FrontendIncrement",
    "FrontendLoad",
    "FrontendReturn",
    "FrontendSwitchEq",
    "RestrictedFrontendProgram",
    "compile_restricted_frontend_program",
    "count_nonzero_i32_buffer_frontend_program",
    "histogram16_u8_frontend_program",
    "serialize_restricted_frontend_program",
    "sum_i32_buffer_frontend_program",
    "validate_restricted_frontend_program",
]
