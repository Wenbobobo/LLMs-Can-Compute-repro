# Todo

- Freeze `structural`, `opcode_shape`, and `opcode_legal` as the default
  baseline ladder.
- Add `flagged_indirect_accumulator` as a new held-out family.
- Add `selector_checkpoint_bank` as a second new held-out family.
- Record first-error step, head, class, reference label, and predicted label
  per failed program.
- Summarize failures by regime and by family before changing model capacity.
- Add exactly one extra intermediate regime only if held-out `opcode_shape`
  failures collapse strongly into one compatibility family.
- Close the milestone either with a stronger fair regime or with a negative
  interpretation that the current staged exactness still depends on mask
  strength.
