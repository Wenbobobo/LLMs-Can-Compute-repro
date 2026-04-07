"""Export the post-H51 2D hard-max retrieval equivalence gate for R55."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from exec_trace import TraceInterpreter, stack_fanout_sum_program
from model import config_for_operations, extract_stack_slot_operations, run_latest_write_decode
from model.exact_hardmax import MemoryOperation
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R55_origin_2d_hardmax_retrieval_equivalence_gate"


@dataclass(frozen=True, slots=True)
class RetrievalEquivalenceTask:
    task_id: str
    category: Literal["overwrite_after_gap", "stack_slot", "duplicate_max", "declared_tie", "coordinate_offset"]
    source_kind: Literal["synthetic_operations", "program_trace"]
    space: Literal["memory", "stack", "call"]
    description: str
    operations: tuple[MemoryOperation, ...]
    notes: str
    program_name: str | None = None


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


def overwrite_after_gap_operations() -> tuple[MemoryOperation, ...]:
    return (
        MemoryOperation(step=0, kind="load", address=8, value=0, space="memory"),
        MemoryOperation(step=1, kind="store", address=8, value=4, space="memory"),
        MemoryOperation(step=2, kind="store", address=1, value=13, space="memory"),
        MemoryOperation(step=4, kind="load", address=8, value=4, space="memory"),
        MemoryOperation(step=6, kind="store", address=8, value=11, space="memory"),
        MemoryOperation(step=7, kind="load", address=1, value=13, space="memory"),
        MemoryOperation(step=9, kind="load", address=8, value=11, space="memory"),
    )


def stack_slot_depth_operations(depth: int, *, base_value: int) -> tuple[MemoryOperation, ...]:
    interpreter = TraceInterpreter()
    result = interpreter.run(stack_fanout_sum_program(depth, base_value=base_value))
    return extract_stack_slot_operations(result.events)


def duplicate_max_identity_operations() -> tuple[MemoryOperation, ...]:
    return (
        MemoryOperation(step=0, kind="store", address=5, value=7, space="memory"),
        MemoryOperation(step=0, kind="store", address=5, value=7, space="memory"),
        MemoryOperation(step=1, kind="load", address=5, value=7, space="memory"),
    )


def declared_tie_average_operations() -> tuple[MemoryOperation, ...]:
    return (
        MemoryOperation(step=0, kind="store", address=5, value=3, space="memory"),
        MemoryOperation(step=0, kind="store", address=5, value=7, space="memory"),
        MemoryOperation(step=1, kind="load", address=5, value=5, space="memory"),
    )


def coordinate_offset_operations() -> tuple[MemoryOperation, ...]:
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


def build_task_manifest() -> list[RetrievalEquivalenceTask]:
    return [
        RetrievalEquivalenceTask(
            task_id="overwrite_after_gap_static_memory",
            category="overwrite_after_gap",
            source_kind="synthetic_operations",
            space="memory",
            description="Latest-write overwrite-after-gap row on one static address with unrelated intervening stores.",
            operations=overwrite_after_gap_operations(),
            notes="Tests that the reference and 2D hard-max path both keep the most recent relevant write only.",
        ),
        RetrievalEquivalenceTask(
            task_id="deep_stack_slot_trace",
            category="stack_slot",
            source_kind="program_trace",
            space="stack",
            description="Trace-derived deeper stack-slot retrieval row from the current deterministic substrate.",
            operations=stack_slot_depth_operations(18, base_value=1),
            notes="Tests the same exact retrieval contract on deeper stack-relative reads.",
            program_name="stack_fanout_sum_18_v1",
        ),
        RetrievalEquivalenceTask(
            task_id="duplicate_max_identity",
            category="duplicate_max",
            source_kind="synthetic_operations",
            space="memory",
            description="Exact duplicate latest rows that preserve value but still require exact maximizer-row identity.",
            operations=duplicate_max_identity_operations(),
            notes="Value equality alone is insufficient; both duplicate rows must remain visible as maximizers.",
        ),
        RetrievalEquivalenceTask(
            task_id="declared_tie_average",
            category="declared_tie",
            source_kind="synthetic_operations",
            space="memory",
            description="Same-step tie row with different values requiring explicit averaging semantics.",
            operations=declared_tie_average_operations(),
            notes="Makes tie handling first-class rather than incidental.",
        ),
        RetrievalEquivalenceTask(
            task_id="coordinate_offset_range_sweep",
            category="coordinate_offset",
            source_kind="synthetic_operations",
            space="memory",
            description="Large-step and large-address coordinate-offset row on the same latest-write contract.",
            operations=coordinate_offset_operations(),
            notes="Stresses the geometric addressing pattern without widening substrate scope.",
        ),
    ]


def row_labels(run: Any, indices: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(run.candidate_rows[index].label for index in indices)


def has_duplicate_maximizers(run: Any, indices: tuple[int, ...]) -> bool:
    if len(indices) <= 1:
        return False
    keys = [
        (run.candidate_rows[index].kind, run.candidate_rows[index].address, run.candidate_rows[index].step)
        for index in indices
    ]
    return len(set(keys)) < len(keys)


def evaluate_task(task: RetrievalEquivalenceTask) -> tuple[dict[str, object], dict[str, object], dict[str, object] | None]:
    config = config_for_operations(task.operations)
    decode_run = run_latest_write_decode(task.operations, config)
    observation_count = len(decode_run.observations)
    linear_expected_exact_count = 0
    accelerated_expected_exact_count = 0
    row_identity_exact_count = 0
    tie_observation_count = 0
    duplicate_maximizer_observation_count = 0
    default_hit_observation_count = 0
    first_failure: dict[str, object] | None = None

    for observation in decode_run.observations:
        linear_expected_exact = observation.linear_value == observation.expected_value
        accelerated_expected_exact = observation.accelerated_value == observation.expected_value
        row_identity_exact = observation.linear_maximizer_indices == observation.accelerated_maximizer_indices
        if linear_expected_exact:
            linear_expected_exact_count += 1
        if accelerated_expected_exact:
            accelerated_expected_exact_count += 1
        if row_identity_exact:
            row_identity_exact_count += 1
        if len(observation.linear_maximizer_indices) > 1:
            tie_observation_count += 1
        if has_duplicate_maximizers(decode_run, observation.linear_maximizer_indices):
            duplicate_maximizer_observation_count += 1
        if any(decode_run.candidate_rows[index].kind == "default" for index in observation.linear_maximizer_indices):
            default_hit_observation_count += 1
        if first_failure is None and (not linear_expected_exact or not accelerated_expected_exact or not row_identity_exact):
            first_failure = {
                "task_id": task.task_id,
                "category": task.category,
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
    exact = (
        observation_count > 0
        and linear_expected_exact_count == observation_count
        and accelerated_expected_exact_count == observation_count
        and row_identity_exact_count == observation_count
    )
    task_row = {
        "task_id": task.task_id,
        "category": task.category,
        "space": task.space,
        "source_kind": task.source_kind,
        "program_name": task.program_name,
        "description": task.description,
        "operation_count": len(task.operations),
        "observation_count": observation_count,
        "candidate_row_count": len(decode_run.candidate_rows),
        "max_step": max_step,
        "max_address": max_address,
        "verdict": "exact" if exact else "break",
        "notes": task.notes,
    }
    measurement_row = {
        "task_id": task.task_id,
        "linear_expected_exact_count": linear_expected_exact_count,
        "accelerated_expected_exact_count": accelerated_expected_exact_count,
        "row_identity_exact_count": row_identity_exact_count,
        "observation_count": observation_count,
        "tie_observation_count": tie_observation_count,
        "duplicate_maximizer_observation_count": duplicate_maximizer_observation_count,
        "default_hit_observation_count": default_hit_observation_count,
        "max_step": max_step,
        "max_address": max_address,
    }
    return task_row, measurement_row, first_failure


def load_inputs() -> dict[str, Any]:
    return {
        "r55_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "README.md"
        ),
        "r55_status_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "status.md"
        ),
        "r55_todo_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "todo.md"
        ),
        "r55_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "acceptance.md"
        ),
        "r55_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "artifact_index.md"
        ),
        "equivalence_contract_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "equivalence_contract.md"
        ),
        "task_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "task_matrix.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h51_summary": read_json(ROOT / "results" / "H51_post_h50_origin_mechanism_reentry_packet" / "summary.json"),
        "f28_summary": read_json(ROOT / "results" / "F28_post_h50_origin_mechanism_reentry_bundle" / "summary.json"),
        "h50_summary": read_json(ROOT / "results" / "H50_post_r51_r52_scope_decision_packet" / "summary.json"),
    }


def build_checklist_rows(
    inputs: dict[str, Any],
    task_rows: list[dict[str, object]],
    measurement_rows: list[dict[str, object]],
    lane_verdict: str,
    stop_rule: dict[str, object],
) -> list[dict[str, object]]:
    h51 = inputs["h51_summary"]["summary"]
    f28 = inputs["f28_summary"]["summary"]
    total_observations = sum(int(row["observation_count"]) for row in measurement_rows)
    exact_linear = sum(int(row["linear_expected_exact_count"]) for row in measurement_rows)
    exact_accelerated = sum(int(row["accelerated_expected_exact_count"]) for row in measurement_rows)
    exact_identity = sum(int(row["row_identity_exact_count"]) for row in measurement_rows)
    categories = {str(row["category"]) for row in task_rows}
    tie_count = sum(int(row["tie_observation_count"]) for row in measurement_rows)
    duplicate_count = sum(int(row["duplicate_maximizer_observation_count"]) for row in measurement_rows)
    return [
        {
            "item_id": "r55_requires_positive_h51_reentry_basis",
            "status": "pass"
            if str(h51["selected_outcome"]) == "authorize_origin_mechanism_reentry_through_r55_first"
            and str(h51["only_next_runtime_candidate"]) == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
            and str(f28["only_next_runtime_candidate"]) == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
            else "blocked",
            "notes": "R55 only runs after H51 selects explicit mechanism reentry through R55 first.",
        },
        {
            "item_id": "r55_docs_fix_reference_contract_and_required_task_classes",
            "status": "pass"
            if contains_all(
                inputs["r55_readme_text"],
                [
                    "tests whether the claimed `2d` hard-max retrieval primitive is exactly equivalent",
                    "next required packet is",
                    "r56_origin_append_only_trace_vm_semantics_gate",
                ],
            )
            and contains_all(
                inputs["equivalence_contract_text"],
                [
                    "the reference path is a transparent latest-relevant-state lookup",
                    "the candidate path is the claimed `2d` hard-max retrieval implementation",
                    "both paths must return the same value and the same maximizer-row identity",
                ],
            )
            and contains_all(
                inputs["task_matrix_text"],
                [
                    "overwrite-after-gap",
                    "stack-slot",
                    "duplicate-max",
                    "declared tie",
                    "coordinate-offset",
                ],
            )
            else "blocked",
            "notes": "R55 milestone docs must explicitly fix the reference contract and the five required task classes.",
        },
        {
            "item_id": "reference_and_candidate_values_match_on_every_declared_read",
            "status": "pass"
            if total_observations > 0 and exact_linear == total_observations and exact_accelerated == total_observations
            else "blocked",
            "notes": "Both the transparent reference and the claimed fast path must match the declared expected value on every read.",
        },
        {
            "item_id": "candidate_path_preserves_exact_maximizer_row_identity",
            "status": "pass" if total_observations > 0 and exact_identity == total_observations else "blocked",
            "notes": "R55 requires maximizer-row identity parity, not value parity alone.",
        },
        {
            "item_id": "task_matrix_covers_duplicate_tie_stack_and_coordinate_offset_cases",
            "status": "pass"
            if categories
            == {"overwrite_after_gap", "stack_slot", "duplicate_max", "declared_tie", "coordinate_offset"}
            and tie_count >= 2
            and duplicate_count >= 2
            else "blocked",
            "notes": "The fixed bounded suite must cover all required task classes and explicit tie/duplicate observations.",
        },
        {
            "item_id": "r55_opens_r56_only_if_exact",
            "status": "pass"
            if (
                lane_verdict == "retrieval_equivalence_supported_exactly"
                and stop_rule["next_required_packet"] == "r56_origin_append_only_trace_vm_semantics_gate"
                and bool(stop_rule["r56_open"]) is True
            )
            or (
                lane_verdict != "retrieval_equivalence_supported_exactly"
                and stop_rule["next_required_packet"] == "h52_post_r55_r56_r57_origin_mechanism_decision_packet"
                and bool(stop_rule["r56_open"]) is False
            )
            else "blocked",
            "notes": "R56 can open only after a positive exact R55 verdict; otherwise the lane must stop and close explicitly.",
        },
    ]


def build_claim_packet(lane_verdict: str, stop_rule: dict[str, object], summary_fields: dict[str, object]) -> dict[str, object]:
    positive = lane_verdict == "retrieval_equivalence_supported_exactly"
    return {
        "summary": {
            "supported_here": [
                "The claimed 2D hard-max retrieval path matches the transparent reference latest-relevant-state lookup exactly on the fixed bounded R55 suite."
                if positive
                else "The claimed 2D hard-max retrieval path does not match the transparent reference latest-relevant-state lookup exactly on the fixed bounded R55 suite.",
                "R55 keeps maximizer-row identity explicit rather than collapsing the gate to value parity only.",
                "R55 makes duplicate-max and tie semantics first-class, machine-readable gate criteria.",
            ],
            "unsupported_here": [
                "R55 does not establish trace-VM semantics or fast-path system value by itself.",
                "R55 does not authorize transformed-model entry, trainable entry, arbitrary C, or broad Wasm claims.",
                "R55 does not permit R56 to open if exact retrieval equivalence fails.",
            ],
            "disconfirmed_here": [
                "The idea that retrieval equivalence can be inferred from end-to-end demo success without exact maximizer-row parity."
            ],
            "distilled_result": {
                **summary_fields,
                "stop_rule_triggered": bool(stop_rule["stop_rule_triggered"]),
            },
        }
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h51 = inputs["h51_summary"]["summary"]
    f28 = inputs["f28_summary"]["summary"]
    h50 = inputs["h50_summary"]["summary"]
    return [
        {
            "source": "results/H51_post_h50_origin_mechanism_reentry_packet/summary.json",
            "fields": {
                "active_stage": h51["active_stage"],
                "selected_outcome": h51["selected_outcome"],
                "only_next_runtime_candidate": h51["only_next_runtime_candidate"],
            },
        },
        {
            "source": "results/F28_post_h50_origin_mechanism_reentry_bundle/summary.json",
            "fields": {
                "active_stage": f28["active_stage"],
                "only_next_runtime_candidate": f28["only_next_runtime_candidate"],
                "current_low_priority_wave": f28["current_low_priority_wave"],
            },
        },
        {
            "source": "results/H50_post_r51_r52_scope_decision_packet/summary.json",
            "fields": {
                "active_stage": h50["active_stage"],
                "selected_outcome": h50["selected_outcome"],
                "current_paper_grade_endpoint": h50["current_paper_grade_endpoint"],
            },
        },
        {
            "path": "docs/milestones/R55_origin_2d_hardmax_retrieval_equivalence_gate/equivalence_contract.md",
            "matched_lines": extract_matching_lines(
                inputs["equivalence_contract_text"],
                needles=[
                    "transparent latest-relevant-state lookup",
                    "same value and the same maximizer-row identity",
                ],
            ),
        },
        {
            "path": "docs/milestones/R55_origin_2d_hardmax_retrieval_equivalence_gate/task_matrix.md",
            "matched_lines": extract_matching_lines(
                inputs["task_matrix_text"],
                needles=["overwrite-after-gap", "stack-slot", "duplicate-max", "declared tie", "coordinate-offset"],
            ),
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "matched_lines": extract_matching_lines(
                inputs["current_stage_driver_text"],
                needles=[
                    "R55_origin_2d_hardmax_retrieval_equivalence_gate",
                    "R56_origin_append_only_trace_vm_semantics_gate",
                ],
            ),
        },
    ]


def main() -> None:
    inputs = load_inputs()
    tasks = build_task_manifest()
    task_rows: list[dict[str, object]] = []
    measurement_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for task in tasks:
        task_row, measurement_row, task_first_failure = evaluate_task(task)
        task_rows.append(task_row)
        measurement_rows.append(measurement_row)
        if first_failure is None and task_first_failure is not None:
            first_failure = task_first_failure

    total_observations = sum(int(row["observation_count"]) for row in measurement_rows)
    linear_exact_observations = sum(int(row["linear_expected_exact_count"]) for row in measurement_rows)
    accelerated_exact_observations = sum(int(row["accelerated_expected_exact_count"]) for row in measurement_rows)
    row_identity_exact_observations = sum(int(row["row_identity_exact_count"]) for row in measurement_rows)
    tie_observation_count = sum(int(row["tie_observation_count"]) for row in measurement_rows)
    duplicate_maximizer_observation_count = sum(int(row["duplicate_maximizer_observation_count"]) for row in measurement_rows)

    lane_positive = (
        total_observations > 0
        and linear_exact_observations == total_observations
        and accelerated_exact_observations == total_observations
        and row_identity_exact_observations == total_observations
    )
    lane_verdict = "retrieval_equivalence_supported_exactly" if lane_positive else "retrieval_equivalence_falsified"
    next_required_packet = (
        "r56_origin_append_only_trace_vm_semantics_gate"
        if lane_positive
        else "h52_post_r55_r56_r57_origin_mechanism_decision_packet"
    )

    stop_rule = {
        "experiment": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
        "stop_rule_triggered": not lane_positive,
        "stop_reason": None if lane_positive else "exact_retrieval_equivalence_broke",
        "r56_open": lane_positive,
        "r57_open": False,
        "next_required_packet": next_required_packet,
        "first_failure": first_failure,
    }

    summary_fields = {
        "current_active_docs_only_stage": "h51_post_h50_origin_mechanism_reentry_packet",
        "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "current_planning_bundle": "f28_post_h50_origin_mechanism_reentry_bundle",
        "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
        "active_runtime_lane": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
        "lane_verdict": lane_verdict,
        "planned_task_count": len(task_rows),
        "executed_task_count": len(task_rows),
        "exact_task_count": sum(int(row["verdict"] == "exact") for row in task_rows),
        "observation_count": total_observations,
        "linear_expected_exact_observation_count": linear_exact_observations,
        "accelerated_expected_exact_observation_count": accelerated_exact_observations,
        "row_identity_exact_observation_count": row_identity_exact_observations,
        "tie_observation_count": tie_observation_count,
        "duplicate_maximizer_observation_count": duplicate_maximizer_observation_count,
        "first_failure_task_id": None if first_failure is None else first_failure["task_id"],
        "next_required_packet": next_required_packet,
    }

    checklist_rows = build_checklist_rows(inputs, task_rows, measurement_rows, lane_verdict, stop_rule)
    claim_packet = build_claim_packet(lane_verdict, stop_rule, summary_fields)
    snapshot_rows = build_snapshot(inputs)

    summary_payload = {
        "summary": {
            "current_active_docs_only_stage": summary_fields["current_active_docs_only_stage"],
            "preserved_prior_docs_only_closeout": summary_fields["preserved_prior_docs_only_closeout"],
            "current_paper_grade_endpoint": summary_fields["current_paper_grade_endpoint"],
            "current_planning_bundle": summary_fields["current_planning_bundle"],
            "current_low_priority_wave": summary_fields["current_low_priority_wave"],
            "active_runtime_lane": summary_fields["active_runtime_lane"],
            "gate": {
                "lane_verdict": summary_fields["lane_verdict"],
                "planned_task_count": summary_fields["planned_task_count"],
                "executed_task_count": summary_fields["executed_task_count"],
                "exact_task_count": summary_fields["exact_task_count"],
                "observation_count": summary_fields["observation_count"],
                "linear_expected_exact_observation_count": summary_fields["linear_expected_exact_observation_count"],
                "accelerated_expected_exact_observation_count": summary_fields["accelerated_expected_exact_observation_count"],
                "row_identity_exact_observation_count": summary_fields["row_identity_exact_observation_count"],
                "tie_observation_count": summary_fields["tie_observation_count"],
                "duplicate_maximizer_observation_count": summary_fields["duplicate_maximizer_observation_count"],
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
        "coverage": {
            "category_count": len({str(row["category"]) for row in task_rows}),
            "categories": sorted({str(row["category"]) for row in task_rows}),
            "total_observation_count": total_observations,
            "tie_observation_count": tie_observation_count,
            "duplicate_maximizer_observation_count": duplicate_maximizer_observation_count,
        },
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
