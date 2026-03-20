# Status

Provisioned on 2026-03-20 during post-`H12` staging and extended the same day
with one bounded per-file timing follow-up.

- targeted standing-guard tests are green, and `pytest --collect-only -q`
  returns successfully on the current suite;
- the base audit collects `192` tests across `44` files and now counts `4`
  genuinely torch-dependent files after excluding string-literal false hits;
- the bounded follow-up times the top-`6` `model_or_training` candidates and
  completes `6/6` files with no timeouts;
- the follow-up classifies the current full-suite gate as `healthy_but_slow`,
  with total shortlisted wall time about `90.6089s`, median per-file wall time
  about `14.3865s`, and slowest-file wall time about `25.1116s`;
- the current operational recommendation is to reserve full `uv run pytest -q`
  for long unattended windows rather than short interactive waits;
- this lane is operational only: it explains validation behavior without
  weakening the scientific gate by fiat;
- under `H14`, it remains a standing validation-hygiene reference rather than
  the active scientific driver.
