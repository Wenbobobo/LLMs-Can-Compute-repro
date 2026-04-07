from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p38_post_h52_compiled_boundary_hygiene_sync.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p38_post_h52_compiled_boundary_hygiene_sync",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p38_writes_compiled_boundary_hygiene_sync(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "P38_post_h52_compiled_boundary_hygiene_sync"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["current_active_stage"] == "h54_post_r58_r59_compiled_boundary_decision_packet"
    assert payload["summary"]["preserved_prior_docs_only_closeout"] == (
        "h52_post_r55_r56_r57_origin_mechanism_decision_packet"
    )
    assert payload["summary"]["preserved_prior_compiled_boundary_reentry_packet"] == (
        "h53_post_h52_compiled_boundary_reentry_packet"
    )
    assert payload["summary"]["current_paper_grade_endpoint"] == "h43_post_r44_useful_case_refreeze"
    assert payload["summary"]["refresh_packet"] == "p38_post_h52_compiled_boundary_hygiene_sync"
    assert payload["summary"]["selected_outcome"] == "compiled_boundary_hygiene_preserved_through_h54_closeout"
    assert payload["summary"]["current_low_priority_wave"] == "p38_post_h52_compiled_boundary_hygiene_sync"
    assert payload["summary"]["current_planning_bundle"] == "f29_post_h52_restricted_compiled_boundary_bundle"
    assert payload["summary"]["preserved_execution_gate"] == "r59_origin_compiled_trace_vm_execution_gate"
    assert payload["summary"]["current_merge_posture"] == "explicit_no_merge_during_wave"
    assert payload["summary"]["merge_executed"] is False
    assert payload["summary"]["root_dirty_main_quarantined"] is True
    assert payload["summary"]["large_artifact_default_policy"] == (
        "raw_step_trace_and_per_read_rows_out_of_git"
    )
    assert payload["summary"]["tracked_large_artifact_count"] == 0
    assert payload["summary"]["tracked_large_artifact_paths"] == []
    assert payload["summary"]["next_required_lane"] == "no_active_downstream_runtime_lane"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["current_low_priority_wave"] == (
        "p38_post_h52_compiled_boundary_hygiene_sync"
    )
    assert len(snapshot_rows) == 9


def test_collect_tracked_large_artifacts_filters_threshold(tmp_path: Path) -> None:
    module = _load_export_module()
    small = tmp_path / "small.txt"
    small.write_bytes(b"0" * (module.LARGE_ARTIFACT_THRESHOLD_BYTES - 1))
    large = tmp_path / "large.bin"
    large.write_bytes(b"0" * module.LARGE_ARTIFACT_THRESHOLD_BYTES)

    rows = module.collect_tracked_large_artifacts(
        tmp_path,
        tracked_paths=["small.txt", "large.bin", "missing.bin"],
    )

    assert rows == [
        {
            "path": "large.bin",
            "size_bytes": module.LARGE_ARTIFACT_THRESHOLD_BYTES,
            "size_mib": 10.0,
        }
    ]
