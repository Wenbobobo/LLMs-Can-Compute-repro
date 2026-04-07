"""Export the post-H52 compiled-boundary hygiene sync packet for P38."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P38_post_h52_compiled_boundary_hygiene_sync"
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
        "p38_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "README.md"
        ),
        "p38_status_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "status.md"
        ),
        "p38_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "todo.md"
        ),
        "p38_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "acceptance.md"
        ),
        "p38_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "artifact_index.md"
        ),
        "worktree_strategy_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "worktree_strategy.md"
        ),
        "artifact_policy_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "artifact_policy.md"
        ),
        "commit_cadence_text": read_text(
            ROOT / "docs" / "milestones" / "P38_post_h52_compiled_boundary_hygiene_sync" / "commit_cadence.md"
        ),
        "gitignore_text": read_text(ROOT / ".gitignore"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h54_summary": read_json(ROOT / "results" / "H54_post_r58_r59_compiled_boundary_decision_packet" / "summary.json"),
        "h53_summary": read_json(ROOT / "results" / "H53_post_h52_compiled_boundary_reentry_packet" / "summary.json"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "tracked_large_artifacts": tracked_large_artifacts,
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h54 = inputs["h54_summary"]["summary"]
    h53 = inputs["h53_summary"]["summary"]
    h43 = inputs["h43_summary"]["summary"]
    return [
        {
            "item_id": "p38_docs_define_post_h52_hygiene_sync_packet",
            "status": "pass"
            if contains_all(
                inputs["p38_readme_text"],
                [
                    "completed low-priority operational/docs sync packet",
                    "`h53` as the preserved prior compiled-boundary reentry packet",
                    "`h54` as the current active docs-only closeout",
                    "`h52` as the preserved prior mechanism closeout",
                    "`h43` as the paper-grade endpoint",
                    "`f29 -> h53 -> r58 -> r59 -> h54`",
                ],
            )
            and contains_all(
                inputs["p38_status_text"],
                [
                    "completed operational/docs sync packet",
                    "preserves `h54` as the current active docs-only closeout",
                    "preserves `h53` as the preserved prior compiled-boundary reentry packet",
                    "preserves the clean `f29` worktree as the control and execution surface",
                    "keeps `merge_executed = false` explicit",
                    "large-artifact-out-of-git defaults",
                    "`uv` as the default execution path",
                ],
            )
            and contains_all(
                inputs["p38_todo_text"],
                [
                    "record one clean worktree strategy",
                    "record one artifact policy",
                    "record one commit cadence",
                    "keep artifacts above roughly `10 mib` out of git by default",
                    "keep `uv` as the default execution path",
                ],
            )
            and contains_all(
                inputs["p38_acceptance_text"],
                [
                    "`p38` remains operational/docs-only",
                    "`h54` remains the current active docs-only packet",
                    "`h53` remains the preserved prior compiled-boundary reentry packet",
                    "artifacts above roughly `10 mib` stay out of git by default",
                    "`uv` remains the default execution path",
                    "merge back to `main` does not occur during this wave",
                ],
            )
            else "blocked",
            "notes": "P38 should codify hygiene and no-merge policy for the closed compiled-boundary wave without changing scientific stage.",
        },
        {
            "item_id": "p38_records_worktree_artifact_and_commit_policy",
            "status": "pass"
            if contains_all(
                inputs["worktree_strategy_text"],
                [
                    "f29-post-h52-compiled-boundary-reentry",
                    "dirty root `main` is not a scientific execution surface",
                    "packet-sized commits",
                ],
            )
            and contains_all(
                inputs["artifact_policy_text"],
                [
                    "compact summaries, checklists, manifests, stop rules, timing digests",
                    "any artifact above roughly `10 mib` as out-of-git by default",
                    "git lfs remains inactive by default",
                    "`uv` remains the default path",
                ],
            )
            and contains_all(
                inputs["commit_cadence_text"],
                [
                    "commit `f29/h53/p38` control surfaces separately",
                    "commit `r58` lowering artifacts separately from `r59` execution artifacts",
                    "commit `h54` decision surfaces separately from runtime gates",
                ],
            )
            and contains_all(
                inputs["p38_artifact_index_text"],
                [
                    "docs/milestones/p38_post_h52_compiled_boundary_hygiene_sync/worktree_strategy.md",
                    "docs/milestones/p38_post_h52_compiled_boundary_hygiene_sync/artifact_policy.md",
                    "docs/milestones/p38_post_h52_compiled_boundary_hygiene_sync/commit_cadence.md",
                    "results/p38_post_h52_compiled_boundary_hygiene_sync/summary.json",
                ],
            )
            else "blocked",
            "notes": "P38 should make the worktree policy, large-artifact policy, and commit cadence explicit for this wave.",
        },
        {
            "item_id": "p38_repo_state_matches_large_artifact_policy",
            "status": "pass"
            if contains_all(inputs["gitignore_text"], RAW_ROW_IGNORE_PATTERNS)
            and not inputs["tracked_large_artifacts"]
            else "blocked",
            "notes": "The clean worktree should keep tracked artifacts under the roughly 10 MiB default limit.",
        },
        {
            "item_id": "shared_control_surfaces_make_p38_current_low_priority_wave",
            "status": "pass"
            if str(h54["selected_outcome"]) == "freeze_restricted_compiled_boundary_supported_narrowly_without_fastpath_value"
            and str(h54["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(h53["selected_outcome"]) == "authorize_compiled_boundary_reentry_through_r58_first"
            and str(h43["active_stage"]) == "h43_post_r44_useful_case_refreeze"
            and bool(h43["merge_executed"]) is False
            and contains_all(
                inputs["readme_text"],
                [
                    "current low-priority operational/docs wave:",
                    "`p38_post_h52_compiled_boundary_hygiene_sync`",
                    "artifacts above roughly `10 mib` stay out of git by default",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "the current low-priority operational/docs wave remains",
                    "`p38_post_h52_compiled_boundary_hygiene_sync`",
                    "dirty root `main` remains quarantined and `merge_executed = false` remains explicit",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "the current low-priority operational/docs wave is:",
                    "- `p38_post_h52_compiled_boundary_hygiene_sync`",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "`p38_post_h52_compiled_boundary_hygiene_sync`",
                    "`h54_post_r58_r59_compiled_boundary_decision_packet`",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`p38_post_h52_compiled_boundary_hygiene_sync` remains the current low-priority",
                    "out-of-git by default",
                    "no merge back to `main` occurs during this wave",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h52` restricted compiled-boundary reentry wave",
                    "new `scripts/export_p38_post_h52_compiled_boundary_hygiene_sync.py`",
                    "new `results/p38_post_h52_compiled_boundary_hygiene_sync/summary.json`",
                ],
            )
            else "blocked",
            "notes": "Shared control docs should expose P38 as the current low-priority wave and keep no-merge posture explicit.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "P38 promotes the clean F29 worktree as the control and execution surface for the compiled-boundary wave.",
            "P38 keeps raw row dumps and artifacts above roughly 10 MiB out of git by default while preserving explicit no-merge posture.",
            "P38 keeps uv as the default exporter and focused-test execution path.",
        ],
        "unsupported_here": [
            "P38 does not change the active scientific stage or overturn H52/H54.",
            "P38 does not merge dirty root main back into the clean line.",
            "P38 does not reopen a downstream runtime lane after the landed H54 closeout.",
        ],
        "disconfirmed_here": [
            "The idea that convenience alone is enough reason to keep large raw artifacts in git or to execute science from dirty root main.",
        ],
        "distilled_result": {
            "current_active_stage": "h54_post_r58_r59_compiled_boundary_decision_packet",
            "preserved_prior_docs_only_closeout": "h52_post_r55_r56_r57_origin_mechanism_decision_packet",
            "preserved_prior_compiled_boundary_reentry_packet": "h53_post_h52_compiled_boundary_reentry_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "refresh_packet": "p38_post_h52_compiled_boundary_hygiene_sync",
            "selected_outcome": "compiled_boundary_hygiene_preserved_through_h54_closeout",
            "current_low_priority_wave": "p38_post_h52_compiled_boundary_hygiene_sync",
            "current_planning_bundle": "f29_post_h52_restricted_compiled_boundary_bundle",
            "preserved_execution_gate": "r59_origin_compiled_trace_vm_execution_gate",
            "current_merge_posture": "explicit_no_merge_during_wave",
            "merge_executed": False,
            "root_dirty_main_quarantined": True,
            "large_artifact_default_policy": "raw_step_trace_and_per_read_rows_out_of_git",
            "next_required_lane": "no_active_downstream_runtime_lane",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    rows = [
        (
            "docs/milestones/P38_post_h52_compiled_boundary_hygiene_sync/worktree_strategy.md",
            inputs["worktree_strategy_text"],
            ["f29-post-h52-compiled-boundary-reentry", "dirty root `main` is not a scientific execution surface"],
        ),
        (
            "docs/milestones/P38_post_h52_compiled_boundary_hygiene_sync/artifact_policy.md",
            inputs["artifact_policy_text"],
            ["artifact above roughly `10 MiB`", "Git LFS remains inactive by default", "`uv` remains the default path"],
        ),
        (
            "docs/milestones/P38_post_h52_compiled_boundary_hygiene_sync/commit_cadence.md",
            inputs["commit_cadence_text"],
            ["commit `F29/H53/P38` control surfaces separately", "commit `H54` decision surfaces separately from runtime gates"],
        ),
        (
            ".gitignore",
            inputs["gitignore_text"],
            RAW_ROW_IGNORE_PATTERNS,
        ),
        (
            "README.md",
            inputs["readme_text"],
            ["`P38_post_h52_compiled_boundary_hygiene_sync`", "artifacts above roughly `10 MiB` stay out of git by default"],
        ),
        (
            "STATUS.md",
            inputs["status_text"],
            ["`P38_post_h52_compiled_boundary_hygiene_sync`", "`merge_executed = false`"],
        ),
        (
            "docs/publication_record/current_stage_driver.md",
            inputs["current_stage_driver_text"],
            ["The current low-priority operational/docs wave is:", "- `P38_post_h52_compiled_boundary_hygiene_sync`"],
        ),
        (
            "tmp/active_wave_plan.md",
            inputs["active_wave_plan_text"],
            ["`P38_post_h52_compiled_boundary_hygiene_sync` remains the current low-priority", "no merge back to `main` occurs during this wave"],
        ),
        (
            "docs/publication_record/experiment_manifest.md",
            inputs["experiment_manifest_text"],
            ["post-`H52` restricted compiled-boundary reentry wave", "new `results/P38_post_h52_compiled_boundary_hygiene_sync/summary.json`"],
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
        "preserved_prior_compiled_boundary_reentry_packet": distilled["preserved_prior_compiled_boundary_reentry_packet"],
        "current_paper_grade_endpoint": distilled["current_paper_grade_endpoint"],
        "refresh_packet": distilled["refresh_packet"],
        "selected_outcome": distilled["selected_outcome"],
        "current_low_priority_wave": distilled["current_low_priority_wave"],
        "current_planning_bundle": distilled["current_planning_bundle"],
        "preserved_execution_gate": distilled["preserved_execution_gate"],
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
