from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h0_release_hygiene.py"
    spec = importlib.util.spec_from_file_location("export_h0_release_hygiene", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_status_lines_tracks_branch_and_rows() -> None:
    module = _load_export_module()

    payload = module.parse_status_lines("## main...origin/main\n M README.md\n?? docs/foo.md\n")

    assert payload["branch"] == "main...origin/main"
    assert payload["rows"] == [
        {"status_code": " M", "path": "README.md"},
        {"status_code": "??", "path": "docs/foo.md"},
    ]


def test_classify_commit_group_prefers_three_review_groups() -> None:
    module = _load_export_module()

    assert module.classify_commit_group("README.md") == "release_surface_cleanup"
    assert module.classify_commit_group("docs/publication_record/claim_ladder.md") == "docs_results_sync"
    assert module.classify_commit_group("src/model/free_running_executor.py") == "experiments_and_runtime"


def test_build_commit_split_plan_counts_paths_per_group() -> None:
    module = _load_export_module()

    plan = module.build_commit_split_plan(
        [
            {"status_code": " M", "path": "README.md"},
            {"status_code": "??", "path": "docs/publication_record/claim_ladder.md"},
            {"status_code": " M", "path": "src/model/free_running_executor.py"},
        ]
    )

    by_group = {row["group_id"]: row for row in plan}
    assert by_group["release_surface_cleanup"]["path_count"] == 1
    assert by_group["docs_results_sync"]["path_count"] == 1
    assert by_group["experiments_and_runtime"]["path_count"] == 1


def test_build_public_surface_audit_accepts_current_gate_shape() -> None:
    module = _load_export_module()

    rows = module.build_public_surface_audit(
        readme_text="frontend widening is not authorized\nblog remains blocked\n",
        status_text="release hygiene\ncommit/release pass\n",
        gitignore_text="docs/Origin/\ndocs/origin/\ntmp/\n",
        p4_summary={"summary": {"release_status": "blog_blocked_readme_only", "blog_authorized": False}},
        m7_summary={"summary": {"decision_status": "stay_on_tiny_typed_bytecode", "frontend_widening_authorized": False}},
        artifact_release_ledger_text="results/H0_repo_consolidation_and_release_hygiene/\n",
        tmp_plan_exists=True,
    )

    assert all(row["status"] == "pass" for row in rows)
    by_id = {row["check_id"]: row for row in rows}
    assert "current H43 paper endpoint" in by_id["m7_no_widening_recorded"]["notes"]
    assert "current compiled endpoint remains D0" not in by_id["m7_no_widening_recorded"]["notes"]
