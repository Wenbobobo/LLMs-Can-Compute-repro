# 2026-03-25 Post-H59 GPTPro Re-Interview Dossier

## How To Use This Dossier

This document is written for a single long-form GPTPro consultation.

Important constraints:

- GPTPro cannot browse the repository.
- Treat this dossier as the full working context.
- Think for a long time before answering.
- Prefer a hard scientific judgment over a diplomatic one.
- If the current route is dead, say so directly.
- If one materially different route is still credible, name it concretely and
  explain why it is not just the current lane in disguise.

Please answer only after considering the full document, including the code
appendix.

## What This Project Was Trying To Reproduce

We are not trying to defend a broad "LLMs are computers" slogan.

The serious scientific reading of the Percepta note plus three follow-up
discussions is narrower:

1. deterministic computation may be rewritten as an append-only execution
   trace;
2. state reads in that trace may reduce to a small number of latest-write or
   stack/control retrieval operations;
3. those retrieval operations may admit exact low-dimensional hard-max
   implementations, especially in `2D`; and
4. a narrow executor or coprocessor might therefore be implemented inside a
   transformer-compatible retrieval mechanism.

The current repository already has a real narrow positive result on that
interpretation, but it does not yet reproduce the broader public headline.

## Current Scientific State

### What is genuinely supported

- Append-only execution traces are a real substrate here.
- Exact latest-write and stack/control retrieval is real here.
- A narrow exact executor on bounded admitted surfaces is real here.
- `H43_post_r44_useful_case_refreeze` remains a meaningful paper-grade
  endpoint for narrow useful-case execution.

### What is now disconfirmed

- The current internal accelerated executor path does not retain bounded value
  over simpler baselines on the best currently justified route.
- This is not only an old systems complaint. The negative result survives even
  after narrowing all the way down to native useful-kernel trace programs.

### Strongest current falsifier

`R62_origin_native_useful_kernel_value_discriminator_gate`:

- `planned_case_count = 4`
- `executed_case_count = 4`
- `exact_case_count = 4`
- `exact_kernel_count = 2`
- `longest_row_accelerated_faster_than_linear_count = 0`
- `longest_row_within_external_order_count = 0`
- `geomean_linear_over_accelerated_speedup = 0.4059897369584522`

Interpretation:

- exactness survives;
- value does not;
- the current executor-value lane is therefore closed.

### Current repo-level decision

`H58_post_r62_origin_value_boundary_closeout_packet` selected:

- `stop_as_mechanism_supported_but_no_bounded_executor_value`

The next current control packet, `H59`, reframes this as:

- narrow mechanism reproduction succeeded;
- broad headline reproduction did not; and
- any future reopen must use a materially different cost structure.

## Are We In A Dead End?

The careful answer is:

- not globally dead;
- yes, locally dead on the current executor-value lane.

Why it is not globally dead:

- the append-only retrieval substrate is real;
- the exact executor substrate is real; and
- the project already achieved a defensible narrow positive endpoint.

Why the current lane is dead enough to stop:

- same-endpoint or adjacent value/system stories have repeatedly gone
  negative;
- `R57`, `R61`, and now `R62` all fail the bounded-value question in stronger
  and cleaner forms; and
- repeating another narrow executor micro-suite on the same runtime path would
  not be scientifically honest progress.

## Distance From The Public Percepta Headline

We remain far from any broad influential positive reproduction of the public
framing.

Missing pieces include:

- no arbitrary `C` or broad Wasm support;
- no million-step exactness story on a broad semantics surface;
- no convincing bounded system value over simpler baselines;
- no evidence that the narrow executor path remains worthwhile once compared to
  transparent external execution; and
- no evidence that the mechanism can be widened without paying major costs.

What we do have instead is a sharper and more useful partial falsification:

> A narrow append-only trace executor with exact retrieval-backed execution is
> real, but bounded executor value is not established and is currently
> disconfirmed on the strongest route we were able to justify.

## What We Need From GPTPro

We need a judgment, not encouragement.

Specifically:

