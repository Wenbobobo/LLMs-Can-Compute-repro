from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r51_origin_memory_control_surface_sufficiency_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r51_origin_memory_control_surface_sufficiency_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r51_writes_memory_control_surface_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R51_origin_memory_control_surface_sufficiency_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    manifest_rows = json.loads((temp_out_dir / "case_manifest.json").read_text(encoding="utf-8"))["rows"]
    execution_report = json.loads((temp_out_dir / "execution_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    exactness_rows = execution_report["exactness_rows"]
    family_rollup_rows = execution_report["family_rollup_rows"]
    gate = payload["summary"]["gate"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h49_post_r50_tinyc_lowering_decision_packet"
    assert payload["summary"]["current_post_h49_planning_bundle"] == (
        "f26_post_h49_origin_claim_delta_and_next_question_bundle"
    )
    assert payload["summary"]["active_runtime_lane"] == "r51_origin_memory_control_surface_sufficiency_gate"
    assert gate["planned_case_count"] == 5
    assert gate["executed_case_count"] == 5
    assert gate["planned_family_count"] == 5
    assert len(manifest_rows) == 5
    assert len(exactness_rows) == 5
    assert len(family_rollup_rows) == 5

    lowered_row = next(row for row in exactness_rows if row["family_id"] == "bounded_static_memory_lowered_row")
    declared_memory = lowered_row["compiled_declared_memory"]
    assert declared_memory["histogram_bin_0"] == 1
    assert declared_memory["histogram_bin_2"] == 3
    assert declared_memory["histogram_bin_3"] == 3
    assert declared_memory["histogram_bin_7"] == 2
    assert declared_memory["histogram_bin_9"] == 1
    assert declared_memory["histogram_bin_15"] == 2

    assert stop_rule["next_required_packet"] in {
        "r52_origin_internal_vs_external_executor_value_gate",
        "h50_post_r51_r52_scope_decision_packet",
    }
