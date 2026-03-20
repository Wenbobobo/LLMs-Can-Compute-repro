# Status

Opened and completed on 2026-03-19.

- `R7` preserved the full `8`-family exact-admitted `R6` index, then profiled
  only the top `4` heaviest family representatives on the same endpoint in one
  bounded single-pass profile;
- all `4/4` profiled rows stayed exact with `0` contradiction candidates and
  exact linear-versus-accelerated final-state / trace agreement throughout;
- the lane stopped at `stop_decode_gain_not_material`: accelerated Hull decode
  is only about `0.973x` of linear on median and still about `1980.3x` slower
  per step than the lowered path on the profiled rows;
- `R5` remained not justified and `E1c` remained inactive, so the next lane
  stayed `H9_refreeze_and_record_sync`.
