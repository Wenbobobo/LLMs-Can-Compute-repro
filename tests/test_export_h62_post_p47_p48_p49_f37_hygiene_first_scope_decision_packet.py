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


def test_export_h62_writes_scope_decision_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet.py",
        "export_h62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet",
    )

    summaries = {
        "h61_summary.json": {"selected_outcome": "archive_first_consolidation_becomes_default_posture"},
        "p47_summary.json": {"selected_outcome": "quarantine_root_and_plan_main_merge_only"},
        "p48_summary.json": {"selected_outcome": "clean_descendant_ready_for_later_explicit_promotion"},
        "p49_summary.json": {"selected_outcome": "advisory_origin_materials_available_in_clean_line"},
        "f37_summary.json": {"selected_outcome": "one_compiled_online_coprocessor_route_specified_but_runtime_closed"},
    }
    paths = {}
    for name, summary in summaries.items():
        path = tmp_path / name
        path.write_text(json.dumps({"summary": summary}, indent=2) + "\n", encoding="utf-8")
        paths[name] = path

    original_out_dir = module.OUT_DIR
    original_h61 = module.H61_SUMMARY_PATH
    original_p47 = module.P47_SUMMARY_PATH
    original_p48 = module.P48_SUMMARY_PATH
    original_p49 = module.P49_SUMMARY_PATH
    original_f37 = module.F37_SUMMARY_PATH
    temp_out_dir = tmp_path / "H62_post_p47_p48_p49_f37_hygiene_first_scope_decision_packet"
    module.OUT_DIR = temp_out_dir
    module.H61_SUMMARY_PATH = paths["h61_summary.json"]
    module.P47_SUMMARY_PATH = paths["p47_summary.json"]
    module.P48_SUMMARY_PATH = paths["p48_summary.json"]
    module.P49_SUMMARY_PATH = paths["p49_summary.json"]
    module.F37_SUMMARY_PATH = paths["f37_summary.json"]
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H61_SUMMARY_PATH = original_h61
        module.P47_SUMMARY_PATH = original_p47
        module.P48_SUMMARY_PATH = original_p48
        module.P49_SUMMARY_PATH = original_p49
        module.F37_SUMMARY_PATH = original_f37

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "hygiene_first_scope_decision_keeps_archive_default_and_limits_any_reopen_to_r63_profile_gate"
    assert payload["summary"]["all_prerequisites_green"] is True
    assert payload["summary"]["conditional_downstream_lane"] == "r63_post_h62_coprocessor_eligibility_profile_gate"
