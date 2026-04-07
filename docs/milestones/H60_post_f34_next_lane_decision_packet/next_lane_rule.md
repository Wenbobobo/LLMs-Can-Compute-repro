# Next-Lane Rule

- keep `planning_only_or_project_stop` as the live downstream state
- do not authorize runtime execution from `H60`
- if a later reopen happens, it must start from a new explicit packet and a
  materially different cost structure
- if no such packet arrives, the correct follow-up is archive / stop / hygiene
