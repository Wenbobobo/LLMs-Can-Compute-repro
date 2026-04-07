from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p28_post_h43_publication_surface_sync.py"
    spec = importlib.util.spec_from_file_location(
        "export_p28_post_h43_publication_surface_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p28_writes_publication_sync_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P28_post_h43_publication_surface_sync"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    snapshot_rows = json.loads((temp_out_dir / "surface_snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_scientific_stage"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["sync_packet"] == "p28_post_h43_publication_surface_sync"
    assert payload["summary"]["current_completed_exact_runtime_gate"] == (
        "r43_origin_bounded_memory_small_vm_execution_gate"
    )
    assert payload["summary"]["current_completed_useful_case_gate"] == (
        "r44_origin_restricted_wasm_useful_case_execution_gate"
    )
    assert payload["summary"]["current_completed_coequal_model_gate"] == (
        "r45_origin_dual_mode_model_mainline_gate"
    )
    assert payload["summary"]["merge_executed"] is False
    assert payload["summary"]["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert payload["summary"]["synced_surface_count"] == len(snapshot_rows)
    assert len(snapshot_rows) == 12
