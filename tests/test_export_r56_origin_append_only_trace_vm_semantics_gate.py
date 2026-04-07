from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r56_origin_append_only_trace_vm_semantics_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r56_origin_append_only_trace_vm_semantics_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r56_writes_trace_vm_semantics_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R56_origin_append_only_trace_vm_semantics_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    execution_report = json.loads((temp_out_dir / "execution_report.json").read_text(encoding="utf-8"))
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    gate = payload["summary"]["gate"]
    task_rows = execution_report["task_rows"]
    measurement_rows = execution_report["measurement_rows"]
    trace_logs = execution_report["trace_logs"]

    assert payload["summary"]["current_active_docs_only_stage"] == "h51_post_h50_origin_mechanism_reentry_packet"
    assert payload["summary"]["preserved_prior_docs_only_closeout"] == "h50_post_r51_r52_scope_decision_packet"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["current_planning_bundle"] == "f28_post_h50_origin_mechanism_reentry_bundle"
    assert payload["summary"]["current_low_priority_wave"] == "p37_post_h50_narrow_executor_closeout_sync"
    assert payload["summary"]["preserved_exact_retrieval_gate"] == "r55_origin_2d_hardmax_retrieval_equivalence_gate"
    assert payload["summary"]["active_runtime_lane"] == "r56_origin_append_only_trace_vm_semantics_gate"
    assert gate["lane_verdict"] == "trace_vm_semantics_supported_exactly"
    assert gate["planned_task_count"] == 5
    assert gate["executed_task_count"] == 5
    assert gate["exact_task_count"] == 5
    assert gate["exact_trace_task_count"] == 5
    assert gate["exact_final_state_task_count"] == 5
    assert gate["transition_count"] > 0
    assert gate["stack_read_count"] > 0
    assert gate["memory_read_count"] > 0
    assert gate["call_read_count"] > 0
    assert gate["first_failure_task_id"] is None
    assert gate["next_required_packet"] == "r57_origin_accelerated_trace_vm_comparator_gate"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert stop_rule["stop_rule_triggered"] is False
    assert stop_rule["r57_open"] is True
    assert stop_rule["next_required_packet"] == "r57_origin_accelerated_trace_vm_comparator_gate"
    assert execution_report["first_failure"] is None
    assert len(task_rows) == 5
    assert len(measurement_rows) == 5
    assert len(trace_logs) == 5
    assert {row["category"] for row in task_rows} == {
        "static_memory",
        "loop_control",
        "indirect_memory",
        "call_return",
        "mixed_surface",
    }
    call_row = next(row for row in measurement_rows if row["task_id"] == "call_return_trace")
    assert call_row["call_read_count"] > 0
    mixed_log = next(row for row in trace_logs if row["task_id"] == "flagged_mixed_surface_trace")
    assert len(mixed_log["reference_transitions"]) == len(mixed_log["candidate_transitions"])
    assert len(mixed_log["reference_transitions"]) > 0
    assert claim_packet["distilled_result"]["lane_verdict"] == "trace_vm_semantics_supported_exactly"
    assert len(snapshot_rows) == 6
