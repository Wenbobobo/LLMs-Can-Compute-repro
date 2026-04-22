"""Standard 2D-head softmax baseline scaffolding for M5."""

from __future__ import annotations

from dataclasses import dataclass
import random
from statistics import mean
from typing import Iterable, Literal, Sequence

from exec_trace import Opcode, Program, TraceEvent, TraceInterpreter

try:  # pragma: no cover - exercised only when torch is installed
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - exercised in environments without torch
    torch = None
    nn = None
    F = None


SPECIAL_TOKENS = ("<pad>", "<bos>", "<instructions>", "<trace>", "<event>", "<eos>")
TraceTokenizationMode = Literal["atomic", "factorized", "event_grouped"]
FACTORIZED_BASE_TOKENS = SPECIAL_TOKENS + (
    "<inst>",
    "</inst>",
    "<int>",
    "</int>",
    "<list>",
    "</list>",
    "<pair>",
    "</pair>",
    "<none>",
    "pc",
    "op",
    "arg",
    "step",
    "popped",
    "pushed",
    "branch",
    "memory_read",
    "memory_write",
    "next_pc",
    "stack_before",
    "stack_after",
    "halted",
    "1",
    "0",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "-",
    "none",
) + tuple(str(opcode) for opcode in Opcode)
EVENT_GROUPED_BASE_TOKENS = SPECIAL_TOKENS + (
    "<inst>",
    "</inst>",
    "<int>",
    "</int>",
    "<list>",
    "</list>",
    "<pair>",
    "</pair>",
    "<none>",
    "pc",
    "op",
    "arg",
    "popped",
    "pushed",
    "branch",
    "memory_read",
    "memory_write",
    "halted",
) + tuple(str(digit) for digit in range(10)) + ("-", "none") + tuple(str(opcode) for opcode in Opcode)


@dataclass(frozen=True, slots=True)
class TraceSequenceExample:
    program_name: str
    program_steps: int
    tokens: tuple[str, ...]
    tokenization_mode: TraceTokenizationMode = "atomic"


@dataclass(frozen=True, slots=True)
class TraceSequenceStats:
    example_count: int
    vocab_size: int
    min_length: int
    max_length: int
    mean_length: float


@dataclass(frozen=True, slots=True)
class EncodedTraceExample:
    program_name: str
    program_steps: int
    token_ids: tuple[int, ...]
    prompt_length: int
    tokenization_mode: TraceTokenizationMode


@dataclass(frozen=True, slots=True)
class TeacherForcedMetrics:
    loss: float
    token_accuracy: float
    example_count: int
    token_count: int
    by_length_bucket: tuple[tuple[str, dict[str, float | int]], ...]


@dataclass(frozen=True, slots=True)
class RolloutOutcome:
    program_name: str
    program_steps: int
    exact_sequence_match: bool
    first_error_token_index: int | None
    generated_token_count: int
    failure_reason: str | None


@dataclass(frozen=True, slots=True)
class RolloutEvaluation:
    exact_sequence_accuracy: float
    example_count: int
    by_length_bucket: tuple[tuple[str, dict[str, float | int]], ...]
    outcomes: tuple[RolloutOutcome, ...]


@dataclass(frozen=True, slots=True)
class SoftmaxTrainingConfig:
    epochs: int = 20
    batch_size: int = 4
    learning_rate: float = 3e-3
    weight_decay: float = 0.0
    seed: int = 0
    max_grad_norm: float | None = 1.0
    device: str | None = None


@dataclass(frozen=True, slots=True)
class TrainingEpochStats:
    epoch: int
    train_loss: float
    eval_loss: float | None


@dataclass(slots=True)
class SoftmaxTrainingRun:
    model: "Standard2DSoftmaxTransformer"
    train_metrics: TeacherForcedMetrics
    eval_metrics: TeacherForcedMetrics | None
    history: tuple[TrainingEpochStats, ...]
    device: str


