from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r34_origin_retrieval_primitive_contract_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r34_origin_retrieval_primitive_contract_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r34_writes_supported_primitive_contract(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R34_origin_retrieval_primitive_contract_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    primitive_rows = json.loads((temp_out_dir / "primitive_rows.json").read_text(encoding="utf-8"))["rows"]
    tie_rows = json.loads((temp_out_dir / "tie_rows.json").read_text(encoding="utf-8"))["rows"]

    verdict_by_id = {row["primitive_id"]: row["verdict"] for row in primitive_rows}

    assert payload["summary"]["gate"]["lane_verdict"] == "origin_retrieval_contract_supported"
    assert verdict_by_id["call_return_target"] == "supported"
    assert verdict_by_id["stack_top"] == "supported"
    assert tie_rows[0]["exact_match"] is True
