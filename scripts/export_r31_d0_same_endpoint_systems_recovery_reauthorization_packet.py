"""Export the post-H23 systems reauthorization packet for R31."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def load_inputs() -> dict[str, Any]:
    inputs: dict[str, Any] = {
        "r31_readme_text": read_text(ROOT / "docs" / "milestones" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "README.md"),
        "r31_status_text": read_text(ROOT / "docs" / "milestones" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "status.md"),
        "r31_todo_text": read_text(ROOT / "docs" / "milestones" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "todo.md"),
        "r31_acceptance_text": read_text(ROOT / "docs" / "milestones" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "acceptance.md"),
        "r31_artifact_index_text": read_text(ROOT / "docs" / "milestones" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "artifact_index.md"),
        "h23_summary_text": read_text(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json"),
        "r23_summary_text": read_text(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "summary.json"),
        "r28_summary_text": read_text(ROOT / "results" / "R28_d0_trace_retrieval_contract_audit" / "summary.json"),
        "r25_hypothesis_text": read_text(ROOT / "docs" / "milestones" / "R25_d0_same_endpoint_systems_recovery_hypotheses" / "hypothesis_matrix.md"),
        "r25_thresholds_text": read_text(ROOT / "docs" / "milestones" / "R25_d0_same_endpoint_systems_recovery_hypotheses" / "thresholds_and_disconfirmers.md"),
    }
    inputs["h23_summary"] = read_json(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json")
    inputs["r23_summary"] = read_json(ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "summary.json")
    inputs["r28_summary"] = read_json(ROOT / "results" / "R28_d0_trace_retrieval_contract_audit" / "summary.json")
    return inputs


def build_checklist_rows(
    *,
    r31_readme_text: str,
    r31_status_text: str,
    r31_todo_text: str,
    r31_acceptance_text: str,
    r31_artifact_index_text: str,
    h23_summary_text: str,
    h23_summary: dict[str, Any],
    r23_summary_text: str,
    r23_summary: dict[str, Any],
    r28_summary_text: str,
    r28_summary: dict[str, Any],
    r25_hypothesis_text: str,
    r25_thresholds_text: str,
) -> list[dict[str, object]]:
    h23 = h23_summary["summary"]
    r23 = r23_summary["summary"]["gate"]
    r28 = r28_summary["summary"]["gate"]
    return [
        {
            "item_id": "r31_docs_define_a_systems_decision_packet_not_a_recovery_run",
            "status": "pass"
            if contains_all(
                r31_readme_text,
                ["does not execute a same-endpoint systems recovery run", "mixed systems story", "non-retrieval overhead audit"],
            )
            and contains_all(
                r31_status_text,
                ["mechanism support distinct from systems competitiveness", "non-retrieval overhead audit", "`R29`"],
            )
            and contains_all(
                r31_todo_text,
                ["dominant bottleneck hypothesis", "comparator set", "`R29` stays blocked", "next lane"],
            )
            and contains_all(
                r31_acceptance_text,
                ["`hold_r29_blocked`", "`audit_non_retrieval_overhead_first`", "`execute_one_bounded_same_endpoint_recovery_probe`"],
            )
            and contains_all(
                r31_artifact_index_text,
                ["results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json", "R25_d0_same_endpoint_systems_recovery_hypotheses", "R33_d0_non_retrieval_overhead_localization_audit"],
            )
            else "blocked",
            "notes": "R31 should stay a decision packet rather than a hidden systems-recovery execution lane.",
        },
        {
            "item_id": "current_systems_state_remains_mixed_after_h23",
            "status": "pass"
            if h23["systems_verdict"] == "systems_still_mixed"
            and str(r23["lane_verdict"]) == "systems_still_mixed"
            and contains_all(
                h23_summary_text,
                ['"systems_verdict": "systems_still_mixed"', '"mechanism_contract_verdict": "mechanism_contract_supported_with_partial_control_isolation"'],
            )
            and contains_all(
                r23_summary_text,
                ['"lane_verdict": "systems_still_mixed"', '"pointer_like_median_ratio_vs_best_reference":'],
            )
            else "blocked",
            "notes": "R31 only exists because the same-endpoint systems story remains mixed even after the H23 refreeze.",
        },
        {
            "item_id": "r28_and_r25_point_to_a_non_retrieval_first_next_question",
            "status": "pass"
            if str(r28["retrieval_bottleneck_verdict"]) == "pointer_like_exact_non_retrieval_dominant"
            and contains_all(r28_summary_text, ['"retrieval_bottleneck_verdict": "pointer_like_exact_non_retrieval_dominant"'])
            and contains_all(
                r25_hypothesis_text,
                ["non_retrieval_overhead_dominates", "best_reference_comparator_gap_remains_the_blocker", "retrieval_mechanism_success_does_not_imply_systems_success"],
            )
            and contains_all(
                r25_thresholds_text,
                ["If a later candidate still shows `non_retrieval` overhead as the dominant component", "If a later candidate only looks better against imported `accelerated`", "If the lag remains suite-stable"],
            )
            else "blocked",
            "notes": "R31 should not authorize a retrieval-first recovery story when R28 and R25 already point elsewhere.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H23_refreeze_after_r26_r27_r28/summary.json",
            "fields": {
                "systems_verdict": inputs["h23_summary"]["summary"]["systems_verdict"],
                "mechanism_contract_verdict": inputs["h23_summary"]["summary"]["mechanism_contract_verdict"],
            },
        },
        {
            "source": "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json",
            "fields": {
                "systems_verdict": inputs["r23_summary"]["summary"]["gate"]["lane_verdict"],
                "best_reference_ratio_median": inputs["r23_summary"]["summary"]["gate"]["pointer_like_median_ratio_vs_best_reference"],
            },
        },
        {
            "source": "results/R28_d0_trace_retrieval_contract_audit/summary.json",
            "fields": {
                "retrieval_bottleneck_verdict": inputs["r28_summary"]["summary"]["gate"]["retrieval_bottleneck_verdict"],
                "mechanism_contract_verdict": inputs["r28_summary"]["summary"]["gate"]["mechanism_contract_verdict"],
            },
        },
        {
            "source": "docs/milestones/R25_d0_same_endpoint_systems_recovery_hypotheses/hypothesis_matrix.md",
            "planned_role": "dominant_bottleneck_hypotheses",
        },
        {
            "source": "docs/milestones/R25_d0_same_endpoint_systems_recovery_hypotheses/thresholds_and_disconfirmers.md",
            "planned_role": "kill_criteria_and_thresholds",
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_frozen_stage": "h23_refreeze_after_r26_r27_r28",
        "systems_reauthorization_verdict": "audit_non_retrieval_overhead_first",
        "dominant_bottleneck_hypothesis": "non_retrieval_overhead_dominates",
        "required_comparators": [
            "spec_reference",
            "lowered_exec_trace",
            "pointer_like_exact",
        ],
        "recovery_probe_scope": "current_positive_d0_suite_non_retrieval_component_localization",
        "recommended_next_lane": "r33_d0_non_retrieval_overhead_localization_audit",
        "blocked_future_lane": "r29_d0_same_endpoint_systems_recovery_execution_gate",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Keep R29 blocked and route the next justified systems work through a narrower non-retrieval overhead audit on the current positive D0 suite."
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "r31_systems_reauthorization_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "r31_systems_reauthorization_snapshot", "environment": environment.as_dict(), "rows": snapshot_rows},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r31_d0_same_endpoint_systems_recovery_reauthorization_packet",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/README.md",
                "docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/status.md",
                "docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/todo.md",
                "docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/acceptance.md",
                "docs/milestones/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/artifact_index.md",
                "results/H23_refreeze_after_r26_r27_r28/summary.json",
                "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json",
                "results/R28_d0_trace_retrieval_contract_audit/summary.json",
                "docs/milestones/R25_d0_same_endpoint_systems_recovery_hypotheses/hypothesis_matrix.md",
                "docs/milestones/R25_d0_same_endpoint_systems_recovery_hypotheses/thresholds_and_disconfirmers.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R31 D0 Same-Endpoint Systems Recovery Reauthorization Packet\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
