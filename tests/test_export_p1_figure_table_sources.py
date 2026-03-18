from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p1_figure_table_sources.py"
    spec = importlib.util.spec_from_file_location("export_p1_figure_table_sources", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_failure_taxonomy_exports_tracks_opcode_shape_heldout_slice() -> None:
    module = _load_export_module()

    summary, rows = module.build_failure_taxonomy_exports()

    assert summary["target_slice"] == {"mask_mode": "opcode_shape", "split": "heldout"}
    assert summary["failed_program_count"] == 15
    provenance_counts = {
        row["provenance_class"]: row["count"]
        for row in summary["by_provenance_class"]
    }
    assert provenance_counts["memory_value_root_cause"] == 8
    assert provenance_counts["downstream_nontermination_after_semantic_error"] == 7
    assert any(row["family"] == "alternating_memory_loop" for row in rows)


def test_build_real_trace_boundary_exports_merge_offset_and_organic_bundles() -> None:
    module = _load_export_module()

    summary, rows = module.build_real_trace_boundary_exports()

    assert {row["suite_bundle"] for row in rows} == {"offset", "organic"}
    assert set(summary["schemes"]) == {"block_recentered", "radix2", "single_head"}
    failure_type_counts = {
        row["failure_type"]: row["count"]
        for row in summary["failure_type_counts"]
    }
    assert failure_type_counts["tie_collapse"] > 0
    assert any(row["stream_name"] == "loop_offset_64_memory" for row in rows)
    assert any(row["family"] == "hotspot_memory_rewrite" for row in rows)


def test_build_exact_trace_final_state_table_uses_current_m6_artifacts() -> None:
    module = _load_export_module()

    payload, rows = module.build_exact_trace_final_state_table()

    assert payload["summary"]["total_rows"] == 22
    assert payload["summary"]["trace_match_count"] == 22
    assert payload["summary"]["final_state_match_count"] == 22
    assert payload["summary"]["verifier_pass_count"] == 22
    assert any(row["status_label"] == "exact_final_state_match" for row in rows)
    assert any(row["suite"] == "control_flow" for row in rows)
    assert all(row["instruction_count_match"] is True for row in rows)


def test_build_memory_surface_diagnostic_exports_syncs_appendix_level_d0_rows() -> None:
    module = _load_export_module()

    payload, rows = module.build_memory_surface_diagnostic_exports()

    assert payload["summary"]["row_count"] == 6
    assert payload["summary"]["surface_match_count"] == 6
    assert payload["summary"]["surface_verifier_pass_count"] == 6
    assert payload["summary"]["negative_control_count"] == 2
    assert payload["summary"]["heap_touch_program_count"] == 2
    error_counts = {
        row["error_class"]: row["count"]
        for row in payload["summary"]["negative_control_error_classes"]
    }
    assert error_counts["undeclared_static_address"] == 1
    assert error_counts["undeclared_address_literal"] == 1
    assert any(row["program_name"] == "bytecode_subroutine_braid_long_12_a160" for row in rows)
    assert all(row["boundary_snapshot_count_match"] is True for row in rows)
    assert payload["coverage_note"].startswith("Appendix-level D0 diagnostic only")
