from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_f23_post_h47_numeric_scaling_bundle.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_f23_post_h47_numeric_scaling_bundle",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f23_writes_numeric_scaling_bundle(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "F23_post_h47_numeric_scaling_bundle"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "f23_post_h47_numeric_scaling_bundle"
    assert payload["summary"]["current_active_docs_only_stage"] == "h47_post_r48_useful_case_bridge_refreeze"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["selected_outcome"] == "post_h47_numeric_scaling_bundle_saved"
    assert payload["summary"]["only_next_runtime_candidate"] == "r49_origin_useful_case_numeric_scaling_gate"
    assert payload["summary"]["dormant_parallel_bundle"] == "f24_post_h47_hybrid_executor_growth_bundle"
    assert payload["summary"]["positive_downstream_placeholder"] == "f25_post_h48_restricted_tinyc_lowering_bundle"
    assert payload["summary"]["negative_downstream_placeholder"] == "p36_post_h48_falsification_closeout_bundle"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["next_required_lane"] == "r49_origin_useful_case_numeric_scaling_gate"
    assert len(snapshot_rows) == 9
