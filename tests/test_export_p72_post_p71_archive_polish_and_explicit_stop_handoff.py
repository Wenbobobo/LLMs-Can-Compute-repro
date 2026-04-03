from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p72_post_p71_archive_polish_and_explicit_stop_handoff.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p72_post_p71_archive_polish_and_explicit_stop_handoff",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p72_writes_archive_polish_and_explicit_stop_handoff_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p71_summary = _write_json(
        "p71_summary.json",
        {
            "summary": {
                "selected_outcome": "clean_descendant_merge_prep_readiness_mapped_without_merge_execution"
            }
        },
    )
    temp_preflight_summary = _write_json(
        "preflight_summary.json",
        {"summary": {"preflight_state": "docs_and_audits_green"}},
    )
    temp_p10_summary = _write_json(
        "p10_summary.json",
        {"summary": {"packet_state": "archive_ready"}},
    )
    temp_readme = _write_text(
        "README.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "explicit stop",
            "no further action",
            "wip/p72-post-p71-archive-polish-stop-handoff",
        ],
    )
    temp_status = _write_text(
        "STATUS.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "explicit stop",
            "no further action",
            "wip/p72-post-p71-archive-polish-stop-handoff",
        ],
    )
    temp_docs_readme = _write_text(
        "docs_readme.md",
        [
            "H65 + P73 + P74/P75/P76 + P72 + P69/P70/P71 + P56/P57/P58/P59 + F38",
            "plans/README.md",
            "milestones/README.md",
        ],
    )
    temp_milestones = _write_text(
        "milestones_readme.md",
        [
            "P74_post_p73_successor_publication_review",
            "P75_post_p74_published_successor_freeze",
            "P76_post_p75_release_hygiene_and_control_rebaseline",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P69_post_h65_repo_graph_hygiene_inventory",
        ],
    )
    temp_plans = _write_text(
        "plans_readme.md",
        [
            "2026-04-02-post-p71-archive-polish-stop-handoff-design.md",
            "2026-04-02-post-p72-next-planmode-handoff.md",
            "2026-04-02-post-p72-next-planmode-startup-prompt.md",
            "2026-04-02-post-p72-next-planmode-brief-prompt.md",
        ],
    )
    temp_publication_readme = _write_text(
        "publication_readme.md",
        [
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "current archive polish and explicit stop handoff wave",
            "P74_post_p73_successor_publication_review",
            "P75_post_p74_published_successor_freeze",
            "P76_post_p75_release_hygiene_and_control_rebaseline",
            "current published successor promotion stack",
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "hygiene-only control sidecars",
        ],
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p74-post-p73-successor-publication-review",
            "wip/p75-post-p74-published-successor-freeze",
            "P74_post_p73_successor_publication_review",
            "P75_post_p74_published_successor_freeze",
            "P76_post_p75_release_hygiene_and_control_rebaseline",
            "explicit stop",
            "no further action",
            "later clean-descendant merge-prep planning only if a new external integration need appears",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "wip/p69-post-h65-hygiene-only-cleanup",
            "wip/p74-post-p73-successor-publication-review",
            "wip/p75-post-p74-published-successor-freeze",
            "wip/p56-main-scratch",
            "wip/p56-main-scratch...wip/p75-post-p74-published-successor-freeze = 0/18",
            "origin/main...wip/p75-post-p74-published-successor-freeze = 0/159",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_release_preflight = _write_text(
        "release_preflight_checklist.md",
        [
            "P72 hygiene-only archive-polish and explicit-stop handoff sidecar",
            "P69/P70/P71 hygiene-only cleanup sidecars",
            "P74/P75/P76 successor promotion stack",
            "H58 as the value-negative closeout",
            "H43 as the preserved paper-grade endpoint",
            "explicit stop or no further action",
        ],
    )
    temp_release_candidate = _write_text(
        "release_candidate_checklist.md",
        [
            "H65/P56/P57/P58/P59/P74/P75/P76/F38",
            "P72 as the current archive-polish explicit-stop handoff sidecar",
            "P69/P70/P71 as hygiene-only cleanup sidecars",
            "do not widen the evidence ladder",
            "explicit stop or no further action",
        ],
    )
    temp_submission_candidate = _write_text(
        "submission_candidate_criteria.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "P71_post_p70_clean_descendant_merge_prep_readiness_sync",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P76_post_p75_release_hygiene_and_control_rebaseline",
            "P75_post_p74_published_successor_freeze",
            "P74_post_p73_successor_publication_review",
            "H58_post_r62_origin_value_boundary_closeout_packet",
            "H43_post_r44_useful_case_refreeze",
            "explicit stop or no further action",
            "do not authorize a runtime reopen",
        ],
    )
    temp_packet_index = _write_text(
        "submission_packet_index.md",
        [
            "P72/P71/P70/P69 entries below are hygiene-only control sidecars",
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P72_post_p71_archive_polish_and_explicit_stop_handoff",
            "results/P72_post_p71_archive_polish_and_explicit_stop_handoff/summary.json",
            "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
            "results/P75_post_p74_published_successor_freeze/summary.json",
            "results/P74_post_p73_successor_publication_review/summary.json",
            "do not widen the paper-facing evidence bundle",
        ],
    )
    temp_manifest = _write_text(
        "archival_repro_manifest.md",
        [
            "P72/P71/P70/P69 summaries below are hygiene-only control sidecars",
            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
            "results/P72_post_p71_archive_polish_and_explicit_stop_handoff/summary.json",
            "results/P71_post_p70_clean_descendant_merge_prep_readiness_sync/summary.json",
            "results/P70_post_p69_archive_index_and_artifact_policy_sync/summary.json",
            "results/P69_post_h65_repo_graph_hygiene_inventory/summary.json",
            "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
            "results/P75_post_p74_published_successor_freeze/summary.json",
            "results/P74_post_p73_successor_publication_review/summary.json",
            "do not change the paper-facing evidence boundary selected by H65",
        ],
    )
    temp_release_summary = _write_text(
        "release_summary_draft.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P72",
            "P69/P70/P71",
            "P74/P75/P76",
            "archive-first terminal freeze",
            "explicit stop",
            "no further action",
        ],
    )
    temp_review_boundary = _write_text(
        "review_boundary_summary.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P72",
            "P69/P70/P71",
            "P74/P75/P76",
            "narrow positive mechanism support survives",
            "dormant no-go dossier at F38",
            "explicit stop",
            "no further action",
        ],
    )
    temp_handoff = _write_text(
        "post_p72_handoff.md",
        [
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "explicit stop",
            "no further action",
            "later clean-descendant merge-prep planning only if a new external integration need appears",
            "wip/p56-main-scratch",
            "clean_descendant_only_never_dirty_root_main",
            "runtime remains closed",
        ],
    )
    temp_startup = _write_text(
        "post_p72_startup.md",
        [
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "explicit stop",
            "no further action",
            "later clean-descendant merge-prep planning only if a new external integration need appears",
            "wip/p56-main-scratch",
            "clean_descendant_only_never_dirty_root_main",
            "runtime remains closed",
        ],
    )
    temp_brief = _write_text(
        "post_p72_brief.md",
        [
            "wip/p72-post-p71-archive-polish-stop-handoff",
            "explicit stop",
            "no further action",
            "later clean-descendant merge-prep planning only if a new external integration need appears",
            "wip/p56-main-scratch",
            "dirty-root integration remains out of bounds",
        ],
    )
    temp_stop_handoff = _write_text(
        "stop_handoff.md",
        [
            "explicit stop",
            "no further action",
            "later clean-descendant merge-prep planning only if a new external integration need appears",
            "runtime remains closed",
            "dirty root main remains quarantine-only",
            "no new evidence-bearing packet is introduced",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p71 = module.P71_SUMMARY_PATH
    original_preflight = module.PREFLIGHT_SUMMARY_PATH
    original_p10 = module.P10_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_readme = module.ROOT_README_PATH
    original_status = module.STATUS_PATH
    original_docs_readme = module.DOCS_README_PATH
    original_milestones = module.MILESTONES_README_PATH
    original_plans = module.PLANS_README_PATH
    original_publication = module.PUBLICATION_README_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    original_release_preflight = module.RELEASE_PREFLIGHT_CHECKLIST_PATH
    original_release_candidate = module.RELEASE_CANDIDATE_CHECKLIST_PATH
    original_submission_candidate = module.SUBMISSION_CANDIDATE_CRITERIA_PATH
    original_packet_index = module.SUBMISSION_PACKET_INDEX_PATH
    original_manifest = module.ARCHIVAL_MANIFEST_PATH
    original_release_summary = module.RELEASE_SUMMARY_PATH
    original_review_boundary = module.REVIEW_BOUNDARY_PATH
    original_handoff = module.POST_P72_HANDOFF_PATH
    original_startup = module.POST_P72_STARTUP_PATH
    original_brief = module.POST_P72_BRIEF_PATH
    original_stop_handoff = module.STOP_HANDOFF_PATH

    temp_out_dir = tmp_path / "P72_post_p71_archive_polish_and_explicit_stop_handoff"
    module.OUT_DIR = temp_out_dir
    module.P71_SUMMARY_PATH = temp_p71_summary
    module.PREFLIGHT_SUMMARY_PATH = temp_preflight_summary
    module.P10_SUMMARY_PATH = temp_p10_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.ROOT_README_PATH = temp_readme
    module.STATUS_PATH = temp_status
    module.DOCS_README_PATH = temp_docs_readme
    module.MILESTONES_README_PATH = temp_milestones
    module.PLANS_README_PATH = temp_plans
    module.PUBLICATION_README_PATH = temp_publication_readme
    module.BRANCH_REGISTRY_PATH = temp_registry
    module.RELEASE_PREFLIGHT_CHECKLIST_PATH = temp_release_preflight
    module.RELEASE_CANDIDATE_CHECKLIST_PATH = temp_release_candidate
    module.SUBMISSION_CANDIDATE_CRITERIA_PATH = temp_submission_candidate
    module.SUBMISSION_PACKET_INDEX_PATH = temp_packet_index
    module.ARCHIVAL_MANIFEST_PATH = temp_manifest
    module.RELEASE_SUMMARY_PATH = temp_release_summary
    module.REVIEW_BOUNDARY_PATH = temp_review_boundary
    module.POST_P72_HANDOFF_PATH = temp_handoff
    module.POST_P72_STARTUP_PATH = temp_startup
    module.POST_P72_BRIEF_PATH = temp_brief
    module.STOP_HANDOFF_PATH = temp_stop_handoff

    monkeypatch.setattr(module, "current_branch", lambda: "wip/p72-post-p71-archive-polish-stop-handoff")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P71_SUMMARY_PATH = original_p71
        module.PREFLIGHT_SUMMARY_PATH = original_preflight
        module.P10_SUMMARY_PATH = original_p10
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.ROOT_README_PATH = original_readme
        module.STATUS_PATH = original_status
        module.DOCS_README_PATH = original_docs_readme
        module.MILESTONES_README_PATH = original_milestones
        module.PLANS_README_PATH = original_plans
        module.PUBLICATION_README_PATH = original_publication
        module.BRANCH_REGISTRY_PATH = original_registry
        module.RELEASE_PREFLIGHT_CHECKLIST_PATH = original_release_preflight
        module.RELEASE_CANDIDATE_CHECKLIST_PATH = original_release_candidate
        module.SUBMISSION_CANDIDATE_CRITERIA_PATH = original_submission_candidate
        module.SUBMISSION_PACKET_INDEX_PATH = original_packet_index
        module.ARCHIVAL_MANIFEST_PATH = original_manifest
        module.RELEASE_SUMMARY_PATH = original_release_summary
        module.REVIEW_BOUNDARY_PATH = original_review_boundary
        module.POST_P72_HANDOFF_PATH = original_handoff
        module.POST_P72_STARTUP_PATH = original_startup
        module.POST_P72_BRIEF_PATH = original_brief
        module.STOP_HANDOFF_PATH = original_stop_handoff

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_polish_surfaces_normalized_and_explicit_stop_handoff_frozen_without_scope_widening"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] > 0

