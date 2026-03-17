"""Export the narrow trainable latest-write M4 experiment."""

from __future__ import annotations

import json
from pathlib import Path

from model import (
    build_countdown_stack_samples,
    build_dynamic_memory_stack_samples,
    evaluate_scorer,
    fit_scorer,
)

TRAIN_STARTS = tuple(range(0, 7))
HELDOUT_STARTS = tuple(range(7, 21))


def encode_evaluation(evaluation):
    return {
        "sample_accuracy": evaluation.sample_accuracy,
        "exact_program_accuracy": evaluation.exact_program_accuracy,
        "program_count": evaluation.program_count,
        "sample_count": evaluation.sample_count,
        "by_length_bucket": [
            {"bucket": bucket, **metrics} for bucket, metrics in evaluation.by_length_bucket
        ],
    }


def main() -> None:
    train_samples = build_countdown_stack_samples(TRAIN_STARTS)
    heldout_samples = build_countdown_stack_samples(HELDOUT_STARTS)
    dynamic_memory_samples = build_dynamic_memory_stack_samples()

    fit_result = fit_scorer(train_samples)

    output = {
        "experiment": "trainable_stack_latest_write",
        "scope": {
            "description": (
                "Fit a two-parameter latest-write scorer on short countdown stack traces, "
                "then evaluate on longer countdown traces and a dynamic-memory stack trace."
            ),
            "train_starts": list(TRAIN_STARTS),
            "heldout_starts": list(HELDOUT_STARTS),
            "notes": [
                "This is a discriminative scorer over reference-generated candidate sets.",
                "It is not yet a token-level learned decoder or free-running generative model.",
            ],
        },
        "best_scorer": {
            "quadratic_scale": fit_result.scorer.quadratic_scale,
            "time_scale": fit_result.scorer.time_scale,
        },
        "fit_summary": {
            "train_sample_accuracy": fit_result.train_sample_accuracy,
            "train_exact_program_accuracy": fit_result.train_exact_program_accuracy,
        },
        "evaluations": {
            "train_countdown": encode_evaluation(evaluate_scorer(fit_result.scorer, train_samples)),
            "heldout_countdown": encode_evaluation(evaluate_scorer(fit_result.scorer, heldout_samples)),
            "dynamic_memory_stack": encode_evaluation(
                evaluate_scorer(fit_result.scorer, dynamic_memory_samples)
            ),
        },
    }

    out_path = Path("results/M4_exact_hardmax_model/trainable_stack_latest_write.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
