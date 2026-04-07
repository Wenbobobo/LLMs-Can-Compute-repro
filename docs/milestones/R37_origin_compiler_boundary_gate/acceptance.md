# R37 Acceptance

`R37` passes only if:

- the compiled/lowered boundary stays tiny and machine-auditable;
- source reference, lowered interpreter, and free-running exact executor agree
  on the exported admitted rows;
- exact trace and exact final state remain separate exported criteria;
- any failure is exported explicitly without being rebranded as a systems win or
  a broad compiler result.
