from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r30_d0_boundary_reauthorization_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r30_d0_boundary_reauthorization_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_inputs():
    return {
        "r30_readme_text": "does not execute a new boundary scan `R21` `R22` `R24` `H23`",
        "r30_status_text": "authorize at most one future bounded family-local sharp zoom principled no-localization grounds `D0`",
        "r30_todo_text": "candidate core approved-axis list stop-rule next boundary lane",
        "r30_acceptance_text": "`execute_one_more_family_local_zoom` `hold_boundary_lane_closed` `needs_new_axis_before_more_execution`",
        "r30_artifact_index_text": "results/R30_d0_boundary_reauthorization_packet/summary.json R24_d0_boundary_localization_zoom_followup R32_d0_family_local_boundary_sharp_zoom",
        "h23_summary_text": '"boundary_verdict": "bounded_grid_still_not_localized" "next_priority_lane": "p14_public_surface_sync_after_h23"',
        "h23_summary": {
            "summary": {
                "boundary_verdict": "bounded_grid_still_not_localized",
                "systems_verdict": "systems_still_mixed",
            }
        },
        "h21_summary_text": '"boundary_verdict": "extended_grid_no_break_still_not_localized" "systems_verdict": "systems_still_mixed"',
        "h21_summary": {
            "summary": {
                "boundary_verdict": "extended_grid_no_break_still_not_localized",
                "systems_verdict": "systems_still_mixed",
            }
        },
        "r22_summary_text": '"lane_verdict": "no_failure_in_extended_grid"',
        "r22_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "no_failure_in_extended_grid",
                    "planned_candidate_count": 102,
                }
            }
        },
        "r26_summary_text": '"lane_verdict": "grid_extended_still_not_localized"',
        "r26_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "grid_extended_still_not_localized",
                    "executed_candidate_count": 22,
                }
            }
        },
        "r27_summary_text": '"lane_verdict": "extension_grid_still_not_localized"',
        "r27_summary": {
            "summary": {
                "gate": {
                    "lane_verdict": "extension_grid_still_not_localized",
                    "executed_candidate_count": 12,
                }
            }
        },
        "r24_matrix_text": "Candidate Core Zoom Axes Stop Rules Predeclared Verdict Vocabulary checkpoint_replay_long",
    }


def test_r30_summary_authorizes_one_more_local_zoom() -> None:
    module = _load_export_module()

    checklist_rows = module.build_checklist_rows(**_fake_inputs())
    summary = module.build_summary(checklist_rows)

    assert summary["current_frozen_stage"] == "h23_refreeze_after_r26_r27_r28"
    assert summary["boundary_reauthorization_verdict"] == "execute_one_more_family_local_zoom"
    assert summary["recommended_next_lane"] == "r32_d0_family_local_boundary_sharp_zoom"
    assert summary["blocked_count"] == 0


def test_export_r30_writes_expected_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "R30_d0_boundary_reauthorization_packet"
    module.OUT_DIR = temp_out_dir
    monkeypatch.setattr(module, "load_inputs", lambda: _fake_inputs())

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["boundary_reauthorization_verdict"] == "execute_one_more_family_local_zoom"
    assert summary["recommended_next_action"].startswith("Authorize one future family-local sharp zoom")
