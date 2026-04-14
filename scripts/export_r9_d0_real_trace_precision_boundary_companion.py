"""Export the bounded R9 real-trace precision companion on admitted R8 rows."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path

from bytecode import lower_program, r8_d0_retrieval_pressure_cases
from exec_trace import TraceInterpreter
from model import check_real_trace_precision, extract_memory_operations
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R9_d0_real_trace_precision_boundary_companion"
R8_OUT_DIR = ROOT / "results" / "R8_d0_retrieval_pressure_gate"
PRECISION_HORIZON_MULTIPLIERS = (1, 2)
PRECISION_DEFAULT_BASE = 64
PRECISION_ACTIVE_BASES = (64, 128)
PRECISION_NEGATIVE_CONTROL_BASE = 256
PRECISION_SCHEMES = ("single_head", "radix2", "block_recentered")
DECOMPOSITION_SCHEMES = ("radix2", "block_recentered")


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_r8_admitted_cases():
    exact_payload = read_json(R8_OUT_DIR / "exact_suite_rows.json")
    admitted_names = {
        str(row["program_name"])
        for row in exact_payload["rows"]
        if str(row["route_bucket"]) == "admitted"
    }
    cases = tuple(
        case
        for case in r8_d0_retrieval_pressure_cases()
        if case.program.name in admitted_names
    )
    return cases, exact_payload


def encode_precision_result(
    result,
    *,
    case,
    stream_name: str,
    native_max_steps: int,
    horizon_multiplier: int,
    negative_control_kind: str | None = None,
) -> dict[str, object]:
    failure = result.first_failure
    return {
        "family": case.family,
        "program_name": case.program.name,
        "baseline_program_name": case.baseline_program_name,
        "baseline_horizon_multiplier": case.baseline_horizon_multiplier,
        "retrieval_horizon_multiplier": case.retrieval_horizon_multiplier,
        "stream_name": stream_name,
        "fmt": result.fmt,
        "scheme": result.scheme,
        "base": result.base,
        "space": result.space,
        "native_max_steps": native_max_steps,
        "horizon_multiplier": horizon_multiplier,
        "max_steps": result.max_steps,
        "read_count": result.read_count,
        "write_count": result.write_count,
        "passed": result.passed,
        "negative_control_kind": negative_control_kind,
        "first_failure": None
        if failure is None
        else {
            "space": failure.space,
            "read_step": failure.read_step,
            "query_address": failure.query_address,
            "expected_address": failure.expected_address,
            "expected_step": failure.expected_step,
            "competing_address": failure.competing_address,
            "competing_step": failure.competing_step,
            "expected_scores": list(failure.expected_scores),
            "competing_scores": list(failure.competing_scores),
            "failure_type": failure.failure_type,
        },
    }


def enters_boundary_followup(rows: list[dict[str, object]]) -> bool:
    for multiplier in PRECISION_HORIZON_MULTIPLIERS:
        multiplier_rows = [row for row in rows if int(row["horizon_multiplier"]) == multiplier]
        single_head = next(row for row in multiplier_rows if str(row["scheme"]) == "single_head")
        if single_head["passed"] is False:
            return True
        if any(row["passed"] != single_head["passed"] for row in multiplier_rows if str(row["scheme"]) != "single_head"):
            return True
    return False


def first_single_head_failure_multiplier(rows: list[dict[str, object]]) -> int | None:
    return next(
        (
            int(row["horizon_multiplier"])
            for row in rows
            if str(row["scheme"]) == "single_head" and row["passed"] is False
        ),
        None,
    )


def build_screening(cases) -> tuple[dict[str, object], list[dict[str, object]]]:
    interpreter = TraceInterpreter()
    streams: dict[str, dict[str, object]] = {}
    base_sweep_rows: list[dict[str, object]] = []

    for case in sorted(cases, key=lambda item: (item.family, item.program.name)):
        reference = interpreter.run(lower_program(case.program), max_steps=case.max_steps)
        operations = extract_memory_operations(reference.events)
        if not operations:
            continue
        native_max_steps = max(operation.step for operation in operations)
        stream_name = f"{case.program.name}_memory"
        screening_rows: list[dict[str, object]] = []

        for horizon_multiplier in PRECISION_HORIZON_MULTIPLIERS:
            max_steps = native_max_steps * horizon_multiplier
            for scheme in PRECISION_SCHEMES:
                screening_rows.append(
                    encode_precision_result(
                        check_real_trace_precision(
                            operations,
                            fmt="float32",
                            scheme=scheme,
                            base=PRECISION_DEFAULT_BASE,
                            max_steps=max_steps,
                        ),
                        case=case,
                        stream_name=stream_name,
                        native_max_steps=native_max_steps,
                        horizon_multiplier=horizon_multiplier,
                    )
                )

        boundary_active = enters_boundary_followup(screening_rows)
        failure_multiplier = first_single_head_failure_multiplier(screening_rows) or 1
        if boundary_active:
            for scheme in DECOMPOSITION_SCHEMES:
                for base in PRECISION_ACTIVE_BASES:
                    base_sweep_rows.append(
                        encode_precision_result(
                            check_real_trace_precision(
                                operations,
                                fmt="float32",
                                scheme=scheme,
                                base=base,
                                max_steps=native_max_steps * failure_multiplier,
                            ),
                            case=case,
                            stream_name=stream_name,
                            native_max_steps=native_max_steps,
                            horizon_multiplier=failure_multiplier,
                        )
                    )
            base_sweep_rows.append(
                encode_precision_result(
                    check_real_trace_precision(
                        operations,
                        fmt="float32",
                        scheme="block_recentered",
                        base=PRECISION_NEGATIVE_CONTROL_BASE,
                        max_steps=native_max_steps * failure_multiplier,
                    ),
                    case=case,
                    stream_name=stream_name,
                    native_max_steps=native_max_steps,
                    horizon_multiplier=failure_multiplier,
                    negative_control_kind="weaker_block_recentered_base256",
                )
            )

        streams[stream_name] = {
            "family": case.family,
            "program_name": case.program.name,
            "space": "memory",
            "operation_count": len(operations),
            "read_count": sum(operation.kind == "load" for operation in operations),
            "write_count": sum(operation.kind == "store" for operation in operations),
            "native_max_steps": native_max_steps,
            "rows": screening_rows,
            "summary": {
                "entered_boundary_followup": boundary_active,
                "single_head_first_failure_multiplier": failure_multiplier
                if any(str(row["scheme"]) == "single_head" and row["passed"] is False for row in screening_rows)
                else None,
                "default_base": PRECISION_DEFAULT_BASE,
            },
        }

    screening_payload = {
        "experiment": "r9_d0_real_trace_precision_screening",
        "environment": detect_runtime_environment().as_dict(),
        "notes": [
            "R9 stays companion-only and inherits its row set strictly from exact-admitted R8 rows.",
            "The bounded grid stays on memory streams only so the follow-up sharpens real-trace precision without reopening a larger stack-wide sweep.",
            "Default base 64 defines the screened grid before boundary-bearing streams receive a small decomposition base sweep.",
            "Base 256 remains a weaker negative control rather than a positive alternative.",
        ],
        "source_artifacts": [
            "results/R8_d0_retrieval_pressure_gate/summary.json",
            "results/R8_d0_retrieval_pressure_gate/exact_suite_rows.json",
        ],
        "horizon_multipliers": list(PRECISION_HORIZON_MULTIPLIERS),
        "default_base": PRECISION_DEFAULT_BASE,
        "active_bases": list(PRECISION_ACTIVE_BASES),
        "negative_control_base": PRECISION_NEGATIVE_CONTROL_BASE,
        "streams": streams,
    }
    return screening_payload, base_sweep_rows


def build_stream_boundary_rows(
    screening_payload: dict[str, object],
    base_sweep_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    base_rows_by_stream: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for row in base_sweep_rows:
        base_rows_by_stream[str(row["stream_name"])].append(row)

    stream_rows: list[dict[str, object]] = []
    for stream_name, payload in sorted(screening_payload["streams"].items()):
        screening_rows = list(payload["rows"])
        combined_rows = screening_rows + base_rows_by_stream.get(stream_name, [])
        [row for row in screening_rows if str(row["scheme"]) == "single_head"]
        decomposition_screening_rows = [
            row for row in screening_rows if str(row["scheme"]) in DECOMPOSITION_SCHEMES
        ]
        grouped_decomposition: defaultdict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
        for row in decomposition_screening_rows:
            grouped_decomposition[(str(row["scheme"]), int(row["base"]))].append(row)

        default_grid_pass = any(
            all(bool(row["passed"]) for row in config_rows)
            for config_rows in grouped_decomposition.values()
        )
        boundary_recovery = any(
            bool(row["passed"])
            for row in base_rows_by_stream.get(stream_name, [])
            if row["negative_control_kind"] is None
        )
        single_head_failure = first_single_head_failure_multiplier(screening_rows)
        if single_head_failure is None or default_grid_pass:
            classification = "effective_here"
        elif boundary_recovery:
            classification = "unproven_here"
        elif single_head_failure == 1:
            classification = "negated_here"
        else:
            classification = "unproven_here"

        stream_rows.append(
            {
                "stream_name": stream_name,
                "family": payload["family"],
                "program_name": payload["program_name"],
                "space": payload["space"],
                "native_max_steps": payload["native_max_steps"],
                "read_count": payload["read_count"],
                "write_count": payload["write_count"],
                "entered_boundary_followup": payload["summary"]["entered_boundary_followup"],
                "single_head_first_failure_multiplier": single_head_failure,
                "default_grid_decomposition_pass": default_grid_pass,
                "boundary_recovery": boundary_recovery,
                "negative_control_row_count": sum(
                    row["negative_control_kind"] is not None for row in base_rows_by_stream.get(stream_name, [])
                ),
                "negative_control_failure_count": sum(
                    row["negative_control_kind"] is not None and row["passed"] is False
                    for row in base_rows_by_stream.get(stream_name, [])
                ),
                "observed_failure_types": sorted(
                    {
                        str(row["first_failure"]["failure_type"])
                        for row in combined_rows
                        if row["first_failure"] is not None
                    }
                ),
                "classification": classification,
            }
        )
    return stream_rows


def build_family_boundary_rows(stream_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for row in stream_rows:
        grouped[str(row["family"])].append(row)

    family_rows: list[dict[str, object]] = []
    for family, family_stream_rows in sorted(grouped.items()):
        family_rows.append(
            {
                "family": family,
                "stream_count": len(family_stream_rows),
                "effective_here_stream_count": sum(
                    str(row["classification"]) == "effective_here" for row in family_stream_rows
                ),
                "unproven_here_stream_count": sum(
                    str(row["classification"]) == "unproven_here" for row in family_stream_rows
                ),
                "negated_here_stream_count": sum(
                    str(row["classification"]) == "negated_here" for row in family_stream_rows
                ),
                "single_head_failure_stream_count": sum(
                    row["single_head_first_failure_multiplier"] is not None for row in family_stream_rows
                ),
                "single_head_failure_at_1x_stream_count": sum(
                    row["single_head_first_failure_multiplier"] == 1 for row in family_stream_rows
                ),
                "boundary_recovery_stream_count": sum(bool(row["boundary_recovery"]) for row in family_stream_rows),
                "default_grid_decomposition_pass_stream_count": sum(
                    bool(row["default_grid_decomposition_pass"]) for row in family_stream_rows
                ),
                "observed_failure_types": sorted(
                    {
                        failure_type
                        for row in family_stream_rows
                        for failure_type in row["observed_failure_types"]
                    }
                ),
            }
        )
    return family_rows


def build_failure_taxonomy_rows(
    screening_payload: dict[str, object],
    base_sweep_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    counter: Counter[str] = Counter()
    for payload in screening_payload["streams"].values():
        for row in payload["rows"]:
            if row["first_failure"] is not None:
                counter[str(row["first_failure"]["failure_type"])] += 1
    for row in base_sweep_rows:
        if row["first_failure"] is not None:
            counter[str(row["first_failure"]["failure_type"])] += 1
    return [
        {"failure_type": failure_type, "count": count}
        for failure_type, count in sorted(counter.items())
    ]


def build_summary(
    screening_payload: dict[str, object],
    stream_rows: list[dict[str, object]],
    family_rows: list[dict[str, object]],
    base_sweep_rows: list[dict[str, object]],
    failure_taxonomy_rows: list[dict[str, object]],
) -> dict[str, object]:
    negative_control_rows = [row for row in base_sweep_rows if row["negative_control_kind"] is not None]
    negative_control_failures = [row for row in negative_control_rows if row["passed"] is False]
    effective_count = sum(str(row["classification"]) == "effective_here" for row in stream_rows)
    unproven_count = sum(str(row["classification"]) == "unproven_here" for row in stream_rows)
    negated_count = sum(str(row["classification"]) == "negated_here" for row in stream_rows)
    boundary_bearing_count = sum(bool(row["entered_boundary_followup"]) for row in stream_rows)

    return {
        "screening": {
            "candidate_stream_count": len(stream_rows),
            "family_count": len(family_rows),
            "boundary_bearing_stream_count": boundary_bearing_count,
            "base_sweep_row_count": len(base_sweep_rows),
            "negative_control_row_count": len(negative_control_rows),
            "negative_control_failure_count": len(negative_control_failures),
        },
        "classification": {
            "effective_here_stream_count": effective_count,
            "unproven_here_stream_count": unproven_count,
            "negated_here_stream_count": negated_count,
        },
        "failure_taxonomy": {
            "row_count": len(failure_taxonomy_rows),
            "rows": failure_taxonomy_rows,
        },
        "claim_impact": {
            "status": "bounded_real_trace_precision_boundary_companion",
            "target_claims": ["D0"],
            "e1c_status": "not_triggered",
            "next_lane": "R10_d0_same_endpoint_cost_attribution",
            "distilled_boundary": {
                "effective_here": [
                    f"Current admitted R8 memory streams remain precision-stable on {effective_count}/{len(stream_rows)} screened streams under the bounded grid."
                ],
                "unproven_here": [
                    f"{unproven_count}/{len(stream_rows)} screened streams need decomposition recovery or remain boundary-bearing, so broader robustness is still unproven."
                ],
                "negated_here": [
                    f"Single-head float32 fails immediately without screened recovery on {negated_count}/{len(stream_rows)} admitted R8 memory streams, and the weaker base-256 control fails on {len(negative_control_failures)}/{len(negative_control_rows)} boundary-bearing follow-ups."
                ],
            },
            "supported_here": [
                "R9 stays companion-only on exact-admitted R8 rows and sharpens the current real-trace precision boundary without changing endpoint scope.",
                "The bounded grid distinguishes streams that remain stable at default settings from streams that only recover under a bounded decomposition follow-up.",
            ],
            "unsupported_here": [
                "R9 does not justify a broader stack-wide or unseen-family precision guarantee.",
                "R9 does not reopen arbitrary compiled-language claims or widen the D0 endpoint.",
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    cases, exact_payload = load_r8_admitted_cases()
    screening_payload, base_sweep_rows = build_screening(cases)
    stream_rows = build_stream_boundary_rows(screening_payload, base_sweep_rows)
    family_rows = build_family_boundary_rows(stream_rows)
    failure_taxonomy_rows = build_failure_taxonomy_rows(screening_payload, base_sweep_rows)
    summary = build_summary(
        screening_payload=screening_payload,
        stream_rows=stream_rows,
        family_rows=family_rows,
        base_sweep_rows=base_sweep_rows,
        failure_taxonomy_rows=failure_taxonomy_rows,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r9_d0_real_trace_precision_boundary_companion",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R8_d0_retrieval_pressure_gate/summary.json",
                "results/R8_d0_retrieval_pressure_gate/exact_suite_rows.json",
            ],
            "notes": screening_payload["notes"],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "screening.json",
        {
            **screening_payload,
            "rows_from_r8_exact_suite": len(exact_payload["rows"]),
            "admitted_program_count": len(cases),
        },
    )
    write_json(
        OUT_DIR / "stream_boundary_summary.json",
        {
            "experiment": "r9_stream_boundary_summary",
            "environment": environment.as_dict(),
            "rows": stream_rows,
        },
    )
    write_json(
        OUT_DIR / "family_boundary_summary.json",
        {
            "experiment": "r9_family_boundary_summary",
            "environment": environment.as_dict(),
            "rows": family_rows,
        },
    )
    write_json(
        OUT_DIR / "negative_control_rows.json",
        {
            "experiment": "r9_negative_control_rows",
            "environment": environment.as_dict(),
            "rows": [row for row in base_sweep_rows if row["negative_control_kind"] is not None],
        },
    )
    write_json(
        OUT_DIR / "failure_taxonomy.json",
        {
            "experiment": "r9_failure_taxonomy",
            "environment": environment.as_dict(),
            "rows": failure_taxonomy_rows,
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r9_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R9 D0 Real-Trace Precision Boundary Companion",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `screening.json`",
                "- `stream_boundary_summary.json`",
                "- `family_boundary_summary.json`",
                "- `negative_control_rows.json`",
                "- `failure_taxonomy.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
