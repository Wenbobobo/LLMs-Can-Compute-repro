from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p4_blog_release_gate.py"
    spec = importlib.util.spec_from_file_location("export_p4_blog_release_gate", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_has_required_gitignore_entries_requires_origin_variants_and_tmp() -> None:
    module = _load_export_module()

    ok, missing = module.has_required_gitignore_entries("docs/Origin/\ndocs/origin/\ntmp/\n")

    assert ok is True
    assert missing == []


def test_blog_outline_is_downstream_accepts_explicit_no_go_wording() -> None:
    module = _load_export_module()

    assert (
        module.blog_outline_is_downstream(
            "Status: currently blocked by the M7/P4 outcome. Broader blog prose should wait until a future scope reopening clears both the systems and public-release gates."
        )
        is True
    )


def test_build_release_checklist_keeps_blog_blocked_on_current_results() -> None:
    module = _load_export_module()

    inputs = module.load_release_inputs()
    rows = module.build_release_checklist(
        p3_summary=inputs["p3_summary"],
        m7_decision=inputs["m7_decision"],
        artifact_release_ledger=inputs["artifact_release_ledger"],
        gitignore_text=inputs["gitignore_text"],
        readme_text=inputs["readme_text"],
        blog_outline_text=inputs["blog_outline_text"],
    )

    by_id = {row["item_id"]: row for row in rows}
    assert by_id["paper_scope_frozen"]["status"] == "pass"
    assert by_id["frontend_scope_decided"]["status"] == "pass"
    assert by_id["blog_release_authorized"]["status"] == "blocked"


def test_build_summary_reports_readme_only_release_state() -> None:
    module = _load_export_module()

    inputs = module.load_release_inputs()
    checklist_rows = module.build_release_checklist(
        p3_summary=inputs["p3_summary"],
        m7_decision=inputs["m7_decision"],
        artifact_release_ledger=inputs["artifact_release_ledger"],
        gitignore_text=inputs["gitignore_text"],
        readme_text=inputs["readme_text"],
        blog_outline_text=inputs["blog_outline_text"],
    )
    claim_rows = module.build_claim_artifact_audit(
        p3_unsupported_claims=inputs["p3_unsupported_claims"],
        m7_decision=inputs["m7_decision"],
    )
    summary = module.build_summary(
        checklist_rows=checklist_rows,
        claim_audit_rows=claim_rows,
        m7_decision=inputs["m7_decision"],
    )

    assert summary["release_status"] == "blog_blocked_readme_only"
    assert summary["blog_authorized"] is False
    assert summary["readme_posture"] == "restrained_research_landing_page_allowed"
