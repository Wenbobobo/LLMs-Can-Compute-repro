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


def test_export_h65_writes_terminal_freeze_packet_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_h65_post_p66_p67_p68_archive_first_terminal_freeze_packet.py",
        "export_h65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
    )

    summaries = {
        "h64_summary.json": {
            "selected_outcome": "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
        },
        "p66_summary.json": {
            "selected_outcome": "successor_publication_review_supports_p67_freeze"
        },
        "p67_summary.json": {
            "selected_outcome": "published_successor_freeze_locked_after_p66_review"
        },
        "p68_summary.json": {
            "selected_outcome": "published_frozen_successor_release_hygiene_and_control_rebaselined"
        },
        "f38_summary.json": {
            "selected_outcome": "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields"
        },
    }
    paths = {}
    for name, summary in summaries.items():
        path = tmp_path / name
        path.write_text(json.dumps({"summary": summary}, indent=2) + "\n", encoding="utf-8")
        paths[name] = path

    original_out_dir = module.OUT_DIR
    original_h64 = module.H64_SUMMARY_PATH
    original_p66 = module.P66_SUMMARY_PATH
    original_p67 = module.P67_SUMMARY_PATH
    original_p68 = module.P68_SUMMARY_PATH
    original_f38 = module.F38_SUMMARY_PATH
    temp_out_dir = tmp_path / "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet"
    module.OUT_DIR = temp_out_dir
    module.H64_SUMMARY_PATH = paths["h64_summary.json"]
    module.P66_SUMMARY_PATH = paths["p66_summary.json"]
    module.P67_SUMMARY_PATH = paths["p67_summary.json"]
    module.P68_SUMMARY_PATH = paths["p68_summary.json"]
    module.F38_SUMMARY_PATH = paths["f38_summary.json"]
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H64_SUMMARY_PATH = original_h64
        module.P66_SUMMARY_PATH = original_p66
        module.P67_SUMMARY_PATH = original_p67
        module.P68_SUMMARY_PATH = original_p68
        module.F38_SUMMARY_PATH = original_f38

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_first_terminal_freeze_becomes_current_active_route_and_defaults_to_explicit_stop"
    assert payload["summary"]["all_prerequisites_green"] is True
    assert payload["summary"]["default_downstream_lane"] == "explicit_archive_stop_or_hygiene_only"