@dataclass(frozen=True, slots=True)
class SoftmaxBaselineConfig:
    vocab_size: int
    d_model: int = 36
    n_heads: int = 18
    n_layers: int = 7
    d_ffn: int = 36
    max_seq_len: int = 4096


class TraceVocabulary:
    def __init__(self, tokens: Sequence[str]) -> None:
        unique = list(dict.fromkeys(tokens))
        self._token_to_id = {token: index for index, token in enumerate(unique)}
        self._id_to_token = tuple(unique)

    @classmethod
    def from_examples(
        cls,
        examples: Sequence[TraceSequenceExample],
        *,
        base_tokens: Sequence[str] = SPECIAL_TOKENS,
    ) -> "TraceVocabulary":
        tokens: list[str] = list(base_tokens)
        for example in examples:
            tokens.extend(example.tokens)
        return cls(tokens)

    def __len__(self) -> int:
        return len(self._id_to_token)

    def encode(self, tokens: Sequence[str]) -> tuple[int, ...]:
        try:
            return tuple(self._token_to_id[token] for token in tokens)
        except KeyError as exc:
            raise KeyError(f"Token {exc.args[0]!r} is not present in the vocabulary.") from exc

    def decode(self, ids: Sequence[int]) -> tuple[str, ...]:
        return tuple(self._id_to_token[index] for index in ids)


def require_torch() -> None:
    if torch is None:
        raise RuntimeError(
            "PyTorch is not installed. Install it explicitly for M5, for example via an "
            "optional dependency group before running the softmax baseline."
        )


def base_tokens_for_mode(mode: TraceTokenizationMode) -> tuple[str, ...]:
    if mode == "atomic":
        return SPECIAL_TOKENS
    if mode == "factorized":
        return FACTORIZED_BASE_TOKENS
    return EVENT_GROUPED_BASE_TOKENS


def _encode_int_tokens(value: int) -> tuple[str, ...]:
    digits = str(abs(value))
    tokens = ["<int>"]
    if value < 0:
        tokens.append("-")
    tokens.extend(digits)
    tokens.append("</int>")
    return tuple(tokens)


def _encode_optional_int_tokens(value: int | None) -> tuple[str, ...]:
    if value is None:
        return ("<none>",)
    return _encode_int_tokens(value)


def _encode_int_list_tokens(values: Sequence[int]) -> tuple[str, ...]:
    if not values:
        return ("<none>",)
    tokens = ["<list>"]
    for value in values:
        tokens.extend(_encode_int_tokens(value))
    tokens.append("</list>")
    return tuple(tokens)


def _encode_optional_pair_tokens(pair: tuple[int, int] | None) -> tuple[str, ...]:
    if pair is None:
        return ("<none>",)
    tokens = ["<pair>"]
    tokens.extend(_encode_int_tokens(pair[0]))
    tokens.extend(_encode_int_tokens(pair[1]))
    tokens.append("</pair>")
    return tuple(tokens)


def serialize_instruction_tokens(
    program: Program,
    *,
    tokenization_mode: TraceTokenizationMode = "atomic",
) -> tuple[str, ...]:
    if tokenization_mode == "atomic":
        tokens: list[str] = ["<instructions>"]
        for pc, instruction in enumerate(program.instructions):
            tokens.extend(
                (
                    f"inst_pc={pc}",
                    f"inst_op={instruction.opcode}",
                    f"inst_arg={instruction.arg if instruction.arg is not None else 'none'}",
                )
            )
        return tuple(tokens)

    tokens: list[str] = ["<instructions>"]
    for pc, instruction in enumerate(program.instructions):
        tokens.extend(("<inst>", "pc"))
        tokens.extend(_encode_int_tokens(pc))
        tokens.extend(("op", str(instruction.opcode), "arg"))
        tokens.extend(_encode_optional_int_tokens(instruction.arg))
        tokens.append("</inst>")
    return tuple(tokens)