1. Are we interpreting the Percepta scientific target correctly?
2. Given the evidence below, is the current lane scientifically over?
3. If one future route is still credible, what exact route is it?
4. If no such route is credible, should the project stop rather than spend
   more resources?
5. If a route is credible, what stop rules should be written before execution?

## Current Architecture In One Paragraph

The repo has a reference append-only stack-machine trace DSL, reference
interpreters that emit `TraceEvent` rows, exact `2D` hard-max reference
semantics, an accelerated `HullKVCache` with exact tie fallback, and a
latest-write decode layer that rewrites memory/stack/call retrieval into exact
hard-max queries. Higher layers use those pieces to demonstrate exact replay
and bounded useful-case execution on admitted surfaces, but the value question
remains negative once compared against simpler baselines.

## Code Appendix

Below are the key local code excerpts that best expose the scientific contract.

### 1. Exact hard-max reference semantics

File: `src/geometry/hardmax.py`

```python
"""Reference implementation for exact 2D hard-max retrieval."""

from dataclasses import dataclass
from fractions import Fraction

def dot_2d(key, query) -> Fraction:
    kx, ky = _coerce_key(key)
    qx, qy = _coerce_key(query)
    return (kx * qx) + (ky * qy)

@dataclass(frozen=True, slots=True)
class HardmaxResult:
    score: NumberLike
    value: NumberLike | tuple[NumberLike, ...]
    maximizer_indices: tuple[int, ...]

def brute_force_hardmax_2d(keys, values, query) -> HardmaxResult:
    if len(keys) != len(values):
        raise ValueError("keys and values must have the same length.")
    if not keys:
        raise ValueError("At least one key/value pair is required.")

    query_key = _coerce_key(query)
    best_score: Fraction | None = None
    maximizer_indices: list[int] = []
    for index, key in enumerate(keys):
        score = dot_2d(key, query_key)
        if best_score is None or score > best_score:
            best_score = score
            maximizer_indices = [index]
        elif score == best_score:
            maximizer_indices.append(index)

    accumulator = [Fraction(0) for _ in range(first_shape)]
    for index in maximizer_indices:
        for coord_index, coord in enumerate(coerced_values[index]):
            accumulator[coord_index] += coord

    divisor = Fraction(len(maximizer_indices))
    averaged = tuple(coord / divisor for coord in accumulator)
    return HardmaxResult(
        score=_normalize_number(best_score),
        value=_restore_value(averaged, scalar_flags[0]),
        maximizer_indices=tuple(maximizer_indices),
    )
```

Reason this matters: the whole executor stack ultimately reduces retrieval to
this exact tie-aware contract.

### 2. Accelerated `2D` retrieval with exact tie fallback

File: `src/geometry/hull_kv.py`

```python
def _build_upper_envelope(points, negate: bool = False) -> _Envelope:
    sign = Fraction(-1 if negate else 1)
    best_by_slope: dict[Fraction, _EnvelopeLine] = {}
    for point_index, point in enumerate(points):
        x_coord, y_coord = point.key
        candidate = _EnvelopeLine(
            slope=sign * x_coord,
            intercept=sign * y_coord,
            point_index=point_index,
        )
        existing = best_by_slope.get(candidate.slope)
        if existing is None or candidate.intercept > existing.intercept:
            best_by_slope[candidate.slope] = candidate
    ...

class HullKVCache:
    def insert(self, key, value) -> None:
        coerced_key = _coerce_key(key)
        coerced_value, is_scalar = _coerce_value(value)
        ...
        self._entries.append((coerced_key, coerced_value))
        self._dirty = True

    def query(self, query) -> HardmaxResult:
        self._rebuild_if_needed()
        qx, qy = _coerce_key(query)
        if qx == 0 and qy == 0:
            ...
        slope = qx / qy
        envelope = self._upper_envelope if qy > 0 else self._negated_upper_envelope
        point_index = envelope.point_index_for_slope(slope)
        point = self._points[point_index]
        score = dot_2d(point.key, (qx, qy))
        if envelope.is_breakpoint(slope):
            return self._scan_maximizers((qx, qy), target_score=score)
        return HardmaxResult(
            score=_normalize_number(score),
            value=_restore_value(point.average_value, self._scalar_mode),
            maximizer_indices=point.entry_indices,
        )
```

