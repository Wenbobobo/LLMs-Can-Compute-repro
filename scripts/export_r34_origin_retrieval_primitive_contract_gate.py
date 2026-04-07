"""Export the Origin-core retrieval primitive contract gate for R34."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from exec_trace import (
    TraceInterpreter,
    call_chain_program,
    countdown_program,
    dynamic_latest_write_program,
    latest_write_program,
    stack_fanout_sum_program,
    stack_memory_ping_pong_program,
)
from geometry import HullKVCache, brute_force_hardmax_2d
from model import (
    LatestWriteDecodeConfig,
    MemoryOperation,
    run_latest_write_decode,
    run_latest_write_decode_for_call_events,
    run_latest_write_decode_for_events,
    run_latest_write_decode_for_stack_events,
)
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R34_origin_retrieval_primitive_contract_gate"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def exact_count(observations: list[Any]) -> int:
    return sum(
        int(obs.expected_value == obs.linear_value == obs.accelerated_value)
        for obs in observations
    )


def build_latest_write_case_rows() -> list[dict[str, object]]:
    interpreter = TraceInterpreter()
    rows: list[dict[str, object]] = []

    for case_id, program in (
        ("latest_write_program", latest_write_program()),
        ("dynamic_latest_write_program", dynamic_latest_write_program()),
    ):
        result = interpreter.run(program)
        decode_run = run_latest_write_decode_for_events(result.events)
        rows.append(
            {
                "primitive_id": "latest_write_address",
                "case_id": case_id,
                "program_name": program.name,
                "observation_count": len(decode_run.observations),
                "exact_observation_count": exact_count(list(decode_run.observations)),
                "supports_default_read": False,
                "notes": "Real trace-derived latest-write audit case.",
            }
        )

    default_ops = (
        MemoryOperation(step=0, kind="load", address=4, value=0),
        MemoryOperation(step=1, kind="store", address=2, value=5),
        MemoryOperation(step=2, kind="store", address=4, value=9),
        MemoryOperation(step=3, kind="load", address=4, value=9),
    )
    decode_run = run_latest_write_decode(
        default_ops,
        LatestWriteDecodeConfig(max_steps=4, addresses=(2, 4), default_value=0),
    )
    rows.append(
        {
            "primitive_id": "latest_write_address",
            "case_id": "synthetic_default_and_alias_read",
            "program_name": None,
            "observation_count": len(decode_run.observations),
            "exact_observation_count": exact_count(list(decode_run.observations)),
            "supports_default_read": True,
            "notes": "Synthetic latest-write case covering default-read and alias-shaped overwrite behavior.",
        }
    )
    return rows


def build_stack_case_rows() -> list[dict[str, object]]:
    interpreter = TraceInterpreter()
    rows: list[dict[str, object]] = []
    programs = (
        countdown_program(6),
        stack_memory_ping_pong_program(),
        stack_fanout_sum_program(6, base_value=2),
    )
    for program in programs:
        result = interpreter.run(program)
        decode_run = run_latest_write_decode_for_stack_events(result.events)
        observation_iter = iter(decode_run.observations)
        aggregate: dict[str, dict[str, object]] = {}

        for event in result.events:
            pop_count = len(event.popped)
            read_base = event.stack_depth_before - pop_count
            for offset, _value in enumerate(event.popped):
                observation = next(observation_iter)
                relative_depth = event.stack_depth_before - 1 - (read_base + offset)
                primitive_id = "stack_top" if relative_depth == 0 else "stack_at_depth"
                state = aggregate.setdefault(
                    primitive_id,
                    {
                        "primitive_id": primitive_id,
                        "case_id": program.name,
                        "program_name": program.name,
                        "observation_count": 0,
                        "exact_observation_count": 0,
                        "max_relative_depth": 0,
                        "notes": "Real stack-pop trace-derived retrieval case.",
                    },
                )
                state["observation_count"] = int(state["observation_count"]) + 1
                state["exact_observation_count"] = int(state["exact_observation_count"]) + int(
                    observation.expected_value == observation.linear_value == observation.accelerated_value
                )
                state["max_relative_depth"] = max(int(state["max_relative_depth"]), relative_depth)

        rows.extend(aggregate.values())
    return rows


def build_call_case_rows() -> list[dict[str, object]]:
    interpreter = TraceInterpreter()
    result = interpreter.run(call_chain_program())
    decode_run = run_latest_write_decode_for_call_events(result.events)
    return [
        {
            "primitive_id": "call_return_target",
            "case_id": "call_chain_program",
            "program_name": result.program.name,
            "observation_count": len(decode_run.observations),
            "exact_observation_count": exact_count(list(decode_run.observations)),
            "notes": "Nested call/return target retrieval expressed as append-only latest-write frame lookup.",
        }
    ]


def build_tie_rows() -> list[dict[str, object]]:
    keys = ((0, 0), (0, 0), (1, -1))
    values = (1, 3, 9)
    query = (0, 1)
    cache = HullKVCache()
    cache.extend(keys, values)
    linear = brute_force_hardmax_2d(keys, values, query)
    accelerated = cache.query(query)
    return [
        {
            "primitive_id": "tie_average_geometry",
            "query": list(query),
            "expected_value": 2,
            "linear_value": linear.value,
            "accelerated_value": accelerated.value,
            "maximizer_count": len(linear.maximizer_indices),
            "exact_match": linear.value == 2 and accelerated.value == 2,
        }
    ]


def build_primitive_rows(case_rows: list[dict[str, object]], tie_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in case_rows:
        grouped[str(row["primitive_id"])].append(row)

    primitive_rows: list[dict[str, object]] = []
    for primitive_id in ("latest_write_address", "stack_top", "stack_at_depth", "call_return_target"):
        rows = grouped[primitive_id]
        observation_count = sum(int(row["observation_count"]) for row in rows)
        exact_observation_count = sum(int(row["exact_observation_count"]) for row in rows)
        primitive_rows.append(
            {
                "primitive_id": primitive_id,
                "case_count": len(rows),
                "observation_count": observation_count,
                "exact_observation_count": exact_observation_count,
                "exact_observation_rate": exact_observation_count / observation_count if observation_count else 0.0,
                "verdict": "supported" if observation_count and exact_observation_count == observation_count else "mixed",
            }
        )

    tie_exact = all(bool(row["exact_match"]) for row in tie_rows)
    primitive_rows.append(
        {
            "primitive_id": "tie_average_geometry",
            "case_count": len(tie_rows),
            "observation_count": len(tie_rows),
            "exact_observation_count": sum(int(bool(row["exact_match"])) for row in tie_rows),
            "exact_observation_rate": 1.0 if tie_exact else 0.0,
            "verdict": "supported" if tie_exact else "mixed",
        }
    )
    return primitive_rows


def assess_gate(primitive_rows: list[dict[str, object]]) -> dict[str, object]:
    supported = {str(row["primitive_id"]): str(row["verdict"]) == "supported" for row in primitive_rows}
    primitive_contract_supported = all(
        supported.get(primitive_id, False)
        for primitive_id in (
            "latest_write_address",
            "stack_top",
            "stack_at_depth",
            "call_return_target",
            "tie_average_geometry",
        )
    )
    return {
        "lane_verdict": "origin_retrieval_contract_supported" if primitive_contract_supported else "origin_retrieval_contract_mixed",
        "primitive_contract_supported": primitive_contract_supported,
        "next_priority_lane": "r35_origin_append_only_stack_vm_execution_gate",
    }


def main() -> None:
    case_rows = build_latest_write_case_rows() + build_stack_case_rows() + build_call_case_rows()
    tie_rows = build_tie_rows()
    primitive_rows = build_primitive_rows(case_rows, tie_rows)
    gate = assess_gate(primitive_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "primitive_case_rows.json", {"rows": case_rows})
    write_json(OUT_DIR / "tie_rows.json", {"rows": tie_rows})
    write_json(OUT_DIR / "primitive_rows.json", {"rows": primitive_rows})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": {
                "current_paper_phase": "r34_origin_retrieval_primitive_contract_gate_complete",
                "active_runtime_lane": "r34_origin_retrieval_primitive_contract_gate",
                "gate": {
                    **gate,
                    "primitive_count": len(primitive_rows),
                    "supported_primitive_count": sum(str(row["verdict"]) == "supported" for row in primitive_rows),
                    "exact_observation_count": sum(int(row["exact_observation_count"]) for row in primitive_rows),
                    "observation_count": sum(int(row["observation_count"]) for row in primitive_rows),
                },
            },
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
