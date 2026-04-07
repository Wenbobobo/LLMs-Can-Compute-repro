"""Export the post-P76 keep-set and provenance normalization sidecar for P77."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P77_post_p76_keep_set_and_provenance_normalization"
P76_SUMMARY_PATH = ROOT / "results" / "P76_post_p75_release_hygiene_and_control_rebaseline" / "summary.json"
ROOT_README_PATH = ROOT / "README.md"
STATUS_PATH = ROOT / "STATUS.md"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
CURRENT_BRANCH = "wip/p75-post-p74-published-successor-freeze"
CURRENT_REVIEW_BRANCH = "wip/p74-post-p73-successor-publication-review"
CURRENT_LOCAL_HYGIENE_BRANCH = "wip/p73-post-p72-hygiene-shrink-mergeprep"
CURRENT_HANDOFF_BRANCH = "wip/p72-post-p71-archive-polish-stop-handoff"
CURRENT_HYGIENE_BRANCH = "wip/p69-post-h65-hygiene-only-cleanup"
LOCAL_INTEGRATION_BRANCH = "wip/p56-main-scratch"
PRESERVED_PRIOR_PUBLISHED_BRANCH = "wip/p66-post-p65-published-successor-freeze"
PRESERVED_DEEPER_REVIEW_BRANCH = "wip/p64-post-p63-successor-stack"
QUARANTINE_BRANCH = "wip/root-main-parking-2026-03-24"
TRACKED_KEEP_BRANCHES = [
    CURRENT_BRANCH,
    CURRENT_REVIEW_BRANCH,
    CURRENT_LOCAL_HYGIENE_BRANCH,
    CURRENT_HANDOFF_BRANCH,
    CURRENT_HYGIENE_BRANCH,
    LOCAL_INTEGRATION_BRANCH,
]


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
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def tracked_upstream(branch: str) -> str:
    return git_output(["for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch}"])


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p76_summary = read_json(P76_SUMMARY_PATH)["summary"]
    if p76_summary["selected_outcome"] != "published_successor_release_hygiene_and_control_rebaselined_after_p75":
        raise RuntimeError("P77 expects the landed P76 release hygiene and control rebaseline sidecar.")

    root_readme_text = read_text(ROOT_README_PATH)
    status_text = read_text(STATUS_PATH)
    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    current_branch_name = current_branch()
    upstreams = {branch: tracked_upstream(branch) for branch in TRACKED_KEEP_BRANCHES}

    checklist_rows = [
        {"item_id": "p77_reads_p76", "status": "pass", "notes": "P77 starts only after the landed P76 sidecar."},
        {
            "item_id": "p77_runs_on_current_p75_branch",
            "status": "pass" if current_branch_name == CURRENT_BRANCH else "blocked",
            "notes": "The keep-set normalization sidecar should run on the live p75 branch.",
        },
        {
            "item_id": "p77_top_level_surfaces_expose_convergence_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        root_readme_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P77_post_p76_keep_set_and_provenance_normalization",
                            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
                            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
                            "P80_post_p79_next_planmode_handoff_sync",
                            CURRENT_BRANCH,
                        ],
                    ),
                    contains_all(
                        status_text,
                        [
                            "P77_post_p76_keep_set_and_provenance_normalization",
                            "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
                            "P79_post_p78_archive_claim_boundary_and_reopen_screen",
                            "P80_post_p79_next_planmode_handoff_sync",
                            CURRENT_LOCAL_HYGIENE_BRANCH,
                            CURRENT_REVIEW_BRANCH,
                            CURRENT_BRANCH,
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "README and STATUS should expose the convergence sidecar stack on top of the p75 route.",
        },
        {
            "item_id": "p77_driver_roles_are_normalized",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "P77_post_p76_keep_set_and_provenance_normalization",
                    "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync",
                    "P79_post_p78_archive_claim_boundary_and_reopen_screen",
                    "P80_post_p79_next_planmode_handoff_sync",
                    CURRENT_REVIEW_BRANCH,
                    PRESERVED_DEEPER_REVIEW_BRANCH,
                    CURRENT_BRANCH,
                    CURRENT_LOCAL_HYGIENE_BRANCH,
                    CURRENT_HANDOFF_BRANCH,
                    CURRENT_HYGIENE_BRANCH,
                    LOCAL_INTEGRATION_BRANCH,
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "Current-stage driver should keep p74 as current review and p64 as preserved deeper review lineage.",
        },
        {
            "item_id": "p77_branch_registry_keeps_balanced_active_set",
            "status": "pass"
            if contains_all(
                branch_registry_text,
                [
                    CURRENT_BRANCH,
                    CURRENT_REVIEW_BRANCH,
                    CURRENT_LOCAL_HYGIENE_BRANCH,
                    CURRENT_HANDOFF_BRANCH,
                    CURRENT_HYGIENE_BRANCH,
                    LOCAL_INTEGRATION_BRANCH,
                    PRESERVED_PRIOR_PUBLISHED_BRANCH,
                    PRESERVED_DEEPER_REVIEW_BRANCH,
                    QUARANTINE_BRANCH,
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "The registry should expose the balanced active keep set and preserved lineage explicitly.",
        },
        {
            "item_id": "p77_keep_branches_have_remote_provenance",
            "status": "pass"
            if all(
                (
                    upstreams[CURRENT_BRANCH] == "origin/wip/p75-post-p74-published-successor-freeze",
                    upstreams[CURRENT_REVIEW_BRANCH] == "origin/wip/p74-post-p73-successor-publication-review",
                    upstreams[CURRENT_LOCAL_HYGIENE_BRANCH] == "origin/wip/p73-post-p72-hygiene-shrink-mergeprep",
                    upstreams[CURRENT_HANDOFF_BRANCH] == "origin/wip/p72-post-p71-archive-polish-stop-handoff",
                    upstreams[CURRENT_HYGIENE_BRANCH] == "origin/wip/p69-post-h65-hygiene-only-cleanup",
                    upstreams[LOCAL_INTEGRATION_BRANCH] == "origin/main",
                )
            )
            else "blocked",
            "notes": "The active keep branches should now have explicit upstream provenance before any convergence work.",
        },
        {
            "item_id": "p77_plans_router_points_to_new_convergence_entrypoints",
            "status": "pass"
            if contains_all(
                plans_readme_text,
                [
                    "2026-04-05-post-p76-hygiene-first-convergence-design.md",
                    "2026-04-05-post-p80-next-planmode-handoff.md",
                    "2026-04-05-post-p80-next-planmode-startup-prompt.md",
                    "2026-04-05-post-p80-next-planmode-brief-prompt.md",
                ],
            )
            else "blocked",
            "notes": "Plans router should expose the new convergence design and post-P80 handoff prompts.",
        },
    ]
    claim_packet = {
        "supports": [
            "P77 normalizes the active keep set around p75, p74, p73, p72, p69, and p56.",
            "P77 publishes remote provenance for p73 and p74 before further local convergence.",
            "P77 corrects control-surface role labeling without reopening runtime or dirty-root integration.",
        ],
        "does_not_support": ["runtime reopen", "dirty-root integration", "same-lane executor-value reopen"],
        "distilled_result": {
            "current_keep_set_normalization_wave": "p77_post_p76_keep_set_and_provenance_normalization",
            "current_published_branch": CURRENT_BRANCH,
            "current_review_branch": CURRENT_REVIEW_BRANCH,
            "current_local_hygiene_branch": CURRENT_LOCAL_HYGIENE_BRANCH,
            "current_handoff_branch": CURRENT_HANDOFF_BRANCH,
            "current_hygiene_branch": CURRENT_HYGIENE_BRANCH,
            "local_integration_branch": LOCAL_INTEGRATION_BRANCH,
            "tracked_keep_branch_count": len(TRACKED_KEEP_BRANCHES),
            "selected_outcome": "keep_set_and_provenance_normalized_after_p76",
            "next_required_lane": "p78_balanced_worktree_convergence_with_quarantines_preserved",
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
            {"field": "tracked_keep_branches", "value": upstreams},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
