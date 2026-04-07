# R46 Stop Conditions

- stop scientific success immediately if any held-out variant breaks verifier,
  scope, source/spec agreement, source/lowered agreement, or free-running exact
  execution;
- stop scope immediately if a variant introduces heap memory or an opcode
  outside the admitted restricted surface;
- do not reinterpret a partial pass as broader support;
- if all `8/8` rows stay exact, stop at
  `surface_generalizes_narrowly` and hand off to `H45`;
- do not authorize `R47`, `R48`, or any broader compiled surface directly from
  `R46`.
