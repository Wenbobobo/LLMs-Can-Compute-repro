# P35 Post-H47 Research Record Rollup

Completed low-priority operational/docs rollup packet after the post-`H47`
stack returned to `no_active_downstream_runtime_lane`.

`P35` does not alter the active scientific stage. It preserves
`H47_post_r48_useful_case_bridge_refreeze` as the current docs-only packet,
preserves `H43_post_r44_useful_case_refreeze` as the paper-grade endpoint,
preserves `F21` and `F22` as the current planning surfaces, and records the
operational state needed for the next narrow planning question.

The packet fixes five things explicitly:

- one artifact inventory with a `>10 MiB` default out-of-git policy;
- one root-dirty quarantine note for dirty root `main`;
- one push-state note recording the saved clean `r48` baseline branch;
- one explicit merge-posture note keeping `main` untouched; and
- one negative-result rollup so later waves do not forget why same-endpoint
  recovery, broad system claims, and momentum-based widening remain blocked.
