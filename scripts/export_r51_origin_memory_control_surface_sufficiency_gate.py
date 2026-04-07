"""Export the post-H49 memory/control surface sufficiency gate for R51."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from bytecode import (
    BytecodeInterpreter,
    BytecodeMemoryRegion,
    BytecodeOpcode,
    BytecodeProgram,
    BytecodeType,
    first_divergence_step,
    lower_program,
    normalize_event,
    normalize_final_state,
    r51_origin_memory_control_surface_sufficiency_cases,
    run_spec_program,
    serialize_restricted_tinyc_program,
    validate_program_contract,
    validate_surface_literals,
    verify_program,
)
from exec_trace import TraceInterpreter
from model import (
    FreeRunningExecutionResult,
    compare_execution_to_reference,
    run_free_running_exact,
    run_latest_write_decode_for_call_events,
    run_latest_write_decode_for_events,
    run_latest_write_decode_for_stack_events,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R51_origin_memory_control_surface_sufficiency_gate"


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


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


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


def declared_memory_snapshot(program: BytecodeProgram, state: object) -> dict[str, int]:
    _, _, memory, _, _, _ = normalize_final_state(state)
    memory_map = {int(address): int(value) for address, value in memory}
    return {
        cell.label: memory_map.get(cell.address, 0)
        for cell in sorted(program.memory_layout, key=lambda item: item.address)
    }


def reference_wrapper(program: Any, result: Any) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def validate_r51_scope(program: BytecodeProgram) -> tuple[bool, str | None]:
    opcodes = {instruction.opcode for instruction in program.instructions}
    if not opcodes.issubset(ALLOWED_OPCODES):
        return False, "opcode_out_of_scope"
    if any(cell.region == BytecodeMemoryRegion.HEAP for cell in program.memory_layout):
        return False, "heap_region_not_admitted"
    return True, None


def max_call_depth(events: tuple[Any, ...]) -> int:
    depth = 0
    best = 0
    for event in events:
        if str(event.opcode) == "call":
            depth += 1
            best = max(best, depth)
        elif str(event.opcode) == "ret":
            depth = max(0, depth - 1)
    return best


def build_identity_space_report(events: tuple[Any, ...], *, space: str) -> dict[str, object]:
    try:
        if space == "memory":
            decode_run = run_latest_write_decode_for_events(events)
        elif space == "stack":
            decode_run = run_latest_write_decode_for_stack_events(events)
        elif space == "call":
            decode_run = run_latest_write_decode_for_call_events(events)
        else:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported logical space: {space}")
    except ValueError:
        return {
            "space": space,
            "candidate_row_count": 0,
            "read_count": 0,
            "identity_passed": True,
            "first_failure": None,
        }

    first_failure: dict[str, object] | None = None
    for observation in decode_run.observations:
        if observation.linear_maximizer_indices != observation.accelerated_maximizer_indices:
            first_failure = {
                "read_step": observation.step,
                "query_address": observation.address,
                "expected_indices": list(observation.linear_maximizer_indices),
                "actual_indices": list(observation.accelerated_maximizer_indices),
                "expected_value": observation.linear_value,
                "actual_value": observation.accelerated_value,
            }
            break

    return {
        "space": space,
        "candidate_row_count": len(decode_run.candidate_rows),
        "read_count": len(decode_run.observations),
        "identity_passed": first_failure is None,
        "first_failure": first_failure,
    }


def build_identity_report(events: tuple[Any, ...]) -> dict[str, object]:
    space_rows = [
        build_identity_space_report(events, space="memory"),
        build_identity_space_report(events, space="stack"),
        build_identity_space_report(events, space="call"),
    ]
    first_failure = next((row["first_failure"] | {"space": row["space"]} for row in space_rows if row["first_failure"] is not None), None)
    return {
        "spaces": space_rows,
        "maximizer_identity_passed": all(bool(row["identity_passed"]) for row in space_rows),
        "first_failure": first_failure,
    }


def budget_metrics(
    *,
    program: BytecodeProgram,
    compiled_result: Any,
    free_running_result: FreeRunningExecutionResult,
    identity_report: dict[str, object],
) -> dict[str, object]:
    program_steps = int(compiled_result.final_state.steps)
    query_budget = len(free_running_result.read_observations)
    candidate_row_count = sum(int(row["candidate_row_count"]) for row in identity_report["spaces"])
    declared_memory_cell_count = len(program.memory_layout)
    typed_address_cell_count = sum(int(cell.cell_type == BytecodeType.ADDR) for cell in program.memory_layout)
    reads_per_step = query_budget / max(program_steps, 1)
    candidate_rows_per_step = candidate_row_count / max(program_steps, 1)
    budget_explosion = reads_per_step > 4.0 or candidate_rows_per_step > 6.0
    return {
        "query_budget": query_budget,
        "candidate_row_count": candidate_row_count,
        "declared_memory_cell_count": declared_memory_cell_count,
        "typed_address_cell_count": typed_address_cell_count,
        "annotation_budget": declared_memory_cell_count + typed_address_cell_count,
        "reads_per_step": reads_per_step,
        "candidate_rows_per_step": candidate_rows_per_step,
        "budget_explosion": budget_explosion,
    }


def failure_class(row: dict[str, object]) -> str | None:
    if not row["scope_passed"]:
        return "surface_scope_break"
    if not row["verifier_passed"]:
        return "verifier_break"
    if not row["spec_contract_passed"]:
        return "spec_contract_break"
    if not row["surface_literal_passed"]:
        return "surface_literal_break"
    if not row["compiled_spec_trace_match"] or not row["compiled_spec_final_state_match"]:
        return "compiled_reference_break"
    if not row["compiled_to_lowered_trace_match"] or not row["compiled_to_lowered_final_state_match"]:
        return "lowering_break"
    if not row["free_running_trace_match"] or not row["free_running_final_state_match"]:
        return "exactness_break"
    if not row["maximizer_identity_passed"]:
        return "maximizer_identity_break"
    if row["budget_explosion"]:
        return "budget_explosion"
    return None


def main() -> None:
    r51_readme_text = read_text(
        ROOT / "docs" / "milestones" / "R51_origin_memory_control_surface_sufficiency_gate" / "README.md"
    )
    execution_manifest_text = read_text(
        ROOT / "docs" / "milestones" / "R51_origin_memory_control_surface_sufficiency_gate" / "execution_manifest.md"
    )
    case_matrix_text = read_text(
        ROOT / "docs" / "milestones" / "R51_origin_memory_control_surface_sufficiency_gate" / "case_matrix.md"
    )
    stop_conditions_text = read_text(
        ROOT / "docs" / "milestones" / "R51_origin_memory_control_surface_sufficiency_gate" / "stop_conditions.md"
    )
    f26_readme_text = read_text(
        ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "README.md"
    )
    route_constraints_text = read_text(
        ROOT / "docs" / "milestones" / "F26_post_h49_origin_claim_delta_and_next_question_bundle" / "route_constraints.md"
    )
    current_stage_driver_text = read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md")

    h49_summary = json.loads(
        (ROOT / "results" / "H49_post_r50_tinyc_lowering_decision_packet" / "summary.json").read_text(encoding="utf-8")
    )["summary"]
    r50_summary = json.loads(
        (ROOT / "results" / "R50_origin_restricted_tinyc_lowering_gate" / "summary.json").read_text(encoding="utf-8")
    )["summary"]["gate"]

    cases = r51_origin_memory_control_surface_sufficiency_cases()
    manifest_rows = [
        {
            "case_order": index + 1,
            "family_id": case.family_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "max_steps": case.max_steps,
            "program_name": case.program.name,
            "source_kind": "restricted_tinyc" if case.tinyc_program is not None else "bytecode",
        }
        for index, case in enumerate(cases)
    ]

    exactness_rows: list[dict[str, object]] = []
    cost_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for case in cases:
        scope_passed, scope_error = validate_r51_scope(case.program)
        verifier_result = verify_program(case.program)
        spec_contract = validate_program_contract(case.program)
        surface_literal = validate_surface_literals(case.program)
        spec_result = run_spec_program(case.program, max_steps=case.max_steps)
        compiled_result = BytecodeInterpreter().run(case.program, max_steps=case.max_steps)
        lowered_program = lower_program(case.program)
        lowered_result = TraceInterpreter().run(lowered_program, max_steps=case.max_steps)
        max_steps = max(case.max_steps, compiled_result.final_state.steps + 8)
        free_running_result = run_free_running_exact(lowered_program, decode_mode="accelerated", max_steps=max_steps)
        free_running_outcome = compare_execution_to_reference(
            lowered_program,
            free_running_result,
            reference=reference_wrapper(lowered_program, lowered_result),
        )

        read_counter = Counter(observation.space for observation in free_running_result.read_observations)
        compiled_spec_trace_match = tuple(normalize_event(event) for event in spec_result.events) == tuple(
            normalize_event(event) for event in compiled_result.events
        )
        compiled_spec_final_state_match = normalize_final_state(spec_result.final_state) == normalize_final_state(
            compiled_result.final_state
        )
        compiled_to_lowered_trace_match = tuple(compiled_result.events) == tuple(lowered_result.events)
        compiled_to_lowered_final_state_match = compiled_result.final_state == lowered_result.final_state

        identity_report = build_identity_report(free_running_result.events)
        budgets = budget_metrics(
            program=case.program,
            compiled_result=compiled_result,
            free_running_result=free_running_result,
            identity_report=identity_report,
        )
        memory_read_event_count = sum(int(event.memory_read_address is not None) for event in compiled_result.events)
        memory_write_event_count = sum(int(event.memory_write is not None) for event in compiled_result.events)
        branch_event_count = sum(int(event.branch_taken is not None) for event in compiled_result.events)
        max_stack_depth = max((int(event.stack_depth_after) for event in compiled_result.events), default=0)

        exactness_row = {
            "family_id": case.family_id,
            "variant_id": case.variant_id,
            "description": case.description,
            "axis_tags": list(case.axis_tags),
            "comparison_mode": case.comparison_mode,
            "executed": True,
            "scope_passed": scope_passed,
            "scope_error_class": scope_error,
            "verifier_passed": verifier_result.passed,
            "verifier_error_class": verifier_result.error_class,
            "spec_contract_passed": spec_contract.passed,
            "spec_contract_error_class": spec_contract.error_class,
            "surface_literal_passed": surface_literal.passed,
            "surface_literal_error_class": surface_literal.error_class,
            "compiled_spec_trace_match": compiled_spec_trace_match,
            "compiled_spec_final_state_match": compiled_spec_final_state_match,
            "compiled_spec_first_mismatch_step": first_divergence_step(spec_result.events, compiled_result.events),
            "compiled_to_lowered_trace_match": compiled_to_lowered_trace_match,
            "compiled_to_lowered_final_state_match": compiled_to_lowered_final_state_match,
            "compiled_to_lowered_first_mismatch_step": first_divergence_step(compiled_result.events, lowered_result.events),
            "free_running_trace_match": free_running_outcome.exact_trace_match,
            "free_running_final_state_match": free_running_outcome.exact_final_state_match,
            "first_mismatch_step": free_running_outcome.first_mismatch_step,
            "failure_reason": free_running_outcome.failure_reason,
            "maximizer_identity_passed": identity_report["maximizer_identity_passed"],
            "identity_report": identity_report,
            "budget_explosion": budgets["budget_explosion"],
            "budget_metrics": budgets,
            "compiled_final_state": normalize_state_dict(compiled_result.final_state),
            "lowered_final_state": normalize_state_dict(lowered_result.final_state),
            "free_running_final_state": normalize_state_dict(free_running_result.final_state),
            "compiled_declared_memory": declared_memory_snapshot(case.program, compiled_result.final_state),
            "free_running_declared_memory": declared_memory_snapshot(case.program, free_running_result.final_state),
            "compiled_program": serialize_bytecode_program(case.program),
            "lowered_program": serialize_trace_program(lowered_program),
            "tinyc_program": serialize_restricted_tinyc_program(case.tinyc_program) if case.tinyc_program is not None else None,
        }
        stop_class = failure_class(exactness_row)
        exactness_row["stop_class"] = stop_class
        exactness_row["verdict"] = "exact" if stop_class is None else "break"
        exactness_rows.append(exactness_row)

        cost_rows.append(
            {
                "family_id": case.family_id,
                "variant_id": case.variant_id,
                "instruction_count": len(case.program.instructions),
                "program_steps": compiled_result.final_state.steps,
                "memory_read_event_count": memory_read_event_count,
                "memory_write_event_count": memory_write_event_count,
                "branch_event_count": branch_event_count,
                "free_running_read_count": len(free_running_result.read_observations),
                "free_running_stack_read_count": read_counter.get("stack", 0),
                "free_running_memory_read_count": read_counter.get("memory", 0),
                "free_running_call_read_count": read_counter.get("call", 0),
                "declared_memory_cell_count": len(case.program.memory_layout),
                "typed_address_cell_count": budgets["typed_address_cell_count"],
                "annotation_budget": budgets["annotation_budget"],
                "reads_per_step": budgets["reads_per_step"],
                "candidate_rows_per_step": budgets["candidate_rows_per_step"],
                "max_stack_depth": max_stack_depth,
                "max_call_depth": max_call_depth(compiled_result.events),
                "opcode_surface": opcode_surface(case.program),
            }
        )

        if first_failure is None and stop_class is not None:
            first_failure = {
                "family_id": case.family_id,
                "variant_id": case.variant_id,
                "stop_class": stop_class,
                "first_mismatch_step": exactness_row["first_mismatch_step"],
                "failure_reason": exactness_row["failure_reason"],
                "identity_failure": identity_report["first_failure"],
            }

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in exactness_rows:
        grouped[str(row["family_id"])].append(row)

    family_rollup_rows: list[dict[str, object]] = []
    for family_id in sorted(grouped):
        rows = grouped[family_id]
        family_rollup_rows.append(
            {
                "family_id": family_id,
                "planned_case_count": len(rows),
                "exact_case_count": sum(int(row["stop_class"] is None) for row in rows),
                "all_cases_exact": all(row["stop_class"] is None for row in rows),
                "identity_exact_case_count": sum(int(bool(row["maximizer_identity_passed"])) for row in rows),
                "budget_clean_case_count": sum(int(not bool(row["budget_explosion"])) for row in rows),
                "first_failure": next((row["stop_class"] for row in rows if row["stop_class"] is not None), None),
            }
        )

    exact_case_count = sum(int(row["stop_class"] is None) for row in exactness_rows)
    lane_passed = exact_case_count == len(exactness_rows)
    next_required_packet = (
        "r52_origin_internal_vs_external_executor_value_gate"
        if lane_passed
        else "h50_post_r51_r52_scope_decision_packet"
    )
    lane_verdict = "memory_control_surface_supported_narrowly" if lane_passed else "memory_control_surface_break"

    checklist_rows = [
        {
            "item_id": "r51_docs_define_mandatory_memory_control_families",
            "status": "pass"
            if contains_all(
                r51_readme_text,
                [
                    "only next runtime candidate after `h49`",
                    "append-only exact substrate remains sufficient",
                ],
            )
            and contains_all(
                execution_manifest_text,
                [
                    "keep exact source/interpreter, lowered replay/reference, and accelerated exact executor visible separately",
                    "do not add hidden helper state to \"make the lane pass\"",
                ],
            )
            and contains_all(
                case_matrix_text,
                [
                    "latest-write overwrite-after-gap",
                    "stack-relative read under deeper control",
                    "loop-carried state",
                    "nested call/return",
                    "bounded multi-step static-memory lowered row",
                ],
            )
            and contains_all(
                stop_conditions_text,
                [
                    "maximizer-row identity breaks",
                    "hidden mutable side state becomes necessary",
                    "annotation/query/head budget explodes",
                ],
            )
            else "blocked",
            "notes": "R51 docs should keep the mandatory family set and hard stop conditions explicit.",
        },
        {
            "item_id": "upstream_h49_f26_fix_r51_as_only_next_runtime_candidate",
            "status": "pass"
            if str(h49_summary["active_stage"]) == "h49_post_r50_tinyc_lowering_decision_packet"
            and str(h49_summary["selected_outcome"]) == "freeze_r50_as_narrow_exact_tinyc_support_only"
            and str(r50_summary["lane_verdict"]) == "restricted_tinyc_lowering_supported_narrowly"
            and contains_all(
                f26_readme_text,
                [
                    "`r51_origin_memory_control_surface_sufficiency_gate` as the only next runtime candidate",
                    "`r52_origin_internal_vs_external_executor_value_gate` as the only later comparator/value gate",
                ],
            )
            and contains_all(
                route_constraints_text,
                [
                    "`r51` is the only next runtime candidate fixed here",
                    "`h50` is the only follow-up packet fixed here",
                ],
            )
            and contains_all(
                current_stage_driver_text,
                [
                    "the only next runtime candidate fixed by `f26` is:",
                    "- `r51_origin_memory_control_surface_sufficiency_gate`",
                ],
            )
            else "blocked",
            "notes": "R51 must remain the only post-H49 runtime lane authorized by H49/F26.",
        },
        {
            "item_id": "r51_runtime_rows_stay_exact_without_identity_or_budget_break",
            "status": "pass"
            if lane_passed
            and len(exactness_rows) == 5
            and len(family_rollup_rows) == 5
            and all(row["maximizer_identity_passed"] for row in exactness_rows)
            and all(not row["budget_explosion"] for row in exactness_rows)
            else "blocked",
            "notes": "All five mandatory R51 rows should stay exact and keep identity/budget guardrails intact.",
        },
    ]

    summary_payload = {
        "experiment": "r51_origin_memory_control_surface_sufficiency_gate",
        "environment": environment_payload(),
        "summary": {
            "current_active_docs_only_stage": "h49_post_r50_tinyc_lowering_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_post_h49_planning_bundle": "f26_post_h49_origin_claim_delta_and_next_question_bundle",
            "current_low_priority_wave": "p36_post_h49_cleanline_hygiene_and_artifact_policy",
            "active_runtime_lane": "r51_origin_memory_control_surface_sufficiency_gate",
            "preserved_prior_runtime_gate": "r50_origin_restricted_tinyc_lowering_gate",
            "gate": {
                "lane_verdict": lane_verdict,
                "planned_case_count": len(manifest_rows),
                "executed_case_count": len(exactness_rows),
                "exact_case_count": exact_case_count,
                "failed_case_count": len(exactness_rows) - exact_case_count,
                "planned_family_count": len(family_rollup_rows),
                "exact_family_count": sum(int(row["all_cases_exact"]) for row in family_rollup_rows),
                "maximizer_identity_exact_count": sum(int(bool(row["maximizer_identity_passed"])) for row in exactness_rows),
                "budget_clean_case_count": sum(int(not bool(row["budget_explosion"])) for row in exactness_rows),
                "claim_ceiling": "bounded_exact_memory_control_surface_only",
                "next_required_packet": next_required_packet,
                "first_failure": first_failure,
            },
            "pass_count": sum(1 for row in checklist_rows if row["status"] == "pass"),
            "blocked_count": sum(1 for row in checklist_rows if row["status"] != "pass"),
        },
    }

    claim_packet = {
        "experiment": "r51_origin_memory_control_surface_sufficiency_gate",
        "supports": [
            "the current append-only exact substrate survives five predeclared memory/control families without widening"
            if lane_passed
            else "the current append-only exact substrate does not survive the full predeclared R51 family set",
            "maximizer-row identity remains aligned with exact hard-max retrieval" if lane_passed else "maximizer-row identity or exactness broke on at least one R51 row",
        ],
        "does_not_support": [
            "arbitrary C support",
            "broader Wasm or unrestricted compiler scope",
            "trainable or transformed executor entry by momentum alone",
        ],
        "next_required_packet": next_required_packet,
        "stop_conditions": [
            "exactness break on a mandatory row",
            "maximizer-row identity break",
            "hidden mutable side state requirement",
            "budget explosion",
        ],
    }

    snapshot = {
        "manifest_rows": manifest_rows,
        "exactness_rows": exactness_rows,
        "cost_rows": cost_rows,
        "family_rollup_rows": family_rollup_rows,
    }

    stop_rule = {
        "experiment": "r51_origin_memory_control_surface_sufficiency_gate",
        "stop_rule_triggered": not lane_passed,
        "first_failure": first_failure,
        "next_required_packet": next_required_packet,
    }

    write_json(OUT_DIR / "summary.json", summary_payload)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "case_manifest.json", {"rows": manifest_rows})
    write_json(
        OUT_DIR / "execution_report.json",
        {
            "exactness_rows": exactness_rows,
            "cost_rows": cost_rows,
            "family_rollup_rows": family_rollup_rows,
        },
    )
    write_json(OUT_DIR / "stop_rule.json", stop_rule)


if __name__ == "__main__":
    main()
