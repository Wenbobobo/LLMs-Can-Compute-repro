from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h66_post_p90_archive_replace_terminal_stop_packet.py"
    )
    assert module_path.exists(), f"missing exporter: {module_path}"
    spec = importlib.util.spec_from_file_location(
        "export_h66_post_p90_archive_replace_terminal_stop_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h66_writes_terminal_stop_packet_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    h65_summary = tmp_path / "h65_summary.json"
    h65_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop"
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    p90_summary = tmp_path / "p90_summary.json"
    p90_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "archive_replace_screen_completed_with_no_additional_salvage_after_p89",
                    "file_specific_salvage_required_count": 0,
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    temp_out_dir = tmp_path / "results" / "H66_post_p90_archive_replace_terminal_stop_packet"
    original_out_dir = module.OUT_DIR
    original_h65 = module.H65_SUMMARY_PATH
    original_p90 = module.P90_SUMMARY_PATH
    module.OUT_DIR = temp_out_dir
    module.H65_SUMMARY_PATH = h65_summary
    module.P90_SUMMARY_PATH = p90_summary
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H65_SUMMARY_PATH = original_h65
        module.P90_SUMMARY_PATH = original_p90

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_replace_terminal_stop_becomes_current_active_route_and_defaults_to_explicit_stop"
    assert payload["summary"]["all_prerequisites_green"] is True
    assert payload["summary"]["default_downstream_lane"] == "explicit_stop_or_no_further_action_archive_first"
    assert payload["summary"]["runtime_authorization"] == "closed"
