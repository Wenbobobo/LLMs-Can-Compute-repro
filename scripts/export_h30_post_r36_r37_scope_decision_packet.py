"""Export the post-R36/R37 scope-decision packet for H30."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H30_post_r36_r37_scope_decision_packet"


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
        "h30_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H30_post_r36_r37_scope_decision_packet" / "README.md"
        ),
        "h30_status_text": read_text(
            ROOT / "docs" / "milestones" / "H30_post_r36_r37_scope_decision_packet" / "status.md"
        ),
        "h30_todo_text": read_text(ROOT / "docs" / "milestones" / "H30_post_r36_r37_scope_decision_packet" / "todo.md"),
        "h30_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H30_post_r36_r37_scope_decision_packet" / "acceptance.md"
        ),
        "h30_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H30_post_r36_r37_scope_decision_packet" / "artifact_index.md"
        ),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h29_summary": read_json(ROOT / "results" / "H29_refreeze_after_r34_r35_origin_core_gate" / "summary.json"),
        "r36_summary": read_json(ROOT / "results" / "R36_origin_long_horizon_precision_scaling_gate" / "summary.json"),
        "r37_summary": read_json(ROOT / "results" / "R37_origin_compiler_boundary_gate" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h29_summary = inputs["h29_summary"]["summary"]
    r36_gate = inputs["r36_summary"]["summary"]["gate"]
    r37_gate = inputs["r37_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h30_docs_freeze_h29_r36_r37_and_preserve_scope_discipline",
            "status": "pass"
            if contains_all(
                inputs["h30_readme_text"],
                ["h29", "r36", "r37", "blocked", "later explicit packet"],
            )
            and contains_all(
                inputs["h30_status_text"],
                ["routing/refreeze packet", "tiny compiled boundary", "r29", "f3"],
            )
            and contains_all(
                inputs["h30_todo_text"],
                ["freeze", "r37", "blocked lanes", "later explicit packet"],
            )
            and contains_all(
                inputs["h30_acceptance_text"],
                ["machine-readable packet", "later scope lift", "blocked lanes remain blocked"],
            )
            and contains_all(
                inputs["h30_artifact_index_text"],
                [
                    "results/r37_origin_compiler_boundary_gate/summary.json",
                    "results/h30_post_r36_r37_scope_decision_packet/checklist.json",
                    "results/h30_post_r36_r37_scope_decision_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "H30 docs should freeze H29/R36/R37 into one explicit no-momentum decision packet.",
        },
        {
            "item_id": "upstream_origin_core_chain_and_tiny_boundary_remain_positive",
            "status": "pass"
            if str(h29_summary["origin_core_chain_state"]) == "positive_on_current_bundle"
            and str(r36_gate["lane_verdict"]) == "origin_precision_scaling_boundary_sharpened"
            and str(r37_gate["lane_verdict"]) == "origin_tiny_compiled_boundary_supported_narrowly"
            and bool(r37_gate["narrow_scope_kept"])
            else "blocked",
            "notes": "H30 only freezes positively if the H29/R36/R37 chain remains narrow and exact.",
        },
        {
            "item_id": "driver_and_active_wave_keep_h30_as_preserved_boundary_packet",
            "status": "pass"
            if contains_all(
                inputs["current_stage_driver_text"],
                ["h30_post_r36_r37_scope_decision_packet", "r29", "f3"],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                ["h30_post_r36_r37_scope_decision_packet", "later explicit packet"],
            )
            else "blocked",
            "notes": "Later packets may supersede H30 as active routing, but the canonical driver and active-wave handoff should still preserve H30 explicitly.",
        },
        {
            "item_id": "blocked_and_planning_only_lanes_remain_explicit",
            "status": "pass"
            if "r29_d0_same_endpoint_systems_recovery_execution_gate" in list(h29_summary["blocked_future_lanes"])
            and "f3_post_h23_scope_lift_decision_bundle" in list(h29_summary["blocked_future_lanes"])
            and str(h29_summary["future_frontier_review_state"]) == "planning_only_f2_preserved"
            else "blocked",
            "notes": "H30 should preserve R29/F3 as blocked and keep F2 planning-only.",
        },
    ]


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    r37_gate = inputs["r37_summary"]["summary"]["gate"]
    return {
        "supported_here": [
            "H30 freezes H29, R36, and R37 into the current Origin-core routing packet.",
            "R37 supports one tiny lowered/compiled bytecode subset on the active append-only / exact-retrieval / small-VM substrate.",
            f"R37 remains `{r37_gate['lane_verdict']}` with the admitted source subset staying narrow and exact.",
            "Any later compiled-boundary extension still requires a new explicit packet rather than momentum.",
        ],
        "unsupported_here": [
            "H30 does not reopen R29 same-endpoint systems recovery.",
            "H30 does not reopen F3 scope lift or relax F2 planning-only discipline.",
            "H30 does not relabel one tiny compiled boundary as arbitrary C, broad compiler support, or a general LLM-computer result.",
        ],
        "disconfirmed_here": [
            "The expectation that one positive tiny-boundary packet is enough to soften blocked lanes or headline scope limits.",
        ],
        "distilled_result": {
            "active_stage": "h30_post_r36_r37_scope_decision_packet",
            "decision_state": "origin_core_tiny_compiled_boundary_refrozen",
            "origin_core_chain_state": "positive_with_narrow_compiled_boundary",
            "compiled_boundary_state": "tiny_compiled_boundary_supported_narrowly",
            "frozen_upstream_gates": [
                "h29_refreeze_after_r34_r35_origin_core_gate",
                "r36_origin_long_horizon_precision_scaling_gate",
                "r37_origin_compiler_boundary_gate",
            ],
            "next_required_lane": "later_explicit_packet_required_before_any_compiler_boundary_extension",
            "blocked_lanes_preserved": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
            "future_frontier_review_state": "planning_only_f2_preserved",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h29 = inputs["h29_summary"]["summary"]
    r36_gate = inputs["r36_summary"]["summary"]["gate"]
    r37_gate = inputs["r37_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H29_refreeze_after_r34_r35_origin_core_gate/summary.json",
            "fields": {
                "active_stage": h29["active_stage"],
                "origin_core_chain_state": h29["origin_core_chain_state"],
                "next_required_lane": h29["next_required_lane"],
            },
        },
        {
            "source": "results/R36_origin_long_horizon_precision_scaling_gate/summary.json",
            "fields": {
                "lane_verdict": r36_gate["lane_verdict"],
                "inflated_single_head_failure_count": r36_gate["inflated_single_head_failure_count"],
                "decomposition_recovery_case_count": r36_gate["decomposition_recovery_case_count"],
            },
        },
        {
            "source": "results/R37_origin_compiler_boundary_gate/summary.json",
            "fields": {
                "lane_verdict": r37_gate["lane_verdict"],
                "admitted_source_case_count": r37_gate["admitted_source_case_count"],
                "free_running_exact_count": r37_gate["free_running_exact_count"],
                "narrow_scope_kept": r37_gate["narrow_scope_kept"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h30_post_r36_r37_scope_decision_packet_complete",
        "active_stage": "h30_post_r36_r37_scope_decision_packet",
        "prior_active_stage": "h29_refreeze_after_r34_r35_origin_core_gate",
        "decision_state": "origin_core_tiny_compiled_boundary_refrozen",
        "origin_core_chain_state": "positive_with_narrow_compiled_boundary",
        "compiled_boundary_state": "tiny_compiled_boundary_supported_narrowly",
        "next_required_lane": "later_explicit_packet_required_before_any_compiler_boundary_extension",
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
