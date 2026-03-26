from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module(script_name: str, module_name: str):
    module_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p55_writes_promotion_prep_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p55_post_h63_clean_descendant_promotion_prep.py",
        "export_p55_post_h63_clean_descendant_promotion_prep",
    )

    temp_h63_summary = tmp_path / "h63_summary.json"
    temp_h63_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_p53_summary = tmp_path / "p53_summary.json"
    temp_p53_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_p54_summary = tmp_path / "p54_summary.json"
    temp_p54_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P55_post_h63_clean_descendant_promotion_prep",
            "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
        ],
    )
    temp_active_wave = _write_text(
        "active_wave_plan.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant",
        ],
    )
    temp_publication_readme = _write_text(
        "publication_readme.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P53_post_h63_paper_archive_claim_sync",
            "P55_post_h63_clean_descendant_promotion_prep",
        ],
    )
    temp_handoff = _write_text(
        "handoff.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "wip/h64-post-h63-archive-first-freeze",
        ],
    )
    temp_prompt = _write_text(
        "prompt.md",
        [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P55_post_h63_clean_descendant_promotion_prep",
            "archive_or_hygiene_stop",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_h63 = module.H63_SUMMARY_PATH
    original_p53 = module.P53_SUMMARY_PATH
    original_p54 = module.P54_SUMMARY_PATH
    original_current_branch = module.current_branch
    original_tracked_upstream = module.tracked_upstream
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_active_wave = module.ACTIVE_WAVE_PLAN_PATH
    original_publication_readme = module.PUBLICATION_README_PATH
    original_handoff = module.HANDOFF_PATH
    original_prompt = module.STARTUP_PROMPT_PATH
    temp_out_dir = tmp_path / "P55_post_h63_clean_descendant_promotion_prep"
    module.OUT_DIR = temp_out_dir
    module.H63_SUMMARY_PATH = temp_h63_summary
    module.P53_SUMMARY_PATH = temp_p53_summary
    module.P54_SUMMARY_PATH = temp_p54_summary
    module.current_branch = lambda: "wip/h64-post-h63-archive-first-freeze"
    module.tracked_upstream = lambda branch: ""
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.ACTIVE_WAVE_PLAN_PATH = temp_active_wave
    module.PUBLICATION_README_PATH = temp_publication_readme
    module.HANDOFF_PATH = temp_handoff
    module.STARTUP_PROMPT_PATH = temp_prompt
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H63_SUMMARY_PATH = original_h63
        module.P53_SUMMARY_PATH = original_p53
        module.P54_SUMMARY_PATH = original_p54
        module.current_branch = original_current_branch
        module.tracked_upstream = original_tracked_upstream
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.ACTIVE_WAVE_PLAN_PATH = original_active_wave
        module.PUBLICATION_README_PATH = original_publication_readme
        module.HANDOFF_PATH = original_handoff
        module.STARTUP_PROMPT_PATH = original_prompt

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze"
    assert payload["summary"]["merge_execution_state"] is False
