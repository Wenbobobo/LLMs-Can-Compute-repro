# Research Notes

- The Discuss files are consistent that Sudoku and Hungarian are downstream
  packaging, not the scientific core.
- "Arbitrary C" remains a rhetorical claim until the supported subset is pinned
  down and tested against a reference runtime.
- The first `M6` target should be a narrow frontend that stresses the execution
  substrate without importing undefined behavior, floating point, or OS-level
  effects.
