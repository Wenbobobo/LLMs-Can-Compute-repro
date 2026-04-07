"""Export the post-H25 family-local boundary sharp zoom execution lane for R32."""

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import export_r22_d0_true_boundary_localization_gate as r22
import export_r26_d0_boundary_localization_execution_gate as r26
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R32_d0_family_local_boundary_sharp_zoom"

FAILURE_LIMIT_PER_BRANCH = 2
MAX_REFERENCE_STEP_LIMIT = 60_000
FIRST_FAIL_RECHECK_REPEATS = 2

LONG_FAMILY_LADDER = {
    "unique_address_deltas": (4, 8),
    "horizon_deltas": (0.5, 1.0),
}
CONTINUITY_LADDER = {
    "unique_address_deltas": (2, 4),
    "horizon_deltas": (0.5, 1.0),
}
ANCHOR_CONFIGS = (
    {
        "family": "checkpoint_replay_long",
        "unique_address_target": 32,
        "horizon_multiplier": 3.0,
        "checkpoint_depth": "plus_two",
        "hot_address_skew": "flattened",
        "ladder": LONG_FAMILY_LADDER,
    },
    {
        "family": "helper_checkpoint_braid_long",
        "unique_address_target": 20,
        "horizon_multiplier": 3.0,
        "checkpoint_depth": "plus_two",
        "hot_address_skew": "flattened",
        "ladder": LONG_FAMILY_LADDER,
    },
    {
        "family": "subroutine_braid_long",
        "unique_address_target": 20,
        "horizon_multiplier": 3.0,
        "checkpoint_depth": "plus_two",
        "hot_address_skew": "flattened",
        "ladder": LONG_FAMILY_LADDER,
    },
    {
        "family": "helper_checkpoint_braid",
        "unique_address_target": 8,
        "horizon_multiplier": 2.0,
        "checkpoint_depth": "plus_one",
        "hot_address_skew": "flattened",
        "ladder": CONTINUITY_LADDER,
    },
    {
        "family": "subroutine_braid",
        "unique_address_target": 6,
        "horizon_multiplier": 2.0,
        "checkpoint_depth": "plus_one",
        "hot_address_skew": "flattened",
        "ladder": CONTINUITY_LADDER,
    },
)

R32_CHECKPOINT_DEPTH_TO_CALL_DEPTH = {
    **r22.CHECKPOINT_DEPTH_TO_CALL_DEPTH,
    "plus_three": 3,
}
R32_CHECKPOINT_DEPTH_ORDER = ("baseline", "plus_one", "plus_two", "plus_three")
r22.CHECKPOINT_DEPTH_TO_CALL_DEPTH = R32_CHECKPOINT_DEPTH_TO_CALL_DEPTH
r22.CHECKPOINT_DEPTH_ORDER = R32_CHECKPOINT_DEPTH_ORDER


def next_checkpoint_depth(current_depth: str) -> str:
    if current_depth == "plus_one":
        return "plus_two"
    if current_depth == "plus_two":
        return "plus_three"
    raise ValueError(f"Unsupported R32 checkpoint ceiling: {current_depth}")


