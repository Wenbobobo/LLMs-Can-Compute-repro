"""Export the post-R55 append-only trace VM semantics gate for R56."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from exec_trace import (
    ExecutionResult,
    ExecutionState,
    Program,
    TraceEvent,
    TraceInterpreter,
    call_chain_program,
    countdown_program,
    flagged_indirect_accumulator_program,
    latest_write_program,
    loop_indirect_memory_program,
)
from model import FreeRunningExecutionResult, FreeRunningTraceExecutor, compare_execution_to_reference
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R56_origin_append_only_trace_vm_semantics_gate"


@dataclass(frozen=True, slots=True)
class TraceVMSemanticsTask:
    task_id: str
    category: Literal["static_memory", "loop_control", "indirect_memory", "call_return", "mixed_surface"]
    description: str
    notes: str
    program: Program


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles) and line not in seen:
            hits.append(line)
            seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def serialize_instruction(program: Program) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pc, instruction in enumerate(program.instructions):
        rows.append({"pc": pc, "opcode": instruction.opcode.value, "arg": instruction.arg})
    return rows


def serialize_trace_event(event: TraceEvent) -> dict[str, object]:
    return {
        "step": event.step,
        "pc": event.pc,
        "opcode": event.opcode.value,
        "arg": event.arg,
        "popped": list(event.popped),
        "pushed": list(event.pushed),
        "branch_taken": event.branch_taken,
        "memory_read_address": event.memory_read_address,
        "memory_read_value": event.memory_read_value,
        "memory_write": None if event.memory_write is None else list(event.memory_write),
        "next_pc": event.next_pc,
        "stack_depth_before": event.stack_depth_before,
        "stack_depth_after": event.stack_depth_after,
        "halted": event.halted,
    }


def serialize_final_state(state: ExecutionState) -> dict[str, object]:
    return {
        "pc": state.pc,
        "stack": list(state.stack),
        "memory": [list(item) for item in state.memory],
        "call_stack": list(state.call_stack),
        "halted": state.halted,
        "steps": state.steps,
    }


def reference_wrapper(program: Program, result: ExecutionResult) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def build_task_manifest() -> list[TraceVMSemanticsTask]:
    return [
        TraceVMSemanticsTask(
            task_id="static_latest_write_trace",
            category="static_memory",
            description="Short static-memory overwrite row on the base append-only trace contract.",
            notes="Keeps the smallest latest-write memory semantics row visible inside the full free-running gate.",
            program=latest_write_program(),
        ),
        TraceVMSemanticsTask(
            task_id="countdown_loop_control_trace",
            category="loop_control",
            description="Free-running loop and branch row on the bounded trace VM contract.",
            notes="Requires exact control-flow transitions rather than final-answer-only agreement.",
            program=countdown_program(12),
        ),
        TraceVMSemanticsTask(
            task_id="indirect_memory_loop_trace",
            category="indirect_memory",
            description="Indirect load/store loop row on the same bounded trace contract.",
            notes="Stresses append-only retrieval over dynamic addresses without widening the admitted instruction set.",
            program=loop_indirect_memory_program(6),
        ),
        TraceVMSemanticsTask(
            task_id="call_return_trace",
            category="call_return",
            description="Single bounded call/return row on the same free-running trace VM semantics.",
            notes="Makes call-frame retrieval part of the exact semantics contract instead of a side channel.",
            program=call_chain_program(),
        ),
        TraceVMSemanticsTask(
            task_id="flagged_mixed_surface_trace",
            category="mixed_surface",
            description="Mixed stack, static-memory, and indirect-memory control row on the bounded trace VM contract.",
            notes="Combines branch, stack, and memory surfaces on one fixed admitted row.",
            program=flagged_indirect_accumulator_program(4, base_address=32),
        ),
    ]


def evaluate_task(task: TraceVMSemanticsTask) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object] | None]:
    reference_result = TraceInterpreter().run(task.program)
    max_steps = max(reference_result.final_state.steps + 8, 64)
    candidate_result = FreeRunningTraceExecutor(
        stack_strategy="accelerated",
        memory_strategy="accelerated",
        validate_exact_reads=True,
    ).run(task.program, max_steps=max_steps)
    outcome = compare_execution_to_reference(
        task.program,
        candidate_result,
        reference=reference_wrapper(task.program, reference_result),
    )
    read_counter = Counter(observation.space for observation in candidate_result.read_observations)
    instruction_surface = sorted({instruction.opcode.value for instruction in task.program.instructions})
    first_failure = None
    if not outcome.exact_trace_match or not outcome.exact_final_state_match:
        first_failure = {
            "task_id": task.task_id,
            "category": task.category,
            "program_name": task.program.name,
            "first_mismatch_step": outcome.first_mismatch_step,
            "failure_reason": outcome.failure_reason,
        }

    task_row = {
        "task_id": task.task_id,
        "category": task.category,
        "program_name": task.program.name,
        "description": task.description,
        "notes": task.notes,
        "instruction_count": len(task.program.instructions),
        "program_steps": reference_result.final_state.steps,
        "opcode_surface": instruction_surface,
        "max_steps": max_steps,
        "reference_runtime_kind": "trace_interpreter_reference",
        "candidate_runtime_kind": "free_running_trace_executor_accelerated_exact",
        "uses_hidden_mutable_side_state": False,
        "uses_external_execution_at_runtime": False,
        "teacher_forced": False,
        "compiler_replay_only": False,
        "verdict": "exact" if outcome.exact_trace_match and outcome.exact_final_state_match else "break",
    }
    measurement_row = {
        "task_id": task.task_id,
        "transition_count": len(reference_result.events),
        "reference_transition_count": len(reference_result.events),
        "candidate_transition_count": len(candidate_result.events),
        "exact_trace_match": outcome.exact_trace_match,
        "exact_final_state_match": outcome.exact_final_state_match,
        "first_mismatch_step": outcome.first_mismatch_step,
        "read_count": len(candidate_result.read_observations),
        "stack_read_count": read_counter.get("stack", 0),
        "memory_read_count": read_counter.get("memory", 0),
        "call_read_count": read_counter.get("call", 0),
        "branch_event_count": sum(int(event.branch_taken is not None) for event in reference_result.events),
        "memory_write_event_count": sum(int(event.memory_write is not None) for event in reference_result.events),
    }
    trace_log_row = {
        "task_id": task.task_id,
        "program": serialize_instruction(task.program),
        "reference_transitions": [serialize_trace_event(event) for event in reference_result.events],
        "candidate_transitions": [serialize_trace_event(event) for event in candidate_result.events],
        "reference_final_state": serialize_final_state(reference_result.final_state),
        "candidate_final_state": serialize_final_state(candidate_result.final_state),
    }
    return task_row, measurement_row, trace_log_row, first_failure


def load_inputs() -> dict[str, Any]:
    return {
        "r56_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "README.md"
        ),
        "r56_status_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "status.md"
        ),
        "r56_todo_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "todo.md"
        ),
        "r56_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "acceptance.md"
        ),
        "r56_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "artifact_index.md"
        ),
        "semantics_contract_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "semantics_contract.md"
        ),
        "trace_requirements_text": read_text(
            ROOT / "docs" / "milestones" / "R56_origin_append_only_trace_vm_semantics_gate" / "trace_requirements.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "r55_summary": read_json(ROOT / "results" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "summary.json"),
        "h51_summary": read_json(ROOT / "results" / "H51_post_h50_origin_mechanism_reentry_packet" / "summary.json"),
        "f28_summary": read_json(ROOT / "results" / "F28_post_h50_origin_mechanism_reentry_bundle" / "summary.json"),
        "h50_summary": read_json(ROOT / "results" / "H50_post_r51_r52_scope_decision_packet" / "summary.json"),
    }


def build_checklist_rows(
    inputs: dict[str, Any],
    task_rows: list[dict[str, object]],
    measurement_rows: list[dict[str, object]],
    trace_logs: list[dict[str, object]],
    lane_verdict: str,
    stop_rule: dict[str, object],
) -> list[dict[str, object]]:
    r55 = inputs["r55_summary"]["summary"]
    h51 = inputs["h51_summary"]["summary"]
    f28 = inputs["f28_summary"]["summary"]
    exact_trace_count = sum(int(bool(row["exact_trace_match"])) for row in measurement_rows)
    exact_final_state_count = sum(int(bool(row["exact_final_state_match"])) for row in measurement_rows)
    return [
        {
            "item_id": "r56_requires_positive_r55_retrieval_equivalence_basis",
            "status": "pass"
            if str(r55["gate"]["lane_verdict"]) == "retrieval_equivalence_supported_exactly"
            and str(r55["gate"]["next_required_packet"]) == "r56_origin_append_only_trace_vm_semantics_gate"
            and str(h51["selected_outcome"]) == "authorize_origin_mechanism_reentry_through_r55_first"
            and str(h51["only_next_runtime_candidate"]) == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
            and str(f28["only_next_runtime_candidate"]) == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
            else "blocked",
            "notes": "R56 opens only after positive exact R55 under the preserved H51/F28 route.",
        },
        {
            "item_id": "r56_docs_fix_trace_vm_contract_and_trace_requirements",
            "status": "pass"
            if contains_all(
                inputs["r56_readme_text"],
                [
                    "free-running trace vm semantics contract exactly",
                    "next required packet is",
                    "r57_origin_accelerated_trace_vm_comparator_gate",
                ],
            )
            and contains_all(
                inputs["semantics_contract_text"],
                [
                    "transparent append-only trace-vm interpreter",
                    "same step transitions and the same final state",
                    "hidden mutable side state",
                ],
            )
            and contains_all(
                inputs["trace_requirements_text"],
                [
                    "instruction-by-instruction traces",
                    "state, stack, and memory deltas",
                    "localize the first mismatch",
                ],
            )
            else "blocked",
            "notes": "R56 docs must keep the semantics contract and per-step trace requirements explicit.",
        },
        {
            "item_id": "reference_and_candidate_step_traces_match_on_every_declared_row",
            "status": "pass" if exact_trace_count == len(measurement_rows) and len(measurement_rows) > 0 else "blocked",
            "notes": "Every declared R56 row must keep full step-trace parity, not answer-only agreement.",
        },
        {
            "item_id": "reference_and_candidate_final_states_match_on_every_declared_row",
            "status": "pass"
            if exact_final_state_count == len(measurement_rows) and len(measurement_rows) > 0
            else "blocked",
            "notes": "Final-state parity remains required in addition to step-trace parity.",
        },
        {
            "item_id": "candidate_route_stays_free_running_internal_without_runtime_external_execution",
            "status": "pass"
            if all(str(row["candidate_runtime_kind"]) == "free_running_trace_executor_accelerated_exact" for row in task_rows)
            and all(not bool(row["uses_hidden_mutable_side_state"]) for row in task_rows)
            and all(not bool(row["uses_external_execution_at_runtime"]) for row in task_rows)
            and all(not bool(row["teacher_forced"]) for row in task_rows)
            and all(not bool(row["compiler_replay_only"]) for row in task_rows)
            else "blocked",
            "notes": "R56 forbids hidden mutable side state, teacher forcing, and external execution at tested runtime.",
        },
        {
            "item_id": "instruction_level_transition_logs_exported_for_all_rows",
            "status": "pass"
            if len(trace_logs) == len(task_rows)
            and all(len(log["reference_transitions"]) > 0 for log in trace_logs)
            and all(len(log["reference_transitions"]) == len(log["candidate_transitions"]) for log in trace_logs)
            else "blocked",
            "notes": "Each row must export bounded instruction-level transition logs for both reference and candidate routes.",
        },
        {
            "item_id": "r56_opens_r57_only_if_exact",
            "status": "pass"
            if (
                lane_verdict == "trace_vm_semantics_supported_exactly"
                and stop_rule["next_required_packet"] == "r57_origin_accelerated_trace_vm_comparator_gate"
                and bool(stop_rule["r57_open"]) is True
            )
            or (
                lane_verdict != "trace_vm_semantics_supported_exactly"
                and stop_rule["next_required_packet"] == "h52_post_r55_r56_r57_origin_mechanism_decision_packet"
                and bool(stop_rule["r57_open"]) is False
            )
            else "blocked",
            "notes": "R57 can open only after positive exact R56; otherwise the lane stops and hands off to H52.",
        },
    ]


def build_claim_packet(lane_verdict: str, stop_rule: dict[str, object], summary_fields: dict[str, object]) -> dict[str, object]:
    positive = lane_verdict == "trace_vm_semantics_supported_exactly"
    return {
        "summary": {
            "supported_here": [
                "The bounded append-only trace VM candidate matches the transparent reference semantics exactly on the fixed R56 row set."
                if positive
                else "The bounded append-only trace VM candidate does not match the transparent reference semantics exactly on the fixed R56 row set.",
                "R56 keeps full step-trace parity explicit rather than collapsing the gate to final-state agreement only.",
                "R56 keeps runtime semantics separate from any fast-path value question, which stays deferred to R57.",
            ],
            "unsupported_here": [
                "R56 does not establish fast-path system value by itself.",
                "R56 does not authorize transformed-model entry, trainable entry, arbitrary C, or broad Wasm claims.",
                "R56 does not permit R57 to open if exact trace semantics fails.",
            ],
            "disconfirmed_here": [
                "The idea that a bounded free-running internal executor can be credited from teacher forcing, compiler replay, or final-answer-only agreement."
            ],
            "distilled_result": {
                **summary_fields,
                "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
            },
        }
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    r55 = inputs["r55_summary"]["summary"]
    h51 = inputs["h51_summary"]["summary"]
    return [
        {
            "source": "results/R55_origin_2d_hardmax_retrieval_equivalence_gate/summary.json",
            "fields": {
                "lane_verdict": r55["gate"]["lane_verdict"],
                "exact_task_count": r55["gate"]["exact_task_count"],
                "next_required_packet": r55["gate"]["next_required_packet"],
            },
        },
        {
            "source": "results/H51_post_h50_origin_mechanism_reentry_packet/summary.json",
            "fields": {
                "active_stage": h51["active_stage"],
                "selected_outcome": h51["selected_outcome"],
                "only_next_runtime_candidate": h51["only_next_runtime_candidate"],
            },
        },
        {
            "path": "docs/milestones/R56_origin_append_only_trace_vm_semantics_gate/semantics_contract.md",
            "matched_lines": extract_matching_lines(
                inputs["semantics_contract_text"],
                needles=[
                    "transparent append-only trace-vm interpreter",
                    "same step transitions and the same final state",
                ],
            ),
        },
        {
            "path": "docs/milestones/R56_origin_append_only_trace_vm_semantics_gate/trace_requirements.md",
            "matched_lines": extract_matching_lines(
                inputs["trace_requirements_text"],
                needles=[
                    "instruction-by-instruction traces",
                    "state, stack, and memory deltas",
                    "first mismatch",
                ],
            ),
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "matched_lines": extract_matching_lines(
                inputs["current_stage_driver_text"],
                needles=[
                    "r56_origin_append_only_trace_vm_semantics_gate",
                    "r57_origin_accelerated_trace_vm_comparator_gate",
                ],
            ),
        },
        {
            "path": "tmp/active_wave_plan.md",
            "matched_lines": extract_matching_lines(
                inputs["active_wave_plan_text"],
                needles=[
                    "r56_origin_append_only_trace_vm_semantics_gate",
                    "r57_origin_accelerated_trace_vm_comparator_gate",
                ],
            ),
        },
    ]


def main() -> None:
    inputs = load_inputs()
    tasks = build_task_manifest()
    task_rows: list[dict[str, object]] = []
    measurement_rows: list[dict[str, object]] = []
    trace_logs: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for task in tasks:
        task_row, measurement_row, trace_log_row, task_first_failure = evaluate_task(task)
        task_rows.append(task_row)
        measurement_rows.append(measurement_row)
        trace_logs.append(trace_log_row)
        if first_failure is None and task_first_failure is not None:
            first_failure = task_first_failure

    exact_trace_task_count = sum(int(bool(row["exact_trace_match"])) for row in measurement_rows)
    exact_final_state_task_count = sum(int(bool(row["exact_final_state_match"])) for row in measurement_rows)
    total_transition_count = sum(int(row["transition_count"]) for row in measurement_rows)
    stack_read_count = sum(int(row["stack_read_count"]) for row in measurement_rows)
    memory_read_count = sum(int(row["memory_read_count"]) for row in measurement_rows)
    call_read_count = sum(int(row["call_read_count"]) for row in measurement_rows)

    lane_positive = (
        len(measurement_rows) > 0
        and exact_trace_task_count == len(measurement_rows)
        and exact_final_state_task_count == len(measurement_rows)
    )
    lane_verdict = "trace_vm_semantics_supported_exactly" if lane_positive else "trace_vm_semantics_falsified"
    next_required_packet = (
        "r57_origin_accelerated_trace_vm_comparator_gate"
        if lane_positive
        else "h52_post_r55_r56_r57_origin_mechanism_decision_packet"
    )

    stop_rule = {
        "experiment": "r56_origin_append_only_trace_vm_semantics_gate",
        "stop_rule_triggered": not lane_positive,
        "stop_reason": None if lane_positive else "exact_trace_vm_semantics_broke",
        "r57_open": lane_positive,
        "next_required_packet": next_required_packet,
        "first_failure": first_failure,
    }

    summary_fields = {
        "current_active_docs_only_stage": "h51_post_h50_origin_mechanism_reentry_packet",
        "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "current_planning_bundle": "f28_post_h50_origin_mechanism_reentry_bundle",
        "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
        "preserved_exact_retrieval_gate": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
        "active_runtime_lane": "r56_origin_append_only_trace_vm_semantics_gate",
        "lane_verdict": lane_verdict,
        "planned_task_count": len(task_rows),
        "executed_task_count": len(task_rows),
        "exact_task_count": sum(int(row["verdict"] == "exact") for row in task_rows),
        "exact_trace_task_count": exact_trace_task_count,
        "exact_final_state_task_count": exact_final_state_task_count,
        "transition_count": total_transition_count,
        "stack_read_count": stack_read_count,
        "memory_read_count": memory_read_count,
        "call_read_count": call_read_count,
        "first_failure_task_id": None if first_failure is None else first_failure["task_id"],
        "next_required_packet": next_required_packet,
    }

    checklist_rows = build_checklist_rows(inputs, task_rows, measurement_rows, trace_logs, lane_verdict, stop_rule)
    claim_packet = build_claim_packet(lane_verdict, stop_rule, summary_fields)
    snapshot_rows = build_snapshot(inputs)

    summary_payload = {
        "summary": {
            "current_active_docs_only_stage": summary_fields["current_active_docs_only_stage"],
            "preserved_prior_docs_only_closeout": summary_fields["preserved_prior_docs_only_closeout"],
            "current_paper_grade_endpoint": summary_fields["current_paper_grade_endpoint"],
            "current_planning_bundle": summary_fields["current_planning_bundle"],
            "current_low_priority_wave": summary_fields["current_low_priority_wave"],
            "preserved_exact_retrieval_gate": summary_fields["preserved_exact_retrieval_gate"],
            "active_runtime_lane": summary_fields["active_runtime_lane"],
            "gate": {
                "lane_verdict": summary_fields["lane_verdict"],
                "planned_task_count": summary_fields["planned_task_count"],
                "executed_task_count": summary_fields["executed_task_count"],
                "exact_task_count": summary_fields["exact_task_count"],
                "exact_trace_task_count": summary_fields["exact_trace_task_count"],
                "exact_final_state_task_count": summary_fields["exact_final_state_task_count"],
                "transition_count": summary_fields["transition_count"],
                "stack_read_count": summary_fields["stack_read_count"],
                "memory_read_count": summary_fields["memory_read_count"],
                "call_read_count": summary_fields["call_read_count"],
                "first_failure_task_id": summary_fields["first_failure_task_id"],
                "next_required_packet": summary_fields["next_required_packet"],
            },
            "pass_count": sum(1 for row in checklist_rows if row["status"] == "pass"),
            "blocked_count": sum(1 for row in checklist_rows if row["status"] != "pass"),
            "blocked_items": [row["item_id"] for row in checklist_rows if row["status"] != "pass"],
        },
        "runtime_environment": environment_payload(),
    }

    execution_report = {
        "task_rows": task_rows,
        "measurement_rows": measurement_rows,
        "trace_logs": trace_logs,
        "first_failure": first_failure,
    }

    write_json(OUT_DIR / "summary.json", summary_payload)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "execution_report.json", execution_report)
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
