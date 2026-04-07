from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h29_refreeze_after_r34_r35_origin_core_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h29_refreeze_after_r34_r35_origin_core_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h29_writes_refreeze_packet_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H29_refreeze_after_r34_r35_origin_core_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["active_stage"] == "h29_refreeze_after_r34_r35_origin_core_gate"
    assert summary["origin_core_chain_state"] == "positive_on_current_bundle"
    assert summary["next_required_lane"] == "r36_origin_long_horizon_precision_scaling_gate"
    assert summary["blocked_count"] == 0
    assert len(checklist["rows"]) == 4
    assert (
        claim_packet["summary"]["distilled_result"]["next_required_lane"]
        == "r36_origin_long_horizon_precision_scaling_gate"
    )
