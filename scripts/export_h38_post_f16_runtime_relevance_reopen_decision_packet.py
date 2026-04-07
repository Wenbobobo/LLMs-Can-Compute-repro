"""Export the post-F16 runtime-relevance reopen decision packet for H38."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H38_post_f16_runtime_relevance_reopen_decision_packet"


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
        "h38_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "README.md"
        ),
        "h38_status_text": read_text(
            ROOT / "docs" / "milestones" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "status.md"
        ),
        "h38_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "todo.md"
        ),
        "h38_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "acceptance.md"
        ),
        "h38_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-h37-f16-h38-p26-candidate-isolation-design.md"),
        "f16_status_text": read_text(
            ROOT / "docs" / "milestones" / "F16_post_h37_r41_candidate_isolation_bundle" / "status.md"
        ),
        "f16_candidate_status_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "F16_post_h37_r41_candidate_isolation_bundle" / "candidate_status_matrix.md"
        ),
        "f16_decision_basis_text": read_text(
            ROOT / "docs" / "milestones" / "F16_post_h37_r41_candidate_isolation_bundle" / "decision_basis.md"
        ),
        "f17_status_text": read_text(
            ROOT / "docs" / "milestones" / "F17_post_h38_same_substrate_exit_criteria_bundle" / "status.md"
        ),
        "h37_summary": read_json(ROOT / "results" / "H37_post_h36_runtime_relevance_decision_packet" / "summary.json"),
        "h36_summary": read_json(ROOT / "results" / "H36_post_r40_bounded_scalar_family_refreeze" / "summary.json"),
        "r40_summary": read_json(ROOT / "results" / "R40_origin_bounded_scalar_locals_and_flags_gate" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h37 = inputs["h37_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    r40_gate = inputs["r40_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h38_docs_select_keep_h36_freeze_after_f16_and_preserve_h37",
            "status": "pass"
            if contains_all(
                inputs["h38_readme_text"],
                [
                    "executed docs-only decision packet",
                    "`keep_h36_freeze`",
                    "`authorize_r41_origin_runtime_relevance_threat_stress_audit`",
                    "named future runtime candidate on the selected branch: none",
                    "did not produce one execution-ready contradiction",
                ],
            )
            and contains_all(
                inputs["h38_status_text"],
                [
                    "completed docs-only runtime-relevance reopen-decision packet",
                    "preserves `h36` as the active routing/refreeze packet",
                    "preserves `h37` as the prior docs-only runtime-relevance decision packet",
                    "selects `keep_h36_freeze` because `f16` produced `no_candidate_ready`",
                ],
            )
            and contains_all(
                inputs["h38_todo_text"],
                [
                    "`keep_h36_freeze` versus",
                    "`authorize_r41_origin_runtime_relevance_threat_stress_audit`",
                    "`f16` produced zero `execution_ready` candidates",
                    "keep `r41`, `r29`, `f3`, and `f2` non-active by default",
                ],
            )
            and contains_all(
                inputs["h38_acceptance_text"],
                [
                    "the packet remains docs-only",
                    "`h36` remains the active routing/refreeze packet underneath `h38`",
                    "`h37` remains visible as the preserved prior docs-only decision packet",
                    "no active downstream runtime lane exists after `h38`",
                ],
            )
            else "blocked",
            "notes": "H38 should remain docs-only, preserve H36/H37, and keep the freeze because F16 found no execution-ready candidate.",
        },
        {
            "item_id": "f16_candidate_isolation_records_zero_execution_ready_candidates",
            "status": "pass"
            if contains_all(
                inputs["f16_status_text"],
                [
                    "completed planning-only candidate-isolation bundle after `h37`",
                    "`nonunique` to",
                    "`helper_annotation_ablation_or_canonicalization`",
                    "`control_surface_neutralization_without_semantic_change`",
                    "`inadmissible` to",
                    "`retrieval_critical_vs_local_easy_step_contrast_slicing`",
                    "`no_candidate_ready`",
                ],
            )
            and contains_all(
                inputs["f16_candidate_status_matrix_text"],
                [
                    "`helper_annotation_ablation_or_canonicalization`",
                    "`control_surface_neutralization_without_semantic_change`",
                    "`retrieval_critical_vs_local_easy_step_contrast_slicing`",
                    "`nonunique`",
                    "`inadmissible`",
                    "`no_candidate_ready`",
                ],
            )
            and contains_all(
                inputs["f16_decision_basis_text"],
                [
                    "`execution_ready_candidate_count = 0`",
                    "`bundle_verdict = no_candidate_ready`",
                    "`h38` must select `keep_h36_freeze`",
                    "`r41` remains deferred",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "the current expected bundle verdict is `no_candidate_ready`",
                    "if `f16` produces zero `execution_ready` candidates",
                    "`h38` must keep the freeze",
                ],
            )
            else "blocked",
            "notes": "F16 must collapse the saved R41 catalog into explicit statuses and end with zero execution-ready candidates.",
        },
        {
            "item_id": "driver_wave_and_exit_bundle_keep_r41_deferred_under_h38",
            "status": "pass"
            if str(h37["selected_outcome"]) == "keep_h36_freeze"
            and str(h36["current_active_routing_stage"]) == "h36_post_r40_bounded_scalar_family_refreeze"
            and str(r40_gate["lane_verdict"]) == "origin_bounded_scalar_locals_and_flags_supported_narrowly"
            and contains_all(
                inputs["f17_status_text"],
                [
                    "completed planning-only same-substrate exit-criteria bundle after `h38`",
                    "route instead to `f9`, `f11`, or",
                    "does not authorize any runtime lane by itself",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h38_post_f16_runtime_relevance_reopen_decision_packet",
                    "selected_outcome = keep_h36_freeze",
                    "authorized_next_runtime_candidate = none",
                    "f16_post_h37_r41_candidate_isolation_bundle",
                    "f17_post_h38_same_substrate_exit_criteria_bundle",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h38_post_f16_runtime_relevance_reopen_decision_packet",
                    "f16_post_h37_r41_candidate_isolation_bundle",
                    "p26_post_h37_promotion_and_artifact_hygiene_audit",
                    "f17_post_h38_same_substrate_exit_criteria_bundle",
                    "no_active_downstream_runtime_lane",
                ],
            )
            and contains_all(
                inputs["h38_artifact_index_text"],
                [
                    "docs/milestones/f16_post_h37_r41_candidate_isolation_bundle/",
                    "docs/milestones/h37_post_h36_runtime_relevance_decision_packet/",
                    "docs/milestones/h36_post_r40_bounded_scalar_family_refreeze/",
                    "results/h38_post_f16_runtime_relevance_reopen_decision_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "The entry surfaces should treat H38 as current, keep R41 deferred, and preserve F17 only as planning-only route storage.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H38 lands the required post-F16 docs-only runtime-relevance reopen decision packet.",
            "F16 reduces the saved R41 catalog to explicit statuses and still produces zero execution-ready candidates.",
            "H36 remains the active routing/refreeze packet underneath H38, so no active downstream runtime lane exists after H38.",
            "F17 stores later route-selection rules without authorizing a new lane now.",
        ],
        "unsupported_here": [
            "H38 does not authorize R41 execution by wording alone.",
            "H38 does not reopen R29, F3, broader compiler scope, or hybrid work.",
        ],
        "disconfirmed_here": [
            "The expectation that any saved same-substrate candidate should reopen the runtime lane once it has been named in F14 or R41 planning docs.",
        ],
        "distilled_result": {
            "active_stage": "h38_post_f16_runtime_relevance_reopen_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "preserved_prior_docs_only_decision_packet": "h37_post_h36_runtime_relevance_decision_packet",
            "selected_outcome": "keep_h36_freeze",
            "non_selected_outcome": "authorize_r41_origin_runtime_relevance_threat_stress_audit",
            "authorized_next_runtime_candidate": "none",
            "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
            "decision_basis": "f16_no_candidate_ready_on_fixed_r40_row_pair",
            "candidate_status_counts": {
                "execution_ready": 0,
                "nonunique": 2,
                "inadmissible": 1,
            },
            "current_candidate_isolation_bundle": "f16_post_h37_r41_candidate_isolation_bundle",
            "current_same_substrate_exit_bundle": "f17_post_h38_same_substrate_exit_criteria_bundle",
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h37 = inputs["h37_summary"]["summary"]
    h36 = inputs["h36_summary"]["summary"]
    return [
        {
            "source": "results/H37_post_h36_runtime_relevance_decision_packet/summary.json",
            "fields": {
                "active_stage": h37["active_stage"],
                "selected_outcome": h37["selected_outcome"],
                "decision_basis": h37["decision_basis"],
            },
        },
        {
            "source": "docs/milestones/F16_post_h37_r41_candidate_isolation_bundle/candidate_status_matrix.md",
            "fields": {
                "bundle_verdict": "no_candidate_ready",
                "execution_ready_candidate_count": 0,
                "nonunique_candidate_count": 2,
                "inadmissible_candidate_count": 1,
            },
        },
        {
            "source": "results/H36_post_r40_bounded_scalar_family_refreeze/summary.json",
            "fields": {
                "active_stage": h36["active_stage"],
                "decision_state": h36["decision_state"],
                "next_required_lane": h36["next_required_lane"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h38_post_f16_runtime_relevance_reopen_decision_packet_complete",
        "active_stage": "h38_post_f16_runtime_relevance_reopen_decision_packet",
        "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_active_routing_packet": "h36_post_r40_bounded_scalar_family_refreeze",
        "preserved_prior_docs_only_decision_packet": "h37_post_h36_runtime_relevance_decision_packet",
        "current_candidate_isolation_bundle": "f16_post_h37_r41_candidate_isolation_bundle",
        "current_same_substrate_exit_bundle": "f17_post_h38_same_substrate_exit_criteria_bundle",
        "selected_outcome": "keep_h36_freeze",
        "non_selected_outcome": "authorize_r41_origin_runtime_relevance_threat_stress_audit",
        "authorized_next_runtime_candidate": "none",
        "deferred_future_runtime_candidate": "r41_origin_runtime_relevance_threat_stress_audit",
        "decision_basis": "f16_no_candidate_ready_on_fixed_r40_row_pair",
        "execution_ready_candidate_count": 0,
        "nonunique_candidate_count": 2,
        "inadmissible_candidate_count": 1,
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
