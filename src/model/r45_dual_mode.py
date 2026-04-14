from __future__ import annotations

from dataclasses import dataclass

from bytecode import lower_program, r43_bounded_memory_vm_cases
from exec_trace import Program, TraceInterpreter

from .exact_hardmax import extract_stack_slot_operations
from .free_running_executor import FreeRunningEvaluation, evaluate_free_running_programs, run_free_running_with_stack_scorer
from .trainable_latest_write import (
    FitResult,
    LatestWriteSample,
    TrainableLatestWriteScorer,
    build_latest_write_samples,
    fit_scorer,
)


@dataclass(frozen=True, slots=True)
class R45ContractProgram:
    family_id: str
    family_role: str
    comparison_mode: str
    max_steps: int
    bytecode_program_name: str
    trace_program: Program
    program_steps: int


@dataclass(frozen=True, slots=True)
class R45ModeEvaluation:
    mode_id: str
    mode_role: str
    memory_strategy: str
    call_strategy: str
    scorer: TrainableLatestWriteScorer
    fit_result: FitResult | None
    train_family_ids: tuple[str, ...]
    heldout_family_ids: tuple[str, ...]
    evaluation: FreeRunningEvaluation


def r45_contract_programs() -> tuple[R45ContractProgram, ...]:
    interpreter = TraceInterpreter()
    rows: list[R45ContractProgram] = []
    for case in r43_bounded_memory_vm_cases():
        trace_program = lower_program(case.program)
        result = interpreter.run(trace_program, max_steps=case.max_steps)
        rows.append(
            R45ContractProgram(
                family_id=case.family_id,
                family_role=case.family_role,
                comparison_mode=case.comparison_mode,
                max_steps=case.max_steps,
                bytecode_program_name=case.program.name,
                trace_program=trace_program,
                program_steps=result.final_state.steps,
            )
        )
    return tuple(rows)


def build_stack_latest_write_samples_for_contract_programs(
    programs: tuple[R45ContractProgram, ...],
) -> tuple[LatestWriteSample, ...]:
    interpreter = TraceInterpreter()
    samples: list[LatestWriteSample] = []
    for program in programs:
        result = interpreter.run(program.trace_program, max_steps=program.max_steps)
        operations = extract_stack_slot_operations(result.events)
        samples.extend(
            build_latest_write_samples(
                operations,
                program_name=program.trace_program.name,
                program_steps=program.program_steps,
            )
        )
    return tuple(samples)


def compiled_weight_executor_scorer(
    programs: tuple[R45ContractProgram, ...],
) -> TrainableLatestWriteScorer:
    max_program_steps = max(program.program_steps for program in programs)
    # Keep address mismatch dominant over any admissible time bias on this bounded contract.
    time_scale = 1.0 / float(max_program_steps + 2)
    quadratic_scale = 1.0 + (time_scale * float(max_program_steps + 2))
    return TrainableLatestWriteScorer(
        quadratic_scale=quadratic_scale,
        time_scale=time_scale,
    )


def fit_trainable_2d_executor(
    programs: tuple[R45ContractProgram, ...],
) -> FitResult:
    return fit_scorer(build_stack_latest_write_samples_for_contract_programs(programs))


def evaluate_r45_dual_mode() -> tuple[tuple[R45ContractProgram, ...], tuple[R45ModeEvaluation, ...]]:
    contract_programs = r45_contract_programs()
    core_programs = tuple(program for program in contract_programs if program.family_role == "core")
    heldout_programs = tuple(program for program in contract_programs if program.family_role != "core")
    trace_programs = tuple(program.trace_program for program in contract_programs)

    compiled_scorer = compiled_weight_executor_scorer(contract_programs)
    compiled_evaluation = evaluate_free_running_programs(
        trace_programs,
        lambda program: run_free_running_with_stack_scorer(program, compiled_scorer),
    )

    fit_result = fit_trainable_2d_executor(core_programs)
    trainable_evaluation = evaluate_free_running_programs(
        trace_programs,
        lambda program: run_free_running_with_stack_scorer(program, fit_result.scorer),
    )

    return contract_programs, (
        R45ModeEvaluation(
            mode_id="compiled_weight_executor",
            mode_role="compiled_analytic",
            memory_strategy="accelerated_exact",
            call_strategy="pointer_like_exact",
            scorer=compiled_scorer,
            fit_result=None,
            train_family_ids=tuple(program.family_id for program in contract_programs),
            heldout_family_ids=(),
            evaluation=compiled_evaluation,
        ),
        R45ModeEvaluation(
            mode_id="trainable_2d_executor",
            mode_role="fitted_stack_latest_write",
            memory_strategy="accelerated_exact",
            call_strategy="pointer_like_exact",
            scorer=fit_result.scorer,
            fit_result=fit_result,
            train_family_ids=tuple(program.family_id for program in core_programs),
            heldout_family_ids=tuple(program.family_id for program in heldout_programs),
            evaluation=trainable_evaluation,
        ),
    )
