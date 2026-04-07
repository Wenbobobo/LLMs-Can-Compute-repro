"""Export the append-only memory retrieval contract gate for R42."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from exec_trace import TraceInterpreter, stack_fanout_sum_program
from model import MemoryOperation, config_for_operations, extract_stack_slot_operations, run_latest_write_decode
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R42_origin_append_only_memory_retrieval_contract_gate"


@dataclass(frozen=True, slots=True)
class RetrievalTaskSpec:
    family_id: str
    task_id: str
    space: Literal["memory", "stack"]
    source_kind: Literal["synthetic_operations", "program_trace"]
    description: str
    operations: tuple[MemoryOperation, ...]
    notes: str
    program_name: str | None = None


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def length_bucket(max_step: int) -> str:
    if max_step <= 16:
        return "steps<=16"
    if max_step <= 128:
        return "17<=steps<=128"
    return "steps>128"


def latest_write_same_address_short_operations() -> tuple[MemoryOperation, ...]:
    return (
        MemoryOperation(step=0, kind="store", address=3, value=5, space="memory"),
        MemoryOperation(step=1, kind="load", address=3, value=5, space="memory"),
        MemoryOperation(step=2, kind="store", address=3, value=9, space="memory"),
        MemoryOperation(step=3, kind="load", address=3, value=9, space="memory"),
        MemoryOperation(step=4, kind="store", address=3, value=-2, space="memory"),
        MemoryOperation(step=5, kind="load", address=3, value=-2, space="memory"),
    )


def latest_write_same_address_long_operations() -> tuple[MemoryOperation, ...]:
    operations: list[MemoryOperation] = []
    address = 11
    for index in range(24):
        step = 2 * index
        value = (index * 7) - 19
        operations.append(MemoryOperation(step=step, kind="store", address=address, value=value, space="memory"))
        if index % 3 == 2:
            operations.append(MemoryOperation(step=step + 1, kind="load", address=address, value=value, space="memory"))
    return tuple(operations)


def stack_slot_operations(depth: int, *, base_value: int) -> tuple[MemoryOperation, ...]:
    interpreter = TraceInterpreter()
    result = interpreter.run(stack_fanout_sum_program(depth, base_value=base_value))
    return extract_stack_slot_operations(result.events)


def address_reuse_duplicate_and_tie_operations() -> tuple[MemoryOperation, ...]:
    return (
        MemoryOperation(step=0, kind="load", address=9, value=0, space="memory"),
        MemoryOperation(step=1, kind="store", address=2, value=4, space="memory"),
        MemoryOperation(step=2, kind="store", address=7, value=11, space="memory"),
        MemoryOperation(step=3, kind="store", address=2, value=8, space="memory"),
        MemoryOperation(step=4, kind="load", address=2, value=8, space="memory"),
        MemoryOperation(step=5, kind="store", address=2, value=3, space="memory"),
        MemoryOperation(step=5, kind="store", address=2, value=7, space="memory"),
        MemoryOperation(step=6, kind="load", address=2, value=5, space="memory"),
        MemoryOperation(step=7, kind="load", address=7, value=11, space="memory"),
        MemoryOperation(step=8, kind="load", address=9, value=0, space="memory"),
    )


def precision_range_sweep_operations() -> tuple[MemoryOperation, ...]:
    return (
        MemoryOperation(step=0, kind="load", address=16384, value=0, space="memory"),
        MemoryOperation(step=1, kind="store", address=64, value=5, space="memory"),
        MemoryOperation(step=2, kind="load", address=64, value=5, space="memory"),
        MemoryOperation(step=255, kind="store", address=4096, value=-7, space="memory"),
        MemoryOperation(step=256, kind="load", address=4096, value=-7, space="memory"),
        MemoryOperation(step=1023, kind="store", address=64, value=11, space="memory"),
        MemoryOperation(step=1024, kind="load", address=64, value=11, space="memory"),
        MemoryOperation(step=4095, kind="store", address=16384, value=21, space="memory"),
        MemoryOperation(step=4096, kind="load", address=16384, value=21, space="memory"),
    )


def build_task_manifest() -> list[RetrievalTaskSpec]:
    return [
        RetrievalTaskSpec(
            family_id="latest_write_same_address_short",
            task_id="latest_write_same_address_short",
            space="memory",
            source_kind="synthetic_operations",
            description="Short same-address overwrite sequence with interleaved loads.",
            operations=latest_write_same_address_short_operations(),
            notes="Minimal append-only latest-write-by-address contract row.",
        ),
        RetrievalTaskSpec(
            family_id="latest_write_same_address_long",
            task_id="latest_write_same_address_long",
            space="memory",
            source_kind="synthetic_operations",
            description="Longer same-address overwrite chain to keep only the latest row visible.",
            operations=latest_write_same_address_long_operations(),
            notes="Stress same-address recency across a longer append-only history.",
        ),
        RetrievalTaskSpec(
            family_id="stack_slot_depth_short",
            task_id="stack_slot_depth_short",
            space="stack",
            source_kind="program_trace",
            description="Trace-derived short stack fanout with multiple stack-slot reads.",
            operations=stack_slot_operations(6, base_value=2),
            program_name="stack_fanout_sum_6_v2",
            notes="Real stack trace extracted from the current deterministic substrate.",
        ),
        RetrievalTaskSpec(
            family_id="stack_slot_depth_long",
            task_id="stack_slot_depth_long",
            space="stack",
            source_kind="program_trace",
            description="Trace-derived deeper stack fanout probing larger stack-slot depths.",
            operations=stack_slot_operations(18, base_value=1),
            program_name="stack_fanout_sum_18_v1",
            notes="Deeper stack-slot contract row without widening beyond append-only retrieval.",
        ),
        RetrievalTaskSpec(
            family_id="address_reuse_duplicate_and_tie_cases",
            task_id="address_reuse_duplicate_and_tie_cases",
            space="memory",
            source_kind="synthetic_operations",
            description="Address reuse, default read, and duplicate-row tie averaging in one fixed sequence.",
            operations=address_reuse_duplicate_and_tie_operations(),
            notes="Includes default-row hits plus duplicate same-step same-address maximizers.",
        ),
        RetrievalTaskSpec(
            family_id="precision_range_sweep",
            task_id="precision_range_sweep",
            space="memory",
            source_kind="synthetic_operations",
            description="Large-step and large-address sweep over the same exact latest-write contract.",
            operations=precision_range_sweep_operations(),
            notes="Checks that exact row identity survives larger step and address ranges on the saved substrate.",
        ),
    ]


def row_labels(run, indices: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(run.candidate_rows[index].label for index in indices)


def has_duplicate_maximizers(run, indices: tuple[int, ...]) -> bool:
    if len(indices) <= 1:
        return False
    keys = [
        (run.candidate_rows[index].kind, run.candidate_rows[index].address, run.candidate_rows[index].step)
        for index in indices
    ]
    return len(set(keys)) < len(keys)


def evaluate_task(task: RetrievalTaskSpec) -> tuple[dict[str, object], dict[str, object], dict[str, object] | None]:
    decode_run = run_latest_write_decode(task.operations, config_for_operations(task.operations))
    observation_count = len(decode_run.observations)
    exact_value_count = 0
    exact_row_identity_count = 0
    tie_observation_count = 0
    duplicate_maximizer_observation_count = 0
    default_hit_observation_count = 0
    first_failure: dict[str, object] | None = None

    for observation in decode_run.observations:
        exact_value = (
            observation.expected_value == observation.linear_value == observation.accelerated_value
        )
        exact_rows = observation.linear_maximizer_indices == observation.accelerated_maximizer_indices
        if exact_value:
            exact_value_count += 1
        if exact_rows:
            exact_row_identity_count += 1
        if len(observation.linear_maximizer_indices) > 1:
            tie_observation_count += 1
        if has_duplicate_maximizers(decode_run, observation.linear_maximizer_indices):
            duplicate_maximizer_observation_count += 1
        if any(decode_run.candidate_rows[index].kind == "default" for index in observation.linear_maximizer_indices):
            default_hit_observation_count += 1
        if first_failure is None and (not exact_value or not exact_rows):
            first_failure = {
                "task_id": task.task_id,
                "step": observation.step,
                "address": observation.address,
                "expected_value": observation.expected_value,
                "linear_value": observation.linear_value,
                "accelerated_value": observation.accelerated_value,
                "linear_row_labels": row_labels(decode_run, observation.linear_maximizer_indices),
                "accelerated_row_labels": row_labels(decode_run, observation.accelerated_maximizer_indices),
            }

    max_step = max(operation.step for operation in task.operations)
    max_address = max(operation.address for operation in task.operations)
    task_row = {
        "family_id": task.family_id,
        "task_id": task.task_id,
        "space": task.space,
        "source_kind": task.source_kind,
        "program_name": task.program_name,
        "description": task.description,
        "length_bucket": length_bucket(max_step),
        "operation_count": len(task.operations),
        "observation_count": observation_count,
        "candidate_row_count": len(decode_run.candidate_rows),
        "max_step": max_step,
        "max_address": max_address,
        "verdict": "exact"
        if observation_count and exact_value_count == observation_count and exact_row_identity_count == observation_count
        else "break",
        "notes": task.notes,
    }
    measurement_row = {
        "family_id": task.family_id,
        "task_id": task.task_id,
        "exact_value_count": exact_value_count,
        "exact_row_identity_count": exact_row_identity_count,
        "observation_count": observation_count,
        "tie_observation_count": tie_observation_count,
        "duplicate_maximizer_observation_count": duplicate_maximizer_observation_count,
        "default_hit_observation_count": default_hit_observation_count,
        "max_linear_multiplicity": max(len(observation.linear_maximizer_indices) for observation in decode_run.observations),
        "max_accelerated_multiplicity": max(
            len(observation.accelerated_maximizer_indices) for observation in decode_run.observations
        ),
        "max_step": max_step,
        "max_address": max_address,
    }
    return task_row, measurement_row, first_failure


def build_execution_manifest(tasks: list[RetrievalTaskSpec]) -> list[dict[str, object]]:
    return [
        {
            "family_id": task.family_id,
            "task_id": task.task_id,
            "space": task.space,
            "source_kind": task.source_kind,
            "program_name": task.program_name,
            "description": task.description,
        }
        for task in tasks
    ]


def assess_gate(
    task_rows: list[dict[str, object]],
    measurement_rows: list[dict[str, object]],
    stop_rule: dict[str, object],
) -> dict[str, object]:
    if stop_rule["stop_rule_triggered"]:
        lane_verdict = "retrieval_contract_break"
    else:
        lane_verdict = "keep_semantic_boundary_route"

    return {
        "lane_verdict": lane_verdict,
        "task_count": len(task_rows),
        "exact_task_count": sum(row["verdict"] == "exact" for row in task_rows),
        "observation_count": sum(int(row["observation_count"]) for row in measurement_rows),
        "exact_value_observation_count": sum(int(row["exact_value_count"]) for row in measurement_rows),
        "exact_row_identity_observation_count": sum(int(row["exact_row_identity_count"]) for row in measurement_rows),
        "tie_observation_count": sum(int(row["tie_observation_count"]) for row in measurement_rows),
        "duplicate_maximizer_observation_count": sum(
            int(row["duplicate_maximizer_observation_count"]) for row in measurement_rows
        ),
        "default_hit_observation_count": sum(int(row["default_hit_observation_count"]) for row in measurement_rows),
        "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
        "later_explicit_packet_required": True,
        "conditional_next_runtime_candidate": "r43_origin_bounded_memory_small_vm_execution_gate"
        if lane_verdict == "keep_semantic_boundary_route"
        else "none",
    }


def main() -> None:
    tasks = build_task_manifest()
    execution_manifest = build_execution_manifest(tasks)
    task_rows: list[dict[str, object]] = []
    measurement_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for task in tasks:
        task_row, measurement_row, task_failure = evaluate_task(task)
        task_rows.append(task_row)
        measurement_rows.append(measurement_row)
        if task_failure is not None:
            first_failure = task_failure
            break

    stop_rule = {
        "planned_task_count": len(tasks),
        "executed_task_count": len(task_rows),
        "stop_rule_triggered": first_failure is not None,
        "first_failure": first_failure,
        "reason": "all tasks stayed exact on value and row identity"
        if first_failure is None
        else "stopped at the first brute-force versus accelerated retrieval mismatch",
    }
    gate = assess_gate(task_rows, measurement_rows, stop_rule)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "execution_manifest.json", {"rows": execution_manifest})
    write_json(OUT_DIR / "task_rows.json", {"rows": task_rows})
    write_json(OUT_DIR / "measurement_rows.json", {"rows": measurement_rows})
    write_json(OUT_DIR / "stop_rule.json", stop_rule)
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "r42_origin_append_only_memory_retrieval_contract_gate_complete",
                "active_runtime_lane": "r42_origin_append_only_memory_retrieval_contract_gate",
                "activation_packet": "h40_post_h38_semantic_boundary_activation_packet",
                "gate": gate,
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
