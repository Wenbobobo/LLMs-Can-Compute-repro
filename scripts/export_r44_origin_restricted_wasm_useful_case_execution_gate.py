"""Export the restricted-Wasm useful-case execution gate for R44."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    BytecodeMemoryRegion,
    BytecodeOpcode,
    BytecodeProgram,
    RestrictedWasmKernelCase,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    r44_restricted_wasm_useful_case_cases,
    run_spec_program,
    validate_program_contract,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, compare_execution_to_reference, run_free_running_exact
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R44_origin_restricted_wasm_useful_case_execution_gate"


ALLOWED_OPCODES: frozenset[BytecodeOpcode] = frozenset(
    {
        BytecodeOpcode.CONST_I32,
        BytecodeOpcode.DUP,
        BytecodeOpcode.POP,
        BytecodeOpcode.ADD_I32,
        BytecodeOpcode.SUB_I32,
        BytecodeOpcode.EQ_I32,
        BytecodeOpcode.LOAD_STATIC,
        BytecodeOpcode.STORE_STATIC,
        BytecodeOpcode.JMP,
        BytecodeOpcode.JZ_ZERO,
        BytecodeOpcode.HALT,
    }
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_state_dict(state: object) -> dict[str, object]:
    pc, stack, memory, call_stack, halted, steps = normalize_final_state(state)
    return {
        "pc": int(pc),
        "stack": list(stack),
        "memory": [list(item) for item in memory],
        "call_stack": list(call_stack),
        "halted": bool(halted),
        "steps": int(steps),
    }


def serialize_bytecode_program(program: BytecodeProgram) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pc, instruction in enumerate(program.instructions):
        rows.append(
            {
                "pc": pc,
                "opcode": instruction.opcode.value,
                "arg": instruction.arg,
                "in_types": [item.value for item in instruction.in_types],
                "out_types": [item.value for item in instruction.out_types],
            }
        )
    return rows


def serialize_trace_program(program: Any) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pc, instruction in enumerate(program.instructions):
        opcode = getattr(getattr(instruction, "opcode", None), "value", getattr(instruction, "opcode", None))
        rows.append({"pc": pc, "opcode": opcode, "arg": instruction.arg})
    return rows


def opcode_surface(program: BytecodeProgram) -> list[str]:
    return sorted({instruction.opcode.value for instruction in program.instructions})


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def validate_r44_scope(case: RestrictedWasmKernelCase) -> tuple[bool, str | None]:
    program = case.program
    opcodes = {instruction.opcode for instruction in program.instructions}
    if not opcodes.issubset(ALLOWED_OPCODES):
        return False, "opcode_out_of_scope"
    if any(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout):
        return False, "heap_region_not_admitted"
    return True, None


def declared_memory_snapshot(program: BytecodeProgram, state: object) -> dict[str, int]:
    _, _, memory, _, _, _ = normalize_final_state(state)
    memory_map = {int(address): int(value) for address, value in memory}
    return {
        cell.label: memory_map.get(cell.address, 0)
        for cell in sorted(program.memory_layout, key=lambda item: item.address)
    }


def failure_class(row: dict[str, object]) -> str | None:
    if not row["scope_passed"]:
        return "scope_break"
    if not row["verifier_passed"]:
        return "verifier_break"
    if not row["spec_contract_passed"]:
        return "spec_contract_break"
    if not row["surface_literal_passed"]:
        return "surface_literal_break"
    if not row["source_spec_trace_match"] or not row["source_spec_final_state_match"]:
        return "source_spec_break"
    if not row["source_to_lowered_trace_match"] or not row["source_to_lowered_final_state_match"]:
        return "lowering_break"
    if not row["free_running_trace_match"] or not row["free_running_final_state_match"]:
        return "free_running_break"
    return None


def assess_gate(exactness_rows: list[dict[str, object]], stop_rule: dict[str, object]) -> dict[str, object]:
    planned_count = len(exactness_rows)
    executed_rows = [row for row in exactness_rows if row["executed"]]
    executed_count = len(executed_rows)
    exact_count = sum(row["verdict"] == "exact" for row in executed_rows)
    first_failure = stop_rule["first_failure"]

    exact_prefix_count = 0
    for row in exactness_rows:
        if row["verdict"] == "exact":
            exact_prefix_count += 1
            continue
        break

    if exact_count == planned_count and executed_count == planned_count:
        lane_verdict = "useful_case_surface_supported_narrowly"
    elif first_failure is None:
        lane_verdict = "keep_semantic_boundary_route"
    elif first_failure["stop_class"] in {
        "scope_break",
        "verifier_break",
        "spec_contract_break",
        "surface_literal_break",
    }:
        lane_verdict = "useful_case_surface_break"
    elif exact_prefix_count > 0:
        lane_verdict = "mixed_nonunique"
    else:
        lane_verdict = "useful_case_surface_break"

    exact_kernel_ids = [row["kernel_id"] for row in executed_rows if row["verdict"] == "exact"]
    return {
        "lane_verdict": lane_verdict,
        "route_posture": "keep_semantic_boundary_route",
        "planned_kernel_count": planned_count,
        "executed_kernel_count": executed_count,
        "exact_kernel_count": exact_count,
        "exact_prefix_count": exact_prefix_count,
        "exact_kernel_ids": exact_kernel_ids,
        "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
        "article_level_substrate_evidence_exceeded_narrowly": "histogram16_u8" in exact_kernel_ids,
        "claim_ceiling": "bounded_useful_cases_only",
        "later_explicit_followup_packet_required": True,
        "conditional_next_runtime_candidate": "none",
    }


def build_artifacts() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    cases = r44_restricted_wasm_useful_case_cases()
    manifest_rows = [
        {
            "kernel_order": index + 1,
            "kernel_id": case.kernel_id,
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
            "description": case.description,
        }
        for index, case in enumerate(cases)
    ]
    exactness_rows: list[dict[str, object]] = []
    cost_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        if first_failure is not None:
            exactness_rows.append(
                {
                    "kernel_id": case.kernel_id,
                    "executed": False,
                    "verdict": "not_executed_after_prior_failure",
                    "stop_class": None,
                    "source_spec_trace_match": None,
                    "source_spec_final_state_match": None,
                    "source_to_lowered_trace_match": None,
                    "source_to_lowered_final_state_match": None,
                    "free_running_trace_match": None,
                    "free_running_final_state_match": None,
                    "first_mismatch_step": None,
                    "failure_reason": None,
                    "source_final_state": None,
                    "lowered_final_state": None,
                    "free_running_final_state": None,
                }
            )
            cost_rows.append(
                {
                    "kernel_id": case.kernel_id,
                    "executed": False,
                    "instruction_count": len(case.program.instructions),
                    "program_steps": None,
                    "memory_read_event_count": None,
                    "memory_write_event_count": None,
                    "branch_event_count": None,
                    "free_running_read_count": None,
                    "free_running_stack_read_count": None,
                    "free_running_memory_read_count": None,
                    "free_running_call_read_count": None,
                    "declared_memory_cell_count": len(case.program.memory_layout),
                    "opcode_surface": opcode_surface(case.program),
                }
            )
            continue

        program = case.program
        verifier_result = verify_program(program)
        spec_contract = validate_program_contract(program)
        surface_literal = validate_surface_literals(program)
        scope_passed, scope_error_class = validate_r44_scope(case)
        spec_result = run_spec_program(program, max_steps=case.max_steps)
        source_result = BytecodeInterpreter().run(program, max_steps=case.max_steps)
        lowered_program = lower_program(program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(case.max_steps, source_result.final_state.steps + 8)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )

        read_counter = Counter(observation.space for observation in free_running_result.read_observations)
        source_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in source_result.events
        )
        source_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            source_result.final_state
        )
        source_to_lowered_trace_match = tuple(source_result.events) == tuple(lowered_result.events)
        source_to_lowered_final_state_match = source_result.final_state == lowered_result.final_state
        memory_read_event_count = sum(int(event.memory_read_address is not None) for event in source_result.events)
        memory_write_event_count = sum(int(event.memory_write is not None) for event in source_result.events)
        branch_event_count = sum(int(bool(event.branch_taken)) for event in source_result.events)

        exactness_row = {
            "kernel_id": case.kernel_id,
            "executed": True,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "scope_passed": scope_passed,
            "scope_error_class": scope_error_class,
            "source_spec_trace_match": source_spec_trace_match,
            "source_spec_final_state_match": source_spec_final_state_match,
            "source_spec_first_mismatch_step": first_divergence_step(spec_result.events, source_result.events),
            "source_to_lowered_trace_match": source_to_lowered_trace_match,
            "source_to_lowered_final_state_match": source_to_lowered_final_state_match,
            "source_to_lowered_first_mismatch_step": first_divergence_step(source_result.events, lowered_result.events),
            "free_running_trace_match": free_running_outcome.exact_trace_match,
            "free_running_final_state_match": free_running_outcome.exact_final_state_match,
            "first_mismatch_step": free_running_outcome.first_mismatch_step,
            "failure_reason": free_running_outcome.failure_reason,
            "source_final_state": normalize_state_dict(source_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "free_running_final_state": normalize_state_dict(free_running_result.final_state),
            "source_declared_memory": declared_memory_snapshot(program, source_result.final_state),
            "lowered_declared_memory": declared_memory_snapshot(program, lowered_result.final_state),
            "free_running_declared_memory": declared_memory_snapshot(program, free_running_result.final_state),
            "source_program": serialize_bytecode_program(program),
            "lowered_program": serialize_trace_program(lowered_program),
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        cost_rows.append(
            {
                "kernel_id": case.kernel_id,
                "executed": True,
                "instruction_count": len(program.instructions),
                "program_steps": source_result.final_state.steps,
                "memory_read_event_count": memory_read_event_count,
                "memory_write_event_count": memory_write_event_count,
                "branch_event_count": branch_event_count,
                "free_running_read_count": len(free_running_result.read_observations),
                "free_running_stack_read_count": read_counter.get("stack", 0),
                "free_running_memory_read_count": read_counter.get("memory", 0),
                "free_running_call_read_count": read_counter.get("call", 0),
                "declared_memory_cell_count": len(program.memory_layout),
                "opcode_surface": opcode_surface(program),
            }
        )

        if stop_class is not None:
            first_failure = {
                "kernel_id": case.kernel_id,
                "stop_class": stop_class,
                "first_mismatch_step": free_running_outcome.first_mismatch_step,
                "failure_reason": free_running_outcome.failure_reason,
            }

    stop_rule = {
        "planned_kernel_count": len(cases),
        "executed_kernel_count": sum(int(row["executed"]) for row in exactness_rows),
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "reason": "all fixed useful kernels stayed exact on source/spec, source/lowered, trace, and final state"
        if first_failure is None
        else "stopped at the first restricted useful-kernel failure",
    }
    return manifest_rows, exactness_rows, cost_rows, stop_rule


def main() -> None:
    manifest_rows, exactness_rows, cost_rows, stop_rule = build_artifacts()
    gate = assess_gate(exactness_rows, stop_rule)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "lowering_manifest.json", {"rows": manifest_rows})
    write_json(
        OUT_DIR / "kernel_suite_report.json",
        {
            "exactness_rows": exactness_rows,
            "cost_rows": cost_rows,
        },
    )
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "r44_origin_restricted_wasm_useful_case_execution_gate_complete",
                "active_runtime_lane": "r44_origin_restricted_wasm_useful_case_execution_gate",
                "activation_packet": "h42_post_r43_route_selection_packet",
                "current_completed_exact_runtime_gate": "r43_origin_bounded_memory_small_vm_execution_gate",
                "coequal_model_comparator_gate": "r45_origin_dual_mode_model_mainline_gate",
                "current_semantic_boundary_roadmap": "f19_post_f18_restricted_wasm_useful_case_roadmap",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