Reason this matters: this is the exact accelerated retrieval story, and the
value question is basically about whether this kind of route can ever beat
simpler baselines under a meaningful contract.

### 3. Append-only execution-trace contract

File: `src/exec_trace/dsl.py`

```python
class Opcode(StrEnum):
    PUSH_CONST = "push_const"
    ADD = "add"
    SUB = "sub"
    EQ = "eq"
    DUP = "dup"
    POP = "pop"
    LOAD = "load"
    STORE = "store"
    LOAD_AT = "load_at"
    STORE_AT = "store_at"
    JMP = "jmp"
    JZ = "jz"
    CALL = "call"
    RET = "ret"
    HALT = "halt"

@dataclass(frozen=True, slots=True)
class TraceEvent:
    step: int
    pc: int
    opcode: Opcode
    arg: int | None
    popped: tuple[int, ...]
    pushed: tuple[int, ...]
    branch_taken: bool | None
    memory_read_address: int | None
    memory_read_value: int | None
    memory_write: tuple[int, int] | None
    next_pc: int
    stack_depth_before: int
    stack_depth_after: int
    halted: bool
```

Reason this matters: the scientific claim is not generic "program execution";
it is specifically that enough state can be exposed through append-only trace
events like these.

### 4. Reference trace interpreter

File: `src/exec_trace/interpreter.py`

```python
class TraceInterpreter:
    def run(self, program: Program, max_steps: int = 10_000) -> ExecutionResult:
        state = ExecutionState()
        events: list[TraceEvent] = []
        while not state.halted:
            instruction = program.instructions[state.pc]
            event, state = self._step(state, instruction)
            events.append(event)
        return ExecutionResult(program=program, events=tuple(events), final_state=state)

    def _step(self, state: ExecutionState, instruction: Instruction):
        ...
        match instruction.opcode:
            case Opcode.LOAD:
                memory_read_address = instruction.arg
                memory_read_value = memory.get(instruction.arg, 0)
                pushed = (memory_read_value,)
                stack.append(memory_read_value)
            case Opcode.STORE:
                value = stack.pop()
                popped = (value,)
                memory[instruction.arg] = value
                memory_write = (instruction.arg, value)
            case Opcode.CALL:
                call_stack.append(state.pc + 1)
                branch_taken = True
                next_pc = instruction.arg
            case Opcode.RET:
                branch_taken = True
                next_pc = call_stack.pop()
        ...
        event = TraceEvent(
            step=state.steps,
            pc=state.pc,
            opcode=instruction.opcode,
            arg=instruction.arg,
            popped=popped,
            pushed=pushed,
            branch_taken=branch_taken,
            memory_read_address=memory_read_address,
            memory_read_value=memory_read_value,
            memory_write=memory_write,
            next_pc=next_pc,
            ...
        )
```

Reason this matters: this is the reference semantics that later retrieval-based
decode and exact-execution claims are supposed to match.

### 5. Latest-write decode layer

File: `src/model/exact_hardmax.py`

```python
@dataclass(frozen=True, slots=True)
class LatestWriteDecodeConfig:
    max_steps: int
    addresses: tuple[int, ...]
    default_value: int = 0
    @property
    def epsilon(self) -> Fraction:
        return Fraction(1, self.max_steps + 2)

def encode_latest_write_key(address: int, step: int, epsilon: Fraction):
    return (address, Fraction(-(address**2)) + (epsilon * step))

def encode_latest_write_query(address: int):
    return (2 * address, 1)

def extract_memory_operations(events):
    operations = []
    for event in events:
        if event.memory_write is not None:
            address, value = event.memory_write
            operations.append(MemoryOperation(step=event.step, kind="store", address=address, value=value))
        if event.memory_read_address is not None:
            operations.append(
                MemoryOperation(
                    step=event.step,
                    kind="load",
                    address=event.memory_read_address,
                    value=event.memory_read_value,
                )
            )
    return tuple(operations)

def run_latest_write_decode(operations, config: LatestWriteDecodeConfig) -> DecodeRun:
    linear_keys = []
    linear_values = []
    accelerated = HullKVCache()
    ...
    for address in config.addresses:
        key = encode_latest_write_key(address, seed_step, config.epsilon)
        linear_keys.append(key)
        linear_values.append(config.default_value)
        accelerated.insert(key, config.default_value)
    for operation in operations:
        if operation.kind == "store":
            key = encode_latest_write_key(operation.address, operation.step, config.epsilon)
            linear_keys.append(key)
            linear_values.append(operation.value)
            accelerated.insert(key, operation.value)
            continue
        query = encode_latest_write_query(operation.address)
        linear_result = brute_force_hardmax_2d(linear_keys, linear_values, query)
        accelerated_result = accelerated.query(query)
        ...
```

