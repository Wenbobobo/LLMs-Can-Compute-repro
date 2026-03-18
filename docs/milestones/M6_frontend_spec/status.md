# Status

Spec now has a fixed execution boundary and should be treated as
implementation-ready at the contract level.

Current blocker summary:
- the typed-bytecode verifier, lowering contract, and stress suite must stay
  consistent with the current `M4` claim freeze and the `D0` wording that will
  be locked in `P3_paper_freeze_and_evidence_mapping`;
- the first implementation batch now exists under `src/bytecode/`, and the
  paper bundle already has a rendered boundary diagram under
  `results/P1_paper_readiness/m6_frontend_boundary_diagram.svg`;
- later frontend broadening remains blocked until
  `R2_systems_baseline_gate` and
  `M7_frontend_candidate_decision` both close positively.
