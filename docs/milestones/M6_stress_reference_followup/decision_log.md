# Decision Log

- Chosen stress family:
  branch-selected helper checkpoint braid.
- Rejected stress families:
  branch-heavy helper braid alone,
  frame/heap checkpoint braid alone.
- Chosen external reference:
  standalone Python spec interpreter with no lowering reuse.
- Minimum planned suite:
  `3` positives
  (`2` medium exact-trace on distinct paths, `1` long exact-final-state),
  plus `2` matched negatives
  (`1` control-flow or typed-branch contract violation, `1`
  memory-surface contract violation).
- Stop/go rule:
  broader compiled demos remain blocked unless the stress suite and the
  external reference both agree under the frozen `D0` semantics.
