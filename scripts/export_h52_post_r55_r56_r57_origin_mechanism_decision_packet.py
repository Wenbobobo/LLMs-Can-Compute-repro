"""Export the post-R55/R56/R57 Origin mechanism decision packet for H52."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet"


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
    except Exception as exc:  # pragma: no cover - defensive fallback
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
    return {
        "h52_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "README.md"
        ),
        "h52_status_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "status.md"
        ),
        "h52_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "todo.md"
        ),
        "h52_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "acceptance.md"
        ),
        "h52_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "artifact_index.md"
        ),
        "h52_decision_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "decision_matrix.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "milestones_readme_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "r55_summary": read_json(ROOT / "results" / "R55_origin_2d_hardmax_retrieval_equivalence_gate" / "summary.json"),
        "r56_summary": read_json(ROOT / "results" / "R56_origin_append_only_trace_vm_semantics_gate" / "summary.json"),
        "r57_summary": read_json(ROOT / "results" / "R57_origin_accelerated_trace_vm_comparator_gate" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "h50_summary": read_json(ROOT / "results" / "H50_post_r51_r52_scope_decision_packet" / "summary.json"),
        "h51_summary": read_json(ROOT / "results" / "H51_post_h50_origin_mechanism_reentry_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    r55 = inputs["r55_summary"]["summary"]
    r56 = inputs["r56_summary"]["summary"]
    r57 = inputs["r57_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    h50 = inputs["h50_summary"]["summary"]
    h51 = inputs["h51_summary"]["summary"]
    return [
        {
            "item_id": "h52_docs_record_one_completed_closeout_outcome",
            "status": "pass"
            if contains_all(
                inputs["h52_readme_text"],
                [
                    "completed current docs-only mechanism decision packet",
                    "selected outcome:",
                    "`freeze_origin_mechanism_supported_without_fastpath_value`",
                    "`freeze_origin_mechanism_supported_with_fastpath_value`",
                    "`stop_as_partial_mechanism_only`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h52_status_text"],
                [
                    "completed docs-only mechanism decision packet",
                    "becomes the current active docs-only packet",
                    "preserves `h51` as the prior mechanism-reentry packet",
                    "selects `freeze_origin_mechanism_supported_without_fastpath_value`",
                    "restores `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["h52_todo_text"],
                [
                    "[x] read landed `r55`, `r56`, and `r57` explicitly",
                    "[x] decide whether fast-path value is supported",
                    "[x] preserve `h43`",
                    "[x] keep transformed or trainable entry blocked",
                ],
            )
            and contains_all(
                inputs["h52_acceptance_text"],
                [
                    "`h52` remains docs-only",
                    "exactly one decision outcome is selected",
                    "`r55`, `r56`, and `r57` are all read explicitly",
                    "`h43` remains visible as the paper-grade endpoint",
                    "transformed and trainable entry stay blocked",
                ],
            )
            and contains_all(
                inputs["h52_decision_matrix_text"],
                [
                    "| `freeze_origin_mechanism_supported_with_fastpath_value` |",
                    "| `freeze_origin_mechanism_supported_without_fastpath_value` |",
                    "| `stop_as_partial_mechanism_only` |",
                ],
            )
            and contains_all(
                inputs["h52_artifact_index_text"],
                [
                    "scripts/export_h52_post_r55_r56_r57_origin_mechanism_decision_packet.py",
                    "tests/test_export_h52_post_r55_r56_r57_origin_mechanism_decision_packet.py",
                    "results/h52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "H52 must land as one explicit docs-only closeout packet with one selected outcome.",
        },
        {
            "item_id": "h52_reads_r55_r56_r57_explicitly_before_closing",
            "status": "pass"
            if str(r55["gate"]["lane_verdict"]) == "retrieval_equivalence_supported_exactly"
            and int(r55["gate"]["exact_task_count"]) == 5
            and str(r56["gate"]["lane_verdict"]) == "trace_vm_semantics_supported_exactly"
            and int(r56["gate"]["exact_task_count"]) == 5
            and str(r57["gate"]["lane_verdict"]) == "accelerated_trace_vm_lacks_bounded_value"
            and str(r57["gate"]["selected_h52_outcome"]) == "freeze_origin_mechanism_supported_without_fastpath_value"
            and int(r57["gate"]["accelerated_faster_than_linear_count"]) == 0
            and int(r57["gate"]["accelerated_faster_than_external_count"]) == 0
            else "blocked",
            "notes": "H52 should read the two positive exact gates plus the negative comparator result explicitly rather than infer by momentum.",
        },
        {
            "item_id": "h52_preserves_h50_h43_and_blocked_future_entry",
            "status": "pass"
            if str(h50["selected_outcome"]) == "stop_as_exact_without_system_value"
            and str(h50["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and str(h51["selected_outcome"]) == "authorize_origin_mechanism_reentry_through_r55_first"
            else "blocked",
            "notes": "H52 must preserve the broader-route H50 closeout, keep H43 as the paper-grade endpoint, and keep blocked future entry blocked.",
        },
        {
            "item_id": "shared_control_surfaces_make_h52_the_current_closed_state",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "no active downstream runtime lane",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`no_active_downstream_runtime_lane`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "- `h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "the current downstream scientific lane is:",
                    "- `no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| d3c |",
                    "| h52 |",
                    "freeze_origin_mechanism_supported_without_fastpath_value",
                ],
            )
            and contains_all(
                inputs["milestones_readme_text"],
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet/`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate/`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`r56` `r57/h52` mechanism closeout wave",
                    "new `scripts/export_h52_post_r55_r56_r57_origin_mechanism_decision_packet.py`",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should expose H52 as the current closed state and remove any active downstream runtime lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "R55 and R56 support the narrow mechanism chain exactly on the fixed mechanism-reentry suite.",
            "R57 keeps the comparator exact while disconfirming bounded fast-path value for the accelerated route.",
            "H52 closes the lane as mechanism support without fast-path value while preserving H50 and H43.",
        ],
        "unsupported_here": [
            "H52 does not authorize transformed-model entry, trainable entry, arbitrary C, or broad Wasm claims.",
            "H52 does not overturn H50 on the broader post-H49 bounded-value question.",
            "H52 does not raise the claim ceiling above H43 or reopen an active downstream runtime lane.",
        ],
        "disconfirmed_here": [
            "The idea that a positive narrow mechanism chain automatically yields bounded fast-path value or justifies broader route reopening.",
        ],
        "distilled_result": {
            "active_stage": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
            "preserved_prior_mechanism_reentry_packet": "h51_post_h50_origin_mechanism_reentry_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_planning_bundle": "f28_post_h50_origin_mechanism_reentry_bundle",
            "selected_outcome": "freeze_origin_mechanism_supported_without_fastpath_value",
            "non_selected_alternatives": [
                "freeze_origin_mechanism_supported_with_fastpath_value",
                "stop_as_partial_mechanism_only",
            ],
            "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
            "preserved_exact_retrieval_gate": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
            "preserved_exact_trace_vm_gate": "r56_origin_append_only_trace_vm_semantics_gate",
            "preserved_comparator_gate": "r57_origin_accelerated_trace_vm_comparator_gate",
            "blocked_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "blocked_future_gates": [
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/H52_post_r55_r56_r57_origin_mechanism_decision_packet/README.md",
            inputs["h52_readme_text"],
            [
                "selected outcome:",
                "`freeze_origin_mechanism_supported_without_fastpath_value`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        (
            "docs/milestones/H52_post_r55_r56_r57_origin_mechanism_decision_packet/status.md",
            inputs["h52_status_text"],
            [
                "becomes the current active docs-only packet",
                "restores `no_active_downstream_runtime_lane`",
            ],
        ),
        (
            "README.md",
            inputs["readme_text"],
            [
                "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "no active downstream runtime lane",
            ],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            [
                "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            [
                "the current active stage is:",
                "- `h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
            ],
        ),
        (
            "docs/claims_matrix.md",
            inputs["claims_matrix_text"],
            ["| D3c |", "| H52 |"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            [
                "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        (
            "results/R57_origin_accelerated_trace_vm_comparator_gate/summary.json",
            json.dumps(inputs["r57_summary"]),
            [
                "accelerated_trace_vm_lacks_bounded_value",
                "freeze_origin_mechanism_supported_without_fastpath_value",
            ],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "preserved_prior_docs_only_closeout": distilled["preserved_prior_docs_only_closeout"],
        "preserved_prior_mechanism_reentry_packet": distilled["preserved_prior_mechanism_reentry_packet"],
        "current_active_routing_stage": distilled["current_active_routing_stage"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "current_planning_bundle": distilled["current_planning_bundle"],
        "selected_outcome": distilled["selected_outcome"],
        "non_selected_alternatives": distilled["non_selected_alternatives"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "preserved_exact_retrieval_gate": distilled["preserved_exact_retrieval_gate"],
        "preserved_exact_trace_vm_gate": distilled["preserved_exact_trace_vm_gate"],
        "preserved_comparator_gate": distilled["preserved_comparator_gate"],
        "blocked_future_bundle": distilled["blocked_future_bundle"],
        "blocked_future_gates": distilled["blocked_future_gates"],
        "next_required_lane": distilled["next_required_lane"],
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
