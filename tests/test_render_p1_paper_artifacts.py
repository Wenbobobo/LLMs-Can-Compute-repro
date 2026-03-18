from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_render_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "render_p1_paper_artifacts.py"
    spec = importlib.util.spec_from_file_location("render_p1_paper_artifacts", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_failure_taxonomy_figure_svg_mentions_current_split() -> None:
    module = _load_render_module()
    summary = module.read_json("results/P1_paper_readiness/m4_failure_taxonomy_summary.json")

    svg = module.build_failure_taxonomy_figure_svg(summary)

    assert "M4 staged-pointer held-out failure taxonomy" in svg
    assert "8 vs 7" in svg
    assert "alternating_memory_loop" in svg


def test_build_real_trace_boundary_figure_svg_contains_schemes_and_streams() -> None:
    module = _load_render_module()
    summary = module.read_json("results/P1_paper_readiness/m4_real_trace_boundary_summary.json")

    svg = module.build_real_trace_boundary_figure_svg(summary)

    assert "single_head" in svg
    assert "radix2" in svg
    assert "block_recentered" in svg
    assert "alternating_offset_2048_memory" in svg
    assert "tie_collapse" in svg


def test_build_frontend_boundary_diagram_svg_stays_narrow() -> None:
    module = _load_render_module()
    exact_table = module.read_json("results/P1_paper_readiness/exact_trace_final_state_table.json")

    svg = module.build_frontend_boundary_diagram_svg(exact_table)

    assert "Tiny typed bytecode v1" in svg
    assert "22 verifier-passing rows" in svg
    assert "static-target call/ret" in svg
    assert "arbitrary C support" in svg


def test_build_exact_trace_final_state_markdown_contains_rows_and_scope_note() -> None:
    module = _load_render_module()
    exact_table = module.read_json("results/P1_paper_readiness/exact_trace_final_state_table.json")

    text = module.build_exact_trace_final_state_markdown(exact_table)

    assert "# Exact Trace / Final State Table" in text
    assert "bytecode_iterated_helper_accumulator_20_a128_b129" in text
    assert "bytecode_checkpoint_replay_long_8_a96" in text
    assert "Current scope covers only the initial typed-bytecode families" in text


def test_build_memory_surface_diagnostic_markdown_contains_rows_and_negative_controls() -> None:
    module = _load_render_module()
    memory_surface = module.read_json("results/P1_paper_readiness/m6_memory_surface_diagnostic_summary.json")

    text = module.build_memory_surface_diagnostic_markdown(memory_surface)

    assert "# Memory Surface Diagnostic Table" in text
    assert "bytecode_subroutine_braid_long_12_a160" in text
    assert "invalid_memory_surface_undeclared_static" in text
    assert "Appendix-level D0 diagnostic only" in text


def test_build_layout_manifest_tracks_rendered_assets() -> None:
    module = _load_render_module()

    manifest = module.build_layout_manifest()

    assert manifest["experiment"] == "p1_render_bundle_artifacts"
    asset_paths = {
        asset["path"]
        for asset in manifest["rendered_assets"]
    }
    assert "results/P1_paper_readiness/m4_failure_taxonomy_figure.svg" in asset_paths
    assert "results/P1_paper_readiness/m6_frontend_boundary_diagram.svg" in asset_paths
    assert "results/P1_paper_readiness/exact_trace_final_state_table.md" in asset_paths
    assert "results/P1_paper_readiness/m6_memory_surface_diagnostic_table.md" in asset_paths
