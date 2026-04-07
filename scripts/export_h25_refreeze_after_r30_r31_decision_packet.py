"""Export the post-R30/R31 decision refreeze summary for H25."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H25_refreeze_after_r30_r31_decision_packet"


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
        "h25_readme_text": read_text(ROOT / "docs" / "milestones" / "H25_refreeze_after_r30_r31_decision_packet" / "README.md"),
        "h25_status_text": read_text(ROOT / "docs" / "milestones" / "H25_refreeze_after_r30_r31_decision_packet" / "status.md"),
        "h25_todo_text": read_text(ROOT / "docs" / "milestones" / "H25_refreeze_after_r30_r31_decision_packet" / "todo.md"),
        "h25_acceptance_text": read_text(ROOT / "docs" / "milestones" / "H25_refreeze_after_r30_r31_decision_packet" / "acceptance.md"),
        "h25_artifact_index_text": read_text(ROOT / "docs" / "milestones" / "H25_refreeze_after_r30_r31_decision_packet" / "artifact_index.md"),
        "h25_result_digest_text": read_text(ROOT / "docs" / "milestones" / "H25_refreeze_after_r30_r31_decision_packet" / "result_digest.md"),
        "h23_summary_text": read_text(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json"),
        "r30_summary_text": read_text(ROOT / "results" / "R30_d0_boundary_reauthorization_packet" / "summary.json"),
        "r31_summary_text": read_text(ROOT / "results" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "summary.json"),
    }
    inputs["h23_summary"] = read_json(ROOT / "results" / "H23_refreeze_after_r26_r27_r28" / "summary.json")
    inputs["r30_summary"] = read_json(ROOT / "results" / "R30_d0_boundary_reauthorization_packet" / "summary.json")
    inputs["r31_summary"] = read_json(ROOT / "results" / "R31_d0_same_endpoint_systems_recovery_reauthorization_packet" / "summary.json")
    return inputs


def build_checklist_rows(
    *,
    h25_readme_text: str,
    h25_status_text: str,
    h25_todo_text: str,
    h25_acceptance_text: str,
    h25_artifact_index_text: str,
    h25_result_digest_text: str,
    h23_summary_text: str,
    h23_summary: dict[str, Any],
    r30_summary_text: str,
    r30_summary: dict[str, Any],
    r31_summary_text: str,
    r31_summary: dict[str, Any],
) -> list[dict[str, object]]:
    h23 = h23_summary["summary"]
    r30 = r30_summary["summary"]
    r31 = r31_summary["summary"]
    return [
        {
            "item_id": "h25_docs_preserve_h23_while_freezing_the_decision_packet",
            "status": "pass"
            if contains_all(
                h25_readme_text,
                ["does not replace `H23` as the frozen scientific evidence state", "`R29` and `F3`", "one primary next science lane and one deferred audit lane"],
            )
            and contains_all(
                h25_status_text,
                ["`H23` remains the current frozen scientific state", "`R32`", "`R33`", "`R29` and `F3` remain blocked"],
            )
            and contains_all(
                h25_todo_text,
                ["`R30` and `R31`", "`supported_here`, `unsupported_here`, and `disconfirmed_here`", "`R29` or `F3`"],
            )
            and contains_all(
                h25_acceptance_text,
                ["machine-readable post-`H23` decision packet", "`H23` remains the frozen scientific state", "`next_priority_lane`"],
            )
            and contains_all(
                h25_result_digest_text,
                ["boundary reauthorization verdict", "systems reauthorization verdict", "`H23` remains the frozen scientific state"],
            )
            else "blocked",
            "notes": "H25 should freeze the decision packet without rewriting the current scientific state.",
        },
        {
            "item_id": "r30_and_r31_feed_one_primary_and_one_deferred_lane",
            "status": "pass"
            if str(r30["boundary_reauthorization_verdict"]) == "execute_one_more_family_local_zoom"
            and str(r31["systems_reauthorization_verdict"]) == "audit_non_retrieval_overhead_first"
            and str(r30["recommended_next_lane"]) == "r32_d0_family_local_boundary_sharp_zoom"
            and str(r31["recommended_next_lane"]) == "r33_d0_non_retrieval_overhead_localization_audit"
            and contains_all(r30_summary_text, ['"boundary_reauthorization_verdict": "execute_one_more_family_local_zoom"'])
            and contains_all(r31_summary_text, ['"systems_reauthorization_verdict": "audit_non_retrieval_overhead_first"'])
            else "blocked",
            "notes": "H25 should turn R30 and R31 into one explicit primary/deferred routing decision.",
        },
        {
            "item_id": "h23_claim_limits_stay_explicit_under_h25",
            "status": "pass"
            if h23["boundary_verdict"] == "bounded_grid_still_not_localized"
            and h23["systems_verdict"] == "systems_still_mixed"
            and contains_all(
                h23_summary_text,
                ['"boundary_verdict": "bounded_grid_still_not_localized"', '"systems_verdict": "systems_still_mixed"', '"next_priority_lane": "p14_public_surface_sync_after_h23"'],
            )
            and contains_all(
                h25_artifact_index_text,
                ["results/H25_refreeze_after_r30_r31_decision_packet/summary.json", "R32_d0_family_local_boundary_sharp_zoom", "R33_d0_non_retrieval_overhead_localization_audit"],
            )
            else "blocked",
            "notes": "H25 should preserve the H23 claim limits while freezing the next-lane decision.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    supported_here = [
        "H23 remains the current frozen scientific state after the bounded post-H21 reopen/refreeze packet.",
        "R30 authorizes one future bounded family-local boundary sharp zoom instead of another full-grid expansion.",
        "R31 routes any later same-endpoint systems recovery discussion through a narrower non-retrieval overhead audit first.",
    ]
    unsupported_here = [
        "H25 does not upgrade the H23 systems verdict from mixed to positive.",
        "H25 does not authorize direct R29 execution or broader scope lift.",
        "H25 does not widen beyond the fixed tiny typed-bytecode D0 endpoint.",
    ]
    disconfirmed_here = [
        "The narrower expectation that another retrieval-first same-endpoint recovery probe is already the best next systems move.",
    ]
    return {
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "source": "results/H23_refreeze_after_r26_r27_r28/summary.json",
            "fields": {
                "boundary_verdict": inputs["h23_summary"]["summary"]["boundary_verdict"],
                "systems_verdict": inputs["h23_summary"]["summary"]["systems_verdict"],
            },
        },
        {
            "source": "results/R30_d0_boundary_reauthorization_packet/summary.json",
            "fields": {
                "boundary_reauthorization_verdict": inputs["r30_summary"]["summary"]["boundary_reauthorization_verdict"],
                "recommended_next_lane": inputs["r30_summary"]["summary"]["recommended_next_lane"],
            },
        },
        {
            "source": "results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json",
            "fields": {
                "systems_reauthorization_verdict": inputs["r31_summary"]["summary"]["systems_reauthorization_verdict"],
                "recommended_next_lane": inputs["r31_summary"]["summary"]["recommended_next_lane"],
            },
        },
    ]


def build_summary(
    checklist_rows: list[dict[str, object]],
    claim_packet: dict[str, object],
    inputs: dict[str, Any],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    r30 = inputs["r30_summary"]["summary"]
    r31 = inputs["r31_summary"]["summary"]
    return {
        "current_paper_phase": "h25_post_h23_reauthorization_packet_complete",
        "active_stage": "h25_refreeze_after_r30_r31_decision_packet",
        "current_frozen_stage": "h23_refreeze_after_r26_r27_r28",
        "decision_state": "post_h23_reauthorization_packet_complete",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "boundary_reauthorization_verdict": r30["boundary_reauthorization_verdict"],
        "systems_reauthorization_verdict": r31["systems_reauthorization_verdict"],
        "next_priority_lane": "r32_d0_family_local_boundary_sharp_zoom",
        "deferred_audit_lane": "r33_d0_non_retrieval_overhead_localization_audit",
        "blocked_future_lanes": [
            "r29_d0_same_endpoint_systems_recovery_execution_gate",
            "f3_post_h23_scope_lift_decision_bundle",
        ],
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Execute R32 only through its predeclared family-local sharp-zoom manifest while keeping R33 deferred as the systems-audit prerequisite and leaving R29/F3 blocked."
        ),
        "supported_here": claim_packet["supported_here"],
        "unsupported_here": claim_packet["unsupported_here"],
        "disconfirmed_here": claim_packet["disconfirmed_here"],
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    claim_packet = build_claim_packet()
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet, inputs)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h25_refreeze_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h25_refreeze_snapshot", "environment": environment.as_dict(), "rows": snapshot_rows},
    )
    write_json(
        OUT_DIR / "claim_packet.json",
        {"experiment": "h25_refreeze_claim_packet", "environment": environment.as_dict(), "summary": claim_packet},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h25_refreeze_after_r30_r31_decision_packet",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H25_refreeze_after_r30_r31_decision_packet/README.md",
                "docs/milestones/H25_refreeze_after_r30_r31_decision_packet/status.md",
                "docs/milestones/H25_refreeze_after_r30_r31_decision_packet/todo.md",
                "docs/milestones/H25_refreeze_after_r30_r31_decision_packet/acceptance.md",
                "docs/milestones/H25_refreeze_after_r30_r31_decision_packet/artifact_index.md",
                "docs/milestones/H25_refreeze_after_r30_r31_decision_packet/result_digest.md",
                "results/H23_refreeze_after_r26_r27_r28/summary.json",
                "results/R30_d0_boundary_reauthorization_packet/summary.json",
                "results/R31_d0_same_endpoint_systems_recovery_reauthorization_packet/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H25 Refreeze After R30 R31 Decision Packet\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n"
        "- `claim_packet.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
