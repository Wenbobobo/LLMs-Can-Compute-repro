# Branch And Worktree Registry

This file records the balanced mounted keep set, quarantine posture, preserved
lineage refs, and cleanup priorities for the clean-descendant-only repo state
after the `P84` keep-set closeout above the `H65` terminal freeze.

## Balanced Mounted Keep Set

| Role | Branch | Path | State | Policy |
| --- | --- | --- | --- | --- |
| current promotion-ready execution branch | `wip/p83-post-p82-promotion-branch-and-pr-handoff` | `D:/zWenbo/AI/wt/p83-post-p82-promotion-branch-and-pr-handoff` | current clean promotion-ready branch after the `P82` probe and `P83` handoff | keep mounted during `P84` and any follow-on promotion/PR finalization; do not treat as the published branch |
| current published clean descendant | `wip/p75-post-p74-published-successor-freeze` | `D:/zWenbo/AI/wt/p75-post-p74-published-successor-freeze` | live clean publication/control branch | keep mounted and tracked; use as the active clean descendant |
| current successor publication review branch | `wip/p74-post-p73-successor-publication-review` | `D:/zWenbo/AI/wt/p74-post-p73-successor-publication-review` | current review/provenance lane preserved beside the published branch | keep mounted; do not treat as the published branch |
| current local hygiene and shrink branch | `wip/p73-post-p72-hygiene-shrink-mergeprep` | `D:/zWenbo/AI/wt/p73-post-p72-hygiene-shrink-mergeprep` | current local cleanup, shrink, and dossier-prep lane | keep mounted; local follow-through only |
| current archive-polish explicit-stop handoff branch | `wip/p72-post-p71-archive-polish-stop-handoff` | `D:/zWenbo/AI/wt/p72-post-p71-archive-polish-stop-handoff` | current docs/export/control handoff lane | keep mounted; archive-facing control only |
| current hygiene-only cleanup branch | `wip/p69-post-h65-hygiene-only-cleanup` | `D:/zWenbo/AI/wt/p69-post-h65-hygiene-only-cleanup` | current hygiene-only execution lane | keep mounted; do not widen scope |
| preserved local integration base | `wip/p56-main-scratch` | `D:/zWenbo/AI/wt/p56-main-scratch` | preserved local integration ancestry only | keep mounted; never treat as live published control |
| dirty-root quarantine | `wip/root-main-parking-2026-03-24` | `D:/zWenbo/AI/LLMCompute` | operationally dirty root checkout | quarantine only; never use as a clean integration base |
| blocked dirty legacy quarantine | `wip/h27-promotion` | `D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion` | blocked historical dirty worktree | keep mounted only until separately resolved or archived |

## Preserved But Expected Unmounted

| Role | Branch | Last known path | Policy |
| --- | --- | --- | --- |
| preserved prior published clean descendant | `wip/p66-post-p65-published-successor-freeze` | `D:/zWenbo/AI/wt/p66-post-p65-published-successor-freeze` | preserve branch ref and provenance; unmounted is acceptable after convergence |
| preserved locked-fact rebaseline lineage | `wip/p81-post-p80-clean-descendant-promotion-prep` | `D:/zWenbo/AI/wt/p81-post-p80-clean-descendant-promotion-prep` | preserve branch ref and immediate promotion-prep provenance; remain unmounted after `P84` |
| preserved clean-main probe lineage | `wip/p82-post-p81-clean-main-promotion-probe` | `D:/zWenbo/AI/wt/p82-post-p81-clean-main-promotion-probe` | preserve branch ref and clean-main probe provenance; remain unmounted after `P84` |
| preserved deeper prior successor review branch | `wip/p64-post-p63-successor-stack` | `D:/zWenbo/AI/wt/p64-post-p63-successor-stack` | preserve branch ref as deeper review lineage; unmounted is acceptable after convergence |
| preserved deeper prior published clean descendant | `wip/p63-post-p62-tight-core-hygiene` | `D:/zWenbo/AI/wt/p63-post-p62-tight-core-hygiene` | preserve branch ref as deeper publication lineage; unmounted is acceptable after convergence |
| preserved older published clean descendant | `wip/p60-post-p59-published-clean-descendant-prep` | `D:/zWenbo/AI/wt/p60-post-p59-published-clean-descendant-prep` | preserve branch ref only; historical lineage |
| preserved archive-first packet lineage | `wip/h64-post-h63-archive-first-freeze`, `wip/f38-post-h62-archive-first-closeout`, `wip/f37-post-h61-hygiene-first-reauth-prep`, `wip/f36-post-h60-archive-first-consolidation`, `wip/f34-post-h59-archive-and-reopen-screen`, `wip/f32-post-h56-last-discriminator`, `wip/r33-next` | historical `D:/zWenbo/AI/wt/` and `D:/zWenbo/AI/LLMCompute-worktrees/` locations | preserve refs or archived outputs only; remove clean legacy mounts |

## Cleanup Status

- the active mounted keep set for the current phase is `p83`, `p75`, `p74`,
  `p73`, `p72`, `p69`, and `p56`
- the temporary `p81` and `p82` worktrees were intentionally removed in `P84`
  and now survive only as preserved unmounted lineage
- only the dirty root checkout and `wip/h27-promotion` should remain dirty and
  mounted after convergence
- clean historical mounts targeted for removal are:
  `wip/r33-next`,
  `wip/f32-post-h56-last-discriminator`,
  `wip/f34-post-h59-archive-and-reopen-screen`,
  `wip/f36-post-h60-archive-first-consolidation`,
  `wip/f37-post-h61-hygiene-first-reauth-prep`,
  `wip/f38-post-h62-archive-first-closeout`,
  `wip/h64-post-h63-archive-first-freeze`,
  `wip/p60-post-p59-published-clean-descendant-prep`,
  `wip/p63-post-p62-tight-core-hygiene`,
  `wip/p64-post-p63-successor-stack`,
  `wip/p66-post-p65-published-successor-freeze`
- live work should prefer `D:/zWenbo/AI/wt/` as the current execution prefix

## Merge Rules

- merge posture remains `clean_descendant_only_never_dirty_root_main`
- `wip/p83-post-p82-promotion-branch-and-pr-handoff` is the current
  promotion-ready branch for clean-descendant promotion/PR finalization only
- `wip/p75-post-p74-published-successor-freeze` is the live published clean
  source for current control wording
- `wip/p81-post-p80-clean-descendant-promotion-prep` and
  `wip/p82-post-p81-clean-main-promotion-probe` remain preserved immediate
  promotion-prep lineage, expected unmounted after `P84`
- `wip/p74-post-p73-successor-publication-review` remains the current review
  and provenance lane
- `wip/p73-post-p72-hygiene-shrink-mergeprep` remains the current local
  hygiene and shrink lane
- `wip/p72-post-p71-archive-polish-stop-handoff` remains the current archive
  polish and explicit-stop handoff lane
- `wip/p69-post-h65-hygiene-only-cleanup` remains the current hygiene-only
  cleanup lane
- `wip/p56-main-scratch...wip/p75-post-p74-published-successor-freeze`
  remains the current clean-descendant-only promotion lineage fact
- `origin/main...wip/p83-post-p82-promotion-branch-and-pr-handoff` keeps
  dirty-root integration out of bounds
- runtime remains closed
- `F38/R63` remains dormant and non-runtime only
