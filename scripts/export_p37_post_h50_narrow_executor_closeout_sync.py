"""Export the post-H50 narrow executor closeout sync packet for P37."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P37_post_h50_narrow_executor_closeout_sync"
LARGE_ARTIFACT_THRESHOLD_BYTES = 10 * 1024 * 1024
RAW_ROW_IGNORE_PATTERNS = [
    "results/**/probe_read_rows.json",
    "results/**/per_read_rows.json",
    "results/**/trace_rows.json",
    "results/**/step_rows.json",
]


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles) and line not in seen:
            hits.append(line)
            seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def git_output(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def collect_tracked_large_artifacts(
    root: Path = ROOT,
    *,
    tracked_paths: list[str] | None = None,
    threshold_bytes: int = LARGE_ARTIFACT_THRESHOLD_BYTES,
) -> list[dict[str, object]]:
    if tracked_paths is None:
        tracked_paths = [path for path in git_output(["ls-files", "-z"]).split("\0") if path]

    oversized: list[dict[str, object]] = []
    for rel_path in tracked_paths:
        path = root / rel_path
        if not path.exists() or not path.is_file():
            continue
        size_bytes = path.stat().st_size
        if size_bytes < threshold_bytes:
            continue
        oversized.append(
            {
                "path": rel_path.replace("\\", "/"),
                "size_bytes": size_bytes,
                "size_mib": round(size_bytes / (1024 * 1024), 2),
            }
        )
    return sorted(oversized, key=lambda row: (int(row["size_bytes"]), str(row["path"])), reverse=True)


def load_inputs() -> dict[str, Any]:
    tracked_large_artifacts = collect_tracked_large_artifacts()
    return {
        "p37_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "README.md"
        ),
        "p37_status_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "status.md"
        ),
        "p37_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "todo.md"
        ),
        "p37_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "acceptance.md"
        ),
        "p37_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "artifact_index.md"
        ),
        "worktree_strategy_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "worktree_strategy.md"
        ),
        "artifact_policy_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "artifact_policy.md"
        ),
        "commit_cadence_text": read_text(
            ROOT / "docs" / "milestones" / "P37_post_h50_narrow_executor_closeout_sync" / "commit_cadence.md"
        ),
        "gitignore_text": read_text(ROOT / ".gitignore"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h50_summary": read_json(ROOT / "results" / "H50_post_r51_r52_scope_decision_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "h51_summary": read_json(ROOT / "results" / "H51_post_h50_origin_mechanism_reentry_packet" / "summary.json"),
        "h52_summary": read_json(ROOT / "results" / "H52_post_r55_r56_r57_origin_mechanism_decision_packet" / "summary.json"),
        "r57_summary": read_json(ROOT / "results" / "R57_origin_accelerated_trace_vm_comparator_gate" / "summary.json"),
        "tracked_large_artifacts": tracked_large_artifacts,
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h50 = inputs["h50_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    h51 = inputs["h51_summary"]["summary"]
    h52 = inputs["h52_summary"]["summary"]
    r57 = inputs["r57_summary"]["summary"]
    return [
        {
            "item_id": "p37_docs_define_post_h50_hygiene_sync_packet",
            "status": "pass"
            if contains_all(
                inputs["p37_readme_text"],
                [
                    "completed low-priority operational/docs sync packet",
                    "`h51` as the preserved prior mechanism-reentry packet",
                    "`h52` as the current active docs-only closeout",
                    "`h50` as the preserved prior broader-route closeout",
                    "`h43` as the paper-grade endpoint",
                    "`f28 -> h51 -> r55 -> r56 -> r57 -> h52`",
                ],
            )
            and contains_all(
                inputs["p37_status_text"],
                [
                    "completed operational/docs sync packet after landed `h50` and landed `h51`",
                    "preserves `h52` as the current active docs-only closeout",
                    "preserves `h51` as the preserved prior mechanism-reentry packet",
                    "preserves the clean `f28/h51` worktree as the historical control surface for the closed wave",
                    "keeps descendant clean worktrees as the only scientific execution surfaces for `r55`, `r56`, and `r57`",
                    "keeps `merge_executed = false` explicit",
                    "codifies compact-summary-in-git and raw-row-dump-out-of-git defaults",
                    ".gitignore`-backed raw-row ignore rules",
                    "zero tracked `>=10 mib` artifacts in the clean worktree",
                ],
            )
            and contains_all(
                inputs["p37_todo_text"],
                [
                    "record one clean control-worktree strategy",
                    "record clean descendant execution-worktree rules for `r55` and `r56`",
                    "record one artifact policy",
                    "record one commit cadence",
                    "keep `.gitignore` carrying the concrete raw-row ignore rules",
                    "keep row-level artifacts above roughly `10 mib` out of git",
                ],
            )
            and contains_all(
                inputs["p37_acceptance_text"],
                [
                    "`p37` remains operational/docs-only",
                    "`h52` remains the current active docs-only packet",
                    "`h51` remains the preserved prior mechanism-reentry packet",
                    "raw step rows, trace rows, per-read rows, and artifacts above roughly",
                    ".gitignore` carries the concrete raw-row ignore rules",
                    "clean worktree tracks no artifacts at or above roughly `10 mib`",
                    "compact summaries, manifests, stop rules, and first-fail digests stay in git",
                    "merge back to `main` does not occur during the closed wave",
                ],
            )
            else "blocked",
            "notes": "P37 should codify hygiene and no-merge policy for the closed mechanism-reentry wave without changing scientific stage.",
        },
        {
            "item_id": "p37_records_worktree_artifact_and_commit_policy",
            "status": "pass"
            if contains_all(
                inputs["worktree_strategy_text"],
                [
                    "f28-h51-post-h50-origin-mechanism-reentry",
                    "r55-origin-2d-hardmax-retrieval-equivalence",
                    "r56-origin-append-only-trace-vm-semantics",
                    "r57-origin-accelerated-trace-vm-comparator",
                    "dirty root `main` is not a scientific execution surface",
                    "`r57` forks only after `r56` fixes an exact row set worth comparing",
                ],
            )
            and contains_all(
                inputs["artifact_policy_text"],
                [
                    "compact summaries, checklists, manifests, stop rules, first-fail digests",
                    "`probe_read_rows.json`",
                    "`per_read_rows.json`",
                    "`.gitignore` carries the concrete raw-row ignore patterns",
                    "any artifact above roughly `10 mib` should be treated as out-of-git",
                    "clean worktrees should track no artifacts at or above roughly `10 mib`",
                    "git lfs remains inactive by default",
                ],
            )
            and contains_all(
                inputs["commit_cadence_text"],
                [
                    "commit `f28` planning surfaces separately",
                    "commit `h51` docs-only control surfaces separately from `p37` hygiene surfaces",
                    "commit `r55` exact retrieval-equivalence outputs separately from `r56` trace-semantics outputs",
                    "commit `r57` comparator outputs separately from `h52` decision surfaces",
                ],
            )
            and contains_all(
                inputs["p37_artifact_index_text"],
                [
                    "docs/milestones/p37_post_h50_narrow_executor_closeout_sync/worktree_strategy.md",
                    "docs/milestones/p37_post_h50_narrow_executor_closeout_sync/artifact_policy.md",
                    "docs/milestones/p37_post_h50_narrow_executor_closeout_sync/commit_cadence.md",
                    ".gitignore",
                    "results/p37_post_h50_narrow_executor_closeout_sync/summary.json",
                ],
            )
            else "blocked",
            "notes": "P37 should make the worktree policy, large-artifact policy, and commit cadence explicit for this wave.",
        },
        {
            "item_id": "p37_repo_state_matches_large_artifact_policy",
            "status": "pass"
            if contains_all(inputs["gitignore_text"], RAW_ROW_IGNORE_PATTERNS)
            and not inputs["tracked_large_artifacts"]
            else "blocked",
            "notes": "The clean worktree should enforce raw-row ignore rules and keep tracked artifacts under the roughly 10 MiB default limit.",
        },
        {
            "item_id": "shared_control_surfaces_make_p37_current_low_priority_wave",
            "status": "pass"
            if str(h50["selected_outcome"]) == "stop_as_exact_without_system_value"
            and str(h51["selected_outcome"]) == "authorize_origin_mechanism_reentry_through_r55_first"
            and str(h52["selected_outcome"]) == "freeze_origin_mechanism_supported_without_fastpath_value"
            and str(h52["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(r57["gate"]["lane_verdict"]) == "accelerated_trace_vm_lacks_bounded_value"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and bool(h43["merge_executed"]) is False
            and contains_all(
                inputs["readme_text"],
                [
                    "current low-priority operational/docs wave:",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "raw row dumps and artifacts above roughly `10 mib` stay out of git by",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current low-priority operational/docs wave remains",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "dirty root `main` remains quarantined and `merge_executed = false` remains",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current low-priority operational/docs wave is:",
                    "- `p37_post_h50_narrow_executor_closeout_sync`",
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`p37_post_h50_narrow_executor_closeout_sync` remains the current low-priority",
                    "out-of-git policy for row dumps and artifacts above roughly `10 mib`",
                    "no merge back to `main` occurs during this wave",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h50` `f28/h51/p37` mechanism reentry wave",
                    "new `scripts/export_p37_post_h50_narrow_executor_closeout_sync.py`",
                    "new `results/p37_post_h50_narrow_executor_closeout_sync/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared control docs should expose P37 as the current low-priority wave and keep no-merge posture explicit.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "P37 promotes the clean F28/H51 worktree as the control surface for the current wave.",
            "P37 keeps descendant clean worktrees as the only scientific execution surfaces for R55, R56, and R57.",
            "P37 keeps raw row dumps and artifacts above roughly 10 MiB out of git by default while preserving explicit no-merge posture.",
            "P37 can now audit that the clean worktree keeps the raw-row ignore rules in .gitignore and tracks no artifacts at or above roughly 10 MiB.",
        ],
        "unsupported_here": [
            "P37 does not change the active scientific stage or overturn H50.",
            "P37 does not merge dirty root main back into the clean line.",
            "P37 does not reopen a downstream runtime lane after the landed H52 closeout.",
        ],
        "disconfirmed_here": [
            "The idea that convenience alone is enough reason to keep large raw row artifacts in git or to execute science from dirty root main.",
        ],
        "distilled_result": {
            "current_active_stage": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "preserved_prior_docs_only_closeout": "h50_post_r51_r52_scope_decision_packet",
            "preserved_prior_mechanism_reentry_packet": "h51_post_h50_origin_mechanism_reentry_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "refresh_packet": "p37_post_h50_narrow_executor_closeout_sync",
            "selected_outcome": "mechanism_reentry_hygiene_preserved_through_h52_closeout",
            "current_low_priority_wave": "p37_post_h50_narrow_executor_closeout_sync",
            "current_planning_bundle": "f28_post_h50_origin_mechanism_reentry_bundle",
            "preserved_comparator_gate": "r57_origin_accelerated_trace_vm_comparator_gate",
            "current_merge_posture": "explicit_merge_wave",
            "merge_executed": False,
            "root_dirty_main_quarantined": True,
            "large_artifact_default_policy": "raw_step_trace_and_per_read_rows_out_of_git",
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/P37_post_h50_narrow_executor_closeout_sync/worktree_strategy.md",
            inputs["worktree_strategy_text"],
            ["f28-h51-post-h50-origin-mechanism-reentry", "r57-origin-accelerated-trace-vm-comparator"],
        ),
        (
            "docs/milestones/P37_post_h50_narrow_executor_closeout_sync/artifact_policy.md",
            inputs["artifact_policy_text"],
            ["`probe_read_rows.json`", "`per_read_rows.json`", "Git LFS remains inactive by default"],
        ),
        (
            "docs/milestones/P37_post_h50_narrow_executor_closeout_sync/commit_cadence.md",
            inputs["commit_cadence_text"],
            ["commit `F28` planning surfaces separately", "commit `R57` comparator outputs separately from `H52` decision surfaces"],
        ),
        (
            ".gitignore",
            inputs["gitignore_text"],
            RAW_ROW_IGNORE_PATTERNS,
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["`P37_post_h50_narrow_executor_closeout_sync`", "artifacts above roughly `10 MiB` stay out of git by default"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`P37_post_h50_narrow_executor_closeout_sync`", "`merge_executed = false`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["The current low-priority operational/docs wave is:", "- `P37_post_h50_narrow_executor_closeout_sync`"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`P37_post_h50_narrow_executor_closeout_sync` remains the current low-priority", "no merge back to `main` occurs during this wave"],
        ),
        (
            "docs/publication_record/experiment_manifest.md",
            inputs["experiment_manifest_text"],
            ["post-`H50` `F28/H51/P37` mechanism reentry wave", "new `results/P37_post_h50_narrow_executor_closeout_sync/summary.json`"],
        ),
    ]
    return [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]


def build_summary(checklist_rows: list[dict[str, object]], claim_packet: dict[str, object]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    distilled = claim_packet["distilled_result"]
    tracked_large_artifacts = collect_tracked_large_artifacts()
    return {
        "current_active_stage": distilled["current_active_stage"],
        "preserved_prior_docs_only_closeout": distilled["preserved_prior_docs_only_closeout"],
        "preserved_prior_mechanism_reentry_packet": distilled["preserved_prior_mechanism_reentry_packet"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "refresh_packet": distilled["refresh_packet"],
        "selected_outcome": distilled["selected_outcome"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "current_planning_bundle": distilled["current_planning_bundle"],
        "preserved_comparator_gate": distilled["preserved_comparator_gate"],
        "current_merge_posture": distilled["current_merge_posture"],
        "merge_executed": distilled["merge_executed"],
        "root_dirty_main_quarantined": distilled["root_dirty_main_quarantined"],
        "large_artifact_default_policy": distilled["large_artifact_default_policy"],
        "tracked_large_artifact_count": len(tracked_large_artifacts),
        "tracked_large_artifact_paths": [str(row["path"]) for row in tracked_large_artifacts],
        "next_required_lane": distilled["next_required_lane"],
        "supported_here_count": len(claim_packet["supported_here"]),
        "unsupported_here_count": len(claim_packet["unsupported_here"]),
        "disconfirmed_here_count": len(claim_packet["disconfirmed_here"]),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, claim_packet)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})
    write_json(OUT_DIR / "summary.json", {"summary": summary, "runtime_environment": environment_payload()})


if __name__ == "__main__":
    main()
