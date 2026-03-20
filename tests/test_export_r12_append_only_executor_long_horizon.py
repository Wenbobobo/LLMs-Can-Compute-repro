from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r12_append_only_executor_long_horizon.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r12_append_only_executor_long_horizon",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r12_mode_summary_rows_cover_all_current_modes() -> None:
    module = _load_export_module()
    inputs = module.load_inputs()

    rows = module.build_mode_summary_rows(inputs["m4_payload"])
    baseline = module.build_free_running_baseline(inputs["m4_payload"], rows)

    assert len(rows) == 12
    assert baseline["all_modes_exact"] is True
    assert baseline["countdown_heldout_program_count"] == 14
    assert baseline["max_exact_heldout_steps"] == 104


def test_r12_inventory_uses_current_r6_and_r8_case_families() -> None:
    module = _load_export_module()

    rows = module.build_horizon_inventory_rows()
    summary = module.build_horizon_inventory_summary(rows)

    assert summary["r6_row_count"] == 24
    assert summary["r6_family_count"] == 8
    assert summary["r8_row_count"] == 4
    assert summary["r8_family_count"] == 4
    assert summary["max_r6_horizon_multiplier"] == 8
    assert summary["max_r8_horizon_multiplier"] == 10
    assert "helper_checkpoint_braid_long" in summary["priority_r8_families"]


def test_export_r12_writes_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(
        Path("results/R12_append_only_executor_long_horizon/summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["free_running_baseline"]["all_modes_exact"] is True
    assert summary["harder_d0_baseline"]["exact_suite_row_count"] == 7
    assert summary["horizon_inventory"]["r8_row_count"] == 4
    assert summary["claim_impact"]["next_lane"] == "H15_refreeze_and_decision_sync"
