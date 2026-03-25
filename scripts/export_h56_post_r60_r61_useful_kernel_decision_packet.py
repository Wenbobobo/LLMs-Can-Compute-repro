"""Export the saved post-R60/R61 useful-kernel decision packet for H56."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H56_post_r60_r61_useful_kernel_decision_packet"


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
    milestone = ROOT / "docs" / "milestones" / "H56_post_r60_r61_useful_kernel_decision_packet"
    return {
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-25-post-h54-useful-kernel-stopgo-design.md"),
        "milestones_readme_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "h56_readme_text": read_text(milestone / "README.md"),
        "h56_status_text": read_text(milestone / "status.md"),
        "h56_todo_text": read_text(milestone / "todo.md"),
        "h56_acceptance_text": read_text(milestone / "acceptance.md"),
        "h56_artifact_index_text": read_text(milestone / "artifact_index.md"),
        "decision_matrix_text": read_text(milestone / "decision_matrix.md"),
        "h54_summary": read_json(ROOT / "results" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h54 = inputs["h54_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "h56_docs_define_saved_successor_decision_packet_only",
            "status": "pass"
            if contains_all(
                inputs["h56_readme_text"],
                [
                    "saved successor docs-only decision packet",
                    "saved_successor_design_only",
                    "interpret `r60` and `r61` together",
                ],
            )
            and contains_all(
                inputs["h56_status_text"],
                [
                    "saved_successor_design_only",
                    "active: `false`",
                    "reads: `r60`, `r61`",
                ],
            )
            and contains_all(
                inputs["h56_todo_text"],
                [
                    "read `r60` and `r61` together",
                    "decide stop, narrow freeze, or later explicit packet",
                    "preserve `h43` as paper-grade endpoint",
                ],
            )
            and contains_all(
                inputs["h56_acceptance_text"],
                [
                    "stays docs-only",
                    "records one explicit selected outcome",
                    "preserves the no-widening defaults",
                    "separate explicit packet",
                ],
            )
            and contains_all(
                inputs["decision_matrix_text"],
                [
                    "`freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`",
                    "`authorize_later_compiled_useful_family_packet`",
                    "`stop_as_compiled_boundary_toy_only`",
                    "`stop_due_to_compiler_work_leakage`",
                ],
            )
            else "blocked",
            "notes": "H56 should remain saved successor decision storage only, with one explicit later stop/go matrix.",
        },
        {
            "item_id": "h56_preserves_h54_closeout_and_h43_ceiling",
            "status": "pass"
            if str(h54["selected_outcome"]) == "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
            and str(h54["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            else "blocked",
            "notes": "H56 must preserve the current H54 closeout and H43 claim ceiling while storing later decision options only.",
        },
        {
            "item_id": "indices_record_h56_as_saved_successor_not_active_closeout",
            "status": "pass"
            if contains_all(
                inputs["design_text"],
                [
                    "`h56_post_r60_r61_useful_kernel_decision_packet`",
                    "`authorize_later_compiled_useful_family_packet`",
                    "`stop_as_compiled_boundary_toy_only`",
                ],
            )
            and contains_all(
                inputs["milestones_readme_text"],
                [
                    "`h56_post_r60_r61_useful_kernel_decision_packet/`",
                    "saved successor docs-only decision packet; not active",
                ],
            )
            else "blocked",
            "notes": "Shared successor indexes should expose H56 as saved decision storage while H54 remains the current active closeout.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H56 stores one saved successor docs-only decision packet that will later read R60 and R61 together if activated.",
            "H56 preserves H54 as the current active closeout and H43 as the paper-grade endpoint.",
            "H56 makes later scope lift conditional on one separate explicit packet rather than automatic momentum.",
        ],
        "unsupported_here": [
            "H56 does not replace H54 as the current active docs-only packet.",
            "H56 does not itself authorize a wider useful-family wave yet.",
            "H56 does not claim any executed R60/R61 result.",
        ],
        "disconfirmed_here": [
            "The idea that successor decision storage should silently widen scope without an explicit later packet.",
        ],
        "distilled_result": {
            "active_stage": "h56_post_r60_r61_useful_kernel_decision_packet",
            "current_active_docs_only_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": "saved_successor_decision_packet_only",
            "declared_decision_matrix": [
                "freeze_minimal_useful_kernel_bridge_supported_without_bounded_value",
                "authorize_later_compiled_useful_family_packet",
                "stop_as_compiled_boundary_toy_only",
                "stop_due_to_compiler_work_leakage",
            ],
            "prerequisite_inputs_if_activated": [
                "r60_origin_compiled_useful_kernel_carryover_gate",
                "r61_origin_compiled_useful_kernel_value_gate",
            ],
            "next_required_lane_if_activated": "h56_post_r60_r61_useful_kernel_decision_packet",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/H56_post_r60_r61_useful_kernel_decision_packet/README.md",
            inputs["h56_readme_text"],
            ["saved successor docs-only decision packet", "interpret `R60` and `R61` together"],
        ),
        (
            "docs/milestones/H56_post_r60_r61_useful_kernel_decision_packet/decision_matrix.md",
            inputs["decision_matrix_text"],
            ["`freeze_minimal_useful_kernel_bridge_supported_without_bounded_value`", "`authorize_later_compiled_useful_family_packet`"],
        ),
        (
            "docs/milestones/H56_post_r60_r61_useful_kernel_decision_packet/acceptance.md",
            inputs["h56_acceptance_text"],
            ["stays docs-only", "separate explicit packet"],
        ),
        (
            "docs/plans/2026-03-25-post-h54-useful-kernel-stopgo-design.md",
            inputs["design_text"],
            ["`H56_post_r60_r61_useful_kernel_decision_packet`", "`stop_as_compiled_boundary_toy_only`"],
        ),
        (
            "docs/milestones/README.md",
            inputs["milestones_readme_text"],
            ["`H56_post_r60_r61_useful_kernel_decision_packet/`", "saved successor docs-only decision packet; not active"],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "current_active_docs_only_stage": distilled["current_active_docs_only_stage"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "selected_outcome": distilled["selected_outcome"],
        "declared_decision_matrix": distilled["declared_decision_matrix"],
        "prerequisite_inputs_if_activated": distilled["prerequisite_inputs_if_activated"],
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
