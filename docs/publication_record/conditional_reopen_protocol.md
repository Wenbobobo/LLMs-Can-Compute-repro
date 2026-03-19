# Conditional Reopen Protocol

State: `dormant_protocol`.

This file defines the only allowed way to reopen evidence after the current
post-`P7` stabilization package.

## Allowed triggers

A reopen may start only when at least one of the following is true:

1. a locked manuscript sentence conflicts with the claim/evidence table;
2. a main-text artifact pairing no longer matches the section map;
3. a required appendix companion is missing for a claim explicitly used in the
   manuscript;
4. a release or review requirement explicitly demands one missing evidence
   class that cannot be satisfied by wording or ledger cleanup alone.

## Patch lanes

Only one patch lane may be active at a time:

- `E1a_precision_patch`
- `E1b_systems_patch`
- `E1c_compiled_boundary_patch`

Each patch lane must name:

- the triggering conflict;
- the smallest artifact bundle needed to answer it;
- the specific claim row affected;
- the stop condition for returning to the locked paper/release lanes.

## Non-rules

- wording drift alone is not a valid reopen trigger;
- curiosity-driven widening is not a valid reopen trigger;
- no reopen may silently broaden to arbitrary C, broader systems superiority,
  or frontend widening.

## Refreeze requirement

Every `E1` patch ends by:

1. recording a result digest for the patch lane;
2. rerunning the relevant audits;
3. returning control to `P8` or `P9` on the same frozen endpoint unless a new
   deliberate scope decision says otherwise.
