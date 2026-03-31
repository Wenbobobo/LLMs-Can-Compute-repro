from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_release_preflight_checklist_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_release_preflight_checklist_audit",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_release_preflight_checklist_audit_summary(tmp_path: Path) -> None:
    module = _load_module()

    def _write_rel_text(rel_path: str, lines: list[str]) -> None:
        path = tmp_path / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _write_rel_json(rel_path: str, payload: dict[str, object]) -> None:
        path = tmp_path / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    _write_rel_text(
        "README.md",
        [
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
            "`P63_post_p62_published_successor_promotion_prep`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P65_post_p64_merge_prep_control_sync`",
            "`wip/p63-post-p62-tight-core-hygiene`",
            "`archive_or_hygiene_stop`",
        ],
    )
    _write_rel_text(
        "STATUS.md",
        [
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
            "`P63_post_p62_published_successor_promotion_prep`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P65_post_p64_merge_prep_control_sync`",
            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
        ],
    )
    _write_rel_text(
        "docs/README.md",
        [
            "publication_record/current_stage_driver.md",
            "branch_worktree_registry.md",
            "F38_post_h62_r63_dormant_eligibility_profile_dossier",
            "live",
            "historical",
            "dormant",
        ],
    )
    _write_rel_text(
        "docs/publication_record/README.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "published successor clean-descendant promotion-prep wave",
        ],
    )
    _write_rel_text(
        "docs/publication_record/current_stage_driver.md",
        [
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
            "`P63_post_p62_published_successor_promotion_prep`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P65_post_p64_merge_prep_control_sync`",
            "`wip/p63-post-p62-tight-core-hygiene`",
            "`archive_or_hygiene_stop`",
        ],
    )
    _write_rel_text(
        "docs/plans/README.md",
        [
            "2026-04-01-post-p63-successor-merge-prep-design.md",
            "2026-04-01-post-p65-next-planmode-handoff.md",
            "2026-04-01-post-p65-next-planmode-startup-prompt.md",
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_summary_draft.md",
        [
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
            "`P56/P57/P58/P59`",
            "`P63/P64/P65`",
            "`wip/p63-post-p62-tight-core-hygiene`",
            "archive-first partial falsification",
            "R63 remains dormant, non-runtime",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_preflight_checklist.md",
        [
            "`P63/P64/P65` published successor stack",
            "`P56/P57/P58/P59/F38` foundation",
            "`H58` as the value-negative closeout",
            "`H43` as the preserved paper-grade endpoint",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_candidate_checklist.md",
        [
            "`H64/P56/P57/P58/P59/P63/P64/P65/F38`",
            "preserved `H58/H43`",
            "No outward wording implies a new runtime lane",
        ],
    )
    _write_rel_text(
        "docs/publication_record/submission_candidate_criteria.md",
        [
            "`P63_post_p62_published_successor_promotion_prep`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P65_post_p64_merge_prep_control_sync`",
            "`H58_post_r62_origin_value_boundary_closeout_packet`",
            "`H43_post_r44_useful_case_refreeze`",
        ],
    )
    _write_rel_text(
        "docs/publication_record/claim_ladder.md",
        [
            "| P63 Published successor promotion prep |",
            "| P64 Release hygiene rebaseline |",
            "| P65 Merge-prep control sync |",
        ],
    )
    _write_rel_text(
        "docs/publication_record/archival_repro_manifest.md",
        [
            "results/P63_post_p62_published_successor_promotion_prep/summary.json",
            "results/P64_post_p63_release_hygiene_rebaseline/summary.json",
            "results/P65_post_p64_merge_prep_control_sync/summary.json",
            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
        ],
    )
    _write_rel_text(
        "docs/publication_record/paper_bundle_status.md",
        [
            "`P63_post_p62_published_successor_promotion_prep`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P65_post_p64_merge_prep_control_sync`",
            "archive-first partial-falsification closeout framing",
        ],
    )
    _write_rel_text(
        "docs/publication_record/review_boundary_summary.md",
        [
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
            "`P56/P57/P58/P59`",
            "narrow positive mechanism support survives",
            "the only remaining future route is a dormant no-go dossier at `F38`",
        ],
    )
    _write_rel_text(
        "docs/publication_record/external_release_note_skeleton.md",
        [
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
            "`P56/P57/P58/P59`",
            "`H43_post_r44_useful_case_refreeze`",
            "`H58_post_r62_origin_value_boundary_closeout_packet`",
            "dormant non-runtime `F38` dossier",
        ],
    )
    _write_rel_text(
        "docs/publication_record/blog_release_rules.md",
        [
            "release_candidate_checklist.md",
            "blog stays blocked unless all of the following are true",
            "no arbitrary C",
            "no broad “LLMs are computers” framing",
        ],
    )
    _write_rel_json(
        "results/P1_paper_readiness/summary.json",
        {
            "figure_table_status_summary": {"by_status": [{"status": "ready", "count": 10}]},
            "blocked_or_partial_items": [],
        },
    )
    _write_rel_json(
        "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
        {
            "summary": {
                "selected_outcome": "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
            }
        },
    )
    _write_rel_json(
        "results/P63_post_p62_published_successor_promotion_prep/summary.json",
        {"summary": {"selected_outcome": "published_successor_promotion_prep_locked_after_p62"}},
    )
    _write_rel_json(
        "results/P56_post_h64_clean_merge_candidate_packet/summary.json",
        {"summary": {"selected_outcome": "clean_descendant_merge_candidate_staged_without_merge_execution"}},
    )
    _write_rel_json(
        "results/P57_post_h64_paper_submission_package_sync/summary.json",
        {"summary": {"selected_outcome": "paper_submission_package_surfaces_synced_to_h64_followthrough_stack"}},
    )
    _write_rel_json(
        "results/P58_post_h64_archive_release_closeout_sync/summary.json",
        {"summary": {"selected_outcome": "archive_release_closeout_surfaces_synced_to_h64_followthrough_stack"}},
    )
    _write_rel_json(
        "results/P59_post_h64_control_and_handoff_sync/summary.json",
        {"summary": {"selected_outcome": "control_and_handoff_surfaces_synced_to_h64_followthrough_stack"}},
    )
    _write_rel_json(
        "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
        {
            "summary": {
                "selected_outcome": "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields",
                "runtime_authorization": "closed",
            }
        },
    )
    _write_rel_json(
        "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
        {"summary": {"selected_outcome": "stop_as_mechanism_supported_but_no_bounded_executor_value"}},
    )
    _write_rel_json(
        "results/H43_post_r44_useful_case_refreeze/summary.json",
        {"summary": {"claim_d_state": "supported_here_narrowly"}},
    )
    _write_rel_json("results/P5_public_surface_sync/summary.json", {"summary": {"blocked_count": 0}})
    _write_rel_json("results/P5_callout_alignment/summary.json", {"summary": {"blocked_count": 0}})
    _write_rel_json("results/H2_bundle_lock_audit/summary.json", {"summary": {"blocked_count": 0}})
    _write_rel_json(
        "results/release_worktree_hygiene_snapshot/summary.json",
        {
            "summary": {
                "release_commit_state": "clean_worktree_ready_if_other_gates_green",
                "git_diff_check_state": "clean",
            }
        },
    )
    _write_rel_json(
        "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
        {"summary": {"runtime_classification": "healthy_but_slow", "timed_out_file_count": 0}},
    )

    original_root = module.ROOT
    original_out_dir = module.OUT_DIR
    module.ROOT = tmp_path
    module.OUT_DIR = tmp_path / "release_preflight_checklist_audit"
    try:
        module.main()
    finally:
        module.ROOT = original_root
        module.OUT_DIR = original_out_dir

    payload = json.loads((tmp_path / "release_preflight_checklist_audit" / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["preflight_state"] == "docs_and_audits_green"
    assert payload["summary"]["blocked_count"] == 0
