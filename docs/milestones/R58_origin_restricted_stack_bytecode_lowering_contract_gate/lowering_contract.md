# Lowering Contract

- The admitted surface is one fixed typed stack-bytecode suite, not broad Wasm
  and not arbitrary `C`.
- The lowering target is the existing append-only trace instruction substrate.
- Exactness requires normalized source-vs-spec parity plus exact
  source-vs-lowered trace and final-state parity.
- Scope remains narrow even when indirect memory or call/return appears on the
  admitted rows.
