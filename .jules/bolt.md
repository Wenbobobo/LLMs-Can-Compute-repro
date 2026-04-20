## 2024-04-20 - [Avoid setdefault with complex defaults in loops]
**Learning:** `dict.setdefault(key, complex_default)` evaluates `complex_default` on every iteration, even if the key already exists. This causes significant performance overhead in hot loops when the default is a dictionary or list, as it constantly creates and immediately discards these objects.
**Action:** Replace `dict.setdefault(key, complex_default)` with `if key not in dict: dict[key] = complex_default` to avoid expensive eager evaluation.
