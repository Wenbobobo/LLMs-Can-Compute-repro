"""Export the post-H64 clean merge-candidate packet for P56."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P56_post_h64_clean_merge_candidate_packet"
DOC_DIR = ROOT / "docs" / "milestones" / "P56_post_h64_clean_merge_candidate_packet"
DESIGN_PATH = ROOT / "docs" / "plans" / "2026-03-31-post-h64-clean-merge-candidate-design.md"
H64_SUMMARY_PATH = ROOT / "results" / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet" / "summary.json"
P54_SUMMARY_PATH = ROOT / "results" / "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming" / "summary.json"
P55_SUMMARY_PATH = ROOT / "results" / "P55_post_h63_clean_descendant_promotion_prep" / "summary.json"
SOURCE_BRANCH = "wip/h64-post-h63-archive-first-freeze"
CANDIDATE_BRANCH = "wip/p56-post-h64-clean-merge-candidate"
SCRATCH_BRANCH = "wip/p56-main-scratch"
TARGET_BRANCH = "main"
ROOT_MAIN_WORKTREE = "D:/zWenbo/AI/LLMCompute"
ROOT_MAIN_BRANCH_PREFIX = "wip/root-main-parking"


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


def git_output(args: list[str], *, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
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


def branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def remote_branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/remotes/origin/{branch}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode == 0


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def parse_worktree_list(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, value = line.split(" ", 1)
        current[key] = value.strip()
    if current:
        entries.append(current)
    return [
        {
            "worktree": entry.get("worktree", "").replace("\\", "/"),
            "branch": entry.get("branch", "").removeprefix("refs/heads/"),
        }
        for entry in entries
    ]


def tracked_large_files() -> list[str]:
    tracked = [path for path in git_output(["ls-files", "-z"]).split("\0") if path]
    rows: list[str] = []
    for rel_path in tracked:
        candidate = ROOT / rel_path
        if candidate.exists() and candidate.is_file() and candidate.stat().st_size >= 10 * 1024 * 1024:
            rows.append(rel_path.replace("\\", "/"))
    return rows


def diff_name_only(revspec: str) -> list[str]:
    output = git_output_optional(["diff", "--name-only", revspec, "--"])
    return [line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()]


def current_candidate_delta_paths() -> list[str]:
    tracked_paths = set(diff_name_only(SOURCE_BRANCH))
    untracked_output = git_output_optional(["ls-files", "--others", "--exclude-standard"])
    for line in untracked_output.splitlines():
        candidate = line.strip().replace("\\", "/")
        if candidate:
            tracked_paths.add(candidate)
    return sorted(tracked_paths)


def top_level_classes(paths: list[str]) -> list[str]:
    classes = {path.split("/", 1)[0] for path in paths if path}
    return sorted(classes)


def main() -> None:
    h64_summary = read_json(H64_SUMMARY_PATH)["summary"]
    p54_summary = read_json(P54_SUMMARY_PATH)["summary"]
    p55_summary = read_json(P55_SUMMARY_PATH)["summary"]
    if h64_summary["selected_outcome"] != "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant":
        raise RuntimeError("P56 expects the landed H64 freeze packet.")
    if p54_summary["selected_outcome"] != "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution":
        raise RuntimeError("P56 expects the landed P54 hygiene packet.")
    if p55_summary["selected_outcome"] != "clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze":
        raise RuntimeError("P56 expects the landed P55 promotion-prep packet.")

    texts = {
        "readme": read_text(DOC_DIR / "README.md"),
        "status": read_text(DOC_DIR / "status.md"),
        "todo": read_text(DOC_DIR / "todo.md"),
        "acceptance": read_text(DOC_DIR / "acceptance.md"),
        "artifact_index": read_text(DOC_DIR / "artifact_index.md"),
        "manifest": read_text(DOC_DIR / "merge_wave_manifest.md"),
        "main_delta": read_text(DOC_DIR / "main_delta_summary.md"),
        "conflict_matrix": read_text(DOC_DIR / "conflict_risk_matrix.md"),
        "runbook": read_text(DOC_DIR / "worktree_runbook.md"),
        "design": read_text(DESIGN_PATH),
    }
    worktrees = parse_worktree_list(git_output(["worktree", "list", "--porcelain"]))
    root_main_entry = next((row for row in worktrees if row["worktree"] == ROOT_MAIN_WORKTREE), None)
    root_main_branch = root_main_entry["branch"] if root_main_entry else ""
    root_main_quarantined = root_main_branch.startswith(ROOT_MAIN_BRANCH_PREFIX)
    source_commit = git_output_optional(["rev-parse", SOURCE_BRANCH])
    source_origin_commit = git_output_optional(["rev-parse", f"origin/{SOURCE_BRANCH}"])
    source_synced = bool(source_commit) and source_commit == source_origin_commit
    left_right = git_output(["rev-list", "--left-right", "--count", f"{TARGET_BRANCH}...{SOURCE_BRANCH}"]).split()
    behind_main_count = int(left_right[0])
    ahead_of_main_count = int(left_right[1])
    main_delta_paths = diff_name_only(f"{TARGET_BRANCH}..{SOURCE_BRANCH}")
    candidate_delta_paths = current_candidate_delta_paths()
    tracked_oversize = tracked_large_files()
    candidate_branch_local_exists = branch_exists(CANDIDATE_BRANCH)
    candidate_branch_remote_exists = remote_branch_exists(CANDIDATE_BRANCH)
    candidate_branch_absorbed_locally = (
        not candidate_branch_local_exists
        and candidate_branch_remote_exists
        and branch_exists(SCRATCH_BRANCH)
        and contains_all(
            texts["status"] + "\n" + texts["readme"],
            [
                "absorbed locally into",
                "`wip/p56-main-scratch`",
            ],
        )
    )

    checklist_rows = [
        {
            "item_id": "p56_prerequisites_green",
            "status": "pass",
            "notes": "P56 starts only after landed H64/P54/P55 summaries stay green.",
        },
        {
            "item_id": "p56_docs_define_operational_merge_candidate_only",
            "status": "pass"
            if all(
                (
                    contains_all(
                        texts["readme"],
                        [
                            "wip/h64-post-h63-archive-first-freeze",
                            "wip/p56-post-h64-clean-merge-candidate",
                            "does not merge `main`",
                        ],
                    ),
                    contains_all(
                        texts["status"],
                        [
                            "`merge_recommended = false`",
                            "`merge_executed = false`",
                            "clean_descendant_only_never_dirty_root_main",
                        ],
                    ),
                    contains_all(
                        texts["acceptance"],
                        [
                            "operational rather than scientific",
                            "dirty root `main` remains quarantine-only",
                            "`merge_executed` remains false",
                        ],
                    ),
                    contains_all(
                        texts["todo"],
                        [
                            "merge-candidate prep separate from merge execution",
                            "dirty root `main` quarantine explicit",
                            "raw-row ignore rules",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "P56 docs must keep candidate prep explicit and merge execution false.",
        },
        {
            "item_id": "p56_manifest_delta_conflict_and_runbook_are_explicit",
            "status": "pass"
            if all(
                (
                    contains_all(
                        texts["manifest"],
                        [
                            "wip/h64-post-h63-archive-first-freeze",
                            "wip/p56-post-h64-clean-merge-candidate",
                            "wip/p56-main-scratch",
                            "clean_descendant_only_never_dirty_root_main",
                            "`merge_executed = false`",
                        ],
                    ),
                    contains_all(
                        texts["main_delta"],
                        [
                            "`138` commits ahead of `main`",
                            "`1966` tracked files",
                            "`docs`",
                            "`scripts`",
                            "`tests`",
                            "`results`",
                        ],
                    ),
                    contains_all(
                        texts["conflict_matrix"],
                        [
                            "`docs/publication_record/current_stage_driver.md`",
                            "`scripts/export_release_preflight_checklist_audit.py`",
                            "`results/P56_*` through `results/P59_*`",
                            "Never resolve any of the high-risk rows from dirty root `main`",
                        ],
                    ),
                    contains_all(
                        texts["runbook"],
                        [
                            "wip/p56-post-h64-clean-merge-candidate",
                            "origin/wip/h64-post-h63-archive-first-freeze",
                            "git worktree list --porcelain",
                            "git diff --stat main..wip/h64-post-h63-archive-first-freeze",
                        ],
                    ),
                    contains_all(
                        texts["artifact_index"],
                        [
                            "results/P56_post_h64_clean_merge_candidate_packet/summary.json",
                            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
                        ],
                    ),
                    contains_all(
                        texts["design"],
                        [
                            "`P56_post_h64_clean_merge_candidate_packet` is the recommended main route",
                            "`P56 -> (P57 || P58) -> P59`",
                        ],
                    ),
                )
            )
            else "blocked",
            "notes": "P56 must make delta, conflict, and runbook surfaces explicit.",
        },
        {
            "item_id": "p56_source_and_root_posture_are_clean_descendant_only",
            "status": "pass"
            if source_synced
            and branch_exists(SOURCE_BRANCH)
            and branch_exists(SCRATCH_BRANCH)
            and (candidate_branch_local_exists or candidate_branch_absorbed_locally)
            and root_main_quarantined
            and not tracked_oversize
            else "blocked",
            "notes": "Source sync, historical candidate availability, root quarantine, and oversize-artifact posture must all hold.",
        },
    ]
    claim_packet = {
        "supports": [
            "P56 stages an explicit clean merge candidate above the stable H64 freeze stack.",
            "P56 keeps dirty root main quarantined and keeps merge execution false.",
            "P56 makes the current main delta, conflict inventory, and runbook explicit without authorizing a merge.",
        ],
        "does_not_support": [
            "merge execution",
            "runtime reopen",
            "dirty-root integration",
            "broad Wasm or arbitrary C scope lift",
        ],
        "distilled_result": {
            "active_stage_at_merge_candidate_time": "h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "current_clean_merge_candidate_packet": "p56_post_h64_clean_merge_candidate_packet",
            "current_clean_source_branch": SOURCE_BRANCH,
            "current_candidate_branch": CANDIDATE_BRANCH,
            "candidate_branch_local_exists": candidate_branch_local_exists,
            "candidate_branch_remote_exists": candidate_branch_remote_exists,
            "candidate_branch_absorbed_locally": candidate_branch_absorbed_locally,
            "current_clean_main_scratch_branch": SCRATCH_BRANCH,
            "target_branch": TARGET_BRANCH,
            "merge_posture": "clean_descendant_only_never_dirty_root_main",
            "merge_recommended": False,
            "merge_execution_state": False,
            "source_branch_synced_to_origin": source_synced,
            "root_main_branch": root_main_branch,
            "root_main_quarantined": root_main_quarantined,
            "ahead_of_main_commit_count": ahead_of_main_count,
            "behind_main_commit_count": behind_main_count,
            "main_delta_file_count": len(main_delta_paths),
            "candidate_delta_file_count": len(candidate_delta_paths),
            "candidate_delta_path_classes": top_level_classes(candidate_delta_paths),
            "tracked_oversize_count": len(tracked_oversize),
            "selected_outcome": "clean_descendant_merge_candidate_staged_without_merge_execution",
            "next_required_lane": "p57_p58_parallel_sidecars_then_p59_control_sync",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
            "tracked_oversize_artifacts": tracked_oversize,
            "main_delta_path_classes": top_level_classes(main_delta_paths),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"field": "current_clean_source_branch", "value": SOURCE_BRANCH},
            {"field": "current_candidate_branch", "value": CANDIDATE_BRANCH},
            {"field": "candidate_branch_local_exists", "value": candidate_branch_local_exists},
            {"field": "candidate_branch_remote_exists", "value": candidate_branch_remote_exists},
            {"field": "ahead_of_main_commit_count", "value": ahead_of_main_count},
            {"field": "main_delta_file_count", "value": len(main_delta_paths)},
            {"field": "candidate_delta_file_count", "value": len(candidate_delta_paths)},
            {"field": "candidate_delta_path_classes", "value": top_level_classes(candidate_delta_paths)},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
