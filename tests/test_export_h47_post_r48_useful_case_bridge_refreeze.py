from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_h47_post_r48_useful_case_bridge_refreeze.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h47_post_r48_useful_case_bridge_refreeze",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h47_writes_useful_case_bridge_refreeze_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H47_post_r48_useful_case_bridge_refreeze"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h47_post_r48_useful_case_bridge_refreeze"
    assert payload["summary"]["current_active_routing_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == (
        "h46_post_r47_frontend_bridge_decision_packet"
    )
    assert payload["summary"]["preserved_route_reauthorization_packet"] == (
        "h44_post_h43_route_reauthorization_packet"
    )
    assert payload["summary"]["current_exact_first_planning_bundle"] == (
        "f21_post_h43_exact_useful_case_expansion_bundle"
    )
    assert payload["summary"]["current_comparator_planning_bundle"] == (
        "f22_post_r46_useful_case_model_bridge_bundle"
    )
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["selected_outcome"] == "freeze_r48_as_narrow_comparator_support_only"
    assert payload["summary"]["current_completed_post_h44_exact_runtime_gate"] == (
        "r46_origin_useful_case_surface_generalization_gate"
    )
    assert payload["summary"]["current_completed_exact_frontend_bridge_gate"] == (
        "r47_origin_restricted_frontend_translation_gate"
    )
    assert payload["summary"]["current_completed_comparator_only_useful_case_model_gate"] == (
        "r48_origin_dual_mode_useful_case_model_gate"
    )
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert len(snapshot_rows) == 7
