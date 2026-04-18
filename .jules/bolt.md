## 2024-05-24 - `dict.setdefault` Performance in Hot Loops
**Learning:** `dict.setdefault(key, complex_default)` evaluates `complex_default` *every* time, even if the key already exists. This can be extremely slow if the default value requires allocating lists or performing operations (like `[Fraction(0) for _ in value]`).
**Action:** Replace `dict.setdefault` in hot loops with explicit `if key not in dict: dict[key] = complex_default` checks to avoid eager evaluation overhead.
