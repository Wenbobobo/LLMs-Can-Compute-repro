"""Export the post-R33 same-endpoint decision packet for H27."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H27_refreeze_after_r32_r33_same_endpoint_decision"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    inputs: dict[str, Any] = {
        "h27_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "README.md"
        ),
        "h27_status_text": read_text(
            ROOT / "docs" / "milestones" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "status.md"
        ),
        "h27_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "todo.md"
        ),
        "h27_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "acceptance.md"
        ),
        "h27_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "artifact_index.md"
        ),
        "h26_summary_text": read_text(ROOT / "results" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "summary.json"),
        "r33_summary_text": read_text(ROOT / "results" / "R33_d0_non_retrieval_overhead_localization_audit" / "summary.json"),
        "r31_summary_text": read_text(
            ROOT / "results" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "summary.json"
        ),
    }
    inputs["h26_summary"] = read_json(ROOT / "results" / "H26_refreeze_after_r32_boundary_sharp_zoom" / "summary.json")
    inputs["r33_summary"] = read_json(ROOT / "results" / "R33_d0_non_retrieval_overhead_localization_audit" / "summary.json")
    inputs["r31_summary"] = read_json(
        ROOT / "results" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "summary.json"
    )
    return inputs


def build_checklist_rows(
    *,
    h27_readme_text: str,
    h27_status_text: str,
    h27_todo_text: str,
    h27_acceptance_text: str,
    h27_artifact_index_text: str,
    h26_summary_text: str,
    h26_summary: dict[str, Any],
    r33_summary_text: str,
    r33_summary: dict[str, Any],
    r31_summary_text: str,
    r31_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h26 = h26_summary["summary"]
    r33 = r33_summary["summary"]
    r33_gate = r33["gate"]
    r31 = r31_summary["summary"]
    return [
        {
            "item_id": "h27_docs_freeze_one_explicit_post_r33_same_endpoint_packet",
            "status": "pass"
            if contains_all(
                h27_readme_text,
                ["freeze the post-`R32/R33` same-endpoint state", "systems story", "blocked future lanes"],
            )
            and contains_all(
                h27_status_text,
                ["executed", "`R33`", "`R29`", "`F3`", "scope"],
            )
            and contains_all(
                h27_todo_text,
                ["post-`R33`", "systems state", "`R29`, `F3`, and `F2`"],
            )
            and contains_all(
                h27_acceptance_text,
                ["post-`R33` same-endpoint decision packet", "blocked future lanes", "does not widen scope"],
            )
            and contains_all(
                h27_artifact_index_text,
                [
                    "results/R33_d0_non_retrieval_overhead_localization_audit/summary.json",
                    "results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json",
                    "F2_future_frontier_recheck_activation_matrix",
                ],
            )
            else "blocked",
            "notes": "H27 should freeze one explicit post-R33 same-endpoint decision packet.",
        },
        {
            "item_id": "h26_explicitly_activates_r33_and_r33_exports_one_bounded_verdict",
            "status": "pass"
            if str(h26["next_priority_lane"]) == "r33_d0_non_retrieval_overhead_localization_audit"
            and str(r33_gate["next_priority_lane"]) == "h27_refreeze_after_r32_r33_same_endpoint_decision"
            and contains_all(
                h26_summary_text,
                ['"next_priority_lane": "r33_d0_non_retrieval_overhead_localization_audit"'],
            )
            and contains_all(
                r33_summary_text,
                ['"status": "r33_non_retrieval_overhead_localization_complete"', '"next_priority_lane": "h27_refreeze_after_r32_r33_same_endpoint_decision"'],
            )
            else "blocked",
            "notes": "H27 should only exist because H26 preserved R33 and R33 actually executed.",
        },
        {
            "item_id": "r31_and_h27_keep_r29_blocked_without_auto_reauthorization",
            "status": "pass"
            if str(r31["recommended_next_lane"]) == "r33_d0_non_retrieval_overhead_localization_audit"
            and contains_all(
                r31_summary_text,
                ['"recommended_next_lane": "r33_d0_non_retrieval_overhead_localization_audit"'],
            )
            else "blocked",
            "notes": "H27 should preserve the R31 discipline that R33 does not directly authorize R29.",
        },
    ]


def derive_systems_verdict(r33_verdict: str) -> str:
    if r33_verdict in {
        "suite_stable_noncompetitive_after_localization",
        "instrumentation_blocked_without_scope_drift",
    }:
        return "systems_more_sharply_negative"
    if r33_verdict == "non_retrieval_overhead_localized":
        return "systems_still_mixed"
    return "systems_still_mixed"


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    h26 = inputs["h26_summary"]["summary"]
    r33 = inputs["r33_summary"]["summary"]
    r33_gate = r33["gate"]
    systems_verdict = derive_systems_verdict(str(r33_gate["lane_verdict"]))

    supported_here = [
        "H27 keeps the same tiny typed-bytecode D0 endpoint and freezes the post-R33 state instead of reopening execution by momentum.",
        f"R33 ended at `{r33_gate['lane_verdict']}` under audit scope `{r33_gate['audit_scope']}`.",
        "H27 preserves blocked future lanes explicitly rather than turning the attribution lane into automatic recovery authorization.",
    ]
    if systems_verdict == "systems_more_sharply_negative":
        supported_here.append("The post-R33 systems story is now more sharply negative than the earlier mixed reading.")
    else:
        supported_here.append("The post-R33 systems story remains mixed on the current endpoint.")

    unsupported_here = [
        "H27 does not widen beyond the fixed tiny typed-bytecode D0 endpoint.",
        "H27 does not authorize direct R29 execution.",
        "H27 does not authorize F3 or bypass F2 by momentum.",
    ]

    disconfirmed_here: list[str] = []
    if str(r33_gate["lane_verdict"]) == "suite_stable_noncompetitive_after_localization":
        disconfirmed_here.append(
            "The narrower expectation that bounded overhead localization alone would make current same-endpoint recovery look directly viable."
        )

    return {
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
        "distilled_result": {
            "h26_boundary_verdict": h26["boundary_verdict"],
            "r33_lane_verdict": r33_gate["lane_verdict"],
            "systems_verdict": systems_verdict,
            "r29_state": "blocked_preserved",
            "f3_state": "blocked_preserved",
            "f2_state": "planning_only_preserved",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h26 = inputs["h26_summary"]["summary"]
    r33_gate = inputs["r33_summary"]["summary"]["gate"]
    r31 = inputs["r31_summary"]["summary"]
    return [
        {
            "source": "results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json",
            "fields": {
                "boundary_verdict": h26["boundary_verdict"],
                "next_priority_lane": h26["next_priority_lane"],
            },
        },
        {
            "source": "results/R33_d0_non_retrieval_overhead_localization_audit/summary.json",
            "fields": {
                "lane_verdict": r33_gate["lane_verdict"],
                "audit_scope": r33_gate["audit_scope"],
            },
        },
        {
            "source": "results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json",
            "fields": {
                "systems_reauthorization_verdict": r31["systems_reauthorization_verdict"],
                "recommended_next_lane": r31["recommended_next_lane"],
            },
        },
    ]


def build_summary(
    checklist_rows: list[dict[str, object]],
    inputs: dict[str, Any],
    claim_packet: dict[str, object],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    h26 = inputs["h26_summary"]["summary"]
    r33_gate = inputs["r33_summary"]["summary"]["gate"]
    systems_verdict = derive_systems_verdict(str(r33_gate["lane_verdict"]))
    return {
        "current_paper_phase": "h27_refreeze_after_r32_r33_same_endpoint_decision_complete",
        "active_stage": "h27_refreeze_after_r32_r33_same_endpoint_decision",
        "prior_frozen_stage": "h26_refreeze_after_r32_boundary_sharp_zoom",
        "source_runtime_lane": "r33_d0_non_retrieval_overhead_localization_audit",
        "decision_state": "post_r33_same_endpoint_decision_complete",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "boundary_verdict": h26["boundary_verdict"],
        "systems_verdict": systems_verdict,
        "r33_audit_verdict": r33_gate["lane_verdict"],
        "next_priority_lane": "later_explicit_packet_required_before_new_runtime",
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "future_frontier_review_state": "planning_only_f2_preserved",
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": "Open a new explicit planning packet before any further runtime lane.",
        "supported_here": claim_packet["supported_here"],
        "unsupported_here": claim_packet["unsupported_here"],
        "disconfirmed_here": claim_packet["disconfirmed_here"],
        "distilled_result": claim_packet["distilled_result"],
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    claim_packet = build_claim_packet(inputs)
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h27_refreeze_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h27_refreeze_snapshot", "environment": environment.as_dict(), "rows": snapshot_rows},
    )
    write_json(
        OUT_DIR / "claim_packet.json",
        {"experiment": "h27_refreeze_claim_packet", "environment": environment.as_dict(), "summary": claim_packet},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h27_refreeze_after_r32_r33_same_endpoint_decision",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/README.md",
                "docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/status.md",
                "docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/todo.md",
                "docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/acceptance.md",
                "docs/milestones/H27_refreeze_after_r32_r33_same_endpoint_decision/artifact_index.md",
                "results/H26_refreeze_after_r32_boundary_sharp_zoom/summary.json",
                "results/R33_d0_non_retrieval_overhead_localization_audit/summary.json",
                "results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H27 Refreeze After R32 R33 Same-Endpoint Decision\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n"
        "- `claim_packet.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
