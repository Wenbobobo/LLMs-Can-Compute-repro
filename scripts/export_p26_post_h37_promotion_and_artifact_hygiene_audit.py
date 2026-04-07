"""Export the post-H37 promotion and artifact hygiene audit for P26."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P26_post_h37_promotion_and_artifact_hygiene_audit"


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


def artifact_status() -> tuple[str, int | None]:
    artifact = ROOT / "results" / "R20_d0_runtime_mechanism_ablation_matrix" / "probe_read_rows.json"
    if not artifact.exists():
        return ("not_present_on_current_source_branch", None)
    return ("present", artifact.stat().st_size)


def load_inputs() -> dict[str, Any]:
    branch_name = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    ahead_of_main = git_output(["rev-list", "--count", "main..HEAD"])
    diff_files = git_output(["diff", "--name-only", "main..HEAD"]).splitlines()
    artifact_state, artifact_size = artifact_status()
    return {
        "p26_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "README.md"
        ),
        "p26_status_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "status.md"
        ),
        "p26_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "todo.md"
        ),
        "p26_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "acceptance.md"
        ),
        "p26_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "artifact_index.md"
        ),
        "commit_split_manifest_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "commit_split_manifest.md"
        ),
        "main_delta_summary_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "main_delta_summary.md"
        ),
        "artifact_tracking_policy_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "artifact_tracking_policy.md"
        ),
        "worktree_runbook_text": read_text(
            ROOT / "docs" / "milestones" / "P26_post_h37_promotion_and_artifact_hygiene_audit" / "worktree_runbook.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-23-post-h37-f16-h38-p26-candidate-isolation-design.md"),
        "h38_summary": read_json(
            ROOT / "results" / "H38_post_f16_runtime_relevance_reopen_decision_packet" / "summary.json"
        ),
        "h37_summary": read_json(ROOT / "results" / "H37_post_h36_runtime_relevance_decision_packet" / "summary.json"),
        "p25_summary": read_json(ROOT / "results" / "P25_post_h36_clean_promotion_prep" / "summary.json"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "branch_name": branch_name,
        "ahead_of_main_commit_count": int(ahead_of_main),
        "ahead_of_main_file_count": len([item for item in diff_files if item.strip()]),
        "artifact_state": artifact_state,
        "artifact_size": artifact_size,
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h38 = inputs["h38_summary"]["summary"]
    p25 = inputs["p25_summary"]["summary"]
    return [
        {
            "item_id": "p26_docs_fix_audit_only_posture_and_current_clean_branch",
            "status": "pass"
            if contains_all(
                inputs["p26_readme_text"],
                [
                    "operational audit lane after the completed `f16 -> h38` docs-only control wave",
                    "inventory the delta against dirty `main`",
                    "classify large raw artifacts",
                ],
            )
            and contains_all(
                inputs["p26_status_text"],
                [
                    "completed operational promotion/artifact audit after `h38`",
                    "`wip/f16-h38-p26-exec`",
                    "`wip/p25-f15-h37-exec`",
                    "`audit_only`",
                ],
            )
            and contains_all(
                inputs["p26_todo_text"],
                [
                    "current clean audit branch",
                    "`audit_only` promotion policy",
                    "large-artifact policy",
                    "merge-by-momentum and runtime widening",
                ],
            )
            and contains_all(
                inputs["p26_acceptance_text"],
                [
                    "`commit_split_manifest.md`",
                    "`main_delta_summary.md`",
                    "`artifact_tracking_policy.md`",
                    "without authorizing it now",
                ],
            )
            else "blocked",
            "notes": "P26 should stay operational-only, fix the clean audit branch, and keep promotion at audit_only.",
        },
        {
            "item_id": "p26_manifest_delta_and_artifact_policy_keep_main_untouched",
            "status": "pass"
            if contains_all(
                inputs["commit_split_manifest_text"],
                [
                    "origin-core-runtime-history",
                    "candidate-isolation-control-wave",
                    "defer-main-until-clean",
                    "do not force-merge",
                ],
            )
            and contains_all(
                inputs["main_delta_summary_text"],
                [
                    "current comparison target",
                    "main",
                    "wip/f16-h38-p26-exec",
                    "audit_only",
                ],
            )
            and contains_all(
                inputs["artifact_tracking_policy_text"],
                [
                    "probe_read_rows.json",
                    "not present on",
                    ".gitignore",
                    "replace_with_compact_summary",
                ],
            )
            and contains_all(
                inputs["worktree_runbook_text"],
                [
                    "wip/f16-h38-p26-exec",
                    "git diff --stat main..wip/f16-h38-p26-exec",
                    "reconcile or isolate dirty `main` work before any promotion attempt",
                    "r41",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "p26 scope",
                    "keep `main` untouched in this wave",
                    "large-artifact policy",
                    "authorize a merge by momentum",
                ],
            )
            else "blocked",
            "notes": "The P26 audit must encode packetized promotion guidance and keep artifact classification separate from scientific widening.",
        },
        {
            "item_id": "driver_wave_and_prior_support_treat_p26_as_completed_audit_not_merge_authorization",
            "status": "pass"
            if inputs["branch_name"] == "wip/f16-h38-p26-exec"
            and str(h38["active_stage"]) == "h38_post_f16_runtime_relevance_reopen_decision_packet"
            and str(p25["promotion_mode"]) == "prepare_only"
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "p26_post_h37_promotion_and_artifact_hygiene_audit",
                    "promotion_mode = audit_only",
                    "merge_recommended = false",
                    "h38_post_f16_runtime_relevance_reopen_decision_packet",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "p26_post_h37_promotion_and_artifact_hygiene_audit",
                    "wip/f16-h38-p26-exec",
                    "audit_only",
                    "h38_post_f16_runtime_relevance_reopen_decision_packet",
                    "no_active_downstream_runtime_lane",
                ],
            )
            and contains_all(
                inputs["p26_artifact_index_text"],
                [
                    "results/p26_post_h37_promotion_and_artifact_hygiene_audit/summary.json",
                    "results/h38_post_f16_runtime_relevance_reopen_decision_packet/summary.json",
                    "results/h37_post_h36_runtime_relevance_decision_packet/summary.json",
                    "results/p25_post_h36_clean_promotion_prep/summary.json",
                ],
            )
            else "blocked",
            "notes": "The entry surfaces should present P26 as a completed operational audit above H38, not as merge authorization.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h38 = inputs["h38_summary"]["summary"]
    h37 = inputs["h37_summary"]["summary"]
    p25 = inputs["p25_summary"]["summary"]
    return [
        {
            "source": "results/H38_post_f16_runtime_relevance_reopen_decision_packet/summary.json",
            "fields": {
                "active_stage": h38["active_stage"],
                "selected_outcome": h38["selected_outcome"],
                "decision_basis": h38["decision_basis"],
            },
        },
        {
            "source": "results/H37_post_h36_runtime_relevance_decision_packet/summary.json",
            "fields": {
                "active_stage": h37["active_stage"],
                "selected_outcome": h37["selected_outcome"],
                "decision_basis": h37["decision_basis"],
            },
        },
        {
            "source": "docs/milestones/P26_post_h37_promotion_and_artifact_hygiene_audit/artifact_tracking_policy.md",
            "fields": {
                "branch_name": inputs["branch_name"],
                "ahead_of_main_commit_count": inputs["ahead_of_main_commit_count"],
                "ahead_of_main_file_count": inputs["ahead_of_main_file_count"],
                "artifact_state": inputs["artifact_state"],
                "artifact_size": inputs["artifact_size"],
                "preserved_prior_promotion_mode": p25["promotion_mode"],
            },
        },
    ]


def build_summary(checklist_rows: list[dict[str, object]], inputs: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "p26_post_h37_promotion_and_artifact_hygiene_audit_complete",
        "active_stage": "p26_post_h37_promotion_and_artifact_hygiene_audit",
        "current_clean_audit_branch": "wip/f16-h38-p26-exec",
        "current_clean_audit_worktree": "D:/zWenbo/AI/LLMCompute-worktrees/f16-h38-p26-exec",
        "preserved_prior_clean_source_branch": "wip/p25-f15-h37-exec",
        "target_branch": "main",
        "promotion_mode": "audit_only",
        "merge_recommended": False,
        "current_decision_packet": "h38_post_f16_runtime_relevance_reopen_decision_packet",
        "preserved_prior_decision_packet": "h37_post_h36_runtime_relevance_decision_packet",
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
