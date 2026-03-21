# R15 D0 Remaining-Family Retrieval-Pressure Design

## Goal

Close the four `R6` family gaps that `R8` deliberately left unprofiled, while
keeping the endpoint, accounting style, and contradiction routing unchanged.

## Inputs

- `results/R6_d0_long_horizon_scaling_gate/summary.json`
- `results/R8_d0_retrieval_pressure_gate/summary.json`
- `src/bytecode/datasets.py`
- `src/bytecode/stress_reference.py`

## Output expectations

- one bounded `10x` retrieval-pressure row per remaining admitted `R6` family;
- exact-suite rows, bounded decode-parity probes, pressure rows, family
  summaries, and claim-impact routing matching `R8` style;
- explicit handoff to `R16` unless a contradiction or harness gap blocks it.

## Acceptance

- all admitted rows stay exact across verifier/spec/lowered/linear/Hull;
- pressure growth is exported quantitatively for the remaining family set;
- only true `D0` contradictions route to `E1c`;
- the remaining-family gap from `R8` is no longer implicit.
