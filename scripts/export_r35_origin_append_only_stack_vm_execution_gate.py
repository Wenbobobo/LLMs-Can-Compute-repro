"""Export the Origin-core append-only stack-VM execution gate for R35."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from exec_trace import (
    TraceInterpreter,
    alternating_memory_loop_program,
    call_chain_program,
    countdown_program,
    dynamic_memory_program,
    equality_branch_program,
    flagged_indirect_accumulator_program,
    latest_write_program,
    loop_indirect_memory_program,
    memory_accumulator_program,
    selector_checkpoint_bank_program,
    stack_fanout_sum_program,
    stack_memory_ping_pong_program,
)
from model import FreeRunningTraceExecutor, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R35_origin_append_only_stack_vm_execution_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def build_case_manifest() -> list[dict[str, object]]:
    return [
        {"suite": "straight_line", "program": latest_write_program(), "holdout": False},
        {"suite": "straight_line", "program": memory_accumulator_program(), "holdout": False},
        {"suite": "loops", "program": countdown_program(12), "holdout": True},
        {"suite": "loops", "program": loop_indirect_memory_program(6), "holdout": True},
        {"suite": "indirect_memory", "program": dynamic_memory_program(), "holdout": False},
        {"suite": "indirect_memory", "program": stack_memory_ping_pong_program(), "holdout": False},
        {"suite": "control_flow", "program": equality_branch_program(2, 3), "holdout": False},
        {"suite": "control_flow", "program": alternating_memory_loop_program(5), "holdout": True},
        {"suite": "call_return", "program": call_chain_program(), "holdout": False},
        {"suite": "mixed_surface", "program": flagged_indirect_accumulator_program(4, base_address=32), "holdout": True},
        {"suite": "mixed_surface", "program": selector_checkpoint_bank_program(4, base_address=40), "holdout": True},
        {"suite": "stack_depth", "program": stack_fanout_sum_program(8, base_value=2), "holdout": True},
    ]


def run_case_row(case: dict[str, object]) -> dict[str, object]:
    program = case["program"]
    assert hasattr(program, "instructions")
    reference = TraceInterpreter().run(program)
    max_steps = max(reference.final_state.steps + 4, 32)

    linear_execution = run_free_running_exact(program, decode_mode="linear", max_steps=max_steps)
    accelerated_execution = run_free_running_exact(program, decode_mode="accelerated", max_steps=max_steps)
    pointer_execution = FreeRunningTraceExecutor(
        stack_strategy="pointer_like_exact",
        memory_strategy="pointer_like_exact",
    ).run(program, max_steps=max_steps)

    linear_outcome = compare_execution_to_reference(program, linear_execution)
    accelerated_outcome = compare_execution_to_reference(program, accelerated_execution)
    pointer_outcome = compare_execution_to_reference(program, pointer_execution)
    read_counter = Counter(observation.space for observation in pointer_execution.read_observations)
    instruction_names = [instruction.opcode.value for instruction in program.instructions]

    return {
        "suite": case["suite"],
        "program_name": program.name,
        "holdout": bool(case["holdout"]),
        "max_steps": max_steps,
        "program_steps": reference.final_state.steps,
        "contains_call": "call" in instruction_names or "ret" in instruction_names,
        "linear_exact_trace_match": linear_outcome.exact_trace_match,
        "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
        "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
        "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
        "pointer_like_exact_trace_match": pointer_outcome.exact_trace_match,
        "pointer_like_exact_final_state_match": pointer_outcome.exact_final_state_match,
        "pointer_like_first_mismatch_step": pointer_outcome.first_mismatch_step,
        "pointer_like_failure_reason": pointer_outcome.failure_reason,
        "pointer_like_exact_read_count": len(pointer_execution.read_observations),
        "pointer_like_exact_stack_read_count": read_counter.get("stack", 0),
        "pointer_like_exact_memory_read_count": read_counter.get("memory", 0),
        "pointer_like_exact_call_read_count": read_counter.get("call", 0),
    }


def build_suite_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["suite"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for suite in sorted(grouped):
        suite_rows = grouped[suite]
        summary_rows.append(
            {
                "suite": suite,
                "case_count": len(suite_rows),
                "pointer_like_exact_trace_match_count": sum(bool(row["pointer_like_exact_trace_match"]) for row in suite_rows),
                "pointer_like_exact_final_state_match_count": sum(
                    bool(row["pointer_like_exact_final_state_match"]) for row in suite_rows
                ),
                "call_read_case_count": sum(int(row["pointer_like_exact_call_read_count"] > 0) for row in suite_rows),
                "holdout_case_count": sum(int(bool(row["holdout"])) for row in suite_rows),
            }
        )
    return summary_rows


def assess_gate(rows: list[dict[str, object]], suite_summary: list[dict[str, object]]) -> dict[str, object]:
    pointer_exact_all = all(bool(row["pointer_like_exact_trace_match"]) for row in rows) and all(
        bool(row["pointer_like_exact_final_state_match"]) for row in rows
    )
    holdout_rows = [row for row in rows if bool(row["holdout"])]
    call_rows = [row for row in rows if bool(row["contains_call"])]
    return {
        "lane_verdict": "origin_stack_vm_exact_supported" if pointer_exact_all else "origin_stack_vm_exact_mixed",
        "pointer_like_exact_all_cases": pointer_exact_all,
        "holdout_exact_count": sum(
            bool(row["pointer_like_exact_trace_match"]) and bool(row["pointer_like_exact_final_state_match"])
            for row in holdout_rows
        ),
        "holdout_case_count": len(holdout_rows),
        "call_case_count": len(call_rows),
        "call_read_case_count": sum(int(row["pointer_like_exact_call_read_count"] > 0) for row in call_rows),
        "suite_count": len(suite_summary),
        "next_priority_lane": "h29_refreeze_after_r34_r35_origin_core_gate",
    }


def main() -> None:
    manifest = build_case_manifest()
    case_manifest_rows = [
        {
            "suite": row["suite"],
            "program_name": row["program"].name,
            "holdout": bool(row["holdout"]),
        }
        for row in manifest
    ]
    execution_rows = [run_case_row(case) for case in manifest]
    suite_summary = build_suite_summary(execution_rows)
    gate = assess_gate(execution_rows, suite_summary)
    failure_rows = [
        row
        for row in execution_rows
        if not (bool(row["pointer_like_exact_trace_match"]) and bool(row["pointer_like_exact_final_state_match"]))
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "case_manifest.json", {"rows": case_manifest_rows})
    write_json(OUT_DIR / "execution_rows.json", {"rows": execution_rows})
    write_json(OUT_DIR / "suite_summary.json", {"rows": suite_summary})
    write_json(OUT_DIR / "trace_failure_rows.json", {"rows": failure_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "r35_origin_append_only_stack_vm_execution_gate_complete",
                "active_runtime_lane": "r35_origin_append_only_stack_vm_execution_gate",
                "gate": {
                    **gate,
                    "executed_case_count": len(execution_rows),
                    "pointer_like_exact_trace_match_count": sum(
                        bool(row["pointer_like_exact_trace_match"]) for row in execution_rows
                    ),
                    "pointer_like_exact_final_state_match_count": sum(
                        bool(row["pointer_like_exact_final_state_match"]) for row in execution_rows
                    ),
                    "pointer_like_exact_read_count": sum(int(row["pointer_like_exact_read_count"]) for row in execution_rows),
                },
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
