from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_h41_post_r42_aggressive_long_arc_decision_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h41_post_r42_aggressive_long_arc_decision_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h41_writes_aggressive_long_arc_decision_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H41_post_r42_aggressive_long_arc_decision_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h41_post_r42_aggressive_long_arc_decision_packet"
    assert payload["summary"]["current_active_routing_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == (
        "h40_post_h38_semantic_boundary_activation_packet"
    )
    assert payload["summary"]["current_model_mainline_bundle"] == "f20_post_r42_dual_mode_model_mainline_bundle"
    assert payload["summary"]["selected_outcome"] == "authorize_r43_exact_mainline_and_coequal_r45_model_lane"
    assert payload["summary"]["authorized_exact_runtime_candidate"] == (
        "r43_origin_bounded_memory_small_vm_execution_gate"
    )
    assert payload["summary"]["authorized_model_runtime_candidate"] == "r45_origin_dual_mode_model_mainline_gate"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["explicit_merge_packet"] == (
        "p27_post_h41_clean_promotion_and_explicit_merge_packet"
    )
    assert len(snapshot_rows) == 3