def serialize_event_tokens(
    event: TraceEvent,
    *,
    tokenization_mode: TraceTokenizationMode = "atomic",
) -> tuple[str, ...]:
    if tokenization_mode == "atomic":
        popped = ",".join(str(value) for value in event.popped) if event.popped else "none"
        pushed = ",".join(str(value) for value in event.pushed) if event.pushed else "none"
        memory_read = (
            "none"
            if event.memory_read_address is None
            else f"{event.memory_read_address}:{event.memory_read_value}"
        )
        memory_write = "none" if event.memory_write is None else f"{event.memory_write[0]}:{event.memory_write[1]}"
        branch_taken = "none" if event.branch_taken is None else str(int(event.branch_taken))

        return (
            "<event>",
            f"step={event.step}",
            f"pc={event.pc}",
            f"opcode={event.opcode}",
            f"arg={event.arg if event.arg is not None else 'none'}",
            f"popped={popped}",
            f"pushed={pushed}",
            f"branch={branch_taken}",
            f"memory_read={memory_read}",
            f"memory_write={memory_write}",
            f"next_pc={event.next_pc}",
            f"stack_before={event.stack_depth_before}",
            f"stack_after={event.stack_depth_after}",
            f"halted={int(event.halted)}",
        )

    popped = ",".join(str(value) for value in event.popped) if event.popped else "none"
    pushed = ",".join(str(value) for value in event.pushed) if event.pushed else "none"
    memory_read = (
        "none"
        if event.memory_read_address is None
        else f"{event.memory_read_address}:{event.memory_read_value}"
    )
    memory_write = "none" if event.memory_write is None else f"{event.memory_write[0]}:{event.memory_write[1]}"
    branch_taken = "none" if event.branch_taken is None else str(int(event.branch_taken))

    if tokenization_mode == "factorized":
        tokens = ["<event>", "step"]
        tokens.extend(_encode_int_tokens(event.step))
        tokens.extend(("pc",))
        tokens.extend(_encode_int_tokens(event.pc))
        tokens.extend(("op", str(event.opcode), "arg"))
        tokens.extend(_encode_optional_int_tokens(event.arg))
        tokens.extend(("popped",))
        tokens.extend(_encode_int_list_tokens(event.popped))
        tokens.extend(("pushed",))
        tokens.extend(_encode_int_list_tokens(event.pushed))
        tokens.extend(("branch",))
        if event.branch_taken is None:
            tokens.append("<none>")
        else:
            tokens.extend(_encode_int_tokens(int(event.branch_taken)))
        tokens.extend(("memory_read",))
        if event.memory_read_address is None:
            tokens.append("<none>")
        else:
            tokens.extend(_encode_optional_pair_tokens((event.memory_read_address, int(event.memory_read_value))))
        tokens.extend(("memory_write",))
        tokens.extend(_encode_optional_pair_tokens(event.memory_write))
        tokens.extend(("next_pc",))
        tokens.extend(_encode_int_tokens(event.next_pc))
        tokens.extend(("stack_before",))
        tokens.extend(_encode_int_tokens(event.stack_depth_before))
        tokens.extend(("stack_after",))
        tokens.extend(_encode_int_tokens(event.stack_depth_after))
        tokens.extend(("halted",))
        tokens.extend(_encode_int_tokens(int(event.halted)))
        return tuple(tokens)

    tokens = ["<event>", "op", str(event.opcode), "arg"]
    tokens.extend(_encode_optional_int_tokens(event.arg))
    tokens.extend(("popped",))
    tokens.extend(_encode_int_list_tokens(event.popped))
    tokens.extend(("pushed",))
    tokens.extend(_encode_int_list_tokens(event.pushed))
    tokens.extend(("branch",))
    if event.branch_taken is None:
        tokens.append("<none>")
    else:
        tokens.extend(_encode_int_tokens(int(event.branch_taken)))
    tokens.extend(("memory_read",))
    if event.memory_read_address is None:
        tokens.append("<none>")
    else:
        tokens.extend(_encode_optional_pair_tokens((event.memory_read_address, int(event.memory_read_value))))
    tokens.extend(("memory_write",))
    tokens.extend(_encode_optional_pair_tokens(event.memory_write))
    tokens.extend(("halted",))
    tokens.extend(_encode_int_tokens(int(event.halted)))
    return tuple(tokens)


