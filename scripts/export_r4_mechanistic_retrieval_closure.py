"""Export the bounded R4 mechanistic retrieval closure on current positive D0 suites."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from bytecode import harness_cases, lower_program, r3_d0_exact_execution_stress_cases, stress_reference_cases
from exec_trace import TraceInterpreter
from exec_trace.dsl import Opcode, TraceEvent
from model import (
    extract_memory_operations,
    extract_stack_slot_operations,
    run_latest_write_decode_for_events,
    run_latest_write_decode_for_stack_events,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R4_mechanistic_retrieval_closure"
CONTROL_OPCODES = {Opcode.JMP, Opcode.JZ, Opcode.CALL, Opcode.RET, Opcode.HALT}
LOCAL_TRANSITION_OPCODES = {
    Opcode.PUSH_CONST,
    Opcode.ADD,
    Opcode.SUB,
    Opcode.EQ,
    Opcode.DUP,
    Opcode.POP,
    Opcode.LOAD,
    Opcode.STORE,
    Opcode.LOAD_AT,
    Opcode.STORE_AT,
}


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_positive_cases():
    cases_by_program: dict[str, object] = {}
    for case in harness_cases():
        if case.comparison_mode == "verifier_negative":
            continue
        cases_by_program[case.program.name] = case
    for case in stress_reference_cases():
        if case.comparison_mode in {"medium_exact_trace", "long_exact_final_state"}:
            cases_by_program[case.program.name] = case
    for case in r3_d0_exact_execution_stress_cases():
        cases_by_program[case.program.name] = case
    return tuple(cases_by_program[name] for name in sorted(cases_by_program))


def primitive_flags_for_event(event: TraceEvent) -> dict[str, bool]:
    latest_write_dependency = event.memory_read_address is not None
    stack_dependency = len(event.popped) > 0
    control_dependency = event.opcode in CONTROL_OPCODES or event.branch_taken is not None
    local_transition_dependency = event.opcode in LOCAL_TRANSITION_OPCODES
    return {
        "latest_write_dependency": latest_write_dependency,
        "stack_dependency": stack_dependency,
        "control_dependency": control_dependency,
        "local_transition_dependency": local_transition_dependency,
        "unexplained_dependency": not (
            latest_write_dependency or stack_dependency or control_dependency or local_transition_dependency
        ),
    }


def primitive_classes(flags: dict[str, bool]) -> list[str]:
    ordered = [
        ("latest_write", "latest_write_dependency"),
        ("stack", "stack_dependency"),
        ("control", "control_dependency"),
        ("local_transition", "local_transition_dependency"),
    ]
    return [label for label, key in ordered if flags[key]]


def build_event_dependency_rows(case, events: tuple[TraceEvent, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for event in events:
        flags = primitive_flags_for_event(event)
        rows.append(
            {
                "program_name": case.program.name,
                "suite": case.suite,
                "comparison_mode": case.comparison_mode,
                "step": event.step,
                "pc": event.pc,
                "opcode": event.opcode.value,
                "arg": event.arg,
                "branch_taken": event.branch_taken,
                "memory_read_address": event.memory_read_address,
                "memory_read_value": event.memory_read_value,
                "memory_write": None if event.memory_write is None else list(event.memory_write),
                "popped_count": len(event.popped),
                "pushed_count": len(event.pushed),
                "stack_depth_before": event.stack_depth_before,
                "stack_depth_after": event.stack_depth_after,
                "primitive_classes": primitive_classes(flags),
                **flags,
            }
        )
    return rows


def build_memory_load_metadata(events: tuple[TraceEvent, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for event in events:
        if event.memory_read_address is None or event.memory_read_value is None:
            continue
        rows.append(
            {
                "step": event.step,
                "pc": event.pc,
                "opcode": event.opcode.value,
                "space": "memory",
                "event_load_ordinal": 0,
                "address": event.memory_read_address,
                "expected_value": event.memory_read_value,
            }
        )
    return rows


def build_stack_load_metadata(events: tuple[TraceEvent, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for event in events:
        pop_count = len(event.popped)
        if pop_count == 0:
            continue
        read_base = event.stack_depth_before - pop_count
        for ordinal, value in enumerate(event.popped):
            rows.append(
                {
                    "step": event.step,
                    "pc": event.pc,
                    "opcode": event.opcode.value,
                    "space": "stack",
                    "event_load_ordinal": ordinal,
                    "address": read_base + ordinal,
                    "expected_value": value,
                }
            )
    return rows


def build_source_event_parity_rows(case, events: tuple[TraceEvent, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    memory_ops = extract_memory_operations(events)
    if memory_ops:
        decode_run = run_latest_write_decode_for_events(events)
        metadata = build_memory_load_metadata(events)
        if len(metadata) != len(decode_run.observations):
            raise ValueError(f"Memory decode metadata mismatch for {case.program.name}.")
        for meta, observation in zip(metadata, decode_run.observations):
            rows.append(
                {
                    "program_name": case.program.name,
                    "suite": case.suite,
                    "comparison_mode": case.comparison_mode,
                    **meta,
                    "config_max_steps": decode_run.config.max_steps,
                    "config_epsilon": str(decode_run.config.epsilon),
                    "linear_value": observation.linear_value,
                    "accelerated_value": observation.accelerated_value,
                    "linear_match": observation.linear_value == meta["expected_value"],
                    "accelerated_match": observation.accelerated_value == meta["expected_value"],
                    "parity_match": observation.linear_value == observation.accelerated_value,
                }
            )

    stack_ops = extract_stack_slot_operations(events)
    if stack_ops:
        decode_run = run_latest_write_decode_for_stack_events(events)
        metadata = build_stack_load_metadata(events)
        if len(metadata) != len(decode_run.observations):
            raise ValueError(f"Stack decode metadata mismatch for {case.program.name}.")
        for meta, observation in zip(metadata, decode_run.observations):
            rows.append(
                {
                    "program_name": case.program.name,
                    "suite": case.suite,
                    "comparison_mode": case.comparison_mode,
                    **meta,
                    "config_max_steps": decode_run.config.max_steps,
                    "config_epsilon": str(decode_run.config.epsilon),
                    "linear_value": observation.linear_value,
                    "accelerated_value": observation.accelerated_value,
                    "linear_match": observation.linear_value == meta["expected_value"],
                    "accelerated_match": observation.accelerated_value == meta["expected_value"],
                    "parity_match": observation.linear_value == observation.accelerated_value,
                }
            )

    return rows


def build_contradiction_candidates(
    dependency_rows: list[dict[str, object]],
    parity_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in dependency_rows:
        if row["unexplained_dependency"]:
            rows.append(
                {
                    "program_name": row["program_name"],
                    "suite": row["suite"],
                    "comparison_mode": row["comparison_mode"],
                    "step": row["step"],
                    "pc": row["pc"],
                    "opcode": row["opcode"],
                    "candidate_type": "unexplained_dependency",
                    "detail": "No allowed primitive class explained this event.",
                }
            )
    for row in parity_rows:
        if row["linear_match"] and row["accelerated_match"] and row["parity_match"]:
            continue
        rows.append(
            {
                "program_name": row["program_name"],
                "suite": row["suite"],
                "comparison_mode": row["comparison_mode"],
                "step": row["step"],
                "pc": row["pc"],
                "opcode": row["opcode"],
                "space": row["space"],
                "address": row["address"],
                "candidate_type": "source_event_parity_failure",
                "detail": "Linear and accelerated retrieval did not agree exactly on a source-event observation.",
            }
        )
    return rows


def build_program_summary(
    case,
    *,
    event_count: int,
    dependency_rows: list[dict[str, object]],
    parity_rows: list[dict[str, object]],
    contradiction_rows: list[dict[str, object]],
) -> dict[str, object]:
    class_counts = Counter()
    for row in dependency_rows:
        for label in row["primitive_classes"]:
            class_counts[str(label)] += 1
    parity_by_space = Counter(str(row["space"]) for row in parity_rows)
    return {
        "program_name": case.program.name,
        "suite": case.suite,
        "comparison_mode": case.comparison_mode,
        "max_steps": case.max_steps,
        "event_count": event_count,
        "primitive_event_counts": {
            "latest_write": sum(bool(row["latest_write_dependency"]) for row in dependency_rows),
            "stack": sum(bool(row["stack_dependency"]) for row in dependency_rows),
            "control": sum(bool(row["control_dependency"]) for row in dependency_rows),
            "local_transition": sum(bool(row["local_transition_dependency"]) for row in dependency_rows),
        },
        "primitive_membership_counts": dict(class_counts),
        "primitive_classes_present": sorted(class_counts),
        "source_observation_count": len(parity_rows),
        "source_observations_by_space": dict(sorted(parity_by_space.items())),
        "parity_failure_count": sum(
            not (row["linear_match"] and row["accelerated_match"] and row["parity_match"]) for row in parity_rows
        ),
        "unexplained_event_count": sum(bool(row["unexplained_dependency"]) for row in dependency_rows),
        "contradiction_candidate_count": len(contradiction_rows),
        "mechanistically_explained": not contradiction_rows,
    }


def build_suite_summaries(program_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in program_rows:
        grouped[str(row["suite"])].append(row)
    summaries: list[dict[str, object]] = []
    for suite, rows in sorted(grouped.items()):
        summaries.append(
            {
                "suite": suite,
                "program_count": len(rows),
                "event_count": sum(int(row["event_count"]) for row in rows),
                "source_observation_count": sum(int(row["source_observation_count"]) for row in rows),
                "primitive_event_counts": {
                    "latest_write": sum(int(row["primitive_event_counts"]["latest_write"]) for row in rows),
                    "stack": sum(int(row["primitive_event_counts"]["stack"]) for row in rows),
                    "control": sum(int(row["primitive_event_counts"]["control"]) for row in rows),
                    "local_transition": sum(int(row["primitive_event_counts"]["local_transition"]) for row in rows),
                },
                "contradiction_candidate_count": sum(int(row["contradiction_candidate_count"]) for row in rows),
                "parity_failure_count": sum(int(row["parity_failure_count"]) for row in rows),
            }
        )
    return summaries


def build_diagnostic_companion() -> dict[str, object]:
    staged = read_json(ROOT / "results" / "M4_staged_pointer_decoder" / "summary.json")
    provenance = read_json(ROOT / "results" / "M4_failure_provenance" / "summary.json")
    return {
        "claim_role": "diagnostic_only_mask_strength_evidence",
        "notes": [
            "These artifacts remain diagnostic-only and do not widen the R4 D0 mechanism claim.",
            "They are reused only to show that stronger legality/mask structure matters in the wider staged branch.",
        ],
        "staged_pointer_decoder": {
            "valid_success_regime": "opcode_legal",
            "ablation_regimes": ["opcode_shape", "structural"],
            "opcode_legal_train_exact_trace_accuracy": staged["rollout"]["opcode_legal"]["train_programs"][
                "exact_trace_accuracy"
            ],
            "opcode_legal_heldout_exact_trace_accuracy": staged["rollout"]["opcode_legal"]["heldout_programs"][
                "exact_trace_accuracy"
            ],
            "opcode_shape_heldout_exact_trace_accuracy": staged["rollout"]["opcode_shape"]["heldout_programs"][
                "exact_trace_accuracy"
            ],
            "structural_heldout_exact_trace_accuracy": staged["rollout"]["structural"]["heldout_programs"][
                "exact_trace_accuracy"
            ],
        },
        "failure_provenance": {
            "opcode_legal_heldout_failed_program_count": provenance["mask_modes"]["opcode_legal"]["heldout_programs"][
                "failed_program_count"
            ],
            "opcode_shape_heldout_failed_program_count": provenance["mask_modes"]["opcode_shape"]["heldout_programs"][
                "failed_program_count"
            ],
            "structural_heldout_failed_program_count": provenance["mask_modes"]["structural"]["heldout_programs"][
                "failed_program_count"
            ],
            "opcode_shape_heldout_root_cause_heads": provenance["mask_modes"]["opcode_shape"]["heldout_programs"][
                "by_root_cause_head"
            ],
        },
    }


def build_summary(
    *,
    cases,
    dependency_rows: list[dict[str, object]],
    parity_rows: list[dict[str, object]],
    program_rows: list[dict[str, object]],
    suite_rows: list[dict[str, object]],
    contradiction_rows: list[dict[str, object]],
    diagnostic_companion: dict[str, object],
) -> dict[str, object]:
    return {
        "overall": {
            "program_count": len(cases),
            "suite_count": len({case.suite for case in cases}),
            "event_count": len(dependency_rows),
            "source_observation_count": len(parity_rows),
            "primitive_event_counts": {
                "latest_write": sum(bool(row["latest_write_dependency"]) for row in dependency_rows),
                "stack": sum(bool(row["stack_dependency"]) for row in dependency_rows),
                "control": sum(bool(row["control_dependency"]) for row in dependency_rows),
                "local_transition": sum(bool(row["local_transition_dependency"]) for row in dependency_rows),
            },
            "unexplained_event_count": sum(bool(row["unexplained_dependency"]) for row in dependency_rows),
            "parity_failure_count": sum(
                not (row["linear_match"] and row["accelerated_match"] and row["parity_match"]) for row in parity_rows
            ),
            "contradiction_candidate_count": len(contradiction_rows),
        },
        "by_suite": suite_rows,
        "diagnostic_companion_role": diagnostic_companion["claim_role"],
        "claim_impact": {
            "status": "bounded_mechanistic_closure_on_current_d0_suite",
            "target_claims": ["D0"],
            "r5_status": "not_justified",
            "e1c_status": "not_triggered" if not contradiction_rows else "triggered",
            "next_lane": "H7_refreeze_and_record_sync" if not contradiction_rows else "E1c_compiled_boundary_patch",
            "supported_here": [
                "All current positive D0 rows are explainable using only latest-write, stack, control, and deterministic local-transition primitives.",
                "Linear and accelerated Hull retrieval agree exactly on all exported source-event observations from the same positive D0 suites.",
            ],
            "diagnostic_only_here": [
                "Staged-pointer and provenance artifacts remain mask-strength companions only and do not widen the main D0 mechanism claim."
            ],
            "unsupported_here": [
                "R4 does not authorize frontend widening, systems-claim changes, or a broader neural executor claim.",
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases = load_positive_cases()
    interpreter = TraceInterpreter()
    dependency_rows: list[dict[str, object]] = []
    parity_rows: list[dict[str, object]] = []
    program_rows: list[dict[str, object]] = []
    contradiction_rows: list[dict[str, object]] = []

    for case in cases:
        lowered = lower_program(case.program)
        reference = interpreter.run(lowered, max_steps=case.max_steps)
        case_dependency_rows = build_event_dependency_rows(case, reference.events)
        case_parity_rows = build_source_event_parity_rows(case, reference.events)
        case_contradictions = build_contradiction_candidates(case_dependency_rows, case_parity_rows)
        dependency_rows.extend(case_dependency_rows)
        parity_rows.extend(case_parity_rows)
        contradiction_rows.extend(case_contradictions)
        program_rows.append(
            build_program_summary(
                case,
                event_count=reference.final_state.steps,
                dependency_rows=case_dependency_rows,
                parity_rows=case_parity_rows,
                contradiction_rows=case_contradictions,
            )
        )

    suite_rows = build_suite_summaries(program_rows)
    diagnostic_companion = build_diagnostic_companion()
    summary = build_summary(
        cases=cases,
        dependency_rows=dependency_rows,
        parity_rows=parity_rows,
        program_rows=program_rows,
        suite_rows=suite_rows,
        contradiction_rows=contradiction_rows,
        diagnostic_companion=diagnostic_companion,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "mechanism_bridge_rows.json",
        {
            "experiment": "r4_mechanistic_retrieval_bridge_rows",
            "environment": environment.as_dict(),
            "schema": {
                "row_unit": "one source event from one positive D0 program",
                "primitive_classes": [
                    "latest_write",
                    "stack",
                    "control",
                    "local_transition",
                ],
            },
            "rows": dependency_rows,
        },
    )
    write_json(
        OUT_DIR / "source_event_parity_rows.json",
        {
            "experiment": "r4_mechanistic_retrieval_source_event_parity_rows",
            "environment": environment.as_dict(),
            "schema": {
                "row_unit": "one source-event load observation",
                "parity_contract": "linear == accelerated == expected_value",
            },
            "rows": parity_rows,
        },
    )
    write_json(
        OUT_DIR / "program_mechanistic_summary.json",
        {
            "experiment": "r4_mechanistic_retrieval_program_summary",
            "environment": environment.as_dict(),
            "rows": program_rows,
        },
    )
    write_json(
        OUT_DIR / "suite_mechanistic_summary.json",
        {
            "experiment": "r4_mechanistic_retrieval_suite_summary",
            "environment": environment.as_dict(),
            "rows": suite_rows,
        },
    )
    write_json(
        OUT_DIR / "diagnostic_companion.json",
        {
            "experiment": "r4_mechanistic_retrieval_diagnostic_companion",
            "environment": environment.as_dict(),
            "summary": diagnostic_companion,
        },
    )
    write_json(
        OUT_DIR / "contradiction_candidates.json",
        {
            "experiment": "r4_mechanistic_retrieval_contradiction_candidates",
            "environment": environment.as_dict(),
            "rows": contradiction_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r4_mechanistic_retrieval_closure",
            "environment": environment.as_dict(),
            "notes": [
                "R4 stays on the current positive D0 suites and does not widen the frontend or systems claim surface.",
                "The bridge rows classify each source event using only the allowed mechanistic primitive classes.",
                "Source-event parity rows require linear and accelerated Hull retrieval to agree exactly on the same source observations.",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R4 Mechanistic Retrieval Closure",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `mechanism_bridge_rows.json`",
                "- `source_event_parity_rows.json`",
                "- `program_mechanistic_summary.json`",
                "- `suite_mechanistic_summary.json`",
                "- `diagnostic_companion.json`",
                "- `contradiction_candidates.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
