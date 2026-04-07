from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r40_origin_bounded_scalar_locals_and_flags_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r40_origin_bounded_scalar_locals_and_flags_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r40_writes_bounded_scalar_locals_and_flags_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R40_origin_bounded_scalar_locals_and_flags_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    source_rows = json.loads((temp_out_dir / "source_case_rows.json").read_text(encoding="utf-8"))["rows"]
    negative_rows = json.loads((temp_out_dir / "negative_control_rows.json").read_text(encoding="utf-8"))["rows"]

    gate = payload["summary"]["gate"]
    assert payload["summary"]["active_runtime_lane"] == "r40_origin_bounded_scalar_locals_and_flags_gate"
    assert gate["lane_verdict"] == "origin_bounded_scalar_locals_and_flags_supported_narrowly"
    assert gate["same_opcode_surface_kept"] is True
    assert gate["admitted_case_count"] == 1
    assert gate["boundary_stress_case_count"] == 1
    assert gate["admitted_free_running_exact_count"] == 1
    assert gate["boundary_free_running_exact_count"] == 1
    assert gate["flag_slot_case_count"] == 2
    assert gate["negative_control_count"] == 3
    assert gate["negative_control_rejection_count"] == 3
    assert gate["family_scope_rejection_count"] == 1
    assert all(row["memory_surface_verifier_passed"] is True for row in source_rows)
    assert {row["case_id"] for row in negative_rows} == {
        "invalid_flag_branch",
        "invalid_flag_layout",
        "invalid_heap_escape",
    }

