from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r39_origin_compiler_control_surface_dependency_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r39_origin_compiler_control_surface_dependency_audit",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r39_writes_control_surface_dependency_audit(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R39_origin_compiler_control_surface_dependency_audit"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    source_rows = json.loads((temp_out_dir / "source_case_rows.json").read_text(encoding="utf-8"))["rows"]
    comparison_rows = json.loads((temp_out_dir / "comparison_rows.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_runtime_lane"] == "r39_origin_compiler_control_surface_dependency_audit"
    assert payload["summary"]["gate"]["lane_verdict"] == "control_surface_dependence_not_detected_on_declared_permutation"
    assert payload["summary"]["gate"]["perturbation_case_count"] == 2
    assert payload["summary"]["gate"]["perturbation_free_running_exact_count"] == 2
    assert payload["summary"]["gate"]["perturbation_final_state_preserved_count"] == 2
    assert payload["summary"]["gate"]["perturbation_trace_changed_count"] == 2
    assert payload["summary"]["gate"]["same_opcode_surface_kept"] is True
    assert {row["control_surface_variant"] for row in source_rows} == {
        "baseline",
        "helper_body_permuted_targets_renumbered",
    }
    assert all(row["same_final_state_as_baseline"] is True for row in comparison_rows)
    assert all(row["same_trace_as_baseline"] is False for row in comparison_rows)
