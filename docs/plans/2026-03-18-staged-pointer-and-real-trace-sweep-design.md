# Staged Pointer Decode and Real-Trace Sweep Design

## Why this branch existed

The direct factorized event-value decoder made the core difficulty explicit:
teacher-forced labels were learnable, but free-running rollout still collapsed.
The next intervention needed to be narrower than a full new neural executor and
more honest than simply hand-coding the induced rules again.

The staged pointer branch was chosen as that middle step. Instead of predicting
raw values directly, it predicts candidate-source expressions such as `read0`,
`add`, `memory_read_value`, and `const_arg`. This keeps the runtime grounded in
append-only retrieval while reducing the burden of raw scalar classification.

## Key design split

Three decode regimes are intentionally tracked:

- `structural`: only broad legality masks such as stack depth and available
  argument/read slots. This is the fairest regime for baseline comparison.
- `opcode_shape`: fixes the event skeleton for a given opcode — read/pop/push
  counts, branch presence, and memory read/write structure — while still
  forcing the model to choose candidate sources.
- `opcode_legal`: strongest current staged regime. It removes impossible DSL
  field combinations for a given opcode and is the current exact staged result.

This split makes the interpretation sharper.

- If `opcode_shape` recovers some rollout, then candidate-source prediction is
  doing real work beyond the strongest legality mask.
- If exactness still requires `opcode_legal`, then the current bridge remains a
  staged decoder result rather than a general learned executor.
- The same split clarifies the `M5` pointer baseline. If the standard softmax
  baseline only looks successful once `opcode_legal` masks are enabled, that is
  not evidence that it learned execution.

## Harder family rationale

The earlier staged export still leaned heavily on countdown, branch,
indirect-memory, and one ping-pong mixed-memory slice. That made the recovery
look cleaner than it should have.

The added `alternating_memory_loop` family is a small but more branch-heavy and
mixed-memory program family. It forces repeated address/value interactions that
are less symmetric than ping-pong and less templated than the shorter branch
examples. The new staged and baseline exports both include this family so the
comparison does not overfit one easy held-out slice.

## Precision sweep rationale

The first real-trace precision export showed that single-head float32 failures
reappear on offset memory streams. That still left two ambiguities:

1. were the failures only about address magnitude?
2. was the current suite too dominated by one loop family?

The new sweep keeps the real streams fixed and inflates `max_steps` by
`1x/4x/16x/64x`. This directly stresses the time-resolution term in the
latest-write encoding. Base sweeps for `radix2` and `block_recentered` then
show whether decomposition survives that extra pressure.

Adding alternating-memory offset streams answers the second ambiguity. The
result is still narrow, but it is materially harder to dismiss as a single-loop
artifact.
