from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r61_origin_compiled_useful_kernel_value_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r61_origin_compiled_useful_kernel_value_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r61_writes_saved_successor_value_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R61_origin_compiled_useful_kernel_value_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "r61_origin_compiled_useful_kernel_value_gate"
    assert payload["summary"]["current_active_docs_only_stage"] == (
        "h54_post_r58_r59_compiled_boundary_decision_packet"
    )
    assert payload["summary"]["selected_outcome"] == "saved_successor_value_gate_only"
    assert payload["summary"]["prerequisite_gate_if_activated"] == (
        "r60_origin_compiled_useful_kernel_carryover_gate"
    )
    assert payload["summary"]["only_followup_packet_if_activated"] == (
        "h56_post_r60_r61_useful_kernel_decision_packet"
    )
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert len(payload["summary"]["declared_comparators"]) == 5
    assert claim_packet["distilled_result"]["selected_outcome"] == "saved_successor_value_gate_only"
    assert len(snapshot_rows) == 6

