from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p91_post_h66_next_planmode_handoff_sync.py"
    )
    assert module_path.exists(), f"missing exporter: {module_path}"
    spec = importlib.util.spec_from_file_location(
        "export_p91_post_h66_next_planmode_handoff_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p91_writes_handoff_sync_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_h66_summary = _write_json(
        "h66_summary.json",
        {
            "summary": {
                "selected_outcome": "archive_replace_terminal_stop_becomes_current_active_route_and_defaults_to_explicit_stop"
            }
        },
    )
    temp_handoff = _write_text(
        "post_h66_handoff.md",
        [
            "H66_post_p90_archive_replace_terminal_stop_packet",
            "P91_post_h66_next_planmode_handoff_sync",
            "wip/p85-post-p84-main-rebaseline",
            "explicit stop",
            "archive polish",
            "no further action",
            "Only discuss R63 if it remains strictly non-runtime.",
            "dirty-root integration remains out of bounds",
        ],
    )
    temp_startup = _write_text(
        "post_h66_startup.md",
        [
            "H66_post_p90_archive_replace_terminal_stop_packet",
            "P91_post_h66_next_planmode_handoff_sync",
            "wip/p85-post-p84-main-rebaseline",
            "explicit stop",
            "archive polish",
            "no further action",
            "Only discuss R63 if it remains strictly non-runtime.",
        ],
    )
    temp_brief = _write_text(
        "post_h66_brief.md",
        [
            "P91_post_h66_next_planmode_handoff_sync",
            "explicit stop",
            "archive polish",
            "no further action",
            "strictly non-runtime future gate only",
        ],
    )
    temp_plans_readme = _write_text(
        "plans_readme.md",
        [
            "2026-04-07-post-h66-next-planmode-handoff.md",
            "2026-04-07-post-h66-next-planmode-startup-prompt.md",
            "2026-04-07-post-h66-next-planmode-brief-prompt.md",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_h66 = module.H66_SUMMARY_PATH
    original_handoff = module.POST_H66_HANDOFF_PATH
    original_startup = module.POST_H66_STARTUP_PATH
    original_brief = module.POST_H66_BRIEF_PATH
    original_plans = module.PLANS_README_PATH
    temp_out_dir = tmp_path / "P91_post_h66_next_planmode_handoff_sync"
    module.OUT_DIR = temp_out_dir
    module.H66_SUMMARY_PATH = temp_h66_summary
    module.POST_H66_HANDOFF_PATH = temp_handoff
    module.POST_H66_STARTUP_PATH = temp_startup
    module.POST_H66_BRIEF_PATH = temp_brief
    module.PLANS_README_PATH = temp_plans_readme
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H66_SUMMARY_PATH = original_h66
        module.POST_H66_HANDOFF_PATH = original_handoff
        module.POST_H66_STARTUP_PATH = original_startup
        module.POST_H66_BRIEF_PATH = original_brief
        module.PLANS_README_PATH = original_plans

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "next_planmode_handoff_synced_to_explicit_stop_after_h66"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["next_required_lane"] == "explicit_stop_archive_polish_or_no_further_action"
