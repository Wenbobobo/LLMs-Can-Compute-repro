"""Export the post-P67 release hygiene/control rebaseline sidecar for P68."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P68_post_p67_release_hygiene_and_control_rebaseline"
P67_SUMMARY_PATH = ROOT / "results" / "P67_post_p66_published_successor_freeze" / "summary.json"
WORKTREE_HYGIENE_SUMMARY_PATH = ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
CURRENT_PUBLISHED_BRANCH = "wip/p66-post-p65-published-successor-freeze"
PRESERVED_PRIOR_PUBLISHED_BRANCH = "wip/p63-post-p62-tight-core-hygiene"
PRESERVED_REVIEW_BRANCH = "wip/p64-post-p63-successor-stack"


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
    p67_summary = read_json(P67_SUMMARY_PATH)["summary"]
    worktree_hygiene_summary = read_json(WORKTREE_HYGIENE_SUMMARY_PATH)["summary"]
    if p67_summary["selected_outcome"] != "published_successor_freeze_locked_after_p66_review":
        raise RuntimeError("P68 expects the landed P67 published successor freeze.")

    current_branch_name = current_branch()
    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)

    checklist_rows = [
        {
            "item_id": "p68_reads_p67",
            "status": "pass",
            "notes": "P68 starts only after the landed P67 freeze wave.",
        },
        {
            "item_id": "p68_current_branch_is_p66",
            "status": "pass" if current_branch_name == CURRENT_PUBLISHED_BRANCH else "blocked",
            "notes": "The rebaseline should run on the live p66 published branch.",
        },
        {
            "item_id": "p68_worktree_hygiene_is_clean_ready",
            "status": "pass"
            if worktree_hygiene_summary["release_commit_state"] == "clean_worktree_ready_if_other_gates_green"
            and worktree_hygiene_summary["branch"] == CURRENT_PUBLISHED_BRANCH
            else "blocked",
            "notes": "The new published successor branch should be clean enough for outward sync if other gates are green.",
        },
        {
            "item_id": "p68_driver_and_registry_expose_rebased_frozen_successor",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P68_post_p67_release_hygiene_and_control_rebaseline",
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
            "P68 reanchors release hygiene and current control on the frozen p66 published branch.",
            "P68 keeps the release-commit classification explicit without implying any dirty-root merge.",
            "P68 preserves p63 and p64 as lineage only while moving live control to p66.",
        ],
        "does_not_support": [
            "dirty-root publication",
            "runtime reopen",
            "merge execution",
        ],
        "distilled_result": {
            "current_release_hygiene_and_control_rebaseline_wave": "p68_post_p67_release_hygiene_and_control_rebaseline",
            "current_published_clean_descendant_branch": CURRENT_PUBLISHED_BRANCH,
            "preserved_prior_published_clean_descendant_branch": PRESERVED_PRIOR_PUBLISHED_BRANCH,
            "preserved_prior_successor_review_branch": PRESERVED_REVIEW_BRANCH,
            "current_execution_branch": current_branch_name,
            "worktree_hygiene_branch": worktree_hygiene_summary["branch"],
            "release_commit_state": worktree_hygiene_summary["release_commit_state"],
            "selected_outcome": "published_frozen_successor_release_hygiene_and_control_rebaselined",
            "next_required_lane": "h65_archive_first_terminal_freeze_packet",
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
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
