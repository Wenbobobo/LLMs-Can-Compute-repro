"""Export the post-H27 Origin-core reanchor packet for H28."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H28_post_h27_origin_core_reanchor_packet"


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
        "h28_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H28_post_h27_origin_core_reanchor_packet" / "README.md"
        ),
        "h28_status_text": read_text(
            ROOT / "docs" / "milestones" / "H28_post_h27_origin_core_reanchor_packet" / "status.md"
        ),
        "h28_todo_text": read_text(ROOT / "docs" / "milestones" / "H28_post_h27_origin_core_reanchor_packet" / "todo.md"),
        "h28_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H28_post_h27_origin_core_reanchor_packet" / "acceptance.md"
        ),
        "h28_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H28_post_h27_origin_core_reanchor_packet" / "artifact_index.md"
        ),
        "h27_summary": read_json(ROOT / "results" / "H27_refreeze_after_r32_r33_same_endpoint_decision" / "summary.json"),
        "claim_delta_text": read_text(
            ROOT / "docs" / "milestones" / "F4_post_h23_origin_claim_delta_matrix" / "claim_delta_matrix.md"
        ),
        "claim_ladder_text": read_text(ROOT / "docs" / "publication_record" / "claim_ladder.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h27_summary = inputs["h27_summary"]["summary"]
    return [
        {
            "item_id": "h28_docs_reanchor_to_origin_core_abc_claims",
            "status": "pass"
            if contains_all(
                inputs["h28_readme_text"],
                ["origin-core", "append-only", "2d", "small exact stack/vm executor"],
            )
            and contains_all(inputs["h28_status_text"], ["active planning", "r29", "f3", "f2"])
            and contains_all(
                inputs["h28_todo_text"],
                ["r34_origin_retrieval_primitive_contract_gate", "r35_origin_append_only_stack_vm_execution_gate"],
            )
            and contains_all(
                inputs["h28_acceptance_text"],
                ["post-`h27` reanchor packet", "r34 -> r35 -> h29", "r29", "f3"],
            )
            and contains_all(
                inputs["h28_artifact_index_text"],
                ["results/h28_post_h27_origin_core_reanchor_packet/summary.json", "claim_delta_matrix", "claim_ladder"],
            )
            else "blocked",
            "notes": "H28 should export one explicit Origin-core reanchor packet.",
        },
        {
            "item_id": "h27_negative_closeout_is_preserved_not_reopened",
            "status": "pass"
            if str(h27_summary["active_stage"]) == "h27_refreeze_after_r32_r33_same_endpoint_decision"
            and str(h27_summary["systems_verdict"]) == "systems_more_sharply_negative"
            and str(h27_summary["next_priority_lane"]) == "later_explicit_packet_required_before_new_runtime"
            else "blocked",
            "notes": "H28 should treat H27 as the negative closeout of the old wave.",
        },
        {
            "item_id": "origin_claim_docs_keep_headline_narrative_blocked",
            "status": "pass"
            if contains_all(
                inputs["claim_delta_text"],
                ["general llm has become a computer", "blocked_by_scope", "arbitrary `c`"],
            )
            and contains_all(inputs["claim_ladder_text"], ["d0 first compiled frontend boundary", "r29/f3", "blocked"])
            else "blocked",
            "notes": "H28 should inherit the existing origin-facing skepticism and blocked headline narrative.",
        },
    ]


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    return {
        "supported_here": [
            "H28 reanchors the active stage around the narrower Origin-core append-only / retrieval / small-VM thesis.",
            "H27 is preserved as the negative closeout of the old same-endpoint D0 recovery wave.",
            "The next required order is R34, then R35, then H29.",
        ],
        "unsupported_here": [
            "H28 does not reopen R29.",
            "H28 does not reopen F3 or bypass F2.",
            "H28 does not claim general LLM-computer, arbitrary-C, or million-step parity.",
        ],
        "disconfirmed_here": [
            "The old expectation that same-endpoint D0 recovery should remain the primary next-stage narrative after H27.",
        ],
        "distilled_result": {
            "active_stage": "h28_post_h27_origin_core_reanchor_packet",
            "scientific_target": "origin_core_append_only_retrieval_small_vm",
            "same_endpoint_recovery_state": "closed_negative_at_h27",
            "next_required_order": [
                "r34_origin_retrieval_primitive_contract_gate",
                "r35_origin_append_only_stack_vm_execution_gate",
                "h29_refreeze_after_r34_r35_origin_core_gate",
            ],
            "blocked_lanes_preserved": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h27_summary = inputs["h27_summary"]["summary"]
    return [
        {
            "source": "results/H27_refreeze_after_r32_r33_same_endpoint_decision/summary.json",
            "fields": {
                "systems_verdict": h27_summary["systems_verdict"],
                "next_priority_lane": h27_summary["next_priority_lane"],
            },
        },
        {
            "source": "docs/milestones/F4_post_h23_origin_claim_delta_matrix/claim_delta_matrix.md",
            "fields": {"headline_narrative_state": "blocked_scope_or_requires_new_substrate"},
        },
        {
            "source": "docs/publication_record/claim_ladder.md",
            "fields": {"d0_row_state": "historical_boundary_preserved_not_current_mainline"},
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h28_post_h27_origin_core_reanchor_active",
        "active_stage": "h28_post_h27_origin_core_reanchor_packet",
        "prior_closeout_stage": "h27_refreeze_after_r32_r33_same_endpoint_decision",
        "decision_state": "origin_core_pivot_active",
        "scientific_target": "origin_core_append_only_retrieval_small_vm",
        "same_endpoint_recovery_state": "closed_negative_at_h27",
        "next_required_order": [
            "r34_origin_retrieval_primitive_contract_gate",
            "r35_origin_append_only_stack_vm_execution_gate",
            "h29_refreeze_after_r34_r35_origin_core_gate",
        ],
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
