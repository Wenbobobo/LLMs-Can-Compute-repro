from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p36_post_h49_cleanline_hygiene_and_artifact_policy.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p36_post_h49_cleanline_hygiene_and_artifact_policy",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p36_writes_cleanline_hygiene_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P36_post_h49_cleanline_hygiene_and_artifact_policy"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["current_active_stage"] == "h49_post_r50_tinyc_lowering_decision_packet"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["refresh_packet"] == "p36_post_h49_cleanline_hygiene_and_artifact_policy"
    assert payload["summary"]["selected_outcome"] == "cleanline_hygiene_saved_without_scientific_widening"
    assert payload["summary"]["current_low_priority_wave"] == "p36_post_h49_cleanline_hygiene_and_artifact_policy"
    assert payload["summary"]["preserved_prior_low_priority_wave"] == "p35_post_h47_research_record_rollup"
    assert payload["summary"]["current_post_h49_planning_bundle"] == "f26_post_h49_origin_claim_delta_and_next_question_bundle"
    assert payload["summary"]["current_merge_posture"] == "explicit_merge_wave"
    assert payload["summary"]["merge_executed"] is False
    assert payload["summary"]["root_dirty_main_quarantined"] is True
    assert payload["summary"]["large_artifact_default_policy"] == "raw_probe_rows_out_of_git"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["next_required_lane"] == "r51_origin_memory_control_surface_sufficiency_gate"
    assert len(snapshot_rows) == 8
