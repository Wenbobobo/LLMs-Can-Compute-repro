"""Export the post-R40 bounded-scalar refreeze packet for H36."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H36_post_r40_bounded_scalar_family_refreeze"


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
        "h36_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H36_post_r40_bounded_scalar_family_refreeze" / "README.md"
        ),
        "h36_status_text": read_text(
            ROOT / "docs" / "milestones" / "H36_post_r40_bounded_scalar_family_refreeze" / "status.md"
        ),
        "h36_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H36_post_r40_bounded_scalar_family_refreeze" / "todo.md"
        ),
        "h36_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H36_post_r40_bounded_scalar_family_refreeze" / "acceptance.md"
        ),
        "h36_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H36_post_r40_bounded_scalar_family_refreeze" / "artifact_index.md"
        ),
        "p24_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P24_post_h36_bounded_scalar_runtime_sync" / "README.md"
        ),
        "h35_summary": read_json(
            ROOT / "results" / "H35_post_p23_bounded_scalar_family_runtime_decision_packet" / "summary.json"
        ),
        "r40_summary": read_json(ROOT / "results" / "R40_origin_bounded_scalar_locals_and_flags_gate" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h35 = inputs["h35_summary"]["summary"]
    r40_gate = inputs["r40_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h36_docs_freeze_r40_narrowly_and_leave_no_active_runtime_lane",
            "status": "pass"
            if contains_all(
                inputs["h36_readme_text"],
                [
                    "current active routing/refreeze packet",
                    "explicit bounded frame locals",
                    "typed `flag` slots",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["h36_status_text"],
                [
                    "current active routing/refreeze packet after `h35` and `r40`",
                    "r41",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["h36_todo_text"],
                [
                    "freeze `h35` and `r40`",
                    "r41_origin_runtime_relevance_threat_stress_audit",
                    "p24_post_h36_bounded_scalar_runtime_sync",
                ],
            )
            and contains_all(
                inputs["h36_acceptance_text"],
                [
                    "results/h36_post_r40_bounded_scalar_family_refreeze/summary.json",
                    "no active downstream runtime lane exists after `h36`",
                ],
            )
            and contains_all(
                inputs["h36_artifact_index_text"],
                [
                    "results/h35_post_p23_bounded_scalar_family_runtime_decision_packet/summary.json",
                    "results/r40_origin_bounded_scalar_locals_and_flags_gate/summary.json",
                    "docs/milestones/p24_post_h36_bounded_scalar_runtime_sync/",
                ],
            )
            else "blocked",
            "notes": "H36 should refreeze the bounded-scalar result narrowly and return the stack to no active downstream runtime lane.",
        },
        {
            "item_id": "h35_and_r40_support_current_refreeze",
            "status": "pass"
            if str(h35["authorized_next_runtime_candidate"]) == "r40_origin_bounded_scalar_locals_and_flags_gate"
            and str(r40_gate["lane_verdict"]) == "origin_bounded_scalar_locals_and_flags_supported_narrowly"
            and bool(r40_gate["same_opcode_surface_kept"]) is True
            and int(r40_gate["admitted_free_running_exact_count"]) == 1
            and int(r40_gate["boundary_free_running_exact_count"]) == 1
            and int(r40_gate["negative_control_rejection_count"]) == 3
            else "blocked",
            "notes": "H36 is only justified if H35 named R40 explicitly and R40 stayed exact on both positive rows while rejecting the declared negatives.",
        },
        {
            "item_id": "driver_wave_and_p24_sync_to_h36_active_state",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h36_post_r40_bounded_scalar_family_refreeze",
                    "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h36_post_r40_bounded_scalar_family_refreeze",
                    "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
                    "r40_origin_bounded_scalar_locals_and_flags_gate",
                    "no active downstream runtime lane",
                ],
            )
            and contains_all(
                inputs["p24_readme_text"],
                [
                    "`h36` is now the current active routing/refreeze packet",
                    "`h35` is the preserved prior docs-only decision packet",
                    "`r41_origin_runtime_relevance_threat_stress_audit` remains deferred",
                ],
            )
            else "blocked",
            "notes": "P24 and the top-level handoff surfaces should move the repo onto the landed H36 state.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H36 freezes the R40 bounded-scalar result as narrow same-substrate evidence.",
            "Explicit bounded frame locals and typed flag slots are now supported narrowly on the current substrate and opcode surface.",
            "No active downstream runtime lane exists after H36 lands.",
        ],
        "unsupported_here": [
            "H36 does not authorize restricted-Wasm, aggregate values, hybrid/planner bridges, or arbitrary-language claims.",
            "H36 does not activate R41 automatically.",
        ],
        "disconfirmed_here": [
            "The expectation that explicit typed flag slots necessarily require a new opcode surface or a new substrate.",
        ],
        "distilled_result": {
            "active_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_control_packet": "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
            "decision_state": "bounded_scalar_family_refrozen_narrowly",
            "bounded_scalar_family_state": "explicit_bounded_scalar_locals_and_flags_supported_narrowly",
            "authorized_next_runtime_candidate": "none",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "reopen_precondition": "new_explicit_post_r40_packet_required",
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h36_post_r40_bounded_scalar_family_refreeze_complete",
        "active_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_control_packet": "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
        "decision_state": "bounded_scalar_family_refrozen_narrowly",
        "bounded_scalar_family_state": "explicit_bounded_scalar_locals_and_flags_supported_narrowly",
        "authorized_next_runtime_candidate": "none",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "reopen_precondition": "new_explicit_post_r40_packet_required",
        "next_required_lane": "no_active_downstream_runtime_lane",
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
    claim_packet = build_claim_packet()
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
