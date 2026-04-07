from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_h43_post_r44_useful_case_refreeze.py"
    spec = importlib.util.spec_from_file_location(
        "export_h43_post_r44_useful_case_refreeze",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h43_writes_useful_case_refreeze_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H43_post_r44_useful_case_refreeze"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_active_routing_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == "h42_post_r43_route_selection_packet"
    assert payload["summary"]["selected_outcome"] == "freeze_r44_as_narrow_supported_here"
    assert payload["summary"]["current_completed_useful_case_gate"] == (
        "r44_origin_restricted_wasm_useful_case_execution_gate"
    )
    assert payload["summary"]["claim_d_state"] == "supported_here_narrowly"
    assert payload["summary"]["authorized_next_runtime_candidate"] == "none"
    assert payload["summary"]["merge_executed"] is False
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert len(snapshot_rows) == 5
