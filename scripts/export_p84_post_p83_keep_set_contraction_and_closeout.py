"""Export the post-P83 keep-set contraction and closeout packet for P84."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P84_post_p83_keep_set_contraction_and_closeout"
P83_SUMMARY_PATH = ROOT / "results" / "P83_post_p82_promotion_branch_and_pr_handoff" / "summary.json"
PROMOTION_BRANCH = "wip/p83-post-p82-promotion-branch-and-pr-handoff"
PUBLISHED_BRANCH = "wip/p75-post-p74-published-successor-freeze"
REQUIRED_WORKTREE_PATHS = [
    "D:/zWenbo/AI/LLMCompute",
    "D:/zWenbo/AI/LLMCompute-worktrees/h27-promotion",
    "D:/zWenbo/AI/wt/p56-main-scratch",
    "D:/zWenbo/AI/wt/p69-post-h65-hygiene-only-cleanup",
    "D:/zWenbo/AI/wt/p72-post-p71-archive-polish-stop-handoff",
    "D:/zWenbo/AI/wt/p73-post-p72-hygiene-shrink-mergeprep",
    "D:/zWenbo/AI/wt/p74-post-p73-successor-publication-review",
    "D:/zWenbo/AI/wt/p75-post-p74-published-successor-freeze",
    "D:/zWenbo/AI/wt/p83-post-p82-promotion-branch-and-pr-handoff",
]
REMOVED_WORKTREE_PATHS = [
    "D:/zWenbo/AI/wt/p81-post-p80-clean-descendant-promotion-prep",
    "D:/zWenbo/AI/wt/p82-post-p81-clean-main-promotion-probe",
]
DOC_REQUIREMENTS = {
    "README.md": [
        "P84_post_p83_keep_set_contraction_and_closeout",
        "P83_post_p82_promotion_branch_and_pr_handoff",
        PROMOTION_BRANCH,
        PUBLISHED_BRANCH,
    ],
    "STATUS.md": [
        "P84_post_p83_keep_set_contraction_and_closeout",
        "P83_post_p82_promotion_branch_and_pr_handoff",
        "p83",
        "p81",
        "p82",
    ],
    "docs/README.md": [
        "H65 + P84 + P83",
        "branch_worktree_registry.md",
        "plans/README.md",
        "milestones/README.md",
    ],
    "docs/branch_worktree_registry.md": [
        PROMOTION_BRANCH,
        "wip/p81-post-p80-clean-descendant-promotion-prep",
        "wip/p82-post-p81-clean-main-promotion-probe",
        "P84",
        "P83",
    ],
    "docs/plans/README.md": [
        "2026-04-07-post-p84-next-planmode-handoff.md",
        "2026-04-07-post-p84-next-planmode-startup-prompt.md",
        "2026-04-07-post-p84-next-planmode-brief-prompt.md",
        "P84",
        "P83",
        PROMOTION_BRANCH,
    ],
    "docs/milestones/README.md": [
        "P84_post_p83_keep_set_contraction_and_closeout",
        "P83_post_p82_promotion_branch_and_pr_handoff",
        "P81_post_p80_locked_fact_rebaseline_and_route_sync",
        "P82_post_p81_clean_main_promotion_probe",
    ],
    "docs/publication_record/README.md": [
        "2026-04-07-post-p84-next-planmode-handoff.md",
        "P84_post_p83_keep_set_contraction_and_closeout",
        "P83_post_p82_promotion_branch_and_pr_handoff",
    ],
    "docs/publication_record/current_stage_driver.md": [
        "P84_post_p83_keep_set_contraction_and_closeout",
        "P83_post_p82_promotion_branch_and_pr_handoff",
        PROMOTION_BRANCH,
        PUBLISHED_BRANCH,
    ],
    "docs/plans/2026-04-07-post-p84-next-planmode-handoff.md": [
        PROMOTION_BRANCH,
        "promotion/PR finalization",
        "no further action",
        "runtime remains closed",
    ],
    "docs/plans/2026-04-07-post-p84-next-planmode-startup-prompt.md": [
        "promotion/PR finalization",
        "no further action",
        "runtime",
        "dirty-root integration",
    ],
    "docs/plans/2026-04-07-post-p84-next-planmode-brief-prompt.md": [
        "promotion/PR finalization",
        "no further action",
        "runtime closed",
    ],
}


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


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def parse_worktree_rows(raw: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            if current:
                rows.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value.strip()
    if current:
        rows.append(current)
    return rows


def doc_sync_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative_path, needles in DOC_REQUIREMENTS.items():
        path = ROOT / relative_path
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "path": relative_path,
                "exists": exists,
                "needle_count": len(needles),
                "ok": exists and contains_all(text, needles),
            }
        )
    return rows


def main() -> None:
    p83_summary = read_json(P83_SUMMARY_PATH)["summary"]
    if p83_summary["selected_outcome"] != "promotion_branch_materialized_and_pr_handoff_prepared_after_p82":
        raise RuntimeError("P84 expects the landed P83 promotion-branch handoff.")
    if p83_summary["blocked_count"] != 0:
        raise RuntimeError("P84 expects a green P83 summary before closeout.")

    current_branch_name = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    closeout_head = git_output(["rev-parse", "--short", "HEAD"])
    published_head = git_output(["rev-parse", "--short", PUBLISHED_BRANCH])
    worktree_rows = parse_worktree_rows(git_output(["worktree", "list", "--porcelain"]))
    mounted_paths = [row["worktree"] for row in worktree_rows]
    doc_rows = doc_sync_rows()

    checklist_rows = [
        {
            "item_id": "p84_reads_green_p83_summary",
            "status": "pass",
            "notes": "P84 starts only after the landed green P83 promotion handoff.",
        },
        {
            "item_id": "p84_runs_on_p83_promotion_branch",
            "status": "pass" if current_branch_name == PROMOTION_BRANCH else "blocked",
            "notes": "The keep-set closeout should be authored from the clean p83 promotion-ready branch.",
        },
        {
            "item_id": "p84_contracts_to_required_keep_set",
            "status": "pass" if all(path in mounted_paths for path in REQUIRED_WORKTREE_PATHS) else "blocked",
            "notes": "Only the required mounted keep set plus quarantined dirty survivors should remain mounted.",
        },
        {
            "item_id": "p84_removes_temporary_p81_p82_worktrees",
            "status": "pass" if all(path not in mounted_paths for path in REMOVED_WORKTREE_PATHS) else "blocked",
            "notes": "The temporary p81 and p82 worktrees should be removed while preserving branch lineage.",
        },
        {
            "item_id": "p84_router_docs_and_handoffs_are_synced",
            "status": "pass" if all(bool(row["ok"]) for row in doc_rows) else "blocked",
            "notes": "README/router/registry/handoff docs should all point at the P84/P83 closeout state.",
        },
    ]

    claim_packet = {
        "supports": [
            "P84 contracts the active mounted keep set to the promotion-ready p83 branch plus the preserved operational branches p75, p74, p73, p72, p69, and p56.",
            "P84 preserves p81 and p82 as unmounted immediate promotion-prep lineage rather than live execution mounts.",
            "P84 leaves promotion/PR finalization from p83 or no further action as the only remaining clean-descendant routes.",
        ],
        "does_not_support": [
            "dirty-root integration",
            "runtime reopen",
            "same-lane executor-value reopen",
            "broad Wasm or arbitrary C scope expansion",
        ],
        "distilled_result": {
            "current_closeout_wave": "p84_post_p83_keep_set_contraction_and_closeout",
            "promotion_branch": PROMOTION_BRANCH,
            "promotion_branch_head": closeout_head,
            "published_branch": PUBLISHED_BRANCH,
            "published_branch_head": published_head,
            "mounted_keep_paths": REQUIRED_WORKTREE_PATHS,
            "removed_temporary_paths": REMOVED_WORKTREE_PATHS,
            "selected_outcome": "keep_set_contracted_and_closeout_synced_after_p83",
            "next_recommended_route": "promotion_pr_finalization_or_no_further_action",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "mounted_worktree_count": len(mounted_paths),
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"field": "current_branch", "value": current_branch_name},
            {"field": "mounted_paths", "value": mounted_paths},
            {"field": "worktree_rows", "value": worktree_rows},
            {"field": "doc_sync_rows", "value": doc_rows},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
