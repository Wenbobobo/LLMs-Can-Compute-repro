# H13 Post-H12 Rollover Design

## Goal

Prepare the repo for the next bounded stage after the completed
`H10/H11/R8/R9/R10/H12` packet without silently reopening scope.

## Options

### Option A: governance-only rollover plus validation hygiene

Keep the completed same-endpoint packet as the latest refrozen evidence state,
stage one successor driver in docs only, and route the unresolved full-suite
`pytest -q` runtime issue into a bounded validation-hygiene lane.

Recommendation: use this option. It preserves the current no-widening decision,
keeps the scientific scope fixed, and turns the remaining operational gap into
an explicit artifact instead of letting it drift.

### Option B: immediately open another same-endpoint science lane

Treat the completed `H12` packet as only an intermediate stop and activate a
new `D0` science lane now.

Not recommended. The current packet did not expose a contradiction, `M7`
explicitly kept widening blocked, and the next unresolved issue is validation
hygiene rather than a missing claim-bearing experiment.

### Option C: move directly to paper/blog finishing work

Stop opening any new operational lanes and spend the next unattended rounds
only on derivative manuscript or release assets.

Not recommended as the primary next wave. Downstream writing can continue, but
the repo still needs a clear post-`H12` handoff and a bounded answer for the
slow or non-returning full-suite validation gate.

## Intended outputs

- one saved post-`H12` execution plan in `tmp/`;
- one `H13` milestone scaffold for the next driver transition;
- one `V1` milestone scaffold for full-suite validation runtime audit;
- minimal root-doc touch-ups that clarify `H12` is closed without widening the
  public claim surface.

## Scope lock

- do not activate a new science lane by wording alone;
- do not weaken `M7` no-widening or `P4` blog-blocked decisions;
- do not treat validation-hygiene work as new scientific evidence.

## Acceptance

- the repo contains one explicit post-`H12` plan and milestone scaffolds for
  the next bounded operational wave;
- the unresolved full-suite validation issue is recorded as a bounded audit
  lane rather than an implicit blocker;
- the completed `H10/H11/R8/R9/R10/H12` packet remains preserved as the latest
  refrozen same-endpoint evidence state.
