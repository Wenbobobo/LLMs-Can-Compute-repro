"""Export the post-P71 archive-polish and explicit-stop handoff sidecar for P72."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P72_post_p71_archive_polish_and_explicit_stop_handoff"
P71_SUMMARY_PATH = ROOT / "results" / "P71_post_p70_clean_descendant_merge_prep_readiness_sync" / "summary.json"
PREFLIGHT_SUMMARY_PATH = ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
P10_SUMMARY_PATH = ROOT / "results" / "P10_submission_archive_ready" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ROOT_README_PATH = ROOT / "README.md"
STATUS_PATH = ROOT / "STATUS.md"
DOCS_README_PATH = ROOT / "docs" / "README.md"
MILESTONES_README_PATH = ROOT / "docs" / "milestones" / "README.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
RELEASE_PREFLIGHT_CHECKLIST_PATH = ROOT / "docs" / "publication_record" / "release_preflight_checklist.md"
RELEASE_CANDIDATE_CHECKLIST_PATH = ROOT / "docs" / "publication_record" / "release_candidate_checklist.md"
SUBMISSION_CANDIDATE_CRITERIA_PATH = ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md"
SUBMISSION_PACKET_INDEX_PATH = ROOT / "docs" / "publication_record" / "submission_packet_index.md"
ARCHIVAL_MANIFEST_PATH = ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"
RELEASE_SUMMARY_PATH = ROOT / "docs" / "publication_record" / "release_summary_draft.md"
REVIEW_BOUNDARY_PATH = ROOT / "docs" / "publication_record" / "review_boundary_summary.md"
POST_P72_HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-02-post-p72-next-planmode-handoff.md"
POST_P72_STARTUP_PATH = ROOT / "docs" / "plans" / "2026-04-02-post-p72-next-planmode-startup-prompt.md"
POST_P72_BRIEF_PATH = ROOT / "docs" / "plans" / "2026-04-02-post-p72-next-planmode-brief-prompt.md"
STOP_HANDOFF_PATH = ROOT / "docs" / "milestones" / "P72_post_p71_archive_polish_and_explicit_stop_handoff" / "stop_handoff.md"
CURRENT_BRANCH = "wip/p72-post-p71-archive-polish-stop-handoff"
PRESERVED_HYGIENE_BRANCH = "wip/p69-post-h65-hygiene-only-cleanup"
PUBLISHED_BRANCH = "wip/p66-post-p65-published-successor-freeze"
LOCAL_INTEGRATION_BRANCH = "wip/p56-main-scratch"
EXPECTED_P56_TO_P66_FACT = "0/18"
EXPECTED_ORIGIN_MAIN_TO_P66_FACT = "0/159"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p71_summary = read_json(P71_SUMMARY_PATH)["summary"]
    preflight_summary = read_json(PREFLIGHT_SUMMARY_PATH)["summary"]
    p10_summary = read_json(P10_SUMMARY_PATH)["summary"]
    if p71_summary["selected_outcome"] != "clean_descendant_merge_prep_readiness_mapped_without_merge_execution":
        raise RuntimeError("P72 expects the landed P71 clean-descendant readiness sidecar.")
    if preflight_summary["preflight_state"] != "docs_and_audits_green":
        raise RuntimeError("P72 expects standing release preflight to remain green.")
    if p10_summary["packet_state"] != "archive_ready":
        raise RuntimeError("P72 expects standing P10 archive readiness to remain green.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    root_readme_text = read_text(ROOT_README_PATH)
    status_text = read_text(STATUS_PATH)
    docs_readme_text = read_text(DOCS_README_PATH)
    milestones_readme_text = read_text(MILESTONES_README_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    release_preflight_text = read_text(RELEASE_PREFLIGHT_CHECKLIST_PATH)
    release_candidate_text = read_text(RELEASE_CANDIDATE_CHECKLIST_PATH)
    submission_candidate_text = read_text(SUBMISSION_CANDIDATE_CRITERIA_PATH)
    submission_packet_index_text = read_text(SUBMISSION_PACKET_INDEX_PATH)
    archival_manifest_text = read_text(ARCHIVAL_MANIFEST_PATH)
    release_summary_text = read_text(RELEASE_SUMMARY_PATH)
    review_boundary_text = read_text(REVIEW_BOUNDARY_PATH)
    handoff_text = read_text(POST_P72_HANDOFF_PATH)
    startup_text = read_text(POST_P72_STARTUP_PATH)
    brief_text = read_text(POST_P72_BRIEF_PATH)
    stop_handoff_text = read_text(STOP_HANDOFF_PATH)
    current_branch_name = current_branch()

    checklist_rows = [
        {"item_id": "p72_reads_p71", "status": "pass", "notes": "P72 runs only after P71 lands the clean-descendant readiness sidecar."},
        {"item_id": "p72_reads_standing_release_audits", "status": "pass", "notes": "P72 preserves the standing green preflight and archive-ready posture."},
        {
            "item_id": "p72_runs_on_current_branch",
            "status": "pass" if current_branch_name == CURRENT_BRANCH else "blocked",
            "notes": "P72 should run from the current archive-polish and explicit-stop handoff branch.",
        },
        {
            "item_id": "p72_root_readme_and_status_mention_current_sidecar",
            "status": "pass"
            if all(
                (
                    contains_all(root_readme_text, ["H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "P72_post_p71_archive_polish_and_explicit_stop_handoff", "P69_post_h65_repo_graph_hygiene_inventory", "P70_post_p69_archive_index_and_artifact_policy_sync", "P71_post_p70_clean_descendant_merge_prep_readiness_sync", "explicit stop", "no further action", CURRENT_BRANCH]),
                    contains_all(status_text, ["H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "P72_post_p71_archive_polish_and_explicit_stop_handoff", "P69_post_h65_repo_graph_hygiene_inventory", "P70_post_p69_archive_index_and_artifact_policy_sync", "P71_post_p70_clean_descendant_merge_prep_readiness_sync", "explicit stop", "no further action", CURRENT_BRANCH]),
                )
            )
            else "blocked",
            "notes": "README and STATUS should expose P72 as the current archive-polish explicit-stop handoff wave.",
        },
        {
            "item_id": "p72_docs_routers_and_indexes_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(docs_readme_text, ["H65 + P72 + P69/P70/P71 + P56/P57/P58/P59 + P66/P67/P68 + F38", "plans/README.md", "milestones/README.md"]),
                    contains_all(milestones_readme_text, ["P72_post_p71_archive_polish_and_explicit_stop_handoff", "P71_post_p70_clean_descendant_merge_prep_readiness_sync", "P70_post_p69_archive_index_and_artifact_policy_sync", "P69_post_h65_repo_graph_hygiene_inventory"]),
                    contains_all(plans_readme_text, ["2026-04-02-post-p71-archive-polish-stop-handoff-design.md", "2026-04-02-post-p72-next-planmode-handoff.md", "2026-04-02-post-p72-next-planmode-startup-prompt.md", "2026-04-02-post-p72-next-planmode-brief-prompt.md"]),
                )
            )
            else "blocked",
            "notes": "Docs routers and planning indexes should expose the P72 handoff stack and prompts.",
        },
        {
            "item_id": "p72_publication_and_branch_registry_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(publication_readme_text, ["P72_post_p71_archive_polish_and_explicit_stop_handoff", "current archive polish and explicit stop handoff wave", "P69_post_h65_repo_graph_hygiene_inventory", "P70_post_p69_archive_index_and_artifact_policy_sync", "P71_post_p70_clean_descendant_merge_prep_readiness_sync", "hygiene-only control sidecars"]),
                    contains_all(branch_registry_text, [CURRENT_BRANCH, PRESERVED_HYGIENE_BRANCH, PUBLISHED_BRANCH, f"{LOCAL_INTEGRATION_BRANCH}...{PUBLISHED_BRANCH} = {EXPECTED_P56_TO_P66_FACT}", f"origin/main...{PUBLISHED_BRANCH} = {EXPECTED_ORIGIN_MAIN_TO_P66_FACT}", "clean_descendant_only_never_dirty_root_main"]),
                )
            )
            else "blocked",
            "notes": "Publication router and branch registry should expose P72 while preserving clean-descendant-only posture.",
        },
        {
            "item_id": "p72_release_and_submission_surfaces_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(release_preflight_text, ["P72 hygiene-only archive-polish and explicit-stop handoff sidecar", "P69/P70/P71 hygiene-only cleanup sidecars", "P66/P67/P68 published frozen successor stack", "H58 as the value-negative closeout", "H43 as the preserved paper-grade endpoint", "explicit stop or no further action"]),
                    contains_all(release_candidate_text, ["H65/P56/P57/P58/P59/P66/P67/P68/F38", "P72 as the current archive-polish explicit-stop handoff sidecar", "P69/P70/P71 as hygiene-only cleanup sidecars", "do not widen the evidence ladder", "explicit stop or no further action"]),
                    contains_all(submission_candidate_text, ["H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "P72_post_p71_archive_polish_and_explicit_stop_handoff", "P71_post_p70_clean_descendant_merge_prep_readiness_sync", "P70_post_p69_archive_index_and_artifact_policy_sync", "P69_post_h65_repo_graph_hygiene_inventory", "H58_post_r62_origin_value_boundary_closeout_packet", "H43_post_r44_useful_case_refreeze", "explicit stop or no further action", "do not authorize a runtime reopen"]),
                )
            )
            else "blocked",
            "notes": "Release-facing and submission-facing docs should treat P72 as a hygiene-only handoff sidecar.",
        },
        {
            "item_id": "p72_archive_ledgers_and_summaries_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(submission_packet_index_text, ["P72/P71/P70/P69 entries below are hygiene-only control sidecars", "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "P72_post_p71_archive_polish_and_explicit_stop_handoff", "results/P72_post_p71_archive_polish_and_explicit_stop_handoff/summary.json", "do not widen the paper-facing evidence bundle"]),
                    contains_all(archival_manifest_text, ["P72/P71/P70/P69 summaries below are hygiene-only control sidecars", "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json", "results/P72_post_p71_archive_polish_and_explicit_stop_handoff/summary.json", "results/P71_post_p70_clean_descendant_merge_prep_readiness_sync/summary.json", "results/P70_post_p69_archive_index_and_artifact_policy_sync/summary.json", "results/P69_post_h65_repo_graph_hygiene_inventory/summary.json", "do not change the paper-facing evidence boundary selected by H65"]),
                    contains_all(release_summary_text, ["H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "P72", "P69/P70/P71", "archive-first terminal freeze", "explicit stop", "no further action"]),
                    contains_all(review_boundary_text, ["H65_post_p66_p67_p68_archive_first_terminal_freeze_packet", "P72", "P69/P70/P71", "narrow positive mechanism support survives", "dormant no-go dossier at F38", "explicit stop", "no further action"]),
                )
            )
            else "blocked",
            "notes": "Archive ledgers and boundary summaries should expose P72 without widening the evidence bundle.",
        },
        {
            "item_id": "p72_handoff_prompts_and_stop_doc_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(current_stage_driver_text, ["P72_post_p71_archive_polish_and_explicit_stop_handoff", CURRENT_BRANCH, PRESERVED_HYGIENE_BRANCH, PUBLISHED_BRANCH, "explicit stop", "no further action", "later clean-descendant merge-prep planning only if a new external integration need appears", "clean_descendant_only_never_dirty_root_main"]),
                    contains_all(handoff_text, [CURRENT_BRANCH, "explicit stop", "no further action", "later clean-descendant merge-prep planning only if a new external integration need appears", LOCAL_INTEGRATION_BRANCH, "clean_descendant_only_never_dirty_root_main", "runtime remains closed"]),
                    contains_all(startup_text, [CURRENT_BRANCH, "explicit stop", "no further action", "later clean-descendant merge-prep planning only if a new external integration need appears", LOCAL_INTEGRATION_BRANCH, "clean_descendant_only_never_dirty_root_main", "runtime remains closed"]),
                    contains_all(brief_text, [CURRENT_BRANCH, "explicit stop", "no further action", "later clean-descendant merge-prep planning only if a new external integration need appears", "dirty-root integration remains out of bounds"]),
                    contains_all(stop_handoff_text, ["explicit stop", "no further action", "later clean-descendant merge-prep planning only if a new external integration need appears", "runtime remains closed", "dirty root main remains quarantine-only", "no new evidence-bearing packet is introduced"]),
                )
            )
            else "blocked",
            "notes": "The live driver and next plan-mode surfaces should freeze explicit-stop handoff facts without reopening scope.",
        },
    ]

    claim_packet = {
        "supports": [
            "P72 normalizes archive-facing, release-facing, and planning-facing surfaces around an explicit stop or no further action recommendation.",
            "P72 preserves P69/P70/P71 as hygiene-only archive/control sidecars rather than evidence-bearing packets.",
            "P72 freezes a stop handoff that keeps later clean-descendant merge-prep planning conditional and non-executing.",
        ],
        "does_not_support": ["runtime reopening", "scope widening", "dirty-root integration", "merge execution"],
        "distilled_result": {
            "active_stage_at_archive_polish_time": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "current_archive_polish_sidecar": "p72_post_p71_archive_polish_and_explicit_stop_handoff",
            "preserved_prior_cleanup_sidecars": ["p69_post_h65_repo_graph_hygiene_inventory", "p70_post_p69_archive_index_and_artifact_policy_sync", "p71_post_p70_clean_descendant_merge_prep_readiness_sync"],
            "current_planning_branch": current_branch_name,
            "published_branch": PUBLISHED_BRANCH,
            "selected_outcome": "archive_polish_surfaces_normalized_and_explicit_stop_handoff_frozen_without_scope_widening",
            "next_required_lane": "explicit_stop_or_no_further_action",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"field": "current_branch", "value": current_branch_name},
            {"field": "preflight_state", "value": preflight_summary["preflight_state"]},
            {"field": "archive_ready_state", "value": p10_summary["packet_state"]},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
