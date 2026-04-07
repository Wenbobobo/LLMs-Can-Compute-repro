# Post-H47 P35 Research Record Rollup Design

## Objective

`P35_post_h47_research_record_rollup` is the first low-priority operational
packet after landed `H47`.

The packet is intentionally narrow:

- it does not change scientific stage;
- it does not authorize a runtime lane;
- it does not merge to `main`; and
- it does not repackage comparator-only `R48` as broader support.

Instead it records the current post-`H47` state cleanly enough that later
runtime or closeout work can proceed from a stable control surface.

## Locked Inputs

- current active docs-only packet:
  `H47_post_r48_useful_case_bridge_refreeze`
- current paper-grade endpoint:
  `H43_post_r44_useful_case_refreeze`
- current exact-first planning bundle:
  `F21_post_h43_exact_useful_case_expansion_bundle`
- current comparator-planning bundle:
  `F22_post_r46_useful_case_model_bridge_bundle`
- explicit merge packet:
  `P27_post_h41_clean_promotion_and_explicit_merge_packet`
- preserved prior helper refresh packets:
  `P31`, `P32`, `P33`, and `P34`

## Deliverables

`P35` must land:

- one post-`H47` artifact inventory;
- one root-dirty quarantine note for root `main`;
- one push-state note recording the clean baseline branch;
- one explicit merge-posture note;
- one negative-result rollup; and
- one exporter-backed `summary/checklist/claim_packet/snapshot` bundle.

## Acceptance

- `P35` remains docs-only and low-priority;
- `H47` remains current and `H43` remains the paper-grade endpoint;
- `P35` becomes the current low-priority operational/docs wave;
- `P31/P32/P33/P34` become preserved prior helper refresh packets;
- dirty root `main` is recorded and quarantined, not rewritten;
- raw artifacts above `10 MiB` remain out of git by default; and
- the next required lane becomes
  `F23_post_h47_numeric_scaling_bundle`.
