"""Export the post-P63 release hygiene rebaseline sidecar for P64."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P64_post_p63_release_hygiene_rebaseline"
P63_SUMMARY_PATH = ROOT / "results" / "P63_post_p62_published_successor_promotion_prep" / "summary.json"
WORKTREE_HYGIENE_SUMMARY_PATH = ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
PREFLIGHT_SUMMARY_PATH = ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
P10_SUMMARY_PATH = ROOT / "results" / "P10_submission_archive_ready" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
CURRENT_PUBLISHED_BRANCH = "wip/p63-post-p62-tight-core-hygiene"
CURRENT_RELEASE_WAVE = "p64_post_p63_release_hygiene_rebaseline"
PRESERVED_PRIOR_BRANCH = "wip/p60-post-p59-published-clean-descendant-prep"


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
    p63_summary = read_json(P63_SUMMARY_PATH)["summary"]
    worktree_hygiene_summary = read_json(WORKTREE_HYGIENE_SUMMARY_PATH)["summary"]
    preflight_summary = read_json(PREFLIGHT_SUMMARY_PATH)["summary"]
    p10_summary = read_json(P10_SUMMARY_PATH)["summary"]
    if p63_summary["selected_outcome"] != "published_successor_promotion_prep_locked_after_p62":
        raise RuntimeError("P64 expects the landed P63 successor promotion-prep wave.")

    current_branch_name = current_branch()
    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    current_branch_registered = current_branch_name == CURRENT_PUBLISHED_BRANCH or contains_all(
        branch_registry_text,
        [CURRENT_PUBLISHED_BRANCH, current_branch_name, "successor"],
    )

    checklist_rows = [
        {
            "item_id": "p64_reads_p63",
            "status": "pass",
            "notes": "P64 starts only after P63 lands.",
        },
        {
            "item_id": "p64_current_branch_matches_rebased_successor_hygiene_branch",
            "status": "pass"
            if current_branch_registered and worktree_hygiene_summary["branch"] == CURRENT_PUBLISHED_BRANCH
            else "blocked",
            "notes": "The hygiene snapshot should classify the published successor branch while execution may occur on a registered successor lane.",
        },
        {
            "item_id": "p64_worktree_hygiene_is_clean_ready",
            "status": "pass"
            if worktree_hygiene_summary["release_commit_state"] == "clean_worktree_ready_if_other_gates_green"
            else "blocked",
            "notes": "The current published successor branch should be clean enough for outward sync if other gates are green.",
        },
        {
            "item_id": "p64_preflight_and_archive_ready_are_green",
            "status": "pass"
            if preflight_summary["preflight_state"] == "docs_and_audits_green"
            and p10_summary["packet_state"] == "archive_ready"
            else "blocked",
            "notes": "Rebaselined successor hygiene expects green release-preflight and archive-ready summaries on the same branch family.",
        },
        {
            "item_id": "p64_current_stage_driver_mentions_successor_release_hygiene_rebaseline",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "P64_post_p63_release_hygiene_rebaseline",
                    CURRENT_PUBLISHED_BRANCH,
                    "clean_worktree_ready_if_other_gates_green",
                ],
            )
            else "blocked",
            "notes": "The current stage driver should expose P64 and the rebaselined clean successor posture.",
        },
    ]
    claim_packet = {
        "supports": [
            "P64 reanchors stateful release hygiene on the current published successor branch.",
            "P64 keeps the clean release-commit classification explicit without implying a main merge.",
            "P64 ties release hygiene, preflight, and archive-ready status to the same published successor branch.",
        ],
        "does_not_support": [
            "merge execution",
            "dirty-root integration",
            "runtime reopen",
        ],
        "distilled_result": {
            "current_release_hygiene_rebaseline_wave": CURRENT_RELEASE_WAVE,
            "current_published_clean_descendant_branch": CURRENT_PUBLISHED_BRANCH,
            "preserved_prior_published_clean_descendant_branch": PRESERVED_PRIOR_BRANCH,
            "current_execution_branch": current_branch_name,
            "worktree_hygiene_branch": worktree_hygiene_summary["branch"],
            "release_commit_state": worktree_hygiene_summary["release_commit_state"],
            "preflight_state": preflight_summary["preflight_state"],
            "archive_ready_state": p10_summary["packet_state"],
            "selected_outcome": "published_successor_release_hygiene_rebaselined",
            "next_required_lane": "p65_merge_prep_control_sync",
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
            {"field": "preserved_prior_published_clean_descendant_branch", "value": PRESERVED_PRIOR_BRANCH},
            {"field": "worktree_hygiene_branch", "value": worktree_hygiene_summary["branch"]},
            {"field": "release_commit_state", "value": worktree_hygiene_summary["release_commit_state"]},
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
