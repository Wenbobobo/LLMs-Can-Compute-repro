# M4 Precision Organic Traces

Goal: widen the current `C3e` boundary beyond offset-derived streams using new
organic trace families, while keeping the scheme set frozen.

Frozen comparison set:
- `single_head`
- `radix2`
- `block_recentered`

Frozen evaluation pattern:
- screen at base `64`;
- if a stream shows a boundary signal, sweep bases `{32, 64, 128, 256}`;
- record native horizon plus `1x/4x/16x/64x` multiplier behavior.

This milestone adds new streams only if they sharpen the current precision
boundary. It does not add new decomposition families.
