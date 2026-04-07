"""Export the post-P90 archive-replace terminal-stop packet for H66."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H66_post_p90_archive_replace_terminal_stop_packet"
H65_SUMMARY_PATH = ROOT / "results" / "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet" / "summary.json"
P90_SUMMARY_PATH = ROOT / "results" / "P90_post_p89_archive_replace_screen_and_replacement_decision" / "summary.json"
CURRENT_BRANCH = "wip/p85-post-p84-main-rebaseline"
R63_NAME = "r63_post_h62_coprocessor_eligibility_profile_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    h65_summary = read_json(H65_SUMMARY_PATH)["summary"]
    p90_summary = read_json(P90_SUMMARY_PATH)["summary"]

    prerequisites = [
        h65_summary["selected_outcome"] == "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop",
        p90_summary["selected_outcome"] == "archive_replace_screen_completed_with_no_additional_salvage_after_p89",
        int(p90_summary["file_specific_salvage_required_count"]) == 0,
    ]
    all_green = all(prerequisites)

    checklist_rows = [
        {
            "item_id": "h66_reads_h65",
            "status": "pass" if prerequisites[0] else "blocked",
            "notes": "H65 must remain the preserved prior active packet before H66 can become current.",
        },
        {
            "item_id": "h66_reads_green_p90",
            "status": "pass" if prerequisites[1] else "blocked",
            "notes": "P90 must already close the archive-replace screen with no additional salvage required.",
        },
        {
            "item_id": "h66_requires_zero_file_specific_salvage",
            "status": "pass" if prerequisites[2] else "blocked",
            "notes": "H66 assumes the remaining dirty-root publication docs stay keep-clean/archive-root-only.",
        },
        {
            "item_id": "h66_runtime_stays_closed",
            "status": "pass",
            "notes": "H66 remains docs-only and does not authorize runtime or any same-lane scientific reopen.",
        },
    ]
    claim_packet = {
        "supports": [
            "H66 promotes archive-replace terminal stop to the current active docs-only packet above preserved H65.",
            "H66 defaults the downstream route to explicit stop, archive polish, or no further action.",
            "H66 keeps any future R63 discussion strictly non-runtime and non-authorizing.",
        ],
        "does_not_support": [
            "runtime reopening",
            "same-lane executor-value reopening",
            "dirty-root integration",
            "broad Wasm or arbitrary C widening",
        ],
        "distilled_result": {
            "active_stage": "h66_post_p90_archive_replace_terminal_stop_packet",
            "preserved_prior_active_packet": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "current_archive_replace_wave": "p90_post_p89_archive_replace_screen_and_replacement_decision",
            "current_clean_branch": CURRENT_BRANCH,
            "default_downstream_lane": "explicit_stop_or_no_further_action_archive_first",
            "secondary_downstream_lane": "archive_polish_or_hygiene_only_docs_cleanup",
            "conditional_downstream_lane": R63_NAME,
            "all_prerequisites_green": all_green,
            "runtime_authorization": "closed",
            "selected_outcome": "archive_replace_terminal_stop_becomes_current_active_route_and_defaults_to_explicit_stop",
            "next_required_lane": "explicit_stop_or_no_further_action_archive_first",
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
            {"field": "preserved_prior_active_packet", "value": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet"},
            {"field": "current_archive_replace_wave", "value": "p90_post_p89_archive_replace_screen_and_replacement_decision"},
            {"field": "next_required_lane", "value": "explicit_stop_or_no_further_action_archive_first"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
