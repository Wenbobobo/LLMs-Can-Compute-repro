from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_f28_post_h50_origin_mechanism_reentry_bundle.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_f28_post_h50_origin_mechanism_reentry_bundle",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f28_writes_mechanism_reentry_bundle(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "F28_post_h50_origin_mechanism_reentry_bundle"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "f28_post_h50_origin_mechanism_reentry_bundle"
    assert payload["summary"]["current_active_docs_only_stage"] == "h51_post_h50_origin_mechanism_reentry_packet"
    assert payload["summary"]["preserved_prior_docs_only_closeout"] == "h50_post_r51_r52_scope_decision_packet"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_routing_refreeze_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["selected_outcome"] == "post_h50_mechanism_reentry_bundle_saved"
    assert payload["summary"]["only_followup_packet"] == "h51_post_h50_origin_mechanism_reentry_packet"
    assert payload["summary"]["only_next_runtime_candidate"] == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
    assert payload["summary"]["current_low_priority_wave"] == "p37_post_h50_narrow_executor_closeout_sync"
    assert payload["summary"]["blocked_future_bundle"] == (
        "f27_post_h50_bounded_trainable_or_transformed_executor_entry_bundle"
    )
    assert payload["summary"]["next_required_lane"] == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert len(payload["summary"]["only_conditional_later_sequence"]) == 3
    assert len(payload["summary"]["blocked_future_gates"]) == 2
    assert claim_packet["distilled_result"]["only_next_runtime_candidate"] == (
        "r55_origin_2d_hardmax_retrieval_equivalence_gate"
    )
    assert len(snapshot_rows) == 8
