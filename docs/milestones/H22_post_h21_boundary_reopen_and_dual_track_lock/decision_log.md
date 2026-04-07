# Decision Log

- Keep `H21_refreeze_after_r22_r23` as the frozen input until `H23` lands.
- Keep `H21` explicit as the preserved frozen control underneath the reopened
  packet.
- Reopen science execution only on the fixed `D0` endpoint.
- Run one bounded runtime lane (`R26`) plus one bounded mechanism audit lane
  (`R28`) in parallel.
- Make `R27` conditional rather than active by default so the first-wave
  verdict remains readable.
- Delay all outward-sync work to `P14`.
