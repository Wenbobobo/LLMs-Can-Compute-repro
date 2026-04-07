"""Export the post-R26/R27/R28 refreeze summary for H23."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H23_refreeze_after_r26_r27_r28"


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


def default_r27_summary() -> dict[str, Any]:
    return {
        "summary": {
            "gate": {
                "execution_mode": "skip",
                "lane_verdict": "skipped_not_triggered",
                "next_priority_lane": "h23_refreeze_after_r26_r27_r28",
            }
        }
    }


def load_inputs() -> dict[str, Any]:
    inputs: dict[str, Any] = {
        "h23_readme_text": read_text(ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "README.md"),
        "h23_status_text": read_text(ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "status.md"),
        "h23_todo_text": read_text(ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "todo.md"),
        "h23_acceptance_text": read_text(ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "acceptance.md"),
        "h23_artifact_index_text": read_text(ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "artifact_index.md"),
        "h23_result_digest_text": read_text(ROOT / "docs" / "milestones" / "H23_refreeze_after_r26_r27_r28" / "result_digest.md"),
        "h21_summary_text": read_text(ROOT / "results" / "H21_refreeze_after_r22_r23" / "summary.json"),
        "h22_summary_text": read_text(ROOT / "results" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "summary.json"),
        "r26_summary_text": read_text(ROOT / "results" / "R26_d0_boundary_localization_execution_gate" / "summary.json"),
        "r28_summary_text": read_text(ROOT / "results" / "R28_d0_trace_retrieval_contract_audit" / "summary.json"),
    }
    inputs["h21_summary"] = read_json(ROOT / "results" / "H21_refreeze_after_r22_r23" / "summary.json")
    inputs["h22_summary"] = read_json(ROOT / "results" / "H22_post_h21_boundary_reopen_and_dual_track_lock" / "summary.json")
    inputs["r26_summary"] = read_json(ROOT / "results" / "R26_d0_boundary_localization_execution_gate" / "summary.json")
    r27_path = ROOT / "results" / "R27_d0_boundary_localization_extension_gate" / "summary.json"
    if r27_path.exists():
        inputs["r27_summary_text"] = read_text(r27_path)
        inputs["r27_summary"] = read_json(r27_path)
    else:
        inputs["r27_summary_text"] = json.dumps(default_r27_summary())
        inputs["r27_summary"] = default_r27_summary()
    inputs["r28_summary"] = read_json(ROOT / "results" / "R28_d0_trace_retrieval_contract_audit" / "summary.json")
    return inputs


def build_checklist_rows(
    *,
    h23_readme_text: str,
    h23_status_text: str,
    h23_todo_text: str,
    h23_acceptance_text: str,
    h23_artifact_index_text: str,
    h23_result_digest_text: str,
    h21_summary_text: str,
    h21_summary: dict[str, Any],
    h22_summary_text: str,
    h22_summary: dict[str, Any],
    r26_summary_text: str,
    r26_summary: dict[str, Any],
    r27_summary_text: str,
    r27_summary: dict[str, Any],
    r28_summary_text: str,
    r28_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h21_state = h21_summary["summary"]
    h22_state = h22_summary["summary"]
    r26_gate = r26_summary["summary"]["gate"]
    r27_gate = r27_summary["summary"]["gate"]
    r28_gate = r28_summary["summary"]["gate"]
    return [
        {
            "item_id": "h23_docs_describe_one_machine_readable_refreeze_packet",
            "status": "pass"
            if contains_all(
                h23_readme_text,
                ["Refreeze", "`R26`", "`R27`", "`R28`", "machine-readable"],
            )
            and contains_all(
                h23_status_text,
                ["`boundary_verdict`", "`mechanism_contract_verdict`", "systems verdict", "next downstream lane"],
            )
            and contains_all(
                h23_todo_text,
                ["`R26`", "`R27`", "`R28`", "machine-readable packet"],
            )
            and contains_all(
                h23_acceptance_text,
                ["machine-readable", "unsupported claims", "next downstream lane"],
            )
            and contains_all(
                h23_artifact_index_text,
                [
                    "results/R26_d0_boundary_localization_execution_gate/summary.json",
                    "results/R28_d0_trace_retrieval_contract_audit/summary.json",
                    "results/H23_refreeze_after_r26_r27_r28/summary.json",
                ],
            )
            else "blocked",
            "notes": "H23 should define one explicit refreeze packet before any outward sync starts.",
        },
        {
            "item_id": "h21_and_h22_remain_the_preserved_controls_under_h23",
            "status": "pass"
            if h21_state["active_stage"] == "h21_refreeze_after_r22_r23"
            and h22_state["current_frozen_stage"] == "h21_refreeze_after_r22_r23"
            and h22_state["active_runtime_lane"] == "r26_d0_boundary_localization_execution_gate"
            and contains_all(
                h21_summary_text,
                ['"active_stage": "h21_refreeze_after_r22_r23"', '"systems_verdict": "systems_still_mixed"'],
            )
            and contains_all(
                h22_summary_text,
                ['"active_stage": "h22_post_h21_boundary_reopen_and_dual_track_lock"', '"active_support_lane": "r28_d0_trace_retrieval_contract_audit"'],
            )
            else "blocked",
            "notes": "H23 is a refreeze on top of H21/H22 rather than a rewrite of the preserved controls.",
        },
        {
            "item_id": "r26_exports_one_explicit_boundary_packet_verdict",
            "status": "pass"
            if str(r26_gate["lane_verdict"])
            in {
                "first_boundary_failure_localized",
                "near_boundary_mixed_signal_needs_confirmation",
                "grid_extended_still_not_localized",
                "resource_limited_before_localization",
            }
            and contains_all(r26_summary_text, ['"source_runtime_stage": "r22_d0_true_boundary_localization_gate"'])
            else "blocked",
            "notes": "H23 must inherit one explicit bounded boundary verdict from R26 before reading R27.",
        },
        {
            "item_id": "r27_is_machine_readable_even_when_skipped",
            "status": "pass"
            if str(r27_gate["execution_mode"]) in {"skip", "confirmation_mode", "extension_mode"}
            and str(r27_gate["next_priority_lane"]) == "h23_refreeze_after_r26_r27_r28"
            and contains_all(r27_summary_text, ['"next_priority_lane": "h23_refreeze_after_r26_r27_r28"'])
            else "blocked",
            "notes": "H23 should not depend on whether R27 actually executed; it only needs one machine-readable R27 state.",
        },
        {
            "item_id": "r28_exports_one_explicit_mechanism_contract_verdict",
            "status": "pass"
            if "mechanism_contract_verdict" in r28_gate
            and str(r28_gate["next_priority_lane"]) == "h23_refreeze_after_r26_r27_r28"
            and contains_all(r28_summary_text, ['"next_priority_lane": "h23_refreeze_after_r26_r27_r28"'])
            and contains_all(
                h23_result_digest_text,
                ["boundary", "mechanism", "systems", "next lane"],
            )
            else "blocked",
            "notes": "H23 should inherit one explicit mechanism-contract verdict rather than restating R28 impressionistically.",
        },
    ]


def map_boundary_verdict(r26_verdict: str, r27_verdict: str) -> str:
    if r26_verdict == "first_boundary_failure_localized" or r27_verdict in {
        "confirmation_failure_localized",
        "extension_failure_localized",
    }:
        return "first_boundary_failure_localized"
    if r26_verdict == "resource_limited_before_localization" or r27_verdict == "resource_limited_before_localization":
        return "resource_limited_without_boundary_localization"
    if r27_verdict in {
        "confirmation_failure_reproduced_without_localization",
        "confirmation_failure_signal_mixed",
        "extension_failure_found_without_localization",
    }:
        return "boundary_signal_not_yet_localized"
    return "bounded_grid_still_not_localized"


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    h21_summary = inputs["h21_summary"]["summary"]
    h22_summary = inputs["h22_summary"]["summary"]
    r26_gate = inputs["r26_summary"]["summary"]["gate"]
    r27_gate = inputs["r27_summary"]["summary"]["gate"]
    r28_gate = inputs["r28_summary"]["summary"]["gate"]

    boundary_verdict = map_boundary_verdict(
        str(r26_gate["lane_verdict"]),
        str(r27_gate["lane_verdict"]),
    )
    mechanism_contract_verdict = str(r28_gate["mechanism_contract_verdict"])
    systems_verdict = str(h21_summary["systems_verdict"])

    supported_here = [
        "H22 reopens the post-H21 mainline only as one bounded dual-track packet on the fixed D0 endpoint.",
        (
            f"R26 executes {r26_gate['executed_candidate_count']}/"
            f"{r26_gate['planned_candidate_count']} planned candidates under the declared first-wave boundary manifest."
        ),
        (
            f"R28 ends at `{mechanism_contract_verdict}` and preserves one explicit claim-layer/primitive audit."
        ),
    ]
    if boundary_verdict == "first_boundary_failure_localized":
        supported_here.append("The reopened boundary packet now localizes one bounded same-endpoint failure.")
    else:
        supported_here.append("The reopened boundary packet remains bounded even when it does not localize a clean failure.")

    unsupported_here = [
        "H23 does not widen beyond the fixed tiny typed-bytecode D0 endpoint.",
        "H23 does not authorize broader compiled-language claims or a wider 'LLMs are computers' headline.",
    ]
    if boundary_verdict != "first_boundary_failure_localized":
        unsupported_here.append("The true executor boundary is still not localized strongly enough for a broader scope lift.")
    if systems_verdict != "systems_materially_positive":
        unsupported_here.append("The same-endpoint systems story remains mixed and cannot be upgraded from the mechanism audit alone.")
    if mechanism_contract_verdict != "mechanism_contract_supported_with_partial_control_isolation":
        unsupported_here.append("The mechanism-contract audit is not clean enough to treat every claim layer as supported.")

    disconfirmed_here: list[str] = []
    if boundary_verdict == "first_boundary_failure_localized":
        disconfirmed_here.append(
            "The reopened R26/R27 packet disconfirms the narrower expectation that no localized failure existed inside the bounded post-H21 follow-up envelope."
        )
    if str(r28_gate["retrieval_bottleneck_verdict"]) == "pointer_like_exact_non_retrieval_dominant":
        disconfirmed_here.append(
            "R28 disconfirms the narrower expectation that retrieval_total still dominates pointer-like exact on the current D0 evidence stack."
        )

    return {
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
        "distilled_result": {
            "h22_active_runtime_lane": h22_summary["active_runtime_lane"],
            "h22_active_support_lane": h22_summary["active_support_lane"],
            "r26_lane_verdict": r26_gate["lane_verdict"],
            "r27_execution_mode": r27_gate["execution_mode"],
            "r27_lane_verdict": r27_gate["lane_verdict"],
            "h23_boundary_verdict": boundary_verdict,
            "r28_mechanism_contract_verdict": mechanism_contract_verdict,
            "h21_systems_verdict": systems_verdict,
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h21_summary = inputs["h21_summary"]["summary"]
    h22_summary = inputs["h22_summary"]["summary"]
    r26_gate = inputs["r26_summary"]["summary"]["gate"]
    r27_gate = inputs["r27_summary"]["summary"]["gate"]
    r28_gate = inputs["r28_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H21_refreeze_after_r22_r23/summary.json",
            "fields": {
                "boundary_verdict": h21_summary["boundary_verdict"],
                "systems_verdict": h21_summary["systems_verdict"],
                "next_priority_lane": h21_summary["next_priority_lane"],
            },
        },
        {
            "source": "results/H22_post_h21_boundary_reopen_and_dual_track_lock/summary.json",
            "fields": {
                "active_runtime_lane": h22_summary["active_runtime_lane"],
                "active_support_lane": h22_summary["active_support_lane"],
                "conditional_runtime_lane": h22_summary["conditional_runtime_lane"],
            },
        },
        {
            "source": "results/R26_d0_boundary_localization_execution_gate/summary.json",
            "fields": {
                "lane_verdict": r26_gate["lane_verdict"],
                "executed_candidate_count": r26_gate["executed_candidate_count"],
                "failure_candidate_count": r26_gate["failure_candidate_count"],
            },
        },
        {
            "source": "results/R27_d0_boundary_localization_extension_gate/summary.json",
            "fields": {
                "execution_mode": r27_gate["execution_mode"],
                "lane_verdict": r27_gate["lane_verdict"],
                "executed_candidate_count": r27_gate.get("executed_candidate_count"),
            },
        },
        {
            "source": "results/R28_d0_trace_retrieval_contract_audit/summary.json",
            "fields": {
                "mechanism_contract_verdict": r28_gate["mechanism_contract_verdict"],
                "retrieval_bottleneck_verdict": r28_gate["retrieval_bottleneck_verdict"],
                "r23_systems_verdict": r28_gate["r23_systems_verdict"],
            },
        },
    ]


def build_summary(
    checklist_rows: list[dict[str, object]],
    inputs: dict[str, Any],
    claim_packet: dict[str, object],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    h21_summary = inputs["h21_summary"]["summary"]
    r26_gate = inputs["r26_summary"]["summary"]["gate"]
    r27_gate = inputs["r27_summary"]["summary"]["gate"]
    r28_gate = inputs["r28_summary"]["summary"]["gate"]

    boundary_verdict = map_boundary_verdict(
        str(r26_gate["lane_verdict"]),
        str(r27_gate["lane_verdict"]),
    )
    mechanism_contract_verdict = str(r28_gate["mechanism_contract_verdict"])
    systems_verdict = str(h21_summary["systems_verdict"])

    unsatisfied_frontier_activation_conditions = []
    if boundary_verdict != "first_boundary_failure_localized":
        unsatisfied_frontier_activation_conditions.append("true_executor_boundary_localization")
    if mechanism_contract_verdict != "mechanism_contract_supported_with_partial_control_isolation":
        unsatisfied_frontier_activation_conditions.append("d0_mechanism_contract_audit_positive")
    if systems_verdict != "systems_materially_positive":
        unsatisfied_frontier_activation_conditions.append("current_scope_systems_story_materially_positive")
    unsatisfied_frontier_activation_conditions.append("scope_lift_thesis_explicitly_reauthorized")

    return {
        "current_paper_phase": "h23_refreeze_after_r26_r27_r28_complete",
        "active_stage": "h23_refreeze_after_r26_r27_r28",
        "prior_frozen_stage": "h21_refreeze_after_r22_r23",
        "reopen_stage": "h22_post_h21_boundary_reopen_and_dual_track_lock",
        "decision_state": "post_r26_r27_r28_refreeze_complete",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "boundary_verdict": boundary_verdict,
        "mechanism_contract_verdict": mechanism_contract_verdict,
        "systems_verdict": systems_verdict,
        "future_frontier_review_state": "planning_only_conditionally_reviewable",
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "unsatisfied_frontier_activation_conditions": unsatisfied_frontier_activation_conditions,
        "next_priority_lane": "p14_public_surface_sync_after_h23",
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Advance to P14 to sync README, STATUS, and publication ledgers downstream of the landed H23 packet without widening any scientific claims."
        ),
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
        {"experiment": "h23_refreeze_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h23_refreeze_snapshot", "environment": environment.as_dict(), "rows": snapshot_rows},
    )
    write_json(
        OUT_DIR / "claim_packet.json",
        {"experiment": "h23_refreeze_claim_packet", "environment": environment.as_dict(), "summary": claim_packet},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h23_refreeze_after_r26_r27_r28",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H23_refreeze_after_r26_r27_r28/README.md",
                "docs/milestones/H23_refreeze_after_r26_r27_r28/status.md",
                "docs/milestones/H23_refreeze_after_r26_r27_r28/todo.md",
                "docs/milestones/H23_refreeze_after_r26_r27_r28/acceptance.md",
                "docs/milestones/H23_refreeze_after_r26_r27_r28/artifact_index.md",
                "docs/milestones/H23_refreeze_after_r26_r27_r28/result_digest.md",
                "results/H21_refreeze_after_r22_r23/summary.json",
                "results/H22_post_h21_boundary_reopen_and_dual_track_lock/summary.json",
                "results/R26_d0_boundary_localization_execution_gate/summary.json",
                "results/R27_d0_boundary_localization_extension_gate/summary.json",
                "results/R28_d0_trace_retrieval_contract_audit/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H23 Refreeze After R26 R27 R28\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n"
        "- `claim_packet.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
