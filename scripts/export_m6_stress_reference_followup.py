"""Export stress-suite and external-reference artifacts for the M6 follow-up."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from bytecode import run_stress_reference_harness, stress_reference_cases
from utils import detect_runtime_environment


def _encode_row(row: dict[str, object]) -> dict[str, object]:
    encoded = dict(row)
    encoded.pop("external_reference", None)
    return encoded


def main() -> None:
    environment = detect_runtime_environment()
    cases = stress_reference_cases()
    rows = run_stress_reference_harness(cases)
    external_rows = [row["external_reference"] for row in rows]
    negative_rows = [row for row in rows if row["comparison_mode"] in {"verifier_negative", "memory_surface_negative"}]
    mismatch_counts = Counter(str(row["mismatch_class"]) for row in rows if row["mismatch_class"] is not None)

    out_dir = Path("results/M6_stress_reference_followup")
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_payload = {
        "experiment": "m6_stress_reference_followup",
        "environment": environment.as_dict(),
        "summary": {
            "row_count": len(rows),
            "positive_row_count": sum(
                row["comparison_mode"] in {"medium_exact_trace", "long_exact_final_state"} for row in rows
            ),
            "negative_control_count": len(negative_rows),
            "exact_trace_match_count": sum(
                row["comparison_mode"] == "medium_exact_trace" and row["mismatch_class"] is None for row in rows
            ),
            "exact_final_state_match_count": sum(
                row["comparison_mode"] == "long_exact_final_state" and row["mismatch_class"] is None for row in rows
            ),
            "matched_negative_count": sum(row["mismatch_class"] is None for row in negative_rows),
            "diagnostic_surface_match_count": sum(
                row["diagnostic_surface_match"] is True for row in rows if row["diagnostic_surface_match"] is not None
            ),
            "mismatch_class_counts": dict(mismatch_counts),
        },
        "rows": [_encode_row(row) for row in rows],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")
    (out_dir / "stress_suite_rows.json").write_text(
        json.dumps(
            {
                "experiment": "m6_stress_suite_rows",
                "environment": environment.as_dict(),
                "rows": [_encode_row(row) for row in rows],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "oracle_agreement_rows.json").write_text(
        json.dumps(
            {
                "experiment": "m6_oracle_agreement_rows",
                "environment": environment.as_dict(),
                "rows": [
                    {
                        "program_name": row["program_name"],
                        "comparison_mode": row["comparison_mode"],
                        "verifier_passed": row["verifier_passed"],
                        "spec_contract_passed": row["spec_contract_passed"],
                        "trace_match_current_lowered": row["trace_match_current_lowered"],
                        "trace_match_current_spec": row["trace_match_current_spec"],
                        "trace_match_lowered_spec": row["trace_match_lowered_spec"],
                        "all_final_state_match": row["all_final_state_match"],
                        "first_divergence_step": row["first_divergence_step"],
                        "diagnostic_surface_match": row["diagnostic_surface_match"],
                        "mismatch_class": row["mismatch_class"],
                        "failure_reason": row["failure_reason"],
                    }
                    for row in rows
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "external_reference_rows.json").write_text(
        json.dumps(
            {
                "experiment": "m6_external_reference_rows",
                "environment": environment.as_dict(),
                "rows": external_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "negative_control_rows.json").write_text(
        json.dumps(
            {
                "experiment": "m6_negative_control_rows",
                "environment": environment.as_dict(),
                "rows": [_encode_row(row) for row in negative_rows],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "README.md").write_text(
        "\n".join(
            [
                "# M6 Stress Reference Follow-up",
                "",
                "One branch-selected helper checkpoint braid family plus one standalone Python spec oracle.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `stress_suite_rows.json`",
                "- `oracle_agreement_rows.json`",
                "- `external_reference_rows.json`",
                "- `negative_control_rows.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(out_dir.as_posix())


if __name__ == "__main__":
    main()
