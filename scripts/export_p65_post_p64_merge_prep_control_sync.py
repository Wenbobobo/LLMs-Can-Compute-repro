"""Export the post-P64 merge-prep control sync sidecar for P65."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P65_post_p64_merge_prep_control_sync"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P63_SUMMARY_PATH = ROOT / "results" / "P63_post_p62_published_successor_promotion_prep" / "summary.json"
P64_SUMMARY_PATH = ROOT / "results" / "P64_post_p63_release_hygiene_rebaseline" / "summary.json"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
MILESTONES_README_PATH = ROOT / "docs" / "milestones" / "README.md"
ACTIVE_WAVE_PATH = ROOT / "tmp" / "active_wave_plan.md"
HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-01-post-p65-next-planmode-handoff.md"
STARTUP_PROMPT_PATH = ROOT / "docs" / "plans" / "2026-04-01-post-p65-next-planmode-startup-prompt.md"
BRIEF_PROMPT_PATH = ROOT / "docs" / "plans" / "2026-04-01-post-p65-next-planmode-brief-prompt.md"
CURRENT_PUBLISHED_WAVE = "p63_post_p62_published_successor_promotion_prep"
CURRENT_RELEASE_WAVE = "p64_post_p63_release_hygiene_rebaseline"
CURRENT_CONTROL_WAVE = "p65_post_p64_merge_prep_control_sync"
CURRENT_PUBLISHED_BRANCH = "wip/p63-post-p62-tight-core-hygiene"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    h64_summary = read_json(H64_SUMMARY_PATH)["summary"]
    p63_summary = read_json(P63_SUMMARY_PATH)["summary"]
    p64_summary = read_json(P64_SUMMARY_PATH)["summary"]
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P65 expects the landed H64 freeze packet.")
    if p63_summary["selected_outcome"] != "published_successor_promotion_prep_locked_after_p62":
        raise RuntimeError("P65 expects the landed P63 successor promotion-prep wave.")
    if p64_summary["selected_outcome"] != "published_successor_release_hygiene_rebaselined":
        raise RuntimeError("P65 expects the landed P64 hygiene rebaseline wave.")

    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    milestones_readme_text = read_text(MILESTONES_README_PATH)
    active_wave_text = read_text(ACTIVE_WAVE_PATH)
    handoff_text = read_text(HANDOFF_PATH)
    startup_prompt_text = read_text(STARTUP_PROMPT_PATH)
    brief_prompt_text = read_text(BRIEF_PROMPT_PATH)

    checklist_rows = [
        {
            "item_id": "p65_reads_h64_p63_p64",
            "status": "pass",
            "notes": "P65 starts only after H64 plus P63/P64 remain green.",
        },
        {
            "item_id": "p65_control_surfaces_expose_current_published_successor_stack",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                            CURRENT_PUBLISHED_BRANCH,
                            "`archive_or_hygiene_stop`",
                        ],
                    ),
                    contains_all(
                        plans_readme_text,
                        [
                            "2026-04-01-post-p63-successor-merge-prep-design.md",
                            "2026-04-01-post-p65-next-planmode-handoff.md",
                            "2026-04-01-post-p65-next-planmode-startup-prompt.md",
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                        ],
                    ),
                    contains_all(
                        milestones_readme_text,
                        [
                            "P65_post_p64_merge_prep_control_sync/",
                            "P64_post_p63_release_hygiene_rebaseline/",
                            "P63_post_p62_published_successor_promotion_prep/",
                        ],
                    ),
                    contains_all(
                        active_wave_text,
                        [
                            "`P65_post_p64_merge_prep_control_sync`",
                            "`P64_post_p63_release_hygiene_rebaseline`",
                            "`P63_post_p62_published_successor_promotion_prep`",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "Control surfaces must expose the live published successor merge-prep stack.",
        },
        {
            "item_id": "p65_handoff_and_startup_prompt_are_current",
            "status": "pass"
            if all(
                (
                    contains_all(
                        handoff_text,
                        [
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                            CURRENT_PUBLISHED_BRANCH,
                        ],
                    ),
                    contains_all(
                        startup_prompt_text,
                        [
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "P63_post_p62_published_successor_promotion_prep",
                            "P64_post_p63_release_hygiene_rebaseline",
                            "P65_post_p64_merge_prep_control_sync",
                            "archive_or_hygiene_stop",
                            "Do not reopen same-lane executor-value work",
                        ],
                    ),
                    contains_all(
                        brief_prompt_text,
                        [
                            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
                            "P63",
                            "P64",
                            "P65",
                            "archive_or_hygiene_stop",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The next entrypoint handoff, startup, and brief docs must start from the P65 successor control state.",
        },
    ]
    claim_packet = {
        "supports": [
            "P65 synchronizes current control and next-entrypoint surfaces to the published successor stack.",
            "P65 keeps H64 active while leaving runtime closed and merge execution absent.",
            "P65 makes the next decision explicitly review/merge-prep or archive-first stop, not scientific reopen.",
        ],
        "does_not_support": [
            "runtime reopen",
            "merge execution",
            "dirty-root integration",
        ],
        "distilled_result": {
            "active_stage": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_published_clean_descendant_wave": CURRENT_PUBLISHED_WAVE,
            "current_release_hygiene_rebaseline_wave": CURRENT_RELEASE_WAVE,
            "current_merge_prep_control_sync_wave": CURRENT_CONTROL_WAVE,
            "selected_outcome": "published_successor_merge_prep_control_synced_to_h64_stack",
            "next_required_lane": "later_published_successor_review_or_explicit_archive_stop_decision",
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
            {"field": "current_published_clean_descendant_wave", "value": CURRENT_PUBLISHED_WAVE},
            {"field": "current_release_hygiene_rebaseline_wave", "value": CURRENT_RELEASE_WAVE},
            {"field": "current_merge_prep_control_sync_wave", "value": CURRENT_CONTROL_WAVE},
            {"field": "handoff_path", "value": "docs/plans/2026-04-01-post-p65-next-planmode-handoff.md"},
            {"field": "startup_prompt_path", "value": "docs/plans/2026-04-01-post-p65-next-planmode-startup-prompt.md"},
            {"field": "brief_prompt_path", "value": "docs/plans/2026-04-01-post-p65-next-planmode-brief-prompt.md"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
