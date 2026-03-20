from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_release_worktree_hygiene_snapshot.py"
    spec = importlib.util.spec_from_file_location("export_release_worktree_hygiene_snapshot", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_status_lines_reads_branch_and_rows() -> None:
    module = _load_export_module()

    parsed = module.parse_status_lines("## main\n M README.md\n?? docs/example.md\n")

    assert parsed["branch"] == "main"
    assert parsed["rows"] == [
        {"status_code": " M", "path": "README.md"},
        {"status_code": "??", "path": "docs/example.md"},
    ]


def _sample_worktree_audit(*, changed_path_count: int) -> dict[str, object]:
    modified_path_count = max(changed_path_count - 1, 0)
    untracked_path_count = 1 if changed_path_count else 0
    return {
        "branch": "main",
        "changed_path_count": changed_path_count,
        "modified_path_count": modified_path_count,
        "tracked_dirty_count": modified_path_count,
        "untracked_path_count": untracked_path_count,
        "untracked_count": untracked_path_count,
        "staged_path_count": 0,
        "staged_count": 0,
        "unstaged_path_count": modified_path_count,
        "unstaged_count": modified_path_count,
    }


def test_classify_diff_check_output_tracks_warnings_and_content_issues() -> None:
    module = _load_export_module()

    summary = module.classify_diff_check_output(
        "warning: LF will be replaced by CRLF\nREADME.md:12: trailing whitespace\n"
    )

    assert summary["git_diff_check_state"] == "content_issues_present"
    assert summary["warning_count"] == 1
    assert summary["issue_count"] == 1


def test_build_summary_blocks_release_commit_for_dirty_tree() -> None:
    module = _load_export_module()

    summary = module.build_summary(
        _sample_worktree_audit(changed_path_count=3),
        diff_check_summary=module.classify_diff_check_output("warning: LF will be replaced by CRLF\n"),
    )

    assert summary["release_commit_state"] == "dirty_worktree_release_commit_blocked"
    assert summary["working_tree_clean"] is False
    assert summary["git_diff_check_state"] == "warnings_only"


def test_build_summary_allows_release_commit_for_clean_tree() -> None:
    module = _load_export_module()

    summary = module.build_summary(_sample_worktree_audit(changed_path_count=0))

    assert summary["release_commit_state"] == "clean_worktree_ready_if_other_gates_green"
    assert summary["working_tree_clean"] is True
    assert summary["git_diff_check_state"] == "clean"


def test_live_repo_state_matches_changed_path_count_rule() -> None:
    module = _load_export_module()

    parsed = module.parse_status_lines(module.git_output("status", "--short", "--branch", "--untracked-files=all"))
    audit = module.build_worktree_audit(parsed["rows"], branch=str(parsed["branch"]))
    diff_proc = module.git_result("diff", "--check")
    diff_check_summary = module.classify_diff_check_output(
        "\n".join(part.strip() for part in (diff_proc.stdout, diff_proc.stderr) if part.strip())
    )
    summary = module.build_summary(audit, diff_check_summary=diff_check_summary)

    if summary["changed_path_count"] == 0:
        assert summary["release_commit_state"] == "clean_worktree_ready_if_other_gates_green"
    else:
        assert summary["release_commit_state"] == "dirty_worktree_release_commit_blocked"
    assert summary["git_diff_check_state"] in {"clean", "warnings_only"}
