# F23 Precision Regime Matrix

| regime_id | role_in_r49 | current evidence state | admission posture |
| --- | --- | --- | --- |
| `float64_reference` | small sampled reference rows only | stable current audit baseline | required as reference only, not the claimed deploy path |
| `float32_single_head` | failure-localization control | preserved finite-precision negative control | required negative control; may not be the sole success basis |
| `float32_radix2` | primary admissible recovery regime | positive on current precision boundary rows | admitted for all `R49` buckets |
| `float32_block_recentered` | coequal admissible recovery regime | positive on current precision boundary rows | admitted for all `R49` buckets |
| `float32_segment_rescaled` | reserve fallback regime | not yet validated on the preserved useful-case contract | planning-only; may appear in `R49` only after earlier admitted regimes fail on the same bucket |
| `bfloat16_single_head` | weak negative control | too unstable on current narrow precision evidence | diagnostic only |
| `float16_single_head` | weak negative control | too unstable on current narrow precision evidence | diagnostic only |
