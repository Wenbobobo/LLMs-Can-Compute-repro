# Worktree Runbook

## Purpose

This runbook exists so a later promotion attempt does not need to rediscover
the mechanics of the clean-prep policy.

## Recommended Future Flow

1. start from `wip/p25-f15-h37-exec`, not dirty `main`;
2. confirm the prep branch remains reviewably scoped;
3. re-run the packet-local exporters and focused tests;
4. inspect `git diff --stat main..wip/p25-f15-h37-exec`;
5. split a later promotion commit only if the path set is still too broad;
6. merge only after `main` is clean enough for a reviewable fast-forward or
   explicit packetized promotion.

## Guardrails

- do not commit from dirty `main`;
- do not mix future runtime experiments into the promotion packet;
- do not use `P25` as justification to activate `R41`;
- do not widen public claims while the promotion packet is still operational.
