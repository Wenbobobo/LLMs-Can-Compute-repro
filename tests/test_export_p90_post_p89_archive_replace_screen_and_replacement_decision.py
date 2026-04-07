from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p90_post_p89_archive_replace_screen_and_replacement_decision.py"
    )
    assert module_path.exists(), f"missing exporter: {module_path}"
    spec = importlib.util.spec_from_file_location(
        "export_p90_post_p89_archive_replace_screen_and_replacement_decision",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p90_writes_archive_replace_screen_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    temp_p89 = tmp_path / "p89_summary.json"
    temp_p89.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "docs_consolidation_and_live_router_sync_after_p88",
                    "blocked_count": 0,
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    docs = {
        "README.md": "\n".join(
            [
                "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                "P90_post_p89_archive_replace_screen_and_replacement_decision",
                "archive-then-replace closeout",
                "H66_post_p90_archive_replace_terminal_stop_packet",
            ]
        ),
        "STATUS.md": "\n".join(
            [
                "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                "P90_post_p89_archive_replace_screen_and_replacement_decision",
                "archive-then-replace closeout",
                "file-specific salvage case",
            ]
        ),
        "docs/README.md": "\n".join(
            [
                "H65 + P90 + P89 + P88 + P87 + P86 + P85",
                "publication_record/current_stage_driver.md",
                "branch_worktree_registry.md",
                "plans/README.md",
            ]
        ),
        "docs/plans/README.md": "\n".join(
            [
                "P90",
                "current archive-replace decision wave",
                "current clean rebaseline branch",
                "wip/p85-post-p84-main-rebaseline",
            ]
        ),
        "docs/milestones/README.md": "\n".join(
            [
                "P90_post_p89_archive_replace_screen_and_replacement_decision",
                "P89_post_p88_docs_consolidation_and_live_router_sync",
                "P88_post_p87_salvage_screen_and_no_import_decision",
            ]
        ),
        "docs/publication_record/README.md": "\n".join(
            [
                "P90_post_p89_archive_replace_screen_and_replacement_decision",
                "root_salvage_shortlist.md",
                "current_stage_driver.md",
                "archival_repro_manifest.md",
            ]
        ),
        "docs/publication_record/current_stage_driver.md": "\n".join(
            [
                "P90_post_p89_archive_replace_screen_and_replacement_decision",
                "archive-then-replace closeout",
                "H66_post_p90_archive_replace_terminal_stop_packet",
                "file-specific salvage case",
            ]
        ),
        "docs/publication_record/root_salvage_shortlist.md": "\n".join(
            [
                "Keep Clean And Archive Root Only",
                "docs/publication_record/archival_repro_manifest.md",
                "docs/publication_record/release_candidate_checklist.md",
                "docs/publication_record/release_preflight_checklist.md",
                "docs/publication_record/submission_candidate_criteria.md",
                "docs/publication_record/submission_packet_index.md",
                "docs/publication_record/experiment_manifest.md",
            ]
        ),
        "docs/publication_record/archival_repro_manifest.md": "\n".join(
            [
                "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
                "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
                "Preserved immediate publication lineage",
            ]
        ),
        "docs/publication_record/release_candidate_checklist.md": "\n".join(
            [
                "`H65/P56/P57/P58/P59/P77/P78/P79/P80/F38`",
                "preserved `H64/H58/H43`",
            ]
        ),
        "docs/publication_record/release_preflight_checklist.md": "\n".join(
            [
                "`H65/P77/P78/P79/P80`",
                "`P72` hygiene-only archive-polish and explicit-stop handoff sidecar",
            ]
        ),
        "docs/publication_record/submission_candidate_criteria.md": "\n".join(
            [
                "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
                "`H58_post_r62_origin_value_boundary_closeout_packet`",
                "`H43_post_r44_useful_case_refreeze`",
            ]
        ),
        "docs/publication_record/submission_packet_index.md": "\n".join(
            [
                "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
                "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
                "do not widen the paper-facing evidence bundle",
            ]
        ),
        "docs/publication_record/experiment_manifest.md": "\n".join(
            [
                "| 2026-03-26 | post-`H63` archive-first freeze wave |",
                "| 2026-03-26 | post-`H62` archive-first closeout wave |",
                "| 2026-03-26 | post-`H61` hygiene-first reauthorization prep |",
            ]
        ),
    }
    for relative, body in docs.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body + "\n", encoding="utf-8")

    dirty_root = tmp_path / "dirty_root"
    dirty_docs = {
        "docs/publication_record/archival_repro_manifest.md": "\n".join(
            [
                "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
                "results/P50_post_h62_archive_first_control_sync/summary.json",
            ]
        ),
        "docs/publication_record/release_candidate_checklist.md": "\n".join(
            [
                "State: `standing_gate`",
                "current `H25` active / `H23` frozen stack",
            ]
        ),
        "docs/publication_record/release_preflight_checklist.md": "\n".join(
            [
                "current active `H25` decision packet",
                "current frozen `H23` scientific state",
            ]
        ),
        "docs/publication_record/submission_candidate_criteria.md": "\n".join(
            [
                "current active `H25` routing",
                "frozen `H23` evidence",
            ]
        ),
        "docs/publication_record/submission_packet_index.md": "\n".join(
            [
                "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
                "P50_post_h62_archive_first_control_sync",
            ]
        ),
        "docs/publication_record/experiment_manifest.md": "\n".join(
            [
                "| 2026-03-25 | post-`H58` reproduction-gap, dossier, and guarded future-planning wave |",
                "| 2026-03-25 | post-`H56` final native useful-kernel value discriminator closeout wave |",
            ]
        ),
    }
    for relative, body in dirty_docs.items():
        path = dirty_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body + "\n", encoding="utf-8")

    temp_out_dir = tmp_path / "results" / "P90_post_p89_archive_replace_screen_and_replacement_decision"
    original_out_dir = module.OUT_DIR
    original_root = module.ROOT
    original_p89_path = module.P89_SUMMARY_PATH
    original_dirty_root = module.DIRTY_ROOT
    module.OUT_DIR = temp_out_dir
    module.ROOT = tmp_path
    module.P89_SUMMARY_PATH = temp_p89
    module.DIRTY_ROOT = dirty_root

    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.ROOT = original_root
        module.P89_SUMMARY_PATH = original_p89_path
        module.DIRTY_ROOT = original_dirty_root

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_replace_screen_completed_with_no_additional_salvage_after_p89"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["screened_now_count"] == 6
    assert payload["summary"]["keep_clean_replace_root_count"] == 6
    assert payload["summary"]["file_specific_salvage_required_count"] == 0
    assert payload["summary"]["next_recommended_route"] == "h66_archive_replace_terminal_stop_packet"
