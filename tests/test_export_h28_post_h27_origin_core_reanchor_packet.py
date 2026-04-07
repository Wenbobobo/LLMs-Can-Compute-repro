from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h28_post_h27_origin_core_reanchor_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h28_post_h27_origin_core_reanchor_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h28_writes_expected_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H28_post_h27_origin_core_reanchor_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["active_stage"] == "h28_post_h27_origin_core_reanchor_packet"
    assert summary["same_endpoint_recovery_state"] == "closed_negative_at_h27"
    assert summary["blocked_count"] == 0
    assert claim_packet["summary"]["distilled_result"]["scientific_target"] == "origin_core_append_only_retrieval_small_vm"
