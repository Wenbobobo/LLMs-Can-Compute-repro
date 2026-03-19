# Blog Release Rules

This file converts the current blocked-blog state into explicit release rules.

## Blog stays blocked unless all of the following are true

1. The manuscript bundle satisfies `freeze_candidate_criteria.md`.
2. `release_preflight_checklist.md` is fully green.
3. The derivative blog text is sourced from the frozen manuscript bundle and
   the approved short `release_summary_draft.md`, not from a parallel
   speculative narrative lane.
4. The blog keeps the current narrow endpoint explicit:
   append-only traces, exact retrieval, bounded precision, mixed systems gate,
   and `D0` as the compiled stop point.
5. The blog preserves the current blocked claims explicitly:
   no arbitrary C, no broad “LLMs are computers” framing, no current-scope
   systems-superiority claim, and no frontend widening.

## Automatic re-block conditions

- any new evidence wave reopens precision, systems, or compiled scope;
- a public-surface sync starts using wording that is not traceable to the
  manuscript bundle or release summary;
- the repo no longer satisfies the current public-surface or callout audits.
