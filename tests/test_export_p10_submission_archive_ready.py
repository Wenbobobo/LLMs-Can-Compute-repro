from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p10_submission_archive_ready.py"
    spec = importlib.util.spec_from_file_location("export_p10_submission_archive_ready", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_extract_matching_lines_returns_unique_hits_in_order() -> None:
    module = _load_export_module()

    lines = module.extract_matching_lines(
        "alpha\nbeta submission_packet_index.md\ngamma submission_packet_index.md\n",
        needles=["submission_packet_index.md"],
    )

    assert lines == ["beta submission_packet_index.md", "gamma submission_packet_index.md"]


def test_contains_none_detects_restricted_source_markers() -> None:
    module = _load_export_module()

    assert module.contains_none("public-safe packet\nreview boundary summary\n", ["docs/origin/", "docs/Origin/"]) is True
    assert module.contains_none("packet\nmentions docs/origin/\n", ["docs/origin/"]) is False


def test_build_checklist_rows_accept_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_archive_ready_packet() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs["worktree_hygiene_summary"])

    assert summary["current_paper_phase"] == "h52_current_control_with_h43_paper_endpoint"
    assert summary["packet_state"] == "archive_ready"
    assert summary["release_commit_state"] in {
        "dirty_worktree_release_commit_blocked",
        "clean_worktree_ready_if_other_gates_green",
    }
    assert summary["git_diff_check_state"] in {"clean", "warnings_only"}
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "use submission_packet_index.md plus archival_repro_manifest.md as the canonical handoff while H52 remains the current docs-only mechanism closeout packet, preserve H50 as the broader-route value closeout, preserve H51 as the prior mechanism-reentry packet, preserve H43 as the paper-grade endpoint, keep R55/R56 as exact mechanism evidence, keep R57 as negative fast-path comparator evidence, preserve H36 as the routing/refreeze packet, keep R42/R43/R44/R45 as the completed semantic-boundary gate stack, preserve P28 as publication alignment to H43, preserve P27/P37 as operational release-control context, and keep no_active_downstream_runtime_lane as the current follow-on state"
    )


def test_preflight_state_reader_reports_green_state() -> None:
    module = _load_export_module()

    summary_doc = {
        "summary": {
            "preflight_state": "docs_and_audits_green",
        }
    }

    assert module.preflight_state_from_summary(summary_doc) == "docs_and_audits_green"


def test_worktree_state_readers_extract_release_hygiene_fields() -> None:
    module = _load_export_module()

    summary_doc = {
        "summary": {
            "release_commit_state": "dirty_worktree_release_commit_blocked",
            "git_diff_check_state": "warnings_only",
        }
    }

    assert module.release_commit_state_from_summary(summary_doc) == "dirty_worktree_release_commit_blocked"
    assert module.diff_check_state_from_summary(summary_doc) == "warnings_only"
