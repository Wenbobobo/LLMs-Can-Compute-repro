# F25 Admitted Surface Matrix

| source fragment family | admitted restricted tiny-`C` form | preserved lowering target | reason admitted now |
| --- | --- | --- | --- |
| bounded scalar math | `int32_t`-like scalars, counters, and accumulators with bounded ranges only | existing `i32` scalar/local operations on the preserved useful-case kernels | already inside the `R47` structured frontend bridge contract |
| static buffer access | declared fixed-size arrays in explicit static memory windows | fixed address windows on the append-only trace substrate | preserves `R47` static-memory-only posture |
| structured control | canonical `if`/`else`, `for`, and `while` lowered to structured loop/branch form | same structured branch/loop lowering family used by `R47` | keeps control flow below irreducible CFG or hidden jumps |
| fixed-range table updates | predeclared bounded update tables such as `hist[16]` with explicit range guards | existing bounded table-update useful-case kernels | keeps `histogram16_u8` inside a fixed finite domain |
| single-kernel entrypoint | one top-level kernel function with explicit inputs and outputs | same one-kernel useful-case execution contract preserved by `R47/R49` | prevents scope drift into general program execution |
