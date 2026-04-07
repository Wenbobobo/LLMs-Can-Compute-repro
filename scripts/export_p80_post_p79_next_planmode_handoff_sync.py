"""Export the post-P79 next-planmode handoff sync sidecar for P80."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P80_post_p79_next_planmode_handoff_sync"
P79_SUMMARY_PATH = ROOT / "results" / "P79_post_p78_archive_claim_boundary_and_reopen_screen" / "summary.json"
POST_P80_HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-05-post-p80-next-planmode-handoff.md"
POST_P80_STARTUP_PATH = ROOT / "docs" / "plans" / "2026-04-05-post-p80-next-planmode-startup-prompt.md"
POST_P80_BRIEF_PATH = ROOT / "docs" / "plans" / "2026-04-05-post-p80-next-planmode-brief-prompt.md"
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
    p79_summary = read_json(P79_SUMMARY_PATH)["summary"]
    if p79_summary["selected_outcome"] != "archive_claim_boundary_and_reopen_screen_locked_after_convergence":
        raise RuntimeError("P80 expects the landed P79 archive claim-boundary and reopen-screen sidecar.")

    handoff_text = read_text(POST_P80_HANDOFF_PATH)
    startup_text = read_text(POST_P80_STARTUP_PATH)
    brief_text = read_text(POST_P80_BRIEF_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)

    checklist_rows = [
        {"item_id": "p80_reads_p79", "status": "pass", "notes": "P80 starts only after the landed P79 sidecar."},
        {
            "item_id": "p80_handoff_surfaces_select_explicit_stop",
            "status": "pass"
            if all(
                (
                    contains_all(
                        handoff_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P80_post_p79_next_planmode_handoff_sync",
                            "wip/p75-post-p74-published-successor-freeze",
                            "explicit stop",
                            "no further action",
                            "only future gate remains strictly non-runtime",
                            "dirty-root integration remains out of bounds",
                        ],
                    ),
                    contains_all(
                        startup_text,
                        [
                            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                            "P80_post_p79_next_planmode_handoff_sync",
                            "wip/p75-post-p74-published-successor-freeze",
                            "explicit stop",
                            "no further action",
                            "only discuss r63 if it remains strictly non-runtime",
                        ],
                    ),
                    contains_all(
                        brief_text,
                        [
                            "P80_post_p79_next_planmode_handoff_sync",
                            "explicit stop",
                            "no further action",
                            "strictly non-runtime future gate only",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "All next-planmode prompts should default to explicit stop/no further action.",
        },
        {
            "item_id": "p80_plans_router_points_to_post_p80_prompts",
            "status": "pass"
            if contains_all(
                plans_readme_text,
                [
                    "2026-04-05-post-p80-next-planmode-handoff.md",
                    "2026-04-05-post-p80-next-planmode-startup-prompt.md",
                    "2026-04-05-post-p80-next-planmode-brief-prompt.md",
                ],
            )
            else "blocked",
            "notes": "Plans router should point to the post-P80 handoff surfaces as the current entrypoints.",
        },
    ]
    claim_packet = {
        "supports": [
            "P80 synchronizes the next plan-mode prompts to the explicit-stop, no-further-action default.",
            "P80 keeps any future discussion constrained to a strictly non-runtime gate.",
            "P80 leaves dirty-root integration and same-lane executor-value reopen out of bounds.",
        ],
        "does_not_support": ["runtime reopen", "dirty-root integration", "executor-value continuation"],
        "distilled_result": {
            "current_handoff_sync_wave": "p80_post_p79_next_planmode_handoff_sync",
            "selected_outcome": "next_planmode_handoff_synced_to_explicit_stop_after_p79",
            "next_required_lane": "explicit_stop_or_no_further_action",
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
            {"field": "handoff_path", "value": str(POST_P80_HANDOFF_PATH).replace("\\", "/")},
            {"field": "startup_path", "value": str(POST_P80_STARTUP_PATH).replace("\\", "/")},
            {"field": "brief_path", "value": str(POST_P80_BRIEF_PATH).replace("\\", "/")},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
