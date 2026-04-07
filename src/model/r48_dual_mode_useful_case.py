from __future__ import annotations

from dataclasses import dataclass

from bytecode import lower_program, r47_restricted_frontend_translation_cases
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


HELDOUT_KERNEL_ID = "histogram16_u8"


@dataclass(frozen=True, slots=True)
class R48ContractProgram:
    kernel_id: str
    variant_id: str
    family_role: str
    axis_tags: tuple[str, ...]
    comparison_mode: str
    max_steps: int
    frontend_program_name: str
    bytecode_program_name: str
    trace_program: Program
    program_steps: int


@dataclass(frozen=True, slots=True)
class R48ModeEvaluation:
    mode_id: str
    mode_role: str
    memory_strategy: str
    call_strategy: str
    scorer: TrainableLatestWriteScorer
    fit_result: FitResult | None
    train_kernel_ids: tuple[str, ...]
    heldout_kernel_ids: tuple[str, ...]
    evaluation: FreeRunningEvaluation


def r48_contract_programs() -> tuple[R48ContractProgram, ...]:
    interpreter = TraceInterpreter()
    rows: list[R48ContractProgram] = []
    for case in r47_restricted_frontend_translation_cases():
        trace_program = lower_program(case.canonical_program)
        result = interpreter.run(trace_program, max_steps=case.max_steps)
        rows.append(
            R48ContractProgram(
                kernel_id=case.kernel_id,
                variant_id=case.variant_id,
                family_role="heldout" if case.kernel_id == HELDOUT_KERNEL_ID else "core",
                axis_tags=tuple(case.axis_tags),
                comparison_mode=case.comparison_mode,
                max_steps=case.max_steps,
                frontend_program_name=case.frontend_program.name,
                bytecode_program_name=case.canonical_program.name,
                trace_program=trace_program,
                program_steps=result.final_state.steps,
            )
        )
    return tuple(rows)


def build_stack_latest_write_samples_for_useful_case_programs(
    programs: tuple[R48ContractProgram, ...],
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


def compiled_weight_executor_scorer_for_useful_case(
    programs: tuple[R48ContractProgram, ...],
) -> TrainableLatestWriteScorer:
    max_program_steps = max(program.program_steps for program in programs)
    time_scale = 1.0 / float(max_program_steps + 2)
    quadratic_scale = 1.0 + (time_scale * float(max_program_steps + 2))
    return TrainableLatestWriteScorer(
        quadratic_scale=quadratic_scale,
        time_scale=time_scale,
    )


def fit_trainable_2d_executor_for_useful_case(
    programs: tuple[R48ContractProgram, ...],
) -> FitResult:
    return fit_scorer(build_stack_latest_write_samples_for_useful_case_programs(programs))


def evaluate_r48_dual_mode_useful_case() -> tuple[tuple[R48ContractProgram, ...], tuple[R48ModeEvaluation, ...]]:
    contract_programs = r48_contract_programs()
    core_programs = tuple(program for program in contract_programs if program.family_role == "core")
    heldout_kernel_ids = tuple(sorted({program.kernel_id for program in contract_programs if program.family_role != "core"}))
    train_kernel_ids = tuple(sorted({program.kernel_id for program in core_programs}))
    trace_programs = tuple(program.trace_program for program in contract_programs)

    compiled_scorer = compiled_weight_executor_scorer_for_useful_case(contract_programs)
    compiled_evaluation = evaluate_free_running_programs(
        trace_programs,
        lambda program: run_free_running_with_stack_scorer(program, compiled_scorer),
    )

    fit_result = fit_trainable_2d_executor_for_useful_case(core_programs)
    trainable_evaluation = evaluate_free_running_programs(
        trace_programs,
        lambda program: run_free_running_with_stack_scorer(program, fit_result.scorer),
    )

    return contract_programs, (
        R48ModeEvaluation(
            mode_id="compiled_weight_executor",
            mode_role="compiled_analytic",
            memory_strategy="accelerated_exact",
            call_strategy="pointer_like_exact",
            scorer=compiled_scorer,
            fit_result=None,
            train_kernel_ids=tuple(sorted({program.kernel_id for program in contract_programs})),
            heldout_kernel_ids=(),
            evaluation=compiled_evaluation,
        ),
        R48ModeEvaluation(
            mode_id="trainable_2d_executor",
            mode_role="fitted_stack_latest_write",
            memory_strategy="accelerated_exact",
            call_strategy="pointer_like_exact",
            scorer=fit_result.scorer,
            fit_result=fit_result,
            train_kernel_ids=train_kernel_ids,
            heldout_kernel_ids=heldout_kernel_ids,
            evaluation=trainable_evaluation,
        ),
    )
