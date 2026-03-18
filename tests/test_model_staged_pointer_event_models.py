from __future__ import annotations

import importlib.util

import pytest

from exec_trace import (
    alternating_memory_loop_program,
    countdown_program,
    dynamic_latest_write_program,
    equality_branch_program,
    latest_write_program,
)
from model import (
    evaluate_free_running_programs,
    FactorizedEventModelConfig,
    FactorizedEventTrainingConfig,
    PointerEventCodec,
    run_free_running_with_pointer_event_model,
    run_free_running_with_pointer_softmax_baseline,
    train_pointer_event_model,
    train_pointer_event_softmax_baseline,
)


def test_pointer_event_codec_builds_examples_from_reference_traces() -> None:
    train_programs = (
        countdown_program(2),
        equality_branch_program(1, 1),
        latest_write_program(),
    )
    codec = PointerEventCodec(FactorizedEventModelConfig(history_window=4))
    examples = codec.build_examples(train_programs)

    assert len(examples) > 0
    assert any(example.context.recent_history for example in examples[1:])
    assert all(example.label.next_pc_mode for example in examples)


@pytest.mark.skipif(importlib.util.find_spec("torch") is None, reason="torch is not installed")
def test_pointer_event_model_rolls_out_heldout_programs_with_opcode_legal_masks() -> None:
    train_programs = [countdown_program(start) for start in range(0, 5)] + [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        latest_write_program(),
        dynamic_latest_write_program(),
    ]
    heldout_programs = [countdown_program(start) for start in range(5, 8)] + [
        equality_branch_program(5, 5),
        equality_branch_program(2, 9),
    ]
    model_config = FactorizedEventModelConfig(
        d_model=48,
        n_heads=4,
        n_layers=2,
        d_ffn=96,
        opcode_dim=12,
        history_window=8,
        max_scalar=128,
        max_address=64,
        max_pc=64,
        include_top_values=True,
    )
    training_config = FactorizedEventTrainingConfig(
        epochs=16,
        batch_size=8,
        learning_rate=5e-3,
        device="cpu",
    )

    run = train_pointer_event_model(
        train_programs,
        eval_programs=heldout_programs,
        model_config=model_config,
        training_config=training_config,
    )
    structural = evaluate_free_running_programs(
        heldout_programs,
        lambda program: run_free_running_with_pointer_event_model(
            program,
            run,
            decode_mode="accelerated",
            max_steps=max(128, len(program.instructions) * 16),
            mask_mode="structural",
        ),
    )
    opcode_shape = evaluate_free_running_programs(
        heldout_programs,
        lambda program: run_free_running_with_pointer_event_model(
            program,
            run,
            decode_mode="accelerated",
            max_steps=max(128, len(program.instructions) * 16),
            mask_mode="opcode_shape",
        ),
    )
    opcode_legal = evaluate_free_running_programs(
        heldout_programs,
        lambda program: run_free_running_with_pointer_event_model(
            program,
            run,
            decode_mode="accelerated",
            max_steps=max(128, len(program.instructions) * 16),
            mask_mode="opcode_legal",
        ),
    )

    assert run.train_metrics.exact_label_accuracy >= 0.9
    assert run.eval_metrics is not None
    assert run.eval_metrics.exact_label_accuracy >= 0.9
    assert structural.exact_trace_accuracy <= opcode_shape.exact_trace_accuracy
    assert opcode_shape.exact_trace_accuracy <= opcode_legal.exact_trace_accuracy
    assert opcode_legal.exact_trace_accuracy == 1.0
    assert opcode_legal.exact_final_state_accuracy == 1.0


@pytest.mark.skipif(importlib.util.find_spec("torch") is None, reason="torch is not installed")
def test_pointer_softmax_baseline_stays_non_exact_with_structural_masks() -> None:
    train_programs = [countdown_program(start) for start in range(0, 5)] + [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        latest_write_program(),
        dynamic_latest_write_program(),
    ]
    heldout_programs = [countdown_program(start) for start in range(5, 8)] + [
        equality_branch_program(5, 5),
        equality_branch_program(2, 9),
    ]
    model_config = FactorizedEventModelConfig(
        d_model=36,
        n_heads=18,
        n_layers=7,
        d_ffn=36,
        opcode_dim=8,
        history_window=8,
        max_scalar=128,
        max_address=64,
        max_pc=64,
        include_top_values=False,
    )
    training_config = FactorizedEventTrainingConfig(
        epochs=12,
        batch_size=8,
        learning_rate=5e-3,
        device="cpu",
    )

    run = train_pointer_event_softmax_baseline(
        train_programs,
        eval_programs=heldout_programs,
        model_config=model_config,
        training_config=training_config,
    )
    rollout = evaluate_free_running_programs(
        heldout_programs,
        lambda program: run_free_running_with_pointer_softmax_baseline(
            program,
            run,
            decode_mode="accelerated",
            max_steps=max(128, len(program.instructions) * 16),
        ),
    )

    assert run.train_metrics.exact_label_accuracy < 0.8
    assert run.eval_metrics is not None
    assert rollout.exact_trace_accuracy == 0.0
    assert rollout.exact_final_state_accuracy < 1.0


def test_alternating_memory_loop_reference_program_family() -> None:
    program = alternating_memory_loop_program(5, base_address=32)

    assert program.name == "alternating_memory_loop_5_a32"
    assert len(program.instructions) == 37
