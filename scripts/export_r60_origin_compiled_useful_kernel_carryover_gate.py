"""Export the saved post-H54 useful-kernel carryover gate for R60."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R60_origin_compiled_useful_kernel_carryover_gate"


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
    milestone = ROOT / "docs" / "milestones" / "R60_origin_compiled_useful_kernel_carryover_gate"
    return {
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-25-post-h54-useful-kernel-stopgo-design.md"),
        "milestones_readme_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "r60_readme_text": read_text(milestone / "README.md"),
        "r60_status_text": read_text(milestone / "status.md"),
        "r60_todo_text": read_text(milestone / "todo.md"),
        "r60_acceptance_text": read_text(milestone / "acceptance.md"),
        "r60_artifact_index_text": read_text(milestone / "artifact_index.md"),
        "carryover_scope_text": read_text(milestone / "carryover_scope.md"),
        "execution_manifest_text": read_text(milestone / "execution_manifest.md"),
        "stop_conditions_text": read_text(milestone / "stop_conditions.md"),
        "kernel_selection_text": read_text(milestone / "kernel_selection.md"),
        "h54_summary": read_json(ROOT / "results" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h54 = inputs["h54_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "r60_docs_define_saved_successor_carryover_gate_only",
            "status": "pass"
            if contains_all(
                inputs["r60_readme_text"],
                [
                    "saved successor exact runtime gate",
                    "saved_successor_design_only",
                    "minimal preserved useful-kernel suite",
                    "exactly",
                ],
            )
            and contains_all(
                inputs["r60_status_text"],
                [
                    "saved_successor_design_only",
                    "active: `false`",
                    "`sum_i32_buffer`, `count_nonzero_i32_buffer`",
                ],
            )
            and contains_all(
                inputs["r60_todo_text"],
                [
                    "freeze the admitted kernel suite",
                    "define source/spec/lowered comparators",
                    "audit compiler-side work leakage",
                    "localize first failure",
                ],
            )
            and contains_all(
                inputs["r60_acceptance_text"],
                [
                    "exact source-vs-lowered trace parity",
                    "exact source-vs-lowered final-state parity",
                    "exact source-vs-spec parity",
                    "explicit kernel and state-pressure coverage",
                    "explicit compiler-work leakage accounting",
                ],
            )
            and contains_all(
                inputs["execution_manifest_text"],
                [
                    "transparent source execution",
                    "transparent lowered-trace execution",
                    "current linear trace-vm execution",
                    "current accelerated trace-vm execution",
                ],
            )
            and contains_all(
                inputs["stop_conditions_text"],
                [
                    "exactness failure on any admitted row",
                    "compiler-side work leakage",
                    "admitted kernel set changing",
                ],
            )
            else "blocked",
            "notes": "R60 should remain saved successor gate storage only and should predeclare exactness, scope, and stop conditions.",
        },
        {
            "item_id": "r60_scope_and_kernel_selection_stay_below_r44_family_lift",
            "status": "pass"
            if contains_all(
                inputs["carryover_scope_text"],
                [
                    "`sum_i32_buffer`",
                    "`count_nonzero_i32_buffer`",
                    "`histogram16_u8`",
                    "arbitrary `c`",
                    "broader wasm",
                ],
            )
            and contains_all(
                inputs["kernel_selection_text"],
                [
                    "stay below the preserved `r44` three-kernel ladder",
                    "both are already preserved useful-kernel shapes",
                    "avoid introducing the wider bucket-update",
                    "`histogram16_u8`",
                ],
            )
            else "blocked",
            "notes": "R60 should keep the first carryover pass on the smallest preserved useful-kernel pair and leave histogram16_u8 out of scope.",
        },
        {
            "item_id": "indices_record_r60_as_saved_successor_gate_not_active_runtime_lane",
            "status": "pass"
            if str(h54["selected_outcome"]) == "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
            and str(h54["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and contains_all(
                inputs["design_text"],
                [
                    "`r60_origin_compiled_useful_kernel_carryover_gate`",
                    "`sum_i32_buffer`",
                    "`count_nonzero_i32_buffer`",
                    "`r61_origin_compiled_useful_kernel_value_gate`",
                ],
            )
            and contains_all(
                inputs["milestones_readme_text"],
                [
                    "`r60_origin_compiled_useful_kernel_carryover_gate/`",
                    "saved successor exact useful-kernel carryover gate; not active",
                ],
            )
            else "blocked",
            "notes": "Shared successor indexes should expose R60 as saved gate storage while H54 remains the current closeout.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "R60 stores one saved successor carryover gate for a minimal preserved useful-kernel pair.",
            "R60 fixes exact source/spec/lowered parity and compiler-leakage accounting as the only admissible acceptance criteria if activated later.",
            "R60 keeps the first carryover pass below the preserved R44 three-kernel family by excluding histogram16_u8.",
        ],
        "unsupported_here": [
            "R60 does not represent an executed runtime gate yet.",
            "R60 does not widen into arbitrary C or broader Wasm.",
            "R60 does not itself prove useful-kernel carryover success.",
        ],
        "disconfirmed_here": [
            "The idea that post-H54 compiled useful-kernel carryover should start by reopening the full preserved useful-case family instead of the smallest preserved pair.",
        ],
        "distilled_result": {
            "active_stage": "r60_origin_compiled_useful_kernel_carryover_gate",
            "current_active_docs_only_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "current_planning_bundle": "f30_post_h54_useful_kernel_bridge_bundle",
            "selected_outcome": "saved_successor_carryover_gate_only",
            "admitted_kernel_suite": ["sum_i32_buffer", "count_nonzero_i32_buffer"],
            "out_of_scope_examples": ["histogram16_u8", "arbitrary_c", "broad_wasm"],
            "only_followup_packet_if_activated": "r61_origin_compiled_useful_kernel_value_gate",
            "next_required_lane_if_activated": "r60_origin_compiled_useful_kernel_carryover_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/R60_origin_compiled_useful_kernel_carryover_gate/README.md",
            inputs["r60_readme_text"],
            ["saved successor exact runtime gate", "minimal preserved useful-kernel suite"],
        ),
        (
            "docs/milestones/R60_origin_compiled_useful_kernel_carryover_gate/carryover_scope.md",
            inputs["carryover_scope_text"],
            ["`sum_i32_buffer`", "`count_nonzero_i32_buffer`", "`histogram16_u8`"],
        ),
        (
            "docs/milestones/R60_origin_compiled_useful_kernel_carryover_gate/kernel_selection.md",
            inputs["kernel_selection_text"],
            ["stay below the preserved `R44` three-kernel ladder", "avoid introducing the wider bucket-update"],
        ),
        (
            "docs/milestones/R60_origin_compiled_useful_kernel_carryover_gate/execution_manifest.md",
            inputs["execution_manifest_text"],
            ["transparent source execution", "current accelerated trace-VM execution"],
        ),
        (
            "docs/milestones/R60_origin_compiled_useful_kernel_carryover_gate/stop_conditions.md",
            inputs["stop_conditions_text"],
            ["exactness failure on any admitted row", "compiler-side work leakage"],
        ),
        (
            "docs/plans/2026-03-25-post-h54-useful-kernel-stopgo-design.md",
            inputs["design_text"],
            ["`R60_origin_compiled_useful_kernel_carryover_gate`", "`sum_i32_buffer`", "`count_nonzero_i32_buffer`"],
        ),
        (
            "docs/milestones/README.md",
            inputs["milestones_readme_text"],
            ["`R60_origin_compiled_useful_kernel_carryover_gate/`", "saved successor exact useful-kernel carryover gate; not active"],
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
        "admitted_kernel_suite": distilled["admitted_kernel_suite"],
        "out_of_scope_examples": distilled["out_of_scope_examples"],
        "only_followup_packet_if_activated": distilled["only_followup_packet_if_activated"],
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