def build_trace_sequence(
    program: Program,
    *,
    interpreter: TraceInterpreter | None = None,
    tokenization_mode: TraceTokenizationMode = "atomic",
) -> TraceSequenceExample:
    interpreter = interpreter or TraceInterpreter()
    result = interpreter.run(program)

    tokens: list[str] = ["<bos>", *serialize_instruction_tokens(program, tokenization_mode=tokenization_mode), "<trace>"]
    for event in result.events:
        tokens.extend(serialize_event_tokens(event, tokenization_mode=tokenization_mode))
    tokens.append("<eos>")

    return TraceSequenceExample(
        program_name=program.name,
        program_steps=result.final_state.steps,
        tokens=tuple(tokens),
        tokenization_mode=tokenization_mode,
    )


def build_trace_sequences(
    programs: Iterable[Program],
    *,
    interpreter: TraceInterpreter | None = None,
    tokenization_mode: TraceTokenizationMode = "atomic",
) -> tuple[TraceSequenceExample, ...]:
    interpreter = interpreter or TraceInterpreter()
    return tuple(
        build_trace_sequence(program, interpreter=interpreter, tokenization_mode=tokenization_mode)
        for program in programs
    )


def summarize_trace_sequences(
    examples: Sequence[TraceSequenceExample],
    *,
    base_tokens: Sequence[str] = SPECIAL_TOKENS,
) -> TraceSequenceStats:
    lengths = [len(example.tokens) for example in examples]
    vocab = TraceVocabulary.from_examples(examples, base_tokens=base_tokens)
    return TraceSequenceStats(
        example_count=len(examples),
        vocab_size=len(vocab),
        min_length=min(lengths) if lengths else 0,
        max_length=max(lengths) if lengths else 0,
        mean_length=mean(lengths) if lengths else 0.0,
    )


def prompt_length(example: TraceSequenceExample) -> int:
    return example.tokens.index("<trace>") + 1


def encode_trace_examples(
    examples: Sequence[TraceSequenceExample],
    vocabulary: TraceVocabulary,
) -> tuple[EncodedTraceExample, ...]:
    return tuple(
        EncodedTraceExample(
            program_name=example.program_name,
            program_steps=example.program_steps,
            token_ids=vocabulary.encode(example.tokens),
            prompt_length=prompt_length(example),
            tokenization_mode=example.tokenization_mode,
        )
        for example in examples
    )


def baseline_bucket_name(program_steps: int) -> str:
    if program_steps <= 24:
        return "steps<=24"
    if program_steps <= 48:
        return "25<=steps<=48"
    return "steps>=49"


