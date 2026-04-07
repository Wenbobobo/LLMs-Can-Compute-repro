# Execution Manifest

## Scope Lock

- fixed tiny typed-bytecode `D0` endpoint only;
- reuse the landed `R30` candidate core exactly;
- keep the four approved axes only:
  `unique_address_target`,
  `horizon_multiplier`,
  `checkpoint_depth`,
  `hot_address_skew`;
- do not reopen the historical full grid or add new families.

## Candidate Core

| Family anchor | Current ceiling anchor | Role in `R32` |
| --- | --- | --- |
| `checkpoint_replay_long/u32/h3.0/plus_two/flattened` | hardest surviving replay-style row | primary long-family stress anchor |
| `helper_checkpoint_braid_long/u20/h3.0/plus_two/flattened` | hardest surviving long braid helper row | primary long-family control-flow anchor |
| `subroutine_braid_long/u20/h3.0/plus_two/flattened` | hardest surviving long subroutine row | primary long-family call/control anchor |
| `helper_checkpoint_braid/u8/h2.0/plus_one/flattened` | shorter helper continuity anchor | neighboring exact confirmation anchor |
| `subroutine_braid/u6/h2.0/plus_one/flattened` | shorter subroutine continuity anchor | neighboring exact confirmation anchor |

## First-Pass Zoom Ladder

| Anchor class | `unique_address_target` | `horizon_multiplier` | `checkpoint_depth` | `hot_address_skew` order |
| --- | --- | --- | --- | --- |
| long-family anchors | current ceiling `+4`, then `+8` | current ceiling `+0.5`, then `+1.0` | one notch beyond current ceiling | `flattened` first, `baseline` only as nearby confirmation |
| continuity anchors | current ceiling `+2`, then `+4` | current ceiling `+0.5`, then `+1.0` | one notch beyond current ceiling | `flattened` first, `baseline` only as nearby confirmation |

The lane should push one axis at a time on a branch before stacking multiple
new maxima. The first preferred order per branch is:

1. `unique_address_target`
2. `horizon_multiplier`
3. `checkpoint_depth`
4. nearby `hot_address_skew` confirmation around any reproduced failure

## Stop Rules

- stop a branch after `2` reproduced exactness failures;
- stop the whole lane if every candidate-core branch either fails cleanly or
  exhausts the predeclared ladder without a failure;
- require one `first_fail` plus at least one neighboring exact row before any
  claim of boundary localization;
- if no failure appears, end with a principled no-localization verdict rather
  than opening another expansion wave by momentum.

## Verdict Vocabulary

- `first_boundary_failure_localized`
- `near_boundary_mixed_signal_needs_confirmation`
- `grid_extended_still_not_localized`
- `resource_limited_before_localization`

## Required Outputs

- `manifest_rows.json`
- `boundary_rows.json`
- `branch_summary.json`
- `positive_rows.json`
- `failure_rows.json`
- `first_fail_digest.json`
- `neighbor_exact_rows.json`
- `localized_boundary.json`
- `summary.json`

## Must Be Explicit Before Execution

- the candidate core remains unchanged from `R30`;
- the ladder above is saved as the only authorized first pass;
- the stop rules remain unchanged from `R30`;
- no fifth axis, no new family, and no wider endpoint is introduced.
