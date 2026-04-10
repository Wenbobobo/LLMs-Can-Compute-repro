## 2024-05-24 - Avoiding setdefault in hot loops
**Learning:** Found a specific performance bottleneck where `dict.setdefault(key, complex_default)` evaluates `complex_default` completely (including memory allocations and list comprehensions) even when `key` exists. This is especially problematic in hot loops processing duplicate keys like `HullKVCache._rebuild_if_needed()`.
**Action:** Always prefer explicit membership checking (`if key not in dict: dict[key] = ...`) when the default value involves creating new objects, lists, or running comprehensions.
