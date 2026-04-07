# F18 Claim Ladder

| claim_id | claim_text | status | required_gate | falsifier | next_route |
| --- | --- | --- | --- | --- | --- |
| `A` | computation can be represented as an append-only trace whose state is reconstructed from prior events | `supported_here_narrowly` | none on the current stack | exact replay/state reconstruction fails on the current Origin-core rows | preserve current substrate and sharpen only bounded memory cases |
| `B0` | exact `2D` hard-max retrieval primitives work on the current Origin-core bundle | `supported_here_narrowly` | none on the current stack | primitive/reference mismatch on current `R34` and `R40` evidence | preserve as upstream support |
| `B1` | latest-write-by-address and stack-slot retrieval remain exact under longer append-only address reuse | `not_yet_validated_here` | `R42_origin_append_only_memory_retrieval_contract_gate` | accelerated retrieval diverges from brute-force reference on bounded memory tasks | semantic-boundary route under `F9/F19` |
| `C0` | a small exact append-only stack/VM executor is supported on the current narrow bundle | `supported_here_narrowly` | none on the current stack | free-running exactness fails on preserved `R35/R40` rows | keep current narrow reading |
| `C1` | a bounded-memory small VM with address reuse, branching, and optional single-layer calls remains exact | `not_yet_validated_here` | `R43_origin_bounded_memory_small_vm_execution_gate` | exact free-running execution fails once bounded memory obligations are added | continue only if `R42` stays exact |
| `D` | a restricted Wasm / tiny-`C` lowering can run useful kernels exactly on the same append-only substrate | `supported_here_narrowly` | none on the current stack | any useful kernel needs heap, alias-heavy pointers, hidden mutable state, or approximation | preserve as bounded useful-case support only until a later explicit packet selects any broader route |
