from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r52_origin_internal_vs_external_executor_value_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r52_origin_internal_vs_external_executor_value_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r52_writes_value_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R52_origin_internal_vs_external_executor_value_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    snapshot = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))
    gate = payload["summary"]["gate"]

    assert payload["summary"]["current_completed_r51_gate"] == "r51_origin_memory_control_surface_sufficiency_gate"
    assert payload["summary"]["active_runtime_lane"] == "r52_origin_internal_vs_external_executor_value_gate"
    assert gate["planned_case_count"] == 5
    assert gate["executed_case_count"] == 5
    assert gate["accelerated_exact_case_count"] == 5
    assert gate["linear_exact_case_count"] == 5
    assert gate["external_exact_case_count"] == 5
    assert gate["next_required_packet"] == "h50_post_r51_r52_scope_decision_packet"
    assert len(snapshot["comparator_rows"]) == 5