if torch is not None:  # pragma: no branch

    class Standard2DSoftmaxTransformer(nn.Module):
        def __init__(self, config: SoftmaxBaselineConfig) -> None:
            super().__init__()
            if config.d_model % config.n_heads != 0:
                raise ValueError("d_model must be divisible by n_heads.")
            if config.d_model // config.n_heads != 2:
                raise ValueError("This baseline intentionally keeps head dimension fixed at 2.")

            self.config = config
            self.tok = nn.Embedding(config.vocab_size, config.d_model)
            self.pos = nn.Embedding(config.max_seq_len, config.d_model)
            self.attn = nn.ModuleList(
                [
                    nn.MultiheadAttention(config.d_model, config.n_heads, batch_first=True, bias=False)
                    for _ in range(config.n_layers)
                ]
            )
            self.ff_in = nn.ModuleList(
                [nn.Linear(config.d_model, 2 * config.d_ffn, bias=False) for _ in range(config.n_layers)]
            )
            self.ff_out = nn.ModuleList(
                [nn.Linear(config.d_ffn, config.d_model, bias=False) for _ in range(config.n_layers)]
            )
            self.head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        def forward(self, token_ids: "torch.Tensor") -> "torch.Tensor":
            batch_size, seq_len = token_ids.shape
            if seq_len > self.config.max_seq_len:
                raise ValueError(f"Sequence length {seq_len} exceeds configured max_seq_len={self.config.max_seq_len}.")

            positions = torch.arange(seq_len, device=token_ids.device)
            x = self.tok(token_ids) + self.pos(positions).unsqueeze(0)
            causal = torch.triu(
                torch.ones(seq_len, seq_len, device=token_ids.device, dtype=torch.bool),
                diagonal=1,
            )

            for attn, ff_in, ff_out in zip(self.attn, self.ff_in, self.ff_out):
                y, _ = attn(x, x, x, attn_mask=causal, need_weights=False)
                x = x + y
                gate, value = ff_in(x).chunk(2, dim=-1)
                x = x + ff_out(F.relu(gate) * value)

            return self.head(x)


    def causal_language_model_loss(logits: "torch.Tensor", targets: "torch.Tensor") -> "torch.Tensor":
        return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), ignore_index=-100)


    def default_baseline_device(preferred: str | None = None) -> str:
        if preferred is not None:
            return preferred
        return "cuda" if torch.cuda.is_available() else "cpu"


    def _batch_examples(
        examples: Sequence[EncodedTraceExample],
        *,
        batch_size: int,
        rng: random.Random | None = None,
    ) -> list[list[EncodedTraceExample]]:
        ordered = list(examples)
        if rng is not None:
            rng.shuffle(ordered)
        return [ordered[index : index + batch_size] for index in range(0, len(ordered), batch_size)]


    def _encode_batch(
        examples: Sequence[EncodedTraceExample],
        *,
        device: str,
    ) -> tuple["torch.Tensor", "torch.Tensor"]:
        max_len = max(len(example.token_ids) for example in examples)
        input_ids = torch.full((len(examples), max_len - 1), 0, dtype=torch.long, device=device)
        targets = torch.full((len(examples), max_len - 1), -100, dtype=torch.long, device=device)

        for index, example in enumerate(examples):
            ids = torch.tensor(example.token_ids, dtype=torch.long, device=device)
            usable = len(example.token_ids) - 1
            input_ids[index, :usable] = ids[:-1]
            targets[index, :usable] = ids[1:]

        return (input_ids, targets)


    def evaluate_teacher_forced_model(
        model: "Standard2DSoftmaxTransformer",
        examples: Sequence[EncodedTraceExample],
        *,
        device: str | None = None,
    ) -> TeacherForcedMetrics:
        if not examples:
            return TeacherForcedMetrics(
                loss=0.0,
                token_accuracy=0.0,
                example_count=0,
                token_count=0,
                by_length_bucket=(),
            )

        device = default_baseline_device(device)
        model.eval()
        per_bucket: dict[str, dict[str, float | int]] = {}
        total_loss = 0.0
        total_tokens = 0
        total_correct = 0

        with torch.no_grad():
            for example in examples:
                input_ids, targets = _encode_batch((example,), device=device)
                logits = model(input_ids)
                loss = causal_language_model_loss(logits, targets)
                predictions = logits.argmax(dim=-1)
                mask = targets != -100
                token_count = int(mask.sum().item())
                correct = int(((predictions == targets) & mask).sum().item())

                total_loss += float(loss.item()) * token_count
                total_tokens += token_count
                total_correct += correct

                bucket = baseline_bucket_name(example.program_steps)

                # Performance optimization: explicit check to avoid eager evaluation
                if bucket not in per_bucket:
                    per_bucket[bucket] = {
                        "example_count": 0,
                        "token_count": 0,
                        "correct_tokens": 0,
                        "weighted_loss": 0.0,
                    }
                bucket_state = per_bucket[bucket]

                bucket_state["example_count"] = int(bucket_state["example_count"]) + 1
                bucket_state["token_count"] = int(bucket_state["token_count"]) + token_count
                bucket_state["correct_tokens"] = int(bucket_state["correct_tokens"]) + correct
                bucket_state["weighted_loss"] = float(bucket_state["weighted_loss"]) + (float(loss.item()) * token_count)

        by_length_bucket = tuple(
            (
                bucket,
                {
                    "example_count": int(state["example_count"]),
                    "token_count": int(state["token_count"]),
                    "loss": float(state["weighted_loss"]) / int(state["token_count"]),
                    "token_accuracy": int(state["correct_tokens"]) / int(state["token_count"]),
                },
            )
            for bucket, state in sorted(per_bucket.items())
        )

        return TeacherForcedMetrics(
            loss=total_loss / total_tokens,
            token_accuracy=total_correct / total_tokens,
            example_count=len(examples),
            token_count=total_tokens,
            by_length_bucket=by_length_bucket,
        )


    def train_teacher_forced_baseline(
        train_examples: Sequence[EncodedTraceExample],
        *,
        model_config: SoftmaxBaselineConfig,
        training_config: SoftmaxTrainingConfig | None = None,
        eval_examples: Sequence[EncodedTraceExample] = (),
    ) -> SoftmaxTrainingRun:
        require_torch()
        training_config = training_config or SoftmaxTrainingConfig()
        device = default_baseline_device(training_config.device)
        torch.manual_seed(training_config.seed)
        random.seed(training_config.seed)

        model = Standard2DSoftmaxTransformer(model_config).to(device)
        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=training_config.learning_rate,
            weight_decay=training_config.weight_decay,
        )

        history: list[TrainingEpochStats] = []
        for epoch in range(1, training_config.epochs + 1):
            model.train()
            epoch_losses: list[float] = []
            batches = _batch_examples(
                train_examples,
                batch_size=training_config.batch_size,
                rng=random.Random(training_config.seed + epoch),
            )
            for batch in batches:
                input_ids, targets = _encode_batch(batch, device=device)
                optimizer.zero_grad(set_to_none=True)
                logits = model(input_ids)
                loss = causal_language_model_loss(logits, targets)
                loss.backward()
                if training_config.max_grad_norm is not None:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), training_config.max_grad_norm)
                optimizer.step()
                epoch_losses.append(float(loss.item()))

            eval_metrics = evaluate_teacher_forced_model(model, eval_examples, device=device) if eval_examples else None
            history.append(
                TrainingEpochStats(
                    epoch=epoch,
                    train_loss=sum(epoch_losses) / len(epoch_losses),
                    eval_loss=None if eval_metrics is None else eval_metrics.loss,
                )
            )

        train_metrics = evaluate_teacher_forced_model(model, train_examples, device=device)
        eval_metrics = evaluate_teacher_forced_model(model, eval_examples, device=device) if eval_examples else None
        return SoftmaxTrainingRun(
            model=model,
            train_metrics=train_metrics,
            eval_metrics=eval_metrics,
            history=tuple(history),
            device=device,
        )


    def greedy_rollout(
        model: "Standard2DSoftmaxTransformer",
        example: EncodedTraceExample,
        *,
        device: str | None = None,
        eos_token_id: int,
        max_total_tokens: int | None = None,
    ) -> tuple[int, ...]:
        device = default_baseline_device(device)
        model.eval()
        generated = list(example.token_ids[: example.prompt_length])
        max_total_tokens = max_total_tokens or max(len(example.token_ids) + 16, example.prompt_length + 1)

        with torch.no_grad():
            while len(generated) < max_total_tokens:
                input_ids = torch.tensor([generated], dtype=torch.long, device=device)
                logits = model(input_ids)
                next_token = int(logits[0, -1].argmax().item())
                generated.append(next_token)
                if next_token == eos_token_id:
                    break

        return tuple(generated)


    def evaluate_free_running_rollout(
        model: "Standard2DSoftmaxTransformer",
        examples: Sequence[EncodedTraceExample],
        *,
        vocabulary: TraceVocabulary,
        device: str | None = None,
        max_total_tokens: int | None = None,
    ) -> RolloutEvaluation:
        if not examples:
            return RolloutEvaluation(exact_sequence_accuracy=0.0, example_count=0, by_length_bucket=(), outcomes=())

        eos_token_id = vocabulary.encode(("<eos>",))[0]
        outcomes: list[RolloutOutcome] = []
        per_bucket: dict[str, dict[str, int]] = {}

        for example in examples:
            generated = greedy_rollout(
                model,
                example,
                device=device,
                eos_token_id=eos_token_id,
                max_total_tokens=max_total_tokens,
            )
            exact = generated == example.token_ids
            first_error = None
            for index, (expected, actual) in enumerate(zip(example.token_ids, generated)):
                if expected != actual:
                    first_error = index
                    break
            if first_error is None and len(generated) != len(example.token_ids):
                first_error = min(len(generated), len(example.token_ids))

            failure_reason = None
            if not exact and generated[-1] != eos_token_id:
                failure_reason = "missing_eos"
            elif not exact and len(generated) != len(example.token_ids):
                failure_reason = "length_mismatch"

            outcomes.append(
                RolloutOutcome(
                    program_name=example.program_name,
                    program_steps=example.program_steps,
                    exact_sequence_match=exact,
                    first_error_token_index=first_error,
                    generated_token_count=len(generated),
                    failure_reason=failure_reason,
                )
            )

            bucket = baseline_bucket_name(example.program_steps)
            # Performance optimization: explicit check to avoid eager evaluation
            if bucket not in per_bucket:
                per_bucket[bucket] = {"example_count": 0, "exact_count": 0}
            bucket_state = per_bucket[bucket]
            bucket_state["example_count"] = int(bucket_state["example_count"]) + 1
            bucket_state["exact_count"] = int(bucket_state["exact_count"]) + int(exact)

        by_length_bucket = tuple(
            (
                bucket,
                {
                    "example_count": int(state["example_count"]),
                    "exact_sequence_accuracy": int(state["exact_count"]) / int(state["example_count"]),
                },
            )
            for bucket, state in sorted(per_bucket.items())
        )

        exact_total = sum(int(outcome.exact_sequence_match) for outcome in outcomes)
        return RolloutEvaluation(
            exact_sequence_accuracy=exact_total / len(outcomes),
            example_count=len(outcomes),
            by_length_bucket=by_length_bucket,
            outcomes=tuple(outcomes),
        )

