"""Export the first bounded post-H21 boundary-localization execution gate for R26."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import export_r22_d0_true_boundary_localization_gate as r22

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R26_d0_boundary_localization_execution_gate"

FAILURE_LIMIT_PER_BRANCH = 2
MAX_REFERENCE_STEP_LIMIT = 60_000
FIRST_FAIL_RECHECK_REPEATS = 2

CORE_BRANCH_PLANS = (
    ("candidate_core", "subroutine_braid", 6, 2.0, "plus_one", "flattened"),
    ("candidate_core", "helper_checkpoint_braid", 8, 2.0, "plus_one", "flattened"),
    ("candidate_core", "subroutine_braid_long", 20, 3.0, "plus_two", "flattened"),
    ("candidate_core", "helper_checkpoint_braid_long", 20, 3.0, "plus_two", "flattened"),
    ("candidate_core", "checkpoint_replay_long", 32, 3.0, "plus_two", "flattened"),
)
FIRST_WAVE_EXTENSION_BRANCH_PLANS = (
    ("first_wave_extension", "subroutine_braid_long", 24, 3.0, "plus_two", "flattened"),
    ("first_wave_extension", "subroutine_braid_long", 20, 3.5, "plus_two", "flattened"),
    ("first_wave_extension", "helper_checkpoint_braid_long", 24, 3.0, "plus_two", "flattened"),
    ("first_wave_extension", "helper_checkpoint_braid_long", 20, 3.5, "plus_two", "flattened"),
    ("first_wave_extension", "checkpoint_replay_long", 40, 3.0, "plus_two", "flattened"),
    ("first_wave_extension", "checkpoint_replay_long", 32, 3.5, "plus_two", "flattened"),
)

_BASE_MEASURE_BRANCH_SPEC = r22.measure_branch_spec


def build_branch_plans() -> list[r22.BranchPlan]:
    return [r22.BranchPlan(*plan) for plan in CORE_BRANCH_PLANS + FIRST_WAVE_EXTENSION_BRANCH_PLANS]


def build_wrapped_program(spec: r22.BranchSpec, base_program):
    padding_instructions = r22.build_padding_instructions(
        padding_base_address=spec.padding_base_address,
        padding_unique_count=spec.padding_unique_count,
        flatten_rounds=spec.flatten_rounds,
        seed_id=spec.seed_id,
    )
    base_instructions = r22.rebase_instructions(base_program.instructions, offset=len(padding_instructions))
    body_instructions = padding_instructions + base_instructions
    if spec.target_wrapper_call_depth == 0:
        wrapped_instructions = body_instructions
    else:
        subroutine = r22.build_nested_checkpoint_subroutine(
            body_instructions,
            call_depth=spec.target_wrapper_call_depth,
        )
        wrapped_instructions = (
            r22.BytecodeInstruction(r22.BytecodeOpcode.CALL, 2),
            r22.BytecodeInstruction(r22.BytecodeOpcode.HALT),
        ) + r22.rebase_instructions(subroutine, offset=2)

    return r22.BytecodeProgram(
        instructions=wrapped_instructions,
        name=(
            f"{base_program.name}_r26_u{spec.unique_address_target}_"
            f"h{r22.multiplier_label(spec.horizon_multiplier)}_"
            f"c{spec.checkpoint_depth}_k{spec.hot_address_skew}_seed{spec.seed_id}"
        ),
        memory_layout=base_program.memory_layout,
    )


def measure_branch_spec(spec: r22.BranchSpec):
    original_build_wrapped_program = r22.build_wrapped_program
    r22.build_wrapped_program = build_wrapped_program
    try:
        row, profile = _BASE_MEASURE_BRANCH_SPEC(spec)
    finally:
        r22.build_wrapped_program = original_build_wrapped_program
    row["source_runtime_stage"] = "r22_d0_true_boundary_localization_gate"
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
        reason = "R26 found a reproducible first failing candidate with at least one nearby exact supporting branch."
        next_priority_lane = "h23_refreeze_after_r26_r27_r28"
    elif first_fail is not None:
        lane_verdict = "near_boundary_mixed_signal_needs_confirmation"
        reason = "R26 found a near-boundary signal, but confirmation is still required before calling it localized."
        next_priority_lane = "r27_d0_boundary_localization_extension_gate"
    elif skipped_rows:
        lane_verdict = "resource_limited_before_localization"
        reason = "R26 did not find a failure before hitting the bounded reference-step cap."
        next_priority_lane = "h23_refreeze_after_r26_r27_r28"
    else:
        lane_verdict = "grid_extended_still_not_localized"
        reason = "Every executed R26 candidate stayed exact inside the first bounded post-H21 execution wave."
        next_priority_lane = "r27_d0_boundary_localization_extension_gate"

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
        "next_priority_lane": next_priority_lane,
    }


def build_summary(branch_specs: list[r22.BranchSpec], gate: dict[str, object]) -> dict[str, object]:
    return {
        "status": "r26_boundary_localization_execution_complete",
        "current_frozen_stage": "h21_refreeze_after_r22_r23",
        "source_runtime_stage": "r22_d0_true_boundary_localization_gate",
        "gate": gate,
        "planned_lane_classes": ["candidate_core", "first_wave_extension"],
        "planned_families": sorted({spec.family for spec in branch_specs}),
        "planned_unique_address_targets": sorted({spec.unique_address_target for spec in branch_specs}),
        "planned_horizon_multipliers": sorted({spec.horizon_multiplier for spec in branch_specs}),
        "planned_checkpoint_depths": sorted(
            {spec.checkpoint_depth for spec in branch_specs},
            key=r22.CHECKPOINT_DEPTH_ORDER.index,
        ),
        "planned_hot_address_skews": sorted(
            {spec.hot_address_skew for spec in branch_specs},
            key=r22.HOT_ADDRESS_SKEW_ORDER.index,
        ),
        "executed_family_count": len({spec.family for spec in branch_specs}),
        "recommended_next_action": (
            "Advance directly to H23 if the boundary is localized; otherwise run conditional R27 before refreezing."
        ),
        "supported_here": [
            "R26 stays on the fixed tiny typed-bytecode D0 endpoint and executes one explicit post-H21 manifest.",
            "R26 preserves positive rows, failure rows, branch summaries, and first-fail diagnostics in one machine-readable export.",
            "R26 keeps the boundary question separate from the mixed same-endpoint systems story.",
        ],
        "unsupported_here": [
            "R26 does not authorize a wider endpoint, a broader softmax-replacement thesis, or a broader 'LLMs are computers' claim.",
            "R26 does not reopen systems repair or frontend widening.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    admitted_rows = r22.load_r19_admitted_runtime_rows()
    template_registry = r22.build_template_registry(admitted_rows)
    branch_plans = build_branch_plans()
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
        OUT_DIR / "branch_manifest.json",
        {"experiment": "r26_branch_manifest", "environment": environment.as_dict(), "rows": manifest_rows},
    )
    r22.write_csv(OUT_DIR / "branch_manifest.csv", manifest_rows)
    r22.write_json(
        OUT_DIR / "boundary_rows.json",
        {"experiment": "r26_boundary_rows", "environment": environment.as_dict(), "rows": rows},
    )
    r22.write_csv(OUT_DIR / "boundary_rows.csv", rows)
    r22.write_json(
        OUT_DIR / "address_profiles.json",
        {"experiment": "r26_address_profiles", "environment": environment.as_dict(), "rows": profiles},
    )
    r22.write_json(
        OUT_DIR / "positive_rows.json",
        {"experiment": "r26_positive_rows", "environment": environment.as_dict(), "rows": [row for row in rows if bool(row["exact"])]},
    )
    r22.write_json(
        OUT_DIR / "failure_rows.json",
        {"experiment": "r26_failure_rows", "environment": environment.as_dict(), "rows": failure_rows},
    )
    r22.write_json(
        OUT_DIR / "skipped_rows.json",
        {"experiment": "r26_skipped_rows", "environment": environment.as_dict(), "rows": skipped_rows},
    )
    r22.write_json(
        OUT_DIR / "branch_summary.json",
        {"experiment": "r26_branch_summary", "environment": environment.as_dict(), "rows": branch_summary_rows},
    )
    r22.write_json(
        OUT_DIR / "first_fail_digest.json",
        {"experiment": "r26_first_fail_digest", "environment": environment.as_dict(), "rows": first_fail_digest_rows},
    )
    r22.write_json(
        OUT_DIR / "localized_boundary.json",
        {"experiment": "r26_localized_boundary", "environment": environment.as_dict(), "rows": localized_boundary_rows},
    )
    r22.write_json(
        OUT_DIR / "neighbor_exact_rows.json",
        {"experiment": "r26_neighbor_exact_rows", "environment": environment.as_dict(), "rows": neighbor_exact_rows},
    )
    r22.write_json(
        OUT_DIR / "failure_rechecks.json",
        {"experiment": "r26_failure_rechecks", "environment": environment.as_dict(), "rows": failure_rechecks},
    )
    r22.write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r26_d0_boundary_localization_execution_gate",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/H21_refreeze_after_r22_r23/summary.json",
                "docs/milestones/R24_d0_boundary_localization_zoom_followup/boundary_zoom_matrix.md",
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
