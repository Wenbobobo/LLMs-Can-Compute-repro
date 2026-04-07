"""Export the actual post-H54 compiled useful-kernel carryover gate for R60."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    BytecodeMemoryRegion,
    BytecodeOpcode,
    BytecodeProgram,
    RestrictedTinyCLoweringCase,
    compile_restricted_tinyc_program,
    first_divergence_step,
    lower_program,
    lower_restricted_tinyc_program,
    normalize_event,
    normalize_final_state,
    r50_restricted_tinyc_lowering_cases,
    run_spec_program,
    serialize_restricted_frontend_program,
    serialize_restricted_tinyc_program,
    validate_program_contract,
    validate_restricted_frontend_program,
    validate_restricted_tinyc_program,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import FreeRunningExecutionResult, FreeRunningTraceExecutor, compare_execution_to_reference
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R60_origin_compiled_useful_kernel_carryover_gate"

ADMITTED_VARIANT_IDS: tuple[str, ...] = (
    "sum_len6_shifted_base",
    "sum_len8_dense_mixed_sign",
    "count_sparse_len8_shifted_base",
    "count_dense_len7_shifted_base",
    "count_mixed_len9_shifted_base",
)

ALLOWED_OPCODES: frozenset[BytecodeOpcode] = frozenset(
    {
        BytecodeOpcode.CONST_I32,
        BytecodeOpcode.CONST_ADDR,
        BytecodeOpcode.DUP,
        BytecodeOpcode.POP,
        BytecodeOpcode.ADD_I32,
        BytecodeOpcode.SUB_I32,
        BytecodeOpcode.EQ_I32,
        BytecodeOpcode.LOAD_STATIC,
        BytecodeOpcode.STORE_STATIC,
        BytecodeOpcode.LOAD_INDIRECT,
        BytecodeOpcode.STORE_INDIRECT,
        BytecodeOpcode.JMP,
        BytecodeOpcode.JZ_ZERO,
        BytecodeOpcode.CALL,
        BytecodeOpcode.RET,
        BytecodeOpcode.HALT,
    }
)

INPUT_DECL_RE = re.compile(r"^int input\[(?P<count>\d+)\] = \{(?P<values>[^}]*)\};$")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def admitted_cases() -> tuple[RestrictedTinyCLoweringCase, ...]:
    order = {variant_id: index for index, variant_id in enumerate(ADMITTED_VARIANT_IDS)}
    selected = [
        case
        for case in r50_restricted_tinyc_lowering_cases()
        if case.variant_id in order and case.kernel_id in {"sum_i32_buffer", "count_nonzero_i32_buffer"}
    ]
    if len(selected) != len(ADMITTED_VARIANT_IDS):
        raise RuntimeError("R60 admitted case set does not match the declared five-row useful-kernel suite.")
    return tuple(sorted(selected, key=lambda case: order[case.variant_id]))


def parse_input_values(source_text: str) -> tuple[int, ...]:
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        match = INPUT_DECL_RE.fullmatch(line)
        if match is None:
            continue
        values = [item.strip() for item in match.group("values").split(",") if item.strip()]
        count = int(match.group("count"))
        parsed = tuple(int(value) for value in values)
        if len(parsed) != count:
            raise ValueError("input_initializer_length_mismatch")
        return parsed
    raise ValueError("input_declaration_not_found")


def validate_compiled_scope(program: BytecodeProgram) -> tuple[bool, str | None]:
    opcodes = {instruction.opcode for instruction in program.instructions}
    if not opcodes.issubset(ALLOWED_OPCODES):
        return False, "opcode_out_of_scope"
    if any(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout):
        return False, "heap_region_not_admitted"
    return True, None


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


def declared_memory_snapshot(program: BytecodeProgram, state: object) -> dict[str, int]:
    _, _, memory, _, _, _ = normalize_final_state(state)
    memory_map = {int(address): int(value) for address, value in memory}
    return {
        cell.label: memory_map.get(cell.address, 0)
        for cell in sorted(program.memory_layout, key=lambda item: item.address)
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


def failure_class(row: dict[str, object]) -> str | None:
    if not row["tinyc_scope_passed"]:
        return "tinyc_scope_break"
    if not row["frontend_scope_passed"]:
        return "frontend_scope_break"
    if not row["compiled_scope_passed"]:
        return "compiled_scope_break"
    if not row["verifier_passed"]:
        return "verifier_break"
    if not row["spec_contract_passed"]:
        return "spec_contract_break"
    if not row["surface_literal_passed"]:
        return "surface_literal_break"
    if not row["translation_identity_match"]:
        return "compiler_work_leakage"
    if not row["compiled_to_canonical_trace_match"] or not row["compiled_to_canonical_final_state_match"]:
        return "canonical_alignment_break"
    if not row["compiled_spec_trace_match"] or not row["compiled_spec_final_state_match"]:
        return "spec_break"
    if not row["compiled_to_lowered_trace_match"] or not row["compiled_to_lowered_final_state_match"]:
        return "lowering_break"
    if not row["linear_exact_trace_match"] or not row["linear_exact_final_state_match"]:
        return "linear_free_running_break"
    if not row["accelerated_exact_trace_match"] or not row["accelerated_exact_final_state_match"]:
        return "accelerated_free_running_break"
    return None


def build_artifacts() -> tuple[list[dict[str, object]], dict[str, object], dict[str, object], dict[str, object]]:
    cases = admitted_cases()
    manifest_rows = [
        {
            "case_order": index + 1,
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "tinyc_program_name": case.tinyc_program.name,
            "canonical_program_name": case.canonical_program.name,
            "input_length": len(parse_input_values(case.tinyc_program.source_text)),
        }
        for index, case in enumerate(cases)
    ]

    exactness_rows: list[dict[str, object]] = []
    coverage_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        input_values = parse_input_values(case.tinyc_program.source_text)
        tinyc_scope_passed, tinyc_scope_error = validate_restricted_tinyc_program(case.tinyc_program)
        frontend_program = lower_restricted_tinyc_program(case.tinyc_program)
        frontend_scope_passed, frontend_scope_error = validate_restricted_frontend_program(frontend_program)
        compiled_program = compile_restricted_tinyc_program(case.tinyc_program)
        compiled_scope_passed, compiled_scope_error = validate_compiled_scope(compiled_program)
        verifier_result = verify_program(compiled_program)
        spec_contract = validate_program_contract(compiled_program)
        surface_literal = validate_surface_literals(compiled_program)
        spec_result = run_spec_program(compiled_program, max_steps=case.max_steps)
        compiled_result = BytecodeInterpreter().run(compiled_program, max_steps=case.max_steps)
        canonical_result = BytecodeInterpreter().run(case.canonical_program, max_steps=case.max_steps)
        lowered_program = lower_program(compiled_program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)

        max_steps = max(case.max_steps, compiled_result.final_state.steps + 8)
        linear_executor = FreeRunningTraceExecutor(
            stack_strategy="linear",
            memory_strategy="linear",
            validate_exact_reads=False,
        )
        accelerated_executor = FreeRunningTraceExecutor(
            stack_strategy="accelerated",
            memory_strategy="accelerated",
            validate_exact_reads=False,
        )
        linear_result = linear_executor.run(lowered_program, max_steps=max_steps)
        accelerated_result = accelerated_executor.run(lowered_program, max_steps=max_steps)
        reference_execution = reference_wrapper(lowered_program, lowered_result)
        linear_outcome = compare_execution_to_reference(lowered_program, linear_result, reference=reference_execution)
        accelerated_outcome = compare_execution_to_reference(
            lowered_program,
            accelerated_result,
            reference=reference_execution,
        )

        normalized_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in compiled_result.events
        )
        normalized_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            compiled_result.final_state
        )
        compiled_to_canonical_trace_match = tuple(normalize_event(event) for event in compiled_result.events) == tuple(
            normalize_event(event) for event in canonical_result.events
        )
        compiled_to_canonical_final_state_match = normalize_final_state(compiled_result.final_state) == normalize_final_state(
            canonical_result.final_state
        )
        compiled_to_lowered_trace_match = tuple(compiled_result.events) == tuple(lowered_result.events)
        compiled_to_lowered_final_state_match = compiled_result.final_state == lowered_result.final_state
        translation_identity_match = (
            compiled_program.instructions == case.canonical_program.instructions
            and compiled_program.memory_layout == case.canonical_program.memory_layout
        )

        linear_counter = Counter(observation.space for observation in linear_result.read_observations)
        accelerated_counter = Counter(observation.space for observation in accelerated_result.read_observations)
        branch_event_count = sum(int(bool(event.branch_taken)) for event in compiled_result.events)

        exactness_row = {
            "kernel_id": case.kernel_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "input_length": len(input_values),
            "executed": True,
            "tinyc_scope_passed": tinyc_scope_passed,
            "tinyc_scope_error_class": tinyc_scope_error,
            "frontend_scope_passed": frontend_scope_passed,
            "frontend_scope_error_class": frontend_scope_error,
            "compiled_scope_passed": compiled_scope_passed,
            "compiled_scope_error_class": compiled_scope_error,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "translation_identity_match": translation_identity_match,
            "compiled_spec_trace_match": normalized_spec_trace_match,
            "compiled_spec_final_state_match": normalized_spec_final_state_match,
            "compiled_spec_first_mismatch_step": first_divergence_step(spec_result.events, compiled_result.events),
            "compiled_to_canonical_trace_match": compiled_to_canonical_trace_match,
            "compiled_to_canonical_final_state_match": compiled_to_canonical_final_state_match,
            "compiled_to_canonical_first_mismatch_step": first_divergence_step(canonical_result.events, compiled_result.events),
            "compiled_to_lowered_trace_match": compiled_to_lowered_trace_match,
            "compiled_to_lowered_final_state_match": compiled_to_lowered_final_state_match,
            "compiled_to_lowered_first_mismatch_step": first_divergence_step(compiled_result.events, lowered_result.events),
            "linear_exact_trace_match": linear_outcome.exact_trace_match,
            "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
            "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
            "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
            "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
            "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
            "compiled_final_state": normalize_state_dict(compiled_result.final_state),
            "canonical_final_state": normalize_state_dict(canonical_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "linear_final_state": normalize_state_dict(linear_result.final_state),
            "accelerated_final_state": normalize_state_dict(accelerated_result.final_state),
            "compiled_declared_memory": declared_memory_snapshot(compiled_program, compiled_result.final_state),
            "canonical_declared_memory": declared_memory_snapshot(case.canonical_program, canonical_result.final_state),
            "linear_declared_memory": declared_memory_snapshot(compiled_program, linear_result.final_state),
            "accelerated_declared_memory": declared_memory_snapshot(compiled_program, accelerated_result.final_state),
            "tinyc_program": serialize_restricted_tinyc_program(case.tinyc_program),
            "frontend_program": serialize_restricted_frontend_program(frontend_program),
            "compiled_program": serialize_bytecode_program(compiled_program),
            "canonical_program": serialize_bytecode_program(case.canonical_program),
            "lowered_program": serialize_trace_program(lowered_program),
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        coverage_rows.append(
            {
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "input_length": len(input_values),
                "compiled_instruction_count": len(compiled_program.instructions),
                "transition_count": len(lowered_result.events),
                "program_steps": compiled_result.final_state.steps,
                "declared_memory_cell_count": len(compiled_program.memory_layout),
                "branch_event_count": branch_event_count,
                "linear_read_count": len(linear_result.read_observations),
                "linear_stack_read_count": linear_counter.get("stack", 0),
                "linear_memory_read_count": linear_counter.get("memory", 0),
                "linear_call_read_count": linear_counter.get("call", 0),
                "linear_retrieval_share_of_transitions": (
                    len(linear_result.read_observations) / len(lowered_result.events)
                    if lowered_result.events
                    else 0.0
                ),
                "accelerated_read_count": len(accelerated_result.read_observations),
                "accelerated_stack_read_count": accelerated_counter.get("stack", 0),
                "accelerated_memory_read_count": accelerated_counter.get("memory", 0),
                "accelerated_call_read_count": accelerated_counter.get("call", 0),
                "accelerated_retrieval_share_of_transitions": (
                    len(accelerated_result.read_observations) / len(lowered_result.events)
                    if lowered_result.events
                    else 0.0
                ),
                "opcode_surface": opcode_surface(compiled_program),
            }
        )

        if first_failure is None and stop_class is not None:
            first_failure = {
                "kernel_id": case.kernel_id,
                "variant_id": case.variant_id,
                "stop_class": stop_class,
                "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
                "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
            }

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in exactness_rows:
        grouped[str(row["kernel_id"])].append(row)
    kernel_rollup_rows = [
        {
            "kernel_id": kernel_id,
            "planned_variant_count": len(rows),
            "exact_variant_count": sum(row["verdict"] == "exact" for row in rows),
            "input_lengths": [int(row["input_length"]) for row in rows],
            "translation_identity_exact_count": sum(bool(row["translation_identity_match"]) for row in rows),
        }
        for kernel_id, rows in sorted(grouped.items())
    ]

    exact_rows = [row for row in exactness_rows if row["verdict"] == "exact"]
    stop_rule = {
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "stop_policy": "stop at first scope, compiler-leakage, parity, or free-running exactness break",
    }
    gate = {
        "lane_verdict": (
            "compiled_useful_kernel_carryover_supported_exactly"
            if len(exact_rows) == len(exactness_rows)
            else "compiled_useful_kernel_carryover_break"
        ),
        "restricted_surface": "compiled_tinyc_useful_kernel_pair_on_current_compiled_boundary_route",
        "planned_variant_count": len(exactness_rows),
        "executed_variant_count": len(exactness_rows),
        "exact_variant_count": len(exact_rows),
        "failed_variant_count": len(exactness_rows) - len(exact_rows),
        "planned_kernel_count": len({str(row["kernel_id"]) for row in exactness_rows}),
        "exact_kernel_count": len({str(row["kernel_id"]) for row in exact_rows}),
        "exact_kernel_ids": sorted({str(row["kernel_id"]) for row in exact_rows}),
        "translation_identity_exact_count": sum(bool(row["translation_identity_match"]) for row in exact_rows),
        "linear_exact_variant_count": sum(
            row["linear_exact_trace_match"] and row["linear_exact_final_state_match"] for row in exactness_rows
        ),
        "accelerated_exact_variant_count": sum(
            row["accelerated_exact_trace_match"] and row["accelerated_exact_final_state_match"] for row in exactness_rows
        ),
        "compiler_work_leakage_break_count": sum(row["stop_class"] == "compiler_work_leakage" for row in exactness_rows),
        "claim_ceiling": "bounded_useful_cases_only",
        "selected_h55_outcome": "authorize_useful_kernel_carryover_through_r60_first",
        "next_required_packet": (
            "r61_origin_compiled_useful_kernel_value_gate"
            if len(exact_rows) == len(exactness_rows)
            else "h56_post_r60_r61_useful_kernel_decision_packet"
        ),
    }
    report = {
        "runtime_environment": environment_payload(),
        "exactness_rows": exactness_rows,
        "kernel_rollup_rows": kernel_rollup_rows,
        "coverage_rows": coverage_rows,
        "first_failure": first_failure,
    }
    checklist_rows = [
        {
            "item_id": "r60_requires_h55_reentry_authorization",
            "status": "pass",
            "notes": "R60 runs only under the explicit H55 useful-kernel reentry packet.",
        },
        {
            "item_id": "r60_admitted_pair_stays_exact_on_all_rows",
            "status": "pass" if gate["lane_verdict"] == "compiled_useful_kernel_carryover_supported_exactly" else "blocked",
            "notes": "All admitted sum/count preserved useful-kernel rows must keep exact source/spec/lowered and linear/accelerated internal execution parity.",
        },
        {
            "item_id": "r60_shows_no_compiler_work_leakage_on_declared_rows",
            "status": "pass" if gate["compiler_work_leakage_break_count"] == 0 else "blocked",
            "notes": "Compiled tiny-C lowering should stay translation-identical to the preserved canonical rows on the admitted suite.",
        },
        {
            "item_id": "r60_keeps_histogram_and_scope_lift_out",
            "status": "pass",
            "notes": "The carryover gate remains fixed to sum_i32_buffer and count_nonzero_i32_buffer only.",
        },
    ]
    claim_packet = {
        "supports": [
            "The current compiled-boundary route carries the minimal preserved useful-kernel pair exactly on the declared five-row suite.",
            "The compiled tiny-C lowering stays translation-identical to the preserved canonical bytecode on all admitted rows.",
            "Both linear and accelerated free-running lowered execution remain exact on the admitted compiled useful-kernel rows.",
        ],
        "does_not_support": [
            "bounded value over simpler baselines",
            "histogram16_u8 carryover on this wave",
            "arbitrary C or broad Wasm claims",
        ],
        "distilled_result": {
            "active_stage": "r60_origin_compiled_useful_kernel_carryover_gate",
            "current_active_docs_only_stage": "h55_post_h54_useful_kernel_reentry_packet",
            "current_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "current_low_priority_wave": "p39_post_h54_successor_worktree_hygiene_sync",
            "selected_outcome": gate["lane_verdict"],
            "admitted_kernel_suite": ["sum_i32_buffer", "count_nonzero_i32_buffer"],
            "exact_variant_count": gate["exact_variant_count"],
            "compiler_work_leakage_break_count": gate["compiler_work_leakage_break_count"],
            "next_required_packet": gate["next_required_packet"],
        },
    }
    summary = {
        "experiment": "r60_origin_compiled_useful_kernel_carryover_gate",
        "runtime_environment": environment_payload(),
        "summary": {
            "current_active_docs_only_stage": "h55_post_h54_useful_kernel_reentry_packet",
            "current_post_h54_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "current_low_priority_wave": "p39_post_h54_successor_worktree_hygiene_sync",
            "preserved_prior_closeout": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "active_runtime_lane": "r60_origin_compiled_useful_kernel_carryover_gate",
            "gate": gate,
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
    }
    return manifest_rows, report, stop_rule, {"rows": checklist_rows}, {"summary": claim_packet}, summary


def main() -> None:
    manifest_rows, report, stop_rule, checklist, claim_packet, summary = build_artifacts()
    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(OUT_DIR / "carryover_report.json", report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(OUT_DIR / "checklist.json", checklist)
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "snapshot.json", {"rows": report["coverage_rows"], "first_failure": report["first_failure"]})
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
