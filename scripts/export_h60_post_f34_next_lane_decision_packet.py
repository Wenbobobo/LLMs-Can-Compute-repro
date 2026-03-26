"""Export the post-F34 next-lane decision packet for H60."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H60_post_f34_next_lane_decision_packet"
H59_SUMMARY_PATH = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet" / "summary.json"
F34_SUMMARY_PATH = ROOT / "results" / "F34_post_h59_compiled_online_retrieval_reopen_screen" / "summary.json"
P43_SUMMARY_PATH = ROOT / "results" / "P43_post_h59_repo_graph_hygiene_and_merge_map" / "summary.json"
F35_SUMMARY_PATH = ROOT / "results" / "F35_post_h59_far_future_model_and_weights_horizon_log" / "summary.json"
SELECTED_OUTCOME = "remain_planning_only_and_prepare_stop_or_archive"


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
    f34_summary = read_json(F34_SUMMARY_PATH)["summary"]
    p43_summary = read_json(P43_SUMMARY_PATH)["summary"]
    f35_summary = read_json(F35_SUMMARY_PATH)["summary"]
    if h59_summary["selected_outcome"] != "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen":
        raise RuntimeError("H60 expects the landed H59 packet.")
    if f34_summary["admissible_reopen_family"] != "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route":
        raise RuntimeError("H60 expects the landed F34 reopen screen.")
    if p43_summary["merge_posture"] != "clean_descendant_only_never_dirty_root_main":
        raise RuntimeError("H60 expects the landed P43 merge posture.")
    if f35_summary["current_execution_candidate_count"] != 0:
        raise RuntimeError("H60 expects F35 to remain far-future-only storage.")

    checklist_rows = [
        {
            "item_id": "h60_preserves_h59",
            "status": "pass",
            "notes": "H59 stays the preserved prior reproduction-gap packet.",
        },
        {
            "item_id": "h60_reads_f34_conditional_family",
            "status": "pass",
            "notes": "H60 keeps only the F34 conditional compiled-online family on record.",
        },
        {
            "item_id": "h60_reads_p43_merge_posture",
            "status": "pass",
            "notes": "Dirty root main remains quarantined; merge posture stays descendant-only.",
        },
        {
            "item_id": "h60_reads_f35_far_future_storage",
            "status": "pass",
            "notes": "Far-future model and weights routes remain stored but inactive.",
        },
        {
            "item_id": "h60_keeps_runtime_lane_closed",
            "status": "pass",
            "notes": "The selected outcome is still planning-only, archive, or stop.",
        },
    ]
    claim_packet = {
        "supports": [
            "H60 makes planning-only / archive / stop the live repo posture after the post-H59 reopen screen.",
            "H60 preserves H59 as the prior reproduction-gap packet rather than erasing it.",
            "H60 keeps only one conditionally credible future family on record and stores farther-future ideas separately.",
        ],
        "does_not_support": [
            "an open runtime lane",
            "same-lane executor-value reopening",
            "treating far-future model or weights routes as current candidates",
        ],
        "distilled_result": {
            "active_stage": "h60_post_f34_next_lane_decision_packet",
            "preserved_prior_active_packet": "h59_post_h58_reproduction_gap_decision_packet",
            "preserved_prior_docs_only_closeout": "h58_post_r62_origin_value_boundary_closeout_packet",
            "preserved_prior_closeout_certification": "f32_post_h58_closeout_certification_bundle",
            "current_planning_bundle": "f34_post_h59_compiled_online_retrieval_reopen_screen",
            "current_repo_hygiene_sidecar": "p43_post_h59_repo_graph_hygiene_and_merge_map",
            "current_low_priority_publication_wave": "p44_post_h59_publication_surface_and_claim_lock",
            "current_far_future_horizon_log": "f35_post_h59_far_future_model_and_weights_horizon_log",
            "preserved_prior_publication_sync": "p41_post_h58_publication_and_archive_sync",
            "preserved_prior_dossier_sidecar": "p42_post_h59_gptpro_reinterview_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "selected_outcome": SELECTED_OUTCOME,
            "conditionally_credible_future_reopen_family": f34_summary["admissible_reopen_family"],
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
            "later_authorization_gate": "no_runtime_lane_open_until_later_explicit_authorization",
            "merge_posture": p43_summary["merge_posture"],
            "blocked_future_storage": [
                "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle",
                "r53_origin_transformed_executor_entry_gate",
                "r54_origin_trainable_executor_comparator_gate",
            ],
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
            {"source": "h59", "selected_outcome": h59_summary["selected_outcome"]},
            {"source": "f34", "admissible_reopen_family": f34_summary["admissible_reopen_family"]},
            {"source": "p43", "merge_posture": p43_summary["merge_posture"]},
            {"source": "f35", "current_execution_candidate_count": f35_summary["current_execution_candidate_count"]},
            {"source": "h60", "selected_outcome": SELECTED_OUTCOME},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
