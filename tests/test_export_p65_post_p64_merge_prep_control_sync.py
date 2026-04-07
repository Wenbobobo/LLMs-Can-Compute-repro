from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p65_post_p64_merge_prep_control_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p65_post_p64_merge_prep_control_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p65_writes_successor_control_sync_summary(tmp_path: Path) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_h64_summary = _write_json(
        "h64_summary.json",
        {
            "summary": {
                "selected_outcome": "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
            }
        },
    )
    temp_p63_summary = _write_json(
        "p63_summary.json",
        {"summary": {"selected_outcome": "published_successor_promotion_prep_locked_after_p62"}},
    )
    temp_p64_summary = _write_json(
        "p64_summary.json",
        {"summary": {"selected_outcome": "published_successor_release_hygiene_rebaselined"}},
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "wip/p63-post-p62-tight-core-hygiene",
            "`archive_or_hygiene_stop`",
        ],
    )
    temp_plans_readme = _write_text(
        "plans_readme.md",
        [
            "2026-04-01-post-p63-successor-merge-prep-design.md",
            "2026-04-01-post-p65-next-planmode-handoff.md",
            "2026-04-01-post-p65-next-planmode-startup-prompt.md",
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
        ],
    )
    temp_milestones_readme = _write_text(
        "milestones_readme.md",
        [
            "P65_post_p64_merge_prep_control_sync/",
            "P64_post_p63_release_hygiene_rebaseline/",
            "P63_post_p62_published_successor_promotion_prep/",
        ],
    )
    temp_active_wave = _write_text(
        "active_wave_plan.md",
        [
            "`P65_post_p64_merge_prep_control_sync`",
            "`P64_post_p63_release_hygiene_rebaseline`",
            "`P63_post_p62_published_successor_promotion_prep`",
        ],
    )
    temp_handoff = _write_text(
        "handoff.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "wip/p63-post-p62-tight-core-hygiene",
        ],
    )
    temp_startup_prompt = _write_text(
        "startup_prompt.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "archive_or_hygiene_stop",
            "Do not reopen same-lane executor-value work",
        ],
    )
    temp_brief_prompt = _write_text(
        "brief_prompt.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P63",
            "P64",
            "P65",
            "archive_or_hygiene_stop",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_h64 = module.H64_SUMMARY_PATH
    original_p63 = module.P63_SUMMARY_PATH
    original_p64 = module.P64_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_plans_readme = module.PLANS_README_PATH
    original_milestones_readme = module.MILESTONES_README_PATH
    original_active_wave = module.ACTIVE_WAVE_PATH
    original_handoff = module.HANDOFF_PATH
    original_startup_prompt = module.STARTUP_PROMPT_PATH
    original_brief_prompt = module.BRIEF_PROMPT_PATH
    temp_out_dir = tmp_path / "P65_post_p64_merge_prep_control_sync"
    module.OUT_DIR = temp_out_dir
    module.H64_SUMMARY_PATH = temp_h64_summary
    module.P63_SUMMARY_PATH = temp_p63_summary
    module.P64_SUMMARY_PATH = temp_p64_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.PLANS_README_PATH = temp_plans_readme
    module.MILESTONES_README_PATH = temp_milestones_readme
    module.ACTIVE_WAVE_PATH = temp_active_wave
    module.HANDOFF_PATH = temp_handoff
    module.STARTUP_PROMPT_PATH = temp_startup_prompt
    module.BRIEF_PROMPT_PATH = temp_brief_prompt
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H64_SUMMARY_PATH = original_h64
        module.P63_SUMMARY_PATH = original_p63
        module.P64_SUMMARY_PATH = original_p64
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.PLANS_README_PATH = original_plans_readme
        module.MILESTONES_README_PATH = original_milestones_readme
        module.ACTIVE_WAVE_PATH = original_active_wave
        module.HANDOFF_PATH = original_handoff
        module.STARTUP_PROMPT_PATH = original_startup_prompt
        module.BRIEF_PROMPT_PATH = original_brief_prompt

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "published_successor_merge_prep_control_synced_to_h64_stack"
    assert payload["summary"]["current_published_clean_descendant_wave"] == "p63_post_p62_published_successor_promotion_prep"
    assert payload["summary"]["current_release_hygiene_rebaseline_wave"] == "p64_post_p63_release_hygiene_rebaseline"
    assert payload["summary"]["current_merge_prep_control_sync_wave"] == "p65_post_p64_merge_prep_control_sync"
    assert payload["summary"]["blocked_count"] == 0
