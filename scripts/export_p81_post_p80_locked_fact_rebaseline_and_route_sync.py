"""Export the post-P80 locked-fact rebaseline and route-sync sidecar for P81."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P81_post_p80_locked_fact_rebaseline_and_route_sync"
P80_SUMMARY_PATH = ROOT / "results" / "P80_post_p79_next_planmode_handoff_sync" / "summary.json"
PREFLIGHT_SUMMARY_PATH = ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
P10_SUMMARY_PATH = ROOT / "results" / "P10_submission_archive_ready" / "summary.json"
ROOT_README_PATH = ROOT / "README.md"
STATUS_PATH = ROOT / "STATUS.md"
DOCS_README_PATH = ROOT / "docs" / "README.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"
CURRENT_STAGE_DRIVER_PATH = ROOT / "docs" / "publication_record" / "current_stage_driver.md"
BRANCH_REGISTRY_PATH = ROOT / "docs" / "branch_worktree_registry.md"
PLANS_README_PATH = ROOT / "docs" / "plans" / "README.md"
MILESTONES_README_PATH = ROOT / "docs" / "milestones" / "README.md"
PLAN_DESIGN_PATH = ROOT / "docs" / "plans" / "2026-04-07-post-p80-clean-descendant-promotion-prep-design.md"
POST_P80_HANDOFF_PATH = ROOT / "docs" / "plans" / "2026-04-05-post-p80-next-planmode-handoff.md"
POST_P80_STARTUP_PATH = ROOT / "docs" / "plans" / "2026-04-05-post-p80-next-planmode-startup-prompt.md"
POST_P80_BRIEF_PATH = ROOT / "docs" / "plans" / "2026-04-05-post-p80-next-planmode-brief-prompt.md"
CURRENT_BRANCH = "wip/p81-post-p80-clean-descendant-promotion-prep"
PUBLISHED_BRANCH = "wip/p75-post-p74-published-successor-freeze"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def current_branch() -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"])


def branch_head(branch: str) -> str:
    return git_output(["rev-parse", "--short", branch])


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p80_summary = read_json(P80_SUMMARY_PATH)["summary"]
    if p80_summary["selected_outcome"] != "next_planmode_handoff_synced_to_explicit_stop_after_p79":
        raise RuntimeError("P81 expects the landed P80 handoff-sync sidecar.")

    preflight_summary = read_json(PREFLIGHT_SUMMARY_PATH)["summary"]
    p10_summary = read_json(P10_SUMMARY_PATH)["summary"]
    root_readme_text = read_text(ROOT_README_PATH)
    status_text = read_text(STATUS_PATH)
    docs_readme_text = read_text(DOCS_README_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)
    current_stage_driver_text = read_text(CURRENT_STAGE_DRIVER_PATH)
    branch_registry_text = read_text(BRANCH_REGISTRY_PATH)
    plans_readme_text = read_text(PLANS_README_PATH)
    milestones_readme_text = read_text(MILESTONES_README_PATH)
    plan_design_text = read_text(PLAN_DESIGN_PATH)
    handoff_text = read_text(POST_P80_HANDOFF_PATH)
    startup_text = read_text(POST_P80_STARTUP_PATH)
    brief_text = read_text(POST_P80_BRIEF_PATH)
    current_branch_name = current_branch()
    published_head = branch_head(PUBLISHED_BRANCH)

    checklist_rows = [
        {"item_id": "p81_reads_p80", "status": "pass", "notes": "P81 starts only after the landed P80 handoff-sync sidecar."},
        {
            "item_id": "p81_runs_on_current_execution_branch",
            "status": "pass" if current_branch_name == CURRENT_BRANCH else "blocked",
            "notes": "The locked-fact rebaseline should run on the dedicated p81 execution branch.",
        },
        {
            "item_id": "p81_prompts_record_current_p75_head_and_green_audits",
            "status": "pass"
            if all(
                (
                    contains_all(handoff_text, [PUBLISHED_BRANCH, published_head, "docs_and_audits_green", "archive_ready", "explicit stop", "no further action"]),
                    contains_all(startup_text, [PUBLISHED_BRANCH, published_head, "docs_and_audits_green", "archive_ready", "explicit stop", "no further action"]),
                    contains_all(brief_text, [PUBLISHED_BRANCH, published_head, "docs_and_audits_green", "archive_ready", "explicit stop", "no further action"]),
                )
            )
            else "blocked",
            "notes": "The post-P80 prompts should record the current published p75 head and the green standing audits.",
        },
        {
            "item_id": "p81_top_level_and_router_surfaces_expose_current_phase",
            "status": "pass"
            if all(
                (
                    contains_all(root_readme_text, ["P81_post_p80_locked_fact_rebaseline_and_route_sync", CURRENT_BRANCH, PUBLISHED_BRANCH, "53962ca"]),
                    contains_all(status_text, ["P81_post_p80_locked_fact_rebaseline_and_route_sync", CURRENT_BRANCH, PUBLISHED_BRANCH, "docs_and_audits_green", "archive_ready"]),
                    contains_all(docs_readme_text, ["H65 + P81 + P77/P78/P79/P80", "publication_record/current_stage_driver.md", "branch_worktree_registry.md"]),
                    contains_all(publication_readme_text, ["P81_post_p80_locked_fact_rebaseline_and_route_sync", CURRENT_BRANCH, "2026-04-07-post-p80-clean-descendant-promotion-prep-design.md"]),
                )
            )
            else "blocked",
            "notes": "Top-level docs and routers should expose P81 as the current locked-fact and promotion-prep phase.",
        },
        {
            "item_id": "p81_driver_and_registry_expose_execution_and_merge_rules",
            "status": "pass"
            if all(
                (
                    contains_all(
                        current_stage_driver_text,
                        [
                            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
                            CURRENT_BRANCH,
                            PUBLISHED_BRANCH,
                            "53962ca",
                            "docs_and_audits_green",
                            "archive_ready",
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                    contains_all(
                        branch_registry_text,
                        [
                            CURRENT_BRANCH,
                            PUBLISHED_BRANCH,
                            "p81`, `p75`, `p74`, `p73`, `p72`, `p69`, and `p56",
                            "clean_descendant_only_never_dirty_root_main",
                            f"origin/main...{CURRENT_BRANCH}",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "The current-stage driver and branch registry should expose the p81 execution branch and keep dirty-root integration out of bounds.",
        },
        {
            "item_id": "p81_design_and_indices_include_current_wave",
            "status": "pass"
            if all(
                (
                    contains_all(plan_design_text, ["P81_post_p80_locked_fact_rebaseline_and_route_sync", "P82_post_p81_clean_main_promotion_probe", "P83_post_p82_promotion_branch_and_pr_handoff", "P84_post_p83_keep_set_contraction_and_closeout"]),
                    contains_all(plans_readme_text, ["2026-04-07-post-p80-clean-descendant-promotion-prep-design.md", "P81_post_p80_locked_fact_rebaseline_and_route_sync", CURRENT_BRANCH]),
                    contains_all(milestones_readme_text, ["P81_post_p80_locked_fact_rebaseline_and_route_sync", "P77_post_p76_keep_set_and_provenance_normalization", "P81"]),
                )
            )
            else "blocked",
            "notes": "The design and the plan/milestone routers should expose the P81 phase as current.",
        },
        {
            "item_id": "p81_standing_release_and_archive_audits_remain_green",
            "status": "pass"
            if preflight_summary["preflight_state"] == "docs_and_audits_green" and p10_summary["packet_state"] == "archive_ready"
            else "blocked",
            "notes": "The standing release-preflight and archive-ready audits should remain green during the rebaseline.",
        },
    ]

    claim_packet = {
        "supports": [
            "P81 rebaselines the locked facts after P80 to the published p75 head 53962ca.",
            "P81 keeps release_preflight green and P10 archive_ready while opening clean-descendant promotion-prep only.",
            "P81 leaves runtime closed and dirty-root integration out of bounds.",
        ],
        "does_not_support": ["runtime reopen", "dirty-root integration", "same-lane executor-value reopen"],
        "distilled_result": {
            "current_locked_fact_wave": "p81_post_p80_locked_fact_rebaseline_and_route_sync",
            "current_execution_branch": CURRENT_BRANCH,
            "published_branch": PUBLISHED_BRANCH,
            "published_branch_head": published_head,
            "preflight_state": preflight_summary["preflight_state"],
            "archive_ready_state": p10_summary["packet_state"],
            "selected_outcome": "locked_facts_rebaselined_and_route_synced_after_p80",
            "next_required_lane": "p82_clean_main_promotion_probe",
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
            {"field": "current_branch", "value": current_branch_name},
            {"field": "published_branch_head", "value": published_head},
            {"field": "preflight_state", "value": preflight_summary["preflight_state"]},
            {"field": "archive_ready_state", "value": p10_summary["packet_state"]},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
