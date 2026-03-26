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


def test_export_f35_writes_far_future_horizon_log(tmp_path: Path) -> None:
    module = _load_module(
        "export_f35_post_h59_far_future_model_and_weights_horizon_log.py",
        "export_f35_post_h59_far_future_model_and_weights_horizon_log",
    )

    temp_h59_summary = tmp_path / "h59_summary.json"
    temp_h59_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f34_summary = tmp_path / "f34_summary.json"
    temp_f34_summary.write_text(
        json.dumps(
            {"summary": {"later_authorization_gate": "no_runtime_lane_open_until_later_explicit_authorization"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h59_summary_path = module.H59_SUMMARY_PATH
    original_f34_summary_path = module.F34_SUMMARY_PATH
    temp_out_dir = tmp_path / "F35_post_h59_far_future_model_and_weights_horizon_log"
    module.OUT_DIR = temp_out_dir
    module.H59_SUMMARY_PATH = temp_h59_summary
    module.F34_SUMMARY_PATH = temp_f34_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H59_SUMMARY_PATH = original_h59_summary_path
        module.F34_SUMMARY_PATH = original_f34_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["high_cost_model_route_status"] == "high_cost_model_route_far_future_only"
    assert payload["summary"]["programs_into_weights_route_status"] == "programs_into_weights_route_far_future_only"
    assert payload["summary"]["current_execution_candidate_count"] == 0
