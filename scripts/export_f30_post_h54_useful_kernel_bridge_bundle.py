"""Export the post-H54 useful-kernel stop/go planning bundle for F30."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F30_post_h54_useful_kernel_bridge_bundle"


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
    milestone = ROOT / "docs" / "milestones" / "F30_post_h54_useful_kernel_bridge_bundle"
    return {
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-25-post-h54-useful-kernel-stopgo-design.md"),
        "plans_readme_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_readme_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "f30_readme_text": read_text(milestone / "README.md"),
        "f30_status_text": read_text(milestone / "status.md"),
        "f30_todo_text": read_text(milestone / "todo.md"),
        "f30_acceptance_text": read_text(milestone / "acceptance.md"),
        "f30_artifact_index_text": read_text(milestone / "artifact_index.md"),
        "route_constraints_text": read_text(milestone / "route_constraints.md"),
        "useful_kernel_question_text": read_text(milestone / "useful_kernel_question.md"),
        "origin_rationale_text": read_text(milestone / "origin_rationale.md"),
        "stopgo_criteria_text": read_text(milestone / "stopgo_criteria.md"),
        "h54_summary": read_json(ROOT / "results" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "summary.json"),
        "h52_summary": read_json(ROOT / "results" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h54 = inputs["h54_summary"]["summary"]
    h52 = inputs["h52_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "f30_docs_define_saved_post_h54_stopgo_bundle",
            "status": "pass"
            if contains_all(
                inputs["design_text"],
                [
                    "`f30_post_h54_useful_kernel_bridge_bundle`",
                    "`h55_post_h54_useful_kernel_reentry_packet`",
                    "`r60_origin_compiled_useful_kernel_carryover_gate`",
                    "`r61_origin_compiled_useful_kernel_value_gate`",
                    "`h56_post_r60_r61_useful_kernel_decision_packet`",
                    "`p39_post_h54_successor_worktree_hygiene_sync`",
                ],
            )
            and contains_all(
                inputs["f30_readme_text"],
                [
                    "saved successor planning bundle above the closed `h54` compiled-boundary wave",
                    "saved_successor_design_only",
                    "not active on the current branch",
                ],
            )
            and contains_all(
                inputs["f30_status_text"],
                [
                    "saved_successor_design_only",
                    "active: `false`",
                    "`h55_post_h54_useful_kernel_reentry_packet`",
                    "`r60 -> r61 -> h56`",
                ],
            )
            and contains_all(
                inputs["route_constraints_text"],
                [
                    "planning-only bundle",
                    "useful-kernel carryover only",
                    "no arbitrary `c`",
                    "no broad wasm reopen",
                    "no transformed or trainable entry",
                ],
            )
            and contains_all(
                inputs["useful_kernel_question_text"],
                [
                    "compiled-boundary route proven by `r58/r59`",
                    "minimal useful-kernel family",
                    "without compiler-side",
                    "without losing bounded value",
                ],
            )
            else "blocked",
            "notes": "F30 should exist only as saved successor planning storage fixing the H55->R60->R61->H56 order.",
        },
        {
            "item_id": "origin_rationale_and_stopgo_criteria_keep_scope_narrow",
            "status": "pass"
            if contains_all(
                inputs["origin_rationale_text"],
                [
                    "the headline \"llms are computers\" is broader than the publicly verifiable evidence",
                    "structured retrieval and a narrow exact executor",
                    "broad `c`, broad wasm, trainable entry, transformed entry",
                    "smallest meaningful falsifier",
                ],
            )
            and contains_all(
                inputs["stopgo_criteria_text"],
                [
                    "`r60` lands exact useful-kernel carryover",
                    "`r61` shows bounded value",
                    "the route should stop",
                    "toy compiled-boundary exactness only",
                ],
            )
            else "blocked",
            "notes": "F30 should preserve the conservative origin reading and define explicit stop/go interpretation before execution starts.",
        },
        {
            "item_id": "indices_record_f30_as_saved_successor_not_current_stage",
            "status": "pass"
            if str(h54["selected_outcome"]) == "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
            and str(h54["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h52["selected_outcome"]) == "freeze_origin_mechanism_supported_without_fastpath_value"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            and contains_all(
                inputs["plans_readme_text"],
                [
                    "`2026-03-25-post-h54-useful-kernel-stopgo-design.md`",
                    "saved successor design for the next explicit post-`h54` stop/go packet",
                ],
            )
            and contains_all(
                inputs["milestones_readme_text"],
                [
                    "`h54_post_r58_r59_compiled_boundary_decision_packet/`",
                    "`f30_post_h54_useful_kernel_bridge_bundle/`",
                    "saved successor planning-only bundle",
                    "saved successor docs-only reentry packet; not active",
                ],
            )
            else "blocked",
            "notes": "Shared planning indexes should record F30 as saved successor storage without replacing H54 as the active packet.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "F30 stores one narrow post-H54 stop/go bundle for minimal useful-kernel carryover.",
            "F30 fixes H55 as the only follow-up packet and R60 as the only next runtime candidate if activated later.",
            "F30 keeps R61 and H56 as the only later sequence while leaving F27, R53, and R54 blocked.",
        ],
        "unsupported_here": [
            "F30 does not replace H54 as the current active docs-only packet.",
            "F30 does not reopen arbitrary C, broad Wasm, transformed entry, or trainable entry.",
            "F30 does not itself execute a runtime lane or claim bounded value.",
        ],
        "disconfirmed_here": [
            "The idea that exact toy compiled-boundary evidence alone justifies broader compiled-execution claims without one minimal useful-kernel carryover test.",
        ],
        "distilled_result": {
            "active_stage": "f30_post_h54_useful_kernel_bridge_bundle",
            "current_active_docs_only_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "preserved_prior_docs_only_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_routing_refreeze_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "selected_outcome": "post_h54_useful_kernel_stopgo_bundle_saved",
            "only_followup_packet": "h55_post_h54_useful_kernel_reentry_packet",
            "only_next_runtime_candidate": "r60_origin_compiled_useful_kernel_carryover_gate",
            "only_conditional_later_sequence": [
                "r61_origin_compiled_useful_kernel_value_gate",
                "h56_post_r60_r61_useful_kernel_decision_packet",
            ],
            "saved_successor_low_priority_wave": "p39_post_h54_successor_worktree_hygiene_sync",
            "blocked_future_bundle": "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
            "blocked_future_gates": [
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
            "next_required_lane_if_activated": "r60_origin_compiled_useful_kernel_carryover_gate",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/plans/2026-03-25-post-h54-useful-kernel-stopgo-design.md",
            inputs["design_text"],
            ["`F30_post_h54_useful_kernel_bridge_bundle`", "`R60_origin_compiled_useful_kernel_carryover_gate`"],
        ),
        (
            "docs/milestones/F30_post_h54_useful_kernel_bridge_bundle/README.md",
            inputs["f30_readme_text"],
            ["saved successor planning bundle", "`saved_successor_design_only`"],
        ),
        (
            "docs/milestones/F30_post_h54_useful_kernel_bridge_bundle/origin_rationale.md",
            inputs["origin_rationale_text"],
            ["structured retrieval and a narrow exact executor", "smallest meaningful falsifier"],
        ),
        (
            "docs/milestones/F30_post_h54_useful_kernel_bridge_bundle/stopgo_criteria.md",
            inputs["stopgo_criteria_text"],
            ["`R60` lands exact useful-kernel carryover", "toy compiled-boundary exactness only"],
        ),
        (
            "docs/milestones/F30_post_h54_useful_kernel_bridge_bundle/route_constraints.md",
            inputs["route_constraints_text"],
            ["useful-kernel carryover only", "no transformed or trainable entry"],
        ),
        (
            "docs/plans/README.md",
            inputs["plans_readme_text"],
            ["`2026-03-25-post-h54-useful-kernel-stopgo-design.md`", "saved successor design"],
        ),
        (
            "docs/milestones/README.md",
            inputs["milestones_readme_text"],
            ["`F30_post_h54_useful_kernel_bridge_bundle/`", "saved successor planning-only bundle"],
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
        "saved_successor_low_priority_wave": distilled["saved_successor_low_priority_wave"],
        "blocked_future_bundle": distilled["blocked_future_bundle"],
        "blocked_future_gates": distilled["blocked_future_gates"],
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
