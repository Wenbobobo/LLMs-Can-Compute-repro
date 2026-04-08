## 2024-03-24 - [Avoid eager evaluation of default dict in hot loops]
**Learning:** Found a specific bottleneck where `setdefault` was used inside a loop to instantiate complex default dicts with `Fraction` objects, causing high overhead. Eager evaluation of the default parameter inside `setdefault` happens on *every* loop iteration regardless of key presence.
**Action:** Replace `setdefault` with an explicit `if key not in dict:` check to instantiate expensive defaults lazily only when necessary. Also beware of local benchmark side effects dirtying `results/` folder tracked files.
