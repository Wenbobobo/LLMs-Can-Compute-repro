from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r36_origin_long_horizon_precision_scaling_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r36_origin_long_horizon_precision_scaling_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r36_writes_narrow_precision_boundary_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R36_origin_long_horizon_precision_scaling_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    screening_rows = json.loads((temp_out_dir / "screening_rows.json").read_text(encoding="utf-8"))["rows"]
    boundary_rows = json.loads((temp_out_dir / "program_boundary_summary.json").read_text(encoding="utf-8"))["rows"]

    inflated_single_head_failures = [
        row
        for row in screening_rows
        if row["scheme"] == "single_head" and row["horizon_multiplier"] > 1 and not row["passed"]
    ]
    recovery_cases = [
        row for row in boundary_rows if row["decomposition_recovers_single_head_failure"]
    ]

    assert payload["summary"]["gate"]["lane_verdict"] == "origin_precision_scaling_boundary_sharpened"
    assert payload["summary"]["gate"]["narrow_scope_kept"] is True
    assert payload["summary"]["gate"]["executed_row_count"] == len(screening_rows)
    assert inflated_single_head_failures
    assert recovery_cases
