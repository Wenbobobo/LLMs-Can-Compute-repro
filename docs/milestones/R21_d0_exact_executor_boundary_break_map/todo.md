# Todo

- [x] Run the bounded grid over address count, horizon multiplier,
  checkpoint depth, and hot-address skew.
- [x] Keep two deterministic seeds per grid point and stop expanding a branch
  after two exactness failures in that branch.
- [x] Export success rows, failure rows, and the first-fail digest.
- [x] Align the bounded branch metadata with `R20`-style mechanism signals
  such as unique-address pressure and hottest-address share.
- [x] Leave one explicit boundary verdict rather than opening a repair loop.
