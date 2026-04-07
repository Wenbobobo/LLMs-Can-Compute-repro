# F7 Post-H34 Reopen Trigger Specification Bundle

Planning-only trigger-specification bundle downstream of the landed
`H32 -> H33 -> R39 -> H34` chain and the completed `F5/F6` closeout.

`F7` exists to specify what a future contradiction-driven same-substrate reopen
packet would need to name before any runtime work could become discussable
again. It does not authorize execution, does not create an `H35`-style packet,
and does not weaken the current saved state:

- `H32` remains the active routing/refreeze packet;
- `H34` remains the current docs-only control packet;
- `F5` remains concluded at `no_reopen_candidate_survives`;
- `F6` remains concluded at
  `hold_no_reopen_freeze_and_continue_docs_or_planning_only_work`;
- there is no active downstream runtime lane.

This bundle is a specification surface only. Its role is to prevent later
planning from drifting into vague "maybe reopen" language by requiring that
any future reopen story arrive as one explicit, contradiction-led packet with a
predeclared comparator set, fixed success/failure rule, and explicit stop
condition.
