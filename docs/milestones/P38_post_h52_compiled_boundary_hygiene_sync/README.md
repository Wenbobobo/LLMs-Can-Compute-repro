# P38 Post-H52 Compiled-Boundary Hygiene Sync

Completed low-priority operational/docs sync packet for the post-`H52`
compiled-boundary wave.

`P38` does not alter the active scientific stage. It preserves `H53` as the
preserved prior compiled-boundary reentry packet, preserves `H54` as the
current active docs-only closeout, preserves `H52` as the preserved prior
mechanism closeout, preserves `H43` as the paper-grade endpoint, and codifies
the worktree, artifact, and commit policy needed for
`F29 -> H53 -> R58 -> R59 -> H54`.

The packet fixes:

- one worktree strategy note;
- one artifact policy note;
- one commit-cadence note;
- one acceptance note keeping dirty root `main` untouched during this wave; and
- one explicit split between compact in-git summaries and raw row dumps that
  stay out of git by default, with `uv` as the default execution path.
