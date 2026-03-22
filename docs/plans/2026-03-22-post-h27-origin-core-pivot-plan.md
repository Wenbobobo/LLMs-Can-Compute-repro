# 2026-03-22 Post-H27 Origin-Core Pivot Plan

## Summary

`H27_refreeze_after_r32_r33_same_endpoint_decision` closes the old
same-endpoint `D0` recovery wave more negatively than before. `R32` did not
localize a clean boundary, `R33` showed the systems story remains
noncompetitive after localization, and `R29/F3` remain blocked.

The next phase therefore pivots away from trying to rescue the frozen tiny
typed-bytecode endpoint by momentum. The active target becomes the narrower
Origin-core reproduction thesis:

1. append-only execution traces can encode deterministic computation;
2. exact `2D` hard-max retrieval can recover latest relevant prior state with a
   geometry-backed cache;
3. those primitives can support a small exact stack/VM executor before any
   broader compiler or demo claim.

## Immediate Execution Order

1. Save this packet and promote it into one explicit `H28` reanchor stage.
2. Execute `R34_origin_retrieval_primitive_contract_gate`.
3. Execute `R35_origin_append_only_stack_vm_execution_gate`.
4. Freeze the outcome in `H29_refreeze_after_r34_r35_origin_core_gate`.

Only if `H29` is positive should the next wave open:

5. `R36_origin_long_horizon_precision_scaling_gate`
6. conditional `R37_origin_compiler_boundary_gate`
7. `H30_post_r36_r37_scope_decision_packet`

## Near-Term Design Decisions

- Treat `H27` as a closeout of the old same-endpoint recovery narrative, not as
  a launch point for `R29`.
- Keep `R29`, `F3`, and frontier/demo scope blocked. They remain optional
  later branches only after a future explicit reauthorization packet.
- Keep paper/blog/public README maintenance low priority until the Origin-core
  experiment stack catches up with or surpasses the source article's defensible
  mechanism claims.
- Run new implementation work from the clean `wip/h27-promotion` base, not from
  dirty `main`.

## `R34` Contract

`R34` should test the smallest falsifiable retrieval primitives directly:

- `latest_write(addr)`
- `stack_top()`
- `stack_at_depth(d)`
- `call_return_target()`
- exact tie-average semantics for hard-max retrieval

Each primitive must keep a linear oracle and an accelerated `HullKVCache`
backend. The gate passes only if all audited primitive rows remain exact and
the tie-average semantics remain exact as part of the retrieval definition.

## `R35` Contract

`R35` should stop talking about the old compiled endpoint and instead test a
small append-only stack machine honestly:

- fixed minimal opcode surface only;
- reference interpreter plus replay oracle;
- retrieval-backed free-running executor;
- exact trace and exact final-state criteria kept separate;
- call/return included as execution semantics, not as a hidden Python-only side
  channel.

The gate should cover straight-line arithmetic, overwrite-readback, loops,
indirect memory, branch/control flow, and at least one nested call/return
program.

## Repo Hygiene Defaults

- Keep `wip/h27-promotion` as the clean integration branch for this wave.
- Do not merge back to dirty `main` yet.
- Prefer one milestone-sized commit at a time: `H28`, then `R34`, then `R35`,
  then doc/driver sync.
- Treat large raw dumps as hygiene candidates unless they are claim-critical
  canonical artifacts.
