"""Export the post-P75 release hygiene/control rebaseline sidecar for P76."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P76_post_p75_release_hygiene_and_control_rebaseline"
P75_SUMMARY_PATH = ROOT / "results" / "P75_post_p74_published_successor_freeze" / "summary.json"
WORKTREE_HYGIENE_SUMMARY_PATH = ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
CURRENT_PUBLISHED_BRANCH = "wip/p75-post-p74-published-successor-freeze"
PRESERVED_PRIOR_PUBLISHED_BRANCH = "wip/p66-post-p65-published-successor-freeze"
PRESERVED_REVIEW_BRANCH = "wip/p74-post-p73-successor-publication-review"
CURRENT_LOCAL_HYGIENE_BRANCH = "wip/p73-post-p72-hygiene-shrink-mergeprep"


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


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p75_summary = read_json(P75_SUMMARY_PATH)["summary"]
    worktree_hygiene_summary = read_json(WORKTREE_HYGIENE_SUMMARY_PATH)["summary"]
    if p75_summary["selected_outcome"] != "published_successor_freeze_locked_after_p74_review":
        raise RuntimeError("P76 expects the landed P75 published successor freeze.")

    current_branch_name = current_branch()
    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)

    checklist_rows = [
        {
            "item_id": "p76_reads_p75",
            "status": "pass",
            "notes": "P76 starts only after the landed P75 freeze wave.",
        },
        {
            "item_id": "p76_current_branch_is_p75",
            "status": "pass" if current_branch_name == CURRENT_PUBLISHED_BRANCH else "blocked",
            "notes": "The rebaseline should run on the live p75 published branch.",
        },
        {
            "item_id": "p76_worktree_hygiene_is_clean_ready",
            "status": "pass"
            if worktree_hygiene_summary["release_commit_state"] == "clean_worktree_ready_if_other_gates_green"
            and worktree_hygiene_summary["branch"] == CURRENT_PUBLISHED_BRANCH
            else "blocked",
            "notes": "The new published successor branch should be clean enough for outward sync if other gates are green.",
        },
        {
            "item_id": "p76_driver_and_registry_expose_rebased_p75_successor",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync",
                            "P74_post_p73_successor_publication_review",
                            "P75_post_p74_published_successor_freeze",
                            "P76_post_p75_release_hygiene_and_control_rebaseline",
                            CURRENT_PUBLISHED_BRANCH,
                            "`explicit_archive_stop_or_hygiene_only`",
                        ],
                    ),
                    contains_all(
                        branch_registry_text,
                        [
                            CURRENT_PUBLISHED_BRANCH,
                            PRESERVED_PRIOR_PUBLISHED_BRANCH,
                            PRESERVED_REVIEW_BRANCH,
                            CURRENT_LOCAL_HYGIENE_BRANCH,
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The rebaseline should expose the new published branch while preserving the prior lineages explicitly.",
        },
    ]
    claim_packet = {
        "supports": [
            "P76 reanchors release hygiene and current control on the p75 published branch.",
            "P76 keeps the release-commit classification explicit without implying any dirty-root merge.",
            "P76 preserves p66 as prior published lineage while keeping p73 and p74 explicit.",
        ],
        "does_not_support": [
            "dirty-root publication",
            "runtime reopen",
            "merge execution",
        ],
        "distilled_result": {
            "current_release_hygiene_and_control_rebaseline_wave": "p76_post_p75_release_hygiene_and_control_rebaseline",
            "current_published_clean_descendant_branch": CURRENT_PUBLISHED_BRANCH,
            "preserved_prior_published_clean_descendant_branch": PRESERVED_PRIOR_PUBLISHED_BRANCH,
            "preserved_prior_successor_review_branch": PRESERVED_REVIEW_BRANCH,
            "current_local_hygiene_branch": CURRENT_LOCAL_HYGIENE_BRANCH,
            "current_execution_branch": current_branch_name,
            "worktree_hygiene_branch": worktree_hygiene_summary["branch"],
            "release_commit_state": worktree_hygiene_summary["release_commit_state"],
            "selected_outcome": "published_successor_release_hygiene_and_control_rebaselined_after_p75",
            "next_required_lane": "standing_release_audit_refresh_on_p75",
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
            {"field": "current_published_clean_descendant_branch", "value": CURRENT_PUBLISHED_BRANCH},
            {"field": "release_commit_state", "value": worktree_hygiene_summary["release_commit_state"]},
            {"field": "worktree_hygiene_branch", "value": worktree_hygiene_summary["branch"]},
            {"field": "current_local_hygiene_branch", "value": CURRENT_LOCAL_HYGIENE_BRANCH},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
