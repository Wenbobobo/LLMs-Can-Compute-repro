from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_e1b_systems_patch.py"
    spec = importlib.util.spec_from_file_location("export_e1b_systems_patch", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_suite_bridge_rows_marks_lagging_suite() -> None:
    module = _load_export_module()

    rows = module.build_suite_bridge_rows(
        [
            {
                "suite": "smoke",
                "profile_step_count": 10,
                "lowered_total_ns_per_step": 160.0,
                "lowered_exec_only_ns_per_step": 120.0,
                "lowering_share_of_lowered_total": 0.25,
                "bytecode_ns_per_step": 100.0,
                "spec_ns_per_step": 90.0,
            },
            {
                "suite": "smoke",
                "profile_step_count": 12,
                "lowered_total_ns_per_step": 180.0,
                "lowered_exec_only_ns_per_step": 130.0,
                "lowering_share_of_lowered_total": 0.30,
                "bytecode_ns_per_step": 110.0,
                "spec_ns_per_step": 95.0,
            },
        ]
    )

    assert len(rows) == 1
    assert rows[0]["bridge_status"] == "lagging_mixed_gate"
    assert rows[0]["lowered_vs_best_reference_ratio"] > 1.0


def test_build_history_bridge_rows_marks_large_history_as_beyond_current_scope() -> None:
    module = _load_export_module()

    rows = module.build_history_bridge_rows(
        [
            {
                "history_size": 512,
                "query_count": 1024,
                "cache_speedup_vs_bruteforce": 40.0,
                "cache_seconds": 1.0,
                "brute_force_seconds": 40.0,
            }
        ],
        [{"profile_step_count": 200}],
    )

    assert len(rows) == 1
    assert rows[0]["bridge_status"] == "beyond_current_d0_scope"
    assert rows[0]["cases_at_or_above_history"] == 0


def test_build_summary_reaffirms_mixed_gate_and_no_widening() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    component_rows = [
        {
            "profile_step_count": 200,
            "lowered_over_best_reference": 1.6,
            "dominant_lowered_component": "lowered_exec_only",
        }
    ]
    suite_rows = [
        {
            "bridge_status": "lagging_mixed_gate",
        }
    ]
    history_rows = [
        {
            "bridge_status": "beyond_current_d0_scope",
        }
    ]
    summary = module.build_summary(
        r2_summary=inputs["r2_summary"],
        m7_decision=inputs["m7_decision"],
        m6_stress_summary=inputs["m6_stress_summary"],
        component_rows=component_rows,
        suite_rows=suite_rows,
        history_rows=history_rows,
    )

    assert summary["gate_status_after_patch"] == "asymptotic_positive_but_end_to_end_not_yet_competitive"
    assert summary["frontend_widening_authorized"] is False
    assert summary["single_bottleneck_fixable_now"] is False
    assert summary["e1c_trigger_required"] is False
