"""Export the post-P66/P67/P68 archive-first terminal freeze packet for H65."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P66_SUMMARY_PATH = ROOT / "results" / "P66_post_p65_successor_publication_review" / "summary.json"
P67_SUMMARY_PATH = ROOT / "results" / "P67_post_p66_published_successor_freeze" / "summary.json"
P68_SUMMARY_PATH = ROOT / "results" / "P68_post_p67_release_hygiene_and_control_rebaseline" / "summary.json"
F38_SUMMARY_PATH = ROOT / "results" / "F38_post_h62_r63_dormant_eligibility_profile_dossier" / "summary.json"
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
    h64_summary = read_json(H64_SUMMARY_PATH)["summary"]
    p66_summary = read_json(P66_SUMMARY_PATH)["summary"]
    p67_summary = read_json(P67_SUMMARY_PATH)["summary"]
    p68_summary = read_json(P68_SUMMARY_PATH)["summary"]
    f38_summary = read_json(F38_SUMMARY_PATH)["summary"]

    prerequisites = [
        h64_summary["selected_outcome"] == "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant",
        p66_summary["selected_outcome"] == "successor_publication_review_supports_p67_freeze",
        p67_summary["selected_outcome"] == "published_successor_freeze_locked_after_p66_review",
        p68_summary["selected_outcome"] == "published_frozen_successor_release_hygiene_and_control_rebaselined",
        f38_summary["selected_outcome"] == "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields",
    ]
    all_green = all(prerequisites)

    checklist_rows = [
        {
            "item_id": "h65_preserves_h64",
            "status": "pass" if prerequisites[0] else "blocked",
            "notes": "H64 remains the preserved prior active packet under H65.",
        },
        {
            "item_id": "h65_reads_p66",
            "status": "pass" if prerequisites[1] else "blocked",
            "notes": "P66 must already confirm the exact successor review range and scope.",
        },
        {
            "item_id": "h65_reads_p67",
            "status": "pass" if prerequisites[2] else "blocked",
            "notes": "P67 must already freeze the new published successor branch.",
        },
        {
            "item_id": "h65_reads_p68",
            "status": "pass" if prerequisites[3] else "blocked",
            "notes": "P68 must already reanchor release hygiene and control on p66.",
        },
        {
            "item_id": "h65_reads_f38",
            "status": "pass" if prerequisites[4] else "blocked",
            "notes": "F38 must remain the only dormant future dossier and remain non-runtime only.",
        },
        {
            "item_id": "h65_runtime_stays_closed",
            "status": "pass",
            "notes": "H65 does not authorize runtime; any future R63 remains dormant and advisory-only unless a later explicit packet says otherwise.",
        },
    ]
    claim_packet = {
        "supports": [
            "H65 makes archive-first terminal freeze the active repo route above the preserved H64 packet.",
            "H65 keeps explicit archive stop or hygiene-only follow-through as the default downstream state.",
            "H65 keeps R63 dormant and non-runtime only rather than converting it into authorization.",
        ],
        "does_not_support": [
            "runtime reopening",
            "same-lane executor-value reopening",
            "integration through dirty root main",
        ],
        "distilled_result": {
            "active_stage": "h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "preserved_prior_active_packet": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_publication_review_wave": "p66_post_p65_successor_publication_review",
            "current_publication_freeze_wave": "p67_post_p66_published_successor_freeze",
            "current_release_hygiene_and_control_rebaseline_wave": "p68_post_p67_release_hygiene_and_control_rebaseline",
            "current_published_clean_descendant_branch": "wip/p66-post-p65-published-successor-freeze",
            "preserved_prior_successor_stack": "p63_p64_p65",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "default_downstream_lane": "explicit_archive_stop_or_hygiene_only",
            "conditional_downstream_lane": R63_NAME,
            "all_prerequisites_green": all_green,
            "runtime_authorization": "closed",
            "selected_outcome": "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop",
            "next_required_lane": "explicit_archive_stop_or_hygiene_only",
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
            {"field": "default_downstream_lane", "value": "explicit_archive_stop_or_hygiene_only"},
            {"field": "conditional_downstream_lane", "value": R63_NAME},
            {"field": "all_prerequisites_green", "value": all_green},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
