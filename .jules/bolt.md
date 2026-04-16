## 2024-05-14 - Eager Evaluation in dict.setdefault

**Learning:** When `dict.setdefault(key, complex_default)` is used inside a loop, Python eagerly evaluates the `complex_default` argument on *every* iteration before calling the method, even if the key already exists. In `src/geometry/hull_kv.py`, this caused a list of `Fraction(0)` objects to be instantiated repeatedly, leading to significant overhead in the `_rebuild_if_needed` loop.
**Action:** Avoid `setdefault` for complex default values (lists, objects, function calls) in hot paths. Instead, use an explicit membership check (`if key not in dict: dict[key] = complex_default()`) to ensure lazy evaluation and avoid unnecessary allocations.
