from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r57_origin_accelerated_trace_vm_comparator_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r57_origin_accelerated_trace_vm_comparator_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r57_writes_accelerated_trace_vm_comparator_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R57_origin_accelerated_trace_vm_comparator_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    execution_report = json.loads((temp_out_dir / "execution_report.json").read_text(encoding="utf-8"))
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    gate = payload["summary"]["gate"]
    comparator_rows = execution_report["comparator_rows"]
    trace_length_sensitivity = execution_report["trace_length_sensitivity"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h51_post_h50_origin_mechanism_reentry_packet"
    assert payload["summary"]["preserved_prior_docs_only_closeout"] == "h50_post_r51_r52_scope_decision_packet"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_planning_bundle"] == "f28_post_h50_origin_mechanism_reentry_bundle"
    assert payload["summary"]["current_low_priority_wave"] == "p37_post_h50_narrow_executor_closeout_sync"
    assert payload["summary"]["preserved_exact_retrieval_gate"] == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
    assert payload["summary"]["preserved_exact_trace_vm_gate"] == "r56_origin_append_only_trace_vm_semantics_gate"
    assert payload["summary"]["active_runtime_lane"] == "r57_origin_accelerated_trace_vm_comparator_gate"
    assert gate["lane_verdict"] == "accelerated_trace_vm_lacks_bounded_value"
    assert gate["planned_task_count"] == 5
    assert gate["executed_task_count"] == 5
    assert gate["accelerated_exact_task_count"] == 5
    assert gate["linear_exact_task_count"] == 5
    assert gate["external_exact_task_count"] == 5
    assert gate["accelerated_faster_than_external_count"] == 0
    assert gate["mean_accelerated_seconds"] > 0.0
    assert gate["mean_linear_seconds"] > 0.0
    assert gate["mean_external_seconds"] > 0.0
    assert gate["overall_internal_retrieval_share_of_transitions"] > 0.0
    assert gate["trace_length_bucket_count"] == 3
    assert gate["first_failure_route"] is None
    assert gate["first_failure_task_id"] is None
    assert gate["selected_h52_outcome"] == "freeze_origin_mechanism_supported_without_fastpath_value"
    assert gate["next_required_packet"] == "h52_post_r55_r56_r57_origin_mechanism_decision_packet"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)

    assert execution_report["first_failure"] is None
    assert execution_report["first_failure_carry_over"]["r56_first_failure"] is None
    assert execution_report["first_failure_carry_over"]["r57_first_failure"] is None
    assert len(comparator_rows) == 5
    assert {row["task_id"] for row in comparator_rows} == {
        "static_latest_write_trace",
        "countdown_loop_control_trace",
        "indirect_memory_loop_trace",
        "call_return_trace",
        "flagged_mixed_surface_trace",
    }
    assert all(row["accelerated_exact_trace_match"] for row in comparator_rows)
    assert all(row["accelerated_exact_final_state_match"] for row in comparator_rows)
    assert all(row["linear_exact_trace_match"] for row in comparator_rows)
    assert all(row["linear_exact_final_state_match"] for row in comparator_rows)
    assert all(row["external_exact_trace_match"] for row in comparator_rows)
    assert all(row["external_exact_final_state_match"] for row in comparator_rows)
    assert all(row["accelerated_read_count"] == row["linear_read_count"] for row in comparator_rows)
    assert all(row["external_read_count"] == 0 for row in comparator_rows)
    assert any(row["accelerated_memory_read_count"] > 0 for row in comparator_rows)
    assert any(row["accelerated_call_read_count"] > 0 for row in comparator_rows)
    assert len(trace_length_sensitivity) == 3
    assert {row["trace_length_bucket"] for row in trace_length_sensitivity} == {"short", "medium", "long"}
    assert claim_packet["distilled_result"]["lane_verdict"] == "accelerated_trace_vm_lacks_bounded_value"
    assert len(snapshot_rows) == 8
