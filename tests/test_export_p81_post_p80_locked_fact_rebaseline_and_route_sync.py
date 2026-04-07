from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p81_post_p80_locked_fact_rebaseline_and_route_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p81_post_p80_locked_fact_rebaseline_and_route_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p81_writes_locked_fact_rebaseline_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p80_summary = _write_json(
        "p80_summary.json",
        {"summary": {"selected_outcome": "next_planmode_handoff_synced_to_explicit_stop_after_p79"}},
    )
    temp_preflight = _write_json("preflight_summary.json", {"summary": {"preflight_state": "docs_and_audits_green"}})
    temp_p10 = _write_json("p10_summary.json", {"summary": {"packet_state": "archive_ready"}})
    temp_readme = _write_text(
        "README.md",
        [
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "wip/p81-post-p80-clean-descendant-promotion-prep",
            "wip/p75-post-p74-published-successor-freeze",
            "53962ca",
        ],
    )
    temp_status = _write_text(
        "STATUS.md",
        [
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "wip/p81-post-p80-clean-descendant-promotion-prep",
            "wip/p75-post-p74-published-successor-freeze",
            "docs_and_audits_green",
            "archive_ready",
        ],
    )
    temp_docs = _write_text(
        "docs_readme.md",
        ["H65 + P81 + P77/P78/P79/P80", "publication_record/current_stage_driver.md", "branch_worktree_registry.md"],
    )
    temp_publication = _write_text(
        "publication_readme.md",
        [
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "wip/p81-post-p80-clean-descendant-promotion-prep",
            "2026-04-07-post-p80-clean-descendant-promotion-prep-design.md",
        ],
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "wip/p81-post-p80-clean-descendant-promotion-prep",
            "wip/p75-post-p74-published-successor-freeze",
            "53962ca",
            "docs_and_audits_green",
            "archive_ready",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )
    temp_registry = _write_text(
        "branch_registry.md",
        [
            "wip/p81-post-p80-clean-descendant-promotion-prep",
            "wip/p75-post-p74-published-successor-freeze",
            "p81`, `p75`, `p74`, `p73`, `p72`, `p69`, and `p56",
            "clean_descendant_only_never_dirty_root_main",
            "origin/main...wip/p81-post-p80-clean-descendant-promotion-prep",
        ],
    )
    temp_plans = _write_text(
        "plans_readme.md",
        [
            "2026-04-07-post-p80-clean-descendant-promotion-prep-design.md",
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "wip/p81-post-p80-clean-descendant-promotion-prep",
        ],
    )
    temp_milestones = _write_text(
        "milestones_readme.md",
        [
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "P77_post_p76_keep_set_and_provenance_normalization",
            "P81",
        ],
    )
    temp_design = _write_text(
        "plan_design.md",
        [
            "P81_post_p80_locked_fact_rebaseline_and_route_sync",
            "P82_post_p81_clean_main_promotion_probe",
            "P83_post_p82_promotion_branch_and_pr_handoff",
            "P84_post_p83_keep_set_contraction_and_closeout",
        ],
    )
    temp_handoff = _write_text(
        "post_p80_handoff.md",
        [
            "wip/p75-post-p74-published-successor-freeze",
            "53962ca",
            "docs_and_audits_green",
            "archive_ready",
            "explicit stop",
            "no further action",
        ],
    )
    temp_startup = _write_text(
        "post_p80_startup.md",
        [
            "wip/p75-post-p74-published-successor-freeze",
            "53962ca",
            "docs_and_audits_green",
            "archive_ready",
            "explicit stop",
            "no further action",
        ],
    )
    temp_brief = _write_text(
        "post_p80_brief.md",
        [
            "wip/p75-post-p74-published-successor-freeze",
            "53962ca",
            "docs_and_audits_green",
            "archive_ready",
            "explicit stop",
            "no further action",
        ],
    )

    original_values = {
        "OUT_DIR": module.OUT_DIR,
        "P80_SUMMARY_PATH": module.P80_SUMMARY_PATH,
        "PREFLIGHT_SUMMARY_PATH": module.PREFLIGHT_SUMMARY_PATH,
        "P10_SUMMARY_PATH": module.P10_SUMMARY_PATH,
        "ROOT_README_PATH": module.ROOT_README_PATH,
        "STATUS_PATH": module.STATUS_PATH,
        "DOCS_README_PATH": module.DOCS_README_PATH,
        "PUBLICATION_README_PATH": module.PUBLICATION_README_PATH,
        "CURRENT_STAGE_DRIVER_PATH": module.CURRENT_STAGE_DRIVER_PATH,
        "BRANCH_REGISTRY_PATH": module.BRANCH_REGISTRY_PATH,
        "PLANS_README_PATH": module.PLANS_README_PATH,
        "MILESTONES_README_PATH": module.MILESTONES_README_PATH,
        "PLAN_DESIGN_PATH": module.PLAN_DESIGN_PATH,
        "POST_P80_HANDOFF_PATH": module.POST_P80_HANDOFF_PATH,
        "POST_P80_STARTUP_PATH": module.POST_P80_STARTUP_PATH,
        "POST_P80_BRIEF_PATH": module.POST_P80_BRIEF_PATH,
    }
    module.OUT_DIR = tmp_path / "P81_post_p80_locked_fact_rebaseline_and_route_sync"
    module.P80_SUMMARY_PATH = temp_p80_summary
    module.PREFLIGHT_SUMMARY_PATH = temp_preflight
    module.P10_SUMMARY_PATH = temp_p10
    module.ROOT_README_PATH = temp_readme
    module.STATUS_PATH = temp_status
    module.DOCS_README_PATH = temp_docs
    module.PUBLICATION_README_PATH = temp_publication
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.BRANCH_REGISTRY_PATH = temp_registry
    module.PLANS_README_PATH = temp_plans
    module.MILESTONES_README_PATH = temp_milestones
    module.PLAN_DESIGN_PATH = temp_design
    module.POST_P80_HANDOFF_PATH = temp_handoff
    module.POST_P80_STARTUP_PATH = temp_startup
    module.POST_P80_BRIEF_PATH = temp_brief

    monkeypatch.setattr(module, "current_branch", lambda: "wip/p81-post-p80-clean-descendant-promotion-prep")
    monkeypatch.setattr(module, "branch_head", lambda branch: "53962ca")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        for key, value in original_values.items():
            setattr(module, key, value)

    payload = json.loads((module.OUT_DIR / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "locked_facts_rebaselined_and_route_synced_after_p80"
    assert payload["summary"]["published_branch_head"] == "53962ca"
    assert payload["summary"]["blocked_count"] == 0
