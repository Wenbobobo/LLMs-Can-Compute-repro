# R51 Execution Manifest

- run only from a clean descendant worktree of the post-`H49` line;
- keep exact source/interpreter, lowered replay/reference, and accelerated
  exact executor visible separately;
- keep case count bounded and predeclared before execution;
- export row-level exactness and first-fail artifacts; and
- do not add hidden helper state to "make the lane pass".
