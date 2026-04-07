"""Export the post-H50 Origin mechanism reentry bundle for F28."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F28_post_h50_origin_mechanism_reentry_bundle"


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
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-25-post-h50-origin-mechanism-reentry-master-plan.md"),
        "f28_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "README.md"
        ),
        "f28_status_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "status.md"
        ),
        "f28_todo_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "todo.md"
        ),
        "f28_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "acceptance.md"
        ),
        "f28_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "artifact_index.md"
        ),
        "mechanism_claim_delta_matrix_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "F28_post_h50_origin_mechanism_reentry_bundle"
            / "mechanism_claim_delta_matrix.md"
        ),
        "reentry_question_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "reentry_question.md"
        ),
        "route_constraints_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "route_constraints.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "claims_matrix_text": read_text(ROOT / "docs" / "claims_matrix.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h50_summary": read_json(ROOT / "results" / "H50_post_r51_r52_scope_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h50 = inputs["h50_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "f28_docs_define_post_h50_mechanism_reentry_bundle",
            "status": "pass"
            if contains_all(
                inputs["design_text"],
                [
                    "`f28_post_h50_origin_mechanism_reentry_bundle`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                    "`r56_origin_append_only_trace_vm_semantics_gate`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                ],
            )
            and contains_all(
                inputs["f28_readme_text"],
                [
                    "mechanism-first reentry",
                    "`h50`",
                    "`h43`",
                    "`h36`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                ],
            )
            and contains_all(
                inputs["f28_status_text"],
                [
                    "completed planning-only post-`h50` mechanism reentry bundle",
                    "fixes `h51` as the only follow-up packet",
                    "fixes `r55` as the only next runtime candidate",
                    "keeps `f27`, `r53`, and `r54` blocked",
                ],
            )
            and contains_all(
                inputs["f28_todo_text"],
                [
                    "define one mechanism claim-delta matrix",
                    "define one reentry question",
                    "define one route-constraints note",
                    "keep `r55` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["f28_acceptance_text"],
                [
                    "the bundle remains planning-only",
                    "`h50` remains the preserved prior docs-only packet",
                    "`h43` remains the current paper-grade endpoint",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate` is the only next runtime candidate fixed here",
                ],
            )
            and contains_all(
                inputs["mechanism_claim_delta_matrix_text"],
                [
                    "| `a` |",
                    "| `b` |",
                    "| `c` |",
                    "| `d` |",
                    "isolate this first in `r55`",
                    "defer value judgment to `r57`, then close explicitly in `h52`",
                ],
            )
            and contains_all(
                inputs["reentry_question_text"],
                [
                    "the next justified question is therefore not transformed-model entry",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                    "`r56_origin_append_only_trace_vm_semantics_gate`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                ],
            )
            and contains_all(
                inputs["route_constraints_text"],
                [
                    "`h51` is the only follow-up packet fixed here",
                    "`r55` is the only next runtime candidate fixed here",
                    "`r56` can run only after positive exact `r55`",
                    "`r57` can run only after positive exact `r56`",
                    "`h52` is the only closeout packet fixed for this mechanism lane",
                    "`f27` remains saved as planning-only",
                    "`r53` and `r54` remain saved future gates only",
                ],
            )
            and contains_all(
                inputs["f28_artifact_index_text"],
                [
                    "docs/milestones/f28_post_h50_origin_mechanism_reentry_bundle/mechanism_claim_delta_matrix.md",
                    "docs/milestones/f28_post_h50_origin_mechanism_reentry_bundle/reentry_question.md",
                    "docs/milestones/f28_post_h50_origin_mechanism_reentry_bundle/route_constraints.md",
                    "results/f28_post_h50_origin_mechanism_reentry_bundle/summary.json",
                ],
            )
            else "blocked",
            "notes": "F28 should save one planning-only mechanism reentry bundle and fix only the narrow H51->R55->R56->R57->H52 lane.",
        },
        {
            "item_id": "upstream_h50_and_h43_support_f28_reframing_without_overturning_h50",
            "status": "pass"
            if str(h50["active_stage"]) == "h50_post_r51_r52_scope_decision_packet"
            and str(h50["selected_outcome"]) == "stop_as_exact_without_system_value"
            and str(h50["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h50["current_paper_grade_endpoint"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and bool(h43["merge_executed"]) is False
            else "blocked",
            "notes": "F28 must preserve H50 as a negative broader-route closeout while keeping H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "shared_control_surfaces_make_f28_current_planning_bundle",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "active docs-only packet:",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "current planning bundle:",
                    "`f28_post_h50_origin_mechanism_reentry_bundle`",
                    "current low-priority operational/docs wave:",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current active docs-only decision packet is",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "the current planning bundle is",
                    "`f28_post_h50_origin_mechanism_reentry_bundle`",
                    "the current low-priority operational/docs wave is",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current planning bundle is:",
                    "- `f28_post_h50_origin_mechanism_reentry_bundle`",
                    "the current downstream scientific lane after `h51` is:",
                    "- `r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| f28 |",
                    "the post-`h50` origin-core line can reopen only through one planning-only mechanism reentry bundle",
                    "fixes `r55 -> r56 -> r57 -> h52` as the only admissible sequence",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`f28_post_h50_origin_mechanism_reentry_bundle` is now the current planning bundle",
                    "`h51_post_h50_origin_mechanism_reentry_packet` is now the current active",
                    "`p37_post_h50_narrow_executor_closeout_sync` is now the current low-priority",
                    "`r55` is the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h50` `f28/h51/p37` mechanism reentry wave",
                    "new `scripts/export_f28_post_h50_origin_mechanism_reentry_bundle.py`",
                    "new `results/f28_post_h50_origin_mechanism_reentry_bundle/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared current-wave surfaces should expose F28 as the planning bundle under active H51 and next-lane R55.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F28 preserves negative H50 while reopening only a narrower mechanism-first reading of the Origin materials.",
            "F28 fixes H51 as the only follow-up packet and R55 as the only next runtime candidate.",
            "F28 keeps R56, R57, and H52 as the only conditional downstream sequence and leaves F27, R53, and R54 blocked.",
        ],
        "unsupported_here": [
            "F28 does not overturn H50 or reactivate transformed or trainable executor entry.",
            "F28 does not authorize arbitrary C, broad Wasm, or general 'LLMs are computers' wording.",
            "F28 does not itself execute a runtime lane or claim fast-path value.",
        ],
        "disconfirmed_here": [
            "The idea that negative H50 should automatically reopen executor-entry work or broader claims by momentum.",
        ],
        "distilled_result": {
            "active_stage": "f28_post_h50_origin_mechanism_reentry_bundle",
            "current_active_docs_only_stage": "h51_post_h50_origin_mechanism_reentry_packet",
            "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_routing_refreeze_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "selected_outcome": "post_h50_mechanism_reentry_bundle_saved",
            "only_followup_packet": "h51_post_h50_origin_mechanism_reentry_packet",
            "only_next_runtime_candidate": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
            "only_conditional_later_sequence": [
                "r56_origin_append_only_trace_vm_semantics_gate",
                "r57_origin_accelerated_trace_vm_comparator_gate",
                "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            ],
            "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
            "blocked_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "blocked_future_gates": [
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
            "next_required_lane": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/plans/2026-03-25-post-h50-origin-mechanism-reentry-master-plan.md",
            inputs["design_text"],
            ["mechanism-first lane", "`r55`", "`r56`", "`r57`", "`h52`"],
        ),
        (
            "docs/milestones/F28_post_h50_origin_mechanism_reentry_bundle/mechanism_claim_delta_matrix.md",
            inputs["mechanism_claim_delta_matrix_text"],
            ["| `A` |", "| `D` |", "`R55`", "`R57`", "`H52`"],
        ),
        (
            "docs/milestones/F28_post_h50_origin_mechanism_reentry_bundle/reentry_question.md",
            inputs["reentry_question_text"],
            ["the selected question is:", "`H51_post_h50_origin_mechanism_reentry_packet`", "`R55_origin_2d_hardmax_retrieval_equivalence_gate`"],
        ),
        (
            "docs/milestones/F28_post_h50_origin_mechanism_reentry_bundle/route_constraints.md",
            inputs["route_constraints_text"],
            ["`H51` is the only follow-up packet fixed here", "`R55` is the only next runtime candidate fixed here"],
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["The current planning bundle is `F28_post_h50_origin_mechanism_reentry_bundle`", "`R55_origin_2d_hardmax_retrieval_equivalence_gate`"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`F28_post_h50_origin_mechanism_reentry_bundle`", "`R55_origin_2d_hardmax_retrieval_equivalence_gate`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["The current planning bundle is:", "- `F28_post_h50_origin_mechanism_reentry_bundle`"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`F28_post_h50_origin_mechanism_reentry_bundle` is now the current planning bundle", "`R55` is the only next runtime candidate"],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    return {
        "active_stage": distilled["active_stage"],
        "current_active_docs_only_stage": distilled["current_active_docs_only_stage"],
        "preserved_prior_docs_only_closeout": distilled["preserved_prior_docs_only_closeout"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "current_routing_refreeze_stage": distilled["current_routing_refreeze_stage"],
        "selected_outcome": distilled["selected_outcome"],
        "only_followup_packet": distilled["only_followup_packet"],
        "only_next_runtime_candidate": distilled["only_next_runtime_candidate"],
        "only_conditional_later_sequence": distilled["only_conditional_later_sequence"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
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
