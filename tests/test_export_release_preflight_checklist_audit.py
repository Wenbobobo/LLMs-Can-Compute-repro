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
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`explicit_stop_or_no_further_action_archive_first`",
        ],
    )
    _write_rel_text(
        "STATUS.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
        ],
    )
    _write_rel_text(
        "docs/README.md",
        [
            "publication_record/current_stage_driver.md",
            "branch_worktree_registry.md",
            "live",
            "historical",
            "dormant",
        ],
    )
    _write_rel_text(
        "docs/publication_record/README.md",
        [
            "H66_post_p90_archive_replace_terminal_stop_packet",
            "P91_post_h66_next_planmode_handoff_sync",
            "P90_post_p89_archive_replace_screen_and_replacement_decision",
            "current_stage_driver.md",
            "future_reopen_screen.md",
        ],
    )
    _write_rel_text(
        "docs/publication_record/current_stage_driver.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`explicit_stop_or_no_further_action_archive_first`",
        ],
    )
    _write_rel_text(
        "docs/plans/README.md",
        [
            "2026-04-07-post-h66-next-planmode-handoff.md",
            "2026-04-07-post-h66-next-planmode-startup-prompt.md",
            "2026-04-07-post-h66-next-planmode-brief-prompt.md",
            "P91_post_h66_next_planmode_handoff_sync",
            "H66_post_p90_archive_replace_terminal_stop_packet",
            "P90_post_p89_archive_replace_screen_and_replacement_decision",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_summary_draft.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "explicit stop",
            "archive polish",
            "no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_preflight_checklist.md",
        [
            "`H66/P91/P90/P77/P78/P79/P80`",
            "`P72` hygiene-only archive-polish and explicit-stop handoff sidecar",
            "`P69/P70/P71` hygiene-only cleanup sidecars",
            "`H65/P90` as the immediate prior closeout lineage",
            "explicit stop or no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_candidate_checklist.md",
        [
            "`H66/P91/P90/H65/P56/P57/P58/P59/P77/P78/P79/P80/F38`",
            "preserved `H64/H58/H43`",
            "explicit stop or no further action",
            "no outward wording implies a new runtime lane",
        ],
    )
    _write_rel_text(
        "docs/publication_record/submission_candidate_criteria.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`H58_post_r62_origin_value_boundary_closeout_packet`",
            "`H43_post_r44_useful_case_refreeze`",
            "explicit stop or no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/claim_ladder.md",
        [
            "| H66 Archive-replace terminal stop packet |",
            "| P91 Next-planmode handoff sync |",
            "| P90 Archive-replace screen and replacement decision |",
        ],
    )
    _write_rel_text(
        "docs/publication_record/archival_repro_manifest.md",
        [
            "results/H66_post_p90_archive_replace_terminal_stop_packet/summary.json",
            "results/P91_post_h66_next_planmode_handoff_sync/summary.json",
            "results/P90_post_p89_archive_replace_screen_and_replacement_decision/summary.json",
            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
        ],
    )
    _write_rel_text(
        "docs/publication_record/paper_bundle_status.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`F38_post_h62_r63_dormant_eligibility_profile_dossier`",
        ],
    )
    _write_rel_text(
        "docs/publication_record/review_boundary_summary.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "explicit stop",
            "no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/external_release_note_skeleton.md",
        [
            "`H66_post_p90_archive_replace_terminal_stop_packet`",
            "`P91_post_h66_next_planmode_handoff_sync`",
            "`P90_post_p89_archive_replace_screen_and_replacement_decision`",
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "archive-replace terminal stop",
            "strongest justified executor-value lane is closed negative",
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
        "results/H66_post_p90_archive_replace_terminal_stop_packet/summary.json",
        {
            "summary": {
                "selected_outcome": "archive_replace_terminal_stop_becomes_current_active_route_and_defaults_to_explicit_stop"
            }
        },
    )
    _write_rel_json(
        "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
        {
            "summary": {
                "selected_outcome": "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop"
            }
        },
    )
    _write_rel_json(
        "results/P91_post_h66_next_planmode_handoff_sync/summary.json",
        {"summary": {"selected_outcome": "next_planmode_handoff_synced_to_explicit_stop_after_h66"}},
    )
    _write_rel_json(
        "results/P90_post_p89_archive_replace_screen_and_replacement_decision/summary.json",
        {"summary": {"selected_outcome": "archive_replace_screen_completed_with_no_additional_salvage_after_p89"}},
    )
    _write_rel_json(
        "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
        {"summary": {"selected_outcome": "archive_claim_boundary_and_reopen_screen_locked_after_convergence"}},
    )
    _write_rel_json(
        "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
        {"summary": {"selected_outcome": "next_planmode_handoff_synced_to_explicit_stop_after_p79"}},
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
        {"summary": {"runtime_authorization": "closed"}},
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
    assert "H66 remains the current active docs-only packet" in payload["summary"]["recommended_next_action"]
    assert "P91/P90 remain the current terminal-stop and handoff stack" in payload["summary"]["recommended_next_action"]
    assert "explicit stop or no further action remains the recommended downstream route" in payload["summary"]["recommended_next_action"]


def test_publication_record_readme_mentions_current_terminal_stop_stack() -> None:
    text = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "publication_record"
        / "README.md"
    ).read_text(encoding="utf-8")

    assert "../milestones/H66_post_p90_archive_replace_terminal_stop_packet/" in text
    assert "../milestones/P91_post_h66_next_planmode_handoff_sync/" in text
    assert "../milestones/P90_post_p89_archive_replace_screen_and_replacement_decision/" in text
