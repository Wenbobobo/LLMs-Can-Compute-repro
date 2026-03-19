# H1 Legacy Backlog Reconciliation Design

## Context

The repository now has a frozen paper scope and a completed `P6`
layout/readiness pass, but multiple older milestone `todo.md` files still
contain unchecked items. Some of those rows were superseded by later freezes,
some now belong to deliberately frozen negative-control branches, and some are
only candidates for a future evidence-wave reopen. Leaving them unclassified
creates a real unattended-execution risk because future agents may misread them
as active work.

## Goal

Create one narrow reconciliation lane that classifies every currently unchecked
legacy row without reopening the underlying work. The output should let future
agents distinguish active work from frozen history immediately.

## Required outputs

- one milestone scaffold under
  `docs/milestones/H1_legacy_backlog_reconciliation/`;
- one classification matrix covering every currently unchecked legacy row;
- short legacy notes at the top of affected historical `todo.md` files that
  point readers to the classification matrix;
- one manifest entry recording the reconciliation as a docs/hygiene batch.

## Classification rules

Use only the following dispositions:

- `active_now`
- `frozen_negative_control`
- `superseded_by_scope_freeze`
- `conditional_future_reopen`

Every row must also record a short rationale and, when relevant, the explicit
condition that would justify reopening it.

## Acceptance

- every current unchecked legacy row has exactly one disposition;
- historical `todo.md` files no longer look silently active;
- future unattended agents can tell which rows are live, frozen, or only
  conditionally reopenable without rereading the full project history.
