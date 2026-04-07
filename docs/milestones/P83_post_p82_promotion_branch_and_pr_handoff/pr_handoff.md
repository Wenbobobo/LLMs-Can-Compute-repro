# PR Handoff

- promotion branch: `wip/p83-post-p82-promotion-branch-and-pr-handoff`
- source branch: `wip/p81-post-p80-clean-descendant-promotion-prep`
- base ref: `origin/main`
- current promotion head: `c9603c1`
- verification command:
  `uv run pytest tests/test_export_release_preflight_checklist_audit.py tests/test_export_p10_submission_archive_ready.py tests/test_export_p81_post_p80_locked_fact_rebaseline_and_route_sync.py tests/test_export_p82_post_p81_clean_main_promotion_probe.py -q`
- guardrails:
  no dirty-root integration
  runtime remains closed
  scientific route remains explicit stop
