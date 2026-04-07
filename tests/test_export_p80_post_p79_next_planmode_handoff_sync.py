from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p80_post_p79_next_planmode_handoff_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p80_post_p79_next_planmode_handoff_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p80_writes_handoff_sync_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p79_summary = _write_json(
        "p79_summary.json",
        {"summary": {"selected_outcome": "archive_claim_boundary_and_reopen_screen_locked_after_convergence"}},
    )
    temp_handoff = _write_text(
        "post_p80_handoff.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P80_post_p79_next_planmode_handoff_sync",
            "wip/p75-post-p74-published-successor-freeze",
            "explicit stop",
            "no further action",
            "only future gate remains strictly non-runtime",
            "dirty-root integration remains out of bounds",
        ],
    )
    temp_startup = _write_text(
        "post_p80_startup.md",
        [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "P80_post_p79_next_planmode_handoff_sync",
            "wip/p75-post-p74-published-successor-freeze",
            "explicit stop",
            "no further action",
            "Only discuss R63 if it remains strictly non-runtime.",
        ],
    )
    temp_brief = _write_text(
        "post_p80_brief.md",
        [
            "P80_post_p79_next_planmode_handoff_sync",
            "explicit stop",
            "no further action",
            "strictly non-runtime future gate only",
        ],
    )
    temp_plans_readme = _write_text(
        "plans_readme.md",
        [
            "2026-04-05-post-p80-next-planmode-handoff.md",
            "2026-04-05-post-p80-next-planmode-startup-prompt.md",
            "2026-04-05-post-p80-next-planmode-brief-prompt.md",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p79 = module.P79_SUMMARY_PATH
    original_handoff = module.POST_P80_HANDOFF_PATH
    original_startup = module.POST_P80_STARTUP_PATH
    original_brief = module.POST_P80_BRIEF_PATH
    original_plans = module.PLANS_README_PATH
    temp_out_dir = tmp_path / "P80_post_p79_next_planmode_handoff_sync"
    module.OUT_DIR = temp_out_dir
    module.P79_SUMMARY_PATH = temp_p79_summary
    module.POST_P80_HANDOFF_PATH = temp_handoff
    module.POST_P80_STARTUP_PATH = temp_startup
    module.POST_P80_BRIEF_PATH = temp_brief
    module.PLANS_README_PATH = temp_plans_readme
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P79_SUMMARY_PATH = original_p79
        module.POST_P80_HANDOFF_PATH = original_handoff
        module.POST_P80_STARTUP_PATH = original_startup
        module.POST_P80_BRIEF_PATH = original_brief
        module.PLANS_README_PATH = original_plans

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "next_planmode_handoff_synced_to_explicit_stop_after_p79"
    assert payload["summary"]["blocked_count"] == 0
