from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_f20_post_r42_dual_mode_model_mainline_bundle.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_f20_post_r42_dual_mode_model_mainline_bundle",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f20_writes_dual_mode_model_mainline_bundle(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "F20_post_r42_dual_mode_model_mainline_bundle"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "f20_post_r42_dual_mode_model_mainline_bundle"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == (
        "h40_post_h38_semantic_boundary_activation_packet"
    )
    assert payload["summary"]["model_mainline_posture"] == "coequal_mainline_exact_non_substitutive"
    assert payload["summary"]["implementation_posture"] == "dual_mode_trainable_2d_and_compiled_weight"
    assert payload["summary"]["decisive_exact_next_gate"] == "r43_origin_bounded_memory_small_vm_execution_gate"
    assert payload["summary"]["authorized_future_model_gate"] == "r45_origin_dual_mode_model_mainline_gate"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["later_route_selection_packet"] == "h42_post_r43_route_selection_packet"
    assert len(snapshot_rows) == 3
