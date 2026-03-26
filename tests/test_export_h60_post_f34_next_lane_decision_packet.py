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


def test_export_h60_writes_next_lane_decision(tmp_path: Path) -> None:
    module = _load_module(
        "export_h60_post_f34_next_lane_decision_packet.py",
        "export_h60_post_f34_next_lane_decision_packet",
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
            {
                "summary": {
                    "admissible_reopen_family": "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_p43_summary = tmp_path / "p43_summary.json"
    temp_p43_summary.write_text(
        json.dumps(
            {"summary": {"merge_posture": "clean_descendant_only_never_dirty_root_main"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f35_summary = tmp_path / "f35_summary.json"
    temp_f35_summary.write_text(
        json.dumps(
            {"summary": {"current_execution_candidate_count": 0}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h59_summary_path = module.H59_SUMMARY_PATH
    original_f34_summary_path = module.F34_SUMMARY_PATH
    original_p43_summary_path = module.P43_SUMMARY_PATH
    original_f35_summary_path = module.F35_SUMMARY_PATH
    temp_out_dir = tmp_path / "H60_post_f34_next_lane_decision_packet"
    module.OUT_DIR = temp_out_dir
    module.H59_SUMMARY_PATH = temp_h59_summary
    module.F34_SUMMARY_PATH = temp_f34_summary
    module.P43_SUMMARY_PATH = temp_p43_summary
    module.F35_SUMMARY_PATH = temp_f35_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H59_SUMMARY_PATH = original_h59_summary_path
        module.F34_SUMMARY_PATH = original_f34_summary_path
        module.P43_SUMMARY_PATH = original_p43_summary_path
        module.F35_SUMMARY_PATH = original_f35_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "remain_planning_only_and_prepare_stop_or_archive"
    assert payload["summary"]["current_planning_bundle"] == "f34_post_h59_compiled_online_retrieval_reopen_screen"
    assert payload["summary"]["current_low_priority_publication_wave"] == "p44_post_h59_publication_surface_and_claim_lock"
