from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h50_post_r51_r52_scope_decision_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h50_post_r51_r52_scope_decision_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h50_writes_scope_decision_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H50_post_r51_r52_scope_decision_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h50_post_r51_r52_scope_decision_packet"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == (
        "h49_post_r50_tinyc_lowering_decision_packet"
    )
    assert payload["summary"]["current_active_routing_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_completed_post_h49_runtime_gate"] == (
        "r51_origin_memory_control_surface_sufficiency_gate"
    )
    assert payload["summary"]["current_completed_post_h49_comparator_gate"] == (
        "r52_origin_internal_vs_external_executor_value_gate"
    )
    assert payload["summary"]["selected_outcome"] == "stop_as_exact_without_system_value"
    assert payload["summary"]["future_bundle_state"] == "f27_saved_but_blocked_after_negative_h50"
    assert payload["summary"]["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["selected_outcome"] == "stop_as_exact_without_system_value"
    assert len(snapshot_rows) == 3
