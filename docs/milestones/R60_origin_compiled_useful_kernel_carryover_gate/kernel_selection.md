# Kernel Selection

The first carryover pass should stay below the preserved `R44` three-kernel
ladder.

Chosen initial kernels:

- `sum_i32_buffer`
- `count_nonzero_i32_buffer`

Reasons:

- both are already preserved useful-kernel shapes in the repo;
- both exercise nontrivial buffer traversal and accumulation behavior;
- both avoid introducing the wider bucket-update and aliasing pressure of
  `histogram16_u8`; and
- together they answer the smallest useful-kernel question without widening the
  carryover surface prematurely.

Excluded in this first pass:

- `histogram16_u8`

Reason for exclusion:

- it is a legitimate later useful-family candidate, but it adds update-shape
  pressure that would make first-fail interpretation less clean if the goal of
  this wave is merely to decide whether the compiled-boundary route carries any
  preserved useful kernel at all.
