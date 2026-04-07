"""Export the dual-mode useful-case comparator gate for R48."""

from __future__ import annotations

import json
from pathlib import Path

from model import HELDOUT_KERNEL_ID, evaluate_r48_dual_mode_useful_case
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R48_origin_dual_mode_useful_case_model_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def failure_class(*, exact_trace_match: bool, exact_final_state_match: bool, failure_reason: str | None) -> str:
    if failure_reason is not None:
        return "runtime_exception"
    if exact_trace_match and exact_final_state_match:
        return "exact"
    if not exact_trace_match and not exact_final_state_match:
        return "trace_and_final_state_divergence"
    if not exact_trace_match:
        return "trace_divergence"
    return "final_state_divergence"


def mode_row(mode, contract_programs) -> dict[str, object]:
    exact_variant_count = sum(
        int(outcome.exact_trace_match and outcome.exact_final_state_match) for outcome in mode.evaluation.outcomes
    )
    heldout_rows = [
        (program, outcome)
        for program, outcome in zip(contract_programs, mode.evaluation.outcomes, strict=True)
        if program.family_role != "core"
    ]
    heldout_exact_variant_count = sum(
        int(outcome.exact_trace_match and outcome.exact_final_state_match) for _, outcome in heldout_rows
    )
    payload = {
        "mode_id": mode.mode_id,
        "mode_role": mode.mode_role,
        "memory_strategy": mode.memory_strategy,
        "call_strategy": mode.call_strategy,
        "train_kernel_ids": list(mode.train_kernel_ids),
        "heldout_kernel_ids": list(mode.heldout_kernel_ids),
        "quadratic_scale": mode.scorer.quadratic_scale,
        "time_scale": mode.scorer.time_scale,
        "fit_train_sample_accuracy": None,
        "fit_train_exact_program_accuracy": None,
        "exact_trace_accuracy": mode.evaluation.exact_trace_accuracy,
        "exact_final_state_accuracy": mode.evaluation.exact_final_state_accuracy,
        "program_count": mode.evaluation.program_count,
        "exact_variant_count": exact_variant_count,
        "heldout_exact_variant_count": heldout_exact_variant_count,
    }
    if mode.fit_result is not None:
        payload["fit_train_sample_accuracy"] = mode.fit_result.train_sample_accuracy
        payload["fit_train_exact_program_accuracy"] = mode.fit_result.train_exact_program_accuracy
    return payload


def variant_rows(contract_programs, mode_evaluations) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for mode in mode_evaluations:
        for contract_program, outcome in zip(contract_programs, mode.evaluation.outcomes, strict=True):
            row_failure_class = failure_class(
                exact_trace_match=outcome.exact_trace_match,
                exact_final_state_match=outcome.exact_final_state_match,
                failure_reason=outcome.failure_reason,
            )
            rows.append(
                {
                    "mode_id": mode.mode_id,
                    "kernel_id": contract_program.kernel_id,
                    "variant_id": contract_program.variant_id,
                    "family_role": contract_program.family_role,
                    "axis_tags": list(contract_program.axis_tags),
                    "comparison_mode": contract_program.comparison_mode,
                    "frontend_program_name": contract_program.frontend_program_name,
                    "bytecode_program_name": contract_program.bytecode_program_name,
                    "trace_program_name": contract_program.trace_program.name,
                    "program_steps": contract_program.program_steps,
                    "exact_trace_match": outcome.exact_trace_match,
                    "exact_final_state_match": outcome.exact_final_state_match,
                    "first_error_position": outcome.first_mismatch_step,
                    "failure_reason": outcome.failure_reason,
                    "failure_class": row_failure_class,
                    "verdict": "exact" if row_failure_class == "exact" else "break",
                }
            )
    return rows


