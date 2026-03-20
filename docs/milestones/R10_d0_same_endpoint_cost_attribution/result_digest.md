# Result Digest

`R10` exported the bounded same-endpoint cost-attribution companion on the
current tiny typed-bytecode `D0` endpoint and made the negative systems result
more explicit rather than trying to rescue it.

## What `R10` closed

- narrowed attribution to the top `2` harder `R8` families plus their matched
  admitted `R6` source rows after a full component-wise exact attribution on
  the heaviest `R8` row exceeded `150s` in one local benchmark;
- profiled `4` representative rows and found exact-versus-lowered runtime
  ratios ranging from about `549.6x` to `3165.2x`, with a median around
  `2429.1x`;
- found retrieval to be the dominant exact-runtime component on `4/4` profiled
  rows, with median retrieval share around `99.8%` and harness share
  effectively negligible;
- made the current implementation detail explicit: exact-read validation still
  pays both the linear and accelerated query paths, so the linear query path
  remains visible as validation overhead inside the accelerated exact run;
- kept `E1c` inactive and handed the packet forward to `H12`.

## What `R10` did not do

- did not reopen a broader systems packet or claim end-to-end superiority;
- did not claim that these representative rows cover every admitted family;
- did not convert same-endpoint attribution into a widening argument.
