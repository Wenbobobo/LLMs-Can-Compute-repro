"""Export a trace-dataset preview for the M5 softmax baseline."""

from __future__ import annotations

import json
from pathlib import Path

from exec_trace import countdown_program, dynamic_memory_program, equality_branch_program
from model import base_tokens_for_mode, build_trace_sequences, summarize_trace_sequences, TraceVocabulary


def main() -> None:
    programs = [
        countdown_program(0),
        countdown_program(3),
        countdown_program(8),
        equality_branch_program(2, 2),
        equality_branch_program(2, 5),
        dynamic_memory_program(),
    ]
    variants: dict[str, dict[str, object]] = {}

    for mode in ("atomic", "factorized"):
        examples = build_trace_sequences(programs, tokenization_mode=mode)
        stats = summarize_trace_sequences(examples, base_tokens=base_tokens_for_mode(mode))
        vocabulary = TraceVocabulary.from_examples(examples, base_tokens=base_tokens_for_mode(mode))
        variants[mode] = {
            "stats": {
                "example_count": stats.example_count,
                "vocab_size": stats.vocab_size,
                "min_length": stats.min_length,
                "max_length": stats.max_length,
                "mean_length": stats.mean_length,
            },
            "preview_examples": [
                {
                    "program_name": example.program_name,
                    "program_steps": example.program_steps,
                    "token_count": len(example.tokens),
                    "first_tokens": list(example.tokens[:64]),
                    "first_token_ids": list(vocabulary.encode(example.tokens[:64])),
                }
                for example in examples
            ],
        }

    output = {
        "experiment": "m5_trace_dataset_preview",
        "variants": variants,
    }

    out_path = Path("results/M5_standard_2d_baseline/dataset_preview.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()
