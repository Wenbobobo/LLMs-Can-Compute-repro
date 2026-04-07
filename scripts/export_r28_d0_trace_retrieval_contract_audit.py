"""Export the bounded D0 trace-retrieval contract audit for R28."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import median
from typing import Any, Iterable

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R28_d0_trace_retrieval_contract_audit"

CONTROL_PREDECESSOR_FAMILIES = {
    "checkpoint_replay_long",
    "helper_checkpoint_braid",
    "helper_checkpoint_braid_long",
    "subroutine_braid",
    "subroutine_braid_long",
}
CONTROL_SUITES = {"control_flow", "stress_reference"}


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def median_or_none(values: Iterable[float | None]) -> float | None:
    filtered = [float(value) for value in values if value is not None]
    return median(filtered) if filtered else None


def relative_path(path: str | Path) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def load_inputs() -> dict[str, Any]:
    return {
        "r19_summary": read_json(ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate" / "summary.json"),
        "r19_runtime_rows": read_json(ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate" / "runtime_rows.json"),
        "r20_summary": read_json(ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "summary.json"),
        "r20_runtime_rows": read_json(ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "runtime_matrix_rows.json"),
        "r20_mechanism_rows": read_json(ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "row_mechanism_summary.json"),
        "r23_summary": read_json(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "summary.json"),
        "r23_runtime_rows": read_json(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "runtime_profile_rows.json"),
    }


def build_primitive_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    r20_runtime_rows = inputs["r20_runtime_rows"]["rows"]
    r20_mechanism_rows = inputs["r20_mechanism_rows"]["rows"]
    r23_runtime_rows = inputs["r23_runtime_rows"]["rows"]

    pointer_exact_probe_rows = [row for row in r20_mechanism_rows if row["strategy_id"] == "pointer_like_exact"]
    shuffled_probe_rows = [row for row in r20_mechanism_rows if row["strategy_id"] == "pointer_like_shuffled"]
    address_oblivious_probe_rows = [
        row for row in r20_mechanism_rows if row["strategy_id"] == "address_oblivious_control"
    ]

    latest_write_rows = [row for row in pointer_exact_probe_rows if int(row["memory_probe_count"]) > 0]
    latest_write_verdict = (
        "supported"
        if latest_write_rows
        and median_or_none(row["memory_retrieval_correct_rate"] for row in latest_write_rows) == 1.0
        and median_or_none(row["memory_address_match_rate"] for row in latest_write_rows) == 1.0
        else "mixed"
    )
    stack_rows = [row for row in pointer_exact_probe_rows if int(row["stack_probe_count"]) > 0]
    stack_verdict = (
        "supported"
        if stack_rows
        and median_or_none(row["stack_retrieval_correct_rate"] for row in stack_rows) == 1.0
        and median_or_none(row["stack_address_match_rate"] for row in stack_rows) == 1.0
        else "mixed"
    )

    r20_control_runtime_rows = [
        row
        for row in r20_runtime_rows
        if row["strategy_id"] == "pointer_like_exact" and row["family"] in CONTROL_PREDECESSOR_FAMILIES
    ]
    r20_control_negative_rows = [
        row
        for row in r20_runtime_rows
        if row["strategy_id"] in {"pointer_like_shuffled", "address_oblivious_control"}
        and row["family"] in CONTROL_PREDECESSOR_FAMILIES
    ]
    r23_control_rows = [row for row in r23_runtime_rows if row["suite"] in CONTROL_SUITES]
    control_probe_rows = [
        row
        for row in pointer_exact_probe_rows
        if row["family"] in CONTROL_PREDECESSOR_FAMILIES
    ]
    control_shuffled_rows = [
        row for row in shuffled_probe_rows if row["family"] in CONTROL_PREDECESSOR_FAMILIES
    ]

    primitive_rows = [
        {
            "primitive_id": "latest_write_address",
            "verdict": latest_write_verdict,
            "direct_probe_available": True,
            "r20_probe_row_count": len(latest_write_rows),
            "pointer_like_median_retrieval_correct_rate": median_or_none(
                row["memory_retrieval_correct_rate"] for row in latest_write_rows
            ),
            "pointer_like_median_address_match_rate": median_or_none(
                row["memory_address_match_rate"] for row in latest_write_rows
            ),
            "shuffled_median_retrieval_correct_rate": median_or_none(
                row["memory_retrieval_correct_rate"]
                for row in shuffled_probe_rows
                if int(row["memory_probe_count"]) > 0
            ),
            "address_oblivious_median_address_match_rate": median_or_none(
                row["memory_address_match_rate"]
                for row in address_oblivious_probe_rows
                if int(row["memory_probe_count"]) > 0
            ),
            "note": "Memory latest-write retrieval stays exact under pointer-like lookup and degrades under address-oblivious controls.",
        },
        {
            "primitive_id": "stack_depth",
            "verdict": stack_verdict,
            "direct_probe_available": True,
            "r20_probe_row_count": len(stack_rows),
            "pointer_like_median_retrieval_correct_rate": median_or_none(
                row["stack_retrieval_correct_rate"] for row in stack_rows
            ),
            "pointer_like_median_address_match_rate": median_or_none(
                row["stack_address_match_rate"] for row in stack_rows
            ),
            "shuffled_median_retrieval_correct_rate": median_or_none(
                row["stack_retrieval_correct_rate"]
                for row in shuffled_probe_rows
                if int(row["stack_probe_count"]) > 0
            ),
            "address_oblivious_median_address_match_rate": median_or_none(
                row["stack_address_match_rate"]
                for row in address_oblivious_probe_rows
                if int(row["stack_probe_count"]) > 0
            ),
            "note": "Stack(depth) retrieval stays exact under pointer-like lookup and remains materially sensitive to shuffled controls.",
        },
        {
            "primitive_id": "control_predecessor_return_site",
            "verdict": "supported_but_not_directly_isolated"
            if r20_control_runtime_rows
            and all(bool(row["exact"]) for row in r20_control_runtime_rows)
            and all(bool(row["pointer_like_exact_exact"]) for row in r23_control_rows)
            else "mixed",
            "direct_probe_available": False,
            "r20_control_family_case_count": len(r20_control_runtime_rows),
            "r20_control_family_exact_count": sum(bool(row["exact"]) for row in r20_control_runtime_rows),
            "r20_control_negative_failure_count": sum(
                not bool(row["exact"]) for row in r20_control_negative_rows
            ),
            "r23_control_suite_case_count": len(r23_control_rows),
            "r23_control_suite_exact_count": sum(
                bool(row["pointer_like_exact_exact"]) for row in r23_control_rows
            ),
            "pointer_like_median_correct_step_gap": median_or_none(
                row["median_correct_step_gap"] for row in control_probe_rows
            ),
            "shuffled_median_step_gap_delta": median_or_none(
                row["median_step_gap_delta"] for row in control_shuffled_rows
            ),
            "note": "Control/return-site behavior is supported end-to-end on control-heavy families and suites, but the current audit lacks a dedicated primitive-only isolation probe.",
        },
    ]
    return primitive_rows


def build_claim_layer_rows(inputs: dict[str, Any], primitive_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    primitive_by_id = {str(row["primitive_id"]): row for row in primitive_rows}
    r19_gate = inputs["r19_summary"]["summary"]["gate"]
    r20_gate = inputs["r20_summary"]["summary"]["gate"]
    r23_gate = inputs["r23_summary"]["summary"]["gate"]
    return [
        {
            "layer_id": "A",
            "claim_id": "append_only_trace_substrate",
            "status": "supported"
            if r19_gate["lane_verdict"] == "same_endpoint_generalization_confirmed"
            else "mixed",
            "primary_evidence": (
                f"R19 pointer-like exact holds on {r19_gate['admitted_case_count'] + r19_gate['heldout_case_count']}/"
                f"{r19_gate['admitted_case_count'] + r19_gate['heldout_case_count']} admitted+heldout rows."
            ),
            "current_limit": "The substrate evidence remains bounded to the fixed D0 endpoint and does not widen the thesis.",
        },
        {
            "layer_id": "B",
            "claim_id": "low_dimensional_retrieval_contract",
            "status": "supported_with_partial_control_isolation"
            if r20_gate["lane_verdict"] == "mechanism_supported"
            and primitive_by_id["latest_write_address"]["verdict"] == "supported"
            and primitive_by_id["stack_depth"]["verdict"] == "supported"
            else "mixed",
            "primary_evidence": (
                "R20 negative controls fail claim-relevantly while latest-write and stack probes stay exact under pointer-like retrieval."
            ),
            "current_limit": (
                "Control predecessor / return-site retrieval is supported end-to-end but not yet isolated by a dedicated primitive-only probe."
            ),
        },
        {
            "layer_id": "C",
            "claim_id": "exact_executor_sufficiency_on_current_endpoint",
            "status": "supported_for_exactness_not_systems_threshold"
            if bool(r23_gate["exact_designated_paths_all_exact"])
            else "mixed",
            "primary_evidence": (
                f"R23 pointer-like exact stays exact on {r23_gate['pointer_like_exact_case_count']}/"
                f"{r23_gate['total_case_count']} current positive D0 rows."
            ),
            "current_limit": (
                f"R23 still ends at `{r23_gate['lane_verdict']}` with median ratio "
                f"{r23_gate['pointer_like_median_ratio_vs_best_reference']:.3f} vs best current reference."
            ),
        },
    ]


def render_claim_layer_map(layer_rows: list[dict[str, object]]) -> str:
    lines = [
        "# R28 Claim Layer Map",
        "",
        "| Layer | Claim | Status | Primary Evidence | Current Limit |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in layer_rows:
        lines.append(
            "| "
            f"{row['layer_id']} | {row['claim_id']} | {row['status']} | "
            f"{row['primary_evidence']} | {row['current_limit']} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_cost_breakdown_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    r20_rows = inputs["r20_runtime_rows"]["rows"]
    r23_rows = inputs["r23_runtime_rows"]["rows"]

    def summarize_r20(strategy_id: str) -> dict[str, object]:
        strategy_rows = [row for row in r20_rows if row["strategy_id"] == strategy_id]
        dominant_counter = {"retrieval_total": 0, "non_retrieval": 0}
        for row in strategy_rows:
            retrieval_seconds = row.get("retrieval_seconds")
            non_retrieval_seconds = row.get("non_retrieval_seconds")
            if retrieval_seconds is None or non_retrieval_seconds is None:
                continue
            dominant_counter[
                "retrieval_total" if retrieval_seconds >= non_retrieval_seconds else "non_retrieval"
            ] += 1
        dominant_component = None
        dominant_component_case_count = 0
        if any(dominant_counter.values()):
            dominant_component, dominant_component_case_count = max(
                dominant_counter.items(),
                key=lambda item: item[1],
            )
        return {
            "stage_id": "r20_mechanism_audit",
            "strategy_id": strategy_id,
            "row_count": len(strategy_rows),
            "exact_case_count": sum(bool(row["exact"]) for row in strategy_rows),
            "median_ns_per_step": median_or_none(row["ns_per_step"] for row in strategy_rows),
            "median_retrieval_share": median_or_none(row["retrieval_share"] for row in strategy_rows),
            "median_ns_per_read": median_or_none(row["ns_per_read"] for row in strategy_rows),
            "dominant_component": dominant_component,
            "dominant_component_case_count": dominant_component_case_count,
        }

    def summarize_r23(strategy_id: str) -> dict[str, object]:
        prefix = strategy_id
        retrieval_key = f"{prefix}_retrieval_share"
        ns_per_step_key = f"{prefix}_ns_per_step"
        ns_per_read_key = f"{prefix}_ns_per_read"
        exact_key = f"{prefix}_exact"
        dominant_key = f"{prefix}_dominant_component"
        strategy_rows = [row for row in r23_rows if row.get(exact_key) is not None]
        dominant_counter = {"retrieval_total": 0, "non_retrieval": 0}
        for row in strategy_rows:
            component = row.get(dominant_key)
            if component in dominant_counter:
                dominant_counter[str(component)] += 1
        dominant_component, dominant_component_case_count = max(
            dominant_counter.items(),
            key=lambda item: item[1],
        )
        return {
            "stage_id": "r23_systems_recheck",
            "strategy_id": strategy_id,
            "row_count": len(strategy_rows),
            "exact_case_count": sum(bool(row[exact_key]) for row in strategy_rows),
            "median_ns_per_step": median_or_none(row[ns_per_step_key] for row in strategy_rows),
            "median_retrieval_share": median_or_none(row[retrieval_key] for row in strategy_rows),
            "median_ns_per_read": median_or_none(row[ns_per_read_key] for row in strategy_rows),
            "dominant_component": dominant_component,
            "dominant_component_case_count": dominant_component_case_count,
        }

    return [
        summarize_r20("linear_exact"),
        summarize_r20("accelerated"),
        summarize_r20("pointer_like_exact"),
        summarize_r23("linear_exact"),
        summarize_r23("accelerated"),
        summarize_r23("pointer_like_exact"),
    ]


def build_stress_limit_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    r23_gate = inputs["r23_summary"]["summary"]["gate"]
    return [
        {
            "limit_id": "same_endpoint_systems_threshold_not_overturned",
            "status": "open",
            "evidence_anchor": "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json",
            "reason": (
                f"R23 still ends at `{r23_gate['lane_verdict']}` and does not overturn the bounded systems threshold."
            ),
            "required_future_evidence": "A new same-endpoint systems result, not a mechanism-only audit.",
        },
        {
            "limit_id": "control_predecessor_not_directly_isolated",
            "status": "open",
            "evidence_anchor": "results/R20_d0_runtime_mechanism_ablation_matrix/row_mechanism_summary.json",
            "reason": "Current control/return-site support is indirect and tied to end-to-end control-heavy families.",
            "required_future_evidence": "A dedicated primitive-only control predecessor / return-site probe.",
        },
        {
            "limit_id": "scope_remains_d0_only",
            "status": "open",
            "evidence_anchor": "results/R19_d0_pointer_like_surface_generalization_gate/summary.json",
            "reason": "The positive mechanism chain remains bounded to the fixed tiny typed-bytecode D0 endpoint.",
            "required_future_evidence": "An explicitly reauthorized wider endpoint, not implied extrapolation.",
        },
    ]


def assess_gate(
    inputs: dict[str, Any],
    *,
    primitive_rows: list[dict[str, object]],
    claim_layer_rows: list[dict[str, object]],
    cost_rows: list[dict[str, object]],
) -> dict[str, object]:
    primitive_by_id = {str(row["primitive_id"]): row for row in primitive_rows}
    claim_layer_by_id = {str(row["layer_id"]): row for row in claim_layer_rows}
    r23_gate = inputs["r23_summary"]["summary"]["gate"]
    pointer_like_r20 = next(
        row for row in cost_rows if row["stage_id"] == "r20_mechanism_audit" and row["strategy_id"] == "pointer_like_exact"
    )
    pointer_like_r23 = next(
        row for row in cost_rows if row["stage_id"] == "r23_systems_recheck" and row["strategy_id"] == "pointer_like_exact"
    )

    if (
        primitive_by_id["latest_write_address"]["verdict"] == "supported"
        and primitive_by_id["stack_depth"]["verdict"] == "supported"
        and claim_layer_by_id["C"]["status"] == "supported_for_exactness_not_systems_threshold"
    ):
        mechanism_contract_verdict = "mechanism_contract_supported_with_partial_control_isolation"
        reason = (
            "Latest-write and stack retrieval stay exact under pointer-like lookup, "
            "the negative controls fail claim-relevantly, and pointer-like exact still runs exactly on the current D0 suites. "
            "Control predecessor / return-site support is present, but not yet isolated by a dedicated primitive-only probe."
        )
    else:
        mechanism_contract_verdict = "mechanism_contract_mixed"
        reason = "The current evidence stack does not cleanly support every contract layer under the bounded D0 audit."

    retrieval_bottleneck_verdict = (
        "pointer_like_exact_non_retrieval_dominant"
        if pointer_like_r20["dominant_component"] == "non_retrieval"
        and pointer_like_r23["dominant_component"] == "non_retrieval"
        else "retrieval_total_still_dominant"
    )

    return {
        "mechanism_contract_verdict": mechanism_contract_verdict,
        "reason": reason,
        "claim_layer_a_status": claim_layer_by_id["A"]["status"],
        "claim_layer_b_status": claim_layer_by_id["B"]["status"],
        "claim_layer_c_status": claim_layer_by_id["C"]["status"],
        "latest_write_status": primitive_by_id["latest_write_address"]["verdict"],
        "stack_status": primitive_by_id["stack_depth"]["verdict"],
        "control_predecessor_status": primitive_by_id["control_predecessor_return_site"]["verdict"],
        "pointer_like_r20_median_retrieval_share": pointer_like_r20["median_retrieval_share"],
        "pointer_like_r23_median_retrieval_share": pointer_like_r23["median_retrieval_share"],
        "retrieval_bottleneck_verdict": retrieval_bottleneck_verdict,
        "r23_systems_verdict": r23_gate["lane_verdict"],
        "next_priority_lane": "h23_refreeze_after_r26_r27_r28",
    }


def build_summary(
    inputs: dict[str, Any],
    *,
    gate: dict[str, object],
    primitive_rows: list[dict[str, object]],
    claim_layer_rows: list[dict[str, object]],
    cost_rows: list[dict[str, object]],
    stress_limit_rows: list[dict[str, object]],
) -> dict[str, object]:
    r19_gate = inputs["r19_summary"]["summary"]["gate"]
    r20_gate = inputs["r20_summary"]["summary"]["gate"]
    r23_gate = inputs["r23_summary"]["summary"]["gate"]
    return {
        "status": "r28_trace_retrieval_contract_audit_complete",
        "current_frozen_stage": "h21_refreeze_after_r22_r23",
        "source_runtime_stages": [
            "r19_d0_pointer_like_surface_generalization_gate",
            "r20_d0_runtime_mechanism_ablation_matrix",
            "r23_d0_same_endpoint_systems_overturn_gate",
        ],
        "gate": gate,
        "claim_layers": claim_layer_rows,
        "primitive_rows": primitive_rows,
        "cost_row_count": len(cost_rows),
        "stress_limit_count": len(stress_limit_rows),
        "recommended_next_action": "Refreeze the bounded R26/R27/R28 packet in H23 before any outward sync or broader planning update.",
        "supported_here": [
            (
                f"R19 keeps pointer-like exact on {r19_gate['admitted_case_count'] + r19_gate['heldout_case_count']}/"
                f"{r19_gate['admitted_case_count'] + r19_gate['heldout_case_count']} bounded D0 rows across admitted and heldout variants."
            ),
            (
                f"R20 ends at `{r20_gate['lane_verdict']}` and records claim-relevant failure in "
                f"{len(r20_gate['negative_controls_with_claim_relevant_failure'])} negative-control families."
            ),
            (
                f"R23 keeps pointer-like exact on {r23_gate['pointer_like_exact_case_count']}/"
                f"{r23_gate['total_case_count']} current positive D0 rows."
            ),
        ],
        "unsupported_here": [
            "R28 does not overturn the mixed same-endpoint systems result by itself.",
            "R28 does not widen beyond the fixed tiny typed-bytecode D0 endpoint.",
            "R28 does not convert the bounded mechanism audit into a broader 'LLMs are computers' headline.",
        ],
        "disconfirmed_here": [
            "R28 disconfirms the narrower expectation that retrieval_total still dominates pointer-like exact after the current mechanism and systems packets."
            if gate["retrieval_bottleneck_verdict"] == "pointer_like_exact_non_retrieval_dominant"
            else "R28 does not disconfirm the expectation that retrieval_total remains dominant."
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    primitive_rows = build_primitive_rows(inputs)
    claim_layer_rows = build_claim_layer_rows(inputs, primitive_rows)
    cost_rows = build_cost_breakdown_rows(inputs)
    stress_limit_rows = build_stress_limit_rows(inputs)
    gate = assess_gate(
        inputs,
        primitive_rows=primitive_rows,
        claim_layer_rows=claim_layer_rows,
        cost_rows=cost_rows,
    )
    summary = build_summary(
        inputs,
        gate=gate,
        primitive_rows=primitive_rows,
        claim_layer_rows=claim_layer_rows,
        cost_rows=cost_rows,
        stress_limit_rows=stress_limit_rows,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "primitive_rows.json",
        {
            "experiment": "r28_primitive_rows",
            "environment": environment.as_dict(),
            "rows": primitive_rows,
        },
    )
    write_json(
        OUT_DIR / "contract_matrix.json",
        {
            "experiment": "r28_contract_matrix",
            "environment": environment.as_dict(),
            "matrix": {
                "claim_layers": claim_layer_rows,
                "primitives": primitive_rows,
            },
        },
    )
    write_csv(OUT_DIR / "cost_breakdown_rows.csv", cost_rows)
    write_json(
        OUT_DIR / "stress_limit_table.json",
        {
            "experiment": "r28_stress_limit_table",
            "environment": environment.as_dict(),
            "rows": stress_limit_rows,
        },
    )
    write_text(OUT_DIR / "claim_layer_map.md", render_claim_layer_map(claim_layer_rows))
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r28_d0_trace_retrieval_contract_audit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                relative_path(ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate" / "summary.json"),
                relative_path(ROOT / "results" / "R19_d0_pointer_like_surface_generalization_gate" / "runtime_rows.json"),
                relative_path(ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "summary.json"),
                relative_path(ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "runtime_matrix_rows.json"),
                relative_path(ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "row_mechanism_summary.json"),
                relative_path(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "summary.json"),
                relative_path(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "runtime_profile_rows.json"),
            ],
            "summary": summary,
        },
    )
    write_text(
        OUT_DIR / "README.md",
        "# R28 D0 Trace Retrieval Contract Audit\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `claim_layer_map.md`\n"
        "- `contract_matrix.json`\n"
        "- `primitive_rows.json`\n"
        "- `cost_breakdown_rows.csv`\n"
        "- `stress_limit_table.json`\n",
    )


if __name__ == "__main__":
    main()
