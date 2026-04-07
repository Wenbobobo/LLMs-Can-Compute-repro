# Post-H36 R41 Runtime Relevance Threat Design

This design saves one deferred future runtime-audit surface after the landed
`H35 -> R40 -> H36 -> P24` wave. It does not authorize execution by itself.

## Objective

Stress the two surviving same-substrate threat families from `F14` against the
now-landed bounded-scalar result in `R40`:

- `runtime_irrelevance_via_compiler_helper_overencoding`
- `fast_path_only_helps_the_easy_part`

The point is not to reopen scope by momentum. The point is to predeclare the
smallest future audit that could falsify the narrow `H36` interpretation on the
same substrate if a later explicit packet decides that the threat is worth
executing.

## Approaches Considered

### Option A: helper-only audit

Only test helper/control-surface overencoding candidates.

Pros:

- smallest future execution packet;
- easiest attribution if it fails.

Cons:

- leaves the easy-part-only threat unresolved;
- risks another near-term reopen just to answer the second caution.

### Option B: one bounded dual-threat audit on fixed rows

Keep one future `R41` lane, but lock it to the two `R40` rows, the two `F14`
threat families, and the predeclared perturbation catalog.

Pros:

- answers both remaining cautions without widening row scope or family scope;
- preserves one future audit lane instead of multiplying packet count;
- matches the current `H36` interpretation that no runtime lane is active now,
  but one deferred threat design may be saved.

Cons:

- requires slightly richer planning upfront.

### Option C: split future lanes by threat family

Create separate future runtime lanes for overencoding and easy-part-only.

Pros:

- the cleanest attribution surface if either lane ever activates.

Cons:

- unnecessary packet proliferation at the current evidence level;
- increases the risk of activation-by-inventory rather than activation-by-need.

Recommendation:

- choose Option B.

## Future Packet Order

If this lane is ever activated later, the order must be:

1. one new explicit post-`H36` docs-only decision packet authorizes only
   `R41_origin_runtime_relevance_threat_stress_audit`;
2. `R41_origin_runtime_relevance_threat_stress_audit` executes only the fixed
   bounded audit described here;
3. one later explicit refreeze packet interprets the local result.

This design intentionally does not pre-name the future authorization or
refreeze packet. The scope lock matters more than the future packet id.

## Fixed Scope

`R41` may touch only the landed `R40` positive rows:

- admitted row:
  `bytecode_bounded_scalar_flag_loop_6_a320`
  (`case_id = bounded_scalar_admitted`);
- boundary row:
  `bytecode_bounded_scalar_flag_loop_long_12_a336`
  (`case_id = bounded_scalar_boundary`).

The family and substrate lock must remain:

- `bounded scalar locals and flags` only;
- same append-only / exact-retrieval / small-VM substrate;
- same opcode surface as `R40`:
  `add_i32`, `const_i32`, `eq_i32`, `halt`, `jmp`, `jz_zero`,
  `load_static`, `store_static`, `sub_i32`;
- no new family, aggregate payload, heap escape, external effect, or new
  opcode.

The declared `R40` negative controls remain context only. `R41` does not
re-open them as primary evidence.

## Candidate Audit Shapes

Allowed candidate ids are inherited from `F14` and remain the complete catalog:

- `helper_annotation_ablation_or_canonicalization`
- `control_surface_neutralization_without_semantic_change`
- `retrieval_critical_vs_local_easy_step_contrast_slicing`

Threat mapping:

- the first two target
  `runtime_irrelevance_via_compiler_helper_overencoding`;
- the third targets `fast_path_only_helps_the_easy_part`.

No new candidate family may be added inside `R41`.

## Measurement Rules

The baseline is fixed to the landed `R40` artifacts.

Every candidate must preserve:

- the same row identity;
- the same opcode surface;
- the same source meaning;
- the same lowered semantics.

Every candidate must record at least:

- source-reference exactness;
- lowered-interpreter exactness;
- accelerated free-running trace match;
- accelerated free-running final-state match;
- stack/memory/call read counts.

The slice-based candidate must additionally record one predeclared
retrieval-critical slice and one predeclared local-easy slice on the same row.

Allowed future verdicts:

- `keep_h36_freeze`:
  no uniquely isolated contradiction survives the fixed measurement rules;
- `mixed_nonunique`:
  some stress appears, but it is not unique or it breaks the scope lock;
- `runtime_relevance_threat_isolated`:
  one candidate preserves source meaning and lowered semantics while isolating
  a same-row contradiction tied to one of the two allowed threat families.

## Stop Rules

`R41` must stop immediately if any candidate:

- requires a new opcode or richer value family;
- requires a new substrate or external runtime comparator;
- changes source meaning instead of stressing runtime relevance;
- cannot predeclare the slice pair mechanically on the same row;
- needs more than the fixed admitted row plus the fixed boundary row.

The future audit should also stop after the first uniquely isolated
contradiction. It is a threat stress, not a broad candidate sweep.

## Required Future Outputs

If `R41` is ever activated, it must emit:

- one execution manifest;
- one candidate-row table;
- one threat-measurement table;
- one summary with the verdict labels above;
- one explicit stop-rule record.

## Non-Goals

This design does not authorize:

- restricted-Wasm work;
- arbitrary `C` rhetoric;
- general LLM-computer rhetoric;
- hybrid planner/executor runtime work;
- broader compiler or family widening;
- any automatic runtime lane after `H36`.
