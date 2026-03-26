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


def test_export_h64_writes_freeze_packet_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_h64_post_p53_p54_p55_f38_archive_first_freeze_packet.py",
        "export_h64_post_p53_p54_p55_f38_archive_first_freeze_packet",
    )

    summaries = {
        "h63_summary.json": {
            "selected_outcome": "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"
        },
        "p53_summary.json": {
            "selected_outcome": "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze"
        },
        "p54_summary.json": {
            "selected_outcome": "clean_descendant_hygiene_and_artifact_policy_locked_without_merge_execution"
        },
        "p55_summary.json": {
            "selected_outcome": "clean_descendant_promotion_prep_refreshed_for_h64_archive_first_freeze"
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
    original_h63 = module.H63_SUMMARY_PATH
    original_p53 = module.P53_SUMMARY_PATH
    original_p54 = module.P54_SUMMARY_PATH
    original_p55 = module.P55_SUMMARY_PATH
    original_f38 = module.F38_SUMMARY_PATH
    temp_out_dir = tmp_path / "H64_post_p53_p54_p55_f38_archive_first_freeze_packet"
    module.OUT_DIR = temp_out_dir
    module.H63_SUMMARY_PATH = paths["h63_summary.json"]
    module.P53_SUMMARY_PATH = paths["p53_summary.json"]
    module.P54_SUMMARY_PATH = paths["p54_summary.json"]
    module.P55_SUMMARY_PATH = paths["p55_summary.json"]
    module.F38_SUMMARY_PATH = paths["f38_summary.json"]
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H63_SUMMARY_PATH = original_h63
        module.P53_SUMMARY_PATH = original_p53
        module.P54_SUMMARY_PATH = original_p54
        module.P55_SUMMARY_PATH = original_p55
        module.F38_SUMMARY_PATH = original_f38

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_first_freeze_becomes_current_active_route_and_r63_remains_dormant"
    assert payload["summary"]["all_prerequisites_green"] is True
    assert payload["summary"]["conditional_downstream_lane"] == "r63_post_h62_coprocessor_eligibility_profile_gate"
