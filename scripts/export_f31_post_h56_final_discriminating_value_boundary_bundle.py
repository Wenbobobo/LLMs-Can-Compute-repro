"""Export the post-H56 final discriminating value-boundary planning bundle for F31."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F31_post_h56_final_discriminating_value_boundary_bundle"
H56_SUMMARY_PATH = ROOT / "results" / "H56_post_r60_r61_useful_kernel_decision_packet" / "summary.json"


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
    h56_summary = read_json(H56_SUMMARY_PATH)["summary"]
    if h56_summary["selected_outcome"] != "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value":
        raise RuntimeError("F31 expects the landed H56 freeze-without-bounded-value outcome.")

    checklist_rows = [
        {
            "item_id": "f31_starts_only_after_closed_h56_lane",
            "status": "pass",
            "notes": "F31 opens only after the H56 useful-kernel bridge lane is explicitly closed.",
        },
        {
            "item_id": "f31_fixes_one_last_sequence_only",
            "status": "pass",
            "notes": "F31 fixes H57 -> R62 -> H58 as the only admissible post-H56 runtime sequence.",
        },
        {
            "item_id": "f31_keeps_broader_routes_blocked",
            "status": "pass",
            "notes": "F27, R53, and R54 remain blocked; arbitrary C and broad Wasm stay out of scope.",
        },
        {
            "item_id": "f31_uses_successor_worktree_sidecar_only",
            "status": "pass",
            "notes": "P40 is the only active low-priority operational sidecar for the successor wave.",
        },
    ]
    claim_packet = {
        "supports": [
            "The post-H56 line may continue only through one final discriminating native useful-kernel packet.",
            "The sole admissible order is F31 -> H57 -> R62 -> H58 with P40 as the only low-priority sidecar.",
            "The active question narrows to bounded executor value on the current append-only substrate.",
        ],
        "does_not_support": [
            "automatic reopening of compiled useful-family growth",
            "automatic reopening of transformed or trainable executor entry",
            "scope lift to arbitrary C or broad Wasm",
        ],
        "distilled_result": {
            "active_stage_at_planning_time": "h56_post_r60_r61_useful_kernel_decision_packet",
            "planning_bundle": "f31_post_h56_final_discriminating_value_boundary_bundle",
            "current_low_priority_wave": "p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
            "only_docs_only_followup": "h57_post_h56_last_discriminator_authorization_packet",
            "only_runtime_candidate": "r62_origin_native_useful_kernel_value_discriminator_gate",
            "only_later_packet": "h58_post_r62_origin_value_boundary_closeout_packet",
            "blocked_future_storage": [
                "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
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
            {
                "source": "h56",
                "selected_outcome": h56_summary["selected_outcome"],
                "current_downstream_scientific_lane": h56_summary["current_downstream_scientific_lane"],
            },
            {
                "source": "f31",
                "fixed_sequence": [
                    "h57_post_h56_last_discriminator_authorization_packet",
                    "r62_origin_native_useful_kernel_value_discriminator_gate",
                    "h58_post_r62_origin_value_boundary_closeout_packet",
                ],
            },
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
