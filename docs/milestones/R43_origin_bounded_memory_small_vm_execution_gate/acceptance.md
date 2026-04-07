# R43 Acceptance

- execution families are fixed before runtime;
- exact source/spec comparison is mandatory;
- exact source/lowered comparison is mandatory;
- exact accelerated free-running trace and final-state comparison is mandatory;
- no heap region, new substrate, or widened semantic surface is introduced;
- the optional call/return family may execute only after the four core
  families stay exact; and
- `R43` stops below `R45` model comparison and below any `R44` useful-case
  widening.
