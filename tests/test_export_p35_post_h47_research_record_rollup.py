from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_p35_post_h47_research_record_rollup.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p35_post_h47_research_record_rollup",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p35_writes_research_record_rollup(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P35_post_h47_research_record_rollup"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["current_active_stage"] == "h47_post_r48_useful_case_bridge_refreeze"
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["refresh_packet"] == "p35_post_h47_research_record_rollup"
    assert payload["summary"]["selected_outcome"] == "research_record_rollup_saved_without_scientific_widening"
    assert payload["summary"]["current_low_priority_wave"] == "p35_post_h47_research_record_rollup"
    assert payload["summary"]["preserved_prior_low_priority_wave"] == "p31_post_h43_blog_guardrails_refresh"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["next_required_lane"] == "f23_post_h47_numeric_scaling_bundle"
    assert len(snapshot_rows) == 8
