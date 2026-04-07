"""Export the post-P74 published successor freeze sidecar for P75."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P75_post_p74_published_successor_freeze"
P74_SUMMARY_PATH = ROOT / "results" / "P74_post_p73_successor_publication_review" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
ACTIVE_WAVE_PLAN_PATH = ROOT / "tmp" / "active_wave_plan.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
EXPECTED_BRANCH = "wip/p75-post-p74-published-successor-freeze"
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
    p74_summary = read_json(P74_SUMMARY_PATH)["summary"]
    if p74_summary["selected_outcome"] != "successor_publication_review_supports_p75_freeze":
        raise RuntimeError("P75 expects the landed P74 successor publication review.")

    current_branch_name = current_branch()
    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    active_wave_text = read_text(ACTIVE_WAVE_PLAN_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)

    checklist_rows = [
        {
            "item_id": "p75_reads_p74",
            "status": "pass",
            "notes": "P75 starts only after the exact P74 successor review lands.",
        },
        {
            "item_id": "p75_current_branch_is_new_published_clean_descendant",
            "status": "pass" if current_branch_name == EXPECTED_BRANCH else "blocked",
            "notes": "The publication freeze should run on the new p75 branch itself.",
        },
        {
            "item_id": "p75_live_control_surfaces_expose_h65_plus_p73_p74_p75_p76",
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
                            PRESERVED_REVIEW_BRANCH,
                            EXPECTED_BRANCH,
                        ],
                    ),
                    contains_all(
                        active_wave_text,
                        [
                            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                            "`P73_post_p72_legacy_worktree_shrink_inventory_and_keep_set_sync`",
                            "`P74_post_p73_successor_publication_review`",
                            "`P75_post_p74_published_successor_freeze`",
                            "`P76_post_p75_release_hygiene_and_control_rebaseline`",
                            f"`{PRESERVED_REVIEW_BRANCH}`",
                            f"`{EXPECTED_BRANCH}`",
                        ],
                    ),
                    contains_all(
                        publication_readme_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P74_post_p73_successor_publication_review",
                            "P75_post_p74_published_successor_freeze",
                            "P76_post_p75_release_hygiene_and_control_rebaseline",
                            "current published successor promotion stack",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Current live surfaces must expose the new successor promotion stack above H65 without reopening runtime.",
        },
        {
            "item_id": "p75_registry_preserves_p66_p73_and_p74",
            "status": "pass"
            if contains_all(
                branch_registry_text,
                [
                    EXPECTED_BRANCH,
                    PRESERVED_REVIEW_BRANCH,
                    CURRENT_LOCAL_HYGIENE_BRANCH,
                    PRESERVED_PRIOR_PUBLISHED_BRANCH,
                    "clean_descendant_only_never_dirty_root_main",
                ],
            )
            else "blocked",
            "notes": "The freeze must preserve p66 as prior published lineage while keeping p73 and p74 explicit.",
        },
    ]
    claim_packet = {
        "supports": [
            "P75 promotes p75 into the live published clean descendant after the exact P74 review.",
            "P75 preserves p66 as the prior published clean descendant and keeps p73 and p74 explicit as local lineage.",
            "P75 keeps merge execution absent while updating live control wording to the new published successor stack.",
        ],
        "does_not_support": [
            "dirty-root integration",
            "runtime reopen",
            "merge execution",
        ],
        "distilled_result": {
            "current_published_clean_descendant_branch": EXPECTED_BRANCH,
            "preserved_prior_published_clean_descendant_branch": PRESERVED_PRIOR_PUBLISHED_BRANCH,
            "preserved_prior_successor_review_branch": PRESERVED_REVIEW_BRANCH,
            "current_local_hygiene_branch": CURRENT_LOCAL_HYGIENE_BRANCH,
            "current_execution_branch": current_branch_name,
            "selected_outcome": "published_successor_freeze_locked_after_p74_review",
            "next_required_lane": "p76_release_hygiene_and_control_rebaseline",
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
            {"field": "preserved_prior_published_clean_descendant_branch", "value": PRESERVED_PRIOR_PUBLISHED_BRANCH},
            {"field": "preserved_prior_successor_review_branch", "value": PRESERVED_REVIEW_BRANCH},
            {"field": "current_local_hygiene_branch", "value": CURRENT_LOCAL_HYGIENE_BRANCH},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
