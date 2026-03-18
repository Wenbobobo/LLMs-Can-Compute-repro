"""Train and export the first runnable M5 softmax-baseline checkpoint."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from exec_trace import (
    countdown_program,
    dynamic_latest_write_program,
    dynamic_memory_program,
    dynamic_memory_transfer_program,
    equality_branch_program,
    latest_write_program,
    memory_accumulator_program,
)
from model import (
    base_tokens_for_mode,
    build_trace_sequences,
    default_baseline_device,
    encode_trace_examples,
    evaluate_free_running_rollout,
    evaluate_teacher_forced_model,
    require_torch,
    SoftmaxBaselineConfig,
    SoftmaxTrainingConfig,
    summarize_trace_sequences,
    train_teacher_forced_baseline,
    TraceVocabulary,
)
from utils import detect_runtime_environment


def encode_teacher_forced(metrics):
    return {
        "loss": metrics.loss,
        "token_accuracy": metrics.token_accuracy,
        "example_count": metrics.example_count,
        "token_count": metrics.token_count,
        "by_length_bucket": [
            {"bucket": bucket, **bucket_metrics} for bucket, bucket_metrics in metrics.by_length_bucket
        ],
    }


def encode_rollout(metrics):
    return {
        "exact_sequence_accuracy": metrics.exact_sequence_accuracy,
        "example_count": metrics.example_count,
        "by_length_bucket": [
            {"bucket": bucket, **bucket_metrics} for bucket, bucket_metrics in metrics.by_length_bucket
        ],
        "outcomes": [
            {
                "program_name": outcome.program_name,
                "program_steps": outcome.program_steps,
                "exact_sequence_match": outcome.exact_sequence_match,
                "first_error_token_index": outcome.first_error_token_index,
                "generated_token_count": outcome.generated_token_count,
                "failure_reason": outcome.failure_reason,
            }
            for outcome in metrics.outcomes
        ],
    }


def run_variant(
    *,
    variant_name: str,
    tokenization_mode: str,
    vocab_source: str,
    train_programs,
    countdown_eval,
    branch_eval,
    memory_eval,
    training_config: SoftmaxTrainingConfig,
) -> dict[str, object]:
    train_sequences = build_trace_sequences(train_programs, tokenization_mode=tokenization_mode)
    countdown_sequences = build_trace_sequences(countdown_eval, tokenization_mode=tokenization_mode)
    branch_sequences = build_trace_sequences(branch_eval, tokenization_mode=tokenization_mode)
    memory_sequences = build_trace_sequences(memory_eval, tokenization_mode=tokenization_mode)
    all_sequences = train_sequences + countdown_sequences + branch_sequences + memory_sequences

    if vocab_source == "train_plus_eval":
        vocabulary_examples = all_sequences
    elif vocab_source == "train_only_plus_base":
        vocabulary_examples = train_sequences
    else:
        raise ValueError(f"Unsupported vocabulary source: {vocab_source}")

    vocabulary = TraceVocabulary.from_examples(
        vocabulary_examples,
        base_tokens=base_tokens_for_mode(tokenization_mode),
    )
    encoded_train = encode_trace_examples(train_sequences, vocabulary)
    encoded_countdown = encode_trace_examples(countdown_sequences, vocabulary)
    encoded_branch = encode_trace_examples(branch_sequences, vocabulary)
    encoded_memory = encode_trace_examples(memory_sequences, vocabulary)
    encoded_eval = encoded_countdown + encoded_branch + encoded_memory

    max_seq_len = max(len(example.token_ids) for example in (encoded_train + encoded_eval)) + 8
    model_config = SoftmaxBaselineConfig(vocab_size=len(vocabulary), max_seq_len=max_seq_len)
    run = train_teacher_forced_baseline(
        encoded_train,
        model_config=model_config,
        training_config=training_config,
        eval_examples=encoded_eval,
    )

    return {
        "variant_name": variant_name,
        "tokenization_mode": tokenization_mode,
        "vocab_source": vocab_source,
        "dataset_stats": {
            "train": asdict(summarize_trace_sequences(train_sequences, base_tokens=base_tokens_for_mode(tokenization_mode))),
            "countdown_eval": asdict(summarize_trace_sequences(
                countdown_sequences,
                base_tokens=base_tokens_for_mode(tokenization_mode),
            )),
            "branch_eval": asdict(summarize_trace_sequences(
                branch_sequences,
                base_tokens=base_tokens_for_mode(tokenization_mode),
            )),
            "memory_eval": asdict(summarize_trace_sequences(
                memory_sequences,
                base_tokens=base_tokens_for_mode(tokenization_mode),
            )),
        },
        "device": run.device,
        "model_config": {
            "vocab_size": model_config.vocab_size,
            "d_model": model_config.d_model,
            "n_heads": model_config.n_heads,
            "n_layers": model_config.n_layers,
            "d_ffn": model_config.d_ffn,
            "max_seq_len": model_config.max_seq_len,
        },
        "training_config": {
            "epochs": training_config.epochs,
            "batch_size": training_config.batch_size,
            "learning_rate": training_config.learning_rate,
            "weight_decay": training_config.weight_decay,
            "seed": training_config.seed,
            "max_grad_norm": training_config.max_grad_norm,
            "requested_device": training_config.device,
            "resolved_device": default_baseline_device(training_config.device),
        },
        "train_metrics": encode_teacher_forced(run.train_metrics),
        "eval_metrics": encode_teacher_forced(run.eval_metrics) if run.eval_metrics is not None else None,
        "history": [
            {
                "epoch": epoch.epoch,
                "train_loss": epoch.train_loss,
                "eval_loss": epoch.eval_loss,
            }
            for epoch in run.history
        ],
        "group_metrics": {
            "countdown_eval_teacher_forced": encode_teacher_forced(
                evaluate_teacher_forced_model(run.model, encoded_countdown, device=run.device)
            ),
            "branch_eval_teacher_forced": encode_teacher_forced(
                evaluate_teacher_forced_model(run.model, encoded_branch, device=run.device)
            ),
            "memory_eval_teacher_forced": encode_teacher_forced(
                evaluate_teacher_forced_model(run.model, encoded_memory, device=run.device)
            ),
            "countdown_eval_rollout": encode_rollout(
                evaluate_free_running_rollout(run.model, encoded_countdown, vocabulary=vocabulary, device=run.device)
            ),
            "branch_eval_rollout": encode_rollout(
                evaluate_free_running_rollout(run.model, encoded_branch, vocabulary=vocabulary, device=run.device)
            ),
            "memory_eval_rollout": encode_rollout(
                evaluate_free_running_rollout(run.model, encoded_memory, vocabulary=vocabulary, device=run.device)
            ),
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    output = {
        "experiment": "m5_softmax_training_run",
        "environment": environment.as_dict(),
        "notes": [
            "This export now compares two representation choices under the same tiny 2D-head softmax baseline.",
            "The atomic branch keeps the original verbose whole-token serialization and still uses a train-plus-eval union vocabulary to avoid OOV failures.",
            "The factorized branch decomposes integers into stable digit-level pieces and builds its vocabulary from train-only traces plus fixed base tokens.",
        ],
    }

    try:
        require_torch()
    except RuntimeError as exc:
        output["status"] = "skipped"
        output["reason"] = str(exc)
        out_path = Path("results/M5_standard_2d_baseline/training_run.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
        print(out_path.as_posix())
        return

    train_programs = [countdown_program(start) for start in range(0, 7)] + [
        equality_branch_program(0, 0),
        equality_branch_program(0, 1),
        latest_write_program(),
        memory_accumulator_program(),
        dynamic_latest_write_program(),
    ]
    countdown_eval = [countdown_program(start) for start in range(7, 11)]
    branch_eval = [
        equality_branch_program(5, 5),
        equality_branch_program(2, 9),
    ]
    memory_eval = [
        dynamic_memory_program(),
        dynamic_memory_transfer_program(),
    ]

    output["status"] = "completed"
    output["variants"] = {
        "atomic_union_vocab": run_variant(
            variant_name="atomic_union_vocab",
            tokenization_mode="atomic",
            vocab_source="train_plus_eval",
            train_programs=train_programs,
            countdown_eval=countdown_eval,
            branch_eval=branch_eval,
            memory_eval=memory_eval,
            training_config=SoftmaxTrainingConfig(epochs=24, batch_size=4, learning_rate=5e-3),
        ),
        "factorized_train_vocab": run_variant(
            variant_name="factorized_train_vocab",
            tokenization_mode="factorized",
            vocab_source="train_only_plus_base",
            train_programs=train_programs,
            countdown_eval=countdown_eval,
            branch_eval=branch_eval,
            memory_eval=memory_eval,
            training_config=SoftmaxTrainingConfig(epochs=24, batch_size=2, learning_rate=5e-3),
        ),
    }

    out_path = Path("results/M5_standard_2d_baseline/training_run.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
