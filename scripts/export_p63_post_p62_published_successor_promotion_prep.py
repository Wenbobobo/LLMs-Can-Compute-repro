"""Export the post-P62 published successor promotion-prep sidecar for P63."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P63_post_p62_published_successor_promotion_prep"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P62_SUMMARY_PATH = ROOT / "results" / "P62_post_p61_merge_prep_control_sync" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ACTIVE_WAVE_PLAN_PATH = ROOT / "tmp" / "active_wave_plan.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
EXPECTED_BRANCH = "wip/p63-post-p62-tight-core-hygiene"
PRESERVED_PRIOR_BRANCH = "wip/p60-post-p59-published-clean-descendant-prep"
SCRATCH_BRANCH = "wip/p56-main-scratch"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"


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


def branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def parse_worktree_list(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in text.splitlines():
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
    return [
        {
            "worktree": entry.get("worktree", "").replace("\\", "/"),
            "branch": entry.get("branch", "").removeprefix("refs/heads/"),
        }
        for entry in entries
    ]


def main() -> None:
    h64_summary = read_json(H64_SUMMARY_PATH)["summary"]
    p62_summary = read_json(P62_SUMMARY_PATH)["summary"]
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P63 expects the landed H64 freeze packet.")
    if p62_summary["selected_outcome"] != "published_clean_descendant_merge_prep_control_synced_to_h64_stack":
        raise RuntimeError("P63 expects the landed P62 preserved-prior control-sync wave.")

    current_branch_name = current_branch()
    current_upstream = tracked_upstream(current_branch_name)
    published_upstream = tracked_upstream(EXPECTED_BRANCH) if branch_exists(EXPECTED_BRANCH) else ""
    preserved_prior_upstream = tracked_upstream(PRESERVED_PRIOR_BRANCH) if branch_exists(PRESERVED_PRIOR_BRANCH) else ""
    worktrees = parse_worktree_list(git_output(["worktree", "list", "--porcelain"]))
    root_main_entry = next((row for row in worktrees if row["worktree"] == ROOT_MAIN_WORKTREE), None)
    root_main_branch = root_main_entry["branch"] if root_main_entry else ""
    root_main_quarantined = root_main_branch.startswith(ROOT_MAIN_BRANCH_PREFIX)

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    active_wave_text = read_text(ACTIVE_WAVE_PLAN_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    current_branch_registered = current_branch_name == EXPECTED_BRANCH or contains_all(
        branch_registry_text,
        [EXPECTED_BRANCH, current_branch_name, "successor"],
    )

    checklist_rows = [
        {
            "item_id": "p63_reads_h64_and_p62",
            "status": "pass",
            "notes": "P63 starts only after H64 and the prior P62 control-sync stack remain landed.",
        },
        {
            "item_id": "p63_current_branch_is_current_published_successor_or_registered_execution_lane",
            "status": "pass" if current_branch_registered else "blocked",
            "notes": "P63 should run either on the published successor branch or on a registered execution successor branch.",
        },
        {
            "item_id": "p63_scratch_branch_remains_available",
            "status": "pass" if branch_exists(SCRATCH_BRANCH) else "blocked",
            "notes": "The scratch integration branch should remain available as the absorbed local base.",
        },
        {
            "item_id": "p63_root_main_remains_quarantined",
            "status": "pass" if root_main_quarantined else "blocked",
            "notes": "Dirty root main must remain parked on its quarantine branch.",
        },
        {
            "item_id": "p63_control_surfaces_expose_successor_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                            EXPECTED_BRANCH,
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        active_wave_text,
                        [
                            "`P63_post_p62_published_successor_promotion_prep`",
                            "`P64_post_p63_release_hygiene_rebaseline`",
                            "`P65_post_p64_merge_prep_control_sync`",
                            f"`{EXPECTED_BRANCH}`",
                        ],
                    ),
                    contains_all(
                        publication_readme_text,
                        [
                            "P63_post_p62_published_successor_promotion_prep",
                            "published successor clean-descendant promotion-prep wave",
                        ],
                    ),
                    contains_all(
                        plans_readme_text,
                        [
                            "2026-04-01-post-p63-successor-merge-prep-design.md",
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                        ],
                    ),
                    contains_all(
                        branch_registry_text,
                        [
                            EXPECTED_BRANCH,
                            current_branch_name,
                            PRESERVED_PRIOR_BRANCH,
                            SCRATCH_BRANCH,
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Current control surfaces must expose P63/P64/P65 as the live successor stack.",
        },
    ]
    claim_packet = {
        "supports": [
            "P63 promotes the clean successor branch above the preserved prior P60/P61/P62 stack.",
            "P63 keeps merge execution absent and preserves the prior published clean descendant explicitly.",
            "P63 leaves dirty-root integration prohibited while advancing live control wording to the successor stack.",
        ],
        "does_not_support": [
            "merge execution",
            "dirty-root integration",
            "runtime reopen",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_published_clean_descendant_wave": "p63_post_p62_published_successor_promotion_prep",
            "current_published_clean_descendant_branch": EXPECTED_BRANCH,
            "current_published_clean_descendant_upstream": published_upstream,
            "preserved_prior_published_clean_descendant_branch": PRESERVED_PRIOR_BRANCH,
            "preserved_prior_published_clean_descendant_upstream": preserved_prior_upstream,
            "current_execution_branch": current_branch_name,
            "current_execution_branch_upstream": current_upstream,
            "preserved_local_integration_branch": SCRATCH_BRANCH,
            "root_main_branch": root_main_branch,
            "root_main_quarantined": root_main_quarantined,
            "merge_posture": "clean_descendant_only_never_dirty_root_main",
            "merge_execution_state": False,
            "selected_outcome": "published_successor_promotion_prep_locked_after_p62",
            "next_required_lane": "p64_release_hygiene_rebaseline_then_p65_merge_prep_control_sync",
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
            {"field": "current_published_clean_descendant_branch", "value": EXPECTED_BRANCH},
            {"field": "current_published_clean_descendant_upstream", "value": published_upstream},
            {"field": "preserved_prior_published_clean_descendant_branch", "value": PRESERVED_PRIOR_BRANCH},
            {"field": "preserved_prior_published_clean_descendant_upstream", "value": preserved_prior_upstream},
            {"field": "current_execution_branch", "value": current_branch_name},
            {"field": "current_execution_branch_upstream", "value": current_upstream},
            {"field": "preserved_local_integration_branch", "value": SCRATCH_BRANCH},
            {"field": "root_main_branch", "value": root_main_branch},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
