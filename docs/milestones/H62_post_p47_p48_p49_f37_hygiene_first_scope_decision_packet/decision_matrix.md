# Decision Matrix

- default downstream state: `archive_or_hygiene_stop`
- only conditional next gate:
  `r63_post_h62_coprocessor_eligibility_profile_gate`
- runtime remains closed even if `R63` later becomes admissible
- any missing prerequisite in `P47/P48/P49/F37` forces the decision back to the
  default stop state
