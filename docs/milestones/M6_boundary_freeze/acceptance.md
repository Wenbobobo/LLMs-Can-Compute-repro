# Acceptance

- the current `D0` slice is described consistently as:
  tiny typed bytecode,
  control-flow-first static-target non-recursive `call/ret`,
  plus appendix-level memory-surface diagnostics;
- the freeze decision does not widen the claim set beyond current `D0`;
- contradiction triggers are explicit enough that future unattended batches can
  tell whether to reopen `M6` widening;
- later compiled demos remain blocked unless this freeze decision and the
  downstream stress/reference checks both hold.
