# Status

Provisioned on 2026-03-19.

- the repository already has the ingredients for this gate: geometry
  benchmarks, exact executors, typed-bytecode reference paths, and a standalone
  spec oracle;
- the first explicit comparison layer now exists under
  `results/R2_systems_baseline_gate/`;
- current gate result is mixed but useful: geometry still shows a strong
  asymptotic win, while the lowered `exec_trace` path is not yet end-to-end
  competitive with the best current reference/oracle path on the exported `D0`
  suites;
- this milestone now has a concrete stop/go artifact for `M7`, even though
  broader cost attribution is still open.
