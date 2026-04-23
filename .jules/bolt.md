## 2024-05-24 - [Avoid `dict.setdefault` in hot loops]
**Learning:** `dict.setdefault(key, default)` evaluates the `default` expression eagerly on *every* loop iteration before performing the membership check. In cases where the default value requires complex allocation or computation (e.g., `{"value_sum": [Fraction(0) for _ in value]}`), this results in significant performance degradation in hot loops.
**Action:** Replace `dict.setdefault` in hot loops with explicit `if key not in dict:` membership checks and lazy assignment.
