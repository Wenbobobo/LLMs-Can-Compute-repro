# Status

## Working State

- M0 scaffold: complete
- M1 claims/scope docs: complete
- M2 geometry exactness: initial implementation added
- M3 trace executor: stack plus bounded-RAM reference semantics implemented
- M4 exact hard-max decode: deterministic latest-write bridge implemented for immediate and dynamic memory addressing plus stack-slot retrieval
- M4 narrow trainable slice: two-parameter stack latest-write scorer fitted and validated on held-out longer traces
- M4 free-running exact executor: linear and accelerated online rollout now match the reference trace on current countdown, branch, and bounded-RAM programs
- M4 induced causal executor: structured transition rules fitted from reference traces now generate exact online events on held-out countdown, branch, and indirect-memory programs
- M4 neural event executor: a trainable structured-event decoder now learns opcode-conditioned transition labels and reaches exact rollout on current held-out countdown, branch, and memory families
- M4 finite-precision stress: scheme-aware address-range failure sweeps now compare single-head, radix-2, and block-recentered latest-write addressing
- M4 factorized event decoder: a richer direct event-value decoder now trains on recent event history plus top-of-stack summaries; it reaches moderate teacher-forced label accuracy but still collapses in free-running rollout
- M4 real-trace precision: offset real-trace checks now confirm that single-head finite-precision failures reappear on real memory streams, while the current radix/block schemes recover the current offset suite
- M4 staged pointer decoder: candidate-source labels plus staged decode masks now run in three regimes. On the exported train/held-out slice, structural exact-trace rollout is `0.1875 / 0.0`, `opcode_shape` is `0.875 / 0.5455`, and `opcode_legal` is `1.0 / 1.0`
- M4 staged pointer coverage: the staged export now includes the harder `alternating_memory_loop` family in both train and held-out groups, reducing the risk that the bridge result only fits the easier loop/ping-pong slice
- M4 mask dependence / executor gap: the broader `M4-D` suite adds `flagged_indirect_accumulator` and `selector_checkpoint_bank`; held-out `opcode_shape` collapses to `0.0`, `opcode_legal` remains exact, and the cleaned failure taxonomy splits between `push_expr_0` memory-value mismatches (`8/15`) and `step_budget` nontermination (`7/15`), so no fourth regime is justified
- M4 failure provenance: the follow-up provenance export now recovers first semantic divergence before staged runtime failure; on held-out `opcode_shape`, the prior `7/15` `step_budget` rows are all downstream nontermination after an earlier semantic mistake, while the remaining `8/15` failures stay direct `push_expr_0` memory-value root causes
- M4 real-trace horizon/base sweep: float32 single-head now fails earlier when the same real streams are evaluated under inflated horizons; `alternating_offset_256_memory` first fails at `16x`, `alternating_offset_2048_memory` fails at `1x`, and `radix2`/`block_recentered` with base `64` stay stable through the exported `64x` sweep on the current offset suite
- M4 precision generalization: new high-address memory families (`hotspot_memory_rewrite`, `flagged_indirect_accumulator`, `selector_checkpoint_bank`) all fail at `1x` under float32 single-head; `stack_fanout_sum_64` stays stable, while `stack_fanout_sum_256` first fails at `4x`, and observed failure type remains `tie_collapse`
- M4 precision organic traces: the broadened `M4-E` evidence is now re-indexed into a dedicated organic-trace artifact bundle with explicit `C3e` claim-impact metadata
- M5 scaffold: structured trace dataset, vocabulary helpers, optional Torch baseline definition, and dataset preview artifact added
- M5 CUDA baseline run: first teacher-forced training run completed on the tiny 2D-head softmax model, with nontrivial teacher-forced accuracy but zero exact free-running rollout on current eval groups
- M5 representation ablation: atomic whole-token vs factorized digit-level vs event-grouped serializations now run side by side; event grouping reduces sequence length and improves held-out teacher-forced accuracy slightly, but exact rollout still remains zero
- M5 event-level baseline: the final standard softmax baseline now shares the factorized event target with the richer M4 branch; it remains a stronger negative control with near-zero exact-label accuracy and zero exact rollout
- M5 pointer baseline: the final narrow repair now shares the staged pointer label space with `M4` and the harder alternating-memory family; it still records exact-label accuracy `0.0 / 0.0`, held-out structural rollout `0.0`, and held-out `opcode_shape` rollout `0.0`, while `opcode_legal` exactness remains diagnostic only
- M6 frontend boundary is fixed at the spec level to a tiny typed bytecode, and the first control-flow-first widening is implemented as static-target non-recursive `call` / `ret`
- M6 typed bytecode harness: the widened verifier / lowering / differential-harness batch now exists under `src/bytecode/`; the exported suite contains `22` passing verifier rows, `7` deterministic verifier failures, `16` short/medium exact-trace matches, and `6` long exact-final-state matches
- M6 memory surface follow-up: program-level `frame`/`heap` layouts, a separate memory-surface verifier, and call-boundary dumps now exist under `src/bytecode/`; the first follow-up export covers `6` annotated programs and `2` negative controls, with `6/6` memory-surface matches between bytecode reference execution and the lowered path
- M6 stress/reference follow-up: a standalone Python spec oracle plus one branch-selected helper checkpoint braid family now exist under `src/bytecode/`; the exported bundle records `2` medium exact-trace positives, `1` long exact-final-state positive, `2` matched negatives, and `3/3` companion memory-surface matches
- Publication ledgers now reserve claim-ladder, figure, manifest, and threat-tracking space for unattended runs
- Publication bundle status now tracks which mandatory figures/tables are ready, blocked, partial, or still missing inputs
- P1 paper readiness: the paper bundle now has rendered `M4` taxonomy and precision-boundary figures, a rendered `M6` frontend-boundary diagram, and a markdown layout for the initial exact-trace / final-state table, all derived from the live `P1` source exports
- P2 public packaging: the release ledger now includes the `M6` typed-bytecode, memory-surface, and stress/reference bundles with Python `3.12` + `uv` regeneration commands
- P3 paper freeze: a machine-readable claim/artifact/unsupported-claim bundle now exists under `results/P3_paper_freeze_and_evidence_mapping/`
- R1 precision closure: a unified boundary bundle now exists under `results/R1_precision_mechanism_closure/`, summarizing `12/25` tracked single-head failure streams and the current decomposition boundary
- R2 systems gate: the first explicit systems baseline now exists under `results/R2_systems_baseline_gate/`; geometry remains strongly positive, but the lowered `exec_trace` path is not yet end-to-end competitive on the current positive `D0` suites
- M7 frontend candidate decision: `results/M7_frontend_candidate_decision/` now records the explicit no-go outcome — stay on tiny typed bytecode, do not widen the frontend on current evidence
- P4 blog release gate: `results/P4_blog_release_gate/` now records the outward-release audit — README may stay restrained, but the blog remains blocked
- H0 release hygiene: `results/H0_repo_consolidation_and_release_hygiene/` now records the clean-worktree checkpoint after the split was applied, with zero blocked public-surface checks
- Runtime environment export: Python `3.12.9`, `torch==2.10.0+cu128`, and CUDA device info are recorded under `results/runtime_environment.json`
- Packaging fix: renamed the trace package to avoid the Python stdlib conflict
- Public GitHub repo created and initial push completed

