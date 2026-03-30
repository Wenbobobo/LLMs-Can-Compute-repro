## 2026-03-30 - Inlining `dot_2d` in `brute_force_hardmax_2d`
**Learning:** Avoid repeated type coercion and length checking (e.g., `_coerce_key` for `Fraction` tuples) inside hot loops for geometry calculations. Inlining operations like dot products on pre-coerced tuples significantly reduces overhead.
**Action:** When working on geometry calculations, measure the overhead of function calls and tuple coercions. Consider inlining if the function is inside a tight loop and the size is fixed and known.
