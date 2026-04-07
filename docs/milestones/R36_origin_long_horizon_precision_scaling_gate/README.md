# R36 Origin Long-Horizon Precision Scaling Gate

Executed narrow precision-scaling gate after `H29`.

`R36` tests the finite-precision boundary on the active Origin-core bundle
without reopening a broad precision campaign. The lane keeps the scope narrow:

- real extracted read streams only;
- current append-only memory / stack / call primitives only;
- native horizon plus a few predeclared inflated horizons only;
- `single_head` vs bounded decomposition schemes only.
