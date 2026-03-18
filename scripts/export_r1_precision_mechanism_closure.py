"""Export the unified precision-boundary closure bundle for R1."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R1_precision_mechanism_closure"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def counter_rows(counter: Counter[str], *, label: str) -> list[dict[str, object]]:
    return [{label: key, "count": value} for key, value in sorted(counter.items())]


def flatten_boundary_rows(payload: dict[str, object], *, suite_bundle: str, stage: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    streams: dict[str, dict[str, object]] = payload["streams"]
    for stream_name, stream_payload in streams.items():
        default_program_name = str(stream_payload.get("program_name") or stream_name.rsplit("_", 1)[0])
        default_family = str(stream_payload.get("family") or default_program_name)
        stream_rows: list[dict[str, object]] = stream_payload["rows"]
        for row in stream_rows:
            failure = row.get("first_failure") or {}
            rows.append(
                {
                    "suite_bundle": suite_bundle,
                    "stage": stage,
                    "stream_name": str(row.get("stream_name", stream_name)),
                    "family": str(row.get("family", default_family)),
                    "program_name": str(row.get("program_name", default_program_name)),
                    "space": str(row["space"]),
                    "scheme": str(row["scheme"]),
                    "base": int(row["base"]),
                    "horizon_multiplier": int(row["horizon_multiplier"]),
                    "native_max_steps": int(row["native_max_steps"]),
                    "max_steps": int(row["max_steps"]),
                    "read_count": int(row["read_count"]),
                    "write_count": int(row["write_count"]),
                    "passed": bool(row["passed"]),
                    "failure_type": failure.get("failure_type"),
                    "first_failure_read_step": failure.get("read_step"),
                    "query_address": failure.get("query_address"),
                    "expected_step": failure.get("expected_step"),
                    "competing_step": failure.get("competing_step"),
                }
            )
    return rows


def dedupe_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    mapping: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = (
            row["suite_bundle"],
            row["stage"],
            row["stream_name"],
            row["scheme"],
            row["base"],
            row["horizon_multiplier"],
        )
        mapping[key] = row
    return list(mapping.values())


def load_rows() -> tuple[list[dict[str, object]], dict[str, object]]:
    offset_boundary = read_json(ROOT / "results" / "M4_precision_scaling_real_traces" / "horizon_base_sweep.json")
    organic_screening = read_json(ROOT / "results" / "M4_precision_generalization" / "screening.json")
    organic_boundary = read_json(ROOT / "results" / "M4_precision_generalization" / "boundary_sweep.json")
    claim_impact = read_json(ROOT / "results" / "M4_precision_organic_traces" / "claim_impact.json")

    rows = dedupe_rows(
        [
            *flatten_boundary_rows(offset_boundary, suite_bundle="offset", stage="boundary"),
            *flatten_boundary_rows(organic_screening, suite_bundle="organic", stage="screening"),
            *flatten_boundary_rows(organic_boundary, suite_bundle="organic", stage="boundary"),
        ]
    )
    return rows, claim_impact


def first_failure_multiplier(rows: list[dict[str, object]]) -> int | None:
    failed = sorted(int(row["horizon_multiplier"]) for row in rows if not row["passed"])
    return failed[0] if failed else None


def max_passed_multiplier(rows: list[dict[str, object]]) -> int | None:
    passed = sorted(int(row["horizon_multiplier"]) for row in rows if row["passed"])
    return passed[-1] if passed else None


def build_stream_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["suite_bundle"]), str(row["stream_name"]))].append(row)

    summaries: list[dict[str, object]] = []
    for (suite_bundle, stream_name), stream_rows in sorted(grouped.items()):
        grouped_by_scheme_base: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
        for row in stream_rows:
            grouped_by_scheme_base[(str(row["scheme"]), int(row["base"]))].append(row)

        single_head_rows = [row for row in stream_rows if row["scheme"] == "single_head"]
        decomposition_rows = [row for row in stream_rows if row["scheme"] != "single_head"]
        stable_configs = []
        for (scheme, base), config_rows in sorted(grouped_by_scheme_base.items()):
            if scheme == "single_head":
                continue
            stable_configs.append(
                {
                    "scheme": scheme,
                    "base": base,
                    "all_rows_passed": all(bool(row["passed"]) for row in config_rows),
                    "max_passed_horizon_multiplier": max_passed_multiplier(config_rows),
                    "first_failure_multiplier": first_failure_multiplier(config_rows),
                }
            )

        summaries.append(
            {
                "suite_bundle": suite_bundle,
                "stream_name": stream_name,
                "family": stream_rows[0]["family"],
                "program_name": stream_rows[0]["program_name"],
                "space": stream_rows[0]["space"],
                "native_max_steps": stream_rows[0]["native_max_steps"],
                "read_count": max(int(row["read_count"]) for row in stream_rows),
                "write_count": max(int(row["write_count"]) for row in stream_rows),
                "single_head_first_failure_multiplier": first_failure_multiplier(single_head_rows),
                "single_head_max_passed_horizon_multiplier": max_passed_multiplier(single_head_rows),
                "single_head_failure_types": sorted(
                    {str(row["failure_type"]) for row in single_head_rows if row["failure_type"] is not None}
                ),
                "decomposition_has_fully_passing_config": any(config["all_rows_passed"] for config in stable_configs),
                "stable_configs": stable_configs,
                "observed_failure_types": sorted(
                    {str(row["failure_type"]) for row in stream_rows if row["failure_type"] is not None}
                ),
                "stages_present": sorted({str(row["stage"]) for row in stream_rows}),
                "decomposition_row_count": len(decomposition_rows),
            }
        )
    return summaries


def build_family_summary(stream_summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in stream_summary_rows:
        grouped[str(row["family"])].append(row)

    summaries: list[dict[str, object]] = []
    for family, family_rows in sorted(grouped.items()):
        first_failure_values = [
            int(row["single_head_first_failure_multiplier"])
            for row in family_rows
            if row["single_head_first_failure_multiplier"] is not None
        ]
        summaries.append(
            {
                "family": family,
                "stream_count": len(family_rows),
                "single_head_failure_stream_count": sum(
                    row["single_head_first_failure_multiplier"] is not None for row in family_rows
                ),
                "single_head_failure_at_1x_stream_count": sum(
                    row["single_head_first_failure_multiplier"] == 1 for row in family_rows
                ),
                "earliest_single_head_failure_multiplier": min(first_failure_values) if first_failure_values else None,
                "decomposition_fully_passing_stream_count": sum(
                    bool(row["decomposition_has_fully_passing_config"]) for row in family_rows
                ),
                "failure_type_counts": counter_rows(
                    Counter(
                        failure_type
                        for row in family_rows
                        for failure_type in row["observed_failure_types"]
                    ),
                    label="failure_type",
                ),
            }
        )
    return summaries


def build_scheme_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["suite_bundle"]), str(row["scheme"]))].append(row)

    summaries: list[dict[str, object]] = []
    for (suite_bundle, scheme), scheme_rows in sorted(grouped.items()):
        stream_keys = {(str(row["stream_name"]), str(row["program_name"])) for row in scheme_rows}
        failed_streams = {
            (str(row["stream_name"]), str(row["program_name"]))
            for row in scheme_rows
            if not row["passed"]
        }
        summaries.append(
            {
                "suite_bundle": suite_bundle,
                "scheme": scheme,
                "stream_count": len(stream_keys),
                "streams_with_failure": len(failed_streams),
                "fully_passing_streams": len(stream_keys) - len(failed_streams),
                "earliest_failed_horizon_multiplier": first_failure_multiplier(scheme_rows),
                "failure_type_counts": counter_rows(
                    Counter(str(row["failure_type"]) for row in scheme_rows if row["failure_type"] is not None),
                    label="failure_type",
                ),
            }
        )
    return summaries


def build_summary(
    *,
    rows: list[dict[str, object]],
    stream_summary_rows: list[dict[str, object]],
    family_summary_rows: list[dict[str, object]],
    scheme_summary_rows: list[dict[str, object]],
    claim_impact: dict[str, object],
) -> dict[str, object]:
    single_head_failures = [
        row for row in stream_summary_rows if row["single_head_first_failure_multiplier"] is not None
    ]
    stable_decomposition = [
        row for row in stream_summary_rows if row["decomposition_has_fully_passing_config"]
    ]
    failure_types = Counter(
        str(row["failure_type"])
        for row in rows
        if row["failure_type"] is not None
    )
    claim_update = claim_impact.get("claim_update") or claim_impact.get("status") or "boundary_closure_in_progress"
    evidence_basis = claim_impact.get("evidence_basis") or []
    return {
        "target_claim": claim_impact.get("target_claim"),
        "claim_update": claim_update,
        "row_count": len(rows),
        "stream_count": len(stream_summary_rows),
        "family_count": len(family_summary_rows),
        "scheme_slice_count": len(scheme_summary_rows),
        "single_head_failure_stream_count": len(single_head_failures),
        "single_head_failure_at_1x_stream_count": sum(
            row["single_head_first_failure_multiplier"] == 1 for row in single_head_failures
        ),
        "stable_decomposition_stream_count": len(stable_decomposition),
        "observed_failure_type_counts": counter_rows(failure_types, label="failure_type"),
        "caption_facts": [
            str(claim_update),
            str(evidence_basis[0]) if evidence_basis else "The current organic bundle re-indexes the broader precision evidence under one explicit claim-impact artifact.",
            (
                f"Single-head failure now appears on {len(single_head_failures)}/{len(stream_summary_rows)} tracked streams; "
                f"{sum(row['single_head_first_failure_multiplier'] == 1 for row in single_head_failures)} fail immediately at 1x."
            ),
            (
                f"At least one decomposition configuration remains fully passing on "
                f"{len(stable_decomposition)}/{len(stream_summary_rows)} tracked streams."
            ),
        ],
        "distilled_boundary": {
            "helps_here": [
                "Decomposition helps on the currently exported memory-heavy streams where single-head fails early."
            ],
            "unproven_here": [
                "The current suite does not justify universal base/horizon claims across unseen trace families."
            ],
            "unsupported_here": [
                "No current result supports broad long-horizon precision robustness beyond the validated suite."
            ],
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    rows, claim_impact = load_rows()
    stream_summary_rows = build_stream_summary(rows)
    family_summary_rows = build_family_summary(stream_summary_rows)
    scheme_summary_rows = build_scheme_summary(rows)
    summary = build_summary(
        rows=rows,
        stream_summary_rows=stream_summary_rows,
        family_summary_rows=family_summary_rows,
        scheme_summary_rows=scheme_summary_rows,
        claim_impact=claim_impact,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT_DIR / "boundary_rows.csv",
        rows,
        [
            "suite_bundle",
            "stage",
            "stream_name",
            "family",
            "program_name",
            "space",
            "scheme",
            "base",
            "horizon_multiplier",
            "native_max_steps",
            "max_steps",
            "read_count",
            "write_count",
            "passed",
            "failure_type",
            "first_failure_read_step",
            "query_address",
            "expected_step",
            "competing_step",
        ],
    )
    write_json(
        OUT_DIR / "stream_boundary_summary.json",
        {
            "experiment": "r1_stream_boundary_summary",
            "environment": environment.as_dict(),
            "rows": stream_summary_rows,
        },
    )
    write_json(
        OUT_DIR / "family_boundary_summary.json",
        {
            "experiment": "r1_family_boundary_summary",
            "environment": environment.as_dict(),
            "rows": family_summary_rows,
        },
    )
    write_json(
        OUT_DIR / "scheme_boundary_summary.json",
        {
            "experiment": "r1_scheme_boundary_summary",
            "environment": environment.as_dict(),
            "rows": scheme_summary_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r1_precision_mechanism_closure",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/M4_precision_scaling_real_traces/horizon_base_sweep.json",
                "results/M4_precision_generalization/screening.json",
                "results/M4_precision_generalization/boundary_sweep.json",
                "results/M4_precision_organic_traces/claim_impact.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R1 Precision Mechanism Closure",
                "",
                "Unified precision-boundary bundle for the current offset + organic current-suite evidence.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `stream_boundary_summary.json`",
                "- `family_boundary_summary.json`",
                "- `scheme_boundary_summary.json`",
                "- `boundary_rows.csv`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
