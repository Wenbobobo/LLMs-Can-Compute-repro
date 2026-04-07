"""Export the post-H30 later-explicit boundary decision packet for H31."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H31_post_h30_later_explicit_boundary_decision_packet"


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
        "h31_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H31_post_h30_later_explicit_boundary_decision_packet" / "README.md"
        ),
        "h31_status_text": read_text(
            ROOT / "docs" / "milestones" / "H31_post_h30_later_explicit_boundary_decision_packet" / "status.md"
        ),
        "h31_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H31_post_h30_later_explicit_boundary_decision_packet" / "todo.md"
        ),
        "h31_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H31_post_h30_later_explicit_boundary_decision_packet" / "acceptance.md"
        ),
        "h31_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H31_post_h30_later_explicit_boundary_decision_packet" / "artifact_index.md"
        ),
        "plan_text": read_text(ROOT / "docs" / "plans" / "2026-03-22-post-h30-h31-r38-extension-plan.md"),
        "h30_summary": read_json(ROOT / "results" / "H30_post_r36_r37_scope_decision_packet" / "summary.json"),
        "r37_summary": read_json(ROOT / "results" / "R37_origin_compiler_boundary_gate" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h30_summary = inputs["h30_summary"]["summary"]
    r37_gate = inputs["r37_summary"]["summary"]["gate"]
    return [
        {
            "item_id": "h31_docs_lock_one_extension_and_one_boundary_probe",
            "status": "pass"
            if contains_all(
                inputs["h31_readme_text"],
                [
                    "execute_one_more_tiny_extension",
                    "subroutine_braid_program(6, base_address=80)",
                    "subroutine_braid_long_program(12, base_address=160)",
                ],
            )
            and contains_all(
                inputs["h31_status_text"],
                ["docs-only", "one richer control/call family", "r29", "f3"],
            )
            and contains_all(
                inputs["h31_todo_text"],
                ["subroutine_braid_program(6, base_address=80)", "subroutine_braid_long_program(12, base_address=160)", "r38"],
            )
            and contains_all(
                inputs["h31_acceptance_text"],
                ["execute_one_more_tiny_extension", "blocked", "arbitrary-language"],
            )
            and contains_all(
                inputs["h31_artifact_index_text"],
                [
                    "results/h31_post_h30_later_explicit_boundary_decision_packet/summary.json",
                    "results/h30_post_r36_r37_scope_decision_packet/summary.json",
                    "results/r37_origin_compiler_boundary_gate/summary.json",
                ],
            )
            else "blocked",
            "notes": "H31 should convert the post-H30 fork into one explicit tiny-extension decision with named admitted and boundary rows.",
        },
        {
            "item_id": "upstream_h30_r37_state_remains_narrow_and_positive",
            "status": "pass"
            if str(h30_summary["decision_state"]) == "origin_core_tiny_compiled_boundary_refrozen"
            and str(h30_summary["compiled_boundary_state"]) == "tiny_compiled_boundary_supported_narrowly"
            and "r29_d0_same_endpoint_systems_recovery_execution_gate" in list(h30_summary["blocked_future_lanes"])
            and "f3_post_h23_scope_lift_decision_bundle" in list(h30_summary["blocked_future_lanes"])
            and str(r37_gate["lane_verdict"]) == "origin_tiny_compiled_boundary_supported_narrowly"
            and bool(r37_gate["narrow_scope_kept"])
            else "blocked",
            "notes": "H31 is only justified if the H30/R37 state being extended is still narrow, positive, and blocked-lane disciplined.",
        },
        {
            "item_id": "saved_plan_preserves_same_substrate_and_no_widening_rules",
            "status": "pass"
            if contains_all(
                inputs["plan_text"],
                [
                    "h31_post_h30_later_explicit_boundary_decision_packet",
                    "r38_origin_compiler_control_surface_extension_gate",
                    "subroutine_braid_program(6, base_address=80)",
                    "subroutine_braid_long_program(12, base_address=160)",
                    "no new opcode",
                    "r29",
                    "f3",
                ],
            )
            else "blocked",
            "notes": "The saved plan should keep execution on the current substrate and reject broad compiler/demo widening.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H31 converts the post-H30 fork into one explicit later-explicit packet.",
            "The only admitted extension row is `subroutine_braid_program(6, base_address=80)`.",
            "The only named non-admission boundary row is `subroutine_braid_long_program(12, base_address=160)`.",
            "The packet preserves `R29` and `F3` as blocked while routing to `R38` only.",
        ],
        "unsupported_here": [
            "H31 does not authorize opcode-surface widening.",
            "H31 does not authorize hidden host-side execution or a new runtime substrate.",
            "H31 does not authorize arbitrary `C`, broad Wasm coverage, or same-endpoint systems recovery.",
        ],
        "disconfirmed_here": [
            "The expectation that `H30` alone should automatically widen compiler scope without a new explicit packet.",
        ],
        "distilled_result": {
            "active_stage": "h31_post_h30_later_explicit_boundary_decision_packet",
            "prior_active_stage": "h30_post_r36_r37_scope_decision_packet",
            "decision_state": "later_explicit_one_tiny_extension_authorized",
            "authorization_outcome": "execute_one_more_tiny_extension",
            "admitted_extension_case": "bytecode_subroutine_braid_6_a80",
            "boundary_probe_case": "bytecode_subroutine_braid_long_12_a160",
            "next_required_lane": "r38_origin_compiler_control_surface_extension_gate",
            "blocked_lanes_preserved": [
                "r29_d0_same_endpoint_systems_recovery_execution_gate",
                "f3_post_h23_scope_lift_decision_bundle",
            ],
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h30 = inputs["h30_summary"]["summary"]
    r37_gate = inputs["r37_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H30_post_r36_r37_scope_decision_packet/summary.json",
            "fields": {
                "active_stage": h30["active_stage"],
                "decision_state": h30["decision_state"],
                "compiled_boundary_state": h30["compiled_boundary_state"],
                "next_required_lane": h30["next_required_lane"],
            },
        },
        {
            "source": "results/R37_origin_compiler_boundary_gate/summary.json",
            "fields": {
                "lane_verdict": r37_gate["lane_verdict"],
                "admitted_source_case_count": r37_gate["admitted_source_case_count"],
                "free_running_exact_count": r37_gate["free_running_exact_count"],
                "opcode_surface": r37_gate["opcode_surface"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h31_post_h30_later_explicit_boundary_decision_packet_complete",
        "active_stage": "h31_post_h30_later_explicit_boundary_decision_packet",
        "prior_active_stage": "h30_post_r36_r37_scope_decision_packet",
        "decision_state": "later_explicit_one_tiny_extension_authorized",
        "authorization_outcome": "execute_one_more_tiny_extension",
        "admitted_extension_case": "bytecode_subroutine_braid_6_a80",
        "boundary_probe_case": "bytecode_subroutine_braid_long_12_a160",
        "next_required_lane": "r38_origin_compiler_control_surface_extension_gate",
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
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
