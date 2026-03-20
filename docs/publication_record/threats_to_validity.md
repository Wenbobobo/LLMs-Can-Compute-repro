# Threats to Validity

- The public source is a field note, not a complete artifact release.
- Current staged-neural success still depends on stronger legality masks, and
  the broader `M4-D` suite strengthens that caveat rather than weakening it:
  the cleaned `opcode_shape` failure taxonomy is split between `push_expr_0`
  memory-value mismatches and `step_budget` nontermination, and the provenance
  follow-up shows those `step_budget` rows are downstream effects of earlier
  semantic errors rather than an independent failure family.
- Current real-trace precision evidence is broader than the original offset
  suite, but it still remains a narrow current-suite claim rather than a
  general long-horizon robustness result.
- Standard softmax baselines are informative negative controls, but they do not
  prove that no other learned executor branch could exist.
- The broadened precision suite still reports only `tie_collapse`; this is a
  useful boundary signal, but it is not yet a rich multi-mode failure theory.
- The first compiled frontend is intentionally narrowed to avoid importing
  unsupported language/runtime semantics too early.
- The current `D0` slice is a boundary check, not a compiler generalization
  result. Its exact agreement on the starter suite, plus its appendix-level
  memory-surface diagnostics, should not be inflated into a claim about
  arbitrary source languages or broader runtimes.
- The first explicit systems gate still separates mechanism from system value:
  current geometry evidence is strong, but current-scope end-to-end timing does
  not show the lowered path beating the best current reference/oracle path.
- The reopened `R11` geometry re-audit strengthens mechanism evidence, not
  end-to-end same-endpoint systems evidence; the preserved standalone cache
  benchmark should not be read as a runtime-bridge result.
- The reopened `R12` executor re-audit remains bounded to the currently staged
  `R6/R8` families and current exported modes; it does not establish
  unseen-family executor robustness or justify a broader trainable-executor
  claim.
