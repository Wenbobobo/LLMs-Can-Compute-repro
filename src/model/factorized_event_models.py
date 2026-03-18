"""Shared event-level models for richer M4 decoding and the final M5 baseline."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Sequence

from exec_trace import Program, TraceEvent, TraceInterpreter
from exec_trace.dsl import Opcode
from model.free_running_executor import (
    FreeRunningExecutionResult,
    FreeRunningTraceExecutor,
    ReadObservation,
)

try:  # pragma: no cover - exercised only when torch is installed
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - exercised in environments without torch
    torch = None
    nn = None
    F = None


_HISTORY_PAD = 0
_NONE_BRANCH = -1
_MAX_STACK_READS = 2
_MAX_PUSHES = 2
MODELED_EVENT_OPCODES = tuple(opcode for opcode in Opcode if opcode not in {Opcode.CALL, Opcode.RET})


@dataclass(frozen=True, slots=True)
class HistoryEventSummary:
    opcode: Opcode
    pop_count: int
    push_count: int
    push_values: tuple[int | None, int | None]
    branch_state: int
    memory_read_address: int | None
    memory_write_address: int | None
    memory_write_value: int | None
    next_pc: int
    halted: bool
    stack_depth_after: int


@dataclass(frozen=True, slots=True)
class FactorizedEventContext:
    program_name: str
    step: int
    pc: int
    opcode: Opcode
    arg: int | None
    stack_depth: int
    top_values: tuple[int | None, int | None]
    recent_history: tuple[HistoryEventSummary, ...]


@dataclass(frozen=True, slots=True)
class FactorizedEventLabel:
    stack_read_count: int
    pop_count: int
    push_count: int
    push_values: tuple[int | None, int | None]
    branch_state: int
    memory_read_address: int | None
    memory_write_address: int | None
    memory_write_value: int | None
    next_pc: int
    halted: bool


@dataclass(frozen=True, slots=True)
class FactorizedEventExample:
    context: FactorizedEventContext
    label: FactorizedEventLabel


@dataclass(frozen=True, slots=True)
class FactorizedEventMetrics:
    loss: float
    exact_label_accuracy: float
    example_count: int
    head_accuracies: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class FactorizedEventModelConfig:
    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    d_ffn: int = 128
    opcode_dim: int = 16
    history_window: int = 16
    max_scalar: int = 128
    max_address: int = 64
    max_pc: int = 64
    include_top_values: bool = True


@dataclass(frozen=True, slots=True)
class FactorizedEventTrainingConfig:
    epochs: int = 32
    batch_size: int = 16
    learning_rate: float = 5e-3
    weight_decay: float = 0.0
    seed: int = 0
    max_grad_norm: float | None = 1.0
    device: str | None = None


@dataclass(frozen=True, slots=True)
class FactorizedEventEpochStats:
    epoch: int
    train_loss: float
    eval_loss: float | None


@dataclass(slots=True)
class FactorizedEventTrainingRun:
    model: "FactorizedEventTransformer"
    codec: "FactorizedEventCodec"
    train_metrics: FactorizedEventMetrics
    eval_metrics: FactorizedEventMetrics | None
    history: tuple[FactorizedEventEpochStats, ...]
    device: str
    variant: str


class FactorizedEventCodec:
    """Encode structured event histories and direct event-value labels."""

    def __init__(self, config: FactorizedEventModelConfig) -> None:
        self.config = config
        self.opcodes = MODELED_EVENT_OPCODES
        self._opcode_to_id = {opcode: index + 1 for index, opcode in enumerate(self.opcodes)}
        scalar_space = tuple(range(-config.max_scalar, config.max_scalar + 1))
        address_space = tuple(range(0, config.max_address + 1))
        pc_space = tuple(range(0, config.max_pc + 1))
        self._head_spaces: dict[str, tuple[object, ...]] = {
            "stack_read_count": (0, 1, 2),
            "pop_count": (0, 1, 2),
            "push_count": (0, 1, 2),
            "push_value_0": (None, *scalar_space),
            "push_value_1": (None, *scalar_space),
            "branch_state": (_NONE_BRANCH, 0, 1),
            "memory_read_address": (None, *address_space),
            "memory_write_address": (None, *address_space),
            "memory_write_value": (None, *scalar_space),
            "next_pc": pc_space,
            "halted": (False, True),
        }
        self._head_indices = {
            name: {value: index for index, value in enumerate(space)}
            for name, space in self._head_spaces.items()
        }

    @property
    def head_names(self) -> tuple[str, ...]:
        return tuple(self._head_spaces)

    @property
    def current_feature_dim(self) -> int:
        return 9

    @property
    def history_feature_dim(self) -> int:
        return 14

    def opcode_id(self, opcode: Opcode | None) -> int:
        if opcode is None:
            return _HISTORY_PAD
        return self._opcode_to_id[opcode]

    def head_size(self, name: str) -> int:
        return len(self._head_spaces[name])

    def label_index(self, head: str, value: object) -> int:
        return self._head_indices[head][value]

    def label_value(self, head: str, index: int) -> object:
        return self._head_spaces[head][index]

    def decode_argmax(self, head: str, logits: "torch.Tensor", *, allowed: Sequence[object] | None = None) -> object:
        allowed_values = tuple(self._head_spaces[head] if allowed is None else allowed)
        if not allowed_values:
            raise ValueError(f"No allowed values provided for head {head!r}.")
        allowed_indices = [self.label_index(head, value) for value in allowed_values]
        best_index = max(allowed_indices, key=lambda idx: float(logits[idx].item()))
        return self.label_value(head, best_index)

    def build_examples(
        self,
        programs: Iterable[Program],
        *,
        interpreter: TraceInterpreter | None = None,
    ) -> tuple[FactorizedEventExample, ...]:
        interpreter = interpreter or TraceInterpreter()
        examples: list[FactorizedEventExample] = []

        for program in programs:
            result = interpreter.run(program)
            stack: list[int] = []
            history: list[HistoryEventSummary] = []

            for event in result.events:
                examples.append(
                    FactorizedEventExample(
                        context=FactorizedEventContext(
                            program_name=program.name,
                            step=event.step,
                            pc=event.pc,
                            opcode=event.opcode,
                            arg=event.arg,
                            stack_depth=len(stack),
                            top_values=self._top_values(stack),
                            recent_history=tuple(history[-self.config.history_window :]),
                        ),
                        label=self.label_from_event(event),
                    )
                )
                self._apply_event_to_stack(event, stack, program_name=program.name)
                history.append(self.summary_from_event(event))

        return tuple(examples)

    def label_from_event(self, event: TraceEvent) -> FactorizedEventLabel:
        pushed = list(event.pushed[:_MAX_PUSHES])
        pushed.extend([None] * (_MAX_PUSHES - len(pushed)))
        branch_state = _NONE_BRANCH if event.branch_taken is None else int(event.branch_taken)
        memory_write_address = None if event.memory_write is None else event.memory_write[0]
        memory_write_value = None if event.memory_write is None else event.memory_write[1]
        return FactorizedEventLabel(
            stack_read_count=_stack_read_count_for_opcode(event.opcode),
            pop_count=len(event.popped),
            push_count=len(event.pushed),
            push_values=(pushed[0], pushed[1]),
            branch_state=branch_state,
            memory_read_address=event.memory_read_address,
            memory_write_address=memory_write_address,
            memory_write_value=memory_write_value,
            next_pc=event.next_pc,
            halted=event.halted,
        )

    def summary_from_event(self, event: TraceEvent) -> HistoryEventSummary:
        pushed = list(event.pushed[:_MAX_PUSHES])
        pushed.extend([None] * (_MAX_PUSHES - len(pushed)))
        return HistoryEventSummary(
            opcode=event.opcode,
            pop_count=len(event.popped),
            push_count=len(event.pushed),
            push_values=(pushed[0], pushed[1]),
            branch_state=_NONE_BRANCH if event.branch_taken is None else int(event.branch_taken),
            memory_read_address=event.memory_read_address,
            memory_write_address=None if event.memory_write is None else event.memory_write[0],
            memory_write_value=None if event.memory_write is None else event.memory_write[1],
            next_pc=event.next_pc,
            halted=event.halted,
            stack_depth_after=event.stack_depth_after,
        )

    def encode_batch(
        self,
        examples: Sequence[FactorizedEventExample],
        *,
        device: str,
        include_top_values: bool | None = None,
    ) -> tuple["torch.Tensor", "torch.Tensor", "torch.Tensor", "torch.Tensor", "torch.Tensor", dict[str, "torch.Tensor"]]:
        require_torch()
        include_top_values = self.config.include_top_values if include_top_values is None else include_top_values
        current_opcodes = torch.tensor(
            [self.opcode_id(example.context.opcode) for example in examples],
            dtype=torch.long,
            device=device,
        )
        current_numeric = torch.tensor(
            [self.current_features(example.context, include_top_values=include_top_values) for example in examples],
            dtype=torch.float32,
            device=device,
        )
        history_opcodes = torch.tensor(
            [self._history_opcode_ids(example.context.recent_history) for example in examples],
            dtype=torch.long,
            device=device,
        )
        history_numeric = torch.tensor(
            [self._history_feature_rows(example.context.recent_history) for example in examples],
            dtype=torch.float32,
            device=device,
        )
        history_mask = torch.tensor(
            [self._history_padding_mask(example.context.recent_history) for example in examples],
            dtype=torch.bool,
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
        return (current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask, labels)

    def encode_context(
        self,
        context: FactorizedEventContext,
        *,
        device: str,
        include_top_values: bool | None = None,
    ) -> tuple["torch.Tensor", "torch.Tensor", "torch.Tensor", "torch.Tensor", "torch.Tensor"]:
        require_torch()
        include_top_values = self.config.include_top_values if include_top_values is None else include_top_values
        return (
            torch.tensor([self.opcode_id(context.opcode)], dtype=torch.long, device=device),
            torch.tensor(
                [self.current_features(context, include_top_values=include_top_values)],
                dtype=torch.float32,
                device=device,
            ),
            torch.tensor([self._history_opcode_ids(context.recent_history)], dtype=torch.long, device=device),
            torch.tensor([self._history_feature_rows(context.recent_history)], dtype=torch.float32, device=device),
            torch.tensor([self._history_padding_mask(context.recent_history)], dtype=torch.bool, device=device),
        )

    def current_features(
        self,
        context: FactorizedEventContext,
        *,
        include_top_values: bool,
    ) -> tuple[float, ...]:
        second_top, top = context.top_values if include_top_values else (None, None)
        return (
            float(context.step),
            float(context.pc),
            0.0 if context.arg is None else float(context.arg),
            0.0 if context.arg is None else 1.0,
            float(context.stack_depth),
            0.0 if second_top is None else float(second_top),
            0.0 if second_top is None else 1.0,
            0.0 if top is None else float(top),
            0.0 if top is None else 1.0,
        )

    def _history_opcode_ids(self, history: Sequence[HistoryEventSummary]) -> tuple[int, ...]:
        rows = [_HISTORY_PAD] * self.config.history_window
        offset = self.config.history_window - len(history)
        for index, summary in enumerate(history[-self.config.history_window :]):
            rows[offset + index] = self.opcode_id(summary.opcode)
        return tuple(rows)

    def _history_feature_rows(self, history: Sequence[HistoryEventSummary]) -> tuple[tuple[float, ...], ...]:
        pad_row = (0.0,) * self.history_feature_dim
        rows: list[tuple[float, ...]] = [pad_row] * self.config.history_window
        offset = self.config.history_window - len(history)
        for index, summary in enumerate(history[-self.config.history_window :]):
            rows[offset + index] = self.history_features(summary)
        return tuple(rows)

    def _history_padding_mask(self, history: Sequence[HistoryEventSummary]) -> tuple[bool, ...]:
        pad_count = self.config.history_window - len(history)
        return tuple([True] * pad_count + [False] * len(history))

    def history_features(self, summary: HistoryEventSummary) -> tuple[float, ...]:
        push0, push1 = summary.push_values
        return (
            float(summary.pop_count),
            float(summary.push_count),
            0.0 if push0 is None else float(push0),
            0.0 if push0 is None else 1.0,
            0.0 if push1 is None else float(push1),
            0.0 if push1 is None else 1.0,
            float(summary.branch_state),
            0.0 if summary.memory_read_address is None else float(summary.memory_read_address),
            0.0 if summary.memory_read_address is None else 1.0,
            0.0 if summary.memory_write_address is None else float(summary.memory_write_address),
            0.0 if summary.memory_write_address is None else 1.0,
            0.0 if summary.memory_write_value is None else float(summary.memory_write_value),
            0.0 if summary.memory_write_value is None else 1.0,
            float(summary.stack_depth_after),
        )

    def _label_value(self, label: FactorizedEventLabel, head: str) -> object:
        match head:
            case "stack_read_count":
                return label.stack_read_count
            case "pop_count":
                return label.pop_count
            case "push_count":
                return label.push_count
            case "push_value_0":
                return label.push_values[0]
            case "push_value_1":
                return label.push_values[1]
            case "branch_state":
                return label.branch_state
            case "memory_read_address":
                return label.memory_read_address
            case "memory_write_address":
                return label.memory_write_address
            case "memory_write_value":
                return label.memory_write_value
            case "next_pc":
                return label.next_pc
            case "halted":
                return label.halted
            case _:
                raise KeyError(f"Unknown factorized-event head: {head}")

    @staticmethod
    def _top_values(stack_before: Sequence[int]) -> tuple[int | None, int | None]:
        if not stack_before:
            return (None, None)
        if len(stack_before) == 1:
            return (None, stack_before[-1])
        return (stack_before[-2], stack_before[-1])

    @staticmethod
    def _apply_event_to_stack(event: TraceEvent, stack: list[int], *, program_name: str) -> None:
        if event.popped:
            observed = tuple(stack[-len(event.popped) :])
            if observed != event.popped:
                raise RuntimeError(
                    f"Replay mismatch while building factorized event examples for {program_name!r}: "
                    f"expected {event.popped}, got {observed}."
                )
            del stack[-len(event.popped) :]
        stack.extend(event.pushed)


def require_torch() -> None:
    if torch is None:
        raise RuntimeError(
            "PyTorch is not installed. Install it explicitly before running the factorized event models."
        )


def default_factorized_event_device(preferred: str | None = None) -> str:
    require_torch()
    if preferred is not None:
        return preferred
    return "cuda" if torch.cuda.is_available() else "cpu"


if torch is not None:  # pragma: no branch

    class FactorizedEventTransformer(nn.Module):
        def __init__(self, codec: FactorizedEventCodec, *, config: FactorizedEventModelConfig) -> None:
            super().__init__()
            if config.d_model % config.n_heads != 0:
                raise ValueError("d_model must be divisible by n_heads.")
            self.codec = codec
            self.config = config
            self.opcode_embedding = nn.Embedding(len(codec.opcodes) + 1, config.opcode_dim)
            self.current_proj = nn.Linear(codec.current_feature_dim + config.opcode_dim, config.d_model)
            self.history_proj = nn.Linear(codec.history_feature_dim + config.opcode_dim, config.d_model)
            self.positional = nn.Embedding(config.history_window + 1, config.d_model)
            layer = nn.TransformerEncoderLayer(
                d_model=config.d_model,
                nhead=config.n_heads,
                dim_feedforward=config.d_ffn,
                dropout=0.0,
                batch_first=True,
                activation="gelu",
            )
            self.encoder = nn.TransformerEncoder(layer, num_layers=config.n_layers)
            self.norm = nn.LayerNorm(config.d_model)
            self.heads = nn.ModuleDict(
                {
                    head: nn.Linear(config.d_model, codec.head_size(head))
                    for head in codec.head_names
                }
            )

        def forward(
            self,
            current_opcodes: "torch.Tensor",
            current_numeric: "torch.Tensor",
            history_opcodes: "torch.Tensor",
            history_numeric: "torch.Tensor",
            history_mask: "torch.Tensor",
        ) -> dict[str, "torch.Tensor"]:
            batch_size = current_opcodes.shape[0]
            history_len = history_opcodes.shape[1]
            current_embedding = self.opcode_embedding(current_opcodes)
            current_token = self.current_proj(torch.cat((current_embedding, current_numeric), dim=-1)).unsqueeze(1)
            history_embedding = self.opcode_embedding(history_opcodes)
            history_tokens = self.history_proj(torch.cat((history_embedding, history_numeric), dim=-1))
            sequence = torch.cat((history_tokens, current_token), dim=1)
            positions = torch.arange(history_len + 1, device=current_opcodes.device).unsqueeze(0).expand(batch_size, -1)
            sequence = sequence + self.positional(positions)
            mask = torch.cat(
                (history_mask, torch.zeros((batch_size, 1), dtype=torch.bool, device=current_opcodes.device)),
                dim=1,
            )
            encoded = self.encoder(sequence, src_key_padding_mask=mask)
            hidden = self.norm(encoded[:, -1, :])
            return {name: head(hidden) for name, head in self.heads.items()}

else:

    class FactorizedEventTransformer:  # pragma: no cover - exercised only without torch
        def __init__(self, codec: FactorizedEventCodec, *, config: FactorizedEventModelConfig) -> None:
            require_torch()


def _batch_examples(
    examples: Sequence[FactorizedEventExample],
    *,
    batch_size: int,
    rng: random.Random | None = None,
) -> list[list[FactorizedEventExample]]:
    ordered = list(examples)
    if rng is not None:
        rng.shuffle(ordered)
    return [ordered[index : index + batch_size] for index in range(0, len(ordered), batch_size)]


def _compute_loss(logits: dict[str, "torch.Tensor"], labels: dict[str, "torch.Tensor"]) -> "torch.Tensor":
    return sum(F.cross_entropy(logits[head], labels[head]) for head in logits)


def evaluate_factorized_event_model(
    model: "FactorizedEventTransformer",
    codec: FactorizedEventCodec,
    examples: Sequence[FactorizedEventExample],
    *,
    device: str | None = None,
    include_top_values: bool | None = None,
) -> FactorizedEventMetrics:
    require_torch()
    if not examples:
        return FactorizedEventMetrics(loss=0.0, exact_label_accuracy=0.0, example_count=0, head_accuracies=())

    device = default_factorized_event_device(device)
    model.eval()
    batch = codec.encode_batch(examples, device=device, include_top_values=include_top_values)
    current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask, labels = batch

    with torch.no_grad():
        logits = model(current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask)
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

    return FactorizedEventMetrics(
        loss=loss,
        exact_label_accuracy=exact / len(examples),
        example_count=len(examples),
        head_accuracies=tuple((head, head_correct[head] / len(examples)) for head in codec.head_names),
    )


def train_factorized_event_model(
    train_programs: Sequence[Program],
    *,
    eval_programs: Sequence[Program] = (),
    model_config: FactorizedEventModelConfig | None = None,
    training_config: FactorizedEventTrainingConfig | None = None,
    interpreter: TraceInterpreter | None = None,
    variant: str = "contextual_event_model",
) -> FactorizedEventTrainingRun:
    require_torch()
    model_config = model_config or FactorizedEventModelConfig()
    training_config = training_config or FactorizedEventTrainingConfig()
    device = default_factorized_event_device(training_config.device)
    torch.manual_seed(training_config.seed)
    random.seed(training_config.seed)

    interpreter = interpreter or TraceInterpreter()
    codec = FactorizedEventCodec(model_config)
    train_examples = codec.build_examples(train_programs, interpreter=interpreter)
    eval_examples = codec.build_examples(eval_programs, interpreter=interpreter) if eval_programs else ()

    model = FactorizedEventTransformer(codec, config=model_config).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=training_config.learning_rate,
        weight_decay=training_config.weight_decay,
    )

    history: list[FactorizedEventEpochStats] = []
    for epoch in range(1, training_config.epochs + 1):
        model.train()
        epoch_losses: list[float] = []
        batches = _batch_examples(
            train_examples,
            batch_size=training_config.batch_size,
            rng=random.Random(training_config.seed + epoch),
        )
        for batch_examples in batches:
            batch = codec.encode_batch(
                batch_examples,
                device=device,
                include_top_values=model_config.include_top_values,
            )
            current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask, labels = batch
            optimizer.zero_grad(set_to_none=True)
            logits = model(current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask)
            loss = _compute_loss(logits, labels)
            loss.backward()
            if training_config.max_grad_norm is not None:
                torch.nn.utils.clip_grad_norm_(model.parameters(), training_config.max_grad_norm)
            optimizer.step()
            epoch_losses.append(float(loss.item()))

        eval_metrics = (
            evaluate_factorized_event_model(
                model,
                codec,
                eval_examples,
                device=device,
                include_top_values=model_config.include_top_values,
            )
            if eval_examples
            else None
        )
        history.append(
            FactorizedEventEpochStats(
                epoch=epoch,
                train_loss=sum(epoch_losses) / len(epoch_losses),
                eval_loss=None if eval_metrics is None else eval_metrics.loss,
            )
        )

    train_metrics = evaluate_factorized_event_model(
        model,
        codec,
        train_examples,
        device=device,
        include_top_values=model_config.include_top_values,
    )
    eval_metrics = (
        evaluate_factorized_event_model(
            model,
            codec,
            eval_examples,
            device=device,
            include_top_values=model_config.include_top_values,
        )
        if eval_examples
        else None
    )
    return FactorizedEventTrainingRun(
        model=model,
        codec=codec,
        train_metrics=train_metrics,
        eval_metrics=eval_metrics,
        history=tuple(history),
        device=device,
        variant=variant,
    )


def train_event_level_softmax_baseline(
    train_programs: Sequence[Program],
    *,
    eval_programs: Sequence[Program] = (),
    model_config: FactorizedEventModelConfig | None = None,
    training_config: FactorizedEventTrainingConfig | None = None,
    interpreter: TraceInterpreter | None = None,
) -> FactorizedEventTrainingRun:
    base = model_config or FactorizedEventModelConfig(
        d_model=36,
        n_heads=18,
        n_layers=7,
        d_ffn=36,
        opcode_dim=8,
        include_top_values=False,
    )
    baseline_config = FactorizedEventModelConfig(
        d_model=base.d_model,
        n_heads=base.n_heads,
        n_layers=base.n_layers,
        d_ffn=base.d_ffn,
        opcode_dim=base.opcode_dim,
        history_window=base.history_window,
        max_scalar=base.max_scalar,
        max_address=base.max_address,
        max_pc=base.max_pc,
        include_top_values=False,
    )
    return train_factorized_event_model(
        train_programs,
        eval_programs=eval_programs,
        model_config=baseline_config,
        training_config=training_config,
        interpreter=interpreter,
        variant="event_level_softmax_baseline",
    )


class FactorizedEventExecutor(FreeRunningTraceExecutor):
    """Run online execution from direct event-field predictions over recent history."""

    def __init__(
        self,
        model: "FactorizedEventTransformer",
        codec: FactorizedEventCodec,
        *,
        device: str | None = None,
        include_top_values: bool | None = None,
        stack_strategy: str = "accelerated",
        memory_strategy: str = "accelerated",
        default_memory_value: int = 0,
        validate_exact_reads: bool = True,
    ) -> None:
        if stack_strategy == "trainable":
            raise ValueError("FactorizedEventExecutor only supports exact stack retrieval strategies.")
        super().__init__(
            stack_strategy=stack_strategy,
            memory_strategy=memory_strategy,
            default_memory_value=default_memory_value,
            validate_exact_reads=validate_exact_reads,
        )
        require_torch()
        self.model = model
        self.codec = codec
        self.device = default_factorized_event_device(device)
        self.include_top_values = codec.config.include_top_values if include_top_values is None else include_top_values
        self.model.to(self.device)
        self.model.eval()
        self._recent_history: list[HistoryEventSummary] = []

    def run(self, program: Program, *, max_steps: int = 10_000) -> FreeRunningExecutionResult:
        self._recent_history = []
        try:
            return super().run(program, max_steps=max_steps)
        finally:
            self._recent_history = []

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
        context = FactorizedEventContext(
            program_name="runtime",
            step=step,
            pc=pc,
            opcode=instruction,
            arg=arg,
            stack_depth=stack_depth,
            top_values=self._peek_stack_values(stack_depth, stack_history),
            recent_history=tuple(self._recent_history[-self.codec.config.history_window :]),
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
        if label.memory_read_address is not None:
            value = self._read_memory(
                step=step,
                address=label.memory_read_address,
                memory_history=memory_history,
                read_observations=read_observations,
            )
            memory_read = (label.memory_read_address, value)

        pushed = tuple(value for value in label.push_values[: label.push_count] if value is not None)
        branch_taken = None if label.branch_state == _NONE_BRANCH else bool(label.branch_state)
        memory_write = None
        if label.memory_write_address is not None:
            if label.memory_write_value is None:
                raise RuntimeError("Predicted a memory-write address without a write value.")
            memory_write = (label.memory_write_address, label.memory_write_value)

        self._recent_history.append(
            HistoryEventSummary(
                opcode=instruction,
                pop_count=label.pop_count,
                push_count=label.push_count,
                push_values=label.push_values,
                branch_state=label.branch_state,
                memory_read_address=label.memory_read_address,
                memory_write_address=label.memory_write_address,
                memory_write_value=label.memory_write_value,
                next_pc=label.next_pc,
                halted=label.halted,
                stack_depth_after=stack_depth - label.pop_count + label.push_count,
            )
        )
        return (popped, pushed, branch_taken, memory_read, memory_write, label.next_pc, label.halted)

    def _peek_stack_values(self, stack_depth: int, stack_history) -> tuple[int | None, int | None]:
        if not self.include_top_values:
            return (None, None)
        second_top = None
        top = None
        if stack_depth >= 2:
            second_top = stack_history.read_exact(stack_depth - 2)[1]
        if stack_depth >= 1:
            top = stack_history.read_exact(stack_depth - 1)[1]
        return (second_top, top)

    def _predict_label(self, context: FactorizedEventContext) -> FactorizedEventLabel:
        current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask = self.codec.encode_context(
            context,
            device=self.device,
            include_top_values=self.include_top_values,
        )
        with torch.no_grad():
            logits = self.model(current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask)
        row_logits = {head: logits[head][0] for head in self.codec.head_names}

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
        push_count = int(self.codec.decode_argmax("push_count", row_logits["push_count"], allowed=(0, 1, 2)))

        push_values: list[int | None] = []
        for slot in range(_MAX_PUSHES):
            if slot >= push_count:
                push_values.append(None)
                continue
            push_values.append(
                self.codec.decode_argmax(
                    f"push_value_{slot}",
                    row_logits[f"push_value_{slot}"],
                    allowed=_allowed_scalar_values(self.codec),
                )
            )

        branch_state = int(
            self.codec.decode_argmax(
                "branch_state",
                row_logits["branch_state"],
                allowed=_allowed_branch_states(context.opcode),
            )
        )
        memory_read_address = self.codec.decode_argmax(
            "memory_read_address",
            row_logits["memory_read_address"],
            allowed=_allowed_memory_read_addresses(self.codec, context.opcode),
        )
        memory_write_address = self.codec.decode_argmax(
            "memory_write_address",
            row_logits["memory_write_address"],
            allowed=_allowed_memory_write_addresses(self.codec, context.opcode),
        )
        memory_write_value = None
        if memory_write_address is not None:
            memory_write_value = self.codec.decode_argmax(
                "memory_write_value",
                row_logits["memory_write_value"],
                allowed=_allowed_scalar_values(self.codec),
            )

        next_pc = int(self.codec.decode_argmax("next_pc", row_logits["next_pc"]))
        halted = bool(
            self.codec.decode_argmax(
                "halted",
                row_logits["halted"],
                allowed=(True,) if context.opcode is Opcode.HALT else (False, True),
            )
        )
        return FactorizedEventLabel(
            stack_read_count=stack_read_count,
            pop_count=pop_count,
            push_count=push_count,
            push_values=(push_values[0], push_values[1]),
            branch_state=branch_state,
            memory_read_address=memory_read_address,
            memory_write_address=memory_write_address,
            memory_write_value=memory_write_value,
            next_pc=next_pc,
            halted=halted,
        )


def run_free_running_with_factorized_event_model(
    program: Program,
    fit: FactorizedEventTrainingRun,
    *,
    decode_mode: str = "accelerated",
    max_steps: int = 10_000,
    include_top_values: bool | None = None,
) -> FreeRunningExecutionResult:
    executor = FactorizedEventExecutor(
        fit.model,
        fit.codec,
        device=fit.device,
        include_top_values=include_top_values,
        stack_strategy=decode_mode,
        memory_strategy=decode_mode,
    )
    return executor.rollout(program, max_steps=max_steps)


def run_free_running_with_event_softmax_baseline(
    program: Program,
    fit: FactorizedEventTrainingRun,
    *,
    decode_mode: str = "accelerated",
    max_steps: int = 10_000,
) -> FreeRunningExecutionResult:
    return run_free_running_with_factorized_event_model(
        program,
        fit,
        decode_mode=decode_mode,
        max_steps=max_steps,
        include_top_values=False,
    )


def _stack_read_count_for_opcode(opcode: Opcode) -> int:
    match opcode:
        case Opcode.ADD | Opcode.SUB | Opcode.EQ | Opcode.STORE_AT:
            return 2
        case Opcode.DUP | Opcode.POP | Opcode.STORE | Opcode.LOAD_AT | Opcode.JZ:
            return 1
        case _:
            return 0


def _expected_popped(reads: Sequence[int], pop_count: int) -> tuple[int, ...]:
    if pop_count == 0:
        return ()
    return tuple(reads[-pop_count:])


def _allowed_scalar_values(codec: FactorizedEventCodec) -> tuple[object, ...]:
    return tuple(value for value in codec._head_spaces["push_value_0"] if value is not None)


def _allowed_branch_states(opcode: Opcode) -> tuple[int, ...]:
    if opcode is Opcode.JMP:
        return (1,)
    if opcode is Opcode.JZ:
        return (0, 1)
    return (_NONE_BRANCH,)


def _allowed_memory_read_addresses(codec: FactorizedEventCodec, opcode: Opcode) -> tuple[object, ...]:
    if opcode in {Opcode.LOAD, Opcode.LOAD_AT}:
        return tuple(codec._head_spaces["memory_read_address"])
    return (None,)


def _allowed_memory_write_addresses(codec: FactorizedEventCodec, opcode: Opcode) -> tuple[object, ...]:
    if opcode in {Opcode.STORE, Opcode.STORE_AT}:
        return tuple(codec._head_spaces["memory_write_address"])
    return (None,)
