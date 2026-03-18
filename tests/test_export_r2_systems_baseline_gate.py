from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r2_systems_baseline_gate.py"
    spec = importlib.util.spec_from_file_location("export_r2_systems_baseline_gate", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_geometry_summary_reads_current_benchmark() -> None:
    module = _load_export_module()

    rows = module.load_geometry_rows()
    summary = module.build_geometry_summary(rows)

    assert summary["row_count"] >= 1
    assert summary["min_cache_speedup_vs_bruteforce"] > 1.0
    assert summary["speedup_grows_with_history"] is True


def test_load_correctness_rows_includes_stress_reference_bundle() -> None:
    module = _load_export_module()

    rows = module.load_correctness_rows()

    assert any(row["program_name"] == "bytecode_helper_checkpoint_braid_6_a200_s0" for row in rows)
    assert any(row["comparison_mode"] == "long_exact_final_state" for row in rows)


def test_assess_gate_reports_asymptotic_positive_when_runtime_lags() -> None:
    module = _load_export_module()

    geometry_summary = {
        "all_cache_rows_faster_than_bruteforce": True,
        "speedup_grows_with_history": True,
    }
    runtime_summary = {
        "median_lowered_ns_per_step": 120.0,
        "median_bytecode_ns_per_step": 60.0,
        "median_spec_ns_per_step": 70.0,
    }

    result = module.assess_gate(geometry_summary=geometry_summary, runtime_summary=runtime_summary)

    assert result["gate_status"] == "asymptotic_positive_but_end_to_end_not_yet_competitive"
    assert result["geometry_positive"] is True
    assert result["lowered_ratio_vs_best_reference"] == 2.0
