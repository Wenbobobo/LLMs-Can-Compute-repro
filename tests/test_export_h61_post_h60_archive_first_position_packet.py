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


def test_export_h61_writes_archive_first_position_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_h61_post_h60_archive_first_position_packet.py",
        "export_h61_post_h60_archive_first_position_packet",
    )

    temp_h60_summary = tmp_path / "h60_summary.json"
    temp_h60_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "remain_planning_only_and_prepare_stop_or_archive"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_p45_summary = tmp_path / "p45_summary.json"
    temp_p45_summary.write_text(
        json.dumps(
            {"summary": {"merge_posture": "clean_descendant_only_never_dirty_root_main"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f36_summary = tmp_path / "f36_summary.json"
    temp_f36_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "compiled_online_route_qualified_on_paper_only_with_strict_preruntime_gates",
                    "admissible_reopen_family": "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route",
                }
            },
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
    original_h60_summary_path = module.H60_SUMMARY_PATH
    original_p45_summary_path = module.P45_SUMMARY_PATH
    original_f36_summary_path = module.F36_SUMMARY_PATH
    original_f35_summary_path = module.F35_SUMMARY_PATH
    temp_out_dir = tmp_path / "H61_post_h60_archive_first_position_packet"
    module.OUT_DIR = temp_out_dir
    module.H60_SUMMARY_PATH = temp_h60_summary
    module.P45_SUMMARY_PATH = temp_p45_summary
    module.F36_SUMMARY_PATH = temp_f36_summary
    module.F35_SUMMARY_PATH = temp_f35_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H60_SUMMARY_PATH = original_h60_summary_path
        module.P45_SUMMARY_PATH = original_p45_summary_path
        module.F36_SUMMARY_PATH = original_f36_summary_path
        module.F35_SUMMARY_PATH = original_f35_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_first_consolidation_becomes_default_posture"
    assert payload["summary"]["preserved_prior_active_packet"] == "h60_post_f34_next_lane_decision_packet"
    assert payload["summary"]["current_reopen_family_on_paper"] == "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"
