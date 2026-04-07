from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module(script_name: str, module_name: str):
    module_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f37_writes_reauthorization_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_f37_post_h61_compiled_online_coprocessor_reauthorization_bundle.py",
        "export_f37_post_h61_compiled_online_coprocessor_reauthorization_bundle",
    )

    temp_h61_summary = tmp_path / "h61_summary.json"
    temp_h61_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "archive_first_consolidation_becomes_default_posture"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_f36_summary = tmp_path / "f36_summary.json"
    temp_f36_summary.write_text(
        json.dumps({"summary": {"admissible_reopen_family": "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_p49_summary = tmp_path / "p49_summary.json"
    temp_p49_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "advisory_origin_materials_available_in_clean_line"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    baseline = tmp_path / "baseline.md"
    baseline.write_text("- a\n- b\n- c\n", encoding="utf-8")
    gates = tmp_path / "gates.md"
    gates.write_text("- a\n- b\n- c\n- d\n- e\n", encoding="utf-8")
    stops = tmp_path / "stops.md"
    stops.write_text("- 1\n- 2\n- 3\n- 4\n- 5\n- 6\n- 7\n", encoding="utf-8")

    original_out_dir = module.OUT_DIR
    original_h61 = module.H61_SUMMARY_PATH
    original_f36 = module.F36_SUMMARY_PATH
    original_p49 = module.P49_SUMMARY_PATH
    original_baseline = module.BASELINE_CONTRACT_PATH
    original_gates = module.ELIGIBILITY_GATES_PATH
    original_stops = module.STOP_RULES_PATH
    temp_out_dir = tmp_path / "F37_post_h61_compiled_online_coprocessor_reauthorization_bundle"
    module.OUT_DIR = temp_out_dir
    module.H61_SUMMARY_PATH = temp_h61_summary
    module.F36_SUMMARY_PATH = temp_f36_summary
    module.P49_SUMMARY_PATH = temp_p49_summary
    module.BASELINE_CONTRACT_PATH = baseline
    module.ELIGIBILITY_GATES_PATH = gates
    module.STOP_RULES_PATH = stops
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H61_SUMMARY_PATH = original_h61
        module.F36_SUMMARY_PATH = original_f36
        module.P49_SUMMARY_PATH = original_p49
        module.BASELINE_CONTRACT_PATH = original_baseline
        module.ELIGIBILITY_GATES_PATH = original_gates
        module.STOP_RULES_PATH = original_stops

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "one_compiled_online_coprocessor_route_specified_but_runtime_closed"
    assert payload["summary"]["eligibility_gate_count"] == 5
    assert payload["summary"]["stop_rule_count"] == 7

