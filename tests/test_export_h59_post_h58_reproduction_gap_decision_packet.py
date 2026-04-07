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


def test_export_h59_writes_reproduction_gap_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_h59_post_h58_reproduction_gap_decision_packet.py",
        "export_h59_post_h58_reproduction_gap_decision_packet",
    )

    temp_h58_summary = tmp_path / "h58_summary.json"
    temp_h58_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "stop_as_mechanism_supported_but_no_bounded_executor_value",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f32_summary = tmp_path / "f32_summary.json"
    temp_f32_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "certified_stop": "same_lane_reopen_not_admissible_without_new_cost_structure",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h58_summary_path = module.H58_SUMMARY_PATH
    original_f32_summary_path = module.F32_SUMMARY_PATH
    temp_out_dir = tmp_path / "H59_post_h58_reproduction_gap_decision_packet"
    module.OUT_DIR = temp_out_dir
    module.H58_SUMMARY_PATH = temp_h58_summary
    module.F32_SUMMARY_PATH = temp_f32_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H58_SUMMARY_PATH = original_h58_summary_path
        module.F32_SUMMARY_PATH = original_f32_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["active_stage"] == "h59_post_h58_reproduction_gap_decision_packet"
    assert payload["summary"]["selected_outcome"] == (
        "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen"
    )
    assert payload["summary"]["current_downstream_scientific_lane"] == "planning_only_or_project_stop"
