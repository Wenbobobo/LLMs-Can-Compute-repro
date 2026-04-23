"""Trainable latest-write retrieval scorer for narrow M4 experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from exec_trace import TraceInterpreter, countdown_program, dynamic_memory_program
from model.exact_hardmax import MemoryOperation, extract_stack_slot_operations


@dataclass(frozen=True, slots=True)
class LatestWriteCandidate:
    address: int
    step: int
    value: int
    is_default: bool = False


@dataclass(frozen=True, slots=True)
class LatestWriteSample:
    program_name: str
    program_steps: int
    query_step: int
    query_address: int
    expected_value: int
    candidates: tuple[LatestWriteCandidate, ...]
    target_index: int


@dataclass(frozen=True, slots=True)
class TrainableLatestWriteScorer:
    quadratic_scale: float
    time_scale: float

    def score(self, query_address: int, candidate: LatestWriteCandidate) -> float:
        return (
            (2.0 * self.quadratic_scale * query_address * candidate.address)
            - (self.quadratic_scale * (candidate.address**2))
            + (self.time_scale * candidate.step)
        )

    def predict_index_for_query(
        self,
        query_address: int,
        candidates: Sequence[LatestWriteCandidate],
    ) -> int:
        best_index = 0
        best_key = None
        for index, candidate in enumerate(candidates):
            key = (self.score(query_address, candidate), candidate.step, index)
            if best_key is None or key > best_key:
                best_key = key
                best_index = index
        return best_index

    def predict_value_for_query(
        self,
        query_address: int,
        candidates: Sequence[LatestWriteCandidate],
    ) -> int:
        return candidates[self.predict_index_for_query(query_address, candidates)].value

    def predict_index(self, sample: LatestWriteSample) -> int:
        return self.predict_index_for_query(sample.query_address, sample.candidates)

    def predict_value(self, sample: LatestWriteSample) -> int:
        return self.predict_value_for_query(sample.query_address, sample.candidates)


@dataclass(frozen=True, slots=True)
class FitResult:
    scorer: TrainableLatestWriteScorer
    train_sample_accuracy: float
    train_exact_program_accuracy: float


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    sample_accuracy: float
    exact_program_accuracy: float
    program_count: int
    sample_count: int
    by_length_bucket: tuple[tuple[str, dict[str, float | int]], ...]


def build_latest_write_samples(
    operations: Sequence[MemoryOperation],
    *,
    program_name: str,
    program_steps: int,
    default_value: int = 0,
) -> tuple[LatestWriteSample, ...]:
    addresses = tuple(sorted({operation.address for operation in operations}))
    candidates: list[LatestWriteCandidate] = [
        LatestWriteCandidate(address=address, step=-1, value=default_value, is_default=True)
        for address in addresses
    ]
    samples: list[LatestWriteSample] = []

    for operation in operations:
        if operation.kind == "store":
            candidates.append(
                LatestWriteCandidate(address=operation.address, step=operation.step, value=operation.value)
            )
            continue

        target_index = -1
        target_step = -10**9
        for index, candidate in enumerate(candidates):
            if candidate.address != operation.address:
                continue
            if candidate.step > target_step:
                target_step = candidate.step
                target_index = index

        if target_index == -1:
            raise RuntimeError("Each sample should have at least its seeded default candidate.")

        samples.append(
            LatestWriteSample(
                program_name=program_name,
                program_steps=program_steps,
                query_step=operation.step,
                query_address=operation.address,
                expected_value=operation.value,
                candidates=tuple(candidates),
                target_index=target_index,
            )
        )

    return tuple(samples)


def build_countdown_stack_samples(starts: Iterable[int]) -> tuple[LatestWriteSample, ...]:
    interpreter = TraceInterpreter()
    samples: list[LatestWriteSample] = []
    for start in starts:
        result = interpreter.run(countdown_program(start))
        operations = extract_stack_slot_operations(result.events)
        samples.extend(
            build_latest_write_samples(
                operations,
                program_name=result.program.name,
                program_steps=result.final_state.steps,
            )
        )
    return tuple(samples)


def build_dynamic_memory_stack_samples() -> tuple[LatestWriteSample, ...]:
    interpreter = TraceInterpreter()
    result = interpreter.run(dynamic_memory_program())
    operations = extract_stack_slot_operations(result.events)
    return build_latest_write_samples(
        operations,
        program_name=result.program.name,
        program_steps=result.final_state.steps,
    )


def sample_accuracy(scorer: TrainableLatestWriteScorer, samples: Sequence[LatestWriteSample]) -> float:
    if not samples:
        return 0.0
    correct = sum(1 for sample in samples if scorer.predict_index(sample) == sample.target_index)
    return correct / len(samples)


def exact_program_accuracy(scorer: TrainableLatestWriteScorer, samples: Sequence[LatestWriteSample]) -> float:
    if not samples:
        return 0.0
    per_program: dict[str, list[bool]] = {}
    for sample in samples:
        # Performance optimization: Replace `setdefault` with an explicit check
        # to avoid list allocation overhead on every loop iteration.
        if sample.program_name not in per_program:
            per_program[sample.program_name] = []
        per_program[sample.program_name].append(scorer.predict_index(sample) == sample.target_index)
    exact = sum(1 for outcomes in per_program.values() if all(outcomes))
    return exact / len(per_program)


def bucket_name(program_steps: int) -> str:
    if program_steps <= 24:
        return "steps<=24"
    if program_steps <= 48:
        return "25<=steps<=48"
    return "steps>=49"


def evaluate_scorer(
    scorer: TrainableLatestWriteScorer,
    samples: Sequence[LatestWriteSample],
) -> EvaluationResult:
    per_bucket: dict[str, dict[str, object]] = {}
    per_program: dict[str, list[bool]] = {}
    program_steps: dict[str, int] = {}

    correct_samples = 0
    for sample in samples:
        correct = scorer.predict_index(sample) == sample.target_index
        correct_samples += int(correct)

        bucket = bucket_name(sample.program_steps)
        # Performance optimization: Replace `setdefault` with an explicit check
        # to avoid dictionary allocation overhead on every loop iteration.
        if bucket not in per_bucket:
            per_bucket[bucket] = {"sample_count": 0, "sample_correct": 0, "programs": {}}
        bucket_state = per_bucket[bucket]
        bucket_state["sample_count"] = int(bucket_state["sample_count"]) + 1
        bucket_state["sample_correct"] = int(bucket_state["sample_correct"]) + int(correct)

        if sample.program_name not in bucket_state["programs"]:
            bucket_state["programs"][sample.program_name] = []
        bucket_state["programs"][sample.program_name].append(correct)

        if sample.program_name not in per_program:
            per_program[sample.program_name] = []
        per_program[sample.program_name].append(correct)
        program_steps[sample.program_name] = sample.program_steps

    exact_programs = sum(1 for outcomes in per_program.values() if all(outcomes))
    bucket_rows: list[tuple[str, dict[str, float | int]]] = []
    for name in sorted(per_bucket):
        bucket_state = per_bucket[name]
        programs = bucket_state["programs"]
        bucket_rows.append(
            (
                name,
                {
                    "sample_count": int(bucket_state["sample_count"]),
                    "sample_accuracy": int(bucket_state["sample_correct"]) / int(bucket_state["sample_count"]),
                    "program_count": len(programs),
                    "exact_program_accuracy": sum(1 for outcomes in programs.values() if all(outcomes))
                    / len(programs),
                },
            )
        )

    return EvaluationResult(
        sample_accuracy=correct_samples / len(samples) if samples else 0.0,
        exact_program_accuracy=exact_programs / len(per_program) if per_program else 0.0,
        program_count=len(per_program),
        sample_count=len(samples),
        by_length_bucket=tuple(bucket_rows),
    )


def fit_scorer(
    train_samples: Sequence[LatestWriteSample],
    *,
    quadratic_grid: Sequence[float] | None = None,
    time_grid: Sequence[float] | None = None,
) -> FitResult:
    quadratic_grid = quadratic_grid or (0.25, 0.5, 1.0, 2.0, 4.0)
    time_grid = time_grid or (0.0005, 0.001, 0.0025, 0.005, 0.01, 0.02, 0.05)

    best: FitResult | None = None
    best_score_key: tuple[float, float, float] | None = None

    for quadratic_scale in quadratic_grid:
        for time_scale in time_grid:
            scorer = TrainableLatestWriteScorer(quadratic_scale=quadratic_scale, time_scale=time_scale)
            train_sample_acc = sample_accuracy(scorer, train_samples)
            train_exact_acc = exact_program_accuracy(scorer, train_samples)
            score_key = (train_exact_acc, train_sample_acc, -time_scale)

            if best_score_key is None or score_key > best_score_key:
                best_score_key = score_key
                best = FitResult(
                    scorer=scorer,
                    train_sample_accuracy=train_sample_acc,
                    train_exact_program_accuracy=train_exact_acc,
                )

    assert best is not None
    return best
