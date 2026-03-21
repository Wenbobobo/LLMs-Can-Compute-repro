"""Export the post-R22/R23 refreeze summary for H21."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H21_refreeze_after_r22_r23"


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
    paths = {
        "h21_readme_text": ROOT / "docs" / "milestones" / "H21_refreeze_after_r22_r23" / "README.md",
        "h21_status_text": ROOT / "docs" / "milestones" / "H21_refreeze_after_r22_r23" / "status.md",
        "h21_todo_text": ROOT / "docs" / "milestones" / "H21_refreeze_after_r22_r23" / "todo.md",
        "h21_acceptance_text": ROOT / "docs" / "milestones" / "H21_refreeze_after_r22_r23" / "acceptance.md",
        "h21_artifact_index_text": ROOT / "docs" / "milestones" / "H21_refreeze_after_r22_r23" / "artifact_index.md",
        "f2_matrix_text": ROOT / "docs" / "milestones" / "F2_future_frontier_recheck_activation_matrix" / "activation_matrix.md",
        "h19_summary_text": ROOT / "results" / "H19_refreeze_and_next_scope_decision" / "summary.json",
        "h20_summary_text": ROOT / "results" / "H20_post_h19_mainline_reentry_and_hygiene_split" / "summary.json",
        "r2_summary_text": ROOT / "results" / "R2_systems_baseline_gate" / "summary.json",
        "e1b_summary_text": ROOT / "results" / "E1b_systems_patch" / "summary.json",
        "r22_summary_text": ROOT / "results" / "R22_d0_true_boundary_localization_gate" / "summary.json",
        "r23_summary_text": ROOT / "results" / "R23_d0_same_endpoint_systems_overturn_gate" / "summary.json",
    }
    inputs: dict[str, Any] = {key: read_text(path) for key, path in paths.items()}
    for key, path in paths.items():
        if key.endswith("_text") and path.suffix == ".json":
            inputs[key.removesuffix("_text")] = read_json(path)
    return inputs


def build_checklist_rows(
    *,
    h21_readme_text: str,
    h21_status_text: str,
    h21_todo_text: str,
    h21_acceptance_text: str,
    h21_artifact_index_text: str,
    f2_matrix_text: str,
    h19_summary_text: str,
    h19_summary: dict[str, Any],
    h20_summary_text: str,
    h20_summary: dict[str, Any],
    r2_summary_text: str,
    r2_summary: dict[str, Any],
    e1b_summary_text: str,
    e1b_summary: dict[str, Any],
    r22_summary_text: str,
    r22_summary: dict[str, Any],
    r23_summary_text: str,
    r23_summary: dict[str, Any],
) -> list[dict[str, object]]:
    r22_verdict = str(r22_summary["summary"]["gate"]["lane_verdict"])
    r23_verdict = str(r23_summary["summary"]["gate"]["lane_verdict"])
    return [
        {
            "item_id": "h21_milestone_docs_describe_the_post_r22_r23_refreeze",
            "status": "pass"
            if contains_all(
                h21_readme_text,
                ["refreeze stage", "`R22`", "`R23`", "machine-readable"],
            )
            and contains_all(
                h21_status_text,
                ["`supported_here`", "`unsupported_here`", "`disconfirmed_here`", "`F2`"],
            )
            and contains_all(
                h21_todo_text,
                ["`R22`", "`R23`", "`supported_here`", "`F2` activation conditions"],
            )
            and contains_all(
                h21_acceptance_text,
                ["`R22` and `R23`", "machine-readable", "`F2` trigger matrix"],
            )
            and contains_all(
                h21_artifact_index_text,
                ["results/R23_d0_same_endpoint_systems_overturn_gate/summary.json", "results/R22_d0_true_boundary_localization_gate/summary.json"],
            )
            else "blocked",
            "notes": "H21 should freeze R22 and R23 coherently before any further outward sync.",
        },
        {
            "item_id": "h19_and_h20_remain_the_preserved_pre_refreeze_controls",
            "status": "pass"
            if h19_summary["summary"]["decision_state"] == "same_endpoint_refreeze_complete"
            and h20_summary["summary"]["current_frozen_stage"] == "h19_refreeze_and_next_scope_decision"
            and contains_all(
                h19_summary_text,
                ['"decision_state": "same_endpoint_refreeze_complete"', '"next_priority_lane": "p13_public_surface_sync_and_repo_hygiene"'],
            )
            and contains_all(
                h20_summary_text,
                ['"lane_order": "h20_then_r22_then_r23_then_h21_then_p13"', '"current_frozen_stage": "h19_refreeze_and_next_scope_decision"'],
            )
            else "blocked",
            "notes": "H21 is a new refreeze on top of H19/H20, not a rewrite of history.",
        },
        {
            "item_id": "r22_exports_one_explicit_boundary_followup_verdict",
            "status": "pass"
            if r22_verdict in {
                "no_failure_in_extended_grid",
                "first_boundary_failure_localized",
                "resource_limited_without_failure",
            }
            and contains_all(r22_summary_text, ['"next_priority_lane": "r23_d0_same_endpoint_systems_overturn_gate"'])
            else "blocked",
            "notes": "H21 must freeze an explicit post-R21 boundary follow-up verdict rather than leaving R22 implicit.",
        },
        {
            "item_id": "r23_exports_one_explicit_same_endpoint_systems_verdict",
            "status": "pass"
            if r23_verdict in {
                "systems_materially_positive",
                "systems_still_mixed",
                "systems_negative_under_same_endpoint",
            }
            and contains_all(
                r23_summary_text,
                [
                    '"r2_systems_baseline_gate"',
                    '"e1b_systems_patch"',
                    '"next_priority_lane": "h21_refreeze_after_r22_r23"',
                ],
            )
            else "blocked",
            "notes": "H21 should inherit one measured systems verdict, not infer it impressionistically.",
        },
        {
            "item_id": "f2_remains_planning_only_after_h21",
            "status": "pass"
            if contains_all(
                f2_matrix_text,
                [
                    "`F2` is planning-only",
                    "Do not use `F2` to backdoor a broader",
                    "Scope-lift thesis is explicitly re-authorized",
                ],
            )
            and contains_all(
                r2_summary_text,
                ['"gate_status": "asymptotic_positive_but_end_to_end_not_yet_competitive"'],
            )
            and contains_all(
                e1b_summary_text,
                ['"gate_status_after_patch": "asymptotic_positive_but_end_to_end_not_yet_competitive"'],
            )
            else "blocked",
            "notes": "H21 may narrow or preserve the blocked F2 conditions, but it must not convert F2 into active widened scope.",
        },
    ]


def map_boundary_verdict(r22_verdict: str) -> str:
    if r22_verdict == "first_boundary_failure_localized":
        return "first_boundary_failure_localized"
    if r22_verdict == "resource_limited_without_failure":
        return "resource_limited_without_boundary_localization"
    return "extended_grid_no_break_still_not_localized"


def build_claim_packet(inputs: dict[str, Any]) -> dict[str, object]:
    r22_gate = inputs["r22_summary"]["summary"]["gate"]
    r23_gate = inputs["r23_summary"]["summary"]["gate"]
    boundary_verdict = map_boundary_verdict(str(r22_gate["lane_verdict"]))
    systems_verdict = str(r23_gate["lane_verdict"])

    supported_here = [
        "R22 stayed on the fixed tiny typed-bytecode D0 endpoint and extended the bounded executor-boundary scan beyond the original R21 grid.",
        (
            f"R22 executed {r22_gate['executed_candidate_count']}/"
            f"{r22_gate['planned_candidate_count']} planned candidates in the harder same-endpoint grid."
        ),
        (
            f"R23 stayed on the full current positive D0 systems universe and kept pointer-like exact exact on "
            f"{r23_gate['pointer_like_exact_case_count']}/{r23_gate['total_case_count']} rows."
        ),
    ]
    if systems_verdict == "systems_materially_positive":
        supported_here.append(
            "R23 overturns the earlier mixed same-endpoint systems gate under the bounded R2 threshold."
        )
    else:
        supported_here.append(
            "R23 keeps the same-endpoint systems story explicit and measured rather than letting the project drift on mechanism-only evidence."
        )

    unsupported_here = [
        "No H21 claim widens beyond the current tiny typed-bytecode D0 endpoint.",
        "H21 still does not authorize arbitrary compiled-language claims, a general softmax-replacement thesis, or a broader 'LLMs are computers' headline.",
        "H21 does not treat F2 planning material as permission to run widened probes by momentum.",
    ]
    if boundary_verdict != "first_boundary_failure_localized":
        unsupported_here.append("The true executor failure boundary is still not localized on the current same-endpoint evidence.")
    if systems_verdict != "systems_materially_positive":
        unsupported_here.append("The current-scope systems story is still not materially positive enough to support broader systems claims.")

    disconfirmed_here = [
        "R22 disconfirms the narrower expectation that the earlier R21 grid had already exposed an executor failure inside the currently tested same-endpoint envelope.",
    ]
    if systems_verdict == "systems_materially_positive":
        disconfirmed_here.append(
            "R23 disconfirms the narrower expectation that the current same-endpoint systems story must remain mixed once pointer-like exact is measured on the full positive D0 suite."
        )
    elif systems_verdict == "systems_negative_under_same_endpoint":
        disconfirmed_here.append(
            "R23 disconfirms the bounded hope that pointer-like exact is already a viable same-endpoint systems candidate on the current positive D0 suite."
        )

    return {
        "supported_here": supported_here,
        "unsupported_here": unsupported_here,
        "disconfirmed_here": disconfirmed_here,
        "distilled_result": {
            "r22_lane_verdict": r22_gate["lane_verdict"],
            "r22_executed_candidate_count": r22_gate["executed_candidate_count"],
            "r22_failure_candidate_count": r22_gate["failure_candidate_count"],
            "r23_lane_verdict": systems_verdict,
            "r23_pointer_like_exact_case_count": r23_gate["pointer_like_exact_case_count"],
            "r23_total_case_count": r23_gate["total_case_count"],
            "r23_pointer_like_median_ratio_vs_best_reference": r23_gate["pointer_like_median_ratio_vs_best_reference"],
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h19_summary = inputs["h19_summary"]["summary"]
    h20_summary = inputs["h20_summary"]["summary"]
    r22_gate = inputs["r22_summary"]["summary"]["gate"]
    r23_gate = inputs["r23_summary"]["summary"]["gate"]
    return [
        {
            "source": "results/H19_refreeze_and_next_scope_decision/summary.json",
            "fields": {
                "decision_state": h19_summary.get("decision_state"),
                "boundary_verdict": h19_summary.get("boundary_verdict"),
                "next_priority_lane": h19_summary.get("next_priority_lane"),
            },
        },
        {
            "source": "results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json",
            "fields": {
                "lane_order": h20_summary.get("lane_order"),
                "unsatisfied_frontier_activation_conditions": h20_summary.get(
                    "unsatisfied_frontier_activation_conditions"
                ),
            },
        },
        {
            "source": "results/R22_d0_true_boundary_localization_gate/summary.json",
            "fields": {
                "lane_verdict": r22_gate.get("lane_verdict"),
                "executed_candidate_count": r22_gate.get("executed_candidate_count"),
                "failure_candidate_count": r22_gate.get("failure_candidate_count"),
            },
        },
        {
            "source": "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json",
            "fields": {
                "lane_verdict": r23_gate.get("lane_verdict"),
                "pointer_like_exact_case_count": r23_gate.get("pointer_like_exact_case_count"),
                "pointer_like_median_ratio_vs_best_reference": r23_gate.get(
                    "pointer_like_median_ratio_vs_best_reference"
                ),
            },
        },
    ]


def build_summary(
    checklist_rows: list[dict[str, object]],
    inputs: dict[str, Any],
    claim_packet: dict[str, object],
) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    r22_verdict = str(inputs["r22_summary"]["summary"]["gate"]["lane_verdict"])
    r23_verdict = str(inputs["r23_summary"]["summary"]["gate"]["lane_verdict"])
    boundary_verdict = map_boundary_verdict(r22_verdict)
    unsatisfied_frontier_activation_conditions = []
    if boundary_verdict != "first_boundary_failure_localized":
        unsatisfied_frontier_activation_conditions.append("true_executor_boundary_localization")
    if r23_verdict != "systems_materially_positive":
        unsatisfied_frontier_activation_conditions.append("current_scope_systems_story_materially_positive")
    unsatisfied_frontier_activation_conditions.append("scope_lift_thesis_explicitly_reauthorized")

    next_priority_lane = (
        "p13_public_surface_sync_and_repo_hygiene"
        if r23_verdict == "systems_materially_positive"
        else "p12_manuscript_and_manifest_maintenance"
    )
    summary = {
        "current_paper_phase": "h21_refreeze_after_r22_r23_complete",
        "active_stage": "h21_refreeze_after_r22_r23",
        "prior_frozen_stage": "h19_refreeze_and_next_scope_decision",
        "reentry_stage": "h20_post_h19_mainline_reentry_and_hygiene_split",
        "decision_state": "post_r22_r23_refreeze_complete",
        "scope_lock_state": "tiny_typed_bytecode_d0_locked",
        "boundary_verdict": boundary_verdict,
        "systems_verdict": r23_verdict,
        "future_frontier_review_state": "planning_only_conditionally_reviewable",
        "future_frontier_lane": "f2_future_frontier_recheck_activation_matrix",
        "unsatisfied_frontier_activation_conditions": unsatisfied_frontier_activation_conditions,
        "next_priority_lane": next_priority_lane,
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "Advance to P13 for outward sync and repo hygiene while keeping F2 planning-only."
            if next_priority_lane == "p13_public_surface_sync_and_repo_hygiene"
            else "Advance to P12 to update claim ladders, manifests, and negative-result ledgers while keeping outward prose downstream."
        ),
        "supported_here": claim_packet["supported_here"],
        "unsupported_here": claim_packet["unsupported_here"],
        "disconfirmed_here": claim_packet["disconfirmed_here"],
        "distilled_result": claim_packet["distilled_result"],
    }
    return summary


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    claim_packet = build_claim_packet(inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h21_refreeze_after_r22_r23_checklist", "environment": environment.as_dict(), "rows": checklist_rows},
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {"experiment": "h21_refreeze_after_r22_r23_snapshot", "environment": environment.as_dict(), "rows": snapshot},
    )
    write_json(
        OUT_DIR / "claim_packet.json",
        {"experiment": "h21_refreeze_after_r22_r23_claim_packet", "environment": environment.as_dict(), "summary": claim_packet},
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h21_refreeze_after_r22_r23",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "docs/milestones/H21_refreeze_after_r22_r23/README.md",
                "docs/milestones/H21_refreeze_after_r22_r23/status.md",
                "docs/milestones/H21_refreeze_after_r22_r23/todo.md",
                "docs/milestones/H21_refreeze_after_r22_r23/acceptance.md",
                "docs/milestones/H21_refreeze_after_r22_r23/artifact_index.md",
                "docs/milestones/F2_future_frontier_recheck_activation_matrix/activation_matrix.md",
                "results/H19_refreeze_and_next_scope_decision/summary.json",
                "results/H20_post_h19_mainline_reentry_and_hygiene_split/summary.json",
                "results/R22_d0_true_boundary_localization_gate/summary.json",
                "results/R23_d0_same_endpoint_systems_overturn_gate/summary.json",
                "results/R2_systems_baseline_gate/summary.json",
                "results/E1b_systems_patch/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# H21 Refreeze After R22 R23\n\n"
        "Machine-readable post-H19 refreeze after the landed R22 boundary follow-up and R23 systems follow-up.\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `checklist.json`\n"
        "- `snapshot.json`\n"
        "- `claim_packet.json`\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
