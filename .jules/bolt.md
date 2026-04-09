## 2024-03-27 - Inline dot_2d to avoid coercion overhead
**Learning:** Calling functions with argument validation (like `_coerce_key` checking types and tuple length) inside a hot loop (like a linear scan over points or brute-force cache queries) introduces massive overhead in Python compared to the actual mathematical operations (fractional dot product).
**Action:** When working on numerical heavy loops, inline exact operations on pre-coerced typed properties instead of repeatedly calling helper functions that perform identical runtime validations on every iteration.
