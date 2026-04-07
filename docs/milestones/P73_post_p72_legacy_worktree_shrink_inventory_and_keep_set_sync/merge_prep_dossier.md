# Merge-Prep Dossier

This file is read-only planning support. It does not authorize merge
execution.

Only admissible later route if a new external integration need appears:

- start from `wip/p56-main-scratch`
- target `wip/p75-post-p74-published-successor-freeze`
- keep `wip/p72-post-p71-archive-polish-stop-handoff` as a preserved archive
  handoff branch, not the published branch
- keep `wip/p73-post-p72-hygiene-shrink-mergeprep` as local hygiene/dossier
  control only
- keep `wip/p74-post-p73-successor-publication-review` as review provenance
  only
- never route any integration work through dirty root `main`

Guardrails:

- merge posture remains `clean_descendant_only_never_dirty_root_main`
- runtime remains closed
- same-lane executor-value work remains closed
- broad Wasm, arbitrary `C`, and transformed/trainable entry remain out of
  scope
- `P71` already captured the non-executing merge-readiness fact; no merge is
  executed here
