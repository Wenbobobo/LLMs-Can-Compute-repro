## 2024-05-15 - [Avoid dict.setdefault in hot loops with complex defaults]
**Learning:** `dict.setdefault(key, complex_default)` eagerly evaluates the default value even when the key exists. In hot loops, especially with dictionary/list comprehensions or complex object creation as the default value, this introduces measurable overhead.
**Action:** Replace `dict.setdefault(key, complex_default)` with an explicit `if key not in dict: dict[key] = complex_default` followed by `bucket = dict[key]` in performance-critical loops.
