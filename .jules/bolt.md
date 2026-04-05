
## 2024-04-05 - Avoid eager default allocation in dictionary lookups
**Learning:** In hot loops, using `dict.setdefault(key, complex_default)` unconditionally allocates the default value (e.g. lists, fraction objects) on every iteration, even when the key already exists. This creates massive memory overhead.
**Action:** Replace `dict.setdefault` with explicit membership checks (`if key not in dict: dict[key] = complex_default`) inside high-frequency loops.
