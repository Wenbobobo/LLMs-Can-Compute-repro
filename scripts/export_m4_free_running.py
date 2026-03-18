"""Export free-running M4 executor evaluations."""

from __future__ import annotations

import json
from pathlib import Path

from exec_trace import (
    countdown_program,
    dynamic_memory_program,
    equality_branch_program,
    latest_write_program,
    memory_accumulator_program,
)
from model import (
    build_countdown_stack_samples,
    evaluate_free_running_programs,
    fit_scorer,
    run_free_running_exact,
    run_free_running_with_stack_scorer,
)


def encode_evaluation(evaluation):
    return {
        "exact_trace_accuracy": evaluation.exact_trace_accuracy,
        "exact_final_state_accuracy": evaluation.exact_final_state_accuracy,
        "program_count": evaluation.program_count,
        "by_length_bucket": [
            {"bucket": bucket, **metrics} for bucket, metrics in evaluation.by_length_bucket
        ],
        "outcomes": [
            {
                "program_name": outcome.program_name,
                "program_steps": outcome.program_steps,
                "exact_trace_match": outcome.exact_trace_match,
                "exact_final_state_match": outcome.exact_final_state_match,
                "first_mismatch_step": outcome.first_mismatch_step,
                "failure_reason": outcome.failure_reason,
            }
            for outcome in evaluation.outcomes
        ],
    }


def main() -> None:
    countdown_train = [countdown_program(start) for start in range(0, 7)]
    countdown_heldout = [countdown_program(start) for start in range(7, 21)]
    branch_programs = [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        equality_branch_program(5, 5),
        equality_branch_program(2, 9),
    ]
    memory_programs = [
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_memory_program(),
    ]

    fit = fit_scorer(build_countdown_stack_samples(range(0, 7)))

    output = {
        "experiment": "m4_free_running_executor",
        "notes": [
            "Exact executors carry only step-local summaries such as PC and stack depth; value state is recovered via latest-write retrieval.",
            "The trainable branch only replaces stack-slot reads with the fitted scorer. Memory reads remain exact in this checkpoint.",
        ],
        "trainable_stack_scorer": {
            "quadratic_scale": fit.scorer.quadratic_scale,
            "time_scale": fit.scorer.time_scale,
            "fit_train_sample_accuracy": fit.train_sample_accuracy,
            "fit_train_exact_program_accuracy": fit.train_exact_program_accuracy,
        },
        "evaluations": {
            "exact_linear": {
                "countdown_train": encode_evaluation(
                    evaluate_free_running_programs(
                        countdown_train,
                        lambda program: run_free_running_exact(program, decode_mode="linear"),
                    )
                ),
                "countdown_heldout": encode_evaluation(
                    evaluate_free_running_programs(
                        countdown_heldout,
                        lambda program: run_free_running_exact(program, decode_mode="linear"),
                    )
                ),
                "branch_programs": encode_evaluation(
                    evaluate_free_running_programs(
                        branch_programs,
                        lambda program: run_free_running_exact(program, decode_mode="linear"),
                    )
                ),
                "memory_programs": encode_evaluation(
                    evaluate_free_running_programs(
                        memory_programs,
                        lambda program: run_free_running_exact(program, decode_mode="linear"),
                    )
                ),
            },
            "exact_accelerated": {
                "countdown_train": encode_evaluation(
                    evaluate_free_running_programs(
                        countdown_train,
                        lambda program: run_free_running_exact(program, decode_mode="accelerated"),
                    )
                ),
                "countdown_heldout": encode_evaluation(
                    evaluate_free_running_programs(
                        countdown_heldout,
                        lambda program: run_free_running_exact(program, decode_mode="accelerated"),
                    )
                ),
                "branch_programs": encode_evaluation(
                    evaluate_free_running_programs(
                        branch_programs,
                        lambda program: run_free_running_exact(program, decode_mode="accelerated"),
                    )
                ),
                "memory_programs": encode_evaluation(
                    evaluate_free_running_programs(
                        memory_programs,
                        lambda program: run_free_running_exact(program, decode_mode="accelerated"),
                    )
                ),
            },
            "trainable_stack": {
                "countdown_train": encode_evaluation(
                    evaluate_free_running_programs(
                        countdown_train,
                        lambda program: run_free_running_with_stack_scorer(program, fit.scorer),
                    )
                ),
                "countdown_heldout": encode_evaluation(
                    evaluate_free_running_programs(
                        countdown_heldout,
                        lambda program: run_free_running_with_stack_scorer(program, fit.scorer),
                    )
                ),
                "branch_programs": encode_evaluation(
                    evaluate_free_running_programs(
                        branch_programs,
                        lambda program: run_free_running_with_stack_scorer(program, fit.scorer),
                    )
                ),
                "memory_programs": encode_evaluation(
                    evaluate_free_running_programs(
                        memory_programs,
                        lambda program: run_free_running_with_stack_scorer(program, fit.scorer),
                    )
                ),
            },
        },
    }

    out_path = Path("results/M4_exact_hardmax_model/free_running_executor.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
