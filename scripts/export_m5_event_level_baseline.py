"""Train and export the event-level softmax baseline for M5."""

from __future__ import annotations

import json
from pathlib import Path

from exec_trace import (
    countdown_program,
    dynamic_memory_transfer_program,
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
    train_event_level_softmax_baseline,
)
from utils import detect_runtime_environment


def encode_metrics(metrics):
    return {
        "loss": metrics.loss,
        "exact_label_accuracy": metrics.exact_label_accuracy,
        "example_count": metrics.example_count,
        "head_accuracies": [{"head": head, "accuracy": accuracy} for head, accuracy in metrics.head_accuracies],
    }


def encode_rollout(evaluation):
    return {
        "exact_trace_accuracy": evaluation.exact_trace_accuracy,
        "exact_final_state_accuracy": evaluation.exact_final_state_accuracy,
        "program_count": evaluation.program_count,
        "by_length_bucket": [{"bucket": bucket, **metrics} for bucket, metrics in evaluation.by_length_bucket],
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


def rollout_budget(program) -> int:
    return max(128, len(program.instructions) * 16)


def main() -> None:
    environment = detect_runtime_environment()
    model_config = FactorizedEventModelConfig(
        d_model=36,
        n_heads=18,
        n_layers=7,
        d_ffn=36,
        opcode_dim=8,
        history_window=16,
        max_scalar=256,
        max_address=1024,
        max_pc=128,
        include_top_values=False,
    )
    training_config = FactorizedEventTrainingConfig(
        epochs=24,
        batch_size=8,
        learning_rate=5e-3,
    )

    train_programs = [countdown_program(start) for start in range(0, 7)] + [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        latest_write_program(),
        memory_accumulator_program(),
        loop_indirect_memory_program(2),
        loop_indirect_memory_program(4),
        stack_memory_ping_pong_program(),
    ]
    heldout_programs = [countdown_program(start) for start in range(7, 11)] + [
        equality_branch_program(5, 5),
        equality_branch_program(2, 9),
        dynamic_memory_transfer_program(),
        loop_indirect_memory_program(6),
        stack_memory_ping_pong_program(base_address=32),
    ]

    output = {
        "experiment": "m5_event_level_baseline",
        "environment": environment.as_dict(),
        "notes": [
            "This baseline drops the flat token trace and trains a standard softmax event-level transformer on the same factorized event targets as the richer M4 branch.",
            "The model sees instruction context and recent event history but not the direct top-of-stack summary that the contextual M4 decoder receives.",
            "This is the last architecture-side baseline intervention before freezing M5 if rollout remains uninformative.",
        ],
    }

    run = train_event_level_softmax_baseline(
        train_programs,
        eval_programs=heldout_programs,
        model_config=model_config,
        training_config=training_config,
    )
    output["status"] = "completed"
    output["model_config"] = {
        "d_model": model_config.d_model,
        "n_heads": model_config.n_heads,
        "n_layers": model_config.n_layers,
        "d_ffn": model_config.d_ffn,
        "opcode_dim": model_config.opcode_dim,
        "history_window": model_config.history_window,
        "max_scalar": model_config.max_scalar,
        "max_address": model_config.max_address,
        "max_pc": model_config.max_pc,
        "include_top_values": model_config.include_top_values,
    }
    output["training_config"] = {
        "epochs": training_config.epochs,
        "batch_size": training_config.batch_size,
        "learning_rate": training_config.learning_rate,
        "weight_decay": training_config.weight_decay,
    }
    output["train_metrics"] = encode_metrics(run.train_metrics)
    output["eval_metrics"] = None if run.eval_metrics is None else encode_metrics(run.eval_metrics)
    output["history"] = [
        {
            "epoch": epoch.epoch,
            "train_loss": epoch.train_loss,
            "eval_loss": epoch.eval_loss,
        }
        for epoch in run.history
    ]
    output["teacher_forced_groups"] = {
        "train_programs": encode_metrics(
            evaluate_factorized_event_model(
                run.model,
                run.codec,
                run.codec.build_examples(train_programs),
                device=run.device,
                include_top_values=False,
            )
        ),
        "heldout_programs": encode_metrics(
            evaluate_factorized_event_model(
                run.model,
                run.codec,
                run.codec.build_examples(heldout_programs),
                device=run.device,
                include_top_values=False,
            )
        ),
    }
    output["rollout"] = {
        "train_programs": encode_rollout(
            evaluate_free_running_programs(
                train_programs,
                lambda program: run_free_running_with_event_softmax_baseline(
                    program,
                    run,
                    decode_mode="accelerated",
                    max_steps=rollout_budget(program),
                ),
            )
        ),
        "heldout_programs": encode_rollout(
            evaluate_free_running_programs(
                heldout_programs,
                lambda program: run_free_running_with_event_softmax_baseline(
                    program,
                    run,
                    decode_mode="accelerated",
                    max_steps=rollout_budget(program),
                ),
            )
        ),
    }

    out_path = Path("results/M5_event_level_baseline/training_run.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
