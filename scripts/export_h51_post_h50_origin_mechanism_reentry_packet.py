"""Export the post-H50 Origin mechanism reentry packet for H51."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H51_post_h50_origin_mechanism_reentry_packet"


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
        "h51_readme_text": read_text(
            ROOT / "docs" / "milestones" / "H51_post_h50_origin_mechanism_reentry_packet" / "README.md"
        ),
        "h51_status_text": read_text(
            ROOT / "docs" / "milestones" / "H51_post_h50_origin_mechanism_reentry_packet" / "status.md"
        ),
        "h51_todo_text": read_text(
            ROOT / "docs" / "milestones" / "H51_post_h50_origin_mechanism_reentry_packet" / "todo.md"
        ),
        "h51_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "H51_post_h50_origin_mechanism_reentry_packet" / "acceptance.md"
        ),
        "h51_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H51_post_h50_origin_mechanism_reentry_packet" / "artifact_index.md"
        ),
        "decision_matrix_text": read_text(
            ROOT / "docs" / "milestones" / "H51_post_h50_origin_mechanism_reentry_packet" / "decision_matrix.md"
        ),
        "f28_readme_text": read_text(
            ROOT / "docs" / "milestones" / "F28_post_h50_origin_mechanism_reentry_bundle" / "README.md"
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
            "item_id": "h51_docs_record_explicit_mechanism_reentry_decision",
            "status": "pass"
            if contains_all(
                inputs["h51_readme_text"],
                [
                    "completed docs-only mechanism reentry packet after landed negative `h50`",
                    "selected outcome:",
                    "`authorize_origin_mechanism_reentry_through_r55_first`",
                    "`keep_h50_stop_state_as_terminal`",
                    "`reactivate_f27_trainable_or_transformed_entry`",
                    "authorize exactly `r55` as the next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h51_status_text"],
                [
                    "completed docs-only post-`h50` mechanism reentry packet",
                    "preserves `h50` as the preserved prior docs-only closeout",
                    "selects `authorize_origin_mechanism_reentry_through_r55_first`",
                    "leaves `keep_h50_stop_state_as_terminal` non-selected",
                    "leaves `reactivate_f27_trainable_or_transformed_entry` non-selected",
                    "fixes `r55` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h51_todo_text"],
                [
                    "read landed `h50` explicitly rather than overwrite it by momentum",
                    "distinguish the broader post-`h49` bounded-value question from the narrower origin mechanism question",
                    "keep transformed and trainable entry blocked here",
                    "fix `r55` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h51_acceptance_text"],
                [
                    "`h51` remains docs-only",
                    "exactly one decision outcome is selected",
                    "`h50` remains visible as the preserved prior docs-only closeout",
                    "`h43` remains visible as the paper-grade endpoint",
                    "`r55` becomes the only next runtime candidate",
                    "`f27`, `r53`, and `r54` remain blocked",
                ],
            )
            and contains_all(
                inputs["decision_matrix_text"],
                [
                    "| `authorize_origin_mechanism_reentry_through_r55_first` |",
                    "| `keep_h50_stop_state_as_terminal` |",
                    "| `reactivate_f27_trainable_or_transformed_entry` |",
                    "set `r55` as the only next runtime candidate",
                ],
            )
            and contains_all(
                inputs["h51_artifact_index_text"],
                [
                    "docs/milestones/h51_post_h50_origin_mechanism_reentry_packet/decision_matrix.md",
                    "docs/milestones/f28_post_h50_origin_mechanism_reentry_bundle/readme.md",
                    "docs/milestones/r55_origin_2d_hardmax_retrieval_equivalence_gate/readme.md",
                    "results/h51_post_h50_origin_mechanism_reentry_packet/summary.json",
                ],
            )
            and contains_all(
                inputs["f28_readme_text"],
                [
                    "`h51_post_h50_origin_mechanism_reentry_packet` as the only follow-up packet",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate` as the only next runtime candidate",
                ],
            )
            else "blocked",
            "notes": "H51 should record one narrow docs-only decision: preserve H50, select reentry through R55, and keep executor-entry work blocked.",
        },
        {
            "item_id": "upstream_h50_negative_closeout_is_preserved_not_overturned",
            "status": "pass"
            if str(h50["active_stage"]) == "h50_post_r51_r52_scope_decision_packet"
            and str(h50["selected_outcome"]) == "stop_as_exact_without_system_value"
            and str(h50["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and str(h43["claim_ceiling"]) == "bounded_useful_cases_only"
            else "blocked",
            "notes": "H51 must preserve H50 as binding on the broader route while preserving H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "shared_control_surfaces_make_h51_current_active_packet",
            "status": "pass"
            if contains_all(
                inputs["readme_text"],
                [
                    "as of `2026-03-25`, the current active packet is",
                    "active docs-only packet:",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "preserved prior broader-route closeout:",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current active docs-only decision packet is",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "the preserved prior docs-only closeout is",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "the current downstream scientific lane after `h51` is",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current active stage is:",
                    "- `h51_post_h50_origin_mechanism_reentry_packet`",
                    "the preserved prior docs-only closeout is:",
                    "- `h50_post_r51_r52_scope_decision_packet`",
                    "the current downstream scientific lane after `h51` is:",
                    "- `r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                ],
            )
            and contains_all(
                inputs["claims_matrix_text"],
                [
                    "| h51 |",
                    "preserve the broader-route negative closeout while explicitly authorizing a narrower mechanism-first reentry through `r55` only",
                    "selects `authorize_origin_mechanism_reentry_through_r55_first`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`h51_post_h50_origin_mechanism_reentry_packet` is now the current active",
                    "selects",
                    "`r55` is the only next runtime candidate",
                    "`f27`, `r53`, and `r54` remain blocked",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h50` `f28/h51/p37` mechanism reentry wave",
                    "new `scripts/export_h51_post_h50_origin_mechanism_reentry_packet.py`",
                    "new `results/h51_post_h50_origin_mechanism_reentry_packet/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared current-wave docs should expose H51 as the active packet, H50 as preserved prior, and R55 as the only next lane.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "H51 preserves H50 as a negative bounded-value closeout on the broader post-H49 route.",
            "H51 authorizes only a narrower mechanism-first reentry through R55.",
            "H51 keeps transformed and trainable executor entry blocked while preserving H43 as the paper-grade endpoint.",
        ],
        "unsupported_here": [
            "H51 does not overturn H50 or restore an open broader-route runtime lane.",
            "H51 does not reactivate F27, R53, or R54.",
            "H51 does not claim mechanism success before exact R55, R56, and R57 evidence exists.",
        ],
        "disconfirmed_here": [
            "The idea that negative H50 should either permanently stop every narrower mechanism question or immediately reopen transformed or trainable executor entry.",
        ],
        "distilled_result": {
            "active_stage": "h51_post_h50_origin_mechanism_reentry_packet",
            "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
            "current_active_routing_stage": "h36_post_r40_bounded_scalar_family_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_planning_bundle": "f28_post_h50_origin_mechanism_reentry_bundle",
            "selected_outcome": "authorize_origin_mechanism_reentry_through_r55_first",
            "non_selected_alternatives": [
                "keep_h50_stop_state_as_terminal",
                "reactivate_f27_trainable_or_transformed_entry",
            ],
            "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
            "only_next_runtime_candidate": "r55_origin_2d_hardmax_retrieval_equivalence_gate",
            "only_conditional_later_sequence": [
                "r56_origin_append_only_trace_vm_semantics_gate",
                "r57_origin_accelerated_trace_vm_comparator_gate",
                "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            ],
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
            "docs/milestones/H51_post_h50_origin_mechanism_reentry_packet/README.md",
            inputs["h51_readme_text"],
            ["selected outcome:", "`authorize_origin_mechanism_reentry_through_r55_first`", "`R55`"],
        ),
        (
            "docs/milestones/H51_post_h50_origin_mechanism_reentry_packet/decision_matrix.md",
            inputs["decision_matrix_text"],
            ["| `authorize_origin_mechanism_reentry_through_r55_first` |", "set `R55` as the only next runtime candidate"],
        ),
        (
            "docs/milestones/H51_post_h50_origin_mechanism_reentry_packet/status.md",
            inputs["h51_status_text"],
            ["selects `authorize_origin_mechanism_reentry_through_r55_first`", "fixes `R55` as the only next runtime candidate"],
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["`H51_post_h50_origin_mechanism_reentry_packet`", "`R55_origin_2d_hardmax_retrieval_equivalence_gate`"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`H51_post_h50_origin_mechanism_reentry_packet`", "`H50_post_r51_r52_scope_decision_packet`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["The current active stage is:", "- `H51_post_h50_origin_mechanism_reentry_packet`"],
        ),
        (
            "docs/claims_matrix.md",
            inputs["claims_matrix_text"],
            ["| H51 |", "selects `authorize_origin_mechanism_reentry_through_r55_first`"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`H51_post_h50_origin_mechanism_reentry_packet` is now the current active", "`R55` is the only next runtime candidate"],
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
