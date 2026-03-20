from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module(name: str, relative_script: str):
    module_path = Path(__file__).resolve().parents[1] / "scripts" / relative_script
    spec = importlib.util.spec_from_file_location(name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_load_exact_admitted_cases_reads_r6_rows() -> None:
    r6 = _load_module("export_r6_d0_long_horizon_scaling_gate", "export_r6_d0_long_horizon_scaling_gate.py")
    r7 = _load_module("export_r7_d0_same_endpoint_runtime_bridge", "export_r7_d0_same_endpoint_runtime_bridge.py")

    r6.main()
    cases = r7.load_exact_admitted_cases()

    assert len(cases) == 8
    assert all(case.horizon_multiplier == 8 for case in cases)


def test_select_profile_cases_keeps_heaviest_exact_admitted_rows() -> None:
    r6 = _load_module("export_r6_d0_long_horizon_scaling_gate_profile", "export_r6_d0_long_horizon_scaling_gate.py")
    r7 = _load_module("export_r7_d0_same_endpoint_runtime_bridge_profile", "export_r7_d0_same_endpoint_runtime_bridge.py")

    r6.main()
    cases = r7.load_exact_admitted_cases()
    profile_cases = r7.select_profile_cases(cases)

    assert len(profile_cases) == 4
    assert {case.family for case in profile_cases} == {
        "checkpoint_replay_long",
        "helper_checkpoint_braid_long",
        "iterated_helper_accumulator",
        "subroutine_braid_long",
    }


def test_export_r7_d0_same_endpoint_runtime_bridge_builds_expected_summary() -> None:
    r6 = _load_module("export_r6_d0_long_horizon_scaling_gate_second", "export_r6_d0_long_horizon_scaling_gate.py")
    r7 = _load_module("export_r7_d0_same_endpoint_runtime_bridge_second", "export_r7_d0_same_endpoint_runtime_bridge.py")

    r6.main()
    r7.main()

    payload = json.loads(Path("results/R7_d0_same_endpoint_runtime_bridge/summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["overall"]["exact_admitted_family_count"] == 8
    assert summary["overall"]["profiled_row_count"] == 4
    assert summary["overall"]["profiled_family_count"] == 4
    assert summary["overall"]["contradiction_candidate_count"] == 0
    assert summary["stopgo"]["stopgo_status"] in {
        "stop_decode_gain_not_material",
        "stop_bridge_not_yet_closed",
        "go_same_endpoint_bridge_positive",
    }
    assert summary["claim_impact"]["e1c_status"] == "not_triggered"
    assert summary["claim_impact"]["next_lane"] == "H9_refreeze_and_record_sync"
