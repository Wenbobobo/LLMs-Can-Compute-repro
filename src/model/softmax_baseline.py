"""Standard 2D-head softmax baseline scaffolding for M5."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable, Sequence

from exec_trace import Program, TraceEvent, TraceInterpreter

try:  # pragma: no cover - exercised only when torch is installed
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - exercised in environments without torch
    torch = None
    nn = None
    F = None


SPECIAL_TOKENS = ("<pad>", "<bos>", "<instructions>", "<trace>", "<event>", "<eos>")


@dataclass(frozen=True, slots=True)
class TraceSequenceExample:
    program_name: str
    program_steps: int
    tokens: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TraceSequenceStats:
    example_count: int
    vocab_size: int
    min_length: int
    max_length: int
    mean_length: float


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
    def from_examples(cls, examples: Sequence[TraceSequenceExample]) -> "TraceVocabulary":
        tokens: list[str] = list(SPECIAL_TOKENS)
        for example in examples:
            tokens.extend(example.tokens)
        return cls(tokens)

    def __len__(self) -> int:
        return len(self._id_to_token)

    def encode(self, tokens: Sequence[str]) -> tuple[int, ...]:
        return tuple(self._token_to_id[token] for token in tokens)

    def decode(self, ids: Sequence[int]) -> tuple[str, ...]:
        return tuple(self._id_to_token[index] for index in ids)


def require_torch() -> None:
    if torch is None:
        raise RuntimeError(
            "PyTorch is not installed. Install it explicitly for M5, for example via an "
            "optional dependency group before running the softmax baseline."
        )


def serialize_instruction_tokens(program: Program) -> tuple[str, ...]:
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


def serialize_event_tokens(event: TraceEvent) -> tuple[str, ...]:
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


def build_trace_sequence(program: Program, *, interpreter: TraceInterpreter | None = None) -> TraceSequenceExample:
    interpreter = interpreter or TraceInterpreter()
    result = interpreter.run(program)

    tokens: list[str] = ["<bos>", *serialize_instruction_tokens(program), "<trace>"]
    for event in result.events:
        tokens.extend(serialize_event_tokens(event))
    tokens.append("<eos>")

    return TraceSequenceExample(
        program_name=program.name,
        program_steps=result.final_state.steps,
        tokens=tuple(tokens),
    )


def build_trace_sequences(
    programs: Iterable[Program],
    *,
    interpreter: TraceInterpreter | None = None,
) -> tuple[TraceSequenceExample, ...]:
    interpreter = interpreter or TraceInterpreter()
    return tuple(build_trace_sequence(program, interpreter=interpreter) for program in programs)


def summarize_trace_sequences(examples: Sequence[TraceSequenceExample]) -> TraceSequenceStats:
    lengths = [len(example.tokens) for example in examples]
    vocab = TraceVocabulary.from_examples(examples)
    return TraceSequenceStats(
        example_count=len(examples),
        vocab_size=len(vocab),
        min_length=min(lengths) if lengths else 0,
        max_length=max(lengths) if lengths else 0,
        mean_length=mean(lengths) if lengths else 0.0,
    )


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
        return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))

else:

    class Standard2DSoftmaxTransformer:  # pragma: no cover - exercised only without torch
        def __init__(self, config: SoftmaxBaselineConfig) -> None:
            require_torch()


    def causal_language_model_loss(logits, targets):  # pragma: no cover - exercised only without torch
        require_torch()
