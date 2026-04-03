"""Export the post-P72 legacy-worktree shrink inventory and keep-set sync sidecar for P73."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync"
P72_SUMMARY_PATH = ROOT / "results" / "P72_post_p71_archive_polish_and_explicit_stop_handoff" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ROOT_README_PATH = ROOT / "README.md"
STATUS_PATH = ROOT / "STATUS.md"
DOCS_README_PATH = ROOT / "docs" / "README.md"
MILESTONES_README_PATH = ROOT / "docs" / "milestones" / "README.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
KEEP_SET_PATH = ROOT / "docs" / "milestones" / "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync" / "keep_set.md"
SHRINK_RUNBOOK_PATH = ROOT / "docs" / "milestones" / "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync" / "shrink_runbook.md"
POST_P73_HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-02-post-p73-next-planmode-handoff.md"
POST_P73_STARTUP_PATH = ROOT / "docs" / "plans" / "2026-04-02-post-p73-next-planmode-startup-prompt.md"
POST_P73_BRIEF_PATH = ROOT / "docs" / "plans" / "2026-04-02-post-p73-next-planmode-brief-prompt.md"
CURRENT_BRANCH = "wip/p73-post-p72-hygiene-shrink-mergeprep"
CURRENT_BRANCH_PATH = "D:/zWenbo/AI/wt/p73-post-p72-hygiene-shrink-mergeprep"
P72_BRANCH = "wip/p72-post-p71-archive-polish-stop-handoff"
P69_BRANCH = "wip/p69-post-h65-hygiene-only-cleanup"
CURRENT_REVIEW_BRANCH = "wip/p74-post-p73-successor-publication-review"
PUBLISHED_BRANCH = "wip/p75-post-p74-published-successor-freeze"
P56_BRANCH = "wip/p56-main-scratch"
ROOT_MAIN_BRANCH = "wip/root-main-parking-2026-03-24"
LEGACY_PREFIX = "D:/zWenbo/AI/LLMCompute-worktrees/"
PREFERRED_PREFIX = "D:/zWenbo/AI/wt/"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
LEGACY_KEEP_BRANCHES = {"wip/r33-next"}


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


def git_output(args: list[str], *, cwd: Path | str | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd or ROOT),
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


def listed_worktrees() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in git_output(["worktree", "list", "--porcelain"]).splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, value = line.split(" ", 1)
        current[key] = value.strip()
    if current:
        entries.append(current)
    rows: list[dict[str, str]] = []
    for entry in entries:
        path = entry.get("worktree", "").replace("\\", "/")
        branch = entry.get("branch", "").removeprefix("refs/heads/")
        rows.append(
            {
                "worktree": path,
                "branch": branch,
                "upstream": tracked_upstream(branch) if branch else "",
            }
        )
    return rows


def worktree_status(path: str) -> dict[str, object]:
    branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    dirty_lines = [line for line in git_output(["status", "--short", "--untracked-files=all"], cwd=path).splitlines() if line]
    return {"branch": branch, "dirty_count": len(dirty_lines), "clean": len(dirty_lines) == 0}


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def classify_legacy_rows(worktrees: list[dict[str, str]]) -> dict[str, list[dict[str, object]]]:
    buckets: dict[str, list[dict[str, object]]] = {
        "keep_set": [],
        "prune_candidates_with_upstream": [],
        "prune_candidates_without_upstream": [],
        "blocked_dirty": [],
        "misplaced_live_branch": [],
    }
    live_branches = {CURRENT_BRANCH, CURRENT_REVIEW_BRANCH, P72_BRANCH, P69_BRANCH, PUBLISHED_BRANCH, P56_BRANCH, ROOT_MAIN_BRANCH}
    for row in worktrees:
        path = row["worktree"]
        if not path.startswith(LEGACY_PREFIX):
            continue
        status = worktree_status(path)
        enriched = {
            "worktree": path,
            "branch": row["branch"],
            "upstream": row.get("upstream", ""),
            "dirty_count": int(status["dirty_count"]),
            "clean": bool(status["clean"]),
        }
        if row["branch"] in live_branches:
            buckets["misplaced_live_branch"].append(enriched)
        elif row["branch"] in LEGACY_KEEP_BRANCHES:
            buckets["keep_set"].append(enriched)
        elif not bool(status["clean"]):
            buckets["blocked_dirty"].append(enriched)
        elif row.get("upstream"):
            buckets["prune_candidates_with_upstream"].append(enriched)
        else:
            buckets["prune_candidates_without_upstream"].append(enriched)
    return buckets


def sample_rows(rows: list[dict[str, object]], *, limit: int = 5) -> list[dict[str, object]]:
    return rows[:limit]


def main() -> None:
    p72_summary = read_json(P72_SUMMARY_PATH)["summary"]
    if p72_summary["selected_outcome"] != "archive_polish_surfaces_normalized_and_explicit_stop_handoff_frozen_without_scope_widening":
        raise RuntimeError("P73 expects the landed P72 archive-polish and explicit-stop handoff sidecar.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    root_readme_text = read_text(ROOT_README_PATH)
    status_text = read_text(STATUS_PATH)
    docs_readme_text = read_text(DOCS_README_PATH)
    milestones_readme_text = read_text(MILESTONES_README_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    keep_set_text = read_text(KEEP_SET_PATH)
    shrink_runbook_text = read_text(SHRINK_RUNBOOK_PATH)
    handoff_text = read_text(POST_P73_HANDOFF_PATH)
    startup_text = read_text(POST_P73_STARTUP_PATH)
    brief_text = read_text(POST_P73_BRIEF_PATH)

    current_branch_name = current_branch()
    worktrees = listed_worktrees()
    legacy_rows = [row for row in worktrees if row["worktree"].startswith(LEGACY_PREFIX)]
    preferred_rows = [row for row in worktrees if row["worktree"].startswith(PREFERRED_PREFIX)]
    legacy_buckets = classify_legacy_rows(worktrees)

    checklist_rows = [
        {"item_id": "p73_reads_p72", "status": "pass", "notes": "P73 runs only after P72 lands the archive-polish explicit-stop handoff sidecar."},
        {
            "item_id": "p73_runs_on_current_preferred_path_branch",
            "status": "pass" if current_branch_name == CURRENT_BRANCH and str(ROOT).replace("\\", "/") == CURRENT_BRANCH_PATH else "blocked",
            "notes": "P73 should run from the preferred D:/zWenbo/AI/wt path, not from the legacy worktree prefix or dirty root main.",
        },
        {
            "item_id": "p73_live_docs_expose_current_local_shrink_wave",
            "status": "pass"
            if all(
                (
                    contains_all(current_stage_driver_text, ["P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync", CURRENT_BRANCH, P72_BRANCH]),
                    contains_all(root_readme_text, ["P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync", CURRENT_BRANCH, P72_BRANCH]),
                    contains_all(status_text, ["P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync", CURRENT_BRANCH, P72_BRANCH]),
                )
            )
            else "blocked",
            "notes": "README, STATUS, and current stage driver should expose P73 as the current local hygiene/shrink lane above the preserved P72 handoff branch.",
        },
        {
            "item_id": "p73_docs_routers_point_to_inventory_and_runbook",
            "status": "pass"
            if all(
                (
                    contains_all(docs_readme_text, ["H65 + P73 + P74/P75/P76 + P72 + P69/P70/P71", "branch_worktree_registry.md", "plans/README.md"]),
                    contains_all(milestones_readme_text, ["P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync", "P74_post_p73_successor_publication_review", "P75_post_p74_published_successor_freeze", "P76_post_p75_release_hygiene_and_control_rebaseline", "P72_post_p71_archive_polish_and_explicit_stop_handoff"]),
                    contains_all(plans_readme_text, ["2026-04-02-post-p72-hygiene-shrink-mergeprep-design.md", "2026-04-02-post-p73-next-planmode-handoff.md", "2026-04-02-post-p73-next-planmode-startup-prompt.md", "2026-04-02-post-p73-next-planmode-brief-prompt.md"]),
                    contains_all(publication_readme_text, ["P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync", "current local hygiene and shrink wave"]),
                )
            )
            else "blocked",
            "notes": "The docs routers should expose the current shrink wave, design doc, and milestone entrypoints.",
        },
        {
            "item_id": "p73_branch_registry_rebases_live_path_policy",
            "status": "pass"
            if contains_all(
                branch_registry_text,
                [
                    CURRENT_BRANCH,
                    CURRENT_BRANCH_PATH,
                    CURRENT_REVIEW_BRANCH,
                    P72_BRANCH,
                    "D:/zWenbo/AI/wt/",
                    "D:/zWenbo/AI/LLMCompute-worktrees/",
                    "wip/r33-next",
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "The branch/worktree registry should make the preferred path explicit and restrict the legacy prefix to preserved history or shrink candidates.",
        },
        {
            "item_id": "p73_keep_set_and_runbook_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(keep_set_text, [CURRENT_BRANCH, CURRENT_REVIEW_BRANCH, P72_BRANCH, P69_BRANCH, PUBLISHED_BRANCH, P56_BRANCH, ROOT_MAIN_BRANCH, "wip/r33-next", "D:/zWenbo/AI/wt/"]),
                    contains_all(shrink_runbook_text, [LEGACY_PREFIX, "git worktree remove", "never touch", ROOT_MAIN_WORKTREE, "do not remove dirty worktrees", "branch refs remain preserved"]),
                )
            )
            else "blocked",
            "notes": "The keep-set and shrink runbook should make the safety boundary explicit before any local removal step.",
        },
        {
            "item_id": "p73_post_p73_handoff_prompts_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(handoff_text, [CURRENT_BRANCH, P72_BRANCH, P69_BRANCH, P56_BRANCH, "legacy local worktree footprint has already been shrunk", "remaining legacy-path worktrees", "wip/h27-promotion", "wip/r33-next", "clean_descendant_only_never_dirty_root_main"]),
                    contains_all(startup_text, [CURRENT_BRANCH, P72_BRANCH, P69_BRANCH, P56_BRANCH, "legacy-path worktree count: `2`", "wip/h27-promotion", "wip/r33-next", "Runtime remains closed"]),
                    contains_all(brief_text, [CURRENT_BRANCH, "legacy-path worktree count: `2`", "wip/h27-promotion", "wip/r33-next", "dirty-root integration remains out of bounds"]),
                )
            )
            else "blocked",
            "notes": "The next plan-mode handoff surfaces should reflect the post-shrink state rather than the earlier pre-shrink P72 state.",
        },
        {
            "item_id": "p73_legacy_inventory_classifies_every_legacy_worktree",
            "status": "pass"
            if (
                len(legacy_rows)
                == len(legacy_buckets["keep_set"])
                + len(legacy_buckets["prune_candidates_with_upstream"])
                + len(legacy_buckets["prune_candidates_without_upstream"])
                + len(legacy_buckets["blocked_dirty"])
                + len(legacy_buckets["misplaced_live_branch"])
            )
            else "blocked",
            "notes": "Every legacy-path worktree should land in exactly one current category.",
        },
        {
            "item_id": "p73_no_live_keep_branch_remains_misplaced_under_legacy_prefix",
            "status": "pass" if not legacy_buckets["misplaced_live_branch"] else "blocked",
            "notes": "The current live keep-set should not accidentally remain under the legacy worktree prefix.",
        },
    ]

    claim_packet = {
        "supports": [
            "P73 inventories the legacy local worktree footprint and classifies shrink candidates without touching dirty root main.",
            "P73 re-anchors live path policy on D:/zWenbo/AI/wt while preserving only narrow historical exceptions under the legacy prefix.",
            "P73 prepares later safe local shrink and merge-prep dossier work without reopening runtime or widening the evidence boundary.",
        ],
        "does_not_support": ["dirty-root integration", "runtime reopening", "same-lane executor-value reopening", "merge execution"],
        "distilled_result": {
            "active_stage_at_inventory_time": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "current_local_hygiene_wave": "p73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
            "preserved_archive_handoff_wave": "p72_post_p71_archive_polish_and_explicit_stop_handoff",
            "current_planning_branch": current_branch_name,
            "total_worktree_count": len(worktrees),
            "preferred_path_worktree_count": len(preferred_rows),
            "legacy_path_worktree_count": len(legacy_rows),
            "legacy_keep_count": len(legacy_buckets["keep_set"]),
            "legacy_prune_with_upstream_count": len(legacy_buckets["prune_candidates_with_upstream"]),
            "legacy_prune_without_upstream_count": len(legacy_buckets["prune_candidates_without_upstream"]),
            "legacy_blocked_dirty_count": len(legacy_buckets["blocked_dirty"]),
            "legacy_misplaced_live_count": len(legacy_buckets["misplaced_live_branch"]),
            "selected_outcome": "legacy_worktree_inventory_and_keep_set_sync_completed_for_safe_local_shrink",
            "next_required_lane": "safe_local_legacy_shrink_or_nonexecuting_merge_prep_dossier",
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
            {"field": "preferred_prefix", "value": PREFERRED_PREFIX},
            {"field": "legacy_prefix", "value": LEGACY_PREFIX},
            {"field": "legacy_keep_examples", "value": sample_rows(legacy_buckets["keep_set"])},
            {"field": "legacy_prune_with_upstream_examples", "value": sample_rows(legacy_buckets["prune_candidates_with_upstream"])},
            {"field": "legacy_prune_without_upstream_examples", "value": sample_rows(legacy_buckets["prune_candidates_without_upstream"])},
            {"field": "legacy_blocked_dirty_examples", "value": sample_rows(legacy_buckets["blocked_dirty"])},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
