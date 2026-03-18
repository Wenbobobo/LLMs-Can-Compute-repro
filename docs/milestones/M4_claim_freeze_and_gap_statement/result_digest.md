# Result Digest

## Supported

- `C2f`: staged pointer decoding reaches exact rollout on the current toy suite
  only under `opcode_legal`.
- `C3e`: decomposition remains stable on the broadened current suite while
  float32 single-head fails immediately on the new high-address memory
  families.

## Unsupported

- A fair staged decoder result independent of strong legality masks.
- A broad long-horizon float32 robustness claim.
- Any compiled-program narrative broader than tiny typed bytecode.

## Unresolved

- Whether future fair-regime decoder improvements can recover exact rollout
  without importing stronger legality structure.
- Whether broader real traces expose non-`tie_collapse` precision failures.
