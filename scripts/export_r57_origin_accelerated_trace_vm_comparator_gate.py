"""Export the post-R56 accelerated trace-VM comparator gate for R57."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from time import perf_counter
from typing import Any, Literal

from exec_trace import (
    ExecutionResult,
    Program,
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
OUT_DIR = ROOT / "results" / "R57_origin_accelerated_trace_vm_comparator_gate"

TRACE_LENGTH_BUCKET = Literal["short", "medium", "long"]


@dataclass(frozen=True, slots=True)
class TraceVMComparatorTask:
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


def reference_wrapper(program: Program, result: ExecutionResult) -> FreeRunningExecutionResult:
    return FreeRunningExecutionResult(
        program=program,
        events=result.events,
        final_state=result.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def timed_average(fn, *, repeats: int = 8) -> float:
    durations: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        fn()
        durations.append(perf_counter() - start)
    return mean(durations)


def classify_trace_length_bucket(transition_count: int) -> TRACE_LENGTH_BUCKET:
    if transition_count <= 16:
        return "short"
    if transition_count <= 80:
        return "medium"
    return "long"


def build_task_manifest() -> list[TraceVMComparatorTask]:
    return [
        TraceVMComparatorTask(
            task_id="static_latest_write_trace",
            category="static_memory",
            description="Short static-memory overwrite row on the exact R56 trace-VM contract.",
            notes="Carries the smallest append-only latest-write row into the R57 comparator without widening scope.",
            program=latest_write_program(),
        ),
        TraceVMComparatorTask(
            task_id="countdown_loop_control_trace",
            category="loop_control",
            description="Loop and branch row on the exact R56 trace-VM contract.",
            notes="Keeps control-flow retrieval visible in the comparator.",
            program=countdown_program(12),
        ),
        TraceVMComparatorTask(
            task_id="indirect_memory_loop_trace",
            category="indirect_memory",
            description="Indirect load/store loop row on the exact R56 trace-VM contract.",
            notes="Measures the longest admitted dynamic-address row from the landed R56 suite.",
            program=loop_indirect_memory_program(6),
        ),
        TraceVMComparatorTask(
            task_id="call_return_trace",
            category="call_return",
            description="Single bounded call/return row on the exact R56 trace-VM contract.",
            notes="Keeps call-frame retrieval inside the same comparator.",
            program=call_chain_program(),
        ),
        TraceVMComparatorTask(
            task_id="flagged_mixed_surface_trace",
            category="mixed_surface",
            description="Mixed stack, static-memory, and indirect-memory row on the exact R56 trace-VM contract.",
            notes="Combines branch, stack, and memory surfaces on the fixed comparator suite.",
            program=flagged_indirect_accumulator_program(4, base_address=32),
        ),
    ]


def load_inputs() -> dict[str, Any]:
    return {
        "r57_readme_text": read_text(
            ROOT / "docs" / "milestones" / "R57_origin_accelerated_trace_vm_comparator_gate" / "README.md"
        ),
        "r57_status_text": read_text(
            ROOT / "docs" / "milestones" / "R57_origin_accelerated_trace_vm_comparator_gate" / "status.md"
        ),
        "r57_todo_text": read_text(
            ROOT / "docs" / "milestones" / "R57_origin_accelerated_trace_vm_comparator_gate" / "todo.md"
        ),
        "r57_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "R57_origin_accelerated_trace_vm_comparator_gate" / "acceptance.md"
        ),
        "r57_comparator_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "R57_origin_accelerated_trace_vm_comparator_gate" / "comparator_matrix.md"
        ),
        "r57_value_rule_text": read_text(
            ROOT / "docs" / "milestones" / "R57_origin_accelerated_trace_vm_comparator_gate" / "value_rule.md"
        ),
        "h52_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "README.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "r56_summary": read_json(ROOT / "results" / "R56_origin_append_only_trace_vm_semantics_gate" / "summary.json"),
        "r56_execution_report": read_json(
            ROOT / "results" / "R56_origin_append_only_trace_vm_semantics_gate" / "execution_report.json"
        ),
        "h51_summary": read_json(ROOT / "results" / "H51_post_h50_origin_mechanism_reentry_packet" / "summary.json"),
        "f28_summary": read_json(ROOT / "results" / "F28_post_h50_origin_mechanism_reentry_bundle" / "summary.json"),
        "h50_summary": read_json(ROOT / "results" / "H50_post_r51_r52_scope_decision_packet" / "summary.json"),
    }


def evaluate_task(
    task: TraceVMComparatorTask,
    *,
    r56_first_failure: dict[str, object] | None,
) -> tuple[dict[str, object], dict[str, object] | None]:
    reference_result = TraceInterpreter().run(task.program)
    max_steps = max(reference_result.final_state.steps + 8, 64)

    accelerated_executor = FreeRunningTraceExecutor(
        stack_strategy="accelerated",
        memory_strategy="accelerated",
        validate_exact_reads=False,
    )
    linear_executor = FreeRunningTraceExecutor(
        stack_strategy="linear",
        memory_strategy="linear",
        validate_exact_reads=False,
    )

    accelerated_result = accelerated_executor.run(task.program, max_steps=max_steps)
    linear_result = linear_executor.run(task.program, max_steps=max_steps)
    reference_execution = reference_wrapper(task.program, reference_result)
    accelerated_outcome = compare_execution_to_reference(
        task.program,
        accelerated_result,
        reference=reference_execution,
    )
    linear_outcome = compare_execution_to_reference(
        task.program,
        linear_result,
        reference=reference_execution,
    )

    accelerated_counter = Counter(observation.space for observation in accelerated_result.read_observations)
    linear_counter = Counter(observation.space for observation in linear_result.read_observations)
    transition_count = len(reference_result.events)
    trace_length_bucket = classify_trace_length_bucket(transition_count)

    accelerated_time = timed_average(lambda: accelerated_executor.run(task.program, max_steps=max_steps))
    linear_time = timed_average(lambda: linear_executor.run(task.program, max_steps=max_steps))
    external_time = timed_average(lambda: TraceInterpreter().run(task.program))

    first_failure = None
    if not accelerated_outcome.exact_trace_match or not accelerated_outcome.exact_final_state_match:
        first_failure = {
            "route": "accelerated_internal_trace_vm",
            "task_id": task.task_id,
            "category": task.category,
            "program_name": task.program.name,
            "first_mismatch_step": accelerated_outcome.first_mismatch_step,
            "failure_reason": accelerated_outcome.failure_reason,
        }
    elif not linear_outcome.exact_trace_match or not linear_outcome.exact_final_state_match:
        first_failure = {
            "route": "linear_internal_trace_vm",
            "task_id": task.task_id,
            "category": task.category,
            "program_name": task.program.name,
            "first_mismatch_step": linear_outcome.first_mismatch_step,
            "failure_reason": linear_outcome.failure_reason,
        }

    prior_failure_note = (
        "R56 carried no prior first failure into R57; the comparator starts from an exact semantics basis."
        if r56_first_failure is None
        else (
            "R56 already carried a prior first failure, so R57 value evidence would be secondary. "
            f"Prior task: {r56_first_failure['task_id']}."
        )
    )

    row = {
        "task_id": task.task_id,
        "category": task.category,
        "program_name": task.program.name,
        "description": task.description,
        "notes": task.notes,
        "reference_runtime_kind": "transparent_external_trace_interpreter",
        "accelerated_runtime_kind": "accelerated_internal_trace_vm",
        "linear_runtime_kind": "linear_internal_trace_vm",
        "transition_count": transition_count,
        "trace_length_bucket": trace_length_bucket,
        "max_steps": max_steps,
        "accelerated_exact_trace_match": accelerated_outcome.exact_trace_match,
        "accelerated_exact_final_state_match": accelerated_outcome.exact_final_state_match,
        "accelerated_first_mismatch_step": accelerated_outcome.first_mismatch_step,
        "linear_exact_trace_match": linear_outcome.exact_trace_match,
        "linear_exact_final_state_match": linear_outcome.exact_final_state_match,
        "linear_first_mismatch_step": linear_outcome.first_mismatch_step,
        "external_exact_trace_match": True,
        "external_exact_final_state_match": True,
        "external_first_mismatch_step": None,
        "accelerated_mean_seconds": accelerated_time,
        "linear_mean_seconds": linear_time,
        "external_mean_seconds": external_time,
        "accelerated_seconds_per_transition": accelerated_time / transition_count,
        "linear_seconds_per_transition": linear_time / transition_count,
        "external_seconds_per_transition": external_time / transition_count,
        "accelerated_vs_linear_speedup": linear_time / accelerated_time if accelerated_time else None,
        "accelerated_vs_external_speedup": external_time / accelerated_time if accelerated_time else None,
        "accelerated_read_count": len(accelerated_result.read_observations),
        "accelerated_stack_read_count": accelerated_counter.get("stack", 0),
        "accelerated_memory_read_count": accelerated_counter.get("memory", 0),
        "accelerated_call_read_count": accelerated_counter.get("call", 0),
        "accelerated_retrieval_share_of_transitions": (
            len(accelerated_result.read_observations) / transition_count if transition_count else 0.0
        ),
        "linear_read_count": len(linear_result.read_observations),
        "linear_stack_read_count": linear_counter.get("stack", 0),
        "linear_memory_read_count": linear_counter.get("memory", 0),
        "linear_call_read_count": linear_counter.get("call", 0),
        "linear_retrieval_share_of_transitions": (
            len(linear_result.read_observations) / transition_count if transition_count else 0.0
        ),
        "external_read_count": 0,
        "external_retrieval_share_of_transitions": 0.0,
        "accelerated_faster_than_linear": accelerated_time < linear_time,
        "accelerated_faster_than_external": accelerated_time < external_time,
        "first_fail_carry_over_note": prior_failure_note,
    }
    return row, first_failure


def build_trace_length_sensitivity(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    sensitivity_rows: list[dict[str, object]] = []
    for bucket in ("short", "medium", "long"):
        bucket_rows = [row for row in rows if row["trace_length_bucket"] == bucket]
        if not bucket_rows:
            continue
        sensitivity_rows.append(
            {
                "trace_length_bucket": bucket,
                "row_count": len(bucket_rows),
                "task_ids": [str(row["task_id"]) for row in bucket_rows],
                "mean_transition_count": mean(float(row["transition_count"]) for row in bucket_rows),
                "mean_accelerated_seconds": mean(float(row["accelerated_mean_seconds"]) for row in bucket_rows),
                "mean_linear_seconds": mean(float(row["linear_mean_seconds"]) for row in bucket_rows),
                "mean_external_seconds": mean(float(row["external_mean_seconds"]) for row in bucket_rows),
                "mean_accelerated_seconds_per_transition": mean(
                    float(row["accelerated_seconds_per_transition"]) for row in bucket_rows
                ),
                "mean_linear_seconds_per_transition": mean(
                    float(row["linear_seconds_per_transition"]) for row in bucket_rows
                ),
                "mean_external_seconds_per_transition": mean(
                    float(row["external_seconds_per_transition"]) for row in bucket_rows
                ),
                "mean_accelerated_vs_linear_speedup": mean(
                    float(row["accelerated_vs_linear_speedup"]) for row in bucket_rows
                ),
                "mean_accelerated_vs_external_speedup": mean(
                    float(row["accelerated_vs_external_speedup"]) for row in bucket_rows
                ),
                "accelerated_faster_than_linear_count": sum(
                    int(bool(row["accelerated_faster_than_linear"])) for row in bucket_rows
                ),
                "accelerated_faster_than_external_count": sum(
                    int(bool(row["accelerated_faster_than_external"])) for row in bucket_rows
                ),
                "mean_internal_retrieval_share_of_transitions": mean(
                    float(row["accelerated_retrieval_share_of_transitions"]) for row in bucket_rows
                ),
            }
        )
    return sensitivity_rows


def build_checklist_rows(
    inputs: dict[str, Any],
    comparator_rows: list[dict[str, object]],
    *,
    lane_verdict: str,
    first_failure: dict[str, object] | None,
) -> list[dict[str, object]]:
    r56 = inputs["r56_summary"]["summary"]
    h51 = inputs["h51_summary"]["summary"]
    f28 = inputs["f28_summary"]["summary"]
    exact_task_ids = [
        str(row["task_id"])
        for row in inputs["r56_execution_report"]["task_rows"]
        if str(row["verdict"]) == "exact"
    ]
    comparator_task_ids = [str(row["task_id"]) for row in comparator_rows]
    accelerated_exact_count = sum(
        int(bool(row["accelerated_exact_trace_match"]) and bool(row["accelerated_exact_final_state_match"]))
        for row in comparator_rows
    )
    linear_exact_count = sum(
        int(bool(row["linear_exact_trace_match"]) and bool(row["linear_exact_final_state_match"]))
        for row in comparator_rows
    )
    return [
        {
            "item_id": "r57_requires_positive_exact_r56_basis",
            "status": "pass"
            if str(r56["gate"]["lane_verdict"]) == "trace_vm_semantics_supported_exactly"
            and int(r56["gate"]["exact_task_count"]) == 5
            and str(r56["gate"]["next_required_packet"]) == "r57_origin_accelerated_trace_vm_comparator_gate"
            and "r57_origin_accelerated_trace_vm_comparator_gate" in h51["only_conditional_later_sequence"]
            and "r57_origin_accelerated_trace_vm_comparator_gate" in f28["only_conditional_later_sequence"]
            else "blocked",
            "notes": "R57 only opens after landed exact R56 on the saved H51/F28 mechanism sequence.",
        },
        {
            "item_id": "r57_docs_fix_three_route_matrix_and_value_rule",
            "status": "pass"
            if contains_all(
                inputs["r57_comparator_matrix_text"],
                [
                    "accelerated internal trace-vm execution",
                    "linear-reference internal trace-vm execution",
                    "transparent external interpreter execution",
                ],
            )
            and contains_all(
                inputs["r57_value_rule_text"],
                [
                    "accelerated route must be compared",
                    "same exact row set",
                    "mechanism supported without fast-path value",
                    "partial mechanism only",
                ],
            )
            and contains_all(
                inputs["r57_acceptance_text"],
                [
                    "runs only on exact `r56` rows",
                    "end-to-end latency",
                    "retrieval-share accounting",
                ],
            )
            else "blocked",
            "notes": "R57 docs must keep the bounded three-route comparator and explicit negative outcome visible.",
        },
        {
            "item_id": "r57_reuses_only_the_exact_r56_rows_without_widening",
            "status": "pass" if comparator_task_ids == exact_task_ids and len(comparator_rows) == 5 else "blocked",
            "notes": "The comparator should stay on the exact five-row R56 suite only.",
        },
        {
            "item_id": "accelerated_and_linear_internal_routes_keep_exactness",
            "status": "pass"
            if accelerated_exact_count == len(comparator_rows) and linear_exact_count == len(comparator_rows)
            else "blocked",
            "notes": "Value comparison is only meaningful if both internal routes stay exact on the transparent reference contract.",
        },
        {
            "item_id": "latency_and_retrieval_share_are_exported_for_each_route",
            "status": "pass"
            if all(float(row["accelerated_mean_seconds"]) > 0.0 for row in comparator_rows)
            and all(float(row["linear_mean_seconds"]) > 0.0 for row in comparator_rows)
            and all(float(row["external_mean_seconds"]) > 0.0 for row in comparator_rows)
            and all("accelerated_retrieval_share_of_transitions" in row for row in comparator_rows)
            and all("linear_retrieval_share_of_transitions" in row for row in comparator_rows)
            else "blocked",
            "notes": "R57 must export end-to-end latency and retrieval-share accounting on the fixed row set.",
        },
        {
            "item_id": "r57_closes_to_h52_without_widening",
            "status": "pass"
            if lane_verdict
            in {
                "accelerated_trace_vm_retains_bounded_value",
                "accelerated_trace_vm_lacks_bounded_value",
                "accelerated_trace_vm_comparator_exactness_broke",
            }
            and (
                first_failure is None
                or str(first_failure["route"]) in {"accelerated_internal_trace_vm", "linear_internal_trace_vm"}
            )
            else "blocked",
            "notes": "R57 should hand the lane directly to H52 instead of reopening broader routes.",
        },
    ]


def build_claim_packet(
    lane_verdict: str,
    *,
    summary_fields: dict[str, object],
) -> dict[str, object]:
    fastpath_positive = lane_verdict == "accelerated_trace_vm_retains_bounded_value"
    comparator_exact = lane_verdict != "accelerated_trace_vm_comparator_exactness_broke"
    return {
        "summary": {
            "supported_here": [
                (
                    "The accelerated and linear internal trace-VM routes both remain exact on the fixed R56 row set."
                    if comparator_exact
                    else "The comparator does not keep both internal routes exact on the fixed R56 row set."
                ),
                "R57 exports latency, retrieval-share, and trace-length sensitivity on the bounded five-row comparator suite.",
                (
                    "The accelerated trace-VM path retains bounded fast-path value on the fixed R56 rows."
                    if fastpath_positive
                    else "Exact mechanism support alone does not imply fast-path value on the fixed R56 rows."
                ),
            ],
            "unsupported_here": [
                (
                    "R57 does not show bounded fast-path value for the accelerated route."
                    if not fastpath_positive
                    else "R57 does not widen the claim ceiling beyond the saved H52 mechanism closeout."
                ),
                "R57 does not reopen transformed-model entry, trainable entry, arbitrary C, or broad Wasm claims.",
                "R57 does not overturn H50 on the broader post-H49 bounded-value question.",
            ],
            "disconfirmed_here": [
                (
                    "The idea that exact mechanism support automatically implies system or fast-path value."
                    if not fastpath_positive
                    else "The idea that a positive narrow fast-path comparator automatically authorizes broader route widening."
                )
            ],
            "distilled_result": summary_fields,
        }
    }


def build_snapshot(
    inputs: dict[str, Any],
    *,
    lane_verdict: str,
    selected_h52_outcome: str,
) -> list[dict[str, object]]:
    r56 = inputs["r56_summary"]["summary"]
    h51 = inputs["h51_summary"]["summary"]
    return [
        {
            "source": "results/R56_origin_append_only_trace_vm_semantics_gate/summary.json",
            "fields": {
                "lane_verdict": r56["gate"]["lane_verdict"],
                "exact_task_count": r56["gate"]["exact_task_count"],
                "transition_count": r56["gate"]["transition_count"],
                "next_required_packet": r56["gate"]["next_required_packet"],
            },
        },
        {
            "source": "results/H51_post_h50_origin_mechanism_reentry_packet/summary.json",
            "fields": {
                "selected_outcome": h51["selected_outcome"],
                "only_conditional_later_sequence": h51["only_conditional_later_sequence"],
            },
        },
        {
            "path": "docs/milestones/R57_origin_accelerated_trace_vm_comparator_gate/comparator_matrix.md",
            "matched_lines": extract_matching_lines(
                inputs["r57_comparator_matrix_text"],
                needles=[
                    "accelerated internal trace-vm execution",
                    "linear-reference internal trace-vm execution",
                    "transparent external interpreter execution",
                ],
            ),
        },
        {
            "path": "docs/milestones/R57_origin_accelerated_trace_vm_comparator_gate/value_rule.md",
            "matched_lines": extract_matching_lines(
                inputs["r57_value_rule_text"],
                needles=[
                    "same exact row set",
                    "without fast-path value",
                    "partial mechanism only",
                ],
            ),
        },
        {
            "path": "docs/milestones/H52_post_r55_r56_r57_origin_mechanism_decision_packet/README.md",
            "matched_lines": extract_matching_lines(
                inputs["h52_readme_text"],
                needles=[
                    "freeze_origin_mechanism_supported_with_fastpath_value",
                    "freeze_origin_mechanism_supported_without_fastpath_value",
                    "stop_as_partial_mechanism_only",
                ],
            ),
        },
        {
            "path": "docs/publication_record/current_stage_driver.md",
            "matched_lines": extract_matching_lines(
                inputs["current_stage_driver_text"],
                needles=[
                    "r57_origin_accelerated_trace_vm_comparator_gate",
                    "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
                ],
            ),
        },
        {
            "path": "tmp/active_wave_plan.md",
            "matched_lines": extract_matching_lines(
                inputs["active_wave_plan_text"],
                needles=[
                    "r57_origin_accelerated_trace_vm_comparator_gate",
                    "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
                ],
            ),
        },
        {
            "derived": {
                "lane_verdict": lane_verdict,
                "selected_h52_outcome": selected_h52_outcome,
            }
        },
    ]


def main() -> None:
    inputs = load_inputs()
    tasks = build_task_manifest()
    r56_first_failure = inputs["r56_execution_report"]["first_failure"]

    comparator_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None

    for task in tasks:
        row, task_first_failure = evaluate_task(task, r56_first_failure=r56_first_failure)
        comparator_rows.append(row)
        if first_failure is None and task_first_failure is not None:
            first_failure = task_first_failure

    accelerated_exact_count = sum(
        int(bool(row["accelerated_exact_trace_match"]) and bool(row["accelerated_exact_final_state_match"]))
        for row in comparator_rows
    )
    linear_exact_count = sum(
        int(bool(row["linear_exact_trace_match"]) and bool(row["linear_exact_final_state_match"]))
        for row in comparator_rows
    )
    external_exact_count = sum(
        int(bool(row["external_exact_trace_match"]) and bool(row["external_exact_final_state_match"]))
        for row in comparator_rows
    )
    accelerated_faster_than_linear_count = sum(int(bool(row["accelerated_faster_than_linear"])) for row in comparator_rows)
    accelerated_faster_than_external_count = sum(
        int(bool(row["accelerated_faster_than_external"])) for row in comparator_rows
    )
    mean_accelerated_seconds = mean(float(row["accelerated_mean_seconds"]) for row in comparator_rows)
    mean_linear_seconds = mean(float(row["linear_mean_seconds"]) for row in comparator_rows)
    mean_external_seconds = mean(float(row["external_mean_seconds"]) for row in comparator_rows)
    total_transition_count = sum(int(row["transition_count"]) for row in comparator_rows)
    total_internal_read_count = sum(int(row["accelerated_read_count"]) for row in comparator_rows)
    overall_internal_retrieval_share = total_internal_read_count / total_transition_count if total_transition_count else 0.0

    comparator_exact = (
        len(comparator_rows) > 0
        and accelerated_exact_count == len(comparator_rows)
        and linear_exact_count == len(comparator_rows)
        and external_exact_count == len(comparator_rows)
    )
    bounded_value_positive = (
        comparator_exact
        and accelerated_faster_than_linear_count >= 3
        and accelerated_faster_than_external_count >= 3
        and mean_accelerated_seconds < mean_linear_seconds
        and mean_accelerated_seconds < mean_external_seconds
    )

    if not comparator_exact:
        lane_verdict = "accelerated_trace_vm_comparator_exactness_broke"
        selected_h52_outcome = "stop_as_partial_mechanism_only"
    elif bounded_value_positive:
        lane_verdict = "accelerated_trace_vm_retains_bounded_value"
        selected_h52_outcome = "freeze_origin_mechanism_supported_with_fastpath_value"
    else:
        lane_verdict = "accelerated_trace_vm_lacks_bounded_value"
        selected_h52_outcome = "freeze_origin_mechanism_supported_without_fastpath_value"

    trace_length_sensitivity = build_trace_length_sensitivity(comparator_rows)

    summary_fields = {
        "current_active_docs_only_stage": "h51_post_h50_origin_mechanism_reentry_packet",
        "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "current_planning_bundle": "f28_post_h50_origin_mechanism_reentry_bundle",
        "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
        "preserved_exact_retrieval_gate": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
        "preserved_exact_trace_vm_gate": "r56_origin_append_only_trace_vm_semantics_gate",
        "active_runtime_lane": "r57_origin_accelerated_trace_vm_comparator_gate",
        "lane_verdict": lane_verdict,
        "planned_task_count": len(comparator_rows),
        "executed_task_count": len(comparator_rows),
        "accelerated_exact_task_count": accelerated_exact_count,
        "linear_exact_task_count": linear_exact_count,
        "external_exact_task_count": external_exact_count,
        "accelerated_faster_than_linear_count": accelerated_faster_than_linear_count,
        "accelerated_faster_than_external_count": accelerated_faster_than_external_count,
        "mean_accelerated_seconds": mean_accelerated_seconds,
        "mean_linear_seconds": mean_linear_seconds,
        "mean_external_seconds": mean_external_seconds,
        "overall_internal_retrieval_share_of_transitions": overall_internal_retrieval_share,
        "trace_length_bucket_count": len(trace_length_sensitivity),
        "first_failure_route": None if first_failure is None else first_failure["route"],
        "first_failure_task_id": None if first_failure is None else first_failure["task_id"],
        "selected_h52_outcome": selected_h52_outcome,
        "next_required_packet": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
    }

    checklist_rows = build_checklist_rows(
        inputs,
        comparator_rows,
        lane_verdict=lane_verdict,
        first_failure=first_failure,
    )
    claim_packet = build_claim_packet(lane_verdict, summary_fields=summary_fields)
    snapshot_rows = build_snapshot(
        inputs,
        lane_verdict=lane_verdict,
        selected_h52_outcome=selected_h52_outcome,
    )

    summary_payload = {
        "summary": {
            "current_active_docs_only_stage": summary_fields["current_active_docs_only_stage"],
            "preserved_prior_docs_only_closeout": summary_fields["preserved_prior_docs_only_closeout"],
            "current_paper_grade_endpoint": summary_fields["current_paper_grade_endpoint"],
            "current_planning_bundle": summary_fields["current_planning_bundle"],
            "current_low_priority_wave": summary_fields["current_low_priority_wave"],
            "preserved_exact_retrieval_gate": summary_fields["preserved_exact_retrieval_gate"],
            "preserved_exact_trace_vm_gate": summary_fields["preserved_exact_trace_vm_gate"],
            "active_runtime_lane": summary_fields["active_runtime_lane"],
            "gate": {
                "lane_verdict": summary_fields["lane_verdict"],
                "planned_task_count": summary_fields["planned_task_count"],
                "executed_task_count": summary_fields["executed_task_count"],
                "accelerated_exact_task_count": summary_fields["accelerated_exact_task_count"],
                "linear_exact_task_count": summary_fields["linear_exact_task_count"],
                "external_exact_task_count": summary_fields["external_exact_task_count"],
                "accelerated_faster_than_linear_count": summary_fields["accelerated_faster_than_linear_count"],
                "accelerated_faster_than_external_count": summary_fields["accelerated_faster_than_external_count"],
                "mean_accelerated_seconds": summary_fields["mean_accelerated_seconds"],
                "mean_linear_seconds": summary_fields["mean_linear_seconds"],
                "mean_external_seconds": summary_fields["mean_external_seconds"],
                "overall_internal_retrieval_share_of_transitions": summary_fields[
                    "overall_internal_retrieval_share_of_transitions"
                ],
                "trace_length_bucket_count": summary_fields["trace_length_bucket_count"],
                "first_failure_route": summary_fields["first_failure_route"],
                "first_failure_task_id": summary_fields["first_failure_task_id"],
                "selected_h52_outcome": summary_fields["selected_h52_outcome"],
                "next_required_packet": summary_fields["next_required_packet"],
            },
            "pass_count": sum(1 for row in checklist_rows if row["status"] == "pass"),
            "blocked_count": sum(1 for row in checklist_rows if row["status"] != "pass"),
            "blocked_items": [row["item_id"] for row in checklist_rows if row["status"] != "pass"],
        },
        "runtime_environment": environment_payload(),
    }

    execution_report = {
        "comparator_rows": comparator_rows,
        "trace_length_sensitivity": trace_length_sensitivity,
        "first_failure": first_failure,
        "first_failure_carry_over": {
            "r56_first_failure": r56_first_failure,
            "r57_first_failure": first_failure,
        },
    }

    write_json(OUT_DIR / "summary.json", summary_payload)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", claim_packet)
    write_json(OUT_DIR / "execution_report.json", execution_report)
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
