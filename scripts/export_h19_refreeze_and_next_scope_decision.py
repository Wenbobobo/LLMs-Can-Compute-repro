"""Export the H19 post-H18 refreeze and next-scope decision summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H19_refreeze_and_next_scope_decision"


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


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def load_inputs() -> dict[str, Any]:
    paths = {
        "h19_readme_text": ROOT / "docs" / "milestones" / "H19_refreeze_and_next_scope_decision" / "README.md",
        "h19_status_text": ROOT / "docs" / "milestones" / "H19_refreeze_and_next_scope_decision" / "status.md",
        "h19_todo_text": ROOT / "docs" / "milestones" / "H19_refreeze_and_next_scope_decision" / "todo.md",
        "h19_acceptance_text": ROOT / "docs" / "milestones" / "H19_refreeze_and_next_scope_decision" / "acceptance.md",
        "h19_artifact_index_text": ROOT / "docs" / "milestones" / "H19_refreeze_and_next_scope_decision" / "artifact_index.md",
        "h17_summary_text": ROOT / "results" / "H17_refreeze_and_conditional_frontier_recheck" / "summary.json",
        "h18_summary_text": ROOT / "results" / "H18_post_h17_mainline_reopen_guard" / "summary.json",
        "r19_summary_text": ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate" / "summary.json",
        "r20_summary_text": ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "summary.json",
        "r21_summary_text": ROOT / "results" / "R21_d0_exact_executor_boundary_break_map" / "summary.json",
        "m7_decision_text": ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json",
        "worktree_summary_text": ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json",
    }
    inputs: dict[str, Any] = {key: read_text(path) for key, path in paths.items()}
    for key, path in paths.items():
        if key.endswith("_text") and path.suffix == ".json":
            inputs[key.removesuffix("_text")] = read_json(path)
    return inputs


def build_checklist_rows(
    *,
    h19_readme_text: str,
    h19_status_text: str,
    h19_todo_text: str,
    h19_acceptance_text: str,
    h19_artifact_index_text: str,
    h17_summary_text: str,
    h17_summary: dict[str, Any],
    h18_summary_text: str,
    h18_summary: dict[str, Any],
    r19_summary_text: str,
    r19_summary: dict[str, Any],
    r20_summary_text: str,
    r20_summary: dict[str, Any],
    r21_summary_text: str,
    r21_summary: dict[str, Any],
    m7_decision_text: str,
    m7_decision: dict[str, Any],
    worktree_summary_text: str,
    worktree_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h17 = h17_summary["summary"]
    h18 = h18_summary["summary"]
    r19 = r19_summary["summary"]
    r20 = r20_summary["summary"]
    r21 = r21_summary["summary"]
    r19_gate = r19["gate"]
    r20_gate = r20["gate"]
    r21_gate = r21["gate"]

    return [
        {
            "item_id": "h19_milestone_docs_describe_a_machine_readable_post_h18_refreeze",
            "status": "pass"
            if contains_all(
                h19_readme_text,
                [
                    "landed closeout stage",
                    "post-`h18` same-endpoint state",
                    "machine-readable packet",
                ],
            )
            and contains_all(
                h19_status_text,
                [
                    "machine-readable `h19` refreeze",
                    "`r19/r20/r21` packet",
                    "`p13`",
                ],
            )
            and contains_all(
                h19_todo_text,
                [
                    "machine-readable `h19` summary",
                    "`supported_here`",
                    "`unsupported_here`",
                    "`disconfirmed_here`",
                ],
            )
            and contains_all(
                h19_acceptance_text,
                [
                    "one explicit post-`h18` frozen state exists",
                    "same-scope evidence is summarized without headline inflation",
                    "machine-readable",
                ],
            )
            and contains_all(
                h19_artifact_index_text,
                [
                    "scripts/export_h19_refreeze_and_next_scope_decision.py",
                    "results/h19_refreeze_and_next_scope_decision/summary.json",
                    "results/h19_refreeze_and_next_scope_decision/claim_packet.json",
                ],
            )
            else "blocked",
            "notes": "H19 should land first as an exporter-backed refreeze packet before a later P13 root/public sync rebases the outward docs.",
        },
        {
            "item_id": "h17_and_h18_are_preserved_as_the_input_control_packet",
            "status": "pass"
            if h17["decision_state"] == "same_scope_refreeze_complete"
            and h17["frontier_recheck_decision"] == "conditional_plan_required"
            and h18["stage_guard_state"] == "planned_same_scope_reopen_ready"
            and h18["current_frozen_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
            and h18["next_priority_lane"] == "h19_refreeze_and_next_scope_decision"
            and contains_all(
                h18_summary_text,
                [
                    "\"lane_order\": \"h18_then_r19_then_r20_then_r21_then_h19_then_p13\"",
                    "\"next_priority_lane\": \"h19_refreeze_and_next_scope_decision\"",
                ],
            )
            else "blocked",
            "notes": "H19 must freeze the landed H18 runtime wave without pretending that H17 never existed.",
        },
        {
            "item_id": "r19_confirms_same_endpoint_generalization_inside_the_declared_envelope",
            "status": "pass"
            if r19_gate["lane_verdict"] == "same_endpoint_generalization_confirmed"
            and bool(r19_gate["admitted_reference_gate_passed"])
            and bool(r19_gate["heldout_reference_gate_passed"])
            and bool(r19_gate["admitted_regression_gate_passed"])
            and bool(r19_gate["heldout_generalization_gate_passed"])
            and int(r19_gate["admitted_pointer_like_exact_count"]) == int(r19_gate["admitted_case_count"]) == 8
            and int(r19_gate["heldout_pointer_like_exact_count"]) == int(r19_gate["heldout_case_count"]) == 16
            and contains_all(
                r19_summary_text,
                [
                    "\"lane_verdict\": \"same_endpoint_generalization_confirmed\"",
                    "\"admitted_pointer_like_exact_count\": 8",
                    "\"heldout_pointer_like_exact_count\": 16",
                ],
            )
            else "blocked",
            "notes": "R19 is the positive same-endpoint runtime generalization result inside the fixed admitted plus heldout envelope.",
        },
        {
            "item_id": "r20_supports_the_mechanism_and_disconfirms_the_bounded_controls",
            "status": "pass"
            if r20_gate["lane_verdict"] == "mechanism_supported"
            and bool(r20_gate["pointer_like_exact_gate_passed"])
            and int(r20_gate["pointer_like_exact_case_count"]) == int(r20_gate["total_case_count"]) == 16
            and set(r20_gate["negative_controls_with_claim_relevant_failure"])
            == {"pointer_like_shuffled", "address_oblivious_control"}
            and contains_all(
                r20_summary_text,
                [
                    "\"lane_verdict\": \"mechanism_supported\"",
                    "\"pointer_like_exact_case_count\": 16",
                    "\"negative_controls_with_claim_relevant_failure\": [",
                ],
            )
            else "blocked",
            "notes": "R20 should carry both the positive target-mechanism result and the bounded negative-control failures into H19.",
        },
        {
            "item_id": "r21_stays_exact_across_the_bounded_grid_without_a_detected_break",
            "status": "pass"
            if r21_gate["lane_verdict"] == "no_boundary_break_detected"
            and int(r21_gate["planned_branch_count"]) == 48
            and int(r21_gate["planned_candidate_count"]) == 96
            and int(r21_gate["executed_candidate_count"]) == 96
            and int(r21_gate["exact_candidate_count"]) == 96
            and int(r21_gate["failure_candidate_count"]) == 0
            and int(r21_gate["failure_branch_count"]) == 0
            and contains_all(
                r21_summary_text,
                [
                    "\"lane_verdict\": \"no_boundary_break_detected\"",
                    "\"planned_branch_count\": 48",
                    "\"failure_candidate_count\": 0",
                ],
            )
            else "blocked",
            "notes": "R21 is still bounded and should be frozen as a no-break-observed result, not as proof that no boundary exists anywhere.",
        },
        {
            "item_id": "no_widening_controls_remain_explicit_after_the_refreeze",
            "status": "pass"
            if m7_decision["summary"]["frontend_widening_authorized"] is False
            and m7_decision["summary"]["public_demo_authorized"] is False
            and h17["frontier_recheck_decision"] == "conditional_plan_required"
            and h18["scope_lock_state"] == "tiny_typed_bytecode_d0_locked"
            and contains_all(
                m7_decision_text,
                [
                    "\"frontend_widening_authorized\": false",
                    "\"public_demo_authorized\": false",
                ],
            )
            else "blocked",
            "notes": "H19 may strengthen the same-endpoint packet, but it must not silently activate wider frontend or demo claims.",
        },
        {
            "item_id": "release_worktree_state_remains_explicit_for_downstream_syncs",
            "status": "pass"
            if release_commit_state_from_summary(worktree_summary)
            in {"dirty_worktree_release_commit_blocked", "clean_worktree_ready_if_other_gates_green"}
            and contains_all(
                worktree_summary_text,
                [
                    "\"release_commit_state\":",
                    "\"changed_path_count\":",
                    "\"untracked_path_count\":",
                ],
            )
            else "blocked",
            "notes": "H19 should keep the outward-sync cleanliness constraint explicit instead of pretending that P13 is already safe to commit.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H17_refreeze_and_conditional_frontier_recheck/summary.json",
            "fields": {
                "decision_state": inputs["h17_summary"]["summary"]["decision_state"],
                "frontier_recheck_decision": inputs["h17_summary"]["summary"]["frontier_recheck_decision"],
                "next_stage": inputs["h17_summary"]["summary"]["next_stage"],
            },
        },
        {
            "source": "results/H18_post_h17_mainline_reopen_guard/summary.json",
            "fields": {
                "stage_guard_state": inputs["h18_summary"]["summary"]["stage_guard_state"],
                "scope_lock_state": inputs["h18_summary"]["summary"]["scope_lock_state"],
                "lane_order": inputs["h18_summary"]["summary"]["lane_order"],
            },
        },
        {
            "source": "results/R19_d0_pointer_like_surface_generalization_gate/summary.json",
            "fields": {
                "lane_verdict": inputs["r19_summary"]["summary"]["gate"]["lane_verdict"],
                "admitted_pointer_like_exact_count": inputs["r19_summary"]["summary"]["gate"][
                    "admitted_pointer_like_exact_count"
                ],
                "heldout_pointer_like_exact_count": inputs["r19_summary"]["summary"]["gate"][
                    "heldout_pointer_like_exact_count"
                ],
            },
        },
        {
            "source": "results/R20_d0_runtime_mechanism_ablation_matrix/summary.json",
            "fields": {
                "lane_verdict": inputs["r20_summary"]["summary"]["gate"]["lane_verdict"],
                "pointer_like_exact_case_count": inputs["r20_summary"]["summary"]["gate"][
                    "pointer_like_exact_case_count"
                ],
                "negative_controls_with_claim_relevant_failure": inputs["r20_summary"]["summary"]["gate"][
                    "negative_controls_with_claim_relevant_failure"
                ],
            },
        },
        {
            "source": "results/R21_d0_exact_executor_boundary_break_map/summary.json",
            "fields": {
                "lane_verdict": inputs["r21_summary"]["summary"]["gate"]["lane_verdict"],
                "executed_candidate_count": inputs["r21_summary"]["summary"]["gate"]["executed_candidate_count"],
                "failure_candidate_count": inputs["r21_summary"]["summary"]["gate"]["failure_candidate_count"],
            },
        },
    ]


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    r19_gate = inputs["r19_summary"]["summary"]["gate"]
    r20_gate = inputs["r20_summary"]["summary"]["gate"]
    r21_gate = inputs["r21_summary"]["summary"]["gate"]

    supported_here = [
        "The reopened H18 wave stayed on the fixed tiny typed-bytecode D0 endpoint and preserved the H17 no-widening control state.",
        "R19 supports same-endpoint runtime generalization inside the declared admitted-plus-heldout envelope: pointer-like exact matched all admitted 8/8 rows and all heldout 16/16 rows.",
        "R20 supports mechanism relevance on the fixed 16-row probe set: pointer-like exact stayed exact on 16/16 rows while both bounded negative controls failed claim-relevantly.",
        "R21 supports a stronger bounded executor packet than before: all 96/96 executed candidates across the planned 48-branch grid stayed exact.",
    ]
    unsupported_here = [
        "No H19 claim widens beyond the current tiny typed-bytecode D0 endpoint.",
        "H19 still does not authorize arbitrary compiled-language claims, a general softmax-replacement claim, or a broader 'LLMs are computers' headline.",
        "The bounded R21 scan does not identify the true failure boundary of the current executor; it only shows that the present grid did not expose one.",
        "The repo still does not have a positive end-to-end systems-superiority result on the current positive D0 suites.",
    ]
    disconfirmed_here = [
        "R20 disconfirms the bounded hypothesis that shuffled pointer-like retrieval can preserve the current speed-and-exactness packet on the fixed 16-row probe set.",
        "R20 disconfirms the bounded hypothesis that an address-oblivious control can preserve the current speed-and-exactness packet on that same 16-row probe set.",
        "R21 disconfirms the narrower expectation that the current planned 48-branch boundary scan had already exposed an exactness failure inside its executed grid.",
    ]
    return {
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
        "distilled_result": {
            "r19_admitted_pointer_like_exact_count": int(r19_gate["admitted_pointer_like_exact_count"]),
            "r19_heldout_pointer_like_exact_count": int(r19_gate["heldout_pointer_like_exact_count"]),
            "r20_pointer_like_exact_case_count": int(r20_gate["pointer_like_exact_case_count"]),
            "r20_negative_controls_with_claim_relevant_failure": list(
                r20_gate["negative_controls_with_claim_relevant_failure"]
            ),
            "r21_executed_candidate_count": int(r21_gate["executed_candidate_count"]),
            "r21_failure_candidate_count": int(r21_gate["failure_candidate_count"]),
            "r21_failure_branch_count": int(r21_gate["failure_branch_count"]),
        },
    }


def build_summary(
    checklist_rows: list[dict[str, object]],
    inputs: dict[str, Any],
    claim_packet: dict[str, object],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    r19_gate = inputs["r19_summary"]["summary"]["gate"]
    r20_gate = inputs["r20_summary"]["summary"]["gate"]
    r21_gate = inputs["r21_summary"]["summary"]["gate"]
    return {
        "current_paper_phase": "h19_refreeze_and_next_scope_decision_complete",
        "active_stage": "h19_refreeze_and_next_scope_decision",
        "prior_frozen_stage": "h17_refreeze_and_conditional_frontier_recheck",
        "guarded_reopen_stage": "h18_post_h17_mainline_reopen_and_scope_lock",
        "decision_state": "same_endpoint_refreeze_complete" if not blocked_items else "further_resolution_required",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "same_endpoint_evidence_state": "materially_extended_same_endpoint_packet" if not blocked_items else "blocked",
        "runtime_generalization_verdict": str(r19_gate["lane_verdict"]),
        "mechanism_verdict": str(r20_gate["lane_verdict"]),
        "boundary_verdict": str(r21_gate["lane_verdict"]),
        "frontier_recheck_decision": "conditional_plan_required",
        "future_frontier_review_state": "planning_only_conditionally_reviewable",
        "future_frontier_lane": "f2_future_frontier_recheck_activation_matrix",
        "next_priority_lane": "p13_public_surface_sync_and_repo_hygiene",
        "release_commit_state": release_commit_state_from_summary(inputs["worktree_summary"]),
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "treat H19 as the machine-readable frozen post-H18 state, keep any broader root/publication rebasing downstream to P13, keep F2 planning-only, and do not widen runtime scope or frontend wording without a later explicit plan"
            if not blocked_items
            else "resolve the blocked H19 inputs before treating this packet as the canonical post-H18 frozen state"
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
    snapshot = build_snapshot(inputs)
    claim_packet = build_claim_packet(inputs)
    summary = build_summary(checklist_rows, inputs, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h19_refreeze_and_next_scope_decision_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h19_refreeze_and_next_scope_decision_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "claim_packet.json",
        {
            "experiment": "h19_refreeze_and_next_scope_decision_claim_packet",
            "environment": environment.as_dict(),
            "summary": claim_packet,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h19_refreeze_and_next_scope_decision",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H19_refreeze_and_next_scope_decision/README.md",
                "docs/milestones/H19_refreeze_and_next_scope_decision/status.md",
                "docs/milestones/H19_refreeze_and_next_scope_decision/todo.md",
                "docs/milestones/H19_refreeze_and_next_scope_decision/acceptance.md",
                "docs/milestones/H19_refreeze_and_next_scope_decision/artifact_index.md",
                "results/H17_refreeze_and_conditional_frontier_recheck/summary.json",
                "results/H18_post_h17_mainline_reopen_guard/summary.json",
                "results/R19_d0_pointer_like_surface_generalization_gate/summary.json",
                "results/R20_d0_runtime_mechanism_ablation_matrix/summary.json",
                "results/R21_d0_exact_executor_boundary_break_map/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H19 Refreeze And Next Scope Decision\n\n"
        "Machine-readable post-H18 refreeze packet for the landed R19/R20/R21 same-endpoint wave.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n"
        "- `claim_packet.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
