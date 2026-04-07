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


def test_export_h63_writes_closeout_packet_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_h63_post_p50_p51_p52_f38_archive_first_closeout_packet.py",
        "export_h63_post_p50_p51_p52_f38_archive_first_closeout_packet",
    )

    summaries = {
        "h62_summary.json": {
            "selected_outcome": "hygiene_first_scope_decision_keeps_archive_default_and_limits_any_reopen_to_r63_profile_gate"
        },
        "p50_summary.json": {
            "selected_outcome": "control_surfaces_locked_to_post_h62_archive_first_closeout"
        },
        "p51_summary.json": {
            "selected_outcome": "paper_surfaces_locked_to_archive_first_partial_falsification_closeout"
        },
        "p52_summary.json": {
            "selected_outcome": "clean_descendant_hygiene_and_merge_prep_locked_without_dirty_root_merge"
        },
        "f38_summary.json": {
            "selected_outcome": "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields"
        },
    }
    paths = {}
    for name, summary in summaries.items():
        path = tmp_path / name
        path.write_text(json.dumps({"summary": summary}, indent=2) + "\n", encoding="utf-8")
        paths[name] = path

    original_out_dir = module.OUT_DIR
    original_h62 = module.H62_SUMMARY_PATH
    original_p50 = module.P50_SUMMARY_PATH
    original_p51 = module.P51_SUMMARY_PATH
    original_p52 = module.P52_SUMMARY_PATH
    original_f38 = module.F38_SUMMARY_PATH
    temp_out_dir = tmp_path / "H63_post_p50_p51_p52_f38_archive_first_closeout_packet"
    module.OUT_DIR = temp_out_dir
    module.H62_SUMMARY_PATH = paths["h62_summary.json"]
    module.P50_SUMMARY_PATH = paths["p50_summary.json"]
    module.P51_SUMMARY_PATH = paths["p51_summary.json"]
    module.P52_SUMMARY_PATH = paths["p52_summary.json"]
    module.F38_SUMMARY_PATH = paths["f38_summary.json"]
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H62_SUMMARY_PATH = original_h62
        module.P50_SUMMARY_PATH = original_p50
        module.P51_SUMMARY_PATH = original_p51
        module.P52_SUMMARY_PATH = original_p52
        module.F38_SUMMARY_PATH = original_f38

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"
    assert payload["summary"]["all_prerequisites_green"] is True
    assert payload["summary"]["conditional_downstream_lane"] == "r63_post_h62_coprocessor_eligibility_profile_gate"
