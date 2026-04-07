# Operational Notes

## Worktrees

- Prefer continuing major planning or implementation in clean successor
  worktrees rather than reusing dirty integration branches by momentum.
- Keep root `main` read-only if it remains materially dirty.

## Subagents

- Use subagents only for clearly disjoint scopes, such as one paper-facing
  audit and one planning-surface audit in parallel.
- Do not parallelize overlapping edits on the same docs.

## Merge Discipline

- Merging back to `main` is not scientifically required from the current
  `H34/P20/F5/F6` state.
- Only consider promotion when the target branch state and the operational goal
  are clear enough that the merge reduces confusion rather than increases it.

## Runtime Discipline

- No future runtime execution should start from this note alone.
- Any future same-substrate execution must begin from a new explicit
  contradiction packet, not from operational convenience.
