"""Export the post-H66 next-planmode handoff sync sidecar for P91."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P91_post_h66_next_planmode_handoff_sync"
H66_SUMMARY_PATH = ROOT / "results" / "H66_post_p90_archive_replace_terminal_stop_packet" / "summary.json"
POST_H66_HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-07-post-h66-next-planmode-handoff.md"
POST_H66_STARTUP_PATH = ROOT / "docs" / "plans" / "2026-04-07-post-h66-next-planmode-startup-prompt.md"
POST_H66_BRIEF_PATH = ROOT / "docs" / "plans" / "2026-04-07-post-h66-next-planmode-brief-prompt.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"


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


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    h66_summary = read_json(H66_SUMMARY_PATH)["summary"]
    if h66_summary["selected_outcome"] != "archive_replace_terminal_stop_becomes_current_active_route_and_defaults_to_explicit_stop":
        raise RuntimeError("P91 expects the landed H66 terminal-stop packet.")

    handoff_text = read_text(POST_H66_HANDOFF_PATH)
    startup_text = read_text(POST_H66_STARTUP_PATH)
    brief_text = read_text(POST_H66_BRIEF_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)

    checklist_rows = [
        {"item_id": "p91_reads_h66", "status": "pass", "notes": "P91 starts only after the landed H66 terminal-stop packet."},
        {
            "item_id": "p91_handoff_surfaces_select_explicit_stop_archive_polish_or_no_further_action",
            "status": "pass"
            if all(
                (
                    contains_all(
                        handoff_text,
                        [
                            "H66_post_p90_archive_replace_terminal_stop_packet",
                            "P91_post_h66_next_planmode_handoff_sync",
                            "wip/p85-post-p84-main-rebaseline",
                            "explicit stop",
                            "archive polish",
                            "no further action",
                            "only discuss r63 if it remains strictly non-runtime",
                            "dirty-root integration remains out of bounds",
                        ],
                    ),
                    contains_all(
                        startup_text,
                        [
                            "H66_post_p90_archive_replace_terminal_stop_packet",
                            "P91_post_h66_next_planmode_handoff_sync",
                            "wip/p85-post-p84-main-rebaseline",
                            "explicit stop",
                            "archive polish",
                            "no further action",
                            "only discuss r63 if it remains strictly non-runtime",
                        ],
                    ),
                    contains_all(
                        brief_text,
                        [
                            "P91_post_h66_next_planmode_handoff_sync",
                            "explicit stop",
                            "archive polish",
                            "no further action",
                            "strictly non-runtime future gate only",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "All next-planmode prompts should default to explicit stop, archive polish, or no further action after H66.",
        },
        {
            "item_id": "p91_plans_router_points_to_post_h66_prompts",
            "status": "pass"
            if contains_all(
                plans_readme_text,
                [
                    "2026-04-07-post-h66-next-planmode-handoff.md",
                    "2026-04-07-post-h66-next-planmode-startup-prompt.md",
                    "2026-04-07-post-h66-next-planmode-brief-prompt.md",
                ],
            )
            else "blocked",
            "notes": "Plans router should point to the post-H66 handoff surfaces as the current entrypoints.",
        },
    ]
    claim_packet = {
        "supports": [
            "P91 syncs the next planning prompts to the honest H66 terminal-stop posture.",
            "P91 keeps the default route at explicit stop, archive polish, or no further action.",
            "P91 leaves any later R63 discussion strictly non-runtime and non-authorizing.",
        ],
        "does_not_support": ["runtime reopen", "dirty-root integration", "executor-value continuation"],
        "distilled_result": {
            "current_handoff_sync_wave": "p91_post_h66_next_planmode_handoff_sync",
            "selected_outcome": "next_planmode_handoff_synced_to_explicit_stop_after_h66",
            "next_required_lane": "explicit_stop_archive_polish_or_no_further_action",
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
            {"field": "handoff_path", "value": str(POST_H66_HANDOFF_PATH).replace("\\", "/")},
            {"field": "startup_path", "value": str(POST_H66_STARTUP_PATH).replace("\\", "/")},
            {"field": "brief_path", "value": str(POST_H66_BRIEF_PATH).replace("\\", "/")},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
