# M5 Factorized Tokenization Design

## Goal

Run the first representation ablation that can separate two failure modes in the
softmax baseline:

- failure from unstable whole-token numeric serialization and union-vocabulary
  leakage,
- versus failure from the model/runtime itself under long structured rollout.

## Decision

Keep the tiny 2D-head softmax model fixed and compare two serialization modes:

1. `atomic_union_vocab`
   Keep the original whole-token serialization such as `step=17` and
   `memory_write=2:9`. Build the vocabulary from train plus eval traces so the
   branch does not fail purely because of OOV tokens.
2. `factorized_train_vocab`
   Serialize the same structure with stable field tokens and digit-level integer
   pieces. Build the vocabulary from train traces plus fixed base tokens only.

This isolates the representation question without also changing model size or
training objective.

## Expected Readout

- If factorization materially improves exact rollout, then the previous failure
  was mainly a representation/vocabulary issue.
- If factorization improves teacher-forced metrics or delays first error but
  rollout stays at zero, then representation matters but is not the whole
  problem.
- If factorization does nothing, then the next move should shift toward model
  architecture, prompt boundary, or rollout strategy.

## Chosen Output

Record both variants in one artifact:

- dataset stats,
- vocabulary size,
- max sequence length,
- teacher-forced train/eval metrics,
- free-running exact rollout by program family,
- first-error position and failure mode.

This keeps the branch data-driven and directly comparable against the current
`M4` exact-rollout results.
