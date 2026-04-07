# Post-R48 H47 Useful-Case Bridge Refreeze Design

## Objective

`H47_post_r48_useful_case_bridge_refreeze` is the required docs-only
interpretation packet after landed comparator-only `R48`.

The packet stays deliberately narrow:

- exact `R46/R47` evidence remains decisive;
- `R48` stays comparator-only and non-substitutive;
- the paper-grade endpoint remains preserved `H43`; and
- broader Wasm/C, broader hybrid executor work, and merge-to-`main` remain
  out of scope.

## Locked Inputs

- current active docs-only packet before `H47`:
  `H46_post_r47_frontend_bridge_decision_packet`;
- preserved prior decision packet:
  `H45_post_r46_surface_decision_packet`;
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`;
- preserved prior exact runtime gate:
  `R46_origin_useful_case_surface_generalization_gate`;
- current exact frontend bridge gate:
  `R47_origin_restricted_frontend_translation_gate`;
- current comparator-only useful-case model gate:
  `R48_origin_dual_mode_useful_case_model_gate`;
- current exact-first planning bundle:
  `F21_post_h43_exact_useful_case_expansion_bundle`; and
- current comparator-planning bundle:
  `F22_post_r46_useful_case_model_bridge_bundle`.

## Decision

`H47` chooses exactly one outcome:

- selected outcome:
  `freeze_r48_as_narrow_comparator_support_only`;
- non-selected alternative:
  `treat_r48_as_scope_widening_authorization`.

The landed `R48` result is positive, but it is still downstream of exact
`R46/R47` and still bounded to the preserved useful-case contract. That means
the scientifically honest interpretation is not “continue by momentum,” but
“freeze the comparator result explicitly and return the stack to no active
downstream runtime lane.”

## Machine-State Consequences

- `active_stage = h47_post_r48_useful_case_bridge_refreeze`
- `preserved_prior_docs_only_decision_packet = h46_post_r47_frontend_bridge_decision_packet`
- `current_paper_grade_endpoint = h43_post_r44_useful_case_refreeze`
- `current_completed_post_h44_exact_runtime_gate = r46_origin_useful_case_surface_generalization_gate`
- `current_completed_exact_frontend_bridge_gate = r47_origin_restricted_frontend_translation_gate`
- `current_completed_comparator_only_useful_case_model_gate = r48_origin_dual_mode_useful_case_model_gate`
- `selected_outcome = freeze_r48_as_narrow_comparator_support_only`
- `claim_ceiling = bounded_useful_cases_only`
- `next_required_lane = no_active_downstream_runtime_lane`
- `no_active_downstream_runtime_lane`
- `later_explicit_packet_required_before_scope_widening = true`

## Acceptance

- `H47` remains docs-only;
- `H46` becomes the preserved prior docs-only decision packet;
- `H43` remains the paper-grade endpoint;
- `R48` remains comparator-only rather than substitutive;
- exact `R46/R47` evidence remains decisive; and
- no downstream runtime, broader Wasm/C, hybrid growth, or merge wave is
  authorized here.

## Rejected

Rejected: momentum-based widening from comparator evidence.
