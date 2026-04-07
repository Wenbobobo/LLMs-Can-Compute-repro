# R48 Acceptance

- the gate remains comparator-only rather than substitutive;
- execution remains bounded to the preserved useful-case contract admitted by
  `R47` and interpreted by `H46`;
- exact evidence remains decisive and model positives do not replace exact
  failures;
- both admitted modes remain exact on the preserved `8/8` useful-case
  variants across the fixed `3/3` kernels;
- the trainable mode remains exact on the explicit held-out
  `histogram16_u8` family;
- first-error position and failure class are mandatory outputs;
- `compiled_weight_executor` and `trainable_2d_executor` remain the only
  admitted modes here; and
- no broader Wasm/C, broader hybrid model work, or merge posture is
  authorized here.
