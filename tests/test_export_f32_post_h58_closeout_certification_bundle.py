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


def test_export_f32_writes_closeout_certification_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_f32_post_h58_closeout_certification_bundle.py",
        "export_f32_post_h58_closeout_certification_bundle",
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

    original_out_dir = module.OUT_DIR
    original_h58_summary_path = module.H58_SUMMARY_PATH
    temp_out_dir = tmp_path / "F32_post_h58_closeout_certification_bundle"
    module.OUT_DIR = temp_out_dir
    module.H58_SUMMARY_PATH = temp_h58_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H58_SUMMARY_PATH = original_h58_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["planning_bundle"] == "f32_post_h58_closeout_certification_bundle"
    assert payload["summary"]["certified_stop"] == "same_lane_reopen_not_admissible_without_new_cost_structure"
    assert payload["summary"]["next_docs_only_packet"] == "h59_post_h58_reproduction_gap_decision_packet"
