# Experiment Matrix

- Inputs:
  frozen tiny bytecode,
  current `M6` positive/negative suite,
  current memory-surface diagnostics,
  current `P1` table schema.
- Interventions:
  add one stress-family suite,
  add one external reference path,
  compare the same rows across all active oracles.
- Outputs:
  stress-family result rows,
  oracle agreement matrix,
  mismatch taxonomy,
  compiled-demo stop/go note.

Minimum planned suite:

- positives:
  `2` medium exact-trace rows with distinct helper/checkpoint paths,
  `1` long exact-final-state row;
- negatives:
  `1` control-flow or typed-branch contract violation,
  `1` memory-surface contract violation.

Current realized bundle:

- medium positives:
  `bytecode_helper_checkpoint_braid_6_a200_s0`,
  `bytecode_helper_checkpoint_braid_6_a216_s1`;
- long positive:
  `bytecode_helper_checkpoint_braid_long_18_a232_s0`;
- matched negatives:
  `invalid_helper_checkpoint_braid_branch_6_a248_s0`,
  `invalid_helper_checkpoint_braid_surface_6_a264_s1`.