## Immediate Next Actions

1. Start the paper lane in the dedicated `paper` worktree and turn the frozen claim set into a manuscript skeleton.
2. Keep `README.md`, `STATUS.md`, and `docs/publication_record/` synchronized with the completed `P3` → `P4` gate chain and its unsupported-claim ledger.
3. Reopen `R1` or `R2` only if the project deliberately wants a stronger systems or precision case; otherwise keep the current `D0` endpoint fixed.
4. Treat any future frontend widening as a fresh scope change that must satisfy the `M7` revisit prerequisites before implementation starts.
5. Keep the blog blocked and the README restrained unless a future widened-scope batch clears both the systems and public-release gates.

## Known Blockers

- Broader compiled-demo work remains blocked by the completed `M7` no-go decision: the current tiny typed-bytecode `D0` slice is the endpoint on present evidence.
- Broader outward narrative remains blocked by the completed `P4` gate: README is acceptable, but a blog would currently outrun the claim/evidence bundle.
- Public release hygiene itself is no longer a blocker on `main`; the remaining operational question is what to build next inside the now-separated worktrees.
- Scientific uncertainty remains concentrated in three places: precision closure on longer organic/real traces, the system-level baseline story for specialized retrieval/runtime choices, and the discipline required to keep staged-pointer / typed-bytecode results from being overstated.