def dedupe_branch_plans(branch_plans: list[r22.BranchPlan]) -> list[r22.BranchPlan]:
    deduped: list[r22.BranchPlan] = []
    seen: set[tuple[str, str, int, float, str, str]] = set()
    for plan in branch_plans:
        key = (
            plan.lane_class,
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


def build_initial_branch_plans() -> list[r22.BranchPlan]:
    branch_plans: list[r22.BranchPlan] = []
    for anchor in ANCHOR_CONFIGS:
        family = str(anchor["family"])
        unique_address_target = int(anchor["unique_address_target"])
        horizon_multiplier = float(anchor["horizon_multiplier"])
        checkpoint_depth = str(anchor["checkpoint_depth"])
        hot_address_skew = str(anchor["hot_address_skew"])
        ladder = anchor["ladder"]

        branch_plans.append(
            r22.BranchPlan(
                lane_class="candidate_core",
                family=family,
                unique_address_target=unique_address_target,
                horizon_multiplier=horizon_multiplier,
                checkpoint_depth=checkpoint_depth,
                hot_address_skew=hot_address_skew,
            )
        )
        for delta in ladder["unique_address_deltas"]:
            branch_plans.append(
                r22.BranchPlan(
                    lane_class="unique_address_extension",
                    family=family,
                    unique_address_target=unique_address_target + int(delta),
                    horizon_multiplier=horizon_multiplier,
                    checkpoint_depth=checkpoint_depth,
                    hot_address_skew=hot_address_skew,
                )
            )
        for delta in ladder["horizon_deltas"]:
            branch_plans.append(
                r22.BranchPlan(
                    lane_class="horizon_extension",
                    family=family,
                    unique_address_target=unique_address_target,
                    horizon_multiplier=horizon_multiplier + float(delta),
                    checkpoint_depth=checkpoint_depth,
                    hot_address_skew=hot_address_skew,
                )
            )
        branch_plans.append(
            r22.BranchPlan(
                lane_class="checkpoint_depth_extension",
                family=family,
                unique_address_target=unique_address_target,
                horizon_multiplier=horizon_multiplier,
                checkpoint_depth=next_checkpoint_depth(checkpoint_depth),
                hot_address_skew=hot_address_skew,
            )
        )
    return dedupe_branch_plans(branch_plans)


def build_hot_skew_confirmation_branch_plans(
    first_fail_digest_rows: list[dict[str, object]],
) -> list[r22.BranchPlan]:
    if not first_fail_digest_rows:
        return []
    first_fail = first_fail_digest_rows[0]
    if str(first_fail["hot_address_skew"]) != "flattened":
        return []
    return [
        r22.BranchPlan(
            lane_class="hot_skew_confirmation",
            family=str(first_fail["family"]),
            unique_address_target=int(first_fail["unique_address_target"]),
            horizon_multiplier=float(first_fail["horizon_multiplier"]),
            checkpoint_depth=str(first_fail["checkpoint_depth"]),
            hot_address_skew="baseline",
        )
    ]


def measure_branch_spec(spec: r22.BranchSpec):
    row, profile = r26.measure_branch_spec(spec)
    row["authorization_source_stage"] = "r30_d0_boundary_reauthorization_packet"
    row["execution_stage"] = "r32_d0_family_local_boundary_sharp_zoom"
    profile["authorization_source_stage"] = "r30_d0_boundary_reauthorization_packet"
    profile["execution_stage"] = "r32_d0_family_local_boundary_sharp_zoom"
    return row, profile


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
        row, profile = measure_branch_spec(spec)
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
        row, _profile = measure_branch_spec(spec)
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


def assess_boundary_gate(
    branch_specs: list[r22.BranchSpec],
    rows: list[dict[str, object]],
    branch_summary_rows: list[dict[str, object]],
    *,
    pruned_count: int,
    skipped_rows: list[dict[str, object]],
    first_fail_digest_rows: list[dict[str, object]],
    localized_boundary_rows: list[dict[str, object]],
    failure_rechecks: list[dict[str, object]],
) -> dict[str, object]:
    exact_candidate_count = sum(bool(row["exact"]) for row in rows)
    failure_candidate_count = sum(not bool(row["exact"]) for row in rows)
    first_fail = first_fail_digest_rows[0] if first_fail_digest_rows else None
    localized_boundary = localized_boundary_rows[0] if localized_boundary_rows else None
    reproduced = bool(failure_rechecks) and all(bool(row["reproduced"]) for row in failure_rechecks)
    supporting_exact_neighbor_count = (
        0 if localized_boundary is None else int(localized_boundary["supporting_exact_neighbor_count"])
    )

    if first_fail is not None and reproduced and supporting_exact_neighbor_count >= 1:
        lane_verdict = "first_boundary_failure_localized"
        reason = (
            "R32 found a reproducible first failing candidate and at least one nearby exact row "
            "inside the authorized family-local sharp zoom."
        )
    elif first_fail is not None:
        lane_verdict = "near_boundary_mixed_signal_needs_confirmation"
        reason = (
            "R32 found a near-boundary failure signal, but the bounded packet did not yet support a clean "
            "localized boundary claim."
        )
    elif skipped_rows:
        lane_verdict = "resource_limited_before_localization"
        reason = "R32 exhausted the bounded family-local ladder under the current reference-step cap."
    else:
        lane_verdict = "grid_extended_still_not_localized"
        reason = "Every executed R32 branch stayed exact inside the authorized family-local sharp zoom."

    return {
        "lane_verdict": lane_verdict,
        "reason": reason,
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
        "next_priority_lane": "h26_refreeze_after_r32_boundary_sharp_zoom",
    }


def build_summary(branch_specs: list[r22.BranchSpec], gate: dict[str, object]) -> dict[str, object]:
    return {
        "status": "r32_family_local_boundary_sharp_zoom_complete",
        "current_frozen_stage": "h23_refreeze_after_r26_r27_r28",
        "current_active_packet": "h25_refreeze_after_r30_r31_decision_packet",
        "authorization_source_stage": "r30_d0_boundary_reauthorization_packet",
        "gate": gate,
        "planned_lane_classes": sorted({spec.lane_class for spec in branch_specs}),
        "planned_families": sorted({spec.family for spec in branch_specs}),
        "planned_unique_address_targets": sorted({spec.unique_address_target for spec in branch_specs}),
        "planned_horizon_multipliers": sorted({spec.horizon_multiplier for spec in branch_specs}),
        "planned_checkpoint_depths": sorted(
            {spec.checkpoint_depth for spec in branch_specs},
            key=R32_CHECKPOINT_DEPTH_ORDER.index,
        ),
        "planned_hot_address_skews": sorted(
            {spec.hot_address_skew for spec in branch_specs},
            key=r22.HOT_ADDRESS_SKEW_ORDER.index,
        ),
        "recommended_next_action": (
            "Freeze the R32 outcome into H26 before deciding whether any deferred same-endpoint follow-up remains justified."
        ),
        "supported_here": [
            "R32 stays on the fixed tiny typed-bytecode D0 endpoint.",
            "R32 reuses the R30-authorized candidate core and only the four approved axes.",
            "R32 exports first-fail, neighboring exact rows, and a machine-readable lane verdict.",
        ],
        "unsupported_here": [
            "R32 does not reopen the historical full grid.",
            "R32 does not widen to a new endpoint or authorize R29 or F3.",
            "R32 does not treat a mixed signal as broader scope-lift evidence.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    admitted_rows = r22.load_r19_admitted_runtime_rows()
    template_registry = r22.build_template_registry(admitted_rows)

    initial_branch_plans = build_initial_branch_plans()
    initial_branch_specs = r22.build_branch_specs(template_registry, initial_branch_plans)
    rows, profiles, pruned_count, skipped_rows = execute_boundary_scan(initial_branch_specs)

    first_fail_digest_rows = r22.build_first_fail_digest(rows)
    confirmation_branch_plans = build_hot_skew_confirmation_branch_plans(first_fail_digest_rows)
    confirmation_branch_specs = (
        []
        if not confirmation_branch_plans
        else r22.build_branch_specs(template_registry, confirmation_branch_plans)
    )
    confirmation_rows, confirmation_profiles, confirmation_pruned_count, confirmation_skipped_rows = (
        execute_boundary_scan(confirmation_branch_specs)
        if confirmation_branch_specs
        else ([], [], 0, [])
    )

    branch_specs = initial_branch_specs + confirmation_branch_specs
    manifest_rows = [r22.branch_spec_to_row(spec) for spec in branch_specs]
    rows.extend(confirmation_rows)
    profiles.extend(confirmation_profiles)
    skipped_rows.extend(confirmation_skipped_rows)
    pruned_count += confirmation_pruned_count

    branch_summary_rows = r22.build_branch_summary(branch_specs, rows, skipped_rows)
    failure_rows = [row for row in rows if not bool(row["exact"])]
    positive_rows = [row for row in rows if bool(row["exact"])]
    first_fail_digest_rows = r22.build_first_fail_digest(rows)
    localized_boundary_rows = r22.build_localized_boundary(first_fail_digest_rows, branch_summary_rows)
    neighbor_exact_rows = (
        [] if not localized_boundary_rows else localized_boundary_rows[0]["supporting_exact_neighbors"]
    )
    spec_lookup = {spec.candidate_id: spec for spec in branch_specs}
    failure_rechecks = build_failure_rechecks(spec_lookup, first_fail_digest_rows)
    gate = assess_boundary_gate(
        branch_specs,
        rows,
        branch_summary_rows,
        pruned_count=pruned_count,
        skipped_rows=skipped_rows,
        first_fail_digest_rows=first_fail_digest_rows,
        localized_boundary_rows=localized_boundary_rows,
        failure_rechecks=failure_rechecks,
    )
    summary = build_summary(branch_specs, gate)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    r22.write_json(
        OUT_DIR / "manifest_rows.json",
        {"experiment": "r32_manifest_rows", "environment": environment.as_dict(), "rows": manifest_rows},
    )
    r22.write_csv(OUT_DIR / "manifest_rows.csv", manifest_rows)
    r22.write_json(
        OUT_DIR / "boundary_rows.json",
        {"experiment": "r32_boundary_rows", "environment": environment.as_dict(), "rows": rows},
    )
    r22.write_csv(OUT_DIR / "boundary_rows.csv", rows)
    r22.write_json(
        OUT_DIR / "address_profiles.json",
        {"experiment": "r32_address_profiles", "environment": environment.as_dict(), "rows": profiles},
    )
    r22.write_json(
        OUT_DIR / "positive_rows.json",
        {"experiment": "r32_positive_rows", "environment": environment.as_dict(), "rows": positive_rows},
    )
    r22.write_json(
        OUT_DIR / "failure_rows.json",
        {"experiment": "r32_failure_rows", "environment": environment.as_dict(), "rows": failure_rows},
    )
    r22.write_json(
        OUT_DIR / "skipped_rows.json",
        {"experiment": "r32_skipped_rows", "environment": environment.as_dict(), "rows": skipped_rows},
    )
    r22.write_json(
        OUT_DIR / "branch_summary.json",
        {"experiment": "r32_branch_summary", "environment": environment.as_dict(), "rows": branch_summary_rows},
    )
    r22.write_json(
        OUT_DIR / "first_fail_digest.json",
        {"experiment": "r32_first_fail_digest", "environment": environment.as_dict(), "rows": first_fail_digest_rows},
    )
    r22.write_json(
        OUT_DIR / "localized_boundary.json",
        {"experiment": "r32_localized_boundary", "environment": environment.as_dict(), "rows": localized_boundary_rows},
    )
    r22.write_json(
        OUT_DIR / "neighbor_exact_rows.json",
        {"experiment": "r32_neighbor_exact_rows", "environment": environment.as_dict(), "rows": neighbor_exact_rows},
    )
    r22.write_json(
        OUT_DIR / "failure_rechecks.json",
        {"experiment": "r32_failure_rechecks", "environment": environment.as_dict(), "rows": failure_rechecks},
    )
    r22.write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r32_d0_family_local_boundary_sharp_zoom",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/H23_refreeze_after_r26_r27_r28/summary.json",
                "results/H25_refreeze_after_r30_r31_decision_packet/summary.json",
                "results/R30_d0_boundary_reauthorization_packet/summary.json",
                "docs/milestones/R32_d0_family_local_boundary_sharp_zoom/execution_manifest.md",
                "docs/plans/2026-03-22-post-unattended-r32-mainline-design.md",
                "tmp/active_wave_plan.md",
                "src/model/free_running_executor.py",
                "src/bytecode/datasets.py",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "# R32 D0 Family-Local Boundary Sharp Zoom\n\n"
        "Artifacts:\n"
        "- `summary.json`\n"
        "- `manifest_rows.json`\n"
        "- `boundary_rows.json`\n"
        "- `branch_summary.json`\n"
        "- `positive_rows.json`\n"
        "- `failure_rows.json`\n"
        "- `first_fail_digest.json`\n"
        "- `neighbor_exact_rows.json`\n"
        "- `localized_boundary.json`\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
