"""Export the post-H62 dormant R63 eligibility-profile dossier for F38."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F38_post_h62_r63_dormant_eligibility_profile_dossier"
H62_SUMMARY_PATH = ROOT / "results" / "H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet" / "summary.json"
F37_SUMMARY_PATH = ROOT / "results" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle" / "summary.json"
ELIGIBILITY_GAP_PATH = ROOT / "docs" / "milestones" / "F38_post_h62_r63_dormant_eligibility_profile_dossier" / "eligibility_gap.md"
NO_GO_RULE_PATH = ROOT / "docs" / "milestones" / "F38_post_h62_r63_dormant_eligibility_profile_dossier" / "no_go_rule.md"
CONDITIONAL_REOPEN_PROTOCOL_PATH = ROOT / "docs" / "publication_record" / "conditional_reopen_protocol.md"


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
    h62_summary = read_json(H62_SUMMARY_PATH)["summary"]
    f37_summary = read_json(F37_SUMMARY_PATH)["summary"]
    if h62_summary["default_downstream_lane"] != "archive_or_hygiene_stop":
        raise RuntimeError("F38 expects the landed H62 archive-default posture.")
    if f37_summary["runtime_authorization"] != "closed":
        raise RuntimeError("F38 expects F37 to keep runtime closed.")

    gap_text = ELIGIBILITY_GAP_PATH.read_text(encoding="utf-8")
    no_go_text = NO_GO_RULE_PATH.read_text(encoding="utf-8")
    protocol_text = CONDITIONAL_REOPEN_PROTOCOL_PATH.read_text(encoding="utf-8")

    exact_target_declared = f37_summary["narrow_target"] in gap_text
    comparator_declared = "honest comparator on the same lifted useful-kernel decode route: unresolved" not in gap_text
    cost_share_declared = "retrieval-head cost share: unresolved" not in gap_text
    query_insert_declared = "expected query:insert ratio: unresolved" not in gap_text
    tie_burden_declared = "tie frequency and tie-handling burden: unresolved" not in gap_text
    materially_different_cost_model_shown = "material cost-structure delta versus `R62/H58`: unresolved" not in gap_text
    dormant_wording_locked = all(
        pattern in no_go_text or pattern in protocol_text
        for pattern in ["R63", "dormant", "non-runtime"]
    )

    checklist_rows = [
        {
            "item_id": "f38_reads_h62",
            "status": "pass",
            "notes": "F38 inherits H62's archive-default downstream state.",
        },
        {
            "item_id": "f38_reads_f37",
            "status": "pass",
            "notes": "F38 inherits the single surviving F37 future family and runtime-closed posture.",
        },
        {
            "item_id": "f38_exact_target_declared",
            "status": "pass" if exact_target_declared else "blocked",
            "notes": "The exact lifted useful target must be named explicitly.",
        },
        {
            "item_id": "f38_comparator_declared",
            "status": "pass" if comparator_declared else "blocked",
            "notes": "The honest comparator remains unresolved and therefore not eligibility-ready.",
        },
        {
            "item_id": "f38_cost_share_declared",
            "status": "pass" if cost_share_declared else "blocked",
            "notes": "The retrieval-head cost share remains unresolved and therefore not eligibility-ready.",
        },
        {
            "item_id": "f38_query_insert_declared",
            "status": "pass" if query_insert_declared else "blocked",
            "notes": "The query:insert ratio remains unresolved and therefore not eligibility-ready.",
        },
        {
            "item_id": "f38_tie_burden_declared",
            "status": "pass" if tie_burden_declared else "blocked",
            "notes": "Tie frequency and tie-handling burden remain unresolved and therefore not eligibility-ready.",
        },
        {
            "item_id": "f38_material_cost_delta_shown",
            "status": "pass" if materially_different_cost_model_shown else "blocked",
            "notes": "A material cost-model delta versus R62/H58 is still unresolved.",
        },
        {
            "item_id": "f38_dormant_wording_locked",
            "status": "pass" if dormant_wording_locked else "blocked",
            "notes": "The dossier and reopen protocol must both keep R63 dormant and non-runtime only.",
        },
    ]
    claim_packet = {
        "supports": [
            "F38 preserves the only surviving future family as a dormant non-runtime dossier.",
            "F38 keeps the exact useful target explicit without pretending the missing cost-profile fields are known.",
            "F38 records an honest no-go rather than drifting back into renamed same-lane work.",
        ],
        "does_not_support": [
            "runtime authorization",
            "same-lane executor-value microvariants",
            "broad Wasm or arbitrary C widening",
        ],
        "distilled_result": {
            "active_stage_at_dossier_time": "h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
            "current_dormant_future_dossier": "f38_post_h62_r63_dormant_eligibility_profile_dossier",
            "preserved_prior_reauthorization_bundle": "f37_post_h61_compiled_online_coprocessor_reauthorization_bundle",
            "narrow_target": f37_summary["narrow_target"],
            "runtime_authorization": "closed",
            "exact_target_declared": exact_target_declared,
            "comparator_declared": comparator_declared,
            "cost_share_declared": cost_share_declared,
            "query_insert_declared": query_insert_declared,
            "tie_burden_declared": tie_burden_declared,
            "materially_different_cost_model_shown": materially_different_cost_model_shown,
            "selected_outcome": "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields",
            "next_required_lane": "archive_or_hygiene_stop_until_later_explicit_non_runtime_profile_reassessment",
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
            {"field": "exact_target_declared", "value": exact_target_declared},
            {"field": "comparator_declared", "value": comparator_declared},
            {"field": "cost_share_declared", "value": cost_share_declared},
            {"field": "query_insert_declared", "value": query_insert_declared},
            {"field": "tie_burden_declared", "value": tie_burden_declared},
            {"field": "materially_different_cost_model_shown", "value": materially_different_cost_model_shown},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
