"""Export the saved post-H54 useful-kernel value gate for R61."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R61_origin_compiled_useful_kernel_value_gate"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles) and line not in seen:
            hits.append(line)
            seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def load_inputs() -> dict[str, Any]:
    milestone = ROOT / "docs" / "milestones" / "R61_origin_compiled_useful_kernel_value_gate"
    return {
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-25-post-h54-useful-kernel-stopgo-design.md"),
        "milestones_readme_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "r61_readme_text": read_text(milestone / "README.md"),
        "r61_status_text": read_text(milestone / "status.md"),
        "r61_todo_text": read_text(milestone / "todo.md"),
        "r61_acceptance_text": read_text(milestone / "acceptance.md"),
        "r61_artifact_index_text": read_text(milestone / "artifact_index.md"),
        "comparator_matrix_text": read_text(milestone / "comparator_matrix.md"),
        "execution_manifest_text": read_text(milestone / "execution_manifest.md"),
        "stop_conditions_text": read_text(milestone / "stop_conditions.md"),
        "value_risk_notes_text": read_text(milestone / "value_risk_notes.md"),
        "h54_summary": read_json(ROOT / "results" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h54 = inputs["h54_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "r61_docs_define_saved_successor_value_gate_only",
            "status": "pass"
            if contains_all(
                inputs["r61_readme_text"],
                [
                    "saved successor comparator/value gate",
                    "saved_successor_design_only",
                    "run only after a positive exact `r60`",
                ],
            )
            and contains_all(
                inputs["r61_status_text"],
                [
                    "saved_successor_design_only",
                    "active: `false`",
                    "`r60_origin_compiled_useful_kernel_carryover_gate`",
                ],
            )
            and contains_all(
                inputs["r61_todo_text"],
                [
                    "reuse only the exact `r60` rows",
                    "compare internal and external baselines",
                    "account for export and compiler overhead",
                    "report one bounded-value verdict",
                ],
            )
            and contains_all(
                inputs["r61_acceptance_text"],
                [
                    "exactness parity across admitted routes",
                    "end-to-end latency and throughput",
                    "retrieval-share and trace-length decomposition",
                    "compiler/export overhead accounting",
                    "one explicit lane verdict",
                ],
            )
            and contains_all(
                inputs["comparator_matrix_text"],
                [
                    "transparent source execution",
                    "transparent lowered-trace execution",
                    "free-running exact linear trace-vm execution",
                    "plain external reference runtime",
                ],
            )
            and contains_all(
                inputs["stop_conditions_text"],
                [
                    "any route loses exactness",
                    "value conclusion depends on undeclared compiler-side work",
                    "comparator set changes",
                ],
            )
            else "blocked",
            "notes": "R61 should remain saved successor value-gate storage only and should predeclare comparators, accounting, and stop conditions.",
        },
        {
            "item_id": "r61_value_risk_notes_preserve_strict_negative_interpretation",
            "status": "pass"
            if contains_all(
                inputs["value_risk_notes_text"],
                [
                    "bounded value question on the exact `r60` rows only",
                    "compiler-side pre-work",
                    "slower than a plain transparent reference path",
                    "not admissible as bounded value",
                    "`r60`-level failure",
                ],
            )
            and contains_all(
                inputs["execution_manifest_text"],
                [
                    "only execute on exact positive `r60` rows",
                ],
            )
            else "blocked",
            "notes": "R61 should treat exact-but-value-negative outcomes as real negative evidence rather than partial systems success.",
        },
        {
            "item_id": "indices_record_r61_as_saved_successor_gate_not_active_runtime_lane",
            "status": "pass"
            if str(h54["selected_outcome"]) == "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
            and str(h54["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and contains_all(
                inputs["design_text"],
                [
                    "`r61_origin_compiled_useful_kernel_value_gate`",
                    "compiler/export overhead accounting",
                    "`h56_post_r60_r61_useful_kernel_decision_packet`",
                ],
            )
            and contains_all(
                inputs["milestones_readme_text"],
                [
                    "`r61_origin_compiled_useful_kernel_value_gate/`",
                    "saved successor value gate; not active",
                ],
            )
            else "blocked",
            "notes": "Shared successor indexes should expose R61 as saved gate storage while H54 remains the current closeout.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "R61 stores one saved successor value gate that runs only on exact positive R60 rows if activated later.",
            "R61 fixes internal and external comparators plus overhead accounting as the only admissible bounded-value question.",
            "R61 preserves a strict reading where exact-but-value-negative outcomes count as negative evidence.",
        ],
        "unsupported_here": [
            "R61 does not represent an executed comparator/value gate yet.",
            "R61 does not itself prove bounded value.",
            "R61 does not widen into broader compiled-family claims.",
        ],
        "disconfirmed_here": [
            "The idea that any exact useful-kernel carryover would automatically count as systems success without explicit bounded-value accounting.",
        ],
        "distilled_result": {
            "active_stage": "r61_origin_compiled_useful_kernel_value_gate",
            "current_active_docs_only_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "current_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "selected_outcome": "saved_successor_value_gate_only",
            "prerequisite_gate_if_activated": "r60_origin_compiled_useful_kernel_carryover_gate",
            "only_followup_packet_if_activated": "h56_post_r60_r61_useful_kernel_decision_packet",
            "declared_comparators": [
                "transparent_source_execution",
                "transparent_lowered_trace_execution",
                "free_running_exact_linear_trace_vm_execution",
                "free_running_exact_accelerated_trace_vm_execution",
                "plain_external_reference_runtime",
            ],
            "next_required_lane_if_activated": "r61_origin_compiled_useful_kernel_value_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/R61_origin_compiled_useful_kernel_value_gate/README.md",
            inputs["r61_readme_text"],
            ["saved successor comparator/value gate", "positive exact `R60`"],
        ),
        (
            "docs/milestones/R61_origin_compiled_useful_kernel_value_gate/comparator_matrix.md",
            inputs["comparator_matrix_text"],
            ["transparent source execution", "plain external reference runtime"],
        ),
        (
            "docs/milestones/R61_origin_compiled_useful_kernel_value_gate/value_risk_notes.md",
            inputs["value_risk_notes_text"],
            ["bounded value question on the exact `R60` rows only", "not admissible as bounded value"],
        ),
        (
            "docs/milestones/R61_origin_compiled_useful_kernel_value_gate/execution_manifest.md",
            inputs["execution_manifest_text"],
            ["Only execute on exact positive `R60` rows."],
        ),
        (
            "docs/plans/2026-03-25-post-h54-useful-kernel-stopgo-design.md",
            inputs["design_text"],
            ["`R61_origin_compiled_useful_kernel_value_gate`", "compiler/export overhead accounting"],
        ),
        (
            "docs/milestones/README.md",
            inputs["milestones_readme_text"],
            ["`R61_origin_compiled_useful_kernel_value_gate/`", "saved successor value gate; not active"],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "current_active_docs_only_stage": distilled["current_active_docs_only_stage"],
        "current_planning_bundle": distilled["current_planning_bundle"],
        "selected_outcome": distilled["selected_outcome"],
        "prerequisite_gate_if_activated": distilled["prerequisite_gate_if_activated"],
        "only_followup_packet_if_activated": distilled["only_followup_packet_if_activated"],
        "declared_comparators": distilled["declared_comparators"],
        "next_required_lane_if_activated": distilled["next_required_lane_if_activated"],
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})
    write_json(OUT_DIR / "summary.json", {"summary": summary, "runtime_environment": environment_payload()})


if __name__ == "__main__":
    main()
