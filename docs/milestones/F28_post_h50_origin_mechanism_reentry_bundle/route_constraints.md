# F28 Route Constraints

- `H51` is the only follow-up packet fixed here.
- `R55` is the only next runtime candidate fixed here.
- `R56` can run only after positive exact `R55`.
- `R57` can run only after positive exact `R56`.
- `H52` is the only closeout packet fixed for this mechanism lane.
- `F27` remains saved as planning-only and cannot authorize execution from
  `F28`.
- `R53` and `R54` remain saved future gates only and do not authorize
  execution from `F28`.
- broader useful-case growth cannot reopen by momentum from positive `R50` or
  positive `R51`.
- transformed-model or trainable entry cannot reopen by momentum from
  preserved `R45` or negative `H50`.
- external execution during tested runtime does not count as internal
  execution evidence for `R56`.
- dirty root `main` remains out of scope for scientific execution in this
  wave.
