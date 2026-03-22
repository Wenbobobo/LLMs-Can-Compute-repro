"""Export the narrow long-horizon precision scaling gate for R36."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Sequence

from exec_trace import (
    TraceInterpreter,
    TraceEvent,
    call_chain_program,
    flagged_indirect_accumulator_program,
    hotspot_memory_rewrite_program,
    loop_indirect_memory_program,
    stack_fanout_sum_program,
)
from exec_trace.dsl import Program
from model import (
    MemoryOperation,
    check_real_trace_precision,
    extract_call_frame_operations,
    extract_memory_operations,
    extract_stack_slot_operations,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R36_origin_long_horizon_precision_scaling_gate"

Space = Literal["memory", "stack", "call"]


@dataclass(frozen=True, slots=True)
class SchemeConfig:
    scheme: Literal["single_head", "radix2", "block_recentered"]
    base: int = 64


@dataclass(frozen=True, slots=True)
class CaseConfig:
    case_id: str
    build_program: Callable[[], Program]
    space: Space
    horizon_multipliers: tuple[int, ...]


SCHEMES: tuple[SchemeConfig, ...] = (
    SchemeConfig(scheme="single_head", base=64),
    SchemeConfig(scheme="radix2", base=64),
    SchemeConfig(scheme="block_recentered", base=64),
)


CASES: tuple[CaseConfig, ...] = (
    CaseConfig(
        case_id="loop_indirect_memory_high_address",
        build_program=lambda: loop_indirect_memory_program(12, counter_address=256, accumulator_address=257),
        space="memory",
        horizon_multipliers=(1, 4, 16),
    ),
    CaseConfig(
        case_id="hotspot_memory_rewrite_high_address",
        build_program=lambda: hotspot_memory_rewrite_program(8, base_address=256),
        space="memory",
        horizon_multipliers=(1, 4, 16, 64),
    ),
    CaseConfig(
        case_id="flagged_indirect_accumulator_control",
        build_program=lambda: flagged_indirect_accumulator_program(6, base_address=128),
        space="memory",
        horizon_multipliers=(1, 16),
    ),
    CaseConfig(
        case_id="stack_fanout_depth_boundary",
        build_program=lambda: stack_fanout_sum_program(256, base_value=1),
        space="stack",
        horizon_multipliers=(1, 4, 16),
    ),
    CaseConfig(
        case_id="call_chain_control",
        build_program=call_chain_program,
        space="call",
        horizon_multipliers=(1, 16),
    ),
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def _extract_operations(space: Space, events: Sequence[TraceEvent]) -> tuple[MemoryOperation, ...]:
    if space == "memory":
        return extract_memory_operations(events)
    if space == "stack":
        return extract_stack_slot_operations(events)
    if space == "call":
        return extract_call_frame_operations(events)
    raise ValueError(f"Unsupported space: {space}")


def _build_case_rows(case: CaseConfig) -> list[dict[str, object]]:
    program = case.build_program()
    events = TraceInterpreter().run(program).events
    operations = _extract_operations(case.space, events)
    if not operations:
        raise ValueError(f"Case {case.case_id} produced no operations for space={case.space}.")

    native_max_steps = max(operation.step for operation in operations)
    rows: list[dict[str, object]] = []
    for multiplier in case.horizon_multipliers:
        max_steps = native_max_steps * multiplier
        for scheme in SCHEMES:
            result = check_real_trace_precision(
                operations,
                fmt="float32",
                scheme=scheme.scheme,
                base=scheme.base,
                max_steps=max_steps,
            )
            failure = result.first_failure
            rows.append(
                {
                    "case_id": case.case_id,
                    "program_name": program.name,
                    "space": case.space,
                    "fmt": "float32",
                    "scheme": scheme.scheme,
                    "base": scheme.base,
                    "native_max_steps": native_max_steps,
                    "horizon_multiplier": multiplier,
                    "max_steps": max_steps,
                    "read_count": result.read_count,
                    "write_count": result.write_count,
                    "passed": result.passed,
                    "failure_type": None if failure is None else failure.failure_type,
                    "failure_read_step": None if failure is None else failure.read_step,
                    "failure_query_address": None if failure is None else failure.query_address,
                    "expected_address": None if failure is None else failure.expected_address,
                    "expected_step": None if failure is None else failure.expected_step,
                    "competing_address": None if failure is None else failure.competing_address,
                    "competing_step": None if failure is None else failure.competing_step,
                    "expected_scores": None if failure is None else list(failure.expected_scores),
                    "competing_scores": None if failure is None else list(failure.competing_scores),
                }
            )
    return rows


def _single_case_boundary_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Boundary summarization requires non-empty rows.")

    first = rows[0]
    multipliers = sorted({int(row["horizon_multiplier"]) for row in rows})
    by_scheme: dict[str, dict[int, dict[str, object]]] = {"single_head": {}, "radix2": {}, "block_recentered": {}}
    for row in rows:
        by_scheme[str(row["scheme"])][int(row["horizon_multiplier"])] = row

    single_failures = [m for m in multipliers if not bool(by_scheme["single_head"][m]["passed"])]
    first_failure = min(single_failures) if single_failures else None

    decomposition_recovery = [
        m
        for m in multipliers
        if (not bool(by_scheme["single_head"][m]["passed"]))
        and bool(by_scheme["radix2"][m]["passed"])
        and bool(by_scheme["block_recentered"][m]["passed"])
    ]

    return {
        "case_id": first["case_id"],
        "program_name": first["program_name"],
        "space": first["space"],
        "native_max_steps": first["native_max_steps"],
        "tested_horizon_multipliers": multipliers,
        "single_head_first_failing_multiplier": first_failure,
        "single_head_failing_multipliers": single_failures,
        "radix2_all_tested_exact": all(bool(by_scheme["radix2"][m]["passed"]) for m in multipliers),
        "block_recentered_all_tested_exact": all(bool(by_scheme["block_recentered"][m]["passed"]) for m in multipliers),
        "decomposition_recovery_multipliers": decomposition_recovery,
        "decomposition_recovers_single_head_failure": bool(decomposition_recovery),
    }


def build_program_boundary_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    case_ids = sorted({str(row["case_id"]) for row in rows})
    boundary_rows: list[dict[str, object]] = []
    for case_id in case_ids:
        case_rows = [row for row in rows if str(row["case_id"]) == case_id]
        boundary_rows.append(_single_case_boundary_rows(case_rows))
    return boundary_rows


def build_summary(rows: list[dict[str, object]], boundary_rows: list[dict[str, object]]) -> dict[str, object]:
    inflated_single_head_failures = [
        row
        for row in rows
        if str(row["scheme"]) == "single_head"
        and int(row["horizon_multiplier"]) > 1
        and not bool(row["passed"])
    ]
    decomposition_recovery_rows = [
        row for row in boundary_rows if bool(row["decomposition_recovers_single_head_failure"])
    ]
    scope_is_narrow = sorted({str(row["case_id"]) for row in rows}) == sorted(case.case_id for case in CASES)

    lane_passed = bool(inflated_single_head_failures) and bool(decomposition_recovery_rows) and scope_is_narrow
    return {
        "current_paper_phase": "r36_origin_long_horizon_precision_scaling_gate_complete",
        "active_runtime_lane": "r36_origin_long_horizon_precision_scaling_gate",
        "gate": {
            "lane_verdict": "origin_precision_scaling_boundary_sharpened"
            if lane_passed
            else "origin_precision_scaling_boundary_mixed",
            "narrow_scope_kept": scope_is_narrow,
            "inflated_single_head_failure_count": len(inflated_single_head_failures),
            "decomposition_recovery_case_count": len(decomposition_recovery_rows),
            "executed_case_count": len({str(row["case_id"]) for row in rows}),
            "executed_scheme_count": len({str(row["scheme"]) for row in rows}),
            "executed_row_count": len(rows),
            "next_priority_lane": "later_explicit_packet_required_before_scope_lift",
        },
    }


def main() -> None:
    screening_rows: list[dict[str, object]] = []
    for case in CASES:
        screening_rows.extend(_build_case_rows(case))
    boundary_rows = build_program_boundary_summary(screening_rows)
    summary = build_summary(screening_rows, boundary_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "screening_rows.json", {"rows": screening_rows})
    write_json(OUT_DIR / "program_boundary_summary.json", {"rows": boundary_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
