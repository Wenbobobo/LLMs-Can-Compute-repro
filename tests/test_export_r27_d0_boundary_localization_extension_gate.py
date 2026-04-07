from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r27_d0_boundary_localization_extension_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r27_d0_boundary_localization_extension_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_r26_inputs(*, verdict: str = "near_boundary_mixed_signal_needs_confirmation"):
    first_fail = {
        "branch_id": "candidate_core_subroutine_braid_long_u20_h3p5_cplus_two_kflattened",
        "candidate_id": "candidate_core_subroutine_braid_long_u20_h3p5_cplus_two_kflattened_seed0",
        "lane_class": "candidate_core",
        "family": "subroutine_braid_long",
        "unique_address_target": 20,
        "horizon_multiplier": 3.5,
        "checkpoint_depth": "plus_two",
        "hot_address_skew": "flattened",
        "program_name": "fake_fail_program",
        "first_mismatch_step": 31,
        "failure_reason": "fake mismatch",
        "failure_class": "exactness_mismatch",
    }
    support_branch = {
        "branch_id": "first_wave_extension_subroutine_braid_long_u20_h3p0_cplus_two_kflattened",
        "lane_class": "first_wave_extension",
        "family": "subroutine_braid_long",
        "unique_address_target": 20,
        "horizon_multiplier": 3.0,
        "checkpoint_depth": "plus_two",
        "hot_address_skew": "flattened",
        "failure_candidate_count": 0,
    }
    return {
        "r26_summary": {"summary": {"gate": {"lane_verdict": verdict}}},
        "r26_branch_manifest": {"rows": []},
        "r26_first_fail_digest": {"rows": [first_fail] if verdict == "near_boundary_mixed_signal_needs_confirmation" else []},
        "r26_localized_boundary": {
            "rows": [
                {
                    **first_fail,
                    "supporting_exact_neighbor_count": 1,
                    "supporting_exact_neighbors": [{"branch_id": support_branch["branch_id"]}],
                }
            ]
            if verdict == "near_boundary_mixed_signal_needs_confirmation"
            else []
        },
        "r26_branch_summary": {"rows": [support_branch]},
    }


def test_r27_builds_second_wave_extension_grid() -> None:
    module = _load_export_module()

    plans, trigger_state = module.build_extension_branch_plans()
    admitted_rows = module.r22.load_r19_admitted_runtime_rows()
    templates = module.r22.build_template_registry(admitted_rows)
    branch_specs = module.r22.build_branch_specs(templates, plans)

    assert trigger_state["execution_mode"] == "extension_mode"
    assert len(plans) == 6
    assert len(branch_specs) == 12
    assert {spec.hot_address_skew for spec in branch_specs} == {"baseline", "flattened"}


def test_r27_confirmation_mode_selects_fail_neighbor_and_counterpart() -> None:
    module = _load_export_module()

    branch_plans, trigger_state = module.build_confirmation_branch_plans(_fake_r26_inputs())

    assert trigger_state["execution_mode"] == "confirmation_mode"
    assert len(branch_plans) == 3
    assert {plan.lane_class for plan in branch_plans} == {
        "confirmation_failure_branch",
        "confirmation_exact_neighbor",
        "confirmation_hot_skew_counterpart",
    }
    assert {plan.hot_address_skew for plan in branch_plans} == {"baseline", "flattened"}


def test_export_r27_skip_writes_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R27_d0_boundary_localization_extension_gate"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(
        module,
        "load_r26_inputs",
        lambda: _fake_r26_inputs(verdict="first_boundary_failure_localized"),
    )

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    trigger_payload = json.loads((temp_out_dir / "trigger_state.json").read_text(encoding="utf-8"))
    summary = payload["summary"]
    gate = summary["gate"]

    assert gate["execution_mode"] == "skip"
    assert gate["lane_verdict"] == "skipped_not_triggered"
    assert gate["planned_candidate_count"] == 0
    assert trigger_payload["summary"]["r26_trigger_verdict"] == "first_boundary_failure_localized"
