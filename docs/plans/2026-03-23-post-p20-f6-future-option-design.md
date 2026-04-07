# 2026-03-23 Post-P20 F6 Future Option Design

## Summary

After the completed `P20` manuscript resync and completed `F5` contradiction
scout, the repo needs one more planning-only surface:

- `F6_post_p20_future_option_matrix`

This lane does not reopen the science stack. It records which future moves are
actually admissible from the current `H32/H34` state and which remain blocked
or conditional.

## Why Land F6

`F5` answers a narrow question:

- does a unique same-substrate contradiction currently survive?

Its answer is:

- `no_reopen_candidate_survives`

That still leaves a broader operational question for later unattended work:

- if no reopen is justified now, what kinds of future work are still legitimate
  from this state?

Without an explicit option matrix, later agents can drift into one of two bad
patterns:

1. reopen by momentum because no immediate runtime lane exists;
2. over-freeze the repo and forget that planning-only or operational work is
   still legitimate.

## Required Outputs

`F6` should remain planning-only and produce:

- one future-option matrix;
- one ranked near-term option list;
- one operational note covering worktrees, subagents, and merge discipline;
- the explicit default state:
  `hold_no_reopen_freeze_and_continue_docs_or_planning_only_work`.

## Option Classes

`F6` should distinguish five option classes:

1. docs-only or publication-system maintenance;
2. planning-only future gating or frontier review preparation;
3. contradiction-driven same-substrate reopen, conditional only;
4. broader scope lift / new substrate / arbitrary-`C` widening, blocked;
5. operational merge or promotion work, orthogonal to scientific routing.

## Default Selection

Selected default:

- preserve the `H34` no-reopen state;
- allow docs-only and planning-only follow-up;
- keep runtime execution inactive by default;
- keep merge/promotion optional and operational rather than scientific.

Not selected:

- create a new runtime packet by default;
- widen the compiler line;
- treat `F6` as a substitute for a future contradiction packet.

## Save Rule

Save this design before creating the milestone bundle.

- keep the lane planning-only;
- keep any future runtime behind a later explicit packet;
- if later work splits, prefer fresh worktrees and disjoint subagent scopes.
