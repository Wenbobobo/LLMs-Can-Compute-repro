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
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P77_post_p76_keep_set_and_provenance_normalization`",
            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
            "`P80_post_p79_next_planmode_handoff_sync`",
            "`wip/p75-post-p74-published-successor-freeze`",
            "`explicit_stop_or_no_further_action_archive_first`",
        ],
    )
    _write_rel_text(
        "STATUS.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P77_post_p76_keep_set_and_provenance_normalization`",
            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
            "`P80_post_p79_next_planmode_handoff_sync`",
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
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P77_post_p76_keep_set_and_provenance_normalization",
            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
            "P80_post_p79_next_planmode_handoff_sync",
            "partial_falsification_boundary.md",
            "future_reopen_screen.md",
        ],
    )
    _write_rel_text(
        "docs/publication_record/current_stage_driver.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P77_post_p76_keep_set_and_provenance_normalization`",
            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
            "`P80_post_p79_next_planmode_handoff_sync`",
            "`P74_post_p73_successor_publication_review`",
            "`wip/p75-post-p74-published-successor-freeze`",
            "`explicit_stop_or_no_further_action_archive_first`",
            "explicit stop",
            "no further action",
        ],
    )
    _write_rel_text(
        "docs/plans/README.md",
        [
            "2026-04-05-post-p76-hygiene-first-convergence-design.md",
            "2026-04-05-post-p80-next-planmode-handoff.md",
            "2026-04-05-post-p80-next-planmode-startup-prompt.md",
            "2026-04-05-post-p80-next-planmode-brief-prompt.md",
            "P77_post_p76_keep_set_and_provenance_normalization",
            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
            "P80_post_p79_next_planmode_handoff_sync",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_summary_draft.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P72`",
            "`P56/P57/P58/P59`",
            "`P66/P67/P68`",
            "`wip/p75-post-p74-published-successor-freeze`",
            "archive-first terminal freeze",
            "R63 remains dormant, non-runtime",
            "explicit stop",
            "no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_preflight_checklist.md",
        [
            "`H65/P77/P78/P79/P80`",
            "`P72` hygiene-only archive-polish and explicit-stop handoff sidecar",
            "`P69/P70/P71` hygiene-only cleanup sidecars",
            "`P74/P75/P76` as the immediate publication lineage",
            "`H64/P56/P57/P58/P59/F38` foundation",
            "`H58` as the value-negative closeout",
            "`H43` as the preserved paper-grade endpoint",
            "explicit stop or no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/release_candidate_checklist.md",
        [
            "`H65/P56/P57/P58/P59/P77/P78/P79/P80/F38`",
            "`P74/P75/P76` remain preserved immediate publication lineage",
            "`P72` remains the current archive-polish explicit-stop handoff sidecar",
            "`P69/P70/P71` remain hygiene-only cleanup sidecars",
            "preserved `H64/H58/H43`",
            "no outward wording implies a new runtime lane",
            "explicit stop or no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/submission_candidate_criteria.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P77_post_p76_keep_set_and_provenance_normalization`",
            "`P78_post_p77_legacy_worktree_convergence_and_quarantine_sync`",
            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
            "`P80_post_p79_next_planmode_handoff_sync`",
            "`P71_post_p70_clean_descendant_merge_prep_readiness_sync`",
            "`P70_post_p69_archive_index_and_artifact_policy_sync`",
            "`P69_post_h65_repo_graph_hygiene_inventory`",
            "`P76_post_p75_release_hygiene_and_control_rebaseline`",
            "`H58_post_r62_origin_value_boundary_closeout_packet`",
            "`H43_post_r44_useful_case_refreeze`",
            "do not authorize a runtime reopen",
            "explicit stop or no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/claim_ladder.md",
        [
            "| P79 Archive claim boundary and reopen screen |",
            "| P80 Next-planmode handoff sync |",
            "| P74/P75/P76 Immediate publication lineage |",
        ],
    )
    _write_rel_text(
        "docs/publication_record/archival_repro_manifest.md",
        [
            "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
            "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
            "results/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/summary.json",
            "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json",
            "results/P72_post_p71_archive_polish_and_explicit_stop_handoff/summary.json",
            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
            "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
        ],
    )
    _write_rel_text(
        "docs/publication_record/paper_bundle_status.md",
        [
            "`P79_post_p78_archive_claim_boundary_and_reopen_screen`",
            "`P80_post_p79_next_planmode_handoff_sync`",
            "`P74_post_p73_successor_publication_review`",
            "`P76_post_p75_release_hygiene_and_control_rebaseline`",
            "archive-first terminal-freeze and explicit-stop framing",
        ],
    )
    _write_rel_text(
        "docs/publication_record/review_boundary_summary.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P79/P80`",
            "`P56/P57/P58/P59`",
            "`P74/P75/P76`",
            "narrow positive mechanism support survives",
            "the only remaining future route is a dormant no-go dossier at `F38` unless a",
            "explicit stop",
            "no further action",
        ],
    )
    _write_rel_text(
        "docs/publication_record/external_release_note_skeleton.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P79/P80`",
            "`P56/P57/P58/P59`",
            "`H64_post_p53_p54_p55_f38_archive_first_freeze_packet`",
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
        "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
        {
            "summary": {
                "selected_outcome": "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop"
            }
        },
    )
    _write_rel_json(
        "results/P74_post_p73_successor_publication_review/summary.json",
        {"summary": {"selected_outcome": "successor_publication_review_supports_p75_freeze"}},
    )
    _write_rel_json(
        "results/P75_post_p74_published_successor_freeze/summary.json",
        {"summary": {"selected_outcome": "published_successor_freeze_locked_after_p74_review"}},
    )
    _write_rel_json(
        "results/P76_post_p75_release_hygiene_and_control_rebaseline/summary.json",
        {"summary": {"selected_outcome": "published_successor_release_hygiene_and_control_rebaselined_after_p75"}},
    )
    _write_rel_json(
        "results/P77_post_p76_keep_set_and_provenance_normalization/summary.json",
        {"summary": {"selected_outcome": "keep_set_and_provenance_normalized_after_p76"}},
    )
    _write_rel_json(
        "results/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/summary.json",
        {"summary": {"selected_outcome": "balanced_worktree_convergence_completed_with_quarantines_preserved"}},
    )
    _write_rel_json(
        "results/P79_post_p78_archive_claim_boundary_and_reopen_screen/summary.json",
        {"summary": {"selected_outcome": "archive_claim_boundary_and_reopen_screen_locked_after_convergence"}},
    )
    _write_rel_json(
        "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
        {"summary": {"selected_outcome": "next_planmode_handoff_synced_to_explicit_stop_after_p79"}},
    )
    _write_rel_json("results/P56_post_h64_clean_merge_candidate_packet/summary.json", {"summary": {"selected_outcome": "clean_descendant_merge_candidate_staged_without_merge_execution"}})
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
    assert "P72/P69/P70/P71 remain hygiene-only archive/control sidecars" in payload["summary"]["recommended_next_action"]
    assert "P77/P78/P79/P80 remain the current archive-facing control stack" in payload["summary"]["recommended_next_action"]
    assert "P74/P75/P76 remain the preserved immediate publication lineage" in payload["summary"]["recommended_next_action"]
    assert "P66/P67/P68 remain the preserved prior successor stack" in payload["summary"]["recommended_next_action"]
    assert "explicit stop or no further action is now the recommended downstream route" in payload["summary"]["recommended_next_action"]


def test_publication_record_readme_mentions_current_archive_facing_stack() -> None:
    text = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "publication_record"
        / "README.md"
    ).read_text(encoding="utf-8")

    assert "../milestones/P77_post_p76_keep_set_and_provenance_normalization/" in text
    assert "../milestones/P78_post_p77_legacy_worktree_convergence_and_quarantine_sync/" in text
    assert "../milestones/P79_post_p78_archive_claim_boundary_and_reopen_screen/" in text
    assert "../milestones/P80_post_p79_next_planmode_handoff_sync/" in text

