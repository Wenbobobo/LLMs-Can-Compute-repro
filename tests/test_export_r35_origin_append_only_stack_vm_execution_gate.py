from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r35_origin_append_only_stack_vm_execution_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r35_origin_append_only_stack_vm_execution_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r35_writes_exact_stack_vm_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R35_origin_append_only_stack_vm_execution_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    execution_rows = json.loads((temp_out_dir / "execution_rows.json").read_text(encoding="utf-8"))["rows"]

    call_rows = [row for row in execution_rows if row["contains_call"]]

    assert payload["summary"]["gate"]["lane_verdict"] == "origin_stack_vm_exact_supported"
    assert payload["summary"]["gate"]["executed_case_count"] == len(execution_rows)
    assert call_rows
    assert all(row["pointer_like_exact_call_read_count"] > 0 for row in call_rows)
