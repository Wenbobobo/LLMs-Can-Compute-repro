"""Export the post-R34/R35 Origin-core refreeze packet for H29."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H29_refreeze_after_r34_r35_origin_core_gate"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    return {
        "h29_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H29_refreeze_after_r34_r35_origin_core_gate" / "README.md"
        ),
        "h29_status_text": read_text(
            ROOT / "docs" / "milestones" / "H29_refreeze_after_r34_r35_origin_core_gate" / "status.md"
        ),
        "h29_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H29_refreeze_after_r34_r35_origin_core_gate" / "todo.md"
        ),
        "h29_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H29_refreeze_after_r34_r35_origin_core_gate" / "acceptance.md"
        ),
        "h29_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H29_refreeze_after_r34_r35_origin_core_gate" / "artifact_index.md"
        ),
        "h28_summary": read_json(ROOT / "results" / "H28_post_h27_origin_core_reanchor_packet" / "summary.json"),
        "r34_summary": read_json(ROOT / "results" / "R34_origin_retrieval_primitive_contract_gate" / "summary.json"),
        "r35_summary": read_json(ROOT / "results" / "R35_origin_append_only_stack_vm_execution_gate" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h28 = inputs["h28_summary"]["summary"]
    r34_gate = inputs["r34_summary"]["summary"]["gate"]
    r35_gate = inputs["r35_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h29_docs_freeze_r34_r35_and_route_to_r36",
            "status": "pass"
            if contains_all(
                inputs["h29_readme_text"],
                ["r34", "r35", "r36", "blocked"],
            )
            and contains_all(
                inputs["h29_status_text"],
                ["origin-core a/b/c chain", "r36_origin_long_horizon_precision_scaling_gate", "r29", "f3"],
            )
            and contains_all(
                inputs["h29_todo_text"],
                ["preserve `r34` and `r35`", "r36_origin_long_horizon_precision_scaling_gate", "blocked"],
            )
            and contains_all(
                inputs["h29_acceptance_text"],
                ["freezes both `r34` and `r35`", "decides whether `r36` is justified next", "`r29`, `f3`, and `f2`"],
            )
            and contains_all(
                inputs["h29_artifact_index_text"],
                [
                    "results/r34_origin_retrieval_primitive_contract_gate/summary.json",
                    "results/r35_origin_append_only_stack_vm_execution_gate/summary.json",
                    "results/h29_refreeze_after_r34_r35_origin_core_gate/summary.json",
                ],
            )
            else "blocked",
            "notes": "H29 should freeze R34/R35 and route only to a narrow R36 next step.",
        },
        {
            "item_id": "h28_reanchor_state_is_preserved",
            "status": "pass"
            if str(h28["active_stage"]) == "h28_post_h27_origin_core_reanchor_packet"
            and str(h28["same_endpoint_recovery_state"]) == "closed_negative_at_h27"
            and str(h28["scientific_target"]) == "origin_core_append_only_retrieval_small_vm"
            else "blocked",
            "notes": "H29 must inherit and preserve the H28 Origin-core pivot state.",
        },
        {
            "item_id": "r34_and_r35_gates_remain_positive",
            "status": "pass"
            if str(r34_gate["lane_verdict"]) == "origin_retrieval_contract_supported"
            and bool(r34_gate["primitive_contract_supported"])
            and str(r35_gate["lane_verdict"]) == "origin_stack_vm_exact_supported"
            and bool(r35_gate["pointer_like_exact_all_cases"])
            else "blocked",
            "notes": "H29 should only freeze as positive if both upstream gates stayed exact.",
        },
        {
            "item_id": "blocked_lanes_preserved_without_scope_widening",
            "status": "pass"
            if "r29_d0_same_endpoint_systems_recovery_execution_gate" in list(h28["blocked_future_lanes"])
            and "f3_post_h23_scope_lift_decision_bundle" in list(h28["blocked_future_lanes"])
            and str(h28["future_frontier_review_state"]) == "planning_only_f2_preserved"
            else "blocked",
            "notes": "H29 should keep R29/F3 blocked and F2 planning-only discipline.",
        },
    ]


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    r34_gate = inputs["r34_summary"]["summary"]["gate"]
    r35_gate = inputs["r35_summary"]["summary"]["gate"]
    return {
        "supported_here": [
            "H29 freezes R34 and R35 as the current positive Origin-core A/B/C evidence chain.",
            f"R34 remains `{r34_gate['lane_verdict']}` with primitive contract support preserved.",
            f"R35 remains `{r35_gate['lane_verdict']}` with exact trace/final-state support preserved.",
            "A narrow precision boundary audit is justified next as R36.",
        ],
        "unsupported_here": [
            "H29 does not reopen R29 same-endpoint recovery by momentum.",
            "H29 does not reopen F3 scope lift or bypass F2 discipline.",
            "H29 does not escalate to broad compiler/demo claims.",
        ],
        "disconfirmed_here": [
            "The expectation that post-H28 progress should automatically reactivate blocked same-endpoint or headline-narrative lanes.",
        ],
        "distilled_result": {
            "active_stage": "h29_refreeze_after_r34_r35_origin_core_gate",
            "origin_core_chain_state": "positive_on_current_bundle",
            "frozen_upstream_gates": [
                "r34_origin_retrieval_primitive_contract_gate",
                "r35_origin_append_only_stack_vm_execution_gate",
            ],
            "next_required_lane": "r36_origin_long_horizon_precision_scaling_gate",
            "blocked_lanes_preserved": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
            "future_frontier_review_state": "planning_only_f2_preserved",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h28 = inputs["h28_summary"]["summary"]
    r34_gate = inputs["r34_summary"]["summary"]["gate"]
    r35_gate = inputs["r35_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H28_post_h27_origin_core_reanchor_packet/summary.json",
            "fields": {
                "active_stage": h28["active_stage"],
                "scientific_target": h28["scientific_target"],
                "same_endpoint_recovery_state": h28["same_endpoint_recovery_state"],
            },
        },
        {
            "source": "results/R34_origin_retrieval_primitive_contract_gate/summary.json",
            "fields": {
                "lane_verdict": r34_gate["lane_verdict"],
                "primitive_contract_supported": r34_gate["primitive_contract_supported"],
                "observation_count": r34_gate["observation_count"],
                "exact_observation_count": r34_gate["exact_observation_count"],
            },
        },
        {
            "source": "results/R35_origin_append_only_stack_vm_execution_gate/summary.json",
            "fields": {
                "lane_verdict": r35_gate["lane_verdict"],
                "pointer_like_exact_all_cases": r35_gate["pointer_like_exact_all_cases"],
                "executed_case_count": r35_gate["executed_case_count"],
                "pointer_like_exact_trace_match_count": r35_gate["pointer_like_exact_trace_match_count"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h29_refreeze_after_r34_r35_origin_core_gate_complete",
        "active_stage": "h29_refreeze_after_r34_r35_origin_core_gate",
        "prior_stage": "h28_post_h27_origin_core_reanchor_packet",
        "decision_state": "origin_core_chain_refrozen_after_r34_r35",
        "origin_core_chain_state": "positive_on_current_bundle",
        "next_required_lane": "r36_origin_long_horizon_precision_scaling_gate",
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
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet(inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
