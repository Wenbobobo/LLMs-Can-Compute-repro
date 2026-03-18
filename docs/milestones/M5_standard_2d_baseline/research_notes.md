# Research Notes

- The blog's tiny PyTorch snippet is too ambiguous to count as evidence by
  itself, but it is still the right starting point for a comparison branch.
- The baseline needs its own data representation. Reusing `M4` conclusions while
  changing tokenization later would make the comparison noisy.
- Torch should remain optional until this branch becomes an active execution
  target. The current checkpoint is a scaffold, not a validated baseline.
