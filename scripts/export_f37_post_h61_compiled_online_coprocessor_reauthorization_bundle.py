"""Export the post-H61 compiled-online coprocessor reauthorization bundle for F37."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle"
H61_SUMMARY_PATH = ROOT / "results" / "H61_post_h60_archive_first_position_packet" / "summary.json"
F36_SUMMARY_PATH = ROOT / "results" / "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle" / "summary.json"
P49_SUMMARY_PATH = ROOT / "results" / "P49_post_h61_origin_advisory_sync" / "summary.json"
BASELINE_CONTRACT_PATH = ROOT / "docs" / "milestones" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle" / "baseline_contract.md"
ELIGIBILITY_GATES_PATH = ROOT / "docs" / "milestones" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle" / "eligibility_gates.md"
STOP_RULES_PATH = ROOT / "docs" / "milestones" / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle" / "stop_rules.md"
SELECTED_ROUTE = "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"
NARROW_TARGET = "compiled_exact_hardmax_attention_coprocessor_on_lifted_useful_kernel_decode"


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


def count_bullets(path: Path) -> int:
    return sum(line.lstrip().startswith("- ") for line in path.read_text(encoding="utf-8").splitlines())


def main() -> None:
    h61_summary = read_json(H61_SUMMARY_PATH)["summary"]
    f36_summary = read_json(F36_SUMMARY_PATH)["summary"]
    p49_summary = read_json(P49_SUMMARY_PATH)["summary"]
    if h61_summary["selected_outcome"] != "archive_first_consolidation_becomes_default_posture":
        raise RuntimeError("F37 expects the landed H61 packet.")
    if f36_summary["admissible_reopen_family"] != SELECTED_ROUTE:
        raise RuntimeError("F37 expects the one surviving route family from F36.")
    if p49_summary["selected_outcome"] != "advisory_origin_materials_available_in_clean_line":
        raise RuntimeError("F37 expects the landed P49 advisory sync wave.")

    baseline_count = count_bullets(BASELINE_CONTRACT_PATH)
    eligibility_gate_count = count_bullets(ELIGIBILITY_GATES_PATH)
    stop_rule_count = count_bullets(STOP_RULES_PATH)

    checklist_rows = [
        {
            "item_id": "f37_reads_h61",
            "status": "pass",
            "notes": "F37 begins only after H61 locks the archive-first posture.",
        },
        {
            "item_id": "f37_reads_f36",
            "status": "pass",
            "notes": "F37 narrows the one surviving F36 route rather than inventing a new family.",
        },
        {
            "item_id": "f37_reads_p49",
            "status": "pass",
            "notes": "F37 uses advisory material only after it is available in the clean line.",
        },
        {
            "item_id": "f37_baseline_contract_count",
            "status": "pass" if baseline_count == 3 else "blocked",
            "notes": "F37 requires exactly three honest baselines.",
        },
        {
            "item_id": "f37_eligibility_gate_count",
            "status": "pass" if eligibility_gate_count == 5 else "blocked",
            "notes": "F37 requires five preruntime eligibility questions.",
        },
        {
            "item_id": "f37_stop_rule_count",
            "status": "pass" if stop_rule_count == 7 else "blocked",
            "notes": "F37 requires seven immediate stop rules.",
        },
        {
            "item_id": "f37_runtime_stays_closed",
            "status": "pass",
            "notes": "F37 does not authorize runtime; it only prepares a later profile gate.",
        },
    ]
    claim_packet = {
        "supports": [
            "F37 keeps exactly one scientific route alive and narrows it to a compiled exact hard-max coprocessor target.",
            "F37 fixes honest baselines and hard stop rules before any later runtime-like profile gate.",
            "F37 reframes the future question away from same-lane executor-value revival.",
        ],
        "does_not_support": [
            "same-lane executor-value microvariants",
            "broad Wasm or arbitrary C reopening",
            "runtime authorization from this bundle alone",
        ],
        "distilled_result": {
            "active_stage_at_bundle_time": "h61_post_h60_archive_first_position_packet",
            "current_reauthorization_bundle": "f37_post_h61_compiled_online_coprocessor_reauthorization_bundle",
            "preserved_prior_reauthorization_bundle": "f36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
            "current_origin_advisory_sync_wave": "p49_post_h61_origin_advisory_sync",
            "selected_candidate_route": SELECTED_ROUTE,
            "narrow_target": NARROW_TARGET,
            "baseline_set": [
                "compiled_linear_scan_exact_hardmax_baseline",
                "current_exact_route_reference",
                "external_simple_or_scalar_baseline",
            ],
            "eligibility_gate_count": eligibility_gate_count,
            "stop_rule_count": stop_rule_count,
            "runtime_authorization": "closed",
            "selected_outcome": "one_compiled_online_coprocessor_route_specified_but_runtime_closed",
            "next_required_lane": "h62_scope_decision_or_later_r63_eligibility_profile",
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
            {"field": "selected_candidate_route", "value": SELECTED_ROUTE},
            {"field": "narrow_target", "value": NARROW_TARGET},
            {"field": "baseline_count", "value": baseline_count},
            {"field": "eligibility_gate_count", "value": eligibility_gate_count},
            {"field": "stop_rule_count", "value": stop_rule_count},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
