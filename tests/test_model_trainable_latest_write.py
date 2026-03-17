from __future__ import annotations

from model.trainable_latest_write import (
    build_countdown_stack_samples,
    build_dynamic_memory_stack_samples,
    evaluate_scorer,
    fit_scorer,
)


def test_trainable_scorer_fits_countdown_stack_training_slice() -> None:
    train_samples = build_countdown_stack_samples(range(0, 7))
    fit = fit_scorer(train_samples)

    assert fit.train_sample_accuracy == 1.0
    assert fit.train_exact_program_accuracy == 1.0


def test_trainable_scorer_generalizes_to_longer_countdowns() -> None:
    train_samples = build_countdown_stack_samples(range(0, 7))
    eval_samples = build_countdown_stack_samples(range(7, 21))

    fit = fit_scorer(train_samples)
    evaluation = evaluate_scorer(fit.scorer, eval_samples)

    assert evaluation.sample_accuracy == 1.0
    assert evaluation.exact_program_accuracy == 1.0
    assert any(name == "steps>=49" for name, _ in evaluation.by_length_bucket)


def test_trainable_scorer_transfers_to_dynamic_memory_stack_trace() -> None:
    train_samples = build_countdown_stack_samples(range(0, 7))
    fit = fit_scorer(train_samples)

    dynamic_samples = build_dynamic_memory_stack_samples()
    evaluation = evaluate_scorer(fit.scorer, dynamic_samples)

    assert evaluation.sample_accuracy == 1.0
    assert evaluation.exact_program_accuracy == 1.0
