# P8 Submission Candidate and Bundle Lock Design

## Context

`P7` already fixed the freeze-candidate package. What remains is not another
scope decision. It is a consistency and submission-readiness pass over the same
frozen scope.

## Goal

Turn the current freeze-candidate checkpoint into a submission-candidate bundle
without widening claims, reopening experiments, or letting outward summaries
outrun the paper-facing ledgers.

## Required Outputs

- one milestone scaffold under
  `docs/milestones/P8_submission_candidate_and_bundle_lock/`;
- explicit submission-candidate criteria on top of the existing freeze package;
- one decision-complete handoff for manuscript, appendix, and ledger lock
  lanes;
- synchronized paper-facing ledgers naming the submission-candidate target.

## Acceptance

- the current manuscript, captions, narrative roles, section map, and appendix
  boundary can be treated as a locked bundle candidate;
- the current claim/evidence bundle is synchronized enough to hand to a later
  release-candidate pass;
- any mismatch is surfaced as a real reopen trigger rather than papered over
  with wording.
