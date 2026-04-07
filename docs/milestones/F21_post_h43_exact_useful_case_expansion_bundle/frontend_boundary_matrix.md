# F21 Frontend Boundary Matrix

| wave | objective | allowed surface | excluded by default | stop rule |
| --- | --- | --- | --- | --- |
| `R47_origin_restricted_frontend_translation_gate` | test one tiny restricted frontend bridge onto the same useful-case contract | bounded `i32`, bounded locals, structured loop/branch, static memory only | no heap, no alias-heavy pointers, no recursion, no float, no IO, no hidden mutable state | stop at first excluded feature or exact free-running break |
| `H46_post_r47_frontend_bridge_decision_packet` | interpret `R47` and decide whether model useful-case comparison is admissible | preserved exact `R46/R47` contract only | no broader frontend or new substrate | stop if `R47` is not `restricted_frontend_supported_narrowly` |
