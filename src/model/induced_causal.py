"""Induce structured transition rules from reference traces and execute them online."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

from exec_trace import Program, TraceEvent, TraceInterpreter
from exec_trace.dsl import Opcode
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadStrategy,
)
from model.trainable_latest_write import TrainableLatestWriteScorer

ScalarExprName = Literal[
    "const_arg",
    "read0",
    "read1",
    "add",
    "sub",
    "eq",
    "memory_read_value",
    "zero",
    "one",
]
AddressExprName = Literal["const_arg", "read0", "read1"]
BoolExprName = Literal["always_true", "always_false", "read0_is_zero", "read0_eq_read1"]
NextPcMode = Literal["sequential", "const_arg", "branch_arg_else_seq", "self_pc"]

_SCALAR_EXPR_CANDIDATES: tuple[ScalarExprName, ...] = (
    "const_arg",
    "read0",
    "read1",
    "memory_read_value",
    "add",
    "sub",
    "eq",
    "zero",
    "one",
)
_ADDRESS_EXPR_CANDIDATES: tuple[AddressExprName, ...] = ("const_arg", "read0", "read1")
_BOOL_EXPR_CANDIDATES: tuple[BoolExprName, ...] = (
    "read0_is_zero",
    "read0_eq_read1",
    "always_true",
    "always_false",
)
_NEXT_PC_CANDIDATES: tuple[NextPcMode, ...] = ("sequential", "const_arg", "branch_arg_else_seq", "self_pc")


@dataclass(frozen=True, slots=True)
class TransitionExample:
    program_name: str
    program_steps: int
    step: int
    pc: int
    opcode: Opcode
    arg: int | None
    stack_before: tuple[int, ...]
    event: TraceEvent


@dataclass(frozen=True, slots=True)
class TransitionRule:
    opcode: Opcode
    stack_read_count: int
    pop_count: int
    push_exprs: tuple[ScalarExprName, ...]
    branch_expr: BoolExprName | None
    memory_read_address_expr: AddressExprName | None
    memory_write_address_expr: AddressExprName | None
    memory_write_value_expr: ScalarExprName | None
    next_pc_mode: NextPcMode
    halted: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "opcode": self.opcode,
            "stack_read_count": self.stack_read_count,
            "pop_count": self.pop_count,
            "push_exprs": list(self.push_exprs),
            "branch_expr": self.branch_expr,
            "memory_read_address_expr": self.memory_read_address_expr,
            "memory_write_address_expr": self.memory_write_address_expr,
            "memory_write_value_expr": self.memory_write_value_expr,
            "next_pc_mode": self.next_pc_mode,
            "halted": self.halted,
        }


@dataclass(frozen=True, slots=True)
class InducedTransitionLibrary:
    rules: tuple[TransitionRule, ...]

    def rule_for(self, opcode: Opcode) -> TransitionRule:
        for rule in self.rules:
            if rule.opcode == opcode:
                return rule
        raise KeyError(f"No induced rule was fitted for opcode {opcode}.")

    def as_dict(self) -> dict[str, object]:
        return {rule.opcode: rule.as_dict() for rule in self.rules}


def build_transition_examples(
    programs: Iterable[Program],
    *,
    interpreter: TraceInterpreter | None = None,
) -> tuple[TransitionExample, ...]:
    interpreter = interpreter or TraceInterpreter()
    examples: list[TransitionExample] = []

    for program in programs:
        result = interpreter.run(program)
        stack: list[int] = []
        memory: dict[int, int] = {}

        for event in result.events:
            examples.append(
                TransitionExample(
                    program_name=program.name,
                    program_steps=result.final_state.steps,
                    step=event.step,
                    pc=event.pc,
                    opcode=event.opcode,
                    arg=event.arg,
                    stack_before=tuple(stack),
                    event=event,
                )
            )

            if event.popped:
                observed = tuple(stack[-len(event.popped) :])
                if observed != event.popped:
                    raise RuntimeError(
                        f"Replay mismatch while building transition examples for {program.name!r}: "
                        f"expected stack suffix {event.popped}, got {observed}."
                    )
                del stack[-len(event.popped) :]
            stack.extend(event.pushed)

            if event.memory_write is not None:
                address, value = event.memory_write
                memory[address] = value

    return tuple(examples)


def _stack_reads(stack_before: Sequence[int], read_count: int) -> tuple[int, ...]:
    if read_count == 0:
        return ()
    if len(stack_before) < read_count:
        raise ValueError("Not enough stack values for this read_count.")
    return tuple(stack_before[-read_count:])


def _expected_popped(reads: Sequence[int], pop_count: int) -> tuple[int, ...]:
    if pop_count == 0:
        return ()
    return tuple(reads[-pop_count:])


def _eval_scalar_expr(
    expr: ScalarExprName,
    *,
    arg: int | None,
    reads: Sequence[int],
    memory_read_value: int | None,
) -> int:
    match expr:
        case "const_arg":
            if arg is None:
                raise ValueError("const_arg requires an integer instruction argument.")
            return arg
        case "read0":
            return reads[0]
        case "read1":
            return reads[1]
        case "add":
            return reads[0] + reads[1]
        case "sub":
            return reads[0] - reads[1]
        case "eq":
            return int(reads[0] == reads[1])
        case "memory_read_value":
            if memory_read_value is None:
                raise ValueError("memory_read_value requires an active memory read.")
            return memory_read_value
        case "zero":
            return 0
        case "one":
            return 1
        case _:
            raise ValueError(f"Unknown scalar expression: {expr}")


def _eval_address_expr(expr: AddressExprName, *, arg: int | None, reads: Sequence[int]) -> int:
    match expr:
        case "const_arg":
            if arg is None:
                raise ValueError("const_arg requires an integer instruction argument.")
            return arg
        case "read0":
            return reads[0]
        case "read1":
            return reads[1]
        case _:
            raise ValueError(f"Unknown address expression: {expr}")


def _eval_bool_expr(expr: BoolExprName, *, reads: Sequence[int]) -> bool:
    match expr:
        case "always_true":
            return True
        case "always_false":
            return False
        case "read0_is_zero":
            return reads[0] == 0
        case "read0_eq_read1":
            return reads[0] == reads[1]
        case _:
            raise ValueError(f"Unknown bool expression: {expr}")


def _eval_next_pc(
    mode: NextPcMode,
    *,
    pc: int,
    arg: int | None,
    branch_taken: bool | None,
) -> int:
    match mode:
        case "sequential":
            return pc + 1
        case "const_arg":
            if arg is None:
                raise ValueError("const_arg next-pc mode requires an integer argument.")
            return arg
        case "branch_arg_else_seq":
            if arg is None or branch_taken is None:
                raise ValueError("branch_arg_else_seq requires both arg and branch_taken.")
            return arg if branch_taken else pc + 1
        case "self_pc":
            return pc
        case _:
            raise ValueError(f"Unknown next-pc mode: {mode}")


def _fit_scalar_expr(
    examples: Sequence[TransitionExample],
    read_count: int,
    *,
    target_getter,
    memory_read_expr: AddressExprName | None,
) -> ScalarExprName:
    for expr in _SCALAR_EXPR_CANDIDATES:
        matched = True
        for example in examples:
            reads = _stack_reads(example.stack_before, read_count)
            memory_read_value = None
            if memory_read_expr is not None:
                memory_read_value = example.event.memory_read_value
            try:
                predicted = _eval_scalar_expr(
                    expr,
                    arg=example.arg,
                    reads=reads,
                    memory_read_value=memory_read_value,
                )
            except (IndexError, ValueError):
                matched = False
                break
            if predicted != target_getter(example):
                matched = False
                break
        if matched:
            return expr
    raise RuntimeError("No scalar expression matched the training examples exactly.")


def _fit_address_expr(
    examples: Sequence[TransitionExample],
    read_count: int,
    *,
    target_getter,
) -> AddressExprName:
    for expr in _ADDRESS_EXPR_CANDIDATES:
        matched = True
        for example in examples:
            reads = _stack_reads(example.stack_before, read_count)
            try:
                predicted = _eval_address_expr(expr, arg=example.arg, reads=reads)
            except (IndexError, ValueError):
                matched = False
                break
            if predicted != target_getter(example):
                matched = False
                break
        if matched:
            return expr
    raise RuntimeError("No address expression matched the training examples exactly.")


def _fit_bool_expr(
    examples: Sequence[TransitionExample],
    read_count: int,
    *,
    target_getter,
) -> BoolExprName:
    for expr in _BOOL_EXPR_CANDIDATES:
        matched = True
        for example in examples:
            reads = _stack_reads(example.stack_before, read_count)
            try:
                predicted = _eval_bool_expr(expr, reads=reads)
            except IndexError:
                matched = False
                break
            if predicted != target_getter(example):
                matched = False
                break
        if matched:
            return expr
    raise RuntimeError("No boolean expression matched the training examples exactly.")


def _fit_next_pc_mode(
    examples: Sequence[TransitionExample],
    read_count: int,
    *,
    branch_expr: BoolExprName | None,
) -> NextPcMode:
    for mode in _NEXT_PC_CANDIDATES:
        matched = True
        for example in examples:
            reads = _stack_reads(example.stack_before, read_count)
            branch_taken = None
            if branch_expr is not None:
                try:
                    branch_taken = _eval_bool_expr(branch_expr, reads=reads)
                except IndexError:
                    matched = False
                    break
            try:
                predicted = _eval_next_pc(mode, pc=example.pc, arg=example.arg, branch_taken=branch_taken)
            except ValueError:
                matched = False
                break
            if predicted != example.event.next_pc:
                matched = False
                break
        if matched:
            return mode
    raise RuntimeError("No next-pc mode matched the training examples exactly.")


def _fit_rule_for_opcode(examples: Sequence[TransitionExample], opcode: Opcode) -> TransitionRule:
    pop_counts = {len(example.event.popped) for example in examples}
    push_counts = {len(example.event.pushed) for example in examples}
    halted_values = {example.event.halted for example in examples}

    if len(pop_counts) != 1 or len(push_counts) != 1 or len(halted_values) != 1:
        raise RuntimeError(f"Opcode {opcode} does not have stable structural arity in the training set.")

    pop_count = next(iter(pop_counts))
    push_count = next(iter(push_counts))
    halted = next(iter(halted_values))

    memory_read_present = any(example.event.memory_read_address is not None for example in examples)
    memory_write_present = any(example.event.memory_write is not None for example in examples)
    branch_present = any(example.event.branch_taken is not None for example in examples)

    for read_count in range(pop_count, 3):
        try:
            reads_per_example = [_stack_reads(example.stack_before, read_count) for example in examples]
        except ValueError:
            continue

        if not all(
            _expected_popped(reads, pop_count) == example.event.popped
            for reads, example in zip(reads_per_example, examples)
        ):
            continue

        try:
            branch_expr = None
            if branch_present:
                branch_expr = _fit_bool_expr(
                    examples,
                    read_count,
                    target_getter=lambda example: bool(example.event.branch_taken),
                )

            memory_read_address_expr = None
            if memory_read_present:
                memory_read_address_expr = _fit_address_expr(
                    examples,
                    read_count,
                    target_getter=lambda example: int(example.event.memory_read_address),
                )

            push_exprs: list[ScalarExprName] = []
            for index in range(push_count):
                push_exprs.append(
                    _fit_scalar_expr(
                        examples,
                        read_count,
                        target_getter=lambda example, idx=index: example.event.pushed[idx],
                        memory_read_expr=memory_read_address_expr,
                    )
                )

            memory_write_address_expr = None
            memory_write_value_expr = None
            if memory_write_present:
                memory_write_address_expr = _fit_address_expr(
                    examples,
                    read_count,
                    target_getter=lambda example: int(example.event.memory_write[0]),
                )
                memory_write_value_expr = _fit_scalar_expr(
                    examples,
                    read_count,
                    target_getter=lambda example: int(example.event.memory_write[1]),
                    memory_read_expr=memory_read_address_expr,
                )

            next_pc_mode = _fit_next_pc_mode(examples, read_count, branch_expr=branch_expr)
        except RuntimeError:
            continue

        return TransitionRule(
            opcode=opcode,
            stack_read_count=read_count,
            pop_count=pop_count,
            push_exprs=tuple(push_exprs),
            branch_expr=branch_expr,
            memory_read_address_expr=memory_read_address_expr,
            memory_write_address_expr=memory_write_address_expr,
            memory_write_value_expr=memory_write_value_expr,
            next_pc_mode=next_pc_mode,
            halted=halted,
        )

    raise RuntimeError(f"Could not induce an exact transition rule for opcode {opcode}.")


def fit_transition_library(
    programs: Iterable[Program],
    *,
    interpreter: TraceInterpreter | None = None,
) -> InducedTransitionLibrary:
    examples = build_transition_examples(programs, interpreter=interpreter)
    by_opcode: dict[Opcode, list[TransitionExample]] = {}
    for example in examples:
        by_opcode.setdefault(example.opcode, []).append(example)

    rules = tuple(_fit_rule_for_opcode(by_opcode[opcode], opcode) for opcode in sorted(by_opcode, key=str))
    return InducedTransitionLibrary(rules=rules)


class InducedTransitionExecutor(FreeRunningTraceExecutor):
    """Execute programs using induced structured transition rules."""

    def __init__(
        self,
        library: InducedTransitionLibrary,
        *,
        stack_strategy: ReadStrategy = "accelerated",
        memory_strategy: Literal["linear", "accelerated"] = "accelerated",
        stack_scorer: TrainableLatestWriteScorer | None = None,
        default_memory_value: int = 0,
        validate_exact_reads: bool = True,
    ) -> None:
        super().__init__(
            stack_strategy=stack_strategy,
            memory_strategy=memory_strategy,
            stack_scorer=stack_scorer,
            default_memory_value=default_memory_value,
            validate_exact_reads=validate_exact_reads,
        )
        self.library = library

    def _execute_instruction(
        self,
        *,
        step: int,
        pc: int,
        stack_depth: int,
        call_depth: int,
        instruction: Opcode,
        arg: int | None,
        stack_history,
        memory_history,
        call_history,
        read_observations,
    ):
        if instruction in {Opcode.CALL, Opcode.RET}:
            return super()._execute_instruction(
                step=step,
                pc=pc,
                stack_depth=stack_depth,
                call_depth=call_depth,
                instruction=instruction,
                arg=arg,
                stack_history=stack_history,
                memory_history=memory_history,
                call_history=call_history,
                read_observations=read_observations,
            )
        rule = self.library.rule_for(instruction)
        reads = (
            ()
            if rule.stack_read_count == 0
            else self._read_stack_suffix(
                step=step,
                count=rule.stack_read_count,
                stack_depth=stack_depth,
                stack_history=stack_history,
                read_observations=read_observations,
            )
        )

        memory_read = None
        memory_read_value = None
        if rule.memory_read_address_expr is not None:
            address = _eval_address_expr(rule.memory_read_address_expr, arg=arg, reads=reads)
            if address < 0:
                raise RuntimeError("Induced executor produced a negative memory-read address.")
            memory_read_value = self._read_memory(
                step=step,
                address=address,
                memory_history=memory_history,
                read_observations=read_observations,
            )
            memory_read = (address, memory_read_value)

        pushed = tuple(
            _eval_scalar_expr(expr, arg=arg, reads=reads, memory_read_value=memory_read_value)
            for expr in rule.push_exprs
        )
        popped = _expected_popped(reads, rule.pop_count)

        branch_taken = None
        if rule.branch_expr is not None:
            branch_taken = _eval_bool_expr(rule.branch_expr, reads=reads)

        memory_write = None
        if rule.memory_write_address_expr is not None and rule.memory_write_value_expr is not None:
            address = _eval_address_expr(rule.memory_write_address_expr, arg=arg, reads=reads)
            if address < 0:
                raise RuntimeError("Induced executor produced a negative memory-write address.")
            value = _eval_scalar_expr(
                rule.memory_write_value_expr,
                arg=arg,
                reads=reads,
                memory_read_value=memory_read_value,
            )
            memory_write = (address, value)

        next_pc = _eval_next_pc(rule.next_pc_mode, pc=pc, arg=arg, branch_taken=branch_taken)
        return (popped, pushed, branch_taken, memory_read, memory_write, next_pc, rule.halted, call_depth)


def run_free_running_with_induced_rules(
    program: Program,
    library: InducedTransitionLibrary,
    *,
    decode_mode: Literal["linear", "accelerated"] = "accelerated",
    max_steps: int = 10_000,
) -> FreeRunningExecutionResult:
    executor = InducedTransitionExecutor(
        library,
        stack_strategy=decode_mode,
        memory_strategy=decode_mode,
    )
    return executor.run(program, max_steps=max_steps)


def run_free_running_with_induced_rules_and_stack_scorer(
    program: Program,
    library: InducedTransitionLibrary,
    scorer: TrainableLatestWriteScorer,
    *,
    memory_mode: Literal["linear", "accelerated"] = "accelerated",
    max_steps: int = 10_000,
) -> FreeRunningExecutionResult:
    executor = InducedTransitionExecutor(
        library,
        stack_strategy="trainable",
        memory_strategy=memory_mode,
        stack_scorer=scorer,
    )
    return executor.run(program, max_steps=max_steps)
