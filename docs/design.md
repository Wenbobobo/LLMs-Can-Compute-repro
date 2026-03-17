# Design

## Scientific Target

This project targets the smallest technically meaningful claim set behind the
Percepta field note:

1. execution can be represented as an append-only trace;
2. key state reads in that trace can be written as exact low-dimensional
   retrieval problems;
3. a specialized runtime path can answer those reads more efficiently than a
   prefix scan;
4. those primitives may support a small exact executor.

The repository does **not** treat "LLMs become computers" as the engineering
target.

## Branch Separation

- `M2`: exact 2D hard-max retrieval, correctness first
- `M3`: append-only trace language and reference semantics
- `M4`: exact hard-max decode branch
- `M5`: standard softmax 2D-head baseline

These branches must remain analytically separate.

## Initial Implementation Choices

- Use Python 3.12 with `uv`.
- Start with integer-heavy semantics and exact fractions where comparisons need
  to be stable.
- Accept correctness-first rebuild-based insertion in the first `HullKVCache`
  implementation, but label it honestly.
- Treat stack-machine execution as the first nontrivial proving ground.

## Acceptance Standard

- Exactness before speed.
- Full-program correctness before demo appearance.
- Honest failure accounting before narrative synthesis.
