"""Export the post-P82 promotion-branch and PR-handoff packet for P83."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P83_post_p82_promotion_branch_and_pr_handoff"
P82_SUMMARY_PATH = ROOT / "results" / "P82_post_p81_clean_main_promotion_probe" / "summary.json"
HANDOFF_PATH = ROOT / "docs" / "milestones" / "P83_post_p82_promotion_branch_and_pr_handoff" / "pr_handoff.md"
PROMOTION_BRANCH = "wip/p83-post-p82-promotion-branch-and-pr-handoff"
SOURCE_BRANCH = "wip/p81-post-p80-clean-descendant-promotion-prep"
BASE_REF = "origin/main"


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


def git_output(args: list[str], *, cwd: str | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd or str(ROOT),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def worktree_clean() -> bool:
    return not bool(git_output(["status", "--short", "--untracked-files=all"]))


def ahead_behind(left: str, right: str) -> dict[str, int]:
    left_only, right_only = git_output(["rev-list", "--left-right", "--count", f"{left}...{right}"]).split()
    return {"left_only": int(left_only), "right_only": int(right_only)}


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p82_summary = read_json(P82_SUMMARY_PATH)["summary"]
    if p82_summary["selected_outcome"] != "clean_main_probe_confirms_fast_forward_promotion_path_after_p81":
        raise RuntimeError("P83 expects the landed P82 clean-main promotion probe.")

    handoff_text = read_text(HANDOFF_PATH)
    current_branch_name = current_branch()
    promotion_head = git_output(["rev-parse", "--short", "HEAD"])
    source_head = git_output(["rev-parse", "--short", SOURCE_BRANCH])
    base_divergence = ahead_behind(BASE_REF, "HEAD")
    source_divergence = ahead_behind("HEAD", SOURCE_BRANCH)

    checklist_rows = [
        {"item_id": "p83_reads_p82", "status": "pass", "notes": "P83 starts only after the landed P82 clean-main probe."},
        {
            "item_id": "p83_runs_on_clean_promotion_branch",
            "status": "pass" if current_branch_name == PROMOTION_BRANCH else "blocked",
            "notes": "The promotion handoff should be prepared on the dedicated p83 branch; final cleanliness is verified after commit.",
        },
        {
            "item_id": "p83_promotion_branch_matches_source_head",
            "status": "pass" if promotion_head == source_head and source_divergence["left_only"] == 0 and source_divergence["right_only"] == 0 else "blocked",
            "notes": "The promotion branch should fast-forward to the exact current source head.",
        },
        {
            "item_id": "p83_promotion_branch_remains_ahead_only_from_origin_main",
            "status": "pass" if base_divergence["left_only"] == 0 and base_divergence["right_only"] > 0 else "blocked",
            "notes": "The promotion branch should remain ahead-only relative to origin/main.",
        },
        {
            "item_id": "p83_handoff_doc_is_pr_ready",
            "status": "pass"
            if contains_all(
                handoff_text,
                [
                    PROMOTION_BRANCH,
                    SOURCE_BRANCH,
                    BASE_REF,
                    promotion_head,
                    "uv run pytest",
                    "no dirty-root integration",
                    "runtime remains closed",
                ],
            )
            else "blocked",
            "notes": "The handoff doc should contain the branch names, head, verification command, and guardrails.",
        },
    ]

    claim_packet = {
        "supports": [
            "P83 materializes a clean promotion branch from the P82 probe without touching dirty root main.",
            "P83 keeps the promotion branch exactly aligned with the current P81 source head.",
            "P83 leaves PR opening optional while making the branch and handoff package ready.",
        ],
        "does_not_support": ["dirty-root integration", "runtime reopen", "direct root-main merge"],
        "distilled_result": {
            "current_promotion_wave": "p83_post_p82_promotion_branch_and_pr_handoff",
            "promotion_branch": PROMOTION_BRANCH,
            "promotion_head": promotion_head,
            "source_branch": SOURCE_BRANCH,
            "source_head": source_head,
            "origin_main_to_promotion_left_right": f"{base_divergence['left_only']}/{base_divergence['right_only']}",
            "promotion_to_source_left_right": f"{source_divergence['left_only']}/{source_divergence['right_only']}",
            "selected_outcome": "promotion_branch_materialized_and_pr_handoff_prepared_after_p82",
            "next_required_lane": "p84_keep_set_contraction_and_closeout",
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
            {"field": "base_divergence", "value": base_divergence},
            {"field": "source_divergence", "value": source_divergence},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
