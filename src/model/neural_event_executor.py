"""Neural event-level executor over structured transition labels."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Sequence

from exec_trace import Program, TraceInterpreter
from exec_trace.dsl import Opcode
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadObservation,
)
from model.induced_causal import (
    _ADDRESS_EXPR_CANDIDATES,
    _BOOL_EXPR_CANDIDATES,
    _NEXT_PC_CANDIDATES,
    _SCALAR_EXPR_CANDIDATES,
    _eval_address_expr,
    _eval_bool_expr,
    _eval_next_pc,
    _eval_scalar_expr,
    _expected_popped,
    build_transition_examples,
    fit_transition_library,
    InducedTransitionLibrary,
)
from model.factorized_event_models import MODELED_EVENT_OPCODES

try:  # pragma: no cover - exercised only when torch is installed
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - exercised in environments without torch
    torch = None
    nn = None
    F = None


_NONE = "<none>"
_MAX_STACK_READS = 2
_MAX_PUSHES = 2


@dataclass(frozen=True, slots=True)
class StructuredEventContext:
    program_name: str
    step: int
    pc: int
    opcode: Opcode
    arg: int | None
    stack_depth: int
    top_values: tuple[int | None, int | None]


@dataclass(frozen=True, slots=True)
class StructuredEventLabel:
    stack_read_count: int
    pop_count: int
    push_count: int
    push_exprs: tuple[str, str]
    branch_expr: str
    memory_read_address_expr: str
    memory_write_address_expr: str
    memory_write_value_expr: str
    next_pc_mode: str
    halted: bool


@dataclass(frozen=True, slots=True)
class StructuredEventExample:
    context: StructuredEventContext
    label: StructuredEventLabel


@dataclass(frozen=True, slots=True)
class StructuredEventMetrics:
    loss: float
    exact_label_accuracy: float
    example_count: int
    head_accuracies: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class NeuralEventTrainingConfig:
    epochs: int = 40
    batch_size: int = 16
    learning_rate: float = 5e-3
    weight_decay: float = 0.0
    seed: int = 0
    max_grad_norm: float | None = 1.0
    embedding_dim: int = 16
    hidden_dim: int = 64
    device: str | None = None


@dataclass(frozen=True, slots=True)
class NeuralEventEpochStats:
    epoch: int
    train_loss: float
    eval_loss: float | None


@dataclass(slots=True)
class NeuralEventTrainingRun:
    model: "StructuredEventTransitionModel"
    codec: "StructuredEventCodec"
    train_metrics: StructuredEventMetrics
    eval_metrics: StructuredEventMetrics | None
    history: tuple[NeuralEventEpochStats, ...]
    device: str
    library: InducedTransitionLibrary


class StructuredEventCodec:
    """Encode structured event contexts and labels for neural rule decoding."""

    def __init__(self) -> None:
        self.opcodes = MODELED_EVENT_OPCODES
        self._opcode_to_id = {opcode: index for index, opcode in enumerate(self.opcodes)}
        self._head_spaces: dict[str, tuple[object, ...]] = {
            "stack_read_count": (0, 1, 2),
            "pop_count": (0, 1, 2),
            "push_count": (0, 1, 2),
            "push_expr_0": (_NONE, *_SCALAR_EXPR_CANDIDATES),
            "push_expr_1": (_NONE, *_SCALAR_EXPR_CANDIDATES),
            "branch_expr": (_NONE, *_BOOL_EXPR_CANDIDATES),
            "memory_read_address_expr": (_NONE, *_ADDRESS_EXPR_CANDIDATES),
            "memory_write_address_expr": (_NONE, *_ADDRESS_EXPR_CANDIDATES),
            "memory_write_value_expr": (_NONE, *_SCALAR_EXPR_CANDIDATES),
            "next_pc_mode": tuple(_NEXT_PC_CANDIDATES),
            "halted": (False, True),
        }
        self._head_indices = {
            name: {value: index for index, value in enumerate(space)}
            for name, space in self._head_spaces.items()
        }

    @property
    def head_names(self) -> tuple[str, ...]:
        return tuple(self._head_spaces)

    def head_size(self, name: str) -> int:
        return len(self._head_spaces[name])

    def label_from_rule(self, rule) -> StructuredEventLabel:
        push_exprs = list(rule.push_exprs)
        if len(push_exprs) > _MAX_PUSHES:
            raise ValueError("Current neural event executor only supports up to two pushes per event.")
        push_exprs.extend([_NONE] * (_MAX_PUSHES - len(push_exprs)))
        return StructuredEventLabel(
            stack_read_count=rule.stack_read_count,
            pop_count=rule.pop_count,
            push_count=len(rule.push_exprs),
            push_exprs=(push_exprs[0], push_exprs[1]),
            branch_expr=_NONE if rule.branch_expr is None else rule.branch_expr,
            memory_read_address_expr=_NONE
            if rule.memory_read_address_expr is None
            else rule.memory_read_address_expr,
            memory_write_address_expr=_NONE
            if rule.memory_write_address_expr is None
            else rule.memory_write_address_expr,
            memory_write_value_expr=_NONE
            if rule.memory_write_value_expr is None
            else rule.memory_write_value_expr,
            next_pc_mode=rule.next_pc_mode,
            halted=rule.halted,
        )

    def context_from_transition(self, example) -> StructuredEventContext:
        top_values = self._top_values(example.stack_before)
        return StructuredEventContext(
            program_name=example.program_name,
            step=example.step,
            pc=example.pc,
            opcode=example.opcode,
            arg=example.arg,
            stack_depth=len(example.stack_before),
            top_values=top_values,
        )

    def build_examples(
        self,
        programs: Iterable[Program],
        *,
        library: InducedTransitionLibrary | None = None,
        interpreter: TraceInterpreter | None = None,
    ) -> tuple[StructuredEventExample, ...]:
        interpreter = interpreter or TraceInterpreter()
        library = library or fit_transition_library(programs, interpreter=interpreter)
        transition_examples = build_transition_examples(programs, interpreter=interpreter)
        return tuple(
            StructuredEventExample(
                context=self.context_from_transition(example),
                label=self.label_from_rule(library.rule_for(example.opcode)),
            )
            for example in transition_examples
        )

    def encode_batch(self, examples: Sequence[StructuredEventExample], *, device: str):
        require_torch()
        opcode_ids = torch.tensor(
            [self._opcode_to_id[example.context.opcode] for example in examples],
            dtype=torch.long,
            device=device,
        )
        numeric_features = torch.tensor(
            [self.context_features(example.context) for example in examples],
            dtype=torch.float32,
            device=device,
        )
        labels = {
            head: torch.tensor(
                [self.label_index(head, self._label_value(example.label, head)) for example in examples],
                dtype=torch.long,
                device=device,
            )
            for head in self.head_names
        }
        return (opcode_ids, numeric_features, labels)

    def encode_context(self, context: StructuredEventContext, *, device: str):
        require_torch()
        opcode_id = torch.tensor([self._opcode_to_id[context.opcode]], dtype=torch.long, device=device)
        numeric_features = torch.tensor([self.context_features(context)], dtype=torch.float32, device=device)
        return (opcode_id, numeric_features)

    def context_features(self, context: StructuredEventContext) -> tuple[float, ...]:
        second_top, top = context.top_values
        return (
            0.0 if context.arg is None else float(context.arg),
            0.0 if context.arg is None else 1.0,
            float(context.stack_depth),
            0.0 if second_top is None else float(second_top),
            0.0 if second_top is None else 1.0,
            0.0 if top is None else float(top),
            0.0 if top is None else 1.0,
        )

    def label_index(self, head: str, value: object) -> int:
        return self._head_indices[head][value]

    def label_value(self, head: str, index: int) -> object:
        return self._head_spaces[head][index]

    def decode_argmax(self, head: str, logits: "torch.Tensor", *, allowed: Sequence[object] | None = None) -> object:
        allowed_values = tuple(self._head_spaces[head] if allowed is None else allowed)
        allowed_indices = [self.label_index(head, value) for value in allowed_values]
        best_index = max(allowed_indices, key=lambda idx: float(logits[idx].item()))
        return self.label_value(head, best_index)

    def _label_value(self, label: StructuredEventLabel, head: str) -> object:
        match head:
            case "stack_read_count":
                return label.stack_read_count
            case "pop_count":
                return label.pop_count
            case "push_count":
                return label.push_count
            case "push_expr_0":
                return label.push_exprs[0]
            case "push_expr_1":
                return label.push_exprs[1]
            case "branch_expr":
                return label.branch_expr
            case "memory_read_address_expr":
                return label.memory_read_address_expr
            case "memory_write_address_expr":
                return label.memory_write_address_expr
            case "memory_write_value_expr":
                return label.memory_write_value_expr
            case "next_pc_mode":
                return label.next_pc_mode
            case "halted":
                return label.halted
            case _:
                raise KeyError(f"Unknown structured-event head: {head}")

    @staticmethod
    def _top_values(stack_before: Sequence[int]) -> tuple[int | None, int | None]:
        if not stack_before:
            return (None, None)
        if len(stack_before) == 1:
            return (None, stack_before[-1])
        return (stack_before[-2], stack_before[-1])


def require_torch() -> None:
    if torch is None:
        raise RuntimeError(
            "PyTorch is not installed. Install it explicitly before running the neural event executor."
        )


def default_neural_device(preferred: str | None = None) -> str:
    require_torch()
    if preferred is not None:
        return preferred
    return "cuda" if torch.cuda.is_available() else "cpu"


if torch is not None:  # pragma: no branch

    class StructuredEventTransitionModel(nn.Module):
        def __init__(self, codec: StructuredEventCodec, *, embedding_dim: int = 16, hidden_dim: int = 64) -> None:
            super().__init__()
            self.codec = codec
            self.opcode_embedding = nn.Embedding(len(codec.opcodes), embedding_dim)
            self.backbone = nn.Sequential(
                nn.Linear(embedding_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
            )
            self.heads = nn.ModuleDict(
                {
                    head: nn.Linear(hidden_dim, codec.head_size(head))
                    for head in codec.head_names
                }
            )

        def forward(self, opcode_ids: "torch.Tensor", numeric_features: "torch.Tensor") -> dict[str, "torch.Tensor"]:
            del numeric_features
            hidden = self.opcode_embedding(opcode_ids)
            hidden = self.backbone(hidden)
            return {name: head(hidden) for name, head in self.heads.items()}

else:

    class StructuredEventTransitionModel:  # pragma: no cover - exercised only without torch
        def __init__(self, codec: StructuredEventCodec, *, embedding_dim: int = 16, hidden_dim: int = 64) -> None:
            require_torch()


def _batch_examples(
    examples: Sequence[StructuredEventExample],
    *,
    batch_size: int,
    rng: random.Random | None = None,
) -> list[list[StructuredEventExample]]:
    ordered = list(examples)
    if rng is not None:
        rng.shuffle(ordered)
    return [ordered[index : index + batch_size] for index in range(0, len(ordered), batch_size)]


def _compute_loss(logits: dict[str, "torch.Tensor"], labels: dict[str, "torch.Tensor"]) -> "torch.Tensor":
    return sum(F.cross_entropy(logits[head], labels[head]) for head in logits)


def evaluate_structured_event_model(
    model: "StructuredEventTransitionModel",
    codec: StructuredEventCodec,
    examples: Sequence[StructuredEventExample],
    *,
    device: str | None = None,
) -> StructuredEventMetrics:
    require_torch()
    if not examples:
        return StructuredEventMetrics(loss=0.0, exact_label_accuracy=0.0, example_count=0, head_accuracies=())

    device = default_neural_device(device)
    model.eval()
    opcode_ids, numeric_features, labels = codec.encode_batch(examples, device=device)

    with torch.no_grad():
        logits = model(opcode_ids, numeric_features)
        loss = float(_compute_loss(logits, labels).item())

    exact = 0
    head_correct: dict[str, int] = {head: 0 for head in codec.head_names}
    for row_index in range(len(examples)):
        row_exact = True
        for head in codec.head_names:
            prediction = int(logits[head][row_index].argmax().item())
            target = int(labels[head][row_index].item())
            correct = prediction == target
            head_correct[head] += int(correct)
            row_exact = row_exact and correct
        exact += int(row_exact)

    return StructuredEventMetrics(
        loss=loss,
        exact_label_accuracy=exact / len(examples),
        example_count=len(examples),
        head_accuracies=tuple(
            (head, head_correct[head] / len(examples))
            for head in codec.head_names
        ),
    )


def train_neural_event_executor(
    train_programs: Sequence[Program],
    *,
    eval_programs: Sequence[Program] = (),
    training_config: NeuralEventTrainingConfig | None = None,
    interpreter: TraceInterpreter | None = None,
) -> NeuralEventTrainingRun:
    require_torch()
    training_config = training_config or NeuralEventTrainingConfig()
    device = default_neural_device(training_config.device)
    torch.manual_seed(training_config.seed)
    random.seed(training_config.seed)

    interpreter = interpreter or TraceInterpreter()
    codec = StructuredEventCodec()
    library = fit_transition_library(train_programs, interpreter=interpreter)
    train_examples = codec.build_examples(train_programs, library=library, interpreter=interpreter)
    eval_examples = codec.build_examples(eval_programs, library=library, interpreter=interpreter) if eval_programs else ()

    model = StructuredEventTransitionModel(
        codec,
        embedding_dim=training_config.embedding_dim,
        hidden_dim=training_config.hidden_dim,
    ).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=training_config.learning_rate,
        weight_decay=training_config.weight_decay,
    )

    history: list[NeuralEventEpochStats] = []
    for epoch in range(1, training_config.epochs + 1):
        model.train()
        epoch_losses: list[float] = []
        batches = _batch_examples(
            train_examples,
            batch_size=training_config.batch_size,
            rng=random.Random(training_config.seed + epoch),
        )
        for batch in batches:
            opcode_ids, numeric_features, labels = codec.encode_batch(batch, device=device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(opcode_ids, numeric_features)
            loss = _compute_loss(logits, labels)
            loss.backward()
            if training_config.max_grad_norm is not None:
                torch.nn.utils.clip_grad_norm_(model.parameters(), training_config.max_grad_norm)
            optimizer.step()
            epoch_losses.append(float(loss.item()))

        eval_metrics = (
            evaluate_structured_event_model(model, codec, eval_examples, device=device)
            if eval_examples
            else None
        )
        history.append(
            NeuralEventEpochStats(
                epoch=epoch,
                train_loss=sum(epoch_losses) / len(epoch_losses),
                eval_loss=None if eval_metrics is None else eval_metrics.loss,
            )
        )

    train_metrics = evaluate_structured_event_model(model, codec, train_examples, device=device)
    eval_metrics = (
        evaluate_structured_event_model(model, codec, eval_examples, device=device)
        if eval_examples
        else None
    )
    return NeuralEventTrainingRun(
        model=model,
        codec=codec,
        train_metrics=train_metrics,
        eval_metrics=eval_metrics,
        history=tuple(history),
        device=device,
        library=library,
    )


class NeuralEventExecutor(FreeRunningTraceExecutor):
    """Run online execution using a neural decoder over structured event labels."""

    def __init__(
        self,
        model: "StructuredEventTransitionModel",
        codec: StructuredEventCodec,
        *,
        device: str | None = None,
        stack_strategy: str = "accelerated",
        memory_strategy: str = "accelerated",
        default_memory_value: int = 0,
        validate_exact_reads: bool = True,
    ) -> None:
        if stack_strategy == "trainable":
            raise ValueError("NeuralEventExecutor only supports exact stack retrieval strategies.")
        super().__init__(
            stack_strategy=stack_strategy,
            memory_strategy=memory_strategy,
            default_memory_value=default_memory_value,
            validate_exact_reads=validate_exact_reads,
        )
        require_torch()
        self.model = model
        self.codec = codec
        self.device = default_neural_device(device)
        self.model.to(self.device)
        self.model.eval()

    def rollout(self, program: Program, *, max_steps: int = 10_000) -> FreeRunningExecutionResult:
        return self.run(program, max_steps=max_steps)

    def _execute_instruction(
        self,
        *,
        step: int,
        pc: int,
        stack_depth: int,
        call_stack: list[int],
        instruction: Opcode,
        arg: int | None,
        stack_history,
        memory_history,
        read_observations: list[ReadObservation],
    ):
        if instruction in {Opcode.CALL, Opcode.RET}:
            return super()._execute_instruction(
                step=step,
                pc=pc,
                stack_depth=stack_depth,
                call_stack=call_stack,
                instruction=instruction,
                arg=arg,
                stack_history=stack_history,
                memory_history=memory_history,
                read_observations=read_observations,
            )
        context = StructuredEventContext(
            program_name="runtime",
            step=step,
            pc=pc,
            opcode=instruction,
            arg=arg,
            stack_depth=stack_depth,
            top_values=self._peek_stack_values(stack_depth, stack_history),
        )
        label = self._predict_label(context)
        reads = (
            ()
            if label.stack_read_count == 0
            else self._read_stack_suffix(
                step=step,
                count=label.stack_read_count,
                stack_depth=stack_depth,
                stack_history=stack_history,
                read_observations=read_observations,
            )
        )
        popped = _expected_popped(reads, label.pop_count)

        memory_read = None
        memory_read_value = None
        if label.memory_read_address_expr != _NONE:
            address = _eval_address_expr(label.memory_read_address_expr, arg=arg, reads=reads)
            if address < 0:
                raise RuntimeError("Neural event executor produced a negative memory-read address.")
            memory_read_value = self._read_memory(
                step=step,
                address=address,
                memory_history=memory_history,
                read_observations=read_observations,
            )
            memory_read = (address, memory_read_value)

        pushed = tuple(
            _eval_scalar_expr(expr, arg=arg, reads=reads, memory_read_value=memory_read_value)
            for expr in label.push_exprs[: label.push_count]
        )

        branch_taken = None
        if label.branch_expr != _NONE:
            branch_taken = _eval_bool_expr(label.branch_expr, reads=reads)

        memory_write = None
        if label.memory_write_address_expr != _NONE:
            address = _eval_address_expr(label.memory_write_address_expr, arg=arg, reads=reads)
            if address < 0:
                raise RuntimeError("Neural event executor produced a negative memory-write address.")
            value = _eval_scalar_expr(
                label.memory_write_value_expr,
                arg=arg,
                reads=reads,
                memory_read_value=memory_read_value,
            )
            memory_write = (address, value)

        next_pc = _eval_next_pc(label.next_pc_mode, pc=pc, arg=arg, branch_taken=branch_taken)
        return (popped, pushed, branch_taken, memory_read, memory_write, next_pc, label.halted)

    def _peek_stack_values(self, stack_depth: int, stack_history) -> tuple[int | None, int | None]:
        second_top = None
        top = None
        if stack_depth >= 2:
            second_top = stack_history.read_exact(stack_depth - 2)[1]
        if stack_depth >= 1:
            top = stack_history.read_exact(stack_depth - 1)[1]
        return (second_top, top)

    def _predict_label(self, context: StructuredEventContext) -> StructuredEventLabel:
        opcode_ids, numeric_features = self.codec.encode_context(context, device=self.device)
        with torch.no_grad():
            logits = self.model(opcode_ids, numeric_features)
        row_logits = {head: logits[head][0] for head in self.codec.head_names}

        has_arg = context.arg is not None
        max_read_count = min(_MAX_STACK_READS, context.stack_depth)
        stack_read_count = int(
            self.codec.decode_argmax(
                "stack_read_count",
                row_logits["stack_read_count"],
                allowed=tuple(range(0, max_read_count + 1)),
            )
        )
        pop_count = int(
            self.codec.decode_argmax(
                "pop_count",
                row_logits["pop_count"],
                allowed=tuple(range(0, stack_read_count + 1)),
            )
        )
        push_count = int(
            self.codec.decode_argmax(
                "push_count",
                row_logits["push_count"],
                allowed=(0, 1, 2),
            )
        )

        memory_read_address_expr = str(
            self.codec.decode_argmax(
                "memory_read_address_expr",
                row_logits["memory_read_address_expr"],
                allowed=_allowed_address_exprs(stack_read_count, has_arg, allow_none=True),
            )
        )
        has_memory_read = memory_read_address_expr != _NONE

        branch_expr = str(
            self.codec.decode_argmax(
                "branch_expr",
                row_logits["branch_expr"],
                allowed=_allowed_bool_exprs(stack_read_count, allow_none=True),
            )
        )
        branch_available = branch_expr != _NONE

        push_exprs: list[str] = []
        for slot in range(_MAX_PUSHES):
            if slot >= push_count:
                push_exprs.append(_NONE)
                continue
            push_exprs.append(
                str(
                    self.codec.decode_argmax(
                        f"push_expr_{slot}",
                        row_logits[f"push_expr_{slot}"],
                        allowed=_allowed_scalar_exprs(
                            stack_read_count,
                            has_arg,
                            has_memory_read,
                            allow_none=False,
                        ),
                    )
                )
            )

        memory_write_address_expr = str(
            self.codec.decode_argmax(
                "memory_write_address_expr",
                row_logits["memory_write_address_expr"],
                allowed=_allowed_address_exprs(stack_read_count, has_arg, allow_none=True),
            )
        )
        if memory_write_address_expr == _NONE:
            memory_write_value_expr = _NONE
        else:
            memory_write_value_expr = str(
                self.codec.decode_argmax(
                    "memory_write_value_expr",
                    row_logits["memory_write_value_expr"],
                    allowed=_allowed_scalar_exprs(
                        stack_read_count,
                        has_arg,
                        has_memory_read,
                        allow_none=False,
                    ),
                )
            )

        next_pc_mode = str(
            self.codec.decode_argmax(
                "next_pc_mode",
                row_logits["next_pc_mode"],
                allowed=_allowed_next_pc_modes(has_arg, branch_available),
            )
        )
        halted = bool(self.codec.decode_argmax("halted", row_logits["halted"]))

        return StructuredEventLabel(
            stack_read_count=stack_read_count,
            pop_count=pop_count,
            push_count=push_count,
            push_exprs=(push_exprs[0], push_exprs[1]),
            branch_expr=branch_expr,
            memory_read_address_expr=memory_read_address_expr,
            memory_write_address_expr=memory_write_address_expr,
            memory_write_value_expr=memory_write_value_expr,
            next_pc_mode=next_pc_mode,
            halted=halted,
        )


def run_free_running_with_neural_executor(
    program: Program,
    fit: NeuralEventTrainingRun,
    *,
    decode_mode: str = "accelerated",
    max_steps: int = 10_000,
) -> FreeRunningExecutionResult:
    executor = NeuralEventExecutor(
        fit.model,
        fit.codec,
        device=fit.device,
        stack_strategy=decode_mode,
        memory_strategy=decode_mode,
    )
    return executor.rollout(program, max_steps=max_steps)


def _allowed_scalar_exprs(
    read_count: int,
    has_arg: bool,
    has_memory_read: bool,
    *,
    allow_none: bool,
) -> tuple[object, ...]:
    values: list[object] = [_NONE] if allow_none else []
    for expr in _SCALAR_EXPR_CANDIDATES:
        if expr == "const_arg" and not has_arg:
            continue
        if expr == "read0" and read_count < 1:
            continue
        if expr in {"read1", "add", "sub", "eq"} and read_count < 2:
            continue
        if expr == "memory_read_value" and not has_memory_read:
            continue
        values.append(expr)
    return tuple(values)


def _allowed_address_exprs(read_count: int, has_arg: bool, *, allow_none: bool) -> tuple[object, ...]:
    values: list[object] = [_NONE] if allow_none else []
    for expr in _ADDRESS_EXPR_CANDIDATES:
        if expr == "const_arg" and not has_arg:
            continue
        if expr == "read0" and read_count < 1:
            continue
        if expr == "read1" and read_count < 2:
            continue
        values.append(expr)
    return tuple(values)


def _allowed_bool_exprs(read_count: int, *, allow_none: bool) -> tuple[object, ...]:
    values: list[object] = [_NONE] if allow_none else []
    for expr in _BOOL_EXPR_CANDIDATES:
        if expr == "read0_is_zero" and read_count < 1:
            continue
        if expr == "read0_eq_read1" and read_count < 2:
            continue
        values.append(expr)
    return tuple(values)


def _allowed_next_pc_modes(has_arg: bool, branch_available: bool) -> tuple[str, ...]:
    values: list[str] = []
    for mode in _NEXT_PC_CANDIDATES:
        if mode == "const_arg" and not has_arg:
            continue
        if mode == "branch_arg_else_seq" and (not has_arg or not branch_available):
            continue
        values.append(mode)
    return tuple(values)
