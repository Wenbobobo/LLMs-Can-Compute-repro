"""Export the conditional post-R26 boundary-localization follow-up gate for R27."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import export_r22_d0_true_boundary_localization_gate as r22
import export_r26_d0_boundary_localization_execution_gate as r26
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
R26_OUT_DIR = ROOT / "results" / "R26_d0_boundary_localization_execution_gate"
OUT_DIR = ROOT / "results" / "R27_d0_boundary_localization_extension_gate"

FAILURE_LIMIT_PER_BRANCH = 2
MAX_REFERENCE_STEP_LIMIT = 60_000
FIRST_FAIL_RECHECK_REPEATS = 2

SECOND_WAVE_EXTENSION_BRANCH_PLANS = (
    ("second_wave_extension", "subroutine_braid_long", 24, 3.5, "plus_two", "baseline"),
    ("second_wave_extension", "subroutine_braid_long", 24, 3.5, "plus_two", "flattened"),
    ("second_wave_extension", "helper_checkpoint_braid_long", 24, 3.5, "plus_two", "baseline"),
    ("second_wave_extension", "helper_checkpoint_braid_long", 24, 3.5, "plus_two", "flattened"),
    ("second_wave_extension", "checkpoint_replay_long", 40, 3.5, "plus_two", "baseline"),
    ("second_wave_extension", "checkpoint_replay_long", 40, 3.5, "plus_two", "flattened"),
)


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_r26_inputs() -> dict[str, Any]:
    return {
        "r26_summary": read_json(R26_OUT_DIR / "summary.json"),
        "r26_branch_manifest": read_json(R26_OUT_DIR / "branch_manifest.json"),
        "r26_first_fail_digest": read_json(R26_OUT_DIR / "first_fail_digest.json"),
        "r26_localized_boundary": read_json(R26_OUT_DIR / "localized_boundary.json"),
        "r26_branch_summary": read_json(R26_OUT_DIR / "branch_summary.json"),
    }


def determine_execution_mode(r26_verdict: str) -> str:
    if r26_verdict == "near_boundary_mixed_signal_needs_confirmation":
        return "confirmation_mode"
    if r26_verdict == "grid_extended_still_not_localized":
        return "extension_mode"
    return "skip"


def branch_plan_from_row(row: dict[str, object], *, lane_class: str) -> r22.BranchPlan:
    return r22.BranchPlan(
        lane_class=lane_class,
        family=str(row["family"]),
        unique_address_target=int(row["unique_address_target"]),
        horizon_multiplier=float(row["horizon_multiplier"]),
        checkpoint_depth=str(row["checkpoint_depth"]),
        hot_address_skew=str(row["hot_address_skew"]),
    )


def opposite_hot_skew(hot_address_skew: str) -> str:
    return "baseline" if hot_address_skew == "flattened" else "flattened"


def dedupe_branch_plans(branch_plans: list[r22.BranchPlan]) -> list[r22.BranchPlan]:
    deduped: list[r22.BranchPlan] = []
    seen: set[tuple[str, int, float, str, str]] = set()
    for plan in branch_plans:
        key = (
            plan.family,
            plan.unique_address_target,
            plan.horizon_multiplier,
            plan.checkpoint_depth,
            plan.hot_address_skew,
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(plan)
    return deduped


def build_confirmation_branch_plans(inputs: dict[str, Any]) -> tuple[list[r22.BranchPlan], dict[str, object]]:
    first_fail_rows = inputs["r26_first_fail_digest"]["rows"]
    if not first_fail_rows:
        raise RuntimeError("R27 confirmation mode requires an R26 first-fail digest.")
    first_fail = first_fail_rows[0]
    branch_summary_rows = inputs["r26_branch_summary"]["rows"]
    branch_summary_by_id = {str(row["branch_id"]): row for row in branch_summary_rows}

    selected_plans: list[r22.BranchPlan] = [
        branch_plan_from_row(first_fail, lane_class="confirmation_failure_branch")
    ]
    supporting_neighbor_branch_id = None
    localized_rows = inputs["r26_localized_boundary"]["rows"]
    if localized_rows:
        neighbors = localized_rows[0].get("supporting_exact_neighbors", [])
        if neighbors:
            supporting_neighbor_branch_id = str(neighbors[0]["branch_id"])
            selected_plans.append(
                branch_plan_from_row(
                    branch_summary_by_id[supporting_neighbor_branch_id],
                    lane_class="confirmation_exact_neighbor",
                )
            )

    counterpart_plan = r22.BranchPlan(
        lane_class="confirmation_hot_skew_counterpart",
        family=str(first_fail["family"]),
        unique_address_target=int(first_fail["unique_address_target"]),
        horizon_multiplier=float(first_fail["horizon_multiplier"]),
        checkpoint_depth=str(first_fail["checkpoint_depth"]),
        hot_address_skew=opposite_hot_skew(str(first_fail["hot_address_skew"])),
    )
    selected_plans.append(counterpart_plan)

    deduped_plans = dedupe_branch_plans(selected_plans)
    trigger_state = {
        "execution_mode": "confirmation_mode",
        "r26_trigger_verdict": "near_boundary_mixed_signal_needs_confirmation",
        "first_fail_branch_id": first_fail["branch_id"],
        "first_fail_candidate_id": first_fail["candidate_id"],
        "supporting_exact_neighbor_branch_id": supporting_neighbor_branch_id,
        "hot_skew_counterpart_branch_id": (
            f"confirmation_hot_skew_counterpart_{first_fail['family']}_"
            f"u{first_fail['unique_address_target']}_h{r22.multiplier_label(float(first_fail['horizon_multiplier']))}_"
            f"c{first_fail['checkpoint_depth']}_k{opposite_hot_skew(str(first_fail['hot_address_skew']))}"
        ),
    }
    return deduped_plans, trigger_state


def build_extension_branch_plans() -> tuple[list[r22.BranchPlan], dict[str, object]]:
    return (
        [r22.BranchPlan(*plan) for plan in SECOND_WAVE_EXTENSION_BRANCH_PLANS],
        {
            "execution_mode": "extension_mode",
            "r26_trigger_verdict": "grid_extended_still_not_localized",
            "planned_second_wave_branch_count": len(SECOND_WAVE_EXTENSION_BRANCH_PLANS),
            "planned_second_wave_families": sorted({plan[1] for plan in SECOND_WAVE_EXTENSION_BRANCH_PLANS}),
        },
    )


def build_branch_plans_for_mode(mode: str, inputs: dict[str, Any]) -> tuple[list[r22.BranchPlan], dict[str, object]]:
    if mode == "confirmation_mode":
        return build_confirmation_branch_plans(inputs)
    if mode == "extension_mode":
        return build_extension_branch_plans()
    return [], {"execution_mode": "skip", "r26_trigger_verdict": inputs["r26_summary"]["summary"]["gate"]["lane_verdict"]}


def execute_boundary_scan(
    branch_specs: list[r22.BranchSpec],
) -> tuple[list[dict[str, object]], list[dict[str, object]], int, list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    profiles: list[dict[str, object]] = []
    skipped_rows: list[dict[str, object]] = []
    failures_by_branch: dict[str, int] = {}
    pruned_count = 0
    for spec in branch_specs:
        if spec.expected_reference_step_count > MAX_REFERENCE_STEP_LIMIT:
            skipped_rows.append(
                {
                    **r22.branch_spec_to_row(spec),
                    "skip_class": "resource_limit",
                    "skip_reason": "expected_reference_step_limit_exceeded",
                }
            )
            continue
        if failures_by_branch.get(spec.branch_id, 0) >= FAILURE_LIMIT_PER_BRANCH:
            pruned_count += 1
            continue
        row, profile = r26.measure_branch_spec(spec)
        rows.append(row)
        profiles.append(profile)
        if not bool(row["exact"]):
            failures_by_branch[spec.branch_id] = failures_by_branch.get(spec.branch_id, 0) + 1
    return rows, profiles, pruned_count, skipped_rows


def build_failure_rechecks(
    spec_lookup: dict[str, r22.BranchSpec],
    first_fail_digest_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    if not first_fail_digest_rows:
        return []
    first_fail = first_fail_digest_rows[0]
    spec = spec_lookup[str(first_fail["candidate_id"])]
    rows: list[dict[str, object]] = []
    for recheck_index in range(FIRST_FAIL_RECHECK_REPEATS):
        row, _profile = r26.measure_branch_spec(spec)
        reproduced = (
            not bool(row["exact"])
            and row["first_mismatch_step"] == first_fail["first_mismatch_step"]
            and row["failure_class"] == first_fail["failure_class"]
            and row["failure_reason"] == first_fail["failure_reason"]
        )
        rows.append(
            {
                "candidate_id": spec.candidate_id,
                "recheck_index": recheck_index,
                "exact": row["exact"],
                "first_mismatch_step": row["first_mismatch_step"],
                "failure_reason": row["failure_reason"],
                "failure_class": row["failure_class"],
                "runtime_seconds": row["runtime_seconds"],
                "reproduced": reproduced,
            }
        )
    return rows


def assess_gate(
    *,
    mode: str,
    branch_specs: list[r22.BranchSpec],
    rows: list[dict[str, object]],
    branch_summary_rows: list[dict[str, object]],
    pruned_count: int,
    skipped_rows: list[dict[str, object]],
    first_fail_digest_rows: list[dict[str, object]],
    localized_boundary_rows: list[dict[str, object]],
    failure_rechecks: list[dict[str, object]],
    trigger_state: dict[str, object],
) -> dict[str, object]:
    exact_candidate_count = sum(bool(row["exact"]) for row in rows)
    failure_candidate_count = sum(not bool(row["exact"]) for row in rows)
    first_fail = first_fail_digest_rows[0] if first_fail_digest_rows else None
    localized_boundary = localized_boundary_rows[0] if localized_boundary_rows else None
    supporting_exact_neighbor_count = (
        0 if localized_boundary is None else int(localized_boundary["supporting_exact_neighbor_count"])
    )
    reproduced = bool(failure_rechecks) and all(bool(row["reproduced"]) for row in failure_rechecks)

    if mode == "skip":
        lane_verdict = "skipped_not_triggered"
        reason = "R27 stayed inactive because R26 already resolved the boundary packet or stopped under its bounded gate."
    elif mode == "confirmation_mode":
        if first_fail is not None and reproduced and supporting_exact_neighbor_count >= 1:
            lane_verdict = "confirmation_failure_localized"
            reason = "R27 confirmation mode reproduced the failing branch and found at least one exact supporting branch in the bounded follow-up packet."
        elif first_fail is not None and reproduced:
            lane_verdict = "confirmation_failure_reproduced_without_localization"
            reason = "R27 reproduced the failing branch, but the bounded confirmation packet still did not localize a clean exact neighbor."
        elif first_fail is not None:
            lane_verdict = "confirmation_failure_signal_mixed"
            reason = "R27 still observed a failing branch, but the bounded confirmation packet did not reproduce a stable localized boundary."
        else:
            lane_verdict = "confirmation_signal_not_reproduced"
            reason = "R27 confirmation mode did not reproduce the earlier near-boundary signal."
    else:
        if first_fail is not None and reproduced and supporting_exact_neighbor_count >= 1:
            lane_verdict = "extension_failure_localized"
            reason = "R27 extension mode found a reproducible failing branch with at least one exact supporting neighbor in the predeclared second-wave ceiling."
        elif first_fail is not None:
            lane_verdict = "extension_failure_found_without_localization"
            reason = "R27 extension mode found a failure, but the bounded second-wave ceiling still did not localize a clean exact neighbor."
        elif skipped_rows:
            lane_verdict = "resource_limited_before_localization"
            reason = "R27 hit the bounded reference-step cap before localizing a failure."
        else:
            lane_verdict = "extension_grid_still_not_localized"
            reason = "Every executed R27 candidate stayed exact inside the predeclared second-wave extension ceiling."

    return {
        "execution_mode": mode,
        "lane_verdict": lane_verdict,
        "reason": reason,
        "r26_trigger_verdict": trigger_state.get("r26_trigger_verdict"),
        "planned_branch_count": len({spec.branch_id for spec in branch_specs}),
        "planned_candidate_count": len(branch_specs),
        "executed_candidate_count": len(rows),
        "resource_skipped_candidate_count": len(skipped_rows),
        "pruned_candidate_count": pruned_count,
        "exact_candidate_count": exact_candidate_count,
        "failure_candidate_count": failure_candidate_count,
        "failure_branch_count": sum(
            int(row["failure_candidate_count"]) > 0 for row in branch_summary_rows
        ),
        "first_fail_candidate_id": None if first_fail is None else first_fail["candidate_id"],
        "first_fail_program_name": None if first_fail is None else first_fail["program_name"],
        "first_fail_reproduced": None if not failure_rechecks else reproduced,
        "first_fail_supporting_exact_neighbor_count": None
        if localized_boundary is None
        else supporting_exact_neighbor_count,
        "next_priority_lane": "h23_refreeze_after_r26_r27_r28",
    }


def build_summary(
    *,
    mode: str,
    branch_specs: list[r22.BranchSpec],
    gate: dict[str, object],
) -> dict[str, object]:
    return {
        "status": "r27_boundary_localization_extension_complete",
        "current_frozen_stage": "h21_refreeze_after_r22_r23",
        "source_runtime_stage": "r26_d0_boundary_localization_execution_gate",
        "gate": gate,
        "planned_lane_classes": sorted({spec.lane_class for spec in branch_specs}) if branch_specs else [],
        "planned_families": sorted({spec.family for spec in branch_specs}),
        "planned_unique_address_targets": sorted({spec.unique_address_target for spec in branch_specs}),
        "planned_horizon_multipliers": sorted({spec.horizon_multiplier for spec in branch_specs}),
        "planned_checkpoint_depths": sorted(
            {spec.checkpoint_depth for spec in branch_specs},
            key=r22.CHECKPOINT_DEPTH_ORDER.index,
        )
        if branch_specs
        else [],
        "planned_hot_address_skews": sorted(
            {spec.hot_address_skew for spec in branch_specs},
            key=r22.HOT_ADDRESS_SKEW_ORDER.index,
        )
        if branch_specs
        else [],
        "recommended_next_action": "Refreeze the bounded packet in H23 and keep any wider follow-up blocked pending that refreeze.",
        "supported_here": [
            "R27 only activates when the landed R26 verdict explicitly triggers confirmation or second-wave extension work.",
            "R27 keeps the boundary question on the fixed tiny typed-bytecode D0 endpoint.",
            "R27 preserves its manifest, row exports, and bounded verdict even when it stays skipped.",
        ],
        "unsupported_here": [
            "R27 does not authorize plus_three checkpoint depth, a new family, or a wider same-endpoint suite.",
            "R27 does not reopen systems repair or any broader scope-lift wording.",
            "R27 ends at H23 rather than opening another momentum-driven runtime lane.",
        ],
        "execution_mode": mode,
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_r26_inputs()
    r26_verdict = str(inputs["r26_summary"]["summary"]["gate"]["lane_verdict"])
    mode = determine_execution_mode(r26_verdict)
    branch_plans, trigger_state = build_branch_plans_for_mode(mode, inputs)

    if branch_plans:
        admitted_rows = r22.load_r19_admitted_runtime_rows()
        template_registry = r22.build_template_registry(admitted_rows)
        branch_specs = r22.build_branch_specs(template_registry, branch_plans)
        spec_lookup = {spec.candidate_id: spec for spec in branch_specs}
        manifest_rows = [r22.branch_spec_to_row(spec) for spec in branch_specs]
        rows, profiles, pruned_count, skipped_rows = execute_boundary_scan(branch_specs)
        branch_summary_rows = r22.build_branch_summary(branch_specs, rows, skipped_rows)
        failure_rows = [row for row in rows if not bool(row["exact"])]
        first_fail_digest_rows = r22.build_first_fail_digest(rows)
        localized_boundary_rows = r22.build_localized_boundary(first_fail_digest_rows, branch_summary_rows)
        neighbor_exact_rows = (
            [] if not localized_boundary_rows else localized_boundary_rows[0]["supporting_exact_neighbors"]
        )
        failure_rechecks = build_failure_rechecks(spec_lookup, first_fail_digest_rows)
    else:
        branch_specs = []
        manifest_rows = []
        rows = []
        profiles = []
        pruned_count = 0
        skipped_rows = []
        branch_summary_rows = []
        failure_rows = []
        first_fail_digest_rows = []
        localized_boundary_rows = []
        neighbor_exact_rows = []
        failure_rechecks = []

    gate = assess_gate(
        mode=mode,
        branch_specs=branch_specs,
        rows=rows,
        branch_summary_rows=branch_summary_rows,
        pruned_count=pruned_count,
        skipped_rows=skipped_rows,
        first_fail_digest_rows=first_fail_digest_rows,
        localized_boundary_rows=localized_boundary_rows,
        failure_rechecks=failure_rechecks,
        trigger_state=trigger_state,
    )
    summary = build_summary(mode=mode, branch_specs=branch_specs, gate=gate)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    r22.write_json(
        OUT_DIR / "trigger_state.json",
        {"experiment": "r27_trigger_state", "environment": environment.as_dict(), "summary": trigger_state},
    )
    r22.write_json(
        OUT_DIR / "branch_manifest.json",
        {"experiment": "r27_branch_manifest", "environment": environment.as_dict(), "rows": manifest_rows},
    )
    r22.write_csv(OUT_DIR / "branch_manifest.csv", manifest_rows)
    r22.write_json(
        OUT_DIR / "boundary_rows.json",
        {"experiment": "r27_boundary_rows", "environment": environment.as_dict(), "rows": rows},
    )
    r22.write_csv(OUT_DIR / "boundary_rows.csv", rows)
    r22.write_json(
        OUT_DIR / "address_profiles.json",
        {"experiment": "r27_address_profiles", "environment": environment.as_dict(), "rows": profiles},
    )
    r22.write_json(
        OUT_DIR / "positive_rows.json",
        {"experiment": "r27_positive_rows", "environment": environment.as_dict(), "rows": [row for row in rows if bool(row["exact"])]},
    )
    r22.write_json(
        OUT_DIR / "failure_rows.json",
        {"experiment": "r27_failure_rows", "environment": environment.as_dict(), "rows": failure_rows},
    )
    r22.write_json(
        OUT_DIR / "skipped_rows.json",
        {"experiment": "r27_skipped_rows", "environment": environment.as_dict(), "rows": skipped_rows},
    )
    r22.write_json(
        OUT_DIR / "branch_summary.json",
        {"experiment": "r27_branch_summary", "environment": environment.as_dict(), "rows": branch_summary_rows},
    )
    r22.write_json(
        OUT_DIR / "first_fail_digest.json",
        {"experiment": "r27_first_fail_digest", "environment": environment.as_dict(), "rows": first_fail_digest_rows},
    )
    r22.write_json(
        OUT_DIR / "localized_boundary.json",
        {"experiment": "r27_localized_boundary", "environment": environment.as_dict(), "rows": localized_boundary_rows},
    )
    r22.write_json(
        OUT_DIR / "neighbor_exact_rows.json",
        {"experiment": "r27_neighbor_exact_rows", "environment": environment.as_dict(), "rows": neighbor_exact_rows},
    )
    r22.write_json(
        OUT_DIR / "failure_rechecks.json",
        {"experiment": "r27_failure_rechecks", "environment": environment.as_dict(), "rows": failure_rechecks},
    )
    r22.write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r27_d0_boundary_localization_extension_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/R26_d0_boundary_localization_execution_gate/summary.json",
                "results/R26_d0_boundary_localization_execution_gate/branch_manifest.json",
                "results/R26_d0_boundary_localization_execution_gate/first_fail_digest.json",
                "results/R26_d0_boundary_localization_execution_gate/localized_boundary.json",
                "results/R26_d0_boundary_localization_execution_gate/branch_summary.json",
                "docs/plans/2026-03-21-post-h21-dual-track-boundary-reopen-design.md",
                "tmp/active_wave_plan.md",
                "src/model/free_running_executor.py",
                "src/bytecode/datasets.py",
            ],
            "summary": summary,
        },
    )


if __name__ == "__main__":
    main()
