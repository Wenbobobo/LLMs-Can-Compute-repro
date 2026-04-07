"""Export the post-H56 last-discriminator authorization packet for H57."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H57_post_h56_last_discriminator_authorization_packet"
H56_SUMMARY_PATH = ROOT / "results" / "H56_post_r60_r61_useful_kernel_decision_packet" / "summary.json"
F31_SUMMARY_PATH = ROOT / "results" / "F31_post_h56_final_discriminating_value_boundary_bundle" / "summary.json"


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
    f31_summary = read_json(F31_SUMMARY_PATH)["summary"]
    if h56_summary["selected_outcome"] != "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value":
        raise RuntimeError("H57 expects the landed H56 freeze-without-bounded-value outcome.")
    if f31_summary["only_runtime_candidate"] != "r62_origin_native_useful_kernel_value_discriminator_gate":
        raise RuntimeError("H57 expects F31 to fix R62 as the only next runtime candidate.")

    selected_outcome = "authorize_one_last_native_useful_kernel_value_discriminator_gate"
    checklist_rows = [
        {
            "item_id": "h57_reads_h56_closeout_before_reopening",
            "status": "pass",
            "notes": "H57 preserves H56 rather than treating the closed useful-kernel bridge lane as open.",
        },
        {
            "item_id": "h57_reads_f31_fixed_sequence",
            "status": "pass",
            "notes": "H57 authorizes only the single R62 native discriminator fixed by F31.",
        },
        {
            "item_id": "h57_writes_stop_rule_up_front",
            "status": "pass",
            "notes": "If R62 cannot show bounded value on the declared native useful-kernel rows, the mainline stops at H58.",
        },
        {
            "item_id": "h57_keeps_scope_ceiling_narrow",
            "status": "pass",
            "notes": "A positive R62 would authorize at most one later narrow coprocessor packet.",
        },
    ]
    claim_packet = {
        "supports": [
            "H57 authorizes one last native useful-kernel value discriminator after H56 closed the compiled useful-kernel lane.",
            "H57 fixes R62 as the only next runtime candidate and H58 as the only follow-up packet.",
            "H57 keeps the scientific target at bounded executor value on the current append-only substrate.",
        ],
        "does_not_support": [
            "more compiled useful-kernel expansion",
            "reopening broad executor entry",
            "scope lift above a narrow coprocessor-style interpretation",
        ],
        "distilled_result": {
            "active_stage": "h57_post_h56_last_discriminator_authorization_packet",
            "preserved_prior_docs_only_closeout": "h56_post_r60_r61_useful_kernel_decision_packet",
            "current_planning_bundle": "f31_post_h56_final_discriminating_value_boundary_bundle",
            "current_low_priority_wave": "p40_post_h56_successor_worktree_and_artifact_hygiene_sync",
            "selected_outcome": selected_outcome,
            "only_next_runtime_candidate": "r62_origin_native_useful_kernel_value_discriminator_gate",
            "only_later_packet": "h58_post_r62_origin_value_boundary_closeout_packet",
            "current_downstream_scientific_lane": "r62_origin_native_useful_kernel_value_discriminator_gate",
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
            {"source": "h56", "selected_outcome": h56_summary["selected_outcome"]},
            {
                "source": "f31",
                "only_runtime_candidate": f31_summary["only_runtime_candidate"],
                "only_later_packet": f31_summary["only_later_packet"],
            },
            {"source": "h57", "selected_outcome": selected_outcome},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
