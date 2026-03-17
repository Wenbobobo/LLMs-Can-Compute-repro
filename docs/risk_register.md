# Risk Register

| Risk | Why it matters | Current mitigation |
| --- | --- | --- |
| Geometry exactness drift | Small errors invalidate the execution claim | Use exact fractions for comparisons and a brute-force oracle |
| Tie semantics underspecified | Equal maximizers change outputs materially | Treat averaging as part of the public API and test it explicitly |
| Numeric stability | Large-address retrieval may fail under finite precision | Start with exact arithmetic in the reference path |
| Compiler leakage | Too much work could be pushed into preprocessing | Keep interpreter semantics and trace events explicit |
| Trace under-specification | Replay becomes hand-wavy instead of exact | Require deterministic event schemas and replay checks |
| Runtime bottleneck migration | Fast lookup may not reduce total decode cost | Separate correctness from benchmark claims and measure both later |
| Over-claiming from demos | Flashy tasks can hide narrow mechanisms | Keep claim ladder A/B/C/D explicit |
| Tooling blockage | Remote setup and local verification can stall | Record the blocker and keep code/tests ready to run once shell works |
