"""Staged / pointer-like event models for richer M4 decoding and the final M5 repair."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Literal, Sequence

from exec_trace import Program, TraceInterpreter
from exec_trace.dsl import Opcode
from model.factorized_event_models import (
    _MAX_PUSHES,
    _MAX_STACK_READS,
    FactorizedEventCodec,
    FactorizedEventContext,
    FactorizedEventEpochStats,
    FactorizedEventModelConfig,
    FactorizedEventTrainingConfig,
    FactorizedEventTransformer,
    HistoryEventSummary,
    default_factorized_event_device,
)
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
    _stack_reads,
)

try:  # pragma: no cover - exercised only when torch is installed
    import torch
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - exercised in environments without torch
    torch = None
    F = None


_NONE = "<none>"


@dataclass(frozen=True, slots=True)
class PointerEventLabel:
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
class PointerEventExample:
    context: FactorizedEventContext
    label: PointerEventLabel


@dataclass(frozen=True, slots=True)
class PointerEventMetrics:
    loss: float
    exact_label_accuracy: float
    example_count: int
    head_accuracies: tuple[tuple[str, float], ...]


@dataclass(slots=True)
class PointerEventTrainingRun:
    model: "FactorizedEventTransformer"
    codec: "PointerEventCodec"
    train_metrics: PointerEventMetrics
    eval_metrics: PointerEventMetrics | None
    history: tuple[FactorizedEventEpochStats, ...]
    device: str
    variant: str


class PointerEventCodec:
    """Encode recent-history contexts with candidate-source labels instead of raw values."""

    def __init__(self, config: FactorizedEventModelConfig) -> None:
        self.config = config
        self.features = FactorizedEventCodec(config)
        self.opcodes = self.features.opcodes
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

    @property
    def current_feature_dim(self) -> int:
        return self.features.current_feature_dim

    @property
    def history_feature_dim(self) -> int:
        return self.features.history_feature_dim

    def opcode_id(self, opcode: Opcode | None) -> int:
        return self.features.opcode_id(opcode)

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
    ) -> tuple[PointerEventExample, ...]:
        interpreter = interpreter or TraceInterpreter()
        examples: list[PointerEventExample] = []

        for program in programs:
            result = interpreter.run(program)
            stack: list[int] = []
            history: list[HistoryEventSummary] = []

            for event in result.events:
                context = FactorizedEventContext(
                    program_name=program.name,
                    step=event.step,
                    pc=event.pc,
                    opcode=event.opcode,
                    arg=event.arg,
                    stack_depth=len(stack),
                    top_values=self.features._top_values(stack),
                    recent_history=tuple(history[-self.config.history_window :]),
                )
                label = self.label_from_event(event, stack_before=tuple(stack))
                examples.append(PointerEventExample(context=context, label=label))
                self.features._apply_event_to_stack(event, stack, program_name=program.name)
                history.append(self.features.summary_from_event(event))

        return tuple(examples)

    def label_from_event(self, event, *, stack_before: Sequence[int]) -> PointerEventLabel:
        read_count = _stack_read_count_for_opcode(event.opcode)
        reads = _stack_reads(stack_before, read_count)
        branch_expr = _NONE if event.branch_taken is None else self._infer_bool_expr(event.branch_taken, reads=reads)
        memory_read_address_expr = _NONE
        memory_read_value = None
        if event.memory_read_address is not None:
            memory_read_address_expr = self._infer_address_expr(event.memory_read_address, arg=event.arg, reads=reads)
            memory_read_value = event.memory_read_value

        push_exprs = [_NONE, _NONE]
        for index, value in enumerate(event.pushed[:_MAX_PUSHES]):
            push_exprs[index] = self._infer_scalar_expr(
                value,
                arg=event.arg,
                reads=reads,
                memory_read_value=memory_read_value,
            )

        memory_write_address_expr = _NONE
        memory_write_value_expr = _NONE
        if event.memory_write is not None:
            address, value = event.memory_write
            memory_write_address_expr = self._infer_address_expr(address, arg=event.arg, reads=reads)
            memory_write_value_expr = self._infer_scalar_expr(
                value,
                arg=event.arg,
                reads=reads,
                memory_read_value=memory_read_value,
            )

        next_pc_mode = self._infer_next_pc_mode(
            event.next_pc,
            pc=event.pc,
            arg=event.arg,
            branch_taken=event.branch_taken,
        )
        return PointerEventLabel(
            stack_read_count=read_count,
            pop_count=len(event.popped),
            push_count=len(event.pushed),
            push_exprs=(push_exprs[0], push_exprs[1]),
            branch_expr=branch_expr,
            memory_read_address_expr=memory_read_address_expr,
            memory_write_address_expr=memory_write_address_expr,
            memory_write_value_expr=memory_write_value_expr,
            next_pc_mode=next_pc_mode,
            halted=event.halted,
        )

    def encode_batch(
        self,
        examples: Sequence[PointerEventExample],
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
            [self.features.current_features(example.context, include_top_values=include_top_values) for example in examples],
            dtype=torch.float32,
            device=device,
        )
        history_opcodes = torch.tensor(
            [self.features._history_opcode_ids(example.context.recent_history) for example in examples],
            dtype=torch.long,
            device=device,
        )
        history_numeric = torch.tensor(
            [self.features._history_feature_rows(example.context.recent_history) for example in examples],
            dtype=torch.float32,
            device=device,
        )
        history_mask = torch.tensor(
            [self.features._history_padding_mask(example.context.recent_history) for example in examples],
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
        return self.features.encode_context(context, device=device, include_top_values=include_top_values)

    def _label_value(self, label: PointerEventLabel, head: str) -> object:
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
                raise KeyError(f"Unknown pointer-event head: {head}")

    def _infer_scalar_expr(
        self,
        target: int,
        *,
        arg: int | None,
        reads: Sequence[int],
        memory_read_value: int | None,
    ) -> str:
        for expr in _SCALAR_EXPR_CANDIDATES:
            try:
                predicted = _eval_scalar_expr(expr, arg=arg, reads=reads, memory_read_value=memory_read_value)
            except (IndexError, ValueError):
                continue
            if predicted == target:
                return expr
        raise RuntimeError(f"No scalar candidate matched target value {target}.")

    def _infer_address_expr(self, target: int, *, arg: int | None, reads: Sequence[int]) -> str:
        for expr in _ADDRESS_EXPR_CANDIDATES:
            try:
                predicted = _eval_address_expr(expr, arg=arg, reads=reads)
            except (IndexError, ValueError):
                continue
            if predicted == target:
                return expr
        raise RuntimeError(f"No address candidate matched target address {target}.")

    def _infer_bool_expr(self, target: bool, *, reads: Sequence[int]) -> str:
        for expr in _BOOL_EXPR_CANDIDATES:
            try:
                predicted = _eval_bool_expr(expr, reads=reads)
            except IndexError:
                continue
            if predicted == target:
                return expr
        raise RuntimeError(f"No boolean candidate matched target branch state {target}.")

    def _infer_next_pc_mode(
        self,
        target: int,
        *,
        pc: int,
        arg: int | None,
        branch_taken: bool | None,
    ) -> str:
        for mode in _NEXT_PC_CANDIDATES:
            try:
                predicted = _eval_next_pc(mode, pc=pc, arg=arg, branch_taken=branch_taken)
            except ValueError:
                continue
            if predicted == target:
                return mode
        raise RuntimeError(f"No next-pc candidate matched target next_pc {target}.")


def require_torch() -> None:
    if torch is None:
        raise RuntimeError(
            "PyTorch is not installed. Install it explicitly before running the staged pointer event models."
        )


def _batch_examples(
    examples: Sequence[PointerEventExample],
    *,
    batch_size: int,
    rng: random.Random | None = None,
) -> list[list[PointerEventExample]]:
    ordered = list(examples)
    if rng is not None:
        rng.shuffle(ordered)
    return [ordered[index : index + batch_size] for index in range(0, len(ordered), batch_size)]


def _compute_loss(logits: dict[str, "torch.Tensor"], labels: dict[str, "torch.Tensor"]) -> "torch.Tensor":
    return sum(F.cross_entropy(logits[head], labels[head]) for head in logits)


def evaluate_pointer_event_model(
    model: "FactorizedEventTransformer",
    codec: PointerEventCodec,
    examples: Sequence[PointerEventExample],
    *,
    device: str | None = None,
    include_top_values: bool | None = None,
) -> PointerEventMetrics:
    require_torch()
    if not examples:
        return PointerEventMetrics(loss=0.0, exact_label_accuracy=0.0, example_count=0, head_accuracies=())

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

    return PointerEventMetrics(
        loss=loss,
        exact_label_accuracy=exact / len(examples),
        example_count=len(examples),
        head_accuracies=tuple((head, head_correct[head] / len(examples)) for head in codec.head_names),
    )


def train_pointer_event_model(
    train_programs: Sequence[Program],
    *,
    eval_programs: Sequence[Program] = (),
    model_config: FactorizedEventModelConfig | None = None,
    training_config: FactorizedEventTrainingConfig | None = None,
    interpreter: TraceInterpreter | None = None,
    variant: str = "staged_pointer_event_model",
) -> PointerEventTrainingRun:
    require_torch()
    model_config = model_config or FactorizedEventModelConfig()
    training_config = training_config or FactorizedEventTrainingConfig()
    device = default_factorized_event_device(training_config.device)
    torch.manual_seed(training_config.seed)
    random.seed(training_config.seed)

    interpreter = interpreter or TraceInterpreter()
    codec = PointerEventCodec(model_config)
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
            evaluate_pointer_event_model(
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

    train_metrics = evaluate_pointer_event_model(
        model,
        codec,
        train_examples,
        device=device,
        include_top_values=model_config.include_top_values,
    )
    eval_metrics = (
        evaluate_pointer_event_model(
            model,
            codec,
            eval_examples,
            device=device,
            include_top_values=model_config.include_top_values,
        )
        if eval_examples
        else None
    )
    return PointerEventTrainingRun(
        model=model,
        codec=codec,
        train_metrics=train_metrics,
        eval_metrics=eval_metrics,
        history=tuple(history),
        device=device,
        variant=variant,
    )


def train_pointer_event_softmax_baseline(
    train_programs: Sequence[Program],
    *,
    eval_programs: Sequence[Program] = (),
    model_config: FactorizedEventModelConfig | None = None,
    training_config: FactorizedEventTrainingConfig | None = None,
    interpreter: TraceInterpreter | None = None,
) -> PointerEventTrainingRun:
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
    return train_pointer_event_model(
        train_programs,
        eval_programs=eval_programs,
        model_config=baseline_config,
        training_config=training_config,
        interpreter=interpreter,
        variant="pointer_event_softmax_baseline",
    )


class PointerEventExecutor(FreeRunningTraceExecutor):
    """Run online execution from staged candidate-source predictions over recent history."""

    def __init__(
        self,
        model: "FactorizedEventTransformer",
        codec: PointerEventCodec,
        *,
        device: str | None = None,
        include_top_values: bool | None = None,
        stack_strategy: str = "accelerated",
        memory_strategy: str = "accelerated",
        default_memory_value: int = 0,
        validate_exact_reads: bool = True,
        mask_mode: Literal[
            "structural",
            "opcode_shape",
            "opcode_legal",
            "control_flow_compatible",
            "memory_address_compatible",
            "memory_value_compatible",
        ] = "opcode_legal",
    ) -> None:
        if stack_strategy == "trainable":
            raise ValueError("PointerEventExecutor only supports exact stack retrieval strategies.")
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
        self.mask_mode = mask_mode
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
        memory_read_value = None
        if label.memory_read_address_expr != _NONE:
            address = _eval_address_expr(label.memory_read_address_expr, arg=arg, reads=reads)
            if address < 0:
                raise RuntimeError("Pointer event executor produced a negative memory-read address.")
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
                raise RuntimeError("Pointer event executor produced a negative memory-write address.")
            value = _eval_scalar_expr(
                label.memory_write_value_expr,
                arg=arg,
                reads=reads,
                memory_read_value=memory_read_value,
            )
            memory_write = (address, value)

        next_pc = _eval_next_pc(label.next_pc_mode, pc=pc, arg=arg, branch_taken=branch_taken)
        self._recent_history.append(
            HistoryEventSummary(
                opcode=instruction,
                pop_count=label.pop_count,
                push_count=label.push_count,
                push_values=tuple(list(pushed[:_MAX_PUSHES]) + [None] * (_MAX_PUSHES - len(pushed)))[:2],
                branch_state=-1 if branch_taken is None else int(branch_taken),
                memory_read_address=None if memory_read is None else memory_read[0],
                memory_write_address=None if memory_write is None else memory_write[0],
                memory_write_value=None if memory_write is None else memory_write[1],
                next_pc=next_pc,
                halted=label.halted,
                stack_depth_after=stack_depth - label.pop_count + label.push_count,
            )
        )
        return (popped, pushed, branch_taken, memory_read, memory_write, next_pc, label.halted)

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

    def _predict_label(self, context: FactorizedEventContext) -> PointerEventLabel:
        current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask = self.codec.encode_context(
            context,
            device=self.device,
            include_top_values=self.include_top_values,
        )
        with torch.no_grad():
            logits = self.model(current_opcodes, current_numeric, history_opcodes, history_numeric, history_mask)
        row_logits = {head: logits[head][0] for head in self.codec.head_names}

        has_arg = context.arg is not None
        if self.mask_mode == "opcode_legal":
            read_count_allowed = _allowed_stack_read_counts(context.opcode, context.stack_depth)
            stack_read_count = int(
                self.codec.decode_argmax(
                    "stack_read_count",
                    row_logits["stack_read_count"],
                    allowed=read_count_allowed,
                )
            )
            pop_count = int(
                self.codec.decode_argmax("pop_count", row_logits["pop_count"], allowed=_allowed_pop_counts(context.opcode))
            )
            push_count = int(
                self.codec.decode_argmax("push_count", row_logits["push_count"], allowed=_allowed_push_counts(context.opcode))
            )
            memory_read_address_expr_allowed = _allowed_memory_read_address_exprs(context.opcode, stack_read_count, has_arg)
            branch_expr_allowed = _allowed_branch_exprs(context.opcode, stack_read_count)
            memory_write_address_expr_allowed = _allowed_memory_write_address_exprs(context.opcode, stack_read_count, has_arg)
            halted_allowed = _allowed_halted(context.opcode)
            use_opcode_legal_push_exprs = True
            use_opcode_legal_write_value_exprs = True
            next_pc_mode_allowed = _allowed_next_pc_modes_for_opcode(context.opcode, has_arg, True)
        elif self.mask_mode in {
            "opcode_shape",
            "control_flow_compatible",
            "memory_address_compatible",
            "memory_value_compatible",
        }:
            read_count_allowed = _allowed_stack_read_counts(context.opcode, context.stack_depth)
            stack_read_count = int(
                self.codec.decode_argmax(
                    "stack_read_count",
                    row_logits["stack_read_count"],
                    allowed=read_count_allowed,
                )
            )
            pop_count = int(
                self.codec.decode_argmax("pop_count", row_logits["pop_count"], allowed=_allowed_pop_counts(context.opcode))
            )
            push_count = int(
                self.codec.decode_argmax("push_count", row_logits["push_count"], allowed=_allowed_push_counts(context.opcode))
            )
            use_opcode_legal_address_exprs = self.mask_mode == "memory_address_compatible"
            use_opcode_legal_branch_exprs = self.mask_mode == "control_flow_compatible"
            use_opcode_legal_push_exprs = self.mask_mode == "memory_value_compatible"
            use_opcode_legal_write_value_exprs = self.mask_mode == "memory_value_compatible"
            memory_read_address_expr_allowed = (
                _allowed_memory_read_address_exprs(context.opcode, stack_read_count, has_arg)
                if use_opcode_legal_address_exprs
                else _allowed_shape_memory_read_address_exprs(
                    context.opcode,
                    stack_read_count,
                    has_arg,
                )
            )
            branch_expr_allowed = (
                _allowed_branch_exprs(context.opcode, stack_read_count)
                if use_opcode_legal_branch_exprs
                else _allowed_shape_branch_exprs(context.opcode, stack_read_count)
            )
            memory_write_address_expr_allowed = (
                _allowed_memory_write_address_exprs(context.opcode, stack_read_count, has_arg)
                if use_opcode_legal_address_exprs
                else _allowed_shape_memory_write_address_exprs(
                    context.opcode,
                    stack_read_count,
                    has_arg,
                )
            )
            halted_allowed = _allowed_halted(context.opcode)
            next_pc_mode_allowed = _allowed_next_pc_modes_for_opcode(context.opcode, has_arg, True)
        else:
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
            memory_read_address_expr_allowed = _allowed_address_exprs(stack_read_count, has_arg, allow_none=True)
            branch_expr_allowed = _allowed_bool_exprs(stack_read_count, allow_none=True)
            memory_write_address_expr_allowed = _allowed_address_exprs(stack_read_count, has_arg, allow_none=True)
            halted_allowed = (False, True)
            use_opcode_legal_push_exprs = False
            use_opcode_legal_write_value_exprs = False
            next_pc_mode_allowed = None

        memory_read_address_expr = str(
            self.codec.decode_argmax(
                "memory_read_address_expr",
                row_logits["memory_read_address_expr"],
                allowed=memory_read_address_expr_allowed,
            )
        )
        has_memory_read = memory_read_address_expr != _NONE

        branch_expr = str(
            self.codec.decode_argmax(
                "branch_expr",
                row_logits["branch_expr"],
                allowed=branch_expr_allowed,
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
                        allowed=(
                            _allowed_push_exprs(context.opcode, stack_read_count, has_arg, has_memory_read)
                            if use_opcode_legal_push_exprs
                            else _allowed_scalar_exprs(
                                stack_read_count,
                                has_arg,
                                has_memory_read,
                                allow_none=False,
                            )
                        ),
                    )
                )
            )

        memory_write_address_expr = str(
            self.codec.decode_argmax(
                "memory_write_address_expr",
                row_logits["memory_write_address_expr"],
                allowed=memory_write_address_expr_allowed,
            )
        )
        if memory_write_address_expr == _NONE:
            memory_write_value_expr = _NONE
        else:
            memory_write_value_expr = str(
                self.codec.decode_argmax(
                    "memory_write_value_expr",
                    row_logits["memory_write_value_expr"],
                    allowed=(
                        _allowed_memory_write_value_exprs(
                            context.opcode,
                            stack_read_count,
                            has_arg,
                            has_memory_read,
                        )
                        if use_opcode_legal_write_value_exprs
                        else _allowed_scalar_exprs(
                            stack_read_count,
                            has_arg,
                            has_memory_read,
                            allow_none=False,
                        )
                    ),
                )
            )

        next_pc_mode = str(
            self.codec.decode_argmax(
                "next_pc_mode",
                row_logits["next_pc_mode"],
                allowed=(
                    next_pc_mode_allowed
                    if next_pc_mode_allowed is not None
                    else _allowed_next_pc_modes(has_arg, branch_available)
                ),
            )
        )
        halted = bool(self.codec.decode_argmax("halted", row_logits["halted"], allowed=halted_allowed))
        return PointerEventLabel(
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


def run_free_running_with_pointer_event_model(
    program: Program,
    fit: PointerEventTrainingRun,
    *,
    decode_mode: str = "accelerated",
    max_steps: int = 10_000,
    include_top_values: bool | None = None,
    mask_mode: Literal[
        "structural",
        "opcode_shape",
        "opcode_legal",
        "control_flow_compatible",
        "memory_address_compatible",
        "memory_value_compatible",
    ] = "opcode_legal",
) -> FreeRunningExecutionResult:
    executor = PointerEventExecutor(
        fit.model,
        fit.codec,
        device=fit.device,
        include_top_values=include_top_values,
        stack_strategy=decode_mode,
        memory_strategy=decode_mode,
        mask_mode=mask_mode,
    )
    return executor.rollout(program, max_steps=max_steps)


def run_free_running_with_pointer_softmax_baseline(
    program: Program,
    fit: PointerEventTrainingRun,
    *,
    decode_mode: str = "accelerated",
    max_steps: int = 10_000,
    mask_mode: Literal[
        "structural",
        "opcode_shape",
        "opcode_legal",
        "control_flow_compatible",
        "memory_address_compatible",
        "memory_value_compatible",
    ] = "structural",
) -> FreeRunningExecutionResult:
    return run_free_running_with_pointer_event_model(
        program,
        fit,
        decode_mode=decode_mode,
        max_steps=max_steps,
        include_top_values=False,
        mask_mode=mask_mode,
    )


def _stack_read_count_for_opcode(opcode: Opcode) -> int:
    match opcode:
        case Opcode.ADD | Opcode.SUB | Opcode.EQ | Opcode.STORE_AT:
            return 2
        case Opcode.DUP | Opcode.POP | Opcode.STORE | Opcode.LOAD_AT | Opcode.JZ:
            return 1
        case _:
            return 0


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


def _allowed_stack_read_counts(opcode: Opcode, stack_depth: int) -> tuple[int, ...]:
    return (min(_stack_read_count_for_opcode(opcode), stack_depth),)


def _allowed_pop_counts(opcode: Opcode) -> tuple[int, ...]:
    match opcode:
        case Opcode.ADD | Opcode.SUB | Opcode.EQ | Opcode.STORE_AT:
            return (2,)
        case Opcode.POP | Opcode.STORE | Opcode.LOAD_AT | Opcode.JZ:
            return (1,)
        case _:
            return (0,)


def _allowed_push_counts(opcode: Opcode) -> tuple[int, ...]:
    match opcode:
        case Opcode.PUSH_CONST | Opcode.ADD | Opcode.SUB | Opcode.EQ | Opcode.DUP | Opcode.LOAD | Opcode.LOAD_AT:
            return (1,)
        case _:
            return (0,)


def _allowed_push_exprs(
    opcode: Opcode,
    read_count: int,
    has_arg: bool,
    has_memory_read: bool,
) -> tuple[object, ...]:
    match opcode:
        case Opcode.PUSH_CONST:
            return ("const_arg",) if has_arg else ()
        case Opcode.ADD:
            return ("add",) if read_count >= 2 else ()
        case Opcode.SUB:
            return ("sub",) if read_count >= 2 else ()
        case Opcode.EQ:
            return ("eq",) if read_count >= 2 else ()
        case Opcode.DUP:
            return ("read0",) if read_count >= 1 else ()
        case Opcode.LOAD | Opcode.LOAD_AT:
            return ("memory_read_value",) if has_memory_read else ()
        case _:
            return _allowed_scalar_exprs(read_count, has_arg, has_memory_read, allow_none=False)


def _allowed_memory_read_address_exprs(opcode: Opcode, read_count: int, has_arg: bool) -> tuple[object, ...]:
    match opcode:
        case Opcode.LOAD:
            return ("const_arg",) if has_arg else (_NONE,)
        case Opcode.LOAD_AT:
            return ("read0",) if read_count >= 1 else (_NONE,)
        case _:
            return (_NONE,)


def _allowed_memory_write_address_exprs(opcode: Opcode, read_count: int, has_arg: bool) -> tuple[object, ...]:
    match opcode:
        case Opcode.STORE:
            return ("const_arg",) if has_arg else (_NONE,)
        case Opcode.STORE_AT:
            return ("read1",) if read_count >= 2 else (_NONE,)
        case _:
            return (_NONE,)


def _allowed_memory_write_value_exprs(
    opcode: Opcode,
    read_count: int,
    has_arg: bool,
    has_memory_read: bool,
) -> tuple[object, ...]:
    match opcode:
        case Opcode.STORE | Opcode.STORE_AT:
            return ("read0",) if read_count >= 1 else _allowed_scalar_exprs(
                read_count,
                has_arg,
                has_memory_read,
                allow_none=False,
            )
        case _:
            return _allowed_scalar_exprs(read_count, has_arg, has_memory_read, allow_none=False)


def _allowed_branch_exprs(opcode: Opcode, read_count: int) -> tuple[object, ...]:
    match opcode:
        case Opcode.JMP:
            return ("always_true",)
        case Opcode.JZ:
            return ("read0_is_zero",) if read_count >= 1 else (_NONE,)
        case _:
            return (_NONE,)


def _allowed_next_pc_modes_for_opcode(opcode: Opcode, has_arg: bool, branch_available: bool) -> tuple[str, ...]:
    match opcode:
        case Opcode.JMP:
            return ("const_arg",) if has_arg else ("sequential",)
        case Opcode.JZ:
            if has_arg and branch_available:
                return ("branch_arg_else_seq",)
            return ("sequential",)
        case Opcode.HALT:
            return ("self_pc",)
        case _:
            return ("sequential",)


def _allowed_halted(opcode: Opcode) -> tuple[bool, ...]:
    return (True,) if opcode is Opcode.HALT else (False,)


def _allowed_shape_memory_read_address_exprs(opcode: Opcode, read_count: int, has_arg: bool) -> tuple[object, ...]:
    if opcode in {Opcode.LOAD, Opcode.LOAD_AT}:
        return _allowed_address_exprs(read_count, has_arg, allow_none=False)
    return (_NONE,)


def _allowed_shape_memory_write_address_exprs(opcode: Opcode, read_count: int, has_arg: bool) -> tuple[object, ...]:
    if opcode in {Opcode.STORE, Opcode.STORE_AT}:
        return _allowed_address_exprs(read_count, has_arg, allow_none=False)
    return (_NONE,)


def _allowed_shape_branch_exprs(opcode: Opcode, read_count: int) -> tuple[object, ...]:
    if opcode is Opcode.JMP:
        return ("always_true",)
    if opcode is Opcode.JZ:
        return _allowed_bool_exprs(read_count, allow_none=False)
    return (_NONE,)
