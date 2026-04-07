# 2026-03-23 Post-H33 R39 Origin-Core Substrate Question Design

## Summary

`H33_post_h32_conditional_next_question_packet` selects exactly one justified
post-`H32` runtime candidate:

- `R39_origin_compiler_control_surface_dependency_audit`

`R39` is still narrow. It is not a broader compiled-family extension, a new
substrate lane, or a scope-lift packet. Its only scientific job is to test the
remaining Origin-core question left open by `R38/H32`:

how much of the current compiled exactness depends on compiler-side
control-surface structuring versus the current append-only / exact-retrieval /
small-VM substrate itself?

## Why This Is The Next Question

After `R38/H32`, the strongest positive claim is still narrow:

1. append-only traces;
2. exact retrieval over those traces;
3. a small exact executor;
4. one tiny compiled family plus one richer same-opcode control/call family.

The main unresolved risk is no longer "can one more family run?" The main
unresolved risk is whether the current compiled result is still mostly a
compiler-shaped convenience path. `R39` is justified only because `H33`
chooses that exact question explicitly instead of widening by momentum.

## Lane Contract

`R39` must stay on the current Origin-core substrate.

Required invariants:

- same opcode surface as `R37` and `R38`;
- same admitted extension row and same named same-family boundary probe from
  `H31/R38`;
- no new opcode;
- no new hidden host evaluator;
- no new program-family breadth;
- no arbitrary `C`, broader Wasm rhetoric, or "LLMs are computers" framing;
- no reopening of `R29`, `F3`, or frontier/demo widening.

`H32` remains the active routing/refreeze packet until `R39` is actually
executed and a later explicit packet decides what its result means.

## Recommended Audit Shape

`R39` should stay small and comparator-driven.

Minimum case set:

- primary admitted case:
  `subroutine_braid_program(6, base_address=80)`;
- primary same-family boundary probe:
  `subroutine_braid_long_program(12, base_address=160)`;
- optional calibration rows, if needed, must come only from the already
  admitted `R37/R38` inventory rather than a new family.

Minimum comparator structure:

1. current `R38` lowering/execution path as the baseline;
2. one semantics-preserving control-surface perturbation that stays within the
   current verifier and opcode contract;
3. at most one additional semantics-preserving comparator if the first
   perturbation is too weak to test the hypothesis cleanly.

The perturbation must be predeclared before execution. It must target
compiler-side control-surface dependence, not introduce a different runtime.

## Required Outputs

If executed, `R39` should export:

- exact trace equality and exact final-state equality separately;
- verifier/spec parity and lowering parity separately;
- one dependency-audit summary that explains whether the baseline exactness
  survives the declared perturbation;
- explicit failure localization if the perturbation breaks exactness.

## Stop Rules

Stop and do not widen if any of the following happens:

- the only viable perturbation needs a new opcode;
- the only viable perturbation needs a hidden host-side semantic shortcut;
- the comparator set starts drifting into a new family rather than a same-row
  audit;
- the lane cannot state a fixed success/failure criterion before execution.

In those cases, preserve `H33` as a useful narrowing packet and freeze the
compiled-boundary line complete-for-now instead of forcing a weak `R39`.

## Save Rule

Save this design before any `R39` runtime work.

- execute on a clean worktree derived from the current `H33`-aligned branch;
- keep commits small and packet-scoped;
- if parallel work is used, isolate write ownership per file set;
- do not merge back into dirty `main` or dirty historical branches by
  momentum.
