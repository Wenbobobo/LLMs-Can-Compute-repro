"""Export the post-H41 clean promotion and explicit merge packet for P27."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet"
SOURCE_BRANCH = "wip/h41-r43-mainline"
SOURCE_WORKTREE = "D:/zWenbo/AI/LLMCompute-worktrees/h41-r43-mainline"
MERGE_BRANCH = "wip/p27-promotion-merge"
MERGE_WORKTREE = "D:/zWenbo/AI/LLMCompute-worktrees/p27-promotion-merge"
TARGET_BRANCH = "main"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def git_output_optional(args: list[str]) -> str:
    try:
        return git_output(args)
    except subprocess.CalledProcessError:
        return ""


def artifact_status() -> tuple[str, int | None]:
    artifact = ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "probe_read_rows.json"
    if not artifact.exists():
        return ("not_present_on_current_source_branch", None)
    return ("present", artifact.stat().st_size)


def load_inputs() -> dict[str, Any]:
    branch_name = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    source_commit = git_output(["rev-parse", SOURCE_BRANCH])
    source_origin_commit = git_output_optional(["rev-parse", f"origin/{SOURCE_BRANCH}"])
    ahead_of_main = git_output(["rev-list", "--count", f"{TARGET_BRANCH}..{SOURCE_BRANCH}"])
    diff_files = git_output(["diff", "--name-only", f"{TARGET_BRANCH}..{SOURCE_BRANCH}"]).splitlines()
    artifact_state, artifact_size = artifact_status()
    return {
        "p27_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "README.md"
        ),
        "p27_status_text": read_text(
            ROOT / "docs" / "milestones" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "status.md"
        ),
        "p27_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "todo.md"
        ),
        "p27_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "acceptance.md"
        ),
        "p27_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "artifact_index.md"
        ),
        "merge_wave_manifest_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "P27_post_h41_clean_promotion_and_explicit_merge_packet"
            / "merge_wave_manifest.md"
        ),
        "main_delta_summary_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "P27_post_h41_clean_promotion_and_explicit_merge_packet"
            / "main_delta_summary.md"
        ),
        "artifact_tracking_policy_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "P27_post_h41_clean_promotion_and_explicit_merge_packet"
            / "artifact_tracking_policy.md"
        ),
        "worktree_runbook_text": read_text(
            ROOT
            / "docs"
            / "milestones"
            / "P27_post_h41_clean_promotion_and_explicit_merge_packet"
            / "worktree_runbook.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h41-p27-explicit-merge-wave-design.md"),
        "h41_summary": read_json(ROOT / "results" / "H41_post_r42_aggressive_long_arc_decision_packet" / "summary.json"),
        "f20_summary": read_json(ROOT / "results" / "F20_post_r42_dual_mode_model_mainline_bundle" / "summary.json"),
        "p26_summary": read_json(
            ROOT / "results" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "summary.json"
        ),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "branch_name": branch_name,
        "ahead_of_main_commit_count": int(ahead_of_main),
        "ahead_of_main_file_count": len([item for item in diff_files if item.strip()]),
        "artifact_state": artifact_state,
        "artifact_size": artifact_size,
        "source_branch_commit": source_commit,
        "source_branch_origin_commit": source_origin_commit,
        "source_branch_synced_to_origin": bool(source_origin_commit) and source_origin_commit == source_commit,
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h41 = inputs["h41_summary"]["summary"]
    f20 = inputs["f20_summary"]["summary"]
    p26 = inputs["p26_summary"]["summary"]
    return [
        {
            "item_id": "p27_docs_fix_operational_explicit_merge_posture_without_merging_main",
            "status": "pass"
            if contains_all(
                inputs["p27_readme_text"],
                [
                    "completed operational merge packet",
                    "wip/h41-r43-mainline",
                    "wip/p27-promotion-merge",
                    "does not merge `main`",
                ],
            )
            and contains_all(
                inputs["p27_status_text"],
                [
                    "completed operational explicit merge packet after `h41`",
                    "wip/h41-r43-mainline",
                    "wip/p27-promotion-merge",
                    "`promotion_mode = explicit_merge_wave`",
                    "`merge_executed = false`",
                ],
            )
            and contains_all(
                inputs["p27_todo_text"],
                [
                    "clean post-`h41` source branch",
                    "reviewable merge set",
                    "keep `main` untouched",
                    "keep `r43` and `r45` execution in their own downstream worktrees",
                ],
            )
            and contains_all(
                inputs["p27_acceptance_text"],
                [
                    "operational rather than scientific",
                    "clean source branch and explicit merge branch",
                    "`r43` stays the next exact gate",
                    "`merge_executed` remains false",
                ],
            )
            and contains_all(
                inputs["p27_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-h41-p27-explicit-merge-wave-design.md",
                    "docs/publication_record/current_stage_driver.md",
                    "tmp/active_wave_plan.md",
                    "results/p27_post_h41_clean_promotion_and_explicit_merge_packet/summary.json",
                    "results/h41_post_r42_aggressive_long_arc_decision_packet/summary.json",
                ],
            )
            else "blocked",
            "notes": "P27 should stay operational-only, preserve the clean source branch, and keep merge execution false.",
        },
        {
            "item_id": "p27_manifest_delta_and_artifact_policy_keep_main_untouched_and_merge_explicit",
            "status": "pass"
            if contains_all(
                inputs["merge_wave_manifest_text"],
                [
                    "clean scientific source branch: `wip/h41-r43-mainline`",
                    "explicit merge packet branch: `wip/p27-promotion-merge`",
                    "target branch: `main`",
                    "`promotion_mode = explicit_merge_wave`",
                    "`merge_recommended = false`",
                    "no direct merge inside `p27`",
                ],
            )
            and contains_all(
                inputs["main_delta_summary_text"],
                [
                    "current comparison target remains `main`",
                    "wip/h41-r43-mainline",
                    "exact commit and file counts are captured",
                    "do not treat this delta inventory as authorization to",
                    "execute `r43`",
                    "execute `r45`",
                ],
            )
            and contains_all(
                inputs["artifact_tracking_policy_text"],
                [
                    "probe_read_rows.json",
                    "not present on the current clean source branch",
                    "stay outside the `p27` merge set",
                    "no `.gitignore` change is authorized inside `p27` alone",
                ],
            )
            and contains_all(
                inputs["worktree_runbook_text"],
                [
                    "start from `wip/p27-promotion-merge`, not dirty `main`",
                    "fast-forward from `wip/h41-r43-mainline`",
                    "confirm `wip/h41-r43-mainline` is synced to",
                    "inspect `git diff --stat main..wip/h41-r43-mainline`",
                    "do not execute `r43` or `r45` inside `p27`",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p27_post_h41_clean_promotion_and_explicit_merge_packet` is the operational",
                    "`wip/h41-r43-mainline`",
                    "`wip/p27-promotion-merge`",
                    "keep dirty `main` out of the control surface",
                    "does not merge `main`, does not execute `r43`, and does not execute `r45`",
                ],
            )
            else "blocked",
            "notes": "The merge manifest must encode explicit merge posture, review conditions, and large-artifact isolation without touching main.",
        },
        {
            "item_id": "driver_wave_and_control_surfaces_treat_p27_as_completed_operational_merge_packet",
            "status": "pass"
            if inputs["branch_name"] == MERGE_BRANCH
            and inputs["source_branch_synced_to_origin"] is True
            and str(h41["active_stage"]) == "h41_post_r42_aggressive_long_arc_decision_packet"
            and str(f20["model_mainline_posture"]) == "coequal_mainline_exact_non_substitutive"
            and str(p26["promotion_mode"]) == "audit_only"
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "completed operational explicit merge packet",
                    "p27_post_h41_clean_promotion_and_explicit_merge_packet",
                    "preserved prior operational promotion/artifact audit lane",
                    "p26_post_h37_promotion_and_artifact_hygiene_audit",
                    "`merge_executed = false`",
                    "the next required order is now:",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "completed operational explicit merge packet:",
                    "`p27_post_h41_clean_promotion_and_explicit_merge_packet`",
                    "`wip/h41-r43-mainline`",
                    "`wip/p27-promotion-merge`",
                    "`r43_origin_bounded_memory_small_vm_execution_gate`",
                    "`r45_origin_dual_mode_model_mainline_gate`",
                ],
            )
            and contains_all(
                inputs["p27_artifact_index_text"],
                [
                    "results/f20_post_r42_dual_mode_model_mainline_bundle/summary.json",
                    "results/p26_post_h37_promotion_and_artifact_hygiene_audit/summary.json",
                ],
            )
            else "blocked",
            "notes": "The entry surfaces should present P27 as a completed operational merge packet while leaving H41 as the active scientific control packet.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h41 = inputs["h41_summary"]["summary"]
    f20 = inputs["f20_summary"]["summary"]
    return [
        {
            "source": "results/H41_post_r42_aggressive_long_arc_decision_packet/summary.json",
            "fields": {
                "active_stage": h41["active_stage"],
                "selected_outcome": h41["selected_outcome"],
                "explicit_merge_packet": h41["explicit_merge_packet"],
            },
        },
        {
            "source": "results/F20_post_r42_dual_mode_model_mainline_bundle/summary.json",
            "fields": {
                "active_stage": f20["active_stage"],
                "model_mainline_posture": f20["model_mainline_posture"],
                "decisive_exact_next_gate": f20["decisive_exact_next_gate"],
                "authorized_future_model_gate": f20["authorized_future_model_gate"],
            },
        },
        {
            "source": "docs/milestones/P27_post_h41_clean_promotion_and_explicit_merge_packet/merge_wave_manifest.md",
            "fields": {
                "branch_name": inputs["branch_name"],
                "source_branch_synced_to_origin": inputs["source_branch_synced_to_origin"],
                "ahead_of_main_commit_count": inputs["ahead_of_main_commit_count"],
                "ahead_of_main_file_count": inputs["ahead_of_main_file_count"],
                "artifact_state": inputs["artifact_state"],
                "artifact_size": inputs["artifact_size"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], inputs: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "p27_post_h41_clean_promotion_and_explicit_merge_packet_complete",
        "active_stage": "p27_post_h41_clean_promotion_and_explicit_merge_packet",
        "current_clean_source_branch": SOURCE_BRANCH,
        "current_clean_source_worktree": SOURCE_WORKTREE,
        "explicit_merge_branch": MERGE_BRANCH,
        "explicit_merge_worktree": MERGE_WORKTREE,
        "preserved_prior_clean_audit_branch": "wip/f16-h38-p26-exec",
        "target_branch": TARGET_BRANCH,
        "promotion_mode": "explicit_merge_wave",
        "merge_recommended": False,
        "merge_executed": False,
        "source_branch_synced_to_origin": inputs["source_branch_synced_to_origin"],
        "current_decision_packet": "h41_post_r42_aggressive_long_arc_decision_packet",
        "current_model_mainline_bundle": "f20_post_r42_dual_mode_model_mainline_bundle",
        "authorized_exact_runtime_candidate": "r43_origin_bounded_memory_small_vm_execution_gate",
        "authorized_model_runtime_candidate": "r45_origin_dual_mode_model_mainline_gate",
        "next_required_lane": "r43_origin_bounded_memory_small_vm_execution_gate",
        "ahead_of_main_commit_count": inputs["ahead_of_main_commit_count"],
        "ahead_of_main_file_count": inputs["ahead_of_main_file_count"],
        "artifact_state": inputs["artifact_state"],
        "artifact_size": inputs["artifact_size"],
        "supported_here_count": 0,
        "unsupported_here_count": 0,
        "disconfirmed_here_count": 0,
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot})
    write_json(
        OUT_DIR / "summary.json",
        {
            "summary": summary,
            "runtime_environment": environment_payload(),
        },
    )


if __name__ == "__main__":
    main()