else:

    class Standard2DSoftmaxTransformer:  # pragma: no cover - exercised only without torch
        def __init__(self, config: SoftmaxBaselineConfig) -> None:
            require_torch()


    def causal_language_model_loss(logits, targets):  # pragma: no cover - exercised only without torch
        require_torch()


    def default_baseline_device(preferred: str | None = None):  # pragma: no cover - exercised only without torch
        require_torch()


    def evaluate_teacher_forced_model(model, examples, *, device: str | None = None):  # pragma: no cover
        require_torch()


    def train_teacher_forced_baseline(
        train_examples,
        *,
        model_config: SoftmaxBaselineConfig,
        training_config: SoftmaxTrainingConfig | None = None,
        eval_examples=(),
    ):  # pragma: no cover - exercised only without torch
        require_torch()


    def greedy_rollout(
        model,
        example: EncodedTraceExample,
        *,
        device: str | None = None,
        eos_token_id: int,
        max_total_tokens: int | None = None,
    ):  # pragma: no cover - exercised only without torch
        require_torch()


    def evaluate_free_running_rollout(
        model,
        examples,
        *,
        vocabulary: TraceVocabulary,
        device: str | None = None,
        max_total_tokens: int | None = None,
    ):  # pragma: no cover - exercised only without torch
        require_torch()
