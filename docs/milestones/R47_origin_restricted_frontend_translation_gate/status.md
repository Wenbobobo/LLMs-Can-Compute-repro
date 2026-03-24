# R47 Status

- completed exact runtime gate under active docs-only `H45`;
- translates one structured restricted frontend surface onto the existing
  useful-case bytecode kernels and exactness pipeline;
- preserves the landed bounded useful-case claim ceiling;
- records `lane_verdict = restricted_frontend_supported_narrowly`;
- keeps translation identity exact on all `8/8` admitted rows across `3/3`
  fixed useful-case kernels;
- remains below heap allocation, alias-heavy pointers, recursion, float, IO,
  hidden mutable state, and broad compiler/runtime claims;
- routes the next interpretation through later explicit
  `H46_post_r47_frontend_bridge_decision_packet`;
- keeps `F22` blocked while later model-side comparison is still unexecuted; and
- does not authorize `R48`, broader Wasm/C, or merge-to-`main`.
