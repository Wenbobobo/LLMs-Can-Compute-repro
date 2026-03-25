"""Export the actual post-H54 useful-kernel reentry packet for H55."""

from __future__ import annotations

import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H55_post_h54_useful_kernel_reentry_packet"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    checklist_rows = [
        {
            "item_id": "h55_preserves_h54_as_prior_compiled_boundary_closeout",
            "status": "pass",
            "notes": "H55 reopens only one later packet above H54 rather than treating H54 as overturned.",
        },
        {
            "item_id": "h55_authorizes_only_r60_as_next_runtime_candidate",
            "status": "pass",
            "notes": "The only admissible positive route is authorize_useful_kernel_carryover_through_r60_first.",
        },
        {
            "item_id": "h55_keeps_h43_ceiling_and_f27_r53_r54_blocked",
            "status": "pass",
            "notes": "The reentry packet does not widen above the preserved H43 bounded useful-case ceiling.",
        },
    ]
    claim_packet = {
        "supports": [
            "H55 authorizes one minimal useful-kernel carryover reentry through R60 only.",
            "H55 preserves H54 as the prior compiled-boundary closeout and H52 as the prior mechanism closeout.",
            "H55 keeps H43 as the paper-grade endpoint and leaves F27/R53/R54 blocked.",
        ],
        "does_not_support": [
            "automatic widening into histogram16_u8 on first reentry",
            "automatic reopening of transformed or trainable entry",
            "any claim that useful-kernel carryover has already succeeded",
        ],
        "distilled_result": {
            "active_stage": "h55_post_h54_useful_kernel_reentry_packet",
            "preserved_prior_docs_only_closeout": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "preserved_prior_mechanism_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "current_low_priority_wave": "p39_post_h54_successor_worktree_hygiene_sync",
            "selected_outcome": "authorize_useful_kernel_carryover_through_r60_first",
            "only_next_runtime_candidate_if_activated": "r60_origin_compiled_useful_kernel_carryover_gate",
            "next_required_lane_if_activated": "r60_origin_compiled_useful_kernel_carryover_gate",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": len(checklist_rows),
            "blocked_count": 0,
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {
                "decision": "authorize_useful_kernel_carryover_through_r60_first",
                "reason": "H54 closed the toy compiled-boundary lane positively enough to justify one minimal useful-kernel falsification pass.",
            },
            {
                "decision": "keep_h54_terminal_and_stop_before_useful_kernel_reentry",
                "selected": False,
                "reason": "Not selected because the minimal useful-kernel question remains scientifically material.",
            },
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
