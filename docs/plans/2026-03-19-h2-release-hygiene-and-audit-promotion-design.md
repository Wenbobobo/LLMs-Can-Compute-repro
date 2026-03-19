# H2 Release Hygiene and Audit Promotion Design

## Context

The repo already has narrow public-surface and callout audits, but the current
post-`P7` stage still relies on human memory to keep the manuscript bundle,
release controls, and conditional reopen rules aligned.

## Goal

Promote the current post-`P7` governance package into a machine-audited
standing gate so unattended runs can keep the bundle locked without reopening
scope by drift.

## Required Outputs

- one milestone scaffold under
  `docs/milestones/H2_release_hygiene_and_audit_promotion/`;
- one new machine-readable bundle-lock / release-hygiene audit export with a
  matching test;
- synchronized publication docs for submission-candidate criteria,
  release-candidate checklist, and conditional reopen protocol;
- one experiment-manifest row recording the new standing gate.

## Acceptance

- post-`P7` release governance is inspectable through docs plus audit outputs;
- unattended runs no longer need to infer reopen discipline from scattered
  prose;
- the new audit stays narrow and does not pretend to validate scientific
  claims, only bundle-lock and release hygiene.
