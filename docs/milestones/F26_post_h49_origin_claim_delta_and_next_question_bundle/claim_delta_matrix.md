# F26 Claim Delta Matrix

| Claim layer | Narrow interpretation after `H49` | Landed support | Still unresolved | Route implication |
| --- | --- | --- | --- | --- |
| `A` | deterministic computation can be represented as an append-only trace with explicit replay semantics | `R34`, `R35`, `R42`, `R43` and preserved `H29/H36/H43/H49` support this narrowly | broader mutable-state emulation outside the bounded current substrate | keep `A` treated as supported on the current bounded exact substrate |
| `B` | critical reads can be rewritten as exact structured retrieval on append-only history | `R34`, `R42`, and preserved exact retrieval identity support latest-write and stack-slot retrieval narrowly | memory/control pressure beyond the landed bounded suite | route the next runtime question to `R51` rather than to another useful-case demo |
| `C` | those primitives support a useful exact executor on bounded programs | `R35`, `R43`, `R44`, `R46`, `R47`, `R49`, and `R50` support a bounded executor/useful-case chain | whether the current substrate still works once memory/control pressure rises beyond the landed tiny useful-case rows | test this in `R51` before any broader trainable or transformed story |
| `D` | a higher-level compile/transform pipeline can target the substrate robustly | `R44`, `R47`, and `R50` support only a narrow, useful-case-bound, exact lowering chain | whether broader internal execution retains scientific or system value over simpler baselines | defer broader `D` growth; evaluate bounded value in `R52` first |

## Reading

- `A/B/C` are supported only on the bounded current substrate.
- `D` is supported only as a narrow useful-case bridge, not as arbitrary `C`,
  general Wasm, or a general trainable executor story.
- The strongest unresolved question is now "sufficiency plus bounded value",
  not "one more slightly richer frontend".
