# Status

Initial `M4` prototype implemented and extended with a narrow trainable slice.

Current scope:

- exact 2D hard-max latest-write encoding,
- linear-scan reference decode,
- `HullKVCache` accelerated decode,
- validation against real `exec_trace` memory examples, including dynamic
  addressing,
- validation against logical stack-slot reads extracted from real traces.
- a two-parameter trainable scorer fitted on short countdown stack traces and
  evaluated on longer countdown traces plus a dynamic-memory stack trace.

This is still not a token-level or free-running learned model branch. The new
trainable slice chooses among reference-generated latest-write candidates rather
than generating trace events on its own.

Current exported result:

- best scorer found so far uses `quadratic_scale=0.25` and `time_scale=0.0005`,
- exact program accuracy is `1.0` on the short countdown training slice,
- exact program accuracy is `1.0` on held-out longer countdown traces,
- exact program accuracy is `1.0` on the current dynamic-memory stack trace.
