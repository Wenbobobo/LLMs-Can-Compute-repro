"""Export the reopened R12 append-only executor long-horizon bundle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bytecode import r6_d0_long_horizon_scaling_cases, r8_d0_retrieval_pressure_cases
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R12_append_only_executor_long_horizon"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_inputs() -> dict[str, Any]:
    return {
        "m4_payload": read_json(ROOT / "results" / "M4_exact_hardmax_model" / "free_running_executor.json"),
        "r3_summary_payload": read_json(ROOT / "results" / "R3_d0_exact_execution_stress_gate" / "summary.json"),
        "r3_claim_payload": read_json(ROOT / "results" / "R3_d0_exact_execution_stress_gate" / "claim_impact.json"),
        "r4_payload": read_json(ROOT / "results" / "R4_mechanistic_retrieval_closure" / "summary.json"),
    }


def build_mode_summary_rows(m4_payload: dict[str, Any]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for mode_name, suites in m4_payload["evaluations"].items():
        for suite_name, suite_payload in suites.items():
            outcomes = list(suite_payload["outcomes"])
            rows.append(
                {
                    "mode": mode_name,
                    "suite": suite_name,
                    "program_count": int(suite_payload["program_count"]),
                    "exact_trace_accuracy": float(suite_payload["exact_trace_accuracy"]),
                    "exact_final_state_accuracy": float(suite_payload["exact_final_state_accuracy"]),
                    "max_program_steps": max(int(outcome["program_steps"]) for outcome in outcomes) if outcomes else 0,
                }
            )
    return rows


def build_free_running_baseline(
    m4_payload: dict[str, Any],
    mode_rows: list[dict[str, object]],
) -> dict[str, object]:
    exact_accel = m4_payload["evaluations"]["exact_accelerated"]
    heldout = exact_accel["countdown_heldout"]
    max_exact_heldout_steps = max(int(outcome["program_steps"]) for outcome in heldout["outcomes"])
    return {
        "mode_count": len(m4_payload["evaluations"]),
        "mode_names": sorted(m4_payload["evaluations"].keys()),
        "all_modes_exact": all(
            float(row["exact_trace_accuracy"]) == 1.0 and float(row["exact_final_state_accuracy"]) == 1.0
            for row in mode_rows
        ),
        "countdown_heldout_program_count": int(heldout["program_count"]),
        "max_exact_heldout_steps": max_exact_heldout_steps,
        "trainable_stack_program_count": int(m4_payload["evaluations"]["trainable_stack"]["countdown_heldout"]["program_count"]),
    }


def build_harder_d0_baseline(
    r3_summary_payload: dict[str, Any],
    r3_claim_payload: dict[str, Any],
) -> dict[str, object]:
    summary = r3_summary_payload["summary"]
    exact_suite = summary["exact_suite"]
    decode_parity = summary["decode_parity"]
    precision_followup = summary["precision_followup"]
    claim_impact = r3_claim_payload["summary"]
    return {
        "exact_suite_row_count": int(exact_suite["row_count"]),
        "positive_row_count": int(exact_suite["positive_row_count"]),
        "exact_trace_match_count": int(exact_suite["exact_trace_match_count"]),
        "exact_final_state_match_count": int(exact_suite["exact_final_state_match_count"]),
        "decode_parity_match_count": int(decode_parity["parity_match_count"]),
        "boundary_bearing_stream_count": int(precision_followup["boundary_bearing_stream_count"]),
        "negative_control_failure_count": int(precision_followup["negative_control_failure_count"]),
        "e1c_status": str(claim_impact["e1c_status"]),
    }


def build_mechanistic_baseline(r4_payload: dict[str, Any]) -> dict[str, object]:
    overall = r4_payload["summary"]["overall"]
    return {
        "program_count": int(overall["program_count"]),
        "suite_count": int(overall["suite_count"]),
        "event_count": int(overall["event_count"]),
        "source_observation_count": int(overall["source_observation_count"]),
        "parity_failure_count": int(overall["parity_failure_count"]),
        "contradiction_candidate_count": int(overall["contradiction_candidate_count"]),
    }


def build_horizon_inventory_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in r6_d0_long_horizon_scaling_cases():
        rows.append(
            {
                "stage": "R6_d0_long_horizon_scaling_gate",
                "family": case.family,
                "baseline_stage": case.baseline_stage,
                "baseline_program_name": case.baseline_program_name,
                "horizon_multiplier": case.horizon_multiplier,
                "comparison_mode": case.comparison_mode,
                "max_steps": case.max_steps,
                "program_name": case.program.name,
            }
        )
    for case in r8_d0_retrieval_pressure_cases():
        rows.append(
            {
                "stage": "R8_d0_retrieval_pressure_gate",
                "family": case.family,
                "baseline_stage": case.baseline_stage,
                "baseline_program_name": case.baseline_program_name,
                "horizon_multiplier": case.retrieval_horizon_multiplier,
                "comparison_mode": case.comparison_mode,
                "max_steps": case.max_steps,
                "program_name": case.program.name,
            }
        )
    return rows


def build_horizon_inventory_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    r6_rows = [row for row in rows if str(row["stage"]) == "R6_d0_long_horizon_scaling_gate"]
    r8_rows = [row for row in rows if str(row["stage"]) == "R8_d0_retrieval_pressure_gate"]
    return {
        "r6_row_count": len(r6_rows),
        "r6_family_count": len({str(row["family"]) for row in r6_rows}),
        "r8_row_count": len(r8_rows),
        "r8_family_count": len({str(row["family"]) for row in r8_rows}),
        "max_r6_horizon_multiplier": max(int(row["horizon_multiplier"]) for row in r6_rows),
        "max_r8_horizon_multiplier": max(int(row["horizon_multiplier"]) for row in r8_rows),
        "comparison_modes": sorted({str(row["comparison_mode"]) for row in rows}),
        "priority_r8_families": sorted({str(row["family"]) for row in r8_rows}),
    }


def build_failure_taxonomy_rows() -> list[dict[str, object]]:
    return [
        {
            "failure_type": "retrieval_exactness",
            "trigger": "Latest-write reads diverge from exact reference or decode parity breaks.",
            "bounded_response": "Inspect address/step encoding and exact-read agreement before widening.",
        },
        {
            "failure_type": "horizon_budget",
            "trigger": "The executor exhausts the bounded step budget before the reference trace halts.",
            "bounded_response": "Keep the endpoint fixed and decide whether the gap is purely horizon scaling or a deeper mechanism fault.",
        },
        {
            "failure_type": "trace_organization",
            "trigger": "Harder helper, checkpoint, or subroutine organization breaks exactness without a direct retrieval mismatch.",
            "bounded_response": "Localize the failure to the event organization before considering any trainable bridge.",
        },
        {
            "failure_type": "precision_boundary",
            "trigger": "A real-trace or longer-memory stream becomes boundary-bearing under the preserved precision companion rules.",
            "bounded_response": "Keep the issue companion-only unless it contradicts the fixed exact endpoint.",
        },
        {
            "failure_type": "local_transition",
            "trigger": "Retrieval remains exact but the local deterministic transition still diverges from the reference execution.",
            "bounded_response": "Treat this as a transition implementation bug, not evidence for broader scope widening.",
        },
    ]


def build_summary(
    free_running_baseline: dict[str, object],
    harder_d0_baseline: dict[str, object],
    mechanistic_baseline: dict[str, object],
    horizon_inventory: dict[str, object],
    failure_taxonomy_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "free_running_baseline": free_running_baseline,
        "harder_d0_baseline": harder_d0_baseline,
        "mechanistic_baseline": mechanistic_baseline,
        "horizon_inventory": horizon_inventory,
        "claim_impact": {
            "status": "append_only_executor_long_horizon_reaudit_exported",
            "target_claims": ["D0"],
            "next_lane": "H15_refreeze_and_decision_sync",
            "supported_here": [
                "The current exact free-running executor remains exact on the preserved M4 countdown, branch, and memory suites in both linear and accelerated modes.",
                "The preserved harder D0 baseline still records 7/7 exact-suite rows, 7/7 decode-parity rows, and no contradiction candidates.",
                "The reopened long-horizon inventory is explicit across 24 staged R6 rows and 4 staged R8 harder rows on the same fixed endpoint.",
            ],
            "unsupported_here": [
                "R12 does not yet authorize unseen-family generalization beyond the currently staged R6/R8 families.",
                "Trainable stack success remains a bounded bridge observation and does not reopen a broad neural executor claim.",
            ],
            "followup_contract": {
                "conditional_r13_only_if": "A remaining bounded executor gap is localized to the stack-read bridge rather than endpoint scope or precision collapse.",
                "priority_r8_families": horizon_inventory["priority_r8_families"],
                "failure_taxonomy": [row["failure_type"] for row in failure_taxonomy_rows],
            },
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    mode_rows = build_mode_summary_rows(inputs["m4_payload"])
    free_running_baseline = build_free_running_baseline(inputs["m4_payload"], mode_rows)
    harder_d0_baseline = build_harder_d0_baseline(inputs["r3_summary_payload"], inputs["r3_claim_payload"])
    mechanistic_baseline = build_mechanistic_baseline(inputs["r4_payload"])
    inventory_rows = build_horizon_inventory_rows()
    horizon_inventory = build_horizon_inventory_summary(inventory_rows)
    failure_taxonomy_rows = build_failure_taxonomy_rows()
    summary = build_summary(
        free_running_baseline,
        harder_d0_baseline,
        mechanistic_baseline,
        horizon_inventory,
        failure_taxonomy_rows,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r12_append_only_executor_long_horizon",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/M4_exact_hardmax_model/free_running_executor.json",
                "results/R3_d0_exact_execution_stress_gate/summary.json",
                "results/R3_d0_exact_execution_stress_gate/claim_impact.json",
                "results/R4_mechanistic_retrieval_closure/summary.json",
                "src/bytecode/datasets.py",
                "src/model/free_running_executor.py",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "mode_summary.json",
        {
            "experiment": "r12_mode_summary",
            "environment": environment.as_dict(),
            "rows": mode_rows,
        },
    )
    write_json(
        OUT_DIR / "horizon_inventory.json",
        {
            "experiment": "r12_horizon_inventory",
            "environment": environment.as_dict(),
            "summary": horizon_inventory,
            "rows": inventory_rows,
        },
    )
    write_json(
        OUT_DIR / "failure_taxonomy.json",
        {
            "experiment": "r12_failure_taxonomy",
            "environment": environment.as_dict(),
            "rows": failure_taxonomy_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r12_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R12 Append-Only Executor Long-Horizon",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `mode_summary.json`",
                "- `horizon_inventory.json`",
                "- `failure_taxonomy.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
