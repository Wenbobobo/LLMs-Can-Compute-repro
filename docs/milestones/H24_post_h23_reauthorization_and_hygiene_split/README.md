# H24 Post-H23 Reauthorization And Hygiene Split

Operational split stage after landed `H23` and completed downstream `P14`.

`H24` exists to separate three concerns that should not be mixed in the same
batch:

- the already-frozen `H23` scientific state;
- the post-`H23` reauthorization packet for deciding what science lane, if any,
  still deserves execution;
- the standing dirty-tree / commit-split hygiene problem.

`H24` does not reopen science by itself. It prepares a bounded
`R30 + R31 -> H25` decision packet while keeping `R29` and `F3` blocked.
