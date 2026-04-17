
## 2024-05-18 - Eager instantiation with dict.setdefault
**Learning:** `dict.setdefault(key, expensive_default)` inside hot loops eagerly evaluates `expensive_default` on *every* iteration, which is a major performance bottleneck for Python loops where defaults are objects or lists.
**Action:** Always replace `setdefault` with an explicit `if key not in dict: dict[key] = ...` membership check to prevent eager evaluation.
