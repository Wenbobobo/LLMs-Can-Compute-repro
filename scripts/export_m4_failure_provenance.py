"""Export mechanistic provenance for staged-pointer failures after M4-D."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
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
from exec_trace.dsl import TraceEvent
from model import FactorizedEventModelConfig, FactorizedEventTrainingConfig, PointerEventCodec, train_pointer_event_model
from model.free_running_executor import _LatestWriteSpace, ReadObservation
from model.staged_pointer_event_models import PointerEventExecutor
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

ROOT_CAUSE_BY_CLASS = {
    "control_flow": "control_flow_root_cause",
    "memory_value": "memory_value_root_cause",
    "memory_address": "memory_address_root_cause",
    "stack_shape": "stack_shape_root_cause",
}


@dataclass(frozen=True, slots=True)
class ProgramSpec:
    split: str
    family: str
    program: Program


@dataclass(frozen=True, slots=True)
class PartialRollout:
    events: tuple[TraceEvent, ...]
    failure_reason: str | None
    halted: bool


def rollout_budget(program: Program) -> int:
    return max(128, len(program.instructions) * 16)


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
    return train_specs, heldout_specs


def build_stack_befores(events: tuple[TraceEvent, ...]) -> dict[int, tuple[int, ...]]:
    stack: list[int] = []
    stack_befores: dict[int, tuple[int, ...]] = {}
    for event in events:
        stack_befores[event.step] = tuple(stack)
        if event.popped:
            del stack[-len(event.popped) :]
        stack.extend(event.pushed)
    return stack_befores


def label_head_value(label, head: str) -> object:
    if head == "push_expr_0":
        return label.push_exprs[0]
    if head == "push_expr_1":
        return label.push_exprs[1]
    return getattr(label, head)


def encode_event(event: TraceEvent | None) -> dict[str, object] | None:
    if event is None:
        return None
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


def first_mismatch_step(reference_events: tuple[TraceEvent, ...], produced_events: tuple[TraceEvent, ...]) -> int | None:
    for produced, expected in zip(produced_events, reference_events):
        if produced != expected:
            return produced.step
    if len(produced_events) != len(reference_events):
        return min(len(produced_events), len(reference_events))
    return None


def compare_events(codec: PointerEventCodec, program: Program, reference_events, produced_events, *, mismatch_step: int) -> dict[str, object]:
    if mismatch_step >= len(reference_events) or mismatch_step >= len(produced_events):
        return {
            "first_error_class": "termination",
            "first_error_head": "halted",
            "context": {"step": mismatch_step, "opcode": None},
            "expected_event": encode_event(reference_events[mismatch_step] if mismatch_step < len(reference_events) else None),
            "produced_event": encode_event(produced_events[mismatch_step] if mismatch_step < len(produced_events) else None),
        }

    reference_stack_befores = build_stack_befores(reference_events)
    produced_stack_befores = build_stack_befores(produced_events)
    expected_event = reference_events[mismatch_step]
    produced_event = produced_events[mismatch_step]
    expected_label = codec.label_from_event(expected_event, stack_before=reference_stack_befores[mismatch_step])
    produced_label = codec.label_from_event(produced_event, stack_before=produced_stack_befores[mismatch_step])
    differing_heads = [
        head
        for head in HEAD_PRIORITY
        if label_head_value(expected_label, head) != label_head_value(produced_label, head)
    ]
    first_head = differing_heads[0] if differing_heads else "halted"
    return {
        "first_error_class": HEAD_TO_CLASS[first_head],
        "first_error_head": first_head,
        "context": {"step": mismatch_step, "opcode": expected_event.opcode, "pc": expected_event.pc},
        "expected_event": encode_event(expected_event),
        "produced_event": encode_event(produced_event),
    }


def run_partial_rollout(program: Program, run, *, mask_mode: str, max_steps: int) -> PartialRollout:
    executor = PointerEventExecutor(
        run.model,
        run.codec,
        device=run.device,
        include_top_values=run.codec.config.include_top_values,
        stack_strategy="accelerated",
        memory_strategy="accelerated",
        mask_mode=mask_mode,
    )
    stack_history = _LatestWriteSpace(epsilon=Fraction(1, max_steps + 2), default_value=0, allow_default_reads=False)
    memory_history = _LatestWriteSpace(epsilon=Fraction(1, max_steps + 2), default_value=0, allow_default_reads=True)
    read_observations: list[ReadObservation] = []
    events: list[TraceEvent] = []
    step = 0
    pc = 0
    stack_depth = 0
    halted = False
    executor._recent_history = []
    try:
        while not halted:
            if step >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= pc < len(program)):
                raise RuntimeError(f"Program counter out of range: {pc}")
            instruction = program.instructions[pc]
            popped, pushed, branch_taken, memory_read, memory_write, next_pc, halted = executor._execute_instruction(
                step=step,
                pc=pc,
                stack_depth=stack_depth,
                instruction=instruction.opcode,
                arg=instruction.arg,
                stack_history=stack_history,
                memory_history=memory_history,
                read_observations=read_observations,
            )
            event = TraceEvent(
                step=step,
                pc=pc,
                opcode=instruction.opcode,
                arg=instruction.arg,
                popped=popped,
                pushed=pushed,
                branch_taken=branch_taken,
                memory_read_address=None if memory_read is None else memory_read[0],
                memory_read_value=None if memory_read is None else memory_read[1],
                memory_write=memory_write,
                next_pc=next_pc,
                stack_depth_before=stack_depth,
                stack_depth_after=stack_depth - len(popped) + len(pushed),
                halted=halted,
            )
            events.append(event)
            write_base = stack_depth - len(popped)
            for offset, value in enumerate(pushed):
                stack_history.write(write_base + offset, value, step)
            if memory_write is not None:
                memory_history.write(memory_write[0], memory_write[1], step)
            step += 1
            pc = next_pc
            stack_depth = event.stack_depth_after
        return PartialRollout(tuple(events), None, True)
    except Exception as exc:
        return PartialRollout(tuple(events), str(exc), False)
    finally:
        executor._recent_history = []


def provenance_row(spec: ProgramSpec, *, mask_mode: str, run, interpreter: TraceInterpreter) -> dict[str, object]:
    reference = interpreter.run(spec.program)
    produced = run_partial_rollout(spec.program, run, mask_mode=mask_mode, max_steps=rollout_budget(spec.program))
    mismatch_step = first_mismatch_step(reference.events, produced.events)
    diagnostic = None if mismatch_step is None else compare_events(run.codec, spec.program, reference.events, produced.events, mismatch_step=mismatch_step)

    provenance_class = "exact_match"
    root_cause_head = None
    root_cause_class = None
    if produced.failure_reason is None and tuple(produced.events) == tuple(reference.events):
        exact_trace_match = True
    else:
        exact_trace_match = False
        if produced.failure_reason and "maximum step budget exceeded" in produced.failure_reason.lower():
            if diagnostic is None:
                provenance_class = "genuine_recurrent_nontermination"
            else:
                provenance_class = "downstream_nontermination_after_semantic_error"
                root_cause_head = diagnostic["first_error_head"]
                root_cause_class = ROOT_CAUSE_BY_CLASS.get(diagnostic["first_error_class"])
        elif diagnostic is not None:
            provenance_class = ROOT_CAUSE_BY_CLASS.get(diagnostic["first_error_class"], "runtime_exception_unattributed")
            root_cause_head = diagnostic["first_error_head"]
            root_cause_class = provenance_class if provenance_class.endswith("_root_cause") else None
        else:
            provenance_class = "runtime_exception_unattributed"

    return {
        "mask_mode": mask_mode,
        "split": spec.split,
        "family": spec.family,
        "program_name": spec.program.name,
        "program_steps": reference.final_state.steps,
        "rollout_budget": rollout_budget(spec.program),
        "exact_trace_match": exact_trace_match,
        "exact_final_state_match": exact_trace_match,
        "first_mismatch_step": mismatch_step,
        "provenance_class": provenance_class,
        "root_cause_class": root_cause_class,
        "root_cause_head": root_cause_head,
        "failure_reason": produced.failure_reason,
        "diagnostic": diagnostic,
    }


def summarize_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    failures = [row for row in rows if not row["exact_trace_match"]]
    return {
        "program_count": len(rows),
        "failed_program_count": len(failures),
        "by_provenance_class": [
            {"provenance_class": key, "count": value}
            for key, value in sorted(Counter(row["provenance_class"] for row in failures).items())
        ],
        "by_root_cause_head": [
            {"root_cause_head": key, "count": value}
            for key, value in sorted(Counter(row["root_cause_head"] for row in failures if row["root_cause_head"] is not None).items())
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    interpreter = TraceInterpreter()
    train_specs, heldout_specs = build_program_specs()
    run = train_pointer_event_model(
        [spec.program for spec in train_specs],
        eval_programs=[spec.program for spec in heldout_specs],
        model_config=FactorizedEventModelConfig(
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
        ),
        training_config=FactorizedEventTrainingConfig(
            epochs=32,
            batch_size=16,
            learning_rate=3e-3,
            seed=0,
        ),
    )

    per_program_rows: list[dict[str, object]] = []
    summary = {
        "experiment": "m4_failure_provenance",
        "environment": environment.as_dict(),
        "notes": [
            "This batch keeps the staged checkpoint family fixed and asks whether step-budget rows are primary failures or downstream symptoms.",
            "The exporter captures the produced prefix before runtime failure so first semantic divergence can be recovered.",
            "No new decode regime is introduced here; the goal is attribution rather than rescue.",
        ],
        "mask_modes": {},
    }
    for mask_mode in ("structural", "opcode_shape", "opcode_legal"):
        train_rows = [provenance_row(spec, mask_mode=mask_mode, run=run, interpreter=interpreter) for spec in train_specs]
        heldout_rows = [provenance_row(spec, mask_mode=mask_mode, run=run, interpreter=interpreter) for spec in heldout_specs]
        per_program_rows.extend(train_rows)
        per_program_rows.extend(heldout_rows)
        summary["mask_modes"][mask_mode] = {
            "train_programs": summarize_rows(train_rows),
            "heldout_programs": summarize_rows(heldout_rows),
        }

    heldout_opcode_shape = [
        row
        for row in per_program_rows
        if row["mask_mode"] == "opcode_shape" and row["split"] == "heldout" and not row["exact_trace_match"]
    ]
    claim_impact = {
        "target_claim": "C2h",
        "heldout_opcode_shape_failed_program_count": len(heldout_opcode_shape),
        "heldout_opcode_shape_by_provenance": [
            {"provenance_class": key, "count": value}
            for key, value in sorted(Counter(row["provenance_class"] for row in heldout_opcode_shape).items())
        ],
        "claim_update": "The fair-regime closure remains negative. Provenance now separates direct semantic mistakes from downstream nontermination instead of treating every step-budget row as primary evidence.",
    }

    out_dir = Path("results/M4_failure_provenance")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "per_program_provenance.json").write_text(json.dumps(per_program_rows, indent=2), encoding="utf-8")
    (out_dir / "claim_impact.json").write_text(json.dumps(claim_impact, indent=2), encoding="utf-8")
    print(out_dir.as_posix())


if __name__ == "__main__":
    main()
