from __future__ import annotations

import importlib.util

import pytest

from exec_trace import (
    countdown_program,
    dynamic_latest_write_program,
    equality_branch_program,
    latest_write_program,
    loop_indirect_memory_program,
    memory_accumulator_program,
    stack_memory_ping_pong_program,
)
from model import (
    evaluate_factorized_event_model,
    evaluate_free_running_programs,
    FactorizedEventModelConfig,
    FactorizedEventTrainingConfig,
    run_free_running_with_event_softmax_baseline,
    run_free_running_with_factorized_event_model,
    train_event_level_softmax_baseline,
    train_factorized_event_model,
)


def test_factorized_event_codec_builds_examples_with_recent_history() -> None:
    train_programs = (
        countdown_program(2),
        latest_write_program(),
        stack_memory_ping_pong_program(),
    )
    from model import FactorizedEventCodec

    codec = FactorizedEventCodec(FactorizedEventModelConfig(history_window=4))
    examples = codec.build_examples(train_programs)

    assert len(examples) > 0
    assert any(example.context.recent_history for example in examples[1:])
    assert all(example.label.next_pc >= 0 for example in examples)


@pytest.mark.skipif(importlib.util.find_spec("torch") is None, reason="torch is not installed")
def test_contextual_factorized_event_model_fits_training_programs() -> None:
    train_programs = [countdown_program(start) for start in range(0, 5)] + [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_latest_write_program(),
        loop_indirect_memory_program(2),
    ]
    model_config = FactorizedEventModelConfig(
        d_model=48,
        n_heads=4,
        n_layers=2,
        d_ffn=96,
        opcode_dim=12,
        history_window=8,
        max_scalar=128,
        max_address=32,
        max_pc=64,
        include_top_values=True,
    )
    training_config = FactorizedEventTrainingConfig(
        epochs=24,
        batch_size=8,
        learning_rate=5e-3,
        device="cpu",
    )

    run = train_factorized_event_model(
        train_programs,
        eval_programs=(countdown_program(5), loop_indirect_memory_program(3)),
        model_config=model_config,
        training_config=training_config,
    )
    metrics = evaluate_factorized_event_model(run.model, run.codec, run.codec.build_examples(train_programs), device="cpu")
    rollout = evaluate_free_running_programs(
        train_programs[:4],
        lambda program: run_free_running_with_factorized_event_model(program, run, decode_mode="accelerated"),
    )

    assert run.train_metrics.example_count > 0
    assert metrics.exact_label_accuracy >= 0.8
    assert rollout.program_count == 4


@pytest.mark.skipif(importlib.util.find_spec("torch") is None, reason="torch is not installed")
def test_event_level_softmax_baseline_trains_and_rolls_out() -> None:
    train_programs = [countdown_program(start) for start in range(0, 4)] + [
        equality_branch_program(0, 0),
        latest_write_program(),
        stack_memory_ping_pong_program(),
    ]
    heldout = [countdown_program(5), equality_branch_program(2, 9)]
    model_config = FactorizedEventModelConfig(
        d_model=36,
        n_heads=18,
        n_layers=2,
        d_ffn=36,
        opcode_dim=8,
        history_window=6,
        max_scalar=128,
        max_address=32,
        max_pc=64,
        include_top_values=False,
    )
    training_config = FactorizedEventTrainingConfig(
        epochs=12,
        batch_size=4,
        learning_rate=5e-3,
        device="cpu",
    )

    run = train_event_level_softmax_baseline(
        train_programs,
        eval_programs=heldout,
        model_config=model_config,
        training_config=training_config,
    )
    rollout = evaluate_free_running_programs(
        heldout,
        lambda program: run_free_running_with_event_softmax_baseline(program, run, decode_mode="accelerated"),
    )

    assert run.train_metrics.example_count > 0
    assert run.eval_metrics is not None
    assert rollout.program_count == len(heldout)
