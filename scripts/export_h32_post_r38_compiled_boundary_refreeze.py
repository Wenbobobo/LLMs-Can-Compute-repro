"""Export the post-R38 compiled-boundary refreeze packet for H32."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H32_post_r38_compiled_boundary_refreeze"


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
        "h32_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H32_post_r38_compiled_boundary_refreeze" / "README.md"
        ),
        "h32_status_text": read_text(
            ROOT / "docs" / "milestones" / "H32_post_r38_compiled_boundary_refreeze" / "status.md"
        ),
        "h32_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H32_post_r38_compiled_boundary_refreeze" / "todo.md"
        ),
        "h32_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H32_post_r38_compiled_boundary_refreeze" / "acceptance.md"
        ),
        "h32_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H32_post_r38_compiled_boundary_refreeze" / "artifact_index.md"
        ),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h30_summary": read_json(ROOT / "results" / "H30_post_r36_r37_scope_decision_packet" / "summary.json"),
        "h31_summary": read_json(ROOT / "results" / "H31_post_h30_later_explicit_boundary_decision_packet" / "summary.json"),
        "r38_summary": read_json(ROOT / "results" / "R38_origin_compiler_control_surface_extension_gate" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h30 = inputs["h30_summary"]["summary"]
    h31 = inputs["h31_summary"]["summary"]
    r38_gate = inputs["r38_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h32_docs_freeze_h30_h31_r38_and_preserve_scope_discipline",
            "status": "pass"
            if contains_all(
                inputs["h32_readme_text"],
                ["h30", "h31", "r38", "narrow", "p18"],
            )
            and contains_all(
                inputs["h32_status_text"],
                ["current active routing/refreeze packet", "h30", "r29", "f3"],
            )
            and contains_all(
                inputs["h32_todo_text"],
                ["freeze", "h30", "h31", "r38", "new plan"],
            )
            and contains_all(
                inputs["h32_acceptance_text"],
                ["summary.json", "blocked", "new plan"],
            )
            and contains_all(
                inputs["h32_artifact_index_text"],
                [
                    "results/h31_post_h30_later_explicit_boundary_decision_packet/summary.json",
                    "results/r38_origin_compiler_control_surface_extension_gate/summary.json",
                    "results/h32_post_r38_compiled_boundary_refreeze/summary.json",
                ],
            )
            else "blocked",
            "notes": "H32 should freeze the post-H30 later-explicit packet and the one-row extension gate without widening scope.",
        },
        {
            "item_id": "upstream_h30_h31_r38_chain_remains_narrow_and_positive",
            "status": "pass"
            if str(h30["compiled_boundary_state"]) == "tiny_compiled_boundary_supported_narrowly"
            and str(h31["authorization_outcome"]) == "execute_one_more_tiny_extension"
            and str(r38_gate["lane_verdict"]) == "origin_compiler_control_surface_extension_supported_narrowly"
            and bool(r38_gate["narrow_scope_kept"])
            and int(r38_gate["admitted_free_running_exact_count"]) == 1
            else "blocked",
            "notes": "H32 is only positive if H30 stays narrow, H31 stays explicit, and R38 passes on the same substrate.",
        },
        {
            "item_id": "driver_and_active_wave_preserve_h32_as_upstream_refreeze_without_scope_lift",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                [
                    "h36_post_r40_bounded_scalar_family_refreeze",
                    "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
                    "h32_post_r38_compiled_boundary_refreeze",
                    "r38_origin_compiler_control_surface_extension_gate",
                    "r29",
                    "f3",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "h36_post_r40_bounded_scalar_family_refreeze",
                    "h32_post_r38_compiled_boundary_refreeze",
                    "r38_origin_compiler_control_surface_extension_gate",
                    "h35_post_p23_bounded_scalar_family_runtime_decision_packet",
                ],
            )
            else "blocked",
            "notes": "The canonical driver and short active-wave handoff should still preserve H32 as upstream refreeze context even though H36 is now active.",
        },
        {
            "item_id": "blocked_and_planning_only_lanes_remain_explicit",
            "status": "pass"
            if "r29_d0_same_endpoint_systems_recovery_execution_gate" in list(h31["blocked_future_lanes"])
            and "f3_post_h23_scope_lift_decision_bundle" in list(h31["blocked_future_lanes"])
            else "blocked",
            "notes": "H32 should not soften R29/F3 or create automatic further compiler widening.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H32 freezes `H30`, `H31`, and `R38` into the current Origin-core routing packet.",
            "One richer compiled control/call family stays exact on the current append-only / exact-retrieval / small-VM substrate.",
            "The longer same-family boundary probe is recorded explicitly without widening the supported claim set.",
            "Further compiler-boundary or scope lift work still requires a new plan.",
        ],
        "unsupported_here": [
            "H32 does not authorize arbitrary `C` or broad compiler support.",
            "H32 does not authorize same-endpoint systems recovery or a general LLM-computer claim.",
            "H32 does not turn one richer family into a broad demo or frontier result.",
        ],
        "disconfirmed_here": [
            "The expectation that one more exact compiled family should automatically dissolve current scope blockers.",
        ],
        "distilled_result": {
            "active_stage": "h32_post_r38_compiled_boundary_refreeze",
            "decision_state": "origin_core_one_richer_compiled_control_family_refrozen",
            "origin_core_chain_state": "positive_with_one_richer_compiled_control_family",
            "compiled_boundary_state": "one_richer_compiled_control_family_supported_narrowly",
            "authorization_packet": "h31_post_h30_later_explicit_boundary_decision_packet",
            "frozen_upstream_gates": [
                "h30_post_r36_r37_scope_decision_packet",
                "r38_origin_compiler_control_surface_extension_gate",
            ],
            "next_required_lane": "new_plan_required_before_any_further_compiled_boundary_or_scope_lift",
            "blocked_lanes_preserved": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
            "future_frontier_review_state": "planning_only_f2_preserved",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h30 = inputs["h30_summary"]["summary"]
    h31 = inputs["h31_summary"]["summary"]
    r38_gate = inputs["r38_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H30_post_r36_r37_scope_decision_packet/summary.json",
            "fields": {
                "active_stage": h30["active_stage"],
                "decision_state": h30["decision_state"],
                "compiled_boundary_state": h30["compiled_boundary_state"],
            },
        },
        {
            "source": "results/H31_post_h30_later_explicit_boundary_decision_packet/summary.json",
            "fields": {
                "active_stage": h31["active_stage"],
                "authorization_outcome": h31["authorization_outcome"],
                "admitted_extension_case": h31["admitted_extension_case"],
                "boundary_probe_case": h31["boundary_probe_case"],
            },
        },
        {
            "source": "results/R38_origin_compiler_control_surface_extension_gate/summary.json",
            "fields": {
                "lane_verdict": r38_gate["lane_verdict"],
                "admitted_case_count": r38_gate["admitted_case_count"],
                "boundary_stress_case_count": r38_gate["boundary_stress_case_count"],
                "admitted_free_running_exact_count": r38_gate["admitted_free_running_exact_count"],
                "boundary_free_running_exact_count": r38_gate["boundary_free_running_exact_count"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h32_post_r38_compiled_boundary_refreeze_complete",
        "active_stage": "h32_post_r38_compiled_boundary_refreeze",
        "prior_active_stage": "h30_post_r36_r37_scope_decision_packet",
        "decision_state": "origin_core_one_richer_compiled_control_family_refrozen",
        "origin_core_chain_state": "positive_with_one_richer_compiled_control_family",
        "compiled_boundary_state": "one_richer_compiled_control_family_supported_narrowly",
        "next_required_lane": "new_plan_required_before_any_further_compiled_boundary_or_scope_lift",
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
