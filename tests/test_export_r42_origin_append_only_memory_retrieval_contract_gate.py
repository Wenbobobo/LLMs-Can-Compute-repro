from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r42_origin_append_only_memory_retrieval_contract_gate.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r42_origin_append_only_memory_retrieval_contract_gate",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_r42_writes_exact_retrieval_contract_gate(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R42_origin_append_only_memory_retrieval_contract_gate"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    task_rows = json.loads((temp_out_dir / "task_rows.json").read_text(encoding="utf-8"))["rows"]
    measurement_rows = json.loads((temp_out_dir / "measurement_rows.json").read_text(encoding="utf-8"))["rows"]
    stop_rule = json.loads((temp_out_dir / "stop_rule.json").read_text(encoding="utf-8"))

    assert payload["summary"]["gate"]["lane_verdict"] == "keep_semantic_boundary_route"
    assert payload["summary"]["gate"]["task_count"] == 6
    assert payload["summary"]["gate"]["exact_task_count"] == 6
    assert payload["summary"]["gate"]["tie_observation_count"] >= 1
    assert payload["summary"]["gate"]["duplicate_maximizer_observation_count"] >= 1
    assert payload["summary"]["gate"]["conditional_next_runtime_candidate"] == (
        "r43_origin_bounded_memory_small_vm_execution_gate"
    )
    assert stop_rule["stop_rule_triggered"] is False
    verdict_by_task = {row["task_id"]: row["verdict"] for row in task_rows}
    assert verdict_by_task["address_reuse_duplicate_and_tie_cases"] == "exact"
    assert verdict_by_task["precision_range_sweep"] == "exact"
    tie_by_task = {row["task_id"]: row["tie_observation_count"] for row in measurement_rows}
    assert tie_by_task["address_reuse_duplicate_and_tie_cases"] >= 1
