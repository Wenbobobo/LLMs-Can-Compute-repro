from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_f26_post_h49_origin_claim_delta_and_next_question_bundle.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_f26_post_h49_origin_claim_delta_and_next_question_bundle",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f26_writes_claim_delta_bundle(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "F26_post_h49_origin_claim_delta_and_next_question_bundle"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "f26_post_h49_origin_claim_delta_and_next_question_bundle"
    assert payload["summary"]["current_active_docs_only_stage"] == "h49_post_r50_tinyc_lowering_decision_packet"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_routing_refreeze_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["selected_outcome"] == "post_h49_claim_delta_bundle_saved"
    assert payload["summary"]["only_next_runtime_candidate"] == "r51_origin_memory_control_surface_sufficiency_gate"
    assert payload["summary"]["only_followup_comparator_gate"] == "r52_origin_internal_vs_external_executor_value_gate"
    assert payload["summary"]["only_followup_packet"] == "h50_post_r51_r52_scope_decision_packet"
    assert payload["summary"]["saved_future_bundle"] == "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle"
    assert payload["summary"]["current_low_priority_wave"] == "p36_post_h49_cleanline_hygiene_and_artifact_policy"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["next_required_lane"] == "r51_origin_memory_control_surface_sufficiency_gate"
    assert len(snapshot_rows) == 8
