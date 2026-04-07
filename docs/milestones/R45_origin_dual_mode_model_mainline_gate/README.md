# R45 Origin Dual-Mode Model Mainline Gate

Executed the coequal dual-mode model gate after the landed exact `R43` gate.

`R45` asks one bounded question:

- can the two admitted model-side executor modes stay exact on the fixed `R43`
  bounded-memory contract family without replacing exact evidence?

The lane compares:

- `compiled_weight_executor`;
- `trainable_2d_executor`;
- the landed exact `R43` contract family.

The landed result is narrow and positive:

- both admitted modes stay exact on all `5/5` fixed bounded-memory families;
- the fitted `trainable_2d_executor` trains only on the `4/4` core families
  and remains exact on the held-out optional single-call/return family;
- memory reads stay on the exact accelerated path and call-frame reads stay on
  the exact pointer-like path;
- model evidence remains explicitly downstream of exact `R43`, so `R45`
  improves the operator/comparator story without changing the scientific claim
  boundary.
