"""Export the dual-mode model mainline gate for R45."""

from __future__ import annotations

import json
from pathlib import Path

from model import evaluate_r45_dual_mode
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R45_origin_dual_mode_model_mainline_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def length_bucket(program_steps: int) -> str:
    if program_steps <= 128:
        return "steps<=128"
    if program_steps <= 256:
        return "129<=steps<=256"
    return "steps>256"


def mode_row(mode) -> dict[str, object]:
    exact_family_count = sum(int(outcome.exact_trace_match and outcome.exact_final_state_match) for outcome in mode.evaluation.outcomes)
    payload = {
        "mode_id": mode.mode_id,
        "mode_role": mode.mode_role,
        "memory_strategy": mode.memory_strategy,
        "call_strategy": mode.call_strategy,
        "train_family_ids": list(mode.train_family_ids),
        "heldout_family_ids": list(mode.heldout_family_ids),
        "quadratic_scale": mode.scorer.quadratic_scale,
        "time_scale": mode.scorer.time_scale,
        "fit_train_sample_accuracy": None,
        "fit_train_exact_program_accuracy": None,
        "exact_trace_accuracy": mode.evaluation.exact_trace_accuracy,
        "exact_final_state_accuracy": mode.evaluation.exact_final_state_accuracy,
        "program_count": mode.evaluation.program_count,
        "exact_family_count": exact_family_count,
    }
    if mode.fit_result is not None:
        payload["fit_train_sample_accuracy"] = mode.fit_result.train_sample_accuracy
        payload["fit_train_exact_program_accuracy"] = mode.fit_result.train_exact_program_accuracy
    return payload


def family_rows(contract_programs, mode_evaluations) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for mode in mode_evaluations:
        for contract_program, outcome in zip(contract_programs, mode.evaluation.outcomes, strict=True):
            rows.append(
                {
                    "mode_id": mode.mode_id,
                    "family_id": contract_program.family_id,
                    "family_role": contract_program.family_role,
                    "comparison_mode": contract_program.comparison_mode,
                    "bytecode_program_name": contract_program.bytecode_program_name,
                    "trace_program_name": contract_program.trace_program.name,
                    "program_steps": contract_program.program_steps,
                    "length_bucket": length_bucket(contract_program.program_steps),
                    "exact_trace_match": outcome.exact_trace_match,
                    "exact_final_state_match": outcome.exact_final_state_match,
                    "first_mismatch_step": outcome.first_mismatch_step,
                    "failure_reason": outcome.failure_reason,
                    "verdict": "exact" if outcome.exact_trace_match and outcome.exact_final_state_match else "break",
                }
            )
    return rows


def assess_gate(mode_rows_payload: list[dict[str, object]], family_rows_payload: list[dict[str, object]]) -> dict[str, object]:
    exact_mode_count = sum(
        int(row["exact_trace_accuracy"] == 1.0 and row["exact_final_state_accuracy"] == 1.0) for row in mode_rows_payload
    )
    heldout_rows = [row for row in family_rows_payload if row["family_role"] != "core" and row["mode_id"] == "trainable_2d_executor"]
    heldout_exact = all(row["verdict"] == "exact" for row in heldout_rows)
    lane_verdict = (
        "coequal_model_lane_supported_without_replacing_exact"
        if exact_mode_count == len(mode_rows_payload)
        else "mixed_model_lane"
    )
    return {
        "lane_verdict": lane_verdict,
        "mode_count": len(mode_rows_payload),
        "exact_mode_count": exact_mode_count,
        "contract_family_count": len({row["family_id"] for row in family_rows_payload}),
        "exact_family_mode_row_count": sum(int(row["verdict"] == "exact") for row in family_rows_payload),
        "family_mode_row_count": len(family_rows_payload),
        "trainable_heldout_family_exact": heldout_exact,
        "exact_r43_dependency_satisfied": True,
        "later_explicit_packet_required": True,
        "next_required_packet": "h42_post_r43_route_selection_packet",
        "conditional_useful_case_candidate": "r44_origin_restricted_wasm_useful_case_execution_gate",
    }


def first_failure(family_rows_payload: list[dict[str, object]]) -> dict[str, object] | None:
    for row in family_rows_payload:
        if row["verdict"] != "exact":
            return {
                "mode_id": row["mode_id"],
                "family_id": row["family_id"],
                "family_role": row["family_role"],
                "first_mismatch_step": row["first_mismatch_step"],
                "failure_reason": row["failure_reason"],
            }
    return None


def main() -> None:
    contract_programs, mode_evaluations = evaluate_r45_dual_mode()

    manifest_rows = [
        {
            "family_order": index + 1,
            "family_id": program.family_id,
            "family_role": program.family_role,
            "comparison_mode": program.comparison_mode,
            "bytecode_program_name": program.bytecode_program_name,
            "trace_program_name": program.trace_program.name,
            "program_steps": program.program_steps,
            "max_steps": program.max_steps,
        }
        for index, program in enumerate(contract_programs)
    ]
    mode_rows_payload = [mode_row(mode) for mode in mode_evaluations]
    family_rows_payload = family_rows(contract_programs, mode_evaluations)
    stop_failure = first_failure(family_rows_payload)
    stop_rule = {
        "mode_count": len(mode_rows_payload),
        "family_mode_row_count": len(family_rows_payload),
        "stop_rule_triggered": stop_failure is not None,
        "first_failure": stop_failure,
        "reason": "both admitted model modes stayed exact against the R43 contract surface"
        if stop_failure is None
        else "stopped at the first dual-mode model mismatch against the exact R43 contract surface",
    }
    gate = assess_gate(mode_rows_payload, family_rows_payload)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "execution_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "mode_rows.json", {"rows": mode_rows_payload})
    write_json(OUT_DIR / "family_rows.json", {"rows": family_rows_payload})
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "r45_origin_dual_mode_model_mainline_gate_complete",
                "active_runtime_lane": "r45_origin_dual_mode_model_mainline_gate",
                "activation_packet": "h41_post_r42_aggressive_long_arc_decision_packet",
                "current_exact_dependency": "r43_origin_bounded_memory_small_vm_execution_gate",
                "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
                "preserved_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
