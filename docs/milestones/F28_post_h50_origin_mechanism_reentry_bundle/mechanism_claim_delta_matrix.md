# F28 Mechanism Claim Delta Matrix

| Claim layer | Narrow interpretation after `H50` | Landed support | Still unresolved | Route implication |
| --- | --- | --- | --- | --- |
| `A` | deterministic execution can be represented as an append-only execution trace with transparent replay semantics | `R34`, `R35`, `R42`, `R43`, `R44`, `R47`, `R50`, `R51`, and preserved `H29/H36/H43/H50` support this narrowly | whether that trace carrier is sufficient as the explicit state surface for a bounded free-running trace VM rather than only as a family of fixed demonstrations | route the next exact semantics question to `R56`, but only after retrieval equivalence is isolated in `R55` |
| `B` | latest relevant state can be recovered exactly from append-only history by structured `2D` hard-max retrieval | `R34` and `R42` support exact latest-write retrieval narrowly | whether the claimed fast path is reference-exact on the required tie, overwrite-after-gap, duplicate-max, and coordinate-offset cases | isolate this first in `R55` rather than hiding it inside a larger end-to-end demo |
| `C` | append-only trace plus exact retrieval can support one bounded free-running internal executor exactly | `R35`, `R43`, `R44`, `R46`, `R47`, `R49`, `R50`, and `R51` support bounded exact execution surfaces narrowly | whether one explicit trace VM can stay step-exact without external execution at tested runtime | test this in `R56` after `R55` is exact |
| `D` | an accelerated retrieval/runtime path adds bounded scientific or system value over transparent reference execution | negative `H50` shows that broader post-`H49` internal-route value was not established | whether the narrower trace-VM fast path still retains bounded value once retrieval equivalence and trace semantics are isolated | defer value judgment to `R57`, then close explicitly in `H52` |

## Reading

- `A/B/C` remain bounded exact substrate claims only.
- `D` is unresolved on the narrower mechanism lane and must not be inferred
  from prior broader internal-route negatives or positives.
- The strongest next question is now mechanism equivalence and trace semantics,
  not transformed or trainable entry.