def kernel_rows(mode_rows_payload: list[dict[str, object]], variant_rows_payload: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    kernels = sorted({row["kernel_id"] for row in variant_rows_payload})
    for mode_row_payload in mode_rows_payload:
        mode_id = mode_row_payload["mode_id"]
        for kernel_id in kernels:
            scoped_rows = [
                row for row in variant_rows_payload if row["mode_id"] == mode_id and row["kernel_id"] == kernel_id
            ]
            exact_variant_count = sum(int(row["verdict"] == "exact") for row in scoped_rows)
            rows.append(
                {
                    "mode_id": mode_id,
                    "kernel_id": kernel_id,
                    "family_role": scoped_rows[0]["family_role"],
                    "variant_count": len(scoped_rows),
                    "exact_variant_count": exact_variant_count,
                    "all_exact": exact_variant_count == len(scoped_rows),
                }
            )
    return rows


def assess_gate(mode_rows_payload: list[dict[str, object]], variant_rows_payload: list[dict[str, object]]) -> dict[str, object]:
    exact_mode_count = sum(
        int(row["exact_trace_accuracy"] == 1.0 and row["exact_final_state_accuracy"] == 1.0) for row in mode_rows_payload
    )
    compiled_row = next(row for row in mode_rows_payload if row["mode_id"] == "compiled_weight_executor")
    trainable_row = next(row for row in mode_rows_payload if row["mode_id"] == "trainable_2d_executor")
    compiled_exact = compiled_row["exact_trace_accuracy"] == 1.0 and compiled_row["exact_final_state_accuracy"] == 1.0
    trainable_exact = trainable_row["exact_trace_accuracy"] == 1.0 and trainable_row["exact_final_state_accuracy"] == 1.0
    if compiled_exact and trainable_exact:
        lane_verdict = "useful_case_model_lane_supported_without_replacing_exact"
    elif compiled_exact:
        lane_verdict = "compiled_mode_exact_trainable_mixed"
    else:
        lane_verdict = "useful_case_model_lane_break"
    heldout_rows = [
        row
        for row in variant_rows_payload
        if row["mode_id"] == "trainable_2d_executor" and row["kernel_id"] == HELDOUT_KERNEL_ID
    ]
    heldout_exact = all(row["verdict"] == "exact" for row in heldout_rows)
    return {
        "lane_verdict": lane_verdict,
        "route_posture": "comparator_only_useful_case_model_bridge",
        "mode_count": len(mode_rows_payload),
        "exact_mode_count": exact_mode_count,
        "contract_variant_count": len({row["variant_id"] for row in variant_rows_payload}),
        "contract_kernel_count": len({row["kernel_id"] for row in variant_rows_payload}),
        "variant_mode_row_count": len(variant_rows_payload),
        "exact_variant_mode_row_count": sum(int(row["verdict"] == "exact") for row in variant_rows_payload),
        "heldout_kernel_id": HELDOUT_KERNEL_ID,
        "heldout_variant_count": len({row["variant_id"] for row in heldout_rows}),
        "trainable_heldout_family_exact": heldout_exact,
        "claim_ceiling": "bounded_useful_cases_only",
        "exact_r47_dependency_satisfied": True,
        "later_explicit_packet_required": True,
        "next_required_packet": "h47_post_r48_useful_case_bridge_refreeze",
    }


def first_failure(variant_rows_payload: list[dict[str, object]]) -> dict[str, object] | None:
    for row in variant_rows_payload:
        if row["verdict"] != "exact":
            return {
                "mode_id": row["mode_id"],
                "kernel_id": row["kernel_id"],
                "variant_id": row["variant_id"],
                "family_role": row["family_role"],
                "first_error_position": row["first_error_position"],
                "failure_reason": row["failure_reason"],
                "failure_class": row["failure_class"],
            }
    return None


def main() -> None:
    contract_programs, mode_evaluations = evaluate_r48_dual_mode_useful_case()

    manifest_rows = [
        {
            "variant_order": index + 1,
            "kernel_id": program.kernel_id,
            "variant_id": program.variant_id,
            "family_role": program.family_role,
            "axis_tags": list(program.axis_tags),
            "comparison_mode": program.comparison_mode,
            "frontend_program_name": program.frontend_program_name,
            "bytecode_program_name": program.bytecode_program_name,
            "trace_program_name": program.trace_program.name,
            "program_steps": program.program_steps,
            "max_steps": program.max_steps,
        }
        for index, program in enumerate(contract_programs)
    ]
    mode_rows_payload = [mode_row(mode, contract_programs) for mode in mode_evaluations]
    variant_rows_payload = variant_rows(contract_programs, mode_evaluations)
    kernel_rows_payload = kernel_rows(mode_rows_payload, variant_rows_payload)
    stop_failure = first_failure(variant_rows_payload)
    stop_rule = {
        "mode_count": len(mode_rows_payload),
        "variant_mode_row_count": len(variant_rows_payload),
        "stop_rule_triggered": stop_failure is not None,
        "first_failure": stop_failure,
        "reason": "both admitted model modes stayed exact against the preserved R47 useful-case contract"
        if stop_failure is None
        else "stopped at the first dual-mode model mismatch against the preserved R47 useful-case contract",
    }
    gate = assess_gate(mode_rows_payload, variant_rows_payload)

    write_json(OUT_DIR / "execution_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "mode_rows.json", {"rows": mode_rows_payload})
    write_json(OUT_DIR / "variant_rows.json", {"rows": variant_rows_payload})
    write_json(OUT_DIR / "kernel_rows.json", {"rows": kernel_rows_payload})
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_active_docs_only_stage": "h46_post_r47_frontend_bridge_decision_packet",
                "active_runtime_lane": "r48_origin_dual_mode_useful_case_model_gate",
                "activation_packet": "h46_post_r47_frontend_bridge_decision_packet",
                "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
                "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
                "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
                "preserved_prior_post_h44_exact_gate": "r46_origin_useful_case_surface_generalization_gate",
                "current_completed_exact_frontend_bridge_gate": "r47_origin_restricted_frontend_translation_gate",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
