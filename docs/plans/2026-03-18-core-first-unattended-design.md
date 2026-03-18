# Core-First Unattended Next-Stage Design

> Status note (2026-03-19): superseded by the post-`M6-E` paper-first plan in
> `tmp/2026-03-18-next-stage-plan.md` and the `P3`/`R1`/`R2`/`M7`/`P4`
> milestone docs.

## Why this phase exists

The current repository has already validated the narrow execution substrate and
established three important later-stage facts:

1. staged pointer decoding can recover exact held-out rollout, but only under a
   stronger legality regime than the fair structural baseline;
2. float32 latest-write precision failures reappear on real offset traces and
   can be delayed or avoided by radix/block decomposition on the current suite;
3. the pointer-space `M5` baseline is now a cleaner negative control rather
   than a branch that still deserves open-ended rescue attempts.

That means the next unattended phase should not chase broader demos. The real
remaining work is to reduce the scientific uncertainty around those three facts
before allowing the project to move into a compiled frontend or presentation
phase.

## Scientific target

This phase continues to optimize for the narrow substrate claims:

- append-only execution traces remain the core representation of computation;
- exact retrieval over those traces remains the main mechanism under test;
- free-running exact execution remains the primary success criterion.

The phase does **not** attempt to validate arbitrary C, general LLM execution,
or flashy demo tasks. Those stay downstream of the current mechanistic
questions.

## Track summary

### Track A — `M4-D` mask dependence and executor gap

Goal: determine how much staged-pointer success comes from stronger legality
masks versus learned candidate-source prediction.

Default decisions:
- keep the current three decode regimes (`structural`, `opcode_shape`,
  `opcode_legal`) as the core comparison ladder;
- do not add new model capacity, broader training data, or new decode tricks
  before a failure taxonomy exists;
- add at least two harder held-out program families beyond the current loop /
  ping-pong slice;
- allow exactly one stronger-than-`opcode_shape` but weaker-than-`opcode_legal`
  intermediate regime **only if** most `opcode_shape` failures collapse into one
  missing compatibility family.

Exit conditions:
- positive closure: held-out `opcode_shape` improves materially on every new
  family; or
- negative closure: a stable failure taxonomy shows that exactness still relies
  on stronger legality constraints.

### Track B — `M4-E` precision generalization and failure taxonomy

Goal: extend real-trace precision evidence beyond the current offset suite while
keeping claims narrow and data-backed.

Default decisions:
- keep `single_head`, `radix2`, and `block_recentered` as the only active
  schemes until a broader failure taxonomy exists;
- prefer organically longer or less templated traces over more cosmetic offset
  variants;
- record failure type (`tie-collapse`, `wrong-address inversion`, `other`) for
  every failing stream;
- update claims only to the exact validated suite.

Exit conditions:
- each tracked stream has a native horizon, first-failure multiplier, and
  failure-type record;
- the project can say exactly where decomposition helps and where it fails,
  without broadening the claim beyond the validated suite.

### Track C — `M6-A` frontend boundary and differential harness

Goal: make the first compiled-frontend step decision-complete without entering
implementation.

Default decisions:
- the first frontend is a **tiny typed bytecode**, not a Wasm-like subset;
- short programs require exact trace matching; longer ones require at least
  exact final-state matching plus first-divergence diagnostics;
- floating point, heap allocation, aliasing, syscalls, threads, undefined
  behavior, and any unbounded runtime surface stay out of scope.

Gating rule:
- no implementation starts until Track A and Track B are closed and `M5`
  remains frozen as the fair negative control.

### Track D — publication pipeline

Goal: ensure future paper/blog writing depends on preserved evidence rather than
memory.

Required ledgers:
- claim ladder;
- figure/table backlog;
- experiment manifest;
- threats-to-validity ledger;
- negative-results ledger.

Default stance:
- paper-first, blog-second;
- the blog may summarize stabilized claims, but it may not define them.

## Parallelization rules

- Track A and Track B are the blocking research tracks.
- Track C and Track D may proceed in parallel, but only as downstream
  documentation/specification work.
- `M5` stays frozen unless Track A changes the fair label space or decode ladder
  enough that a matched negative-control rerun becomes mandatory.

## Artifact capture rules

Every unattended batch should leave behind:

- a concise delta summary;
- updated claim status if any claim changed;
- newly blocked or unblocked hypotheses;
- a pointer to the exact artifact that supports the change;
- the next stop/go decision.

The default record format for new milestones is:

- `README.md`
- `acceptance.md`
- `status.md`
- `todo.md`
- `research_notes.md`
- `blocked_hypotheses.md`
- `brainstorm_log.md`
- `artifact_index.md`
- `experiment_matrix.md`
- `result_digest.md`

## Non-goals for this phase

- claiming that a general LLM is now a computer;
- claiming arbitrary C support;
- using Sudoku / Hungarian / similar demos as primary evidence;
- adding new decomposition families or new frontend surfaces before current
  uncertainties are narrowed;
- reopening `M5` as an open-ended performance branch.
