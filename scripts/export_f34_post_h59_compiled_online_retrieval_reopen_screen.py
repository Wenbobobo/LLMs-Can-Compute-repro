"""Export the post-H59 compiled/online retrieval reopen screen for F34."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F34_post_h59_compiled_online_retrieval_reopen_screen"
H59_SUMMARY_PATH = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet" / "summary.json"
F33_SUMMARY_PATH = ROOT / "results" / "F33_post_h59_different_cost_structure_reopen_bundle" / "summary.json"
P42_SUMMARY_PATH = ROOT / "results" / "P42_post_h59_gptpro_reinterview_packet" / "summary.json"
ADMISSIBLE_REOPEN_FAMILY = "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"
SELECTED_OUTCOME = (
    "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route_"
    "screened_without_runtime_authorization"
)
NON_ADMISSIBLE_NEAR_TERM = [
    "same_lane_executor_value_microvariants_not_admissible",
    "high_cost_model_route_far_future_only",
    "programs_into_weights_route_far_future_only",
]


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
    h59_summary = read_json(H59_SUMMARY_PATH)["summary"]
    f33_summary = read_json(F33_SUMMARY_PATH)["summary"]
    p42_summary = read_json(P42_SUMMARY_PATH)["summary"]
    if h59_summary["selected_outcome"] != "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen":
        raise RuntimeError("F34 expects the landed H59 reproduction-gap packet.")
    if f33_summary["admissible_reopen_requirement"] != "materially_different_cost_structure":
        raise RuntimeError("F34 expects F33 to preserve the different-cost-structure rule.")
    if p42_summary["selected_outcome"] != "self_contained_gptpro_dossier_ready":
        raise RuntimeError("F34 expects the landed P42 dossier packet.")

    checklist_rows = [
        {
            "item_id": "f34_starts_after_h59",
            "status": "pass",
            "notes": "F34 begins only after H59 makes the reproduction gap explicit.",
        },
        {
            "item_id": "f34_preserves_f33_cost_structure_rule",
            "status": "pass",
            "notes": "The admissible family must still change the cost structure materially.",
        },
        {
            "item_id": "f34_uses_p42_as_advisory_input_only",
            "status": "pass",
            "notes": "The GPTPro dossier remains advisory and does not become evidence.",
        },
        {
            "item_id": "f34_names_only_one_conditional_reopen_family",
            "status": "pass",
            "notes": "Only the compiled-online exact-retrieval / attention-coprocessor family stays conditionally credible.",
        },
        {
            "item_id": "f34_keeps_runtime_lane_closed",
            "status": "pass",
            "notes": "No runtime lane opens until later explicit authorization.",
        },
        {
            "item_id": "f34_excludes_far_future_model_and_weights_routes",
            "status": "pass",
            "notes": "High-cost model and programs-into-weights routes are not current candidates.",
        },
    ]
    claim_packet = {
        "supports": [
            "F34 keeps the current branch in planning-only mode while naming one conditionally credible future reopen family.",
            "That family is a materially different compiled/online exact-retrieval primitive or attention-coprocessor route.",
            "Same-lane executor-value microvariants remain inadmissible after H58/F32/H59.",
        ],
        "does_not_support": [
            "runtime authorization",
            "automatic reopening of the same lane",
            "promoting model-route or weights-route ideas into current candidates",
        ],
        "distilled_result": {
            "active_stage_at_screen_time": "h59_post_h58_reproduction_gap_decision_packet",
            "planning_bundle": "f34_post_h59_compiled_online_retrieval_reopen_screen",
            "preserved_prior_planning_bundle": "f33_post_h59_different_cost_structure_reopen_bundle",
            "current_low_priority_wave": "p42_post_h59_gptpro_reinterview_packet",
            "admissible_reopen_family": ADMISSIBLE_REOPEN_FAMILY,
            "same_lane_status": "same_lane_executor_value_microvariants_not_admissible",
            "later_authorization_gate": "no_runtime_lane_open_until_later_explicit_authorization",
            "selected_outcome": SELECTED_OUTCOME,
            "non_admissible_near_term_routes": NON_ADMISSIBLE_NEAR_TERM,
            "required_baseline_contract": "exact_useful_case_or_stronger_narrow_target_with_transparent_linear_and_external_baselines",
            "project_default_fallback": "planning_only_or_project_stop",
            "next_required_lane": "docs_only_decision_or_stop_archive",
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
            {"route_family": "same_lane_executor_value_microvariants", "status": "inadmissible"},
            {"route_family": ADMISSIBLE_REOPEN_FAMILY, "status": "conditional_only"},
            {"route_family": "high_cost_model_route", "status": "far_future_only"},
            {"route_family": "programs_into_weights_route", "status": "far_future_only"},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
