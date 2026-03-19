# Decision Log

- Split future reopen work into three dormant lanes rather than one generic
  “evidence patch” bucket, so later activation stays minimal and auditable.
- Keep `E1a` pinned to bounded precision rows `C3d` / `C3e` rather than letting
  it absorb systems or compiled-boundary questions.
- Keep `E1b` pinned to the current mixed `R2` gate and make clear that even a
  stronger current-scope systems result does not auto-authorize frontend
  widening.
- Keep `E1c` pinned to the existing tiny typed-bytecode `D0` slice and require
  any future repair to preserve the current no-widening decision.
- Treat all `F1` outputs as dormant protocols only; the current repo state has
  no active reopen lane.
