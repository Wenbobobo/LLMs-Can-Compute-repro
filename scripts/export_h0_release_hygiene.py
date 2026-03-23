"""Export the current release-hygiene and commit-split snapshot for H0."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H0_repo_consolidation_and_release_hygiene"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


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
            branch_line = raw_line[3:].strip()
            continue
        status_code = raw_line[:2]
        path = normalize_status_path(raw_line[3:])
        rows.append({"status_code": status_code, "path": path})
    return {"branch": branch_line, "rows": rows}


def classify_commit_group(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized in {".gitignore", "README.md", "STATUS.md", "pyproject.toml", "scripts/README.md"}:
        return "release_surface_cleanup"
    if normalized.startswith("scripts/export_h0") or normalized.startswith("tests/test_export_h0"):
        return "release_surface_cleanup"
    if normalized.startswith("docs/milestones/H0_repo_consolidation_and_release_hygiene/"):
        return "release_surface_cleanup"
    if normalized.startswith("docs/milestones/P2_public_research_packaging/"):
        return "release_surface_cleanup"
    if normalized.startswith("docs/publication_record/"):
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
    if normalized.startswith("scripts/export_m") or normalized.startswith("scripts/export_h0"):
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
    by_group: dict[str, list[str]] = {}
    for row in status_rows:
        group = classify_commit_group(row["path"])
        by_group.setdefault(group, []).append(row["path"])

    return {
        "branch": branch,
        "changed_path_count": len(status_rows),
        "modified_path_count": len(modified),
        "untracked_path_count": len(untracked),
        "group_counts": [
            {"group": group, "count": len(paths)}
            for group, paths in sorted(by_group.items())
        ],
        "sample_paths": {
            group: sorted(paths)[:10]
            for group, paths in sorted(by_group.items())
        },
    }


def build_commit_split_plan(status_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups = {
        "docs_results_sync": {
            "label": "docs/results: sync evidence and ledgers",
            "commit_message": "docs/results: sync M4-M7 evidence and publication ledgers",
            "description": "Milestone docs, publication ledgers, tracked result bundles, and export-layer tests.",
        },
        "experiments_and_runtime": {
            "label": "experiments: runtime and artifact exports",
            "commit_message": "experiments: add runtime, bytecode, and closure exports",
            "description": "Core implementation, experiment exports, and runtime-facing regression tests.",
        },
        "release_surface_cleanup": {
            "label": "release: public surface cleanup",
            "commit_message": "release: refresh README, STATUS, packaging, and hygiene docs",
            "description": "Root docs, packaging ledgers, ignore rules, and release-hygiene checkpoint material.",
        },
        "misc": {
            "label": "misc: uncategorized leftovers",
            "commit_message": "chore: resolve uncategorized repository leftovers",
            "description": "Anything not covered by the three preferred review groups should be triaged before outward sync.",
        },
    }
    grouped_paths: dict[str, list[str]] = {group: [] for group in groups}
    for row in status_rows:
        grouped_paths[classify_commit_group(row["path"])].append(row["path"])

    plan = []
    for group_id, metadata in groups.items():
        paths = sorted(grouped_paths[group_id])
        plan.append(
            {
                "group_id": group_id,
                "label": metadata["label"],
                "description": metadata["description"],
                "commit_message": metadata["commit_message"],
                "path_count": len(paths),
                "status": "ready" if paths else "empty",
                "paths": paths,
            }
        )
    return plan


def has_required_gitignore_entries(text: str) -> tuple[bool, list[str]]:
    required = ["docs/Origin/", "docs/origin/", "tmp/"]
    missing = [entry for entry in required if entry not in text]
    return not missing, missing


def build_public_surface_audit(
    *,
    readme_text: str,
    status_text: str,
    gitignore_text: str,
    p4_summary: dict[str, object],
    m7_summary: dict[str, object],
    artifact_release_ledger_text: str,
    tmp_plan_exists: bool,
) -> list[dict[str, object]]:
    p4 = p4_summary["summary"]
    m7 = m7_summary["summary"]
    gitignore_ok, missing_gitignore = has_required_gitignore_entries(gitignore_text)
    release_ledger_mentions_h0 = "results/H0_repo_consolidation_and_release_hygiene/" in artifact_release_ledger_text
    return [
        {
            "check_id": "readme_tracks_current_gate",
            "status": "pass"
            if "frontend widening is not authorized" in readme_text and "blog remains blocked" in readme_text
            else "fail",
            "notes": "README states the current M7/P4 outcome rather than leaving it implied.",
        },
        {
            "check_id": "status_tracks_h0_followup",
            "status": "pass"
            if (
                ("release hygiene" in status_text or "release-hygiene" in status_text)
                and ("commit/release pass" in status_text or "commit split" in status_text)
            )
            else "fail",
            "notes": "STATUS keeps the operational repo-hygiene work visible.",
        },
        {
            "check_id": "gitignore_covers_restricted_material",
            "status": "pass" if gitignore_ok else "fail",
            "notes": "Required ignore entries present."
            if gitignore_ok
            else f"Missing entries: {', '.join(missing_gitignore)}.",
        },
        {
            "check_id": "m7_no_widening_recorded",
            "status": "pass"
            if m7["decision_status"] == "stay_on_tiny_typed_bytecode" and not m7["frontend_widening_authorized"]
            else "fail",
            "notes": "M7 still blocks widening; the preserved first compiled step remains D0 inside the broader current H43 paper endpoint.",
        },
        {
            "check_id": "p4_blog_hold_recorded",
            "status": "pass"
            if p4["release_status"] == "blog_blocked_readme_only" and not p4["blog_authorized"]
            else "fail",
            "notes": "README is allowed, broader blog release is still blocked.",
        },
        {
            "check_id": "p2_ledger_mentions_h0",
            "status": "pass" if release_ledger_mentions_h0 else "fail",
            "notes": "Artifact release ledger includes the H0 snapshot."
            if release_ledger_mentions_h0
            else "Artifact release ledger still needs an H0 row.",
        },
        {
            "check_id": "tmp_plan_retained",
            "status": "pass" if tmp_plan_exists else "fail",
            "notes": "Temporary next-stage plan is still retained for unattended handoff continuity."
            if tmp_plan_exists
            else "Temporary next-stage plan is missing.",
        },
    ]


def build_summary(
    *,
    worktree_audit: dict[str, object],
    commit_split_plan: list[dict[str, object]],
    public_surface_audit: list[dict[str, object]],
) -> dict[str, object]:
    blocked_checks = [row["check_id"] for row in public_surface_audit if row["status"] != "pass"]
    nonempty_groups = [row for row in commit_split_plan if row["path_count"] > 0]
    return {
        "branch": worktree_audit["branch"],
        "changed_path_count": worktree_audit["changed_path_count"],
        "modified_path_count": worktree_audit["modified_path_count"],
        "untracked_path_count": worktree_audit["untracked_path_count"],
        "public_surface_check_count": len(public_surface_audit),
        "public_surface_pass_count": sum(row["status"] == "pass" for row in public_surface_audit),
        "public_surface_blocked_count": sum(row["status"] != "pass" for row in public_surface_audit),
        "blocked_checks": blocked_checks,
        "nonempty_commit_groups": [
            {"group_id": row["group_id"], "path_count": row["path_count"]}
            for row in nonempty_groups
        ],
        "recommended_next_action": (
            "apply the recorded commit split before the next outward sync"
            if nonempty_groups
            else "worktree is already clean"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    status_payload = parse_status_lines(git_output("status", "--porcelain=v1", "--branch"))
    status_rows = status_payload["rows"]
    worktree_audit = build_worktree_audit(status_rows, branch=str(status_payload["branch"]))
    commit_split_plan = build_commit_split_plan(status_rows)
    public_surface_audit = build_public_surface_audit(
        readme_text=read_text(ROOT / "README.md"),
        status_text=read_text(ROOT / "STATUS.md"),
        gitignore_text=read_text(ROOT / ".gitignore"),
        p4_summary=read_json(ROOT / "results" / "P4_blog_release_gate" / "summary.json"),
        m7_summary=read_json(ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json"),
        artifact_release_ledger_text=read_text(
            ROOT / "docs" / "milestones" / "P2_public_research_packaging" / "artifact_release_ledger.md"
        ),
        tmp_plan_exists=(ROOT / "tmp" / "2026-03-18-next-stage-plan.md").exists(),
    )
    summary = build_summary(
        worktree_audit=worktree_audit,
        commit_split_plan=commit_split_plan,
        public_surface_audit=public_surface_audit,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "worktree_audit.json",
        {
            "experiment": "h0_worktree_audit",
            "environment": environment.as_dict(),
            "summary": worktree_audit,
        },
    )
    write_json(
        OUT_DIR / "commit_split_plan.json",
        {
            "experiment": "h0_commit_split_plan",
            "environment": environment.as_dict(),
            "rows": commit_split_plan,
        },
    )
    write_json(
        OUT_DIR / "public_surface_audit.json",
        {
            "experiment": "h0_public_surface_audit",
            "environment": environment.as_dict(),
            "rows": public_surface_audit,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h0_repo_consolidation_and_release_hygiene",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                ".gitignore",
                "docs/milestones/P2_public_research_packaging/artifact_release_ledger.md",
                "results/M7_frontend_candidate_decision/decision_summary.json",
                "results/P4_blog_release_gate/summary.json",
                "tmp/2026-03-18-next-stage-plan.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# H0 Repo Consolidation and Release Hygiene",
                "",
                "Machine-readable snapshot of the current public surface, dirty worktree state, and suggested commit split.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `worktree_audit.json`",
                "- `commit_split_plan.json`",
                "- `public_surface_audit.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
