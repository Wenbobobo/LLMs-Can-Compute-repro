from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p62_post_p61_merge_prep_control_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p62_post_p61_merge_prep_control_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p62_writes_merge_prep_control_sync_summary(tmp_path: Path) -> None:
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
    temp_p60_summary = _write_json(
        "p60_summary.json",
        {"summary": {"selected_outcome": "published_clean_descendant_promotion_prep_locked_after_p59"}},
    )
    temp_p61_summary = _write_json(
        "p61_summary.json",
        {"summary": {"selected_outcome": "published_clean_descendant_release_hygiene_rebaselined"}},
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P60_post_p59_published_clean_descendant_promotion_prep",
            "P61_post_p60_release_hygiene_rebaseline",
            "P62_post_p61_merge_prep_control_sync",
            "wip/p60-post-p59-published-clean-descendant-prep",
            "`archive_or_hygiene_stop`",
        ],
    )
    temp_plans_readme = _write_text(
        "plans_readme.md",
        [
            "2026-03-31-post-p59-published-clean-descendant-merge-prep-design.md",
            "2026-03-31-post-p62-next-planmode-handoff.md",
            "2026-03-31-post-p62-next-planmode-startup-prompt.md",
            "P60_post_p59_published_clean_descendant_promotion_prep",
            "P61_post_p60_release_hygiene_rebaseline",
            "P62_post_p61_merge_prep_control_sync",
        ],
    )
    temp_milestones_readme = _write_text(
        "milestones_readme.md",
        [
            "P62_post_p61_merge_prep_control_sync/",
            "P61_post_p60_release_hygiene_rebaseline/",
            "P60_post_p59_published_clean_descendant_promotion_prep/",
        ],
    )
    temp_active_wave = _write_text(
        "active_wave_plan.md",
        [
            "`P62_post_p61_merge_prep_control_sync`",
            "`P61_post_p60_release_hygiene_rebaseline`",
            "`P60_post_p59_published_clean_descendant_promotion_prep`",
        ],
    )
    temp_handoff = _write_text(
        "handoff.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P60_post_p59_published_clean_descendant_promotion_prep",
            "P61_post_p60_release_hygiene_rebaseline",
            "P62_post_p61_merge_prep_control_sync",
            "wip/p60-post-p59-published-clean-descendant-prep",
        ],
    )
    temp_startup_prompt = _write_text(
        "startup_prompt.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P60_post_p59_published_clean_descendant_promotion_prep",
            "P61_post_p60_release_hygiene_rebaseline",
            "P62_post_p61_merge_prep_control_sync",
            "archive_or_hygiene_stop",
            "Do not reopen same-lane executor-value work",
        ],
    )
    temp_brief_prompt = _write_text(
        "brief_prompt.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P60",
            "P61",
            "P62",
            "archive_or_hygiene_stop",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_h64 = module.H64_SUMMARY_PATH
    original_p60 = module.P60_SUMMARY_PATH
    original_p61 = module.P61_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_plans_readme = module.PLANS_README_PATH
    original_milestones_readme = module.MILESTONES_README_PATH
    original_active_wave = module.ACTIVE_WAVE_PATH
    original_handoff = module.HANDOFF_PATH
    original_startup_prompt = module.STARTUP_PROMPT_PATH
    original_brief_prompt = module.BRIEF_PROMPT_PATH
    temp_out_dir = tmp_path / "P62_post_p61_merge_prep_control_sync"
    module.OUT_DIR = temp_out_dir
    module.H64_SUMMARY_PATH = temp_h64_summary
    module.P60_SUMMARY_PATH = temp_p60_summary
    module.P61_SUMMARY_PATH = temp_p61_summary
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
        module.P60_SUMMARY_PATH = original_p60
        module.P61_SUMMARY_PATH = original_p61
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.PLANS_README_PATH = original_plans_readme
        module.MILESTONES_README_PATH = original_milestones_readme
        module.ACTIVE_WAVE_PATH = original_active_wave
        module.HANDOFF_PATH = original_handoff
        module.STARTUP_PROMPT_PATH = original_startup_prompt
        module.BRIEF_PROMPT_PATH = original_brief_prompt

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "published_clean_descendant_merge_prep_control_synced_to_h64_stack"
    assert payload["summary"]["blocked_count"] == 0
