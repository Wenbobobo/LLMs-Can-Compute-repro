# 2026-03-24 Post-H49 Origin-Core Next-Wave Design

## Summary

This packet saves the post-`H49` next-wave plan without widening scope by
momentum.

`H49` already froze `R50` as narrow exact tiny-`C` support only and restored
`no_active_downstream_runtime_lane`. The next question is therefore not
"what broader useful-case demo should run next", but "how far the current
append-only exact substrate actually extends before the project should stop."

This design chooses a `substrate_first_falsification` route with four parts:

- complete one post-`H49` claim-delta bundle, `F26`;
- complete one post-`H49` cleanline hygiene packet, `P36`;
- fix exactly one next runtime candidate, `R51`;
- fix exactly one later comparator/value gate, `R52`, followed by one
  docs-only `H50` decision packet.

Broader useful-case growth, trainable-executor growth, and transformed-model
entry remain blocked until `H50` says otherwise.

## Chosen Route

The chosen route is:

`F26_post_h49_origin_claim_delta_and_next_question_bundle` ->
`P36_post_h49_cleanline_hygiene_and_artifact_policy` ->
`R51_origin_memory_control_surface_sufficiency_gate` ->
`R52_origin_internal_vs_external_executor_value_gate` ->
`H50_post_r51_r52_scope_decision_packet`.

Only if `H50` returns a positive narrow decision may the saved future bundle
`F27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle` become
relevant. `F27` is planning-only here and does not authorize execution.

## F26 Contract

`F26` must remain planning-only and must do five things:

- preserve `H49` as the active docs-only packet, `H43` as the paper-grade
  endpoint, and `H36` as the preserved routing/refreeze packet;
- map Origin claim layers `A/B/C/D` onto the landed evidence stack
  explicitly;
- identify the smallest unresolved substrate question that still changes the
  scientific conclusion materially;
- fix `R51` as the only next runtime candidate, `R52` as the only follow-on
  comparator/value gate, and `H50` as the only follow-up packet; and
- keep useful-case/trainable expansion blocked pending a positive `H50`.

## P36 Contract

`P36` remains operational/docs-only and must codify:

- clean worktree as the only scientific execution surface for this wave;
- dirty root `main` quarantine;
- explicit no-merge posture during `F26/R51/R52/H50`;
- raw-artifact default out-of-git policy, with summaries/manifests kept in git;
- commit cadence split into planning, runtime, comparator, and decision
  packets; and
- a later explicit LFS trigger only if review-critical artifacts cannot stay
  compact.

## R51 Contract

`R51` is the only next runtime candidate fixed here. It must test whether the
current substrate can extend beyond the landed tiny useful-case surface on a
strictly exact, append-only, no-hidden-side-state basis.

Required families:

- latest-write overwrite-after-gap;
- stack-relative reads under deeper control flow;
- loop-carried state;
- nested call/return;
- bounded multi-step static-memory tiny-`C` / lowered rows that materially
  increase memory/control pressure without widening into arbitrary `C`.

Required outputs:

- full-trace and final-state parity;
- per-read maximizer-row identity;
- first-fail localization;
- annotation-budget accounting; and
- one explicit lane verdict.

## R52 Contract

`R52` runs only after `R51` and only on `R51` exact rows. Its question is not
whether internal execution merely exists, but whether it retains bounded value
relative to simpler baselines.

Required comparators:

- internal exact executor with the current accelerated retrieval path;
- internal exact linear/reference path; and
- plain external interpreter/runtime.

Required outputs:

- exactness parity across comparators where applicable;
- end-to-end latency;
- retrieval-share decomposition;
- trace-length sensitivity;
- debugging/operational burden notes; and
- one explicit lane verdict.

## H50 Decision Rule

`H50` is a docs-only packet and must make one narrow decision:

- `freeze_as_narrow_specialized_executor_only`;
- `allow_planning_only_f27_entry_bundle`; or
- `stop_as_exact_without_system_value`.

`H50` must restore `no_active_downstream_runtime_lane` unless both `R51` and
`R52` are positive in the bounded sense required by this design.

## Defaults

- Do not widen into broader Wasm, arbitrary `C`, or natural-language-facing
  demos.
- Do not reopen same-endpoint `D0` lanes.
- Do not merge back to `main` during this wave.
- Treat high-quality negative results as first-class closeout evidence.
- Prefer "stop after a strong falsifier" over another broadening wave.
