"""Export paper-ready figure/table source artifacts from existing milestone bundles."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from statistics import median
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P1_paper_readiness"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def relative_path(path: str | Path) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix()


def counter_rows(counter: Counter[str], *, label: str) -> list[dict[str, object]]:
    return [
        {label: key, "count": value}
        for key, value in sorted(counter.items())
    ]


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def infer_family(program_name: str) -> str:
    tokens = program_name.split("_")
    while tokens and any(character.isdigit() for character in tokens[-1]):
        tokens.pop()
    return "_".join(tokens) if tokens else program_name


def mismatch_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    mismatch_steps = [
        row["first_mismatch_step"]
        for row in rows
        if row["first_mismatch_step"] is not None
    ]
    if not mismatch_steps:
        return {
            "median_first_mismatch_step": None,
            "min_first_mismatch_step": None,
            "max_first_mismatch_step": None,
        }
    return {
        "median_first_mismatch_step": median(mismatch_steps),
        "min_first_mismatch_step": min(mismatch_steps),
        "max_first_mismatch_step": max(mismatch_steps),
    }


def build_failure_taxonomy_exports() -> tuple[dict[str, object], list[dict[str, object]]]:
    per_program_path = ROOT / "results" / "M4_failure_provenance" / "per_program_provenance.json"
    summary_path = ROOT / "results" / "M4_failure_provenance" / "summary.json"
    claim_impact_path = ROOT / "results" / "M4_failure_provenance" / "claim_impact.json"

    rows: list[dict[str, object]] = read_json(per_program_path)
    claim_impact: dict[str, object] = read_json(claim_impact_path)
    read_json(summary_path)

    family_program_counts = Counter(
        (row["mask_mode"], row["split"], row["family"])
        for row in rows
    )
    failed_rows = [row for row in rows if not row["exact_trace_match"]]

    grouped_rows: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in failed_rows:
        grouped_rows[
            (
                row["mask_mode"],
                row["split"],
                row["family"],
                row["provenance_class"],
                row["root_cause_class"],
                row["root_cause_head"],
            )
        ].append(row)

    csv_rows: list[dict[str, object]] = []
    for key, grouped in sorted(grouped_rows.items()):
        mask_mode, split, family, provenance_class, root_cause_class, root_cause_head = key
        program_count = family_program_counts[(mask_mode, split, family)]
        failed_program_count = len(grouped)
        csv_rows.append(
            {
                "mask_mode": mask_mode,
                "split": split,
                "family": family,
                "provenance_class": provenance_class,
                "root_cause_class": root_cause_class,
                "root_cause_head": root_cause_head,
                "program_count": program_count,
                "failed_program_count": failed_program_count,
                "failure_fraction": failed_program_count / program_count,
                **mismatch_summary(grouped),
            }
        )

    target_rows = [
        row
        for row in rows
        if row["mask_mode"] == "opcode_shape" and row["split"] == "heldout"
    ]
    target_failed_rows = [row for row in target_rows if not row["exact_trace_match"]]

    families = sorted({row["family"] for row in target_rows})
    by_family = []
    for family in families:
        family_rows = [row for row in target_rows if row["family"] == family]
        family_failed_rows = [row for row in family_rows if not row["exact_trace_match"]]
        by_family.append(
            {
                "family": family,
                "program_count": len(family_rows),
                "failed_program_count": len(family_failed_rows),
                "by_provenance_class": counter_rows(
                    Counter(row["provenance_class"] for row in family_failed_rows),
                    label="provenance_class",
                ),
            }
        )

    provenance_counts = Counter(row["provenance_class"] for row in target_failed_rows)
    root_cause_counts = Counter(
        row["root_cause_head"]
        for row in target_failed_rows
        if row["root_cause_head"] is not None
    )
    total_program_count = len(target_rows)
    failed_program_count = len(target_failed_rows)
    memory_value_failures = provenance_counts.get("memory_value_root_cause", 0)
    downstream_failures = provenance_counts.get("downstream_nontermination_after_semantic_error", 0)

    summary_payload = {
        "experiment": "p1_m4_failure_taxonomy_summary",
        "source_artifacts": [
            relative_path(per_program_path),
            relative_path(summary_path),
            relative_path(claim_impact_path),
        ],
        "target_slice": {
            "mask_mode": "opcode_shape",
            "split": "heldout",
        },
        "target_claim": claim_impact["target_claim"],
        "total_program_count": total_program_count,
        "failed_program_count": failed_program_count,
        "by_provenance_class": counter_rows(provenance_counts, label="provenance_class"),
        "by_root_cause_head": counter_rows(root_cause_counts, label="root_cause_head"),
        "by_family": by_family,
        "caption_facts": [
            str(claim_impact["claim_update"]),
            (
                f"Held-out opcode_shape failures remain {failed_program_count}/{total_program_count}; "
                f"direct memory-value root causes account for {memory_value_failures}, "
                f"downstream nontermination after earlier semantic error accounts for {downstream_failures}."
            ),
        ],
    }
    return summary_payload, csv_rows


def flatten_boundary_rows(payload: dict[str, object], *, suite_bundle: str) -> list[dict[str, object]]:
    flat_rows: list[dict[str, object]] = []
    streams: dict[str, dict[str, object]] = payload["streams"]  # type: ignore[assignment]
    for stream_name, stream_payload in streams.items():
        default_program_name = str(stream_payload.get("program_name") or stream_name.rsplit("_", 1)[0])
        default_family = str(stream_payload.get("family") or infer_family(default_program_name))
        stream_rows: list[dict[str, object]] = stream_payload["rows"]  # type: ignore[assignment]
        for row in stream_rows:
            first_failure = row.get("first_failure") or {}
            flat_rows.append(
                {
                    "suite_bundle": suite_bundle,
                    "stream_name": row.get("stream_name", stream_name),
                    "family": row.get("family", default_family),
                    "program_name": row.get("program_name", default_program_name),
                    "space": row["space"],
                    "scheme": row["scheme"],
                    "base": row["base"],
                    "horizon_multiplier": row["horizon_multiplier"],
                    "native_max_steps": row["native_max_steps"],
                    "max_steps": row["max_steps"],
                    "read_count": row["read_count"],
                    "write_count": row["write_count"],
                    "passed": row["passed"],
                    "failure_type": first_failure.get("failure_type"),
                    "first_failure_read_step": first_failure.get("read_step"),
                    "query_address": first_failure.get("query_address"),
                    "expected_step": first_failure.get("expected_step"),
                    "competing_step": first_failure.get("competing_step"),
                }
            )
    return flat_rows


def build_real_trace_boundary_exports() -> tuple[dict[str, object], list[dict[str, object]]]:
    organic_screening_path = ROOT / "results" / "M4_precision_organic_traces" / "screening.json"
    organic_boundary_path = ROOT / "results" / "M4_precision_organic_traces" / "boundary_sweep.json"
    organic_claim_impact_path = ROOT / "results" / "M4_precision_organic_traces" / "claim_impact.json"
    offset_boundary_path = ROOT / "results" / "M4_precision_scaling_real_traces" / "horizon_base_sweep.json"

    read_json(organic_screening_path)
    organic_boundary: dict[str, object] = read_json(organic_boundary_path)
    organic_claim_impact: dict[str, object] = read_json(organic_claim_impact_path)
    offset_boundary: dict[str, object] = read_json(offset_boundary_path)

    all_rows = [
        *flatten_boundary_rows(offset_boundary, suite_bundle="offset"),
        *flatten_boundary_rows(organic_boundary, suite_bundle="organic"),
    ]

    stream_keys = sorted(
        {
            (row["suite_bundle"], row["stream_name"], row["scheme"])
            for row in all_rows
        }
    )
    by_stream_boundary = []
    for suite_bundle, stream_name, scheme in stream_keys:
        rows = [
            row
            for row in all_rows
            if row["suite_bundle"] == suite_bundle and row["stream_name"] == stream_name and row["scheme"] == scheme
        ]
        failed_rows = [row for row in rows if not row["passed"]]
        by_stream_boundary.append(
            {
                "suite_bundle": suite_bundle,
                "stream_name": stream_name,
                "family": rows[0]["family"],
                "program_name": rows[0]["program_name"],
                "space": rows[0]["space"],
                "scheme": scheme,
                "bases_evaluated": sorted({int(row["base"]) for row in rows}),
                "max_passed_horizon_multiplier": max(
                    (int(row["horizon_multiplier"]) for row in rows if row["passed"]),
                    default=None,
                ),
                "min_failed_horizon_multiplier": min(
                    (int(row["horizon_multiplier"]) for row in failed_rows),
                    default=None,
                ),
                "failure_types": sorted(
                    {
                        str(row["failure_type"])
                        for row in failed_rows
                        if row["failure_type"] is not None
                    }
                ),
                "all_rows_passed": not failed_rows,
            }
        )

    scheme_keys = sorted({(row["suite_bundle"], row["scheme"]) for row in all_rows})
    by_scheme_boundary = []
    for suite_bundle, scheme in scheme_keys:
        rows = [
            row
            for row in all_rows
            if row["suite_bundle"] == suite_bundle and row["scheme"] == scheme
        ]
        grouped_streams = {
            (row["stream_name"], row["program_name"])
            for row in rows
        }
        streams_with_failure = {
            (row["stream_name"], row["program_name"])
            for row in rows
            if not row["passed"]
        }
        by_scheme_boundary.append(
            {
                "suite_bundle": suite_bundle,
                "scheme": scheme,
                "stream_count": len(grouped_streams),
                "streams_with_failure": len(streams_with_failure),
                "fully_passed_streams": len(grouped_streams) - len(streams_with_failure),
                "earliest_failed_horizon_multiplier": min(
                    (int(row["horizon_multiplier"]) for row in rows if not row["passed"]),
                    default=None,
                ),
                "failure_type_counts": counter_rows(
                    Counter(
                        str(row["failure_type"])
                        for row in rows
                        if row["failure_type"] is not None
                    ),
                    label="failure_type",
                ),
            }
        )

    failure_type_counts = Counter(
        str(row["failure_type"])
        for row in all_rows
        if row["failure_type"] is not None
    )
    summary_payload = {
        "experiment": "p1_m4_real_trace_boundary_summary",
        "source_artifacts": [
            relative_path(organic_screening_path),
            relative_path(organic_boundary_path),
            relative_path(organic_claim_impact_path),
            relative_path(offset_boundary_path),
        ],
        "focus_format": organic_boundary["focus_format"],
        "schemes": sorted({str(row["scheme"]) for row in all_rows}),
        "streams": [
            {
                "suite_bundle": suite_bundle,
                "stream_name": stream_name,
                "family": family,
                "program_name": program_name,
                "space": space,
            }
            for suite_bundle, stream_name, family, program_name, space in sorted(
                {
                    (
                        str(row["suite_bundle"]),
                        str(row["stream_name"]),
                        str(row["family"]),
                        str(row["program_name"]),
                        str(row["space"]),
                    )
                    for row in all_rows
                }
            )
        ],
        "by_stream_boundary": by_stream_boundary,
        "by_scheme_boundary": by_scheme_boundary,
        "failure_type_counts": counter_rows(failure_type_counts, label="failure_type"),
        "caption_facts": [
            *organic_claim_impact["evidence_basis"],
            (
                f"Combined plot rows now cover {len({(row['suite_bundle'], row['stream_name']) for row in all_rows})} "
                f"stream slices across offset and organic bundles."
            ),
        ],
    }
    return summary_payload, all_rows


def infer_length_bucket(comparison_mode: str) -> str:
    if comparison_mode.startswith("short_"):
        return "short"
    if comparison_mode.startswith("medium_"):
        return "medium"
    if comparison_mode.startswith("long_"):
        return "long"
    return "unknown"


def infer_success_target(comparison_mode: str) -> str:
    if "final_state" in comparison_mode:
        return "exact_final_state"
    return "exact_trace"


def format_address_cells(addresses: list[object]) -> str:
    return "|".join(str(address) for address in addresses)


def build_exact_trace_final_state_table() -> tuple[dict[str, object], list[dict[str, object]]]:
    short_trace_path = ROOT / "results" / "M6_typed_bytecode_harness" / "short_exact_trace.json"
    long_final_state_path = ROOT / "results" / "M6_typed_bytecode_harness" / "long_exact_final_state.json"
    lowering_path = ROOT / "results" / "M6_typed_bytecode_harness" / "lowering_equivalence.json"
    verifier_path = ROOT / "results" / "M6_typed_bytecode_harness" / "verifier_rows.json"

    short_rows: list[dict[str, object]] = read_json(short_trace_path)["rows"]
    long_rows: list[dict[str, object]] = read_json(long_final_state_path)["rows"]
    lowering_rows = {
        row["program_name"]: row
        for row in read_json(lowering_path)["rows"]
    }
    verifier_rows = {
        row["program_name"]: row
        for row in read_json(verifier_path)["rows"]
    }

    rows: list[dict[str, object]] = []
    for source_row in [*short_rows, *long_rows]:
        program_name = source_row["program_name"]
        lowering_row = lowering_rows[program_name]
        verifier_row = verifier_rows.get(program_name)
        success_target = infer_success_target(source_row["comparison_mode"])
        if success_target == "exact_trace" and source_row["trace_match"]:
            status_label = "exact_trace_match"
        elif success_target == "exact_final_state" and source_row["final_state_match"]:
            status_label = "exact_final_state_match"
        else:
            status_label = "mismatch"
        rows.append(
            {
                "program_name": program_name,
                "suite": source_row["suite"],
                "comparison_mode": source_row["comparison_mode"],
                "length_bucket": infer_length_bucket(source_row["comparison_mode"]),
                "success_target": success_target,
                "trace_match": source_row["trace_match"],
                "final_state_match": source_row["final_state_match"],
                "status_label": status_label,
                "bytecode_instruction_count": lowering_row["bytecode_instruction_count"],
                "lowered_instruction_count": lowering_row["lowered_instruction_count"],
                "instruction_count_match": lowering_row["instruction_count_match"],
                "verifier_passed": None if verifier_row is None else verifier_row["passed"],
                "first_divergence_step": source_row["first_divergence_step"],
                "failure_class": source_row["failure_class"],
                "failure_reason": source_row["failure_reason"],
            }
        )

    rows.sort(key=lambda row: (row["suite"], row["comparison_mode"], row["program_name"]))

    summary_payload = {
        "experiment": "p1_exact_trace_final_state_table",
        "source_artifacts": [
            relative_path(short_trace_path),
            relative_path(long_final_state_path),
            relative_path(lowering_path),
            relative_path(verifier_path),
        ],
        "rows": rows,
        "summary": {
            "total_rows": len(rows),
            "by_comparison_mode": counter_rows(
                Counter(str(row["comparison_mode"]) for row in rows),
                label="comparison_mode",
            ),
            "by_suite": [
                {
                    "suite": suite,
                    "row_count": len(suite_rows),
                    "trace_match_count": sum(bool(row["trace_match"]) for row in suite_rows),
                    "final_state_match_count": sum(bool(row["final_state_match"]) for row in suite_rows),
                }
                for suite in sorted({str(row["suite"]) for row in rows})
                for suite_rows in [[row for row in rows if row["suite"] == suite]]
            ],
            "trace_match_count": sum(bool(row["trace_match"]) for row in rows),
            "final_state_match_count": sum(bool(row["final_state_match"]) for row in rows),
            "verifier_pass_count": sum(bool(row["verifier_passed"]) for row in rows),
            "pending_scope_note": "Current scope covers only the initial typed-bytecode families; later compiled frontend families are still absent.",
        },
        "coverage_note": "Machine-readable paper-table rows now exist for the initial typed-bytecode harness, but this is still not the full compiled-frontend table.",
    }
    return summary_payload, rows


def build_memory_surface_diagnostic_exports() -> tuple[dict[str, object], list[dict[str, object]]]:
    summary_path = ROOT / "results" / "M6_memory_surface_followup" / "summary.json"
    boundary_path = ROOT / "results" / "M6_memory_surface_followup" / "call_boundary_snapshots.json"
    delta_path = ROOT / "results" / "M6_memory_surface_followup" / "memory_surface_delta.csv"

    summary_bundle: dict[str, object] = read_json(summary_path)
    boundary_bundle: dict[str, object] = read_json(boundary_path)

    source_rows: list[dict[str, object]] = summary_bundle["rows"]  # type: ignore[assignment]
    negative_controls: list[dict[str, object]] = summary_bundle["negative_controls"]  # type: ignore[assignment]
    boundary_rows = {
        str(row["program_name"]): row
        for row in boundary_bundle["rows"]  # type: ignore[index]
    }

    rows: list[dict[str, object]] = []
    heap_touch_program_count = 0
    for source_row in source_rows:
        program_name = str(source_row["program_name"])
        boundary_row = boundary_rows[program_name]
        reference: dict[str, object] = boundary_row["reference"]  # type: ignore[index]
        lowered: dict[str, object] = boundary_row["lowered"]  # type: ignore[index]
        reference_snapshots: list[dict[str, object]] = reference["boundary_snapshots"]  # type: ignore[assignment]
        lowered_snapshots: list[dict[str, object]] = lowered["boundary_snapshots"]  # type: ignore[assignment]
        reference_accesses: list[dict[str, object]] = reference["accesses"]  # type: ignore[assignment]
        lowered_accesses: list[dict[str, object]] = lowered["accesses"]  # type: ignore[assignment]
        touched_frame_addresses: list[object] = source_row["touched_frame_addresses"]  # type: ignore[assignment]
        touched_heap_addresses: list[object] = source_row["touched_heap_addresses"]  # type: ignore[assignment]
        if touched_heap_addresses:
            heap_touch_program_count += 1
        rows.append(
            {
                "program_name": program_name,
                "suite": source_row["suite"],
                "comparison_mode": source_row["comparison_mode"],
                "base_trace_match": source_row["base_trace_match"],
                "base_final_state_match": source_row["base_final_state_match"],
                "memory_surface_verifier_passed": source_row["memory_surface_verifier_passed"],
                "memory_surface_match": source_row["memory_surface_match"],
                "boundary_snapshot_count": source_row["boundary_snapshot_count"],
                "reference_boundary_snapshot_count": len(reference_snapshots),
                "lowered_boundary_snapshot_count": len(lowered_snapshots),
                "boundary_snapshot_count_match": len(reference_snapshots) == len(lowered_snapshots) == int(source_row["boundary_snapshot_count"]),
                "reference_access_count": len(reference_accesses),
                "lowered_access_count": len(lowered_accesses),
                "access_count_match": len(reference_accesses) == len(lowered_accesses),
                "max_call_depth": source_row["max_call_depth"],
                "undeclared_address_count": source_row["undeclared_address_count"],
                "touched_frame_addresses": format_address_cells(touched_frame_addresses),
                "touched_heap_addresses": format_address_cells(touched_heap_addresses),
            }
        )

    rows.sort(key=lambda row: (row["comparison_mode"], row["program_name"]))

    summary_payload = {
        "experiment": "p1_m6_memory_surface_diagnostic_summary",
        "source_artifacts": [
            relative_path(summary_path),
            relative_path(boundary_path),
            relative_path(delta_path),
        ],
        "rows": rows,
        "negative_controls": negative_controls,
        "summary": {
            "row_count": len(rows),
            "surface_match_count": sum(bool(row["memory_surface_match"]) for row in rows),
            "surface_verifier_pass_count": sum(bool(row["memory_surface_verifier_passed"]) for row in rows),
            "base_trace_match_count": sum(bool(row["base_trace_match"]) for row in rows),
            "base_final_state_match_count": sum(bool(row["base_final_state_match"]) for row in rows),
            "boundary_snapshot_alignment_count": sum(
                bool(row["boundary_snapshot_count_match"]) and bool(row["access_count_match"])
                for row in rows
            ),
            "heap_touch_program_count": heap_touch_program_count,
            "frame_only_program_count": len(rows) - heap_touch_program_count,
            "max_call_depth": max(int(row["max_call_depth"]) for row in rows),
            "max_boundary_snapshot_count": max(int(row["boundary_snapshot_count"]) for row in rows),
            "negative_control_count": len(negative_controls),
            "negative_control_error_classes": counter_rows(
                Counter(str(row["error_class"]) for row in negative_controls),
                label="error_class",
            ),
            "by_comparison_mode": counter_rows(
                Counter(str(row["comparison_mode"]) for row in rows),
                label="comparison_mode",
            ),
        },
        "coverage_note": "Appendix-level D0 diagnostic only: this preserves the same tiny typed-bytecode control-flow slice and does not introduce a new claim layer.",
        "caption_facts": [
            (
                f"All {len(rows)} annotated call/ret rows preserve base exactness and match "
                "between reference and lowered memory-surface diagnostics."
            ),
            (
                f"{len(negative_controls)} deterministic negative controls fail on undeclared-address "
                "checks; this remains a D0-supporting diagnostic layer, not a broader frontend claim."
            ),
        ],
    }
    return summary_payload, rows


def main() -> None:
    environment = detect_runtime_environment()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    failure_summary, failure_rows = build_failure_taxonomy_exports()
    write_json(
        OUT_DIR / "m4_failure_taxonomy_summary.json",
        {
            "environment": environment.as_dict(),
            **failure_summary,
        },
    )
    write_csv(
        OUT_DIR / "m4_failure_taxonomy_by_family.csv",
        failure_rows,
        [
            "mask_mode",
            "split",
            "family",
            "provenance_class",
            "root_cause_class",
            "root_cause_head",
            "program_count",
            "failed_program_count",
            "failure_fraction",
            "median_first_mismatch_step",
            "min_first_mismatch_step",
            "max_first_mismatch_step",
        ],
    )

    boundary_summary, boundary_rows = build_real_trace_boundary_exports()
    write_json(
        OUT_DIR / "m4_real_trace_boundary_summary.json",
        {
            "environment": environment.as_dict(),
            **boundary_summary,
        },
    )
    write_csv(
        OUT_DIR / "m4_real_trace_boundary_rows.csv",
        boundary_rows,
        [
            "suite_bundle",
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

    exact_table_summary, exact_table_rows = build_exact_trace_final_state_table()
    write_json(
        OUT_DIR / "exact_trace_final_state_table.json",
        {
            "environment": environment.as_dict(),
            **exact_table_summary,
        },
    )
    write_csv(
        OUT_DIR / "exact_trace_final_state_table.csv",
        exact_table_rows,
        [
            "program_name",
            "suite",
            "comparison_mode",
            "length_bucket",
            "success_target",
            "trace_match",
            "final_state_match",
            "status_label",
            "bytecode_instruction_count",
            "lowered_instruction_count",
            "instruction_count_match",
            "verifier_passed",
            "first_divergence_step",
            "failure_class",
            "failure_reason",
        ],
    )

    memory_surface_summary, memory_surface_rows = build_memory_surface_diagnostic_exports()
    write_json(
        OUT_DIR / "m6_memory_surface_diagnostic_summary.json",
        {
            "environment": environment.as_dict(),
            **memory_surface_summary,
        },
    )
    write_csv(
        OUT_DIR / "m6_memory_surface_diagnostic_rows.csv",
        memory_surface_rows,
        [
            "program_name",
            "suite",
            "comparison_mode",
            "base_trace_match",
            "base_final_state_match",
            "memory_surface_verifier_passed",
            "memory_surface_match",
            "boundary_snapshot_count",
            "reference_boundary_snapshot_count",
            "lowered_boundary_snapshot_count",
            "boundary_snapshot_count_match",
            "reference_access_count",
            "lowered_access_count",
            "access_count_match",
            "max_call_depth",
            "undeclared_address_count",
            "touched_frame_addresses",
            "touched_heap_addresses",
        ],
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
