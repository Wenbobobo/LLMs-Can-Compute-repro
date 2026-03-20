# R8 D0 Retrieval-Pressure Design

## Goal

Stress the same fixed `D0` endpoint with harder latest-write / stack / control
retrieval pressure without widening semantics.

## Intended outputs

- one bounded harder-family suite;
- verifier/spec/lowered/linear/Hull parity rows on the same endpoint;
- retrieval-pressure rows exported per admitted case;
- contradiction routing only through `E1c`.

## Scope lock

- no frontend widening;
- no open-ended family expansion;
- no broad runtime claim.

## Acceptance

- every admitted row remains exact across the same endpoint stack;
- every failure is typed as finite-precision, harness/annotation, or true
  `D0` contradiction;
- retrieval pressure is quantified rather than implied.
