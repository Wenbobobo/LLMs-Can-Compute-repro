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


def test_export_p50_writes_control_sync_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p50_post_h62_archive_first_control_sync.py",
        "export_p50_post_h62_archive_first_control_sync",
    )

    temp_h62_summary = tmp_path / "h62_summary.json"
    temp_h62_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "hygiene_first_scope_decision_keeps_archive_default_and_limits_any_reopen_to_r63_profile_gate"
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    required_files = {}
    for name in ["README.md", "STATUS.md", "publication_readme.md", "current_stage_driver.md", "active_wave_plan.md"]:
        path = tmp_path / name
        path.write_text(
            "\n".join(
                [
                    "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
                    "P50_post_h62_archive_first_control_sync",
                    "archive-first closeout",
                    "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        required_files[path] = [
            "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "P50_post_h62_archive_first_control_sync",
        ]

    original_out_dir = module.OUT_DIR
    original_h62 = module.H62_SUMMARY_PATH
    original_requirements = module.AUDITED_FILE_REQUIREMENTS
    temp_out_dir = tmp_path / "P50_post_h62_archive_first_control_sync"
    module.OUT_DIR = temp_out_dir
    module.H62_SUMMARY_PATH = temp_h62_summary
    module.AUDITED_FILE_REQUIREMENTS = required_files
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H62_SUMMARY_PATH = original_h62
        module.AUDITED_FILE_REQUIREMENTS = original_requirements

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "control_surfaces_locked_to_post_h62_archive_first_closeout"
    assert payload["summary"]["audited_file_count"] == 5
    assert payload["summary"]["locked_file_count"] == 5