Reason this matters: this is the central causal rewrite from program-state
reads into exact hard-max retrieval.

### 6. Lowered bytecode interpreter

File: `src/bytecode/interpreter.py`

```python
class BytecodeInterpreter:
    def run(self, program: BytecodeProgram, max_steps: int = 10_000) -> ExecutionResult:
        state = ExecutionState()
        events: list[TraceEvent] = []
        while not state.halted:
            instruction = program.instructions[state.pc]
            event, state = self._step(state, instruction)
            events.append(event)
        return ExecutionResult(program=program, events=tuple(events), final_state=state)

    def _step(self, state: ExecutionState, instruction: BytecodeInstruction):
        ...
        match instruction.opcode:
            case BytecodeOpcode.LOAD_STATIC:
                memory_read_address = instruction.arg
                memory_read_value = memory.get(instruction.arg, 0)
                pushed = (memory_read_value,)
                stack.append(memory_read_value)
            case BytecodeOpcode.STORE_STATIC:
                value = stack.pop()
                popped = (value,)
                memory[instruction.arg] = value
                memory_write = (instruction.arg, value)
            case BytecodeOpcode.LOAD_INDIRECT:
                address = stack.pop()
                popped = (address,)
                memory_read_address = address
                memory_read_value = memory.get(address, 0)
                pushed = (memory_read_value,)
                stack.append(memory_read_value)
            case BytecodeOpcode.CALL:
                call_stack.append(state.pc + 1)
                branch_taken = True
                next_pc = instruction.arg
            case BytecodeOpcode.RET:
                branch_taken = True
                next_pc = call_stack.pop()
        event = TraceEvent(opcode=LOWERING_MAP[instruction.opcode], ...)
```

Reason this matters: it shows how the higher-level lowered execution path still
funnels back into the same `TraceEvent` substrate.

## Single Long-Form Inquiry For GPTPro

Please answer the following as one integrated analysis, not as separate short
replies.

We have achieved a real narrow positive result: append-only trace execution,
exact `2D` hard-max retrieval, and bounded useful-case execution survive on a
carefully scoped substrate, with `H43` as the strongest positive endpoint.
But we now also have a strong negative result: after mechanism-first, compiled
useful-kernel, and finally native useful-kernel follow-ups, bounded
executor/system value remains disconfirmed, culminating in `R62` where exact
native execution stayed exact on `4/4` declared cases across `2/2` kernels yet
accelerated execution beat native linear on `0/2` longest rows and stayed out
of the external scalar comparator's order regime on `0/2` kernels.

Given that state:

1. Is our interpretation of the original Percepta scientific target correct,
   namely "narrow append-only retrieval-backed executor" rather than broad
   "LLMs are computers"?
2. Is the current executor-value lane scientifically closed enough that we
   should stop rather than spend more resources on same-lane variants?
3. If there is still one credible future route, what exact materially
   different cost structure would you nominate, and why is it not just the
   current lane in new clothes?
4. What concrete stop rules should be written before running that route?
5. If no route is credible, how would you phrase the strongest honest
   reproduction/partial-falsification claim we have already earned?

Please be explicit about whether you recommend:

- stop the project;
- keep only paper/archive consolidation work;
- or authorize exactly one new planning-to-execution route with strict stop
  rules.
