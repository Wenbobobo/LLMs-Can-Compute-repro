"""Export a machine-readable snapshot of current git worktree release hygiene."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "release_worktree_hygiene_snapshot"
HYGIENE_GIT_ROOT_ENV = "LLMCOMPUTE_HYGIENE_GIT_ROOT"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def resolved_git_root() -> Path:
    override = os.environ.get(HYGIENE_GIT_ROOT_ENV)
    return Path(override).resolve() if override else ROOT.resolve()


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=resolved_git_root(),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def git_result(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=resolved_git_root(),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def normalize_status_path(raw_path: str) -> str:
    path = raw_path.strip()
    if " -> " in path:
        _, new_path = path.split(" -> ", 1)
        return new_path.strip()
    return path


def parse_status_lines(text: str) -> dict[str, object]:
    branch_line = ""
    rows: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        if not raw_line:
            continue
        if raw_line.startswith("## "):
            branch_line = raw_line[3:].strip().split("...", 1)[0]
            continue
        status_code = raw_line[:2]
        path = normalize_status_path(raw_line[3:])
        rows.append({"status_code": status_code, "path": path})
    return {"branch": branch_line, "rows": rows}


def classify_commit_group(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized in {".gitignore", "README.md", "STATUS.md", "pyproject.toml", "scripts/README.md"}:
        return "release_surface_cleanup"
    if normalized.startswith("docs/publication_record/") or normalized.startswith("docs/milestones/"):
        return "docs_results_sync"
    if normalized.startswith("docs/") or normalized.startswith("results/"):
        return "docs_results_sync"
    if normalized.startswith("scripts/export_p") or normalized.startswith("scripts/export_r"):
        return "docs_results_sync"
    if normalized.startswith("tests/test_export_") or normalized.startswith("scripts/render_p1"):
        return "docs_results_sync"
    if normalized.startswith("tests/test_render_p1"):
        return "docs_results_sync"
    if normalized.startswith("src/"):
        return "experiments_and_runtime"
    if normalized.startswith("scripts/export_m") or normalized.startswith("scripts/export_h"):
        return "experiments_and_runtime"
    if normalized.startswith("tests/test_model") or normalized.startswith("tests/test_trace"):
        return "experiments_and_runtime"
    if normalized.startswith("tests/test_bytecode"):
        return "experiments_and_runtime"
    if normalized.startswith("scripts/setup_unattended_worktrees.ps1"):
        return "release_surface_cleanup"
    return "misc"


def build_worktree_audit(status_rows: list[dict[str, str]], *, branch: str) -> dict[str, object]:
    modified = [row for row in status_rows if row["status_code"] != "??"]
    untracked = [row for row in status_rows if row["status_code"] == "??"]
    staged = [row for row in status_rows if row["status_code"][0] not in {" ", "?"}]
    unstaged = [row for row in status_rows if row["status_code"][1] != " " and row["status_code"] != "??"]

    by_group: dict[str, list[str]] = {}
    for row in status_rows:
        group = classify_commit_group(row["path"])
        by_group.setdefault(group, []).append(row["path"])

    return {
        "branch": branch,
        "changed_path_count": len(status_rows),
        "modified_path_count": len(modified),
        "tracked_dirty_count": len(modified),
        "untracked_path_count": len(untracked),
        "untracked_count": len(untracked),
        "staged_path_count": len(staged),
        "staged_count": len(staged),
        "unstaged_path_count": len(unstaged),
        "unstaged_count": len(unstaged),
        "group_counts": [
            {"group": group, "count": len(paths)}
            for group, paths in sorted(by_group.items())
        ],
        "sample_paths": {
            group: sorted(paths)[:10]
            for group, paths in sorted(by_group.items())
        },
    }


def classify_diff_check_output(text: str) -> dict[str, object]:
    warnings = [line.strip() for line in text.splitlines() if line.strip().lower().startswith("warning:")]
    issues = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().lower().startswith("warning:")]
    return {
        "git_diff_check_state": "content_issues_present" if issues else "warnings_only" if warnings else "clean",
        "warning_count": len(warnings),
        "issue_count": len(issues),
        "sample_warnings": warnings[:10],
        "sample_issues": issues[:10],
    }


def build_checklist_rows(
    *,
    status_returncode: int,
    diff_check_returncode: int,
    diff_check_summary: dict[str, object],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "git_status_command_completed",
            "status": "pass" if status_returncode == 0 else "blocked",
            "notes": "The snapshot should read current git status successfully.",
        },
        {
            "item_id": "git_diff_check_has_no_content_issues",
            "status": "pass"
            if diff_check_returncode == 0 and diff_check_summary["git_diff_check_state"] != "content_issues_present"
            else "blocked",
            "notes": "Warnings-only diff-check output is acceptable, but content issues are not.",
        },
    ]


def build_summary(
    worktree_audit: dict[str, object],
    diff_check_summary: dict[str, object] | None = None,
    checklist_rows: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    diff_summary = diff_check_summary or {
        "git_diff_check_state": "clean",
        "warning_count": 0,
        "issue_count": 0,
        "sample_warnings": [],
        "sample_issues": [],
    }
    rows = checklist_rows or []
    changed_path_count = int(worktree_audit["changed_path_count"])
    release_commit_state = (
        "clean_worktree_ready_if_other_gates_green"
        if changed_path_count == 0
        else "dirty_worktree_release_commit_blocked"
    )
    return {
        "repo_hygiene_scope": "current_worktree_and_diff_check",
        "git_root": resolved_git_root().as_posix(),
        "branch": worktree_audit["branch"],
        "changed_path_count": changed_path_count,
        "modified_path_count": int(worktree_audit["modified_path_count"]),
        "tracked_dirty_count": int(worktree_audit["tracked_dirty_count"]),
        "untracked_path_count": int(worktree_audit["untracked_path_count"]),
        "untracked_count": int(worktree_audit["untracked_count"]),
        "staged_path_count": int(worktree_audit["staged_path_count"]),
        "staged_count": int(worktree_audit["staged_count"]),
        "unstaged_path_count": int(worktree_audit["unstaged_path_count"]),
        "unstaged_count": int(worktree_audit["unstaged_count"]),
        "release_commit_state": release_commit_state,
        "working_tree_clean": changed_path_count == 0,
        "git_diff_check_state": str(diff_summary["git_diff_check_state"]),
        "warning_count": int(diff_summary["warning_count"]),
        "issue_count": int(diff_summary["issue_count"]),
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": [row["item_id"] for row in rows if row["status"] != "pass"],
        "recommended_next_action": (
            "the repo is clean enough for an outward sync commit if the other release-facing audits are green"
            if changed_path_count == 0
            else "do not create an outward sync commit from the current tree; isolate the intended release subset or wait for a clean tree"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    status_proc = git_result("status", "--short", "--branch", "--untracked-files=all")
    diff_proc = git_result("diff", "--check")
    parsed = parse_status_lines(status_proc.stdout)
    worktree_audit = build_worktree_audit(parsed["rows"], branch=str(parsed["branch"]))
    diff_check_text = "\n".join(
        part.strip() for part in (diff_proc.stdout, diff_proc.stderr) if part.strip()
    )
    diff_check_summary = classify_diff_check_output(diff_check_text)
    checklist_rows = build_checklist_rows(
        status_returncode=status_proc.returncode,
        diff_check_returncode=diff_proc.returncode,
        diff_check_summary=diff_check_summary,
    )
    summary = build_summary(worktree_audit, diff_check_summary, checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "release_worktree_hygiene_snapshot_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "status_snapshot.json",
        {
            "experiment": "release_worktree_hygiene_snapshot_status_snapshot",
            "environment": environment.as_dict(),
            "git_root": resolved_git_root().as_posix(),
            "branch": parsed["branch"],
            "rows": parsed["rows"],
            "worktree_audit": worktree_audit,
            "diff_check_summary": diff_check_summary,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "release_worktree_hygiene_snapshot",
            "environment": environment.as_dict(),
            "source_artifacts": ["git status --short --branch --untracked-files=all", "git diff --check"],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Release Worktree Hygiene Snapshot",
                "",
                "Operational snapshot of the live git worktree used to decide whether the",
                "current tree blocks a release-facing commit.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `status_snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
