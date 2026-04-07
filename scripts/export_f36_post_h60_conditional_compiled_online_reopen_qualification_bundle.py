"""Export the post-H60 compiled-online reopen qualification bundle for F36."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle"
H60_SUMMARY_PATH = ROOT / "results" / "H60_post_f34_next_lane_decision_packet" / "summary.json"
F34_SUMMARY_PATH = ROOT / "results" / "F34_post_h59_compiled_online_retrieval_reopen_screen" / "summary.json"
F35_SUMMARY_PATH = ROOT / "results" / "F35_post_h59_far_future_model_and_weights_horizon_log" / "summary.json"
ADMISSIBLE_REOPEN_FAMILY = "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"
USEFUL_CASE_TARGET = (
    "exact_useful_kernel_or_stricter_narrow_target_with_transparent_linear_and_external_baselines"
)
SELECTED_OUTCOME = "compiled_online_route_qualified_on_paper_only_with_strict_preruntime_gates"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    h60_summary = read_json(H60_SUMMARY_PATH)["summary"]
    f34_summary = read_json(F34_SUMMARY_PATH)["summary"]
    f35_summary = read_json(F35_SUMMARY_PATH)["summary"]
    if h60_summary["selected_outcome"] != "remain_planning_only_and_prepare_stop_or_archive":
        raise RuntimeError("F36 expects the landed H60 decision.")
    if f34_summary["admissible_reopen_family"] != ADMISSIBLE_REOPEN_FAMILY:
        raise RuntimeError("F36 expects the landed F34 admissible family.")
    if f35_summary["current_execution_candidate_count"] != 0:
        raise RuntimeError("F36 expects F35 to keep far-future routes inactive.")

    preregistered_questions = [
        "what exact useful-case target survives as the comparator",
        "what exact cost model differs materially from the closed executor-value lane",
        "what transparent linear and external baselines must be beaten",
        "what measured bounded-value win condition would count as success",
        "what immediate stop rules terminate the lane before runtime expansion",
    ]
    stop_rules = [
        "stop_if_route_is_just_renamed_same_lane_executor_value_work",
        "stop_if_useful_case_target_is_broader_than_preserved_narrow_endpoint",
        "stop_if_transparent_linear_and_external_baselines_are_missing",
        "stop_if_cost_structure_delta_is_not_materially_different",
        "stop_if_runtime_is_requested_without_later_explicit_authorization_packet",
    ]
    checklist_rows = [
        {
            "item_id": "f36_reads_h60",
            "status": "pass",
            "notes": "F36 begins only after H60 leaves the branch planning-only.",
        },
        {
            "item_id": "f36_preserves_f34_single_admissible_family",
            "status": "pass",
            "notes": "F36 keeps only the same admissible family that F34 allowed on paper.",
        },
        {
            "item_id": "f36_keeps_far_future_routes_separate",
            "status": "pass",
            "notes": "F35 far-future routes stay outside the active qualification bundle.",
        },
        {
            "item_id": "f36_fixates_useful_case_target",
            "status": "pass",
            "notes": "F36 requires an exact useful-kernel or stricter narrow target before any runtime work.",
        },
        {
            "item_id": "f36_requires_material_cost_structure_change",
            "status": "pass",
            "notes": "A renamed same-lane executor-value microvariant is not admissible.",
        },
        {
            "item_id": "f36_requires_declared_stop_rules",
            "status": "pass",
            "notes": "F36 makes stop conditions explicit before any future authorization.",
        },
        {
            "item_id": "f36_keeps_runtime_lane_closed",
            "status": "pass",
            "notes": "F36 is qualification-only and does not authorize runtime by itself.",
        },
    ]
    claim_packet = {
        "supports": [
            "F36 converts the one admissible compiled-online family into a qualification-only dossier with strict pre-runtime gates.",
            "F36 requires a concrete useful-case target, transparent baseline set, and material cost-model change before later authorization.",
            "F36 keeps same-lane executor-value microvariants, transformed entry, and trainable entry outside the admissible current route.",
        ],
        "does_not_support": [
            "runtime authorization",
            "renamed same-lane executor-value experimentation",
            "reopening F27, R53, or R54",
        ],
        "distilled_result": {
            "active_stage_at_bundle_time": "h60_post_f34_next_lane_decision_packet",
            "current_reopen_qualification_bundle": "f36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
            "preserved_prior_reopen_screen": "f34_post_h59_compiled_online_retrieval_reopen_screen",
            "admissible_reopen_family": ADMISSIBLE_REOPEN_FAMILY,
            "useful_case_target_contract": USEFUL_CASE_TARGET,
            "required_cost_structure_delta": "material_change_relative_to_closed_r62_h58_executor_value_lane",
            "mandatory_baseline_set": [
                "transparent_linear_internal_baseline",
                "external_simple_or_scalar_baseline",
                "current_exact_route_reference",
            ],
            "preruntime_question_count": len(preregistered_questions),
            "immediate_stop_rule_count": len(stop_rules),
            "later_authorization_gate": "no_runtime_lane_open_until_later_explicit_authorization",
            "selected_outcome": SELECTED_OUTCOME,
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "next_required_lane": "later_explicit_authorization_packet_or_archive_stop",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"question": question, "status": "must_answer_before_runtime"}
            for question in preregistered_questions
        ]
        + [
            {"stop_rule": rule, "status": "active"}
            for rule in stop_rules
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
