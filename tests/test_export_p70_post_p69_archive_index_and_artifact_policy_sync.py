from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p70_post_p69_archive_index_and_artifact_policy_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p70_post_p69_archive_index_and_artifact_policy_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p70_writes_archive_index_and_artifact_policy_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p69_summary = _write_json(
        "p69_summary.json",
        {
            "summary": {
                "selected_outcome": "repo_graph_hygiene_inventory_confirms_clean_descendant_keep_set_and_root_quarantine"
            }
        },
    )
    temp_preflight = _write_json(
        "preflight.json",
        {"summary": {"preflight_state": "docs_and_audits_green"}},
    )
    temp_p10 = _write_json(
        "p10.json",
        {"summary": {"packet_state": "archive_ready"}},
    )
    temp_plans = _write_text(
        "plans_readme.md",
        [
            "2026-04-01-post-h65-hygiene-only-cleanup-design.md",
            "2026-04-01-post-p71-next-planmode-handoff.md",
            "2026-04-01-post-p71-next-planmode-startup-prompt.md",
            "2026-04-01-post-p71-next-planmode-brief-prompt.md",
        ],
    )
    temp_publication = _write_text(
        "publication_readme.md",
        [
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "current hygiene-only cleanup stack",
            "artifact policy",
        ],
    )
    temp_packet_index = _write_text(
        "submission_packet_index.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P68_post_p67_release_hygiene_and_control_rebaseline",
            "P67_post_p66_published_successor_freeze",
            "P66_post_p65_successor_publication_review",
        ],
    )
    temp_manifest = _write_text(
        "archival_repro_manifest.md",
        [
            "results/P70_post_p69_archive_index_and_artifact_policy_sync/summary.json",
            "results/P69_post_h65_repo_graph_hygiene_inventory/summary.json",
            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
            "results/P68_post_p67_release_hygiene_and_control_rebaseline/summary.json",
            "results/P67_post_p66_published_successor_freeze/summary.json",
            "results/P66_post_p65_successor_publication_review/summary.json",
            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
            "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
            "results/H43_post_r44_useful_case_refreeze/summary.json",
        ],
    )
    temp_policy = _write_text(
        "artifact_policy.md",
        [
            "probe_read_rows.json",
            "per_read_rows.json",
            "trace_rows.json",
            "step_rows.json",
            "10 MiB",
            "surface_report.json",
            "Git LFS remains inactive by default",
            "review-critical packet",
            "runtime reopening",
            "dirty-root integration",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p69 = module.P69_SUMMARY_PATH
    original_preflight = module.PREFLIGHT_SUMMARY_PATH
    original_p10 = module.P10_SUMMARY_PATH
    original_plans = module.PLANS_README_PATH
    original_publication = module.PUBLICATION_README_PATH
    original_packet = module.SUBMISSION_PACKET_INDEX_PATH
    original_manifest = module.ARCHIVAL_MANIFEST_PATH
    original_policy = module.ARTIFACT_POLICY_PATH
    temp_out_dir = tmp_path / "P70_post_p69_archive_index_and_artifact_policy_sync"
    module.OUT_DIR = temp_out_dir
    module.P69_SUMMARY_PATH = temp_p69_summary
    module.PREFLIGHT_SUMMARY_PATH = temp_preflight
    module.P10_SUMMARY_PATH = temp_p10
    module.PLANS_README_PATH = temp_plans
    module.PUBLICATION_README_PATH = temp_publication
    module.SUBMISSION_PACKET_INDEX_PATH = temp_packet_index
    module.ARCHIVAL_MANIFEST_PATH = temp_manifest
    module.ARTIFACT_POLICY_PATH = temp_policy

    monkeypatch.setattr(module, "tracked_large_files", lambda: [])
    monkeypatch.setattr(module, "raw_row_ignore_rules_active", lambda: True)
    monkeypatch.setattr(module, "current_branch", lambda: "wip/p69-post-h65-hygiene-only-cleanup")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P69_SUMMARY_PATH = original_p69
        module.PREFLIGHT_SUMMARY_PATH = original_preflight
        module.P10_SUMMARY_PATH = original_p10
        module.PLANS_README_PATH = original_plans
        module.PUBLICATION_README_PATH = original_publication
        module.SUBMISSION_PACKET_INDEX_PATH = original_packet
        module.ARCHIVAL_MANIFEST_PATH = original_manifest
        module.ARTIFACT_POLICY_PATH = original_policy

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_indexes_and_artifact_policy_synced_to_h65_hygiene_cleanup_stack"
    assert payload["summary"]["tracked_oversize_count"] == 0
    assert payload["summary"]["blocked_count"] == 0


def test_export_p70_blocks_when_run_from_wrong_branch(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p69_summary = _write_json(
        "p69_summary.json",
        {"summary": {"selected_outcome": "repo_graph_hygiene_inventory_confirms_clean_descendant_keep_set_and_root_quarantine"}},
    )
    temp_preflight = _write_json("preflight.json", {"summary": {"preflight_state": "docs_and_audits_green"}})
    temp_p10 = _write_json("p10.json", {"summary": {"packet_state": "archive_ready"}})
    temp_plans = _write_text(
        "plans_readme.md",
        [
            "2026-04-01-post-h65-hygiene-only-cleanup-design.md",
            "2026-04-01-post-p71-next-planmode-handoff.md",
            "2026-04-01-post-p71-next-planmode-startup-prompt.md",
            "2026-04-01-post-p71-next-planmode-brief-prompt.md",
        ],
    )
    temp_publication = _write_text(
        "publication_readme.md",
        [
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "current hygiene-only cleanup stack",
            "artifact policy",
        ],
    )
    temp_packet_index = _write_text(
        "submission_packet_index.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P70_post_p69_archive_index_and_artifact_policy_sync",
            "P69_post_h65_repo_graph_hygiene_inventory",
            "P68_post_p67_release_hygiene_and_control_rebaseline",
            "P67_post_p66_published_successor_freeze",
            "P66_post_p65_successor_publication_review",
        ],
    )
    temp_manifest = _write_text(
        "archival_repro_manifest.md",
        [
            "results/P70_post_p69_archive_index_and_artifact_policy_sync/summary.json",
            "results/P69_post_h65_repo_graph_hygiene_inventory/summary.json",
            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
            "results/P68_post_p67_release_hygiene_and_control_rebaseline/summary.json",
            "results/P67_post_p66_published_successor_freeze/summary.json",
            "results/P66_post_p65_successor_publication_review/summary.json",
            "results/F38_post_h62_r63_dormant_eligibility_profile_dossier/summary.json",
            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
            "results/H58_post_r62_origin_value_boundary_closeout_packet/summary.json",
            "results/H43_post_r44_useful_case_refreeze/summary.json",
        ],
    )
    temp_policy = _write_text(
        "artifact_policy.md",
        [
            "probe_read_rows.json",
            "per_read_rows.json",
            "trace_rows.json",
            "step_rows.json",
            "10 MiB",
            "surface_report.json",
            "Git LFS remains inactive by default",
            "review-critical packet",
            "runtime reopening",
            "dirty-root integration",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p69 = module.P69_SUMMARY_PATH
    original_preflight = module.PREFLIGHT_SUMMARY_PATH
    original_p10 = module.P10_SUMMARY_PATH
    original_plans = module.PLANS_README_PATH
    original_publication = module.PUBLICATION_README_PATH
    original_packet = module.SUBMISSION_PACKET_INDEX_PATH
    original_manifest = module.ARCHIVAL_MANIFEST_PATH
    original_policy = module.ARTIFACT_POLICY_PATH
    temp_out_dir = tmp_path / "P70_post_p69_archive_index_and_artifact_policy_sync"
    module.OUT_DIR = temp_out_dir
    module.P69_SUMMARY_PATH = temp_p69_summary
    module.PREFLIGHT_SUMMARY_PATH = temp_preflight
    module.P10_SUMMARY_PATH = temp_p10
    module.PLANS_README_PATH = temp_plans
    module.PUBLICATION_README_PATH = temp_publication
    module.SUBMISSION_PACKET_INDEX_PATH = temp_packet_index
    module.ARCHIVAL_MANIFEST_PATH = temp_manifest
    module.ARTIFACT_POLICY_PATH = temp_policy

    monkeypatch.setattr(module, "tracked_large_files", lambda: [])
    monkeypatch.setattr(module, "raw_row_ignore_rules_active", lambda: True)
    monkeypatch.setattr(module, "current_branch", lambda: "wip/p66-post-p65-published-successor-freeze")
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P69_SUMMARY_PATH = original_p69
        module.PREFLIGHT_SUMMARY_PATH = original_preflight
        module.P10_SUMMARY_PATH = original_p10
        module.PLANS_README_PATH = original_plans
        module.PUBLICATION_README_PATH = original_publication
        module.SUBMISSION_PACKET_INDEX_PATH = original_packet
        module.ARCHIVAL_MANIFEST_PATH = original_manifest
        module.ARTIFACT_POLICY_PATH = original_policy

    payload = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))
    rows = {row["item_id"]: row for row in payload["rows"]}
    assert rows["p70_runs_on_current_hygiene_branch"]["status"] == "blocked"
