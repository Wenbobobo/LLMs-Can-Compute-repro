"""Export the post-H52 compiled-boundary reentry packet for H53."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H53_post_h52_compiled_boundary_reentry_packet"


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
        "h53_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H53_post_h52_compiled_boundary_reentry_packet" / "README.md"
        ),
        "h53_status_text": read_text(
            ROOT / "docs" / "milestones" / "H53_post_h52_compiled_boundary_reentry_packet" / "status.md"
        ),
        "h53_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H53_post_h52_compiled_boundary_reentry_packet" / "todo.md"
        ),
        "h53_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H53_post_h52_compiled_boundary_reentry_packet" / "acceptance.md"
        ),
        "h53_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H53_post_h52_compiled_boundary_reentry_packet" / "artifact_index.md"
        ),
        "decision_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "H53_post_h52_compiled_boundary_reentry_packet" / "decision_matrix.md"
        ),
        "f29_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F29_post_h52_restricted_compiled_boundary_bundle" / "README.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h52_summary": read_json(ROOT / "results" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h52 = inputs["h52_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "h53_docs_record_explicit_compiled_boundary_reentry_decision",
            "status": "pass"
            if contains_all(
                inputs["h53_readme_text"],
                [
                    "completed docs-only compiled-boundary reentry packet after landed negative",
                    "selected outcome:",
                    "`authorize_compiled_boundary_reentry_through_r58_first`",
                    "`keep_h52_terminal_and_stop_before_compiled_boundary`",
                    "authorize exactly `r58` as the next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h53_status_text"],
                [
                    "completed docs-only post-`h52` compiled-boundary reentry packet",
                    "preserves `h52` as the preserved prior docs-only closeout",
                    "selects `authorize_compiled_boundary_reentry_through_r58_first`",
                    "leaves `keep_h52_terminal_and_stop_before_compiled_boundary` non-selected",
                    "fixes `r58` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h53_todo_text"],
                [
                    "read landed `h52` explicitly rather than overwrite it by momentum",
                    "compiled-boundary question",
                    "keep transformed and trainable entry blocked here",
                    "fix `r58` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h53_acceptance_text"],
                [
                    "`h53` remains docs-only",
                    "exactly one decision outcome is selected",
                    "`h52` remains visible as the preserved prior docs-only closeout",
                    "`h43` remains visible as the paper-grade endpoint",
                    "`r58` becomes the only next runtime candidate",
                    "`f27`, `r53`, and `r54` remain blocked",
                ],
            )
            and contains_all(
                inputs["decision_matrix_text"],
                [
                    "| `authorize_compiled_boundary_reentry_through_r58_first` |",
                    "| `keep_h52_terminal_and_stop_before_compiled_boundary` |",
                    "set `r58` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h53_artifact_index_text"],
                [
                    "docs/milestones/h53_post_h52_compiled_boundary_reentry_packet/decision_matrix.md",
                    "docs/milestones/f29_post_h52_restricted_compiled_boundary_bundle/readme.md",
                    "docs/milestones/r58_origin_restricted_stack_bytecode_lowering_contract_gate/readme.md",
                    "results/h53_post_h52_compiled_boundary_reentry_packet/summary.json",
                ],
            )
            and contains_all(
                inputs["f29_readme_text"],
                [
                    "`h53_post_h52_compiled_boundary_reentry_packet` as the only follow-up packet",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate` as the only next runtime candidate",
                ],
            )
            else "blocked",
            "notes": "H53 should record one narrow docs-only decision: preserve H52, select reentry through R58, and keep executor-entry work blocked.",
        },
        {
            "item_id": "upstream_h52_negative_closeout_is_preserved_not_overturned",
            "status": "pass"
            if str(h52["selected_outcome"]) == "freeze_origin_mechanism_supported_without_fastpath_value"
            and str(h52["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            else "blocked",
            "notes": "H53 must preserve H52 as binding on fast-path value while preserving H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "shared_control_surfaces_record_h53_as_preserved_prior_reentry_packet",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "active docs-only packet:",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "preserved prior compiled-boundary reentry packet:",
                    "`h53_post_h52_compiled_boundary_reentry_packet`",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "`h53_post_h52_compiled_boundary_reentry_packet`",
                    "`r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the preserved prior compiled-boundary reentry packet is:",
                    "- `h53_post_h52_compiled_boundary_reentry_packet`",
                    "the completed lowering gate under the current compiled-boundary lane is:",
                    "- `r58_origin_restricted_stack_bytecode_lowering_contract_gate`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                    "`h53_post_h52_compiled_boundary_reentry_packet`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h53 |",
                    "preserve the prior mechanism closeout while explicitly authorizing a narrower compiled-boundary reentry through `r58` only",
                    "selects `authorize_compiled_boundary_reentry_through_r58_first`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h53_post_h52_compiled_boundary_reentry_packet` remains the preserved prior compiled-boundary reentry packet",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet` is now the current active",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h52` restricted compiled-boundary reentry wave",
                    "new `scripts/export_h53_post_h52_compiled_boundary_reentry_packet.py`",
                    "new `results/h53_post_h52_compiled_boundary_reentry_packet/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared current-wave docs should expose H53 as preserved prior authorization history inside the current H54 stack.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H53 preserves H52 as a negative fast-path closeout on the prior mechanism lane.",
            "H53 authorizes only a narrower compiled-boundary reentry through R58.",
            "H53 keeps transformed and trainable executor entry blocked while preserving H43 as the paper-grade endpoint.",
        ],
        "unsupported_here": [
            "H53 does not overturn H52 or restore an open broader runtime lane.",
            "H53 does not reactivate F27, R53, or R54.",
            "H53 does not claim compiled-boundary success before exact R58 and R59 evidence exists.",
        ],
        "disconfirmed_here": [
            "The idea that negative H52 should either permanently stop every narrower compiled-boundary question or automatically reopen broader executor-entry work.",
        ],
        "distilled_result": {
            "active_stage": "h53_post_h52_compiled_boundary_reentry_packet",
            "preserved_prior_docs_only_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_planning_bundle": "f29_post_h52_restricted_compiled_boundary_bundle",
            "selected_outcome": "authorize_compiled_boundary_reentry_through_r58_first",
            "non_selected_alternatives": [
                "keep_h52_terminal_and_stop_before_compiled_boundary",
            ],
            "current_low_priority_wave": "p38_post_h52_compiled_boundary_hygiene_sync",
            "only_next_runtime_candidate": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
            "only_conditional_later_sequence": [
                "r59_origin_compiled_trace_vm_execution_gate",
                "h54_post_r58_r59_compiled_boundary_decision_packet",
            ],
            "blocked_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "blocked_future_gates": [
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
            "next_required_lane": "r58_origin_restricted_stack_bytecode_lowering_contract_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/H53_post_h52_compiled_boundary_reentry_packet/README.md",
            inputs["h53_readme_text"],
            ["selected outcome:", "`authorize_compiled_boundary_reentry_through_r58_first`", "`R58`"],
        ),
        (
            "docs/milestones/H53_post_h52_compiled_boundary_reentry_packet/decision_matrix.md",
            inputs["decision_matrix_text"],
            ["| `authorize_compiled_boundary_reentry_through_r58_first` |", "set `R58` as the only next runtime candidate"],
        ),
        (
            "docs/milestones/H53_post_h52_compiled_boundary_reentry_packet/status.md",
            inputs["h53_status_text"],
            ["selects `authorize_compiled_boundary_reentry_through_r58_first`", "fixes `R58` as the only next runtime candidate"],
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["`H53_post_h52_compiled_boundary_reentry_packet`", "`R58_origin_restricted_stack_bytecode_lowering_contract_gate`"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`H53_post_h52_compiled_boundary_reentry_packet`", "`H54_post_r58_r59_compiled_boundary_decision_packet`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["The preserved prior compiled-boundary reentry packet is:", "- `H53_post_h52_compiled_boundary_reentry_packet`"],
        ),
        (
            "docs/claims_matrix.md",
            inputs["claims_matrix_text"],
            ["| H53 |", "selects `authorize_compiled_boundary_reentry_through_r58_first`"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`H53_post_h52_compiled_boundary_reentry_packet` remains the preserved prior compiled-boundary reentry packet", "`no_active_downstream_runtime_lane`"],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "preserved_prior_docs_only_closeout": distilled["preserved_prior_docs_only_closeout"],
        "current_active_routing_stage": distilled["current_active_routing_stage"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "current_planning_bundle": distilled["current_planning_bundle"],
        "selected_outcome": distilled["selected_outcome"],
        "non_selected_alternatives": distilled["non_selected_alternatives"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "only_next_runtime_candidate": distilled["only_next_runtime_candidate"],
        "only_conditional_later_sequence": distilled["only_conditional_later_sequence"],
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
