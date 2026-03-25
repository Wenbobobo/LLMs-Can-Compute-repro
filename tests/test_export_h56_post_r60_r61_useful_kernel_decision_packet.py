from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h56_post_r60_r61_useful_kernel_decision_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h56_post_r60_r61_useful_kernel_decision_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h56_writes_saved_successor_decision_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H56_post_r60_r61_useful_kernel_decision_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h56_post_r60_r61_useful_kernel_decision_packet"
    assert payload["summary"]["current_active_docs_only_stage"] == (
        "h54_post_r58_r59_compiled_boundary_decision_packet"
    )
    assert payload["summary"]["selected_outcome"] == "saved_successor_decision_packet_only"
    assert len(payload["summary"]["declared_decision_matrix"]) == 4
    assert payload["summary"]["prerequisite_inputs_if_activated"] == [
        "r60_origin_compiled_useful_kernel_carryover_gate",
        "r61_origin_compiled_useful_kernel_value_gate",
    ]
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["selected_outcome"] == "saved_successor_decision_packet_only"
    assert len(snapshot_rows) == 5

