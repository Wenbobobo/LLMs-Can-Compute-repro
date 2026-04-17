"""Free-running latest-write executor over the append-only trace substrate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Literal, Sequence

from exec_trace import ExecutionState, Program, TraceEvent, TraceInterpreter, replay_trace
from exec_trace.dsl import Opcode
from geometry import HullKVCache, brute_force_hardmax_2d
from model.exact_hardmax import encode_latest_write_key, encode_latest_write_query
from model.trainable_latest_write import LatestWriteCandidate, TrainableLatestWriteScorer, bucket_name

ReadStrategy = Literal[
    "linear",
    "accelerated",
    "partitioned_exact",
    "pointer_like_exact",
    "staged_exact",
    "trainable",
]
SpaceName = Literal["stack", "memory", "call"]


@dataclass(frozen=True, slots=True)
class ReadObservation:
    step: int
    space: SpaceName
    address: int
    source: ReadStrategy
    chosen_value: int
    linear_value: int
    accelerated_value: int


@dataclass(frozen=True, slots=True)
class FreeRunningExecutionResult:
    program: Program
    events: tuple[TraceEvent, ...]
    final_state: ExecutionState
    read_observations: tuple[ReadObservation, ...]
    stack_strategy: ReadStrategy
    memory_strategy: ReadStrategy


@dataclass(frozen=True, slots=True)
class ProgramExecutionOutcome:
    program_name: str
    program_steps: int
    exact_trace_match: bool
    exact_final_state_match: bool
    first_mismatch_step: int | None
    failure_reason: str | None = None


@dataclass(frozen=True, slots=True)
class FreeRunningEvaluation:
    exact_trace_accuracy: float
    exact_final_state_accuracy: float
    program_count: int
    by_length_bucket: tuple[tuple[str, dict[str, float | int]], ...]
    outcomes: tuple[ProgramExecutionOutcome, ...]


class _LatestWriteSpace:
    """Maintain one append-only latest-write history for a logical address space."""

    def __init__(
        self,
        *,
        epsilon: Fraction,
        default_value: int,
        allow_default_reads: bool,
    ) -> None:
        self.epsilon = epsilon
        self.default_value = default_value
        self.allow_default_reads = allow_default_reads
        self._seen_addresses: set[int] = set()
        self._linear_keys: list[tuple[int, Fraction]] = []
        self._linear_values: list[int] = []
        self._accelerated = HullKVCache()
        self._latest_by_address: dict[int, int] = {}
        self._latest_candidate_index_by_address: dict[int, int] = {}
        self._candidate_values: list[int] = []
        self._staged_head_by_address: dict[int, int] = {}
        self._staged_values: list[int] = []
        self._staged_prev_index: list[int | None] = []
        self._candidates: list[LatestWriteCandidate] = []

    @property
    def candidates(self) -> tuple[LatestWriteCandidate, ...]:
        return tuple(self._candidates)

    def write(self, address: int, value: int, step: int) -> None:
        self._seed_address(address)
        key = encode_latest_write_key(address, step, self.epsilon)
        self._linear_keys.append(key)
        self._linear_values.append(value)
        self._accelerated.insert(key, value)
        self._latest_by_address[address] = value
        self._record_candidate(address=address, value=value, step=step)

    def read_linear(self, address: int) -> int:
        self._ensure_readable_address(address)
        query = encode_latest_write_query(address)
        linear_value = brute_force_hardmax_2d(self._linear_keys, self._linear_values, query).value
        if not isinstance(linear_value, int):
            raise TypeError("Latest-write runtime expects scalar integer values.")
        return linear_value

    def read_accelerated(self, address: int) -> int:
        self._ensure_readable_address(address)
        query = encode_latest_write_query(address)
        accelerated_value = self._accelerated.query(query).value
        if not isinstance(accelerated_value, int):
            raise TypeError("Latest-write runtime expects scalar integer values.")
        return accelerated_value

    def read_exact(self, address: int) -> tuple[int, int]:
        return (self.read_linear(address), self.read_accelerated(address))

    def read_partitioned(self, address: int) -> int:
        self._ensure_readable_address(address)
        return self._latest_by_address[address]

    def read_pointer_like(self, address: int) -> int:
        self._ensure_readable_address(address)
        latest_index = self._latest_candidate_index_by_address[address]
        return self._candidate_values[latest_index]

    def read_staged_exact(self, address: int) -> int:
        self._ensure_readable_address(address)
        head_index = self._staged_head_by_address[address]
        if head_index < 0:
            raise RuntimeError(f"Invalid staged head index for address {address}.")
        return self._staged_values[head_index]

    def _seed_address(self, address: int) -> None:
        if address in self._seen_addresses:
            return
        self._seen_addresses.add(address)
        key = encode_latest_write_key(address, -1, self.epsilon)
        self._linear_keys.append(key)
        self._linear_values.append(self.default_value)
        self._accelerated.insert(key, self.default_value)
        self._latest_by_address[address] = self.default_value
        self._record_candidate(address=address, value=self.default_value, step=-1, is_default=True)

    def _record_candidate(self, *, address: int, value: int, step: int, is_default: bool = False) -> None:
        self._candidates.append(LatestWriteCandidate(address=address, step=step, value=value, is_default=is_default))
        self._candidate_values.append(value)
        candidate_index = len(self._candidate_values) - 1
        self._latest_candidate_index_by_address[address] = candidate_index

        previous_index = self._staged_head_by_address.get(address)
        self._staged_values.append(value)
        self._staged_prev_index.append(previous_index)
        self._staged_head_by_address[address] = len(self._staged_values) - 1

    def _ensure_readable_address(self, address: int) -> None:
        if address in self._seen_addresses:
            return
        if not self.allow_default_reads:
            raise RuntimeError(f"Address {address} was read before any write in this space.")
        self._seed_address(address)


class FreeRunningTraceExecutor:
    """Execute programs online using latest-write retrieval over append-only history."""

    def __init__(
        self,
        *,
        stack_strategy: ReadStrategy = "accelerated",
        memory_strategy: ReadStrategy = "accelerated",
        stack_scorer: TrainableLatestWriteScorer | None = None,
        default_memory_value: int = 0,
        validate_exact_reads: bool = True,
    ) -> None:
        if stack_strategy == "partitioned_exact":
            raise ValueError("stack_strategy='partitioned_exact' is reserved for memory-only counterfactual probes.")
        if stack_strategy == "trainable" and stack_scorer is None:
            raise ValueError("stack_strategy='trainable' requires a stack_scorer.")
        if stack_strategy != "trainable" and stack_scorer is not None:
            raise ValueError("stack_scorer should only be provided for trainable stack execution.")
        if memory_strategy == "trainable":
            raise ValueError("memory_strategy='trainable' is unsupported for free-running exact execution.")

        self.stack_strategy = stack_strategy
        self.memory_strategy = memory_strategy
        self.call_strategy: ReadStrategy = "pointer_like_exact" if stack_strategy == "trainable" else stack_strategy
        self.stack_scorer = stack_scorer
        self.default_memory_value = default_memory_value
        self.validate_exact_reads = validate_exact_reads

    def run(self, program: Program, *, max_steps: int = 10_000) -> FreeRunningExecutionResult:
        epsilon = Fraction(1, max_steps + 2)
        stack_history = _LatestWriteSpace(
            epsilon=epsilon,
            default_value=0,
            allow_default_reads=False,
        )
        memory_history = _LatestWriteSpace(
            epsilon=epsilon,
            default_value=self.default_memory_value,
            allow_default_reads=True,
        )
        call_history = _LatestWriteSpace(
            epsilon=epsilon,
            default_value=0,
            allow_default_reads=False,
        )

        events: list[TraceEvent] = []
        read_observations: list[ReadObservation] = []
        step = 0
        pc = 0
        stack_depth = 0
        call_depth = 0
        halted = False

        while not halted:
            if step >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= pc < len(program)):
                raise RuntimeError(f"Program counter out of range: {pc}")

            instruction = program.instructions[pc]
            execution_result = self._execute_instruction(
                step=step,
                pc=pc,
                stack_depth=stack_depth,
                call_depth=call_depth,
                instruction=instruction.opcode,
                arg=instruction.arg,
                stack_history=stack_history,
                memory_history=memory_history,
                call_history=call_history,
                read_observations=read_observations,
            )
            popped, pushed, branch_taken, memory_read, memory_write, next_pc, halted, call_depth = execution_result

            event = TraceEvent(
                step=step,
                pc=pc,
                opcode=instruction.opcode,
                arg=instruction.arg,
                popped=popped,
                pushed=pushed,
                branch_taken=branch_taken,
                memory_read_address=None if memory_read is None else memory_read[0],
                memory_read_value=None if memory_read is None else memory_read[1],
                memory_write=memory_write,
                next_pc=next_pc,
                stack_depth_before=stack_depth,
                stack_depth_after=stack_depth - len(popped) + len(pushed),
                halted=halted,
            )
            events.append(event)

            write_base = stack_depth - len(popped)
            for offset, value in enumerate(pushed):
                stack_history.write(write_base + offset, value, step)
            if memory_write is not None:
                memory_history.write(memory_write[0], memory_write[1], step)

            step += 1
            pc = next_pc
            stack_depth = event.stack_depth_after

        final_state = replay_trace(program, tuple(events))
        return FreeRunningExecutionResult(
            program=program,
            events=tuple(events),
            final_state=final_state,
            read_observations=tuple(read_observations),
            stack_strategy=self.stack_strategy,
            memory_strategy=self.memory_strategy,
        )

    def _execute_instruction(
        self,
        *,
        step: int,
        pc: int,
        stack_depth: int,
        call_depth: int,
        instruction: Opcode,
        arg: int | None,
        stack_history: _LatestWriteSpace,
        memory_history: _LatestWriteSpace,
        call_history: _LatestWriteSpace,
        read_observations: list[ReadObservation],
    ) -> tuple[
        tuple[int, ...],
        tuple[int, ...],
        bool | None,
        tuple[int, int] | None,
        tuple[int, int] | None,
        int,
        bool,
        int,
    ]:
        next_pc = pc + 1
        branch_taken: bool | None = None
        memory_read: tuple[int, int] | None = None
        memory_write: tuple[int, int] | None = None
        halted = False

        match instruction:
            case Opcode.PUSH_CONST:
                if arg is None:
                    raise RuntimeError("push_const requires an integer argument.")
                return ((), (arg,), None, None, None, next_pc, False, call_depth)
            case Opcode.ADD:
                lhs, rhs = self._read_stack_suffix(
                    step=step,
                    count=2,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                return ((lhs, rhs), (lhs + rhs,), None, None, None, next_pc, False, call_depth)
            case Opcode.SUB:
                lhs, rhs = self._read_stack_suffix(
                    step=step,
                    count=2,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                return ((lhs, rhs), (lhs - rhs,), None, None, None, next_pc, False, call_depth)
            case Opcode.EQ:
                lhs, rhs = self._read_stack_suffix(
                    step=step,
                    count=2,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                return ((lhs, rhs), (int(lhs == rhs),), None, None, None, next_pc, False, call_depth)
            case Opcode.DUP:
                (value,) = self._read_stack_suffix(
                    step=step,
                    count=1,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                return ((), (value,), None, None, None, next_pc, False, call_depth)
            case Opcode.POP:
                (value,) = self._read_stack_suffix(
                    step=step,
                    count=1,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                return ((value,), (), None, None, None, next_pc, False, call_depth)
            case Opcode.LOAD:
                if arg is None:
                    raise RuntimeError("load requires an integer address.")
                if arg < 0:
                    raise RuntimeError("load address must be non-negative.")
                value = self._read_memory(
                    step=step,
                    address=arg,
                    memory_history=memory_history,
                    read_observations=read_observations,
                )
                memory_read = (arg, value)
                return ((), (value,), None, memory_read, None, next_pc, False, call_depth)
            case Opcode.STORE:
                if arg is None:
                    raise RuntimeError("store requires an integer address.")
                if arg < 0:
                    raise RuntimeError("store address must be non-negative.")
                (value,) = self._read_stack_suffix(
                    step=step,
                    count=1,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                memory_write = (arg, value)
                return ((value,), (), None, None, memory_write, next_pc, False, call_depth)
            case Opcode.LOAD_AT:
                (address,) = self._read_stack_suffix(
                    step=step,
                    count=1,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                if address < 0:
                    raise RuntimeError("load_at address must be non-negative.")
                value = self._read_memory(
                    step=step,
                    address=address,
                    memory_history=memory_history,
                    read_observations=read_observations,
                )
                memory_read = (address, value)
                return ((address,), (value,), None, memory_read, None, next_pc, False, call_depth)
            case Opcode.STORE_AT:
                value, address = self._read_stack_suffix(
                    step=step,
                    count=2,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                if address < 0:
                    raise RuntimeError("store_at address must be non-negative.")
                memory_write = (address, value)
                return ((value, address), (), None, None, memory_write, next_pc, False, call_depth)
            case Opcode.JMP:
                if arg is None:
                    raise RuntimeError("jmp requires a target PC.")
                return ((), (), True, None, None, arg, False, call_depth)
            case Opcode.JZ:
                if arg is None:
                    raise RuntimeError("jz requires a target PC.")
                (condition,) = self._read_stack_suffix(
                    step=step,
                    count=1,
                    stack_depth=stack_depth,
                    stack_history=stack_history,
                    read_observations=read_observations,
                )
                branch_taken = condition == 0
                return ((condition,), (), branch_taken, None, None, arg if branch_taken else next_pc, False, call_depth)
            case Opcode.CALL:
                if arg is None:
                    raise RuntimeError("call requires a target PC.")
                call_history.write(call_depth, pc + 1, step)
                return ((), (), True, None, None, arg, False, call_depth + 1)
            case Opcode.RET:
                if call_depth <= 0:
                    raise RuntimeError("ret requires a pending return address.")
                return_pc = self._read_from_space(
                    step=step,
                    address=call_depth - 1,
                    space="call",
                    strategy=self.call_strategy,
                    history=call_history,
                    scorer=None,
                    read_observations=read_observations,
                )
                return ((), (), True, None, None, return_pc, False, call_depth - 1)
            case Opcode.HALT:
                return ((), (), None, None, None, pc, True, call_depth)
            case _:
                raise RuntimeError(f"Unsupported opcode: {instruction}")

    def _read_stack_suffix(
        self,
        *,
        step: int,
        count: int,
        stack_depth: int,
        stack_history: _LatestWriteSpace,
        read_observations: list[ReadObservation],
    ) -> tuple[int, ...]:
        if stack_depth < count:
            raise RuntimeError("Stack underflow during free-running execution.")

        values: list[int] = []
        for address in range(stack_depth - count, stack_depth):
            values.append(
                self._read_from_space(
                    step=step,
                    address=address,
                    space="stack",
                    strategy=self.stack_strategy,
                    history=stack_history,
                    scorer=self.stack_scorer,
                    read_observations=read_observations,
                )
            )
        return tuple(values)

    def _read_memory(
        self,
        *,
        step: int,
        address: int,
        memory_history: _LatestWriteSpace,
        read_observations: list[ReadObservation],
    ) -> int:
        return self._read_from_space(
            step=step,
            address=address,
            space="memory",
            strategy=self.memory_strategy,
            history=memory_history,
            scorer=None,
            read_observations=read_observations,
        )

    def _read_from_space(
        self,
        *,
        step: int,
        address: int,
        space: SpaceName,
        strategy: ReadStrategy,
        history: _LatestWriteSpace,
        scorer: TrainableLatestWriteScorer | None,
        read_observations: list[ReadObservation],
    ) -> int:
        linear_value: int | None = None
        accelerated_value: int | None = None
        partitioned_value: int | None = None
        pointer_value: int | None = None
        staged_value: int | None = None

        if strategy == "linear":
            linear_value = history.read_linear(address)
            chosen_value = linear_value
        elif strategy == "accelerated":
            accelerated_value = history.read_accelerated(address)
            chosen_value = accelerated_value
        elif strategy == "partitioned_exact":
            if space != "memory":
                raise RuntimeError("partitioned_exact is only supported for memory reads.")
            partitioned_value = history.read_partitioned(address)
            chosen_value = partitioned_value
        elif strategy == "pointer_like_exact":
            pointer_value = history.read_pointer_like(address)
            chosen_value = pointer_value
        elif strategy == "staged_exact":
            staged_value = history.read_staged_exact(address)
            chosen_value = staged_value
        elif strategy == "trainable":
            if scorer is None:
                raise RuntimeError("Trainable stack reads require a scorer.")
            chosen_value = scorer.predict_value_for_query(address, history.candidates)
        else:
            raise RuntimeError(f"Unsupported read strategy: {strategy}")

        if self.validate_exact_reads:
            if linear_value is None:
                linear_value = history.read_linear(address)
            if accelerated_value is None:
                accelerated_value = history.read_accelerated(address)
            if partitioned_value is None:
                partitioned_value = history.read_partitioned(address)
            if pointer_value is None:
                pointer_value = history.read_pointer_like(address)
            if staged_value is None:
                staged_value = history.read_staged_exact(address)

        if self.validate_exact_reads and linear_value != accelerated_value:
            raise RuntimeError(
                f"Exact read mismatch at step {step} for {space}[{address}]: "
                f"{linear_value} != {accelerated_value}"
            )
        if self.validate_exact_reads and partitioned_value != linear_value:
            raise RuntimeError(
                f"Partitioned exact read mismatch at step {step} for {space}[{address}]: "
                f"{partitioned_value} != {linear_value}"
            )
        if self.validate_exact_reads and pointer_value != linear_value:
            raise RuntimeError(
                f"Pointer-like exact read mismatch at step {step} for {space}[{address}]: "
                f"{pointer_value} != {linear_value}"
            )
        if self.validate_exact_reads and staged_value != linear_value:
            raise RuntimeError(
                f"Staged exact read mismatch at step {step} for {space}[{address}]: "
                f"{staged_value} != {linear_value}"
            )

        if linear_value is None:
            linear_value = chosen_value
        if accelerated_value is None:
            accelerated_value = chosen_value

        read_observations.append(
            ReadObservation(
                step=step,
                space=space,
                address=address,
                source=strategy,
                chosen_value=chosen_value,
                linear_value=linear_value,
                accelerated_value=accelerated_value,
            )
        )
        return chosen_value


def run_free_running_exact(
    program: Program,
    *,
    decode_mode: Literal["linear", "accelerated"] = "accelerated",
    max_steps: int = 10_000,
) -> FreeRunningExecutionResult:
    executor = FreeRunningTraceExecutor(
        stack_strategy=decode_mode,
        memory_strategy=decode_mode,
    )
    return executor.run(program, max_steps=max_steps)


def run_free_running_with_stack_scorer(
    program: Program,
    scorer: TrainableLatestWriteScorer,
    *,
    memory_mode: Literal[
        "linear",
        "accelerated",
        "partitioned_exact",
        "pointer_like_exact",
        "staged_exact",
    ] = "accelerated",
    max_steps: int = 10_000,
) -> FreeRunningExecutionResult:
    executor = FreeRunningTraceExecutor(
        stack_strategy="trainable",
        memory_strategy=memory_mode,
        stack_scorer=scorer,
    )
    return executor.run(program, max_steps=max_steps)


def compare_execution_to_reference(
    program: Program,
    execution: FreeRunningExecutionResult,
    *,
    reference: FreeRunningExecutionResult | None = None,
) -> ProgramExecutionOutcome:
    reference_result = reference
    if reference_result is None:
        oracle = TraceInterpreter().run(program)
        reference_events = oracle.events
        reference_state = oracle.final_state
        program_steps = oracle.final_state.steps
    else:
        reference_events = reference.events
        reference_state = reference.final_state
        program_steps = reference.final_state.steps

    first_mismatch_step: int | None = None
    for produced, expected in zip(execution.events, reference_events):
        if produced != expected:
            first_mismatch_step = produced.step
            break

    if first_mismatch_step is None and len(execution.events) != len(reference_events):
        first_mismatch_step = min(len(execution.events), len(reference_events))

    return ProgramExecutionOutcome(
        program_name=program.name,
        program_steps=program_steps,
        exact_trace_match=tuple(execution.events) == tuple(reference_events),
        exact_final_state_match=execution.final_state == reference_state,
        first_mismatch_step=first_mismatch_step,
    )


def evaluate_free_running_programs(
    programs: Sequence[Program],
    runner: Callable[[Program], FreeRunningExecutionResult],
) -> FreeRunningEvaluation:
    interpreter = TraceInterpreter()
    outcomes: list[ProgramExecutionOutcome] = []
    per_bucket: dict[str, dict[str, int]] = {}

    for program in programs:
        reference = interpreter.run(program)
        try:
            execution = runner(program)
            outcome = compare_execution_to_reference(
                program,
                execution,
                reference=FreeRunningExecutionResult(
                    program=program,
                    events=reference.events,
                    final_state=reference.final_state,
                    read_observations=(),
                    stack_strategy="linear",
                    memory_strategy="linear",
                ),
            )
        except Exception as exc:  # pragma: no cover - exercised through evaluation exports
            outcome = ProgramExecutionOutcome(
                program_name=program.name,
                program_steps=reference.final_state.steps,
                exact_trace_match=False,
                exact_final_state_match=False,
                first_mismatch_step=None,
                failure_reason=str(exc),
            )

        outcomes.append(outcome)
        bucket = bucket_name(outcome.program_steps)
        # Avoid eager instantiation of default dict on every iteration
        if bucket not in per_bucket:
            per_bucket[bucket] = {
                "program_count": 0,
                "exact_trace_count": 0,
                "exact_final_state_count": 0,
            }
        bucket_state = per_bucket[bucket]
        bucket_state["program_count"] += 1
        bucket_state["exact_trace_count"] += int(outcome.exact_trace_match)
        bucket_state["exact_final_state_count"] += int(outcome.exact_final_state_match)

    bucket_rows: list[tuple[str, dict[str, float | int]]] = []
    for name in sorted(per_bucket):
        bucket_state = per_bucket[name]
        bucket_rows.append(
            (
                name,
                {
                    "program_count": bucket_state["program_count"],
                    "exact_trace_accuracy": bucket_state["exact_trace_count"] / bucket_state["program_count"],
                    "exact_final_state_accuracy": bucket_state["exact_final_state_count"]
                    / bucket_state["program_count"],
                },
            )
        )

    program_count = len(outcomes)
    exact_trace_total = sum(int(outcome.exact_trace_match) for outcome in outcomes)
    exact_final_state_total = sum(int(outcome.exact_final_state_match) for outcome in outcomes)

    return FreeRunningEvaluation(
        exact_trace_accuracy=exact_trace_total / program_count if program_count else 0.0,
        exact_final_state_accuracy=exact_final_state_total / program_count if program_count else 0.0,
        program_count=program_count,
        by_length_bucket=tuple(bucket_rows),
        outcomes=tuple(outcomes),
    )
