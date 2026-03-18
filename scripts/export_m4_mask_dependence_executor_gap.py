"""Export the next-stage staged-pointer mask-dependence analysis for M4-D."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import json
from pathlib import Path

from exec_trace import (
    TraceInterpreter,
    Program,
    alternating_memory_loop_program,
    countdown_program,
    dynamic_latest_write_program,
    dynamic_memory_transfer_program,
    equality_branch_program,
    flagged_indirect_accumulator_program,
    latest_write_program,
    loop_indirect_memory_program,
    selector_checkpoint_bank_program,
    stack_memory_ping_pong_program,
)
from model import (
    FactorizedEventModelConfig,
    FactorizedEventTrainingConfig,
    PointerEventCodec,
    evaluate_pointer_event_model,
    run_free_running_with_pointer_event_model,
    train_pointer_event_model,
)
from model.free_running_executor import (
    FreeRunningExecutionResult,
    ProgramExecutionOutcome,
    compare_execution_to_reference,
)
from model.trainable_latest_write import bucket_name
from utils import detect_runtime_environment


HEAD_PRIORITY = (
    "branch_expr",
    "next_pc_mode",
    "memory_read_address_expr",
    "memory_write_address_expr",
    "memory_write_value_expr",
    "stack_read_count",
    "pop_count",
    "push_count",
    "push_expr_0",
    "push_expr_1",
    "halted",
)

HEAD_TO_CLASS = {
    "branch_expr": "control_flow",
    "next_pc_mode": "control_flow",
    "memory_read_address_expr": "memory_address",
    "memory_write_address_expr": "memory_address",
    "memory_write_value_expr": "memory_value",
    "stack_read_count": "stack_shape",
    "pop_count": "stack_shape",
    "push_count": "stack_shape",
    "push_expr_0": "memory_value",
    "push_expr_1": "memory_value",
    "halted": "termination",
}

RECOMMENDED_MODE_BY_CLASS = {
    "control_flow": "control_flow_compatible",
    "memory_address": "memory_address_compatible",
    "memory_value": "memory_value_compatible",
}

PRIMARY_REGIMES = ("structural", "opcode_shape", "opcode_legal")


@dataclass(frozen=True, slots=True)
class ProgramSpec:
    split: str
    family: str
    program: Program


def encode_metrics(metrics):
    return {
        "loss": metrics.loss,
        "exact_label_accuracy": metrics.exact_label_accuracy,
        "example_count": metrics.example_count,
        "head_accuracies": [{"head": head, "accuracy": accuracy} for head, accuracy in metrics.head_accuracies],
    }


def rollout_budget(program: Program) -> int:
    return max(128, len(program.instructions) * 16)


def encode_event(event) -> dict[str, object]:
    return {
        "step": event.step,
        "pc": event.pc,
        "opcode": event.opcode,
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


def encode_value(value: object) -> object:
    if isinstance(value, tuple):
        return [encode_value(item) for item in value]
    return value


def build_stack_befores(events) -> dict[int, tuple[int, ...]]:
    stack: list[int] = []
    stack_befores: dict[int, tuple[int, ...]] = {}
    for event in events:
        stack_befores[event.step] = tuple(stack)
        if event.popped:
            del stack[-len(event.popped) :]
        stack.extend(event.pushed)
    return stack_befores


def build_reference_result(program: Program, interpreter: TraceInterpreter) -> FreeRunningExecutionResult:
    reference = interpreter.run(program)
    return FreeRunningExecutionResult(
        program=program,
        events=reference.events,
        final_state=reference.final_state,
        read_observations=(),
        stack_strategy="linear",
        memory_strategy="linear",
    )


def label_head_value(label, head: str) -> object:
    if head == "push_expr_0":
        return label.push_exprs[0]
    if head == "push_expr_1":
        return label.push_exprs[1]
    return getattr(label, head)


def compare_events(
    codec: PointerEventCodec,
    program: Program,
    reference_events,
    produced_events,
    *,
    first_mismatch_step: int,
) -> dict[str, object]:
    if first_mismatch_step >= len(reference_events) or first_mismatch_step >= len(produced_events):
        return {
            "program_name": program.name,
            "diagnostic_source": "trace_mismatch",
            "first_error_class": "termination",
            "first_error_head": "halted",
            "reference_label": first_mismatch_step < len(reference_events),
            "predicted_label": first_mismatch_step < len(produced_events),
            "all_differing_heads": ["halted"],
            "context": {
                "program_name": program.name,
                "step": first_mismatch_step,
                "opcode": None,
            },
            "expected_event": None if first_mismatch_step >= len(reference_events) else encode_event(reference_events[first_mismatch_step]),
            "produced_event": None if first_mismatch_step >= len(produced_events) else encode_event(produced_events[first_mismatch_step]),
        }

    reference_stack_befores = build_stack_befores(reference_events)
    produced_stack_befores = build_stack_befores(produced_events)
    expected_event = reference_events[first_mismatch_step]
    produced_event = produced_events[first_mismatch_step]
    expected_label = codec.label_from_event(
        expected_event,
        stack_before=reference_stack_befores[first_mismatch_step],
    )
    produced_label = codec.label_from_event(
        produced_event,
        stack_before=produced_stack_befores[first_mismatch_step],
    )

    differing_heads = [
        head
        for head in HEAD_PRIORITY
        if label_head_value(expected_label, head) != label_head_value(produced_label, head)
    ]
    if not differing_heads:
        if expected_event.halted != produced_event.halted:
            differing_heads = ["halted"]
        elif expected_event.next_pc != produced_event.next_pc or expected_event.branch_taken != produced_event.branch_taken:
            differing_heads = ["next_pc_mode"]
        elif (
            expected_event.memory_read_address != produced_event.memory_read_address
            or expected_event.memory_write != produced_event.memory_write
        ):
            differing_heads = ["memory_write_address_expr"]
        else:
            differing_heads = ["push_expr_0"]

    first_head = differing_heads[0]
    return {
        "program_name": program.name,
        "diagnostic_source": "trace_mismatch",
        "first_error_class": HEAD_TO_CLASS[first_head],
        "first_error_head": first_head,
        "reference_label": encode_value(label_head_value(expected_label, first_head)),
        "predicted_label": encode_value(label_head_value(produced_label, first_head)),
        "all_differing_heads": differing_heads,
        "context": {
            "program_name": program.name,
            "step": expected_event.step,
            "pc": expected_event.pc,
            "opcode": expected_event.opcode,
            "arg": expected_event.arg,
            "stack_depth_before": expected_event.stack_depth_before,
        },
        "expected_event": encode_event(expected_event),
        "produced_event": encode_event(produced_event),
    }


def classify_runtime_exception(program: Program, failure_reason: str) -> dict[str, object]:
    lowered = failure_reason.lower()
    if "program counter out of range" in lowered:
        error_class = "control_flow"
        head = "next_pc_mode"
    elif "stack underflow" in lowered:
        error_class = "stack_shape"
        head = "pop_count"
    elif "negative memory-read address" in lowered or "read before any write" in lowered:
        error_class = "memory_address"
        head = "memory_read_address_expr"
    elif "negative memory-write address" in lowered:
        error_class = "memory_address"
        head = "memory_write_address_expr"
    elif "address" in lowered:
        error_class = "memory_address"
        head = "memory_read_address_expr"
    elif "maximum step budget exceeded" in lowered:
        error_class = "rollout_nontermination"
        head = "step_budget"
    elif "exact read mismatch" in lowered:
        error_class = "retrieval_exactness"
        head = "exact_read"
    else:
        error_class = "runtime_exception"
        head = "runtime_exception"

    return {
        "program_name": program.name,
        "diagnostic_source": "runtime_exception",
        "first_error_class": error_class,
        "first_error_head": head,
        "reference_label": None,
        "predicted_label": failure_reason,
        "all_differing_heads": [head],
        "context": {
            "program_name": program.name,
            "step": None,
            "opcode": None,
        },
        "expected_event": None,
        "produced_event": None,
    }


def classify_diagnostic_exception(program: Program, failure_reason: str) -> dict[str, object]:
    return {
        "program_name": program.name,
        "diagnostic_source": "diagnostic_exception",
        "first_error_class": "diagnostic_exception",
        "first_error_head": "diagnostic_exception",
        "reference_label": None,
        "predicted_label": failure_reason,
        "all_differing_heads": ["diagnostic_exception"],
        "context": {
            "program_name": program.name,
            "step": None,
            "opcode": None,
        },
        "expected_event": None,
        "produced_event": None,
    }


def evaluate_regime(
    specs: tuple[ProgramSpec, ...],
    fit,
    *,
    mask_mode: str,
    interpreter: TraceInterpreter,
) -> dict[str, object]:
    outcomes: list[ProgramExecutionOutcome] = []
    diagnostics: list[dict[str, object]] = []
    bucket_state: dict[str, dict[str, int]] = {}

    for spec in specs:
        reference = build_reference_result(spec.program, interpreter)
        diagnostic = None
        try:
            execution = run_free_running_with_pointer_event_model(
                spec.program,
                fit,
                decode_mode="accelerated",
                max_steps=rollout_budget(spec.program),
                mask_mode=mask_mode,
            )
            outcome = compare_execution_to_reference(spec.program, execution, reference=reference)
            if not outcome.exact_trace_match:
                mismatch_step = outcome.first_mismatch_step
                if mismatch_step is None:
                    mismatch_step = min(len(execution.events), len(reference.events))
                try:
                    diagnostic = compare_events(
                        fit.codec,
                        spec.program,
                        reference.events,
                        execution.events,
                        first_mismatch_step=mismatch_step,
                    )
                except Exception as exc:
                    diagnostic = classify_diagnostic_exception(spec.program, str(exc))
        except Exception as exc:
            outcome = ProgramExecutionOutcome(
                program_name=spec.program.name,
                program_steps=reference.final_state.steps,
                exact_trace_match=False,
                exact_final_state_match=False,
                first_mismatch_step=None,
                failure_reason=str(exc),
            )
            diagnostic = classify_runtime_exception(spec.program, str(exc))

        bucket = bucket_name(outcome.program_steps)
        counts = bucket_state.setdefault(bucket, {"program_count": 0, "exact_trace_count": 0, "exact_final_state_count": 0})
        counts["program_count"] += 1
        counts["exact_trace_count"] += int(outcome.exact_trace_match)
        counts["exact_final_state_count"] += int(outcome.exact_final_state_match)

        encoded_outcome = {
            "family": spec.family,
            "split": spec.split,
            "program_name": outcome.program_name,
            "program_steps": outcome.program_steps,
            "exact_trace_match": outcome.exact_trace_match,
            "exact_final_state_match": outcome.exact_final_state_match,
            "first_mismatch_step": outcome.first_mismatch_step,
            "failure_reason": outcome.failure_reason,
            "rollout_budget": rollout_budget(spec.program),
        }
        outcomes.append(ProgramExecutionOutcome(**{k: encoded_outcome[k] for k in (
            "program_name",
            "program_steps",
            "exact_trace_match",
            "exact_final_state_match",
            "first_mismatch_step",
            "failure_reason",
        )}))
        if diagnostic is not None:
            diagnostics.append(
                {
                    **encoded_outcome,
                    **diagnostic,
                }
            )
        else:
            diagnostics.append(
                {
                    **encoded_outcome,
                    "first_error_class": None,
                    "first_error_head": None,
                    "diagnostic_source": "exact_match",
                    "reference_label": None,
                    "predicted_label": None,
                    "all_differing_heads": [],
                    "context": None,
                    "expected_event": None,
                    "produced_event": None,
                }
            )

    by_bucket = [
        {
            "bucket": bucket,
            "program_count": counts["program_count"],
            "exact_trace_accuracy": counts["exact_trace_count"] / counts["program_count"],
            "exact_final_state_accuracy": counts["exact_final_state_count"] / counts["program_count"],
        }
        for bucket, counts in sorted(bucket_state.items())
    ]
    exact_trace_total = sum(int(outcome.exact_trace_match) for outcome in outcomes)
    exact_final_state_total = sum(int(outcome.exact_final_state_match) for outcome in outcomes)
    program_count = len(outcomes)

    family_rows = []
    for family in sorted({spec.family for spec in specs}):
        family_outcomes = [row for row in diagnostics if row["family"] == family]
        family_rows.append(
            {
                "family": family,
                "program_count": len(family_outcomes),
                "exact_trace_accuracy": sum(int(row["exact_trace_match"]) for row in family_outcomes) / len(family_outcomes),
                "exact_final_state_accuracy": sum(int(row["exact_final_state_match"]) for row in family_outcomes)
                / len(family_outcomes),
            }
        )

    failure_rows = [row for row in diagnostics if not row["exact_trace_match"]]
    by_source = Counter(row["diagnostic_source"] for row in failure_rows if row["diagnostic_source"] is not None)
    by_class = Counter(row["first_error_class"] for row in failure_rows if row["first_error_class"] is not None)
    by_head = Counter(row["first_error_head"] for row in failure_rows if row["first_error_head"] is not None)

    return {
        "exact_trace_accuracy": exact_trace_total / program_count if program_count else 0.0,
        "exact_final_state_accuracy": exact_final_state_total / program_count if program_count else 0.0,
        "program_count": program_count,
        "by_length_bucket": by_bucket,
        "by_family": family_rows,
        "outcomes": diagnostics,
        "failure_taxonomy": {
            "failed_program_count": len(failure_rows),
            "by_source": [{"diagnostic_source": key, "count": value} for key, value in sorted(by_source.items())],
            "by_class": [{"first_error_class": key, "count": value} for key, value in sorted(by_class.items())],
            "by_head": [{"first_error_head": key, "count": value} for key, value in sorted(by_head.items())],
        },
    }


def decide_fourth_regime(heldout_opcode_shape_outcomes: list[dict[str, object]]) -> dict[str, object]:
    failures = [row for row in heldout_opcode_shape_outcomes if not row["exact_trace_match"]]
    if not failures:
        return {
            "fourth_regime_justified": False,
            "recommended_mode": None,
            "reason": "opcode_shape already reaches exact held-out rollout on the current suite.",
            "support_ratio": 0.0,
        }

    class_counts = Counter(row["first_error_class"] for row in failures if row["first_error_class"] is not None)
    head_counts = Counter(row["first_error_head"] for row in failures if row["first_error_head"] is not None)
    if not class_counts or not head_counts:
        return {
            "fourth_regime_justified": False,
            "recommended_mode": None,
            "reason": "opcode_shape failures were not attributable to a stable class/head pair.",
            "support_ratio": 0.0,
        }

    dominant_class, dominant_class_count = class_counts.most_common(1)[0]
    dominant_head, dominant_head_count = head_counts.most_common(1)[0]
    support_ratio = min(dominant_class_count / len(failures), dominant_head_count / len(failures))
    recommended_mode = RECOMMENDED_MODE_BY_CLASS.get(dominant_class)

    if support_ratio < 0.7:
        return {
            "fourth_regime_justified": False,
            "recommended_mode": None,
            "reason": "opcode_shape failures remain too dispersed across classes/heads.",
            "support_ratio": support_ratio,
            "dominant_class": dominant_class,
            "dominant_head": dominant_head,
        }
    if recommended_mode is None:
        return {
            "fourth_regime_justified": False,
            "recommended_mode": None,
            "reason": f"dominant failure class {dominant_class!r} has no matched fourth regime.",
            "support_ratio": support_ratio,
            "dominant_class": dominant_class,
            "dominant_head": dominant_head,
        }

    return {
        "fourth_regime_justified": True,
        "recommended_mode": recommended_mode,
        "reason": "opcode_shape failures concentrate strongly enough to justify one narrower compatibility regime.",
        "support_ratio": support_ratio,
        "dominant_class": dominant_class,
        "dominant_head": dominant_head,
    }


def build_program_specs() -> tuple[tuple[ProgramSpec, ...], tuple[ProgramSpec, ...]]:
    train_specs = (
        *(ProgramSpec("train", "countdown", countdown_program(start)) for start in range(0, 7)),
        ProgramSpec("train", "equality_branch", equality_branch_program(0, 0)),
        ProgramSpec("train", "equality_branch", equality_branch_program(0, 1)),
        ProgramSpec("train", "latest_write", latest_write_program()),
        ProgramSpec("train", "dynamic_latest_write", dynamic_latest_write_program()),
        ProgramSpec("train", "loop_indirect_memory", loop_indirect_memory_program(2)),
        ProgramSpec("train", "loop_indirect_memory", loop_indirect_memory_program(4)),
        ProgramSpec("train", "stack_memory_ping_pong", stack_memory_ping_pong_program()),
        ProgramSpec("train", "alternating_memory_loop", alternating_memory_loop_program(2)),
        ProgramSpec("train", "alternating_memory_loop", alternating_memory_loop_program(4, base_address=16)),
        ProgramSpec("train", "flagged_indirect_accumulator", flagged_indirect_accumulator_program(2, base_address=8)),
        ProgramSpec("train", "flagged_indirect_accumulator", flagged_indirect_accumulator_program(4, base_address=24)),
        ProgramSpec("train", "selector_checkpoint_bank", selector_checkpoint_bank_program(2, base_address=32)),
        ProgramSpec("train", "selector_checkpoint_bank", selector_checkpoint_bank_program(4, base_address=48)),
    )
    heldout_specs = (
        *(ProgramSpec("heldout", "countdown", countdown_program(start)) for start in range(7, 11)),
        ProgramSpec("heldout", "equality_branch", equality_branch_program(5, 5)),
        ProgramSpec("heldout", "equality_branch", equality_branch_program(2, 9)),
        ProgramSpec("heldout", "dynamic_memory_transfer", dynamic_memory_transfer_program()),
        ProgramSpec("heldout", "loop_indirect_memory", loop_indirect_memory_program(6)),
        ProgramSpec("heldout", "stack_memory_ping_pong", stack_memory_ping_pong_program(base_address=32)),
        ProgramSpec("heldout", "alternating_memory_loop", alternating_memory_loop_program(6)),
        ProgramSpec("heldout", "alternating_memory_loop", alternating_memory_loop_program(5, base_address=48)),
        ProgramSpec("heldout", "flagged_indirect_accumulator", flagged_indirect_accumulator_program(6, base_address=64)),
        ProgramSpec("heldout", "flagged_indirect_accumulator", flagged_indirect_accumulator_program(5, base_address=96)),
        ProgramSpec("heldout", "selector_checkpoint_bank", selector_checkpoint_bank_program(6, base_address=128)),
        ProgramSpec("heldout", "selector_checkpoint_bank", selector_checkpoint_bank_program(5, base_address=160)),
    )
    return (train_specs, heldout_specs)


def main() -> None:
    environment = detect_runtime_environment()
    interpreter = TraceInterpreter()
    train_specs, heldout_specs = build_program_specs()
    model_config = FactorizedEventModelConfig(
        d_model=96,
        n_heads=4,
        n_layers=3,
        d_ffn=192,
        opcode_dim=16,
        history_window=16,
        max_scalar=256,
        max_address=1024,
        max_pc=128,
        include_top_values=True,
    )
    training_config = FactorizedEventTrainingConfig(
        epochs=32,
        batch_size=16,
        learning_rate=3e-3,
    )

    run = train_pointer_event_model(
        [spec.program for spec in train_specs],
        eval_programs=[spec.program for spec in heldout_specs],
        model_config=model_config,
        training_config=training_config,
    )

    rollout = {
        mask_mode: {
            "train_programs": evaluate_regime(train_specs, run, mask_mode=mask_mode, interpreter=interpreter),
            "heldout_programs": evaluate_regime(heldout_specs, run, mask_mode=mask_mode, interpreter=interpreter),
        }
        for mask_mode in PRIMARY_REGIMES
    }

    decision = decide_fourth_regime(rollout["opcode_shape"]["heldout_programs"]["outcomes"])
    if decision["fourth_regime_justified"]:
        recommended_mode = decision["recommended_mode"]
        rollout[recommended_mode] = {
            "train_programs": evaluate_regime(train_specs, run, mask_mode=recommended_mode, interpreter=interpreter),
            "heldout_programs": evaluate_regime(heldout_specs, run, mask_mode=recommended_mode, interpreter=interpreter),
        }

    summary = {
        "experiment": "m4_mask_dependence_executor_gap",
        "environment": environment.as_dict(),
        "notes": [
            "This batch asks whether staged exactness survives fairer decode regimes once two harder held-out families are added.",
            "The default ladder remains structural, opcode_shape, and opcode_legal; a fourth regime is only evaluated if opcode_shape failures concentrate strongly enough.",
            "The staged pointer result is interpreted as a mechanistic bridge only if its dependence on decode legality remains explicit.",
        ],
        "model_config": asdict(model_config),
        "training_config": asdict(training_config),
        "train_metrics": encode_metrics(run.train_metrics),
        "eval_metrics": None if run.eval_metrics is None else encode_metrics(run.eval_metrics),
        "teacher_forced_groups": {
            "train_programs": encode_metrics(
                evaluate_pointer_event_model(run.model, run.codec, run.codec.build_examples([spec.program for spec in train_specs]), device=run.device)
            ),
            "heldout_programs": encode_metrics(
                evaluate_pointer_event_model(
                    run.model,
                    run.codec,
                    run.codec.build_examples([spec.program for spec in heldout_specs]),
                    device=run.device,
                )
            ),
        },
        "programs": {
            "train": [{"family": spec.family, "program_name": spec.program.name} for spec in train_specs],
            "heldout": [{"family": spec.family, "program_name": spec.program.name} for spec in heldout_specs],
        },
        "rollout": rollout,
        "regime_decision": decision,
    }

    out_dir = Path("results/M4_mask_dependence_executor_gap")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    per_program = []
    for mask_mode, groups in rollout.items():
        for group_name, group in groups.items():
            for row in group["outcomes"]:
                per_program.append({"mask_mode": mask_mode, "group": group_name, **row})
    (out_dir / "per_program_failure_digest.json").write_text(json.dumps(per_program, indent=2), encoding="utf-8")
    (out_dir / "regime_decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")
    print((out_dir / "summary.json").as_posix())


if __name__ == "__main__":
    main()
