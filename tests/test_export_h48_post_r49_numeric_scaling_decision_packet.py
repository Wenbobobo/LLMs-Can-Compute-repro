from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h48_post_r49_numeric_scaling_decision_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h48_post_r49_numeric_scaling_decision_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h48_writes_numeric_scaling_decision_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H48_post_r49_numeric_scaling_decision_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h48_post_r49_numeric_scaling_decision_packet"
    assert payload["summary"]["current_active_routing_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == (
        "h47_post_r48_useful_case_bridge_refreeze"
    )
    assert payload["summary"]["current_exact_first_planning_bundle"] == "f23_post_h47_numeric_scaling_bundle"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["selected_outcome"] == "authorize_f25_restricted_tinyc_lowering_bundle"
    assert payload["summary"]["current_completed_numeric_scaling_gate"] == (
        "r49_origin_useful_case_numeric_scaling_gate"
    )
    assert payload["summary"]["authorized_next_planning_bundle"] == (
        "f25_post_h48_restricted_tinyc_lowering_bundle"
    )
    assert payload["summary"]["non_selected_closeout_bundle"] == (
        "p36_post_h48_falsification_closeout_bundle"
    )
    assert payload["summary"]["current_low_priority_wave"] == "p35_post_h47_research_record_rollup"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["next_required_lane"] == "f25_post_h48_restricted_tinyc_lowering_bundle"
    assert claim_packet["distilled_result"]["next_required_lane"] == (
        "f25_post_h48_restricted_tinyc_lowering_bundle"
    )
    assert len(snapshot_rows) == 7
