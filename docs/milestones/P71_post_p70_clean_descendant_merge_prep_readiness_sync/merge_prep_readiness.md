# Merge-Prep Readiness

- `wip/p56-main-scratch` remains the only clean local integration base
- `wip/p66-post-p65-published-successor-freeze` remains the live published
  clean descendant
- the read-only merge probe is:
  `git merge-tree <merge-base> wip/p56-main-scratch wip/p66-post-p65-published-successor-freeze`
- the probe records no content-conflict markers at this phase
- merge execution remains absent
- dirty root `main` remains quarantine-only and cannot become a merge base here
