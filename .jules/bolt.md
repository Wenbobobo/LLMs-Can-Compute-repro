## 2024-05-18 - Unintended file modifications from tests
**Learning:** Running `uv run pytest` or targeted tests and scripts locally can regenerate files in the `results/` directory, causing unintended modifications to tracked benchmark baselines and snapshots.
**Action:** Always check `git status` after running tests/benchmarks and run `git restore --staged results/` and `git checkout results/` to clean up the repository before committing and submitting PRs.
