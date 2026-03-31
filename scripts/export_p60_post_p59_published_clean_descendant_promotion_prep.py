"""Export the post-P59 published clean-descendant promotion-prep sidecar for P60."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P60_post_p59_published_clean_descendant_promotion_prep"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P56_SUMMARY_PATH = ROOT / "results" / "P56_post_h64_clean_merge_candidate_packet" / "summary.json"
P57_SUMMARY_PATH = ROOT / "results" / "P57_post_h64_paper_submission_package_sync" / "summary.json"
P58_SUMMARY_PATH = ROOT / "results" / "P58_post_h64_archive_release_closeout_sync" / "summary.json"
P59_SUMMARY_PATH = ROOT / "results" / "P59_post_h64_control_and_handoff_sync" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ACTIVE_WAVE_PLAN_PATH = ROOT / "tmp" / "active_wave_plan.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
EXPECTED_BRANCH = "wip/p60-post-p59-published-clean-descendant-prep"
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
    p56_summary = read_json(P56_SUMMARY_PATH)["summary"]
    p57_summary = read_json(P57_SUMMARY_PATH)["summary"]
    p58_summary = read_json(P58_SUMMARY_PATH)["summary"]
    p59_summary = read_json(P59_SUMMARY_PATH)["summary"]
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P60 expects the landed H64 freeze packet.")
    if p56_summary["selected_outcome"] != "clean_descendant_merge_candidate_staged_without_merge_execution":
        raise RuntimeError("P60 expects the landed P56 merge-candidate packet.")
    if p57_summary["selected_outcome"] != "paper_submission_package_surfaces_synced_to_h64_followthrough_stack":
        raise RuntimeError("P60 expects the landed P57 paper/submission sync.")
    if p58_summary["selected_outcome"] != "archive_release_closeout_surfaces_synced_to_h64_followthrough_stack":
        raise RuntimeError("P60 expects the landed P58 archive/release sync.")
    if p59_summary["selected_outcome"] != "control_and_handoff_surfaces_synced_to_h64_followthrough_stack":
        raise RuntimeError("P60 expects the landed P59 control sync.")

    current_branch_name = current_branch()
    current_upstream = tracked_upstream(current_branch_name)
    published_upstream = tracked_upstream(EXPECTED_BRANCH) if branch_exists(EXPECTED_BRANCH) else ""
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
            "item_id": "p60_reads_h64_p56_p57_p58_p59",
            "status": "pass",
            "notes": "P60 starts only after the landed H64 + P56/P57/P58/P59 stack.",
        },
        {
            "item_id": "p60_current_branch_is_expected_published_descendant_or_registered_successor",
            "status": "pass" if current_branch_registered else "blocked",
            "notes": "P60 should run either on the published clean-descendant branch or on a registered successor clean descendant.",
        },
        {
            "item_id": "p60_scratch_branch_remains_available",
            "status": "pass" if branch_exists(SCRATCH_BRANCH) else "blocked",
            "notes": "The scratch integration branch should remain available as the absorbed local base.",
        },
        {
            "item_id": "p60_root_main_remains_quarantined",
            "status": "pass" if root_main_quarantined else "blocked",
            "notes": "Dirty root main must remain parked on its quarantine branch.",
        },
        {
            "item_id": "p60_control_surfaces_expose_published_descendant_wave",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "P60_post_p59_published_clean_descendant_promotion_prep",
                            EXPECTED_BRANCH,
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        active_wave_text,
                        [
                            "`P60_post_p59_published_clean_descendant_promotion_prep`",
                            f"`{EXPECTED_BRANCH}`",
                            f"`{SCRATCH_BRANCH}`",
                        ],
                    ),
                    contains_all(
                        publication_readme_text,
                        [
                            "P60_post_p59_published_clean_descendant_promotion_prep",
                            "published clean-descendant promotion-prep wave",
                        ],
                    ),
                    contains_all(
                        plans_readme_text,
                        [
                            "2026-03-31-post-p59-published-clean-descendant-merge-prep-design.md",
                            "P60_post_p59_published_clean_descendant_promotion_prep",
                        ],
                    ),
                    contains_all(
                        branch_registry_text,
                        [EXPECTED_BRANCH, SCRATCH_BRANCH, "clean_descendant_only_never_dirty_root_main"],
                    ),
                )
            )
            else "blocked",
            "notes": "Current control surfaces must expose P60 as the current published clean-descendant wave.",
        },
    ]
    claim_packet = {
        "supports": [
            "P60 locks a dedicated published clean descendant above the landed H64 follow-through stack.",
            "P60 keeps the scratch branch as a preserved local integration base rather than the publication branch.",
            "P60 keeps merge execution absent and dirty-root integration prohibited.",
        ],
        "does_not_support": [
            "merge execution",
            "dirty-root integration",
            "runtime reopen",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_published_clean_descendant_wave": "p60_post_p59_published_clean_descendant_promotion_prep",
            "current_published_clean_descendant_branch": EXPECTED_BRANCH,
            "current_published_clean_descendant_upstream": published_upstream,
            "current_execution_branch": current_branch_name,
            "current_execution_branch_upstream": current_upstream,
            "preserved_local_integration_branch": SCRATCH_BRANCH,
            "root_main_branch": root_main_branch,
            "root_main_quarantined": root_main_quarantined,
            "merge_posture": "clean_descendant_only_never_dirty_root_main",
            "merge_execution_state": False,
            "selected_outcome": "published_clean_descendant_promotion_prep_locked_after_p59",
            "next_required_lane": "p61_release_hygiene_rebaseline_then_p62_merge_prep_control_sync",
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
