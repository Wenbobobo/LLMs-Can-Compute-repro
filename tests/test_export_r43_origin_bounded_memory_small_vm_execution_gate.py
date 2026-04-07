from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r43_origin_bounded_memory_small_vm_execution_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r43_origin_bounded_memory_small_vm_execution_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r43_writes_bounded_memory_small_vm_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R43_origin_bounded_memory_small_vm_execution_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "execution_manifest.json").read_text(encoding="utf-8"))["rows"]
    program_rows = json.loads((temp_out_dir / "program_table.json").read_text(encoding="utf-8"))["rows"]
    exactness_rows = json.loads((temp_out_dir / "exactness_rows.json").read_text(encoding="utf-8"))["rows"]
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    gate = payload["summary"]["gate"]
    assert payload["summary"]["active_runtime_lane"] == "r43_origin_bounded_memory_small_vm_execution_gate"
    assert payload["summary"]["activation_packet"] == "h41_post_r42_aggressive_long_arc_decision_packet"
    assert payload["summary"]["current_completed_retrieval_contract_gate"] == (
        "r42_origin_append_only_memory_retrieval_contract_gate"
    )
    assert gate["lane_verdict"] == "keep_semantic_boundary_route"
    assert gate["planned_family_count"] == 5
    assert gate["executed_family_count"] == 5
    assert gate["exact_family_count"] == 5
    assert gate["exact_core_family_count"] == 4
    assert gate["optional_call_family_executed"] is True
    assert gate["optional_call_family_exact"] is True
    assert gate["conditional_next_runtime_candidate"] == "r45_origin_dual_mode_model_mainline_gate"
    assert stop_rule["stop_rule_triggered"] is False
    assert len(manifest_rows) == 5
    assert len(program_rows) == 5
    assert len(exactness_rows) == 5
    verdict_by_family = {row["family_id"]: row["verdict"] for row in exactness_rows}
    assert verdict_by_family["bounded_static_sum_loop"] == "exact"
    assert verdict_by_family["single_call_return_accumulator"] == "exact"
