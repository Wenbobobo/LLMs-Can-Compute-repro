from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p67_post_p66_published_successor_freeze.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p67_post_p66_published_successor_freeze",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p67_writes_published_successor_freeze_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p66_summary = _write_json(
        "p66_summary.json",
        {"summary": {"selected_outcome": "successor_publication_review_supports_p67_freeze"}},
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P66_post_p65_successor_publication_review",
            "P67_post_p66_published_successor_freeze",
            "P68_post_p67_release_hygiene_and_control_rebaseline",
            "wip/p66-post-p65-published-successor-freeze",
        ],
    )
    temp_active_wave = _write_text(
        "active_wave_plan.md",
        [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`P66_post_p65_successor_publication_review`",
            "`P67_post_p66_published_successor_freeze`",
            "`P68_post_p67_release_hygiene_and_control_rebaseline`",
            "`wip/p66-post-p65-published-successor-freeze`",
        ],
    )
    temp_publication_readme = _write_text(
        "publication_readme.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P67_post_p66_published_successor_freeze",
            "current published frozen successor stack",
        ],
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p66-post-p65-published-successor-freeze",
            "wip/p63-post-p62-tight-core-hygiene",
            "wip/p64-post-p63-successor-stack",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p66 = module.P66_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_active = module.ACTIVE_WAVE_PLAN_PATH
    original_publication = module.PUBLICATION_README_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    temp_out_dir = tmp_path / "P67_post_p66_published_successor_freeze"
    module.OUT_DIR = temp_out_dir
    module.P66_SUMMARY_PATH = temp_p66_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.ACTIVE_WAVE_PLAN_PATH = temp_active_wave
    module.PUBLICATION_README_PATH = temp_publication_readme
    module.BRANCH_REGISTRY_PATH = temp_registry
    monkeypatch.setattr(module, "git_output", lambda args: "wip/p66-post-p65-published-successor-freeze")
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P66_SUMMARY_PATH = original_p66
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.ACTIVE_WAVE_PLAN_PATH = original_active
        module.PUBLICATION_README_PATH = original_publication
        module.BRANCH_REGISTRY_PATH = original_registry

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "published_successor_freeze_locked_after_p66_review"
    assert payload["summary"]["current_published_clean_descendant_branch"] == "wip/p66-post-p65-published-successor-freeze"
    assert payload["summary"]["blocked_count"] == 0
