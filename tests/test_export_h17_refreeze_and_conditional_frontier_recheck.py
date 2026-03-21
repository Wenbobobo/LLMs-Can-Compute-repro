from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h17_refreeze_and_conditional_frontier_recheck.py"
    )
    spec = importlib.util.spec_from_file_location("export_h17_refreeze_and_conditional_frontier_recheck", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _build_fake_inputs(*, r18_confirmed: bool) -> dict[str, object]:
    return {
        "h16_guard": {
            "summary": {
                "stage_guard_state": "same_scope_reopen_guard_green",
                "blocked_count": 0,
                "latest_landed_lane": "r17_d0_full_surface_runtime_bridge",
                "active_comparator_lane": "r18_d0_same_endpoint_runtime_repair_counterfactual",
            }
        },
        "r15_summary": {"summary": {"claim_impact": {"next_lane": "R16_d0_real_trace_precision_boundary_saturation"}}},
        "r16_summary": {"summary": {"claim_impact": {"next_lane": "R17_d0_full_surface_runtime_bridge"}}},
        "r17_summary": {
            "summary": {
                "claim_impact": {"status": "full_surface_same_endpoint_runtime_bridge_measured"},
                "stopgo": {"stopgo_status": "stop_decode_gain_not_material"},
            }
        },
        "r18_summary": {
            "summary": {
                "status": "r18c_staged_exact_complete" if r18_confirmed else "r18b_pointer_like_complete",
                "probe_strategy": "staged_exact_both_spaces" if r18_confirmed else "pointer_like_exact_both_spaces",
                "executed_probe_ids": ["r18b_pointer_like", "r18c_staged_exact"]
                if r18_confirmed
                else ["r18b_pointer_like"],
                "frontier_recheck_hint": "conditional_plan_required" if r18_confirmed else "blocked",
                "confirmation": {"gate_passed": r18_confirmed},
                "claim_impact": {
                    "status": "r18_runtime_repair_confirmed" if r18_confirmed else "r18_runtime_repair_not_confirmed",
                    "next_lane": "H17_refreeze_and_conditional_frontier_recheck",
                    "next_probe": None,
                },
            }
        },
        "p5_summary": {"summary": {"blocked_count": 0}},
        "h2_summary": {"summary": {"blocked_count": 0}},
        "p10_summary": {"summary": {"blocked_count": 0}},
        "worktree_summary": {"summary": {"release_commit_state": "dirty_worktree_release_commit_blocked"}},
    }


def test_build_summary_blocks_frontier_recheck_after_negative_r18() -> None:
    module = _load_export_module()
    inputs = _build_fake_inputs(r18_confirmed=False)

    rows = module.build_checklist_rows(**inputs)
    summary = module.build_summary(rows, inputs)

    assert summary["decision_state"] == "same_scope_refreeze_complete"
    assert summary["r18_decision"] == "r18_runtime_repair_not_confirmed"
    assert summary["frontier_recheck_decision"] == "blocked"
    assert summary["next_stage"] == "same_scope_stop_and_archive"
    assert summary["blocked_count"] == 0


def test_export_h17_writes_expected_summary(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    original_load_inputs = module.load_inputs
    temp_out_dir = tmp_path / "H17_refreeze_and_conditional_frontier_recheck"
    module.OUT_DIR = temp_out_dir
    module.load_inputs = lambda: _build_fake_inputs(r18_confirmed=True)

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.load_inputs = original_load_inputs

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["current_paper_phase"] == "h17_refreeze_and_conditional_frontier_recheck_complete"
    assert summary["active_stage"] == "h17_refreeze_and_conditional_frontier_recheck"
    assert summary["decision_state"] == "same_scope_refreeze_complete"
    assert summary["r18_decision"] == "r18_runtime_repair_confirmed"
    assert summary["frontier_recheck_decision"] == "conditional_plan_required"
    assert summary["next_stage"] == "future_frontier_recheck_plan_required"
