from __future__ import annotations

import importlib.util

import pytest

from exec_trace import countdown_program, dynamic_memory_program
from model.softmax_baseline import (
    build_trace_sequence,
    build_trace_sequences,
    require_torch,
    serialize_event_tokens,
    summarize_trace_sequences,
    TraceVocabulary,
)


def test_build_trace_sequence_contains_instruction_and_trace_markers() -> None:
    example = build_trace_sequence(countdown_program(3))

    assert example.tokens[0] == "<bos>"
    assert "<instructions>" in example.tokens
    assert "<trace>" in example.tokens
    assert example.tokens[-1] == "<eos>"


def test_trace_vocabulary_roundtrips_tokens() -> None:
    examples = build_trace_sequences((countdown_program(2), dynamic_memory_program()))
    vocabulary = TraceVocabulary.from_examples(examples)
    encoded = vocabulary.encode(examples[0].tokens[:12])

    assert vocabulary.decode(encoded) == examples[0].tokens[:12]
    assert len(vocabulary) >= len(set(examples[0].tokens[:12]))


def test_trace_sequence_summary_reports_lengths_and_vocab() -> None:
    examples = build_trace_sequences((countdown_program(2), countdown_program(5)))
    stats = summarize_trace_sequences(examples)

    assert stats.example_count == 2
    assert stats.max_length >= stats.min_length > 0
    assert stats.vocab_size > 0


def test_event_serialization_captures_memory_annotations() -> None:
    example = build_trace_sequence(dynamic_memory_program())
    memory_write_tokens = [token for token in example.tokens if token.startswith("memory_write=")]

    assert any(token != "memory_write=none" for token in memory_write_tokens)


def test_require_torch_matches_environment() -> None:
    torch_present = importlib.util.find_spec("torch") is not None
    if torch_present:
        require_torch()
    else:
        with pytest.raises(RuntimeError):
            require_torch()
