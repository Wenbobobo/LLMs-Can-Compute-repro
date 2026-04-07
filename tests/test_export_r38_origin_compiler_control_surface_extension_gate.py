from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r38_origin_compiler_control_surface_extension_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r38_origin_compiler_control_surface_extension_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r38_writes_control_surface_extension_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R38_origin_compiler_control_surface_extension_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    source_rows = json.loads((temp_out_dir / "source_case_rows.json").read_text(encoding="utf-8"))["rows"]
    execution_rows = json.loads((temp_out_dir / "execution_rows.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["gate"]["lane_verdict"] == "origin_compiler_control_surface_extension_supported_narrowly"
    assert payload["summary"]["gate"]["admitted_case_count"] == 1
    assert payload["summary"]["gate"]["boundary_stress_case_count"] == 1
    assert payload["summary"]["gate"]["admitted_free_running_exact_count"] == 1
    assert payload["summary"]["gate"]["boundary_free_running_exact_count"] == 1
    assert payload["summary"]["gate"]["r37_opcode_surface_matches"] is True
    assert {row["admission_role"] for row in source_rows} == {"admitted", "boundary_stress"}
    assert all(row["free_running_stack_strategy"] == "accelerated" for row in execution_rows)
