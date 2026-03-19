"""Export the bounded E1a precision patch bundle from existing artifacts."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "E1a_precision_patch"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def load_inputs() -> dict[str, Any]:
    return {
        "r1_summary": read_json(ROOT / "results" / "R1_precision_mechanism_closure" / "summary.json"),
        "stream_summary": read_json(ROOT / "results" / "R1_precision_mechanism_closure" / "stream_boundary_summary.json"),
        "family_summary": read_json(ROOT / "results" / "R1_precision_mechanism_closure" / "family_boundary_summary.json"),
        "boundary_sweep": read_json(ROOT / "results" / "M4_precision_generalization" / "boundary_sweep.json"),
    }


def flatten_rows(payload: dict[str, object], *, suite_bundle: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    streams: dict[str, dict[str, object]] = payload["streams"]
    for stream_name, stream_payload in streams.items():
        default_program_name = str(stream_payload.get("program_name") or stream_name.rsplit("_", 1)[0])
        default_family = str(stream_payload.get("family") or default_program_name)
        default_space = str(stream_payload.get("space") or "unknown")
        for row in stream_payload["rows"]:
            failure = row.get("first_failure") or {}
            rows.append(
                {
                    "suite_bundle": suite_bundle,
                    "stream_name": str(row.get("stream_name", stream_name)),
                    "family": str(row.get("family", default_family)),
                    "program_name": str(row.get("program_name", default_program_name)),
                    "space": str(row.get("space", default_space)),
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
                }
            )
    return rows


def dedupe_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    mapping: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = (
            row["suite_bundle"],
            row["stream_name"],
            row["scheme"],
            row["base"],
            row["horizon_multiplier"],
        )
        mapping[key] = row
    return list(mapping.values())


def build_first_failure_rows(
    rows: list[dict[str, object]] | dict[str, object],
    negative_control_rows: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    if negative_control_rows is not None:
        stream_summary = rows
        negative_by_stream: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in negative_control_rows:
            negative_by_stream[str(row["stream_name"])].append(row)

        return [
            {
                "suite_bundle": row["suite_bundle"],
                "stream_name": row["stream_name"],
                "family": row["family"],
                "program_name": row["program_name"],
                "space": row["space"],
                "single_head_first_failure_multiplier": row["single_head_first_failure_multiplier"],
                "decomposition_has_fully_passing_config": row["decomposition_has_fully_passing_config"],
                "weak_negative_control_row_count": len(negative_by_stream.get(str(row["stream_name"]), [])),
            }
            for row in stream_summary["rows"]
        ]

    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["suite_bundle"]), str(row["stream_name"]))].append(row)

    first_rows: list[dict[str, object]] = []
    for (_, _), stream_rows in sorted(grouped.items()):
        single_head_rows = [row for row in stream_rows if row["scheme"] == "single_head"]
        failed_single_head = sorted(
            [row for row in single_head_rows if not row["passed"]],
            key=lambda row: int(row["horizon_multiplier"]),
        )
        if not failed_single_head:
            continue
        first_failure = failed_single_head[0]
        failure_horizon = int(first_failure["horizon_multiplier"])
        decomposition_same_horizon = [
            row
            for row in stream_rows
            if row["scheme"] != "single_head" and int(row["horizon_multiplier"]) == failure_horizon
        ]
        first_rows.append(
            {
                "suite_bundle": first_failure["suite_bundle"],
                "stream_name": first_failure["stream_name"],
                "family": first_failure["family"],
                "program_name": first_failure["program_name"],
                "space": first_failure["space"],
                "native_max_steps": first_failure["native_max_steps"],
                "first_failure_horizon_multiplier": failure_horizon,
                "first_failure_type": first_failure["failure_type"],
                "first_failure_read_step": first_failure["first_failure_read_step"],
                "decomposition_passes_at_failure_horizon": any(
                    bool(row["passed"]) for row in decomposition_same_horizon
                ),
            }
        )
    return first_rows


def build_family_boundary_rows(
    rows: list[dict[str, object]] | dict[str, object],
    first_failure_rows: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    if first_failure_rows is None:
        return list(rows["rows"])

    first_failure_by_family: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in first_failure_rows:
        first_failure_by_family[str(row["family"])].append(row)

    stream_by_family: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for row in rows:
        stream_by_family[str(row["family"])].add((str(row["suite_bundle"]), str(row["stream_name"])))

    family_rows: list[dict[str, object]] = []
    for family, stream_keys in sorted(stream_by_family.items()):
        family_failures = first_failure_by_family.get(family, [])
        family_rows.append(
            {
                "family": family,
                "stream_count": len(stream_keys),
                "single_head_failure_stream_count": len(family_failures),
                "single_head_failure_at_1x_stream_count": sum(
                    int(row["first_failure_horizon_multiplier"]) == 1 for row in family_failures
                ),
                "decomposition_recovered_stream_count": sum(
                    bool(row["decomposition_passes_at_failure_horizon"]) for row in family_failures
                ),
                "observed_failure_types": ",".join(
                    sorted(
                        {
                            str(row["first_failure_type"])
                            for row in family_failures
                            if row["first_failure_type"] is not None
                        }
                    )
                ),
            }
        )
    return family_rows


def build_negative_control_rows(
    first_failure_rows: list[dict[str, object]] | dict[str, object],
) -> dict[str, object] | list[dict[str, object]]:
    if isinstance(first_failure_rows, dict):
        boundary_sweep = first_failure_rows
        rows: list[dict[str, object]] = []
        for stream_payload in boundary_sweep["streams"].values():
            for row in stream_payload["rows"]:
                if row["scheme"] == "single_head" or bool(row["passed"]):
                    continue
                rows.append(
                    {
                        "suite_bundle": "c3e_generalized",
                        "stream_name": row["stream_name"],
                        "family": row["family"],
                        "program_name": row["program_name"],
                        "space": row["space"],
                        "scheme": row["scheme"],
                        "base": row["base"],
                        "horizon_multiplier": row["horizon_multiplier"],
                        "passed": row["passed"],
                        "negative_control_kind": "weaker_decomposition",
                    }
                )
        return rows

    weak_rows = [
        row
        for row in first_failure_rows
        if int(row["first_failure_horizon_multiplier"]) == 1
    ]
    return {
        "experiment": "e1a_precision_patch_weak_negative_control",
        "description": "Existing immediate single-head failures at 1x on current suites.",
        "row_count": len(weak_rows),
        "rows": weak_rows,
    }


def build_claim_impact(
    *,
    first_failure_rows: list[dict[str, object]],
    family_boundary_rows: list[dict[str, object]],
    organic_claim_impact: dict[str, object],
) -> dict[str, object]:
    failure_type_counter = Counter(
        str(row["first_failure_type"])
        for row in first_failure_rows
        if row["first_failure_type"] is not None
    )
    return {
        "target_claims": ["C3d", "C3e"],
        "status": "sharpened_current_suite_boundary",
        "claim_update": "narrowed_positive_with_boundary_sharpened_same_suite",
        "source_basis": [
            "No new trace-family programs were added in E1a; this lane re-indexes existing M4/R1 evidence only.",
            str(
                organic_claim_impact.get("evidence_basis", ["Current organic-trace impact basis reused."])[0]
            ),
        ],
        "observed_failure_type_counts": [
            {"failure_type": key, "count": value}
            for key, value in sorted(failure_type_counter.items())
        ],
        "boundary_delta": {
            "single_head_failure_stream_count": len(first_failure_rows),
            "single_head_failure_at_1x_stream_count": sum(
                int(row["first_failure_horizon_multiplier"]) == 1 for row in first_failure_rows
            ),
            "family_count": len(family_boundary_rows),
        },
        "distilled_boundary": {
            "helps_here": [
                "Decomposition still recovers many streams at the horizon where single-head first fails."
            ],
            "unproven_here": [
                "Current-suite rows still do not support universal horizon/base robustness claims."
            ],
            "unsupported_here": [
                "No E1a output broadens beyond current validated families."
            ],
        },
    }


def build_summary(
    *,
    first_failure_rows: list[dict[str, object]],
    family_boundary_rows: list[dict[str, object]],
    negative_control_rows: dict[str, object] | list[dict[str, object]],
    all_rows: list[dict[str, object]] | None = None,
    claim_impact: dict[str, object] | None = None,
    r1_summary: dict[str, object] | None = None,
) -> dict[str, object]:
    if all_rows is None or claim_impact is None:
        assert r1_summary is not None
        return {
            "patch_status": "bounded_positive_sharpened_without_scope_widening",
            "single_head_failure_stream_count": int(r1_summary["summary"]["single_head_failure_stream_count"]),
            "single_head_failure_at_1x_stream_count": int(
                r1_summary["summary"]["single_head_failure_at_1x_stream_count"]
            ),
            "stable_decomposition_stream_count": int(r1_summary["summary"]["stable_decomposition_stream_count"]),
            "weak_negative_control_row_count": len(negative_control_rows),
        }

    stream_keys = {(str(row["suite_bundle"]), str(row["stream_name"])) for row in all_rows}
    return {
        "target_claims": claim_impact["target_claims"],
        "claim_update": claim_impact["claim_update"],
        "patch_status": "bounded_positive_sharpened_without_scope_widening",
        "row_count": len(all_rows),
        "stream_count": len(stream_keys),
        "family_count": len(family_boundary_rows),
        "first_failure_row_count": len(first_failure_rows),
        "weak_negative_control_row_count": int(negative_control_rows["row_count"]),
        "single_head_failure_stream_count": len(first_failure_rows),
        "single_head_failure_at_1x_stream_count": sum(
            int(row["first_failure_horizon_multiplier"]) == 1 for row in first_failure_rows
        ),
        "stable_decomposition_stream_count": int(
            r1_summary["summary"]["stable_decomposition_stream_count"]
        ),
        "decomposition_recovered_at_first_failure_stream_count": sum(
            bool(row["decomposition_passes_at_failure_horizon"]) for row in first_failure_rows
        ),
        "r1_baseline_single_head_failure_stream_count": int(
            r1_summary["summary"]["single_head_failure_stream_count"]
        ),
        "caption_facts": [
            "E1a stays on current C3d/C3e suites with no new family additions.",
            f"First single-head failure is now indexed for {len(first_failure_rows)} streams.",
            (
                f"Weak negative-control slice contains {int(negative_control_rows['row_count'])} "
                "immediate single-head failures at 1x."
            ),
        ],
    }


def main() -> None:
    environment = environment_payload()
    c3d_rows = flatten_rows(
        read_json(ROOT / "results" / "M4_precision_scaling_real_traces" / "horizon_base_sweep.json"),
        suite_bundle="c3d_real",
    )
    c3e_rows = flatten_rows(
        read_json(ROOT / "results" / "M4_precision_generalization" / "boundary_sweep.json"),
        suite_bundle="c3e_generalized",
    )
    all_rows = dedupe_rows([*c3d_rows, *c3e_rows])
    organic_claim_impact = read_json(ROOT / "results" / "M4_precision_organic_traces" / "claim_impact.json")
    r1_summary = read_json(ROOT / "results" / "R1_precision_mechanism_closure" / "summary.json")

    first_failure_rows = build_first_failure_rows(all_rows)
    family_boundary_rows = build_family_boundary_rows(all_rows, first_failure_rows)
    negative_control_rows = build_negative_control_rows(first_failure_rows)
    claim_impact = build_claim_impact(
        first_failure_rows=first_failure_rows,
        family_boundary_rows=family_boundary_rows,
        organic_claim_impact=organic_claim_impact,
    )
    summary = build_summary(
        all_rows=all_rows,
        first_failure_rows=first_failure_rows,
        family_boundary_rows=family_boundary_rows,
        negative_control_rows=negative_control_rows,
        claim_impact=claim_impact,
        r1_summary=r1_summary,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT_DIR / "first_failure_rows.csv",
        first_failure_rows,
        [
            "suite_bundle",
            "stream_name",
            "family",
            "program_name",
            "space",
            "native_max_steps",
            "first_failure_horizon_multiplier",
            "first_failure_type",
            "first_failure_read_step",
            "decomposition_passes_at_failure_horizon",
        ],
    )
    write_csv(
        OUT_DIR / "family_boundary_rows.csv",
        family_boundary_rows,
        [
            "family",
            "stream_count",
            "single_head_failure_stream_count",
            "single_head_failure_at_1x_stream_count",
            "decomposition_recovered_stream_count",
            "observed_failure_types",
        ],
    )
    write_json(OUT_DIR / "negative_control_rows.json", negative_control_rows)
    write_json(OUT_DIR / "claim_impact.json", claim_impact)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "e1a_precision_patch",
            "environment": environment,
            "source_artifacts": [
                "results/M4_precision_scaling_real_traces/horizon_base_sweep.json",
                "results/M4_precision_generalization/screening.json",
                "results/M4_precision_generalization/boundary_sweep.json",
                "results/M4_precision_organic_traces/claim_impact.json",
                "results/R1_precision_mechanism_closure/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# E1a Precision Patch",
                "",
                "Bounded precision patch bundle on existing C3d/C3e suites.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `first_failure_rows.csv`",
                "- `family_boundary_rows.csv`",
                "- `negative_control_rows.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
