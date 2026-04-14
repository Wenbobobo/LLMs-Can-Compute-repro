from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from bytecode import (
    analyze_memory_surfaces,
    call_frame_roundtrip_program,
    memory_surface_cases,
    memory_surface_negative_programs,
    run_memory_surface_case,
    verify_memory_surfaces,
)
from bytecode.interpreter import BytecodeInterpreter


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_m6_memory_surface_followup.py"
    spec = importlib.util.spec_from_file_location("export_m6_memory_surface_followup", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_memory_surface_verifier_accepts_annotated_call_programs() -> None:
    for case in memory_surface_cases():
        result = verify_memory_surfaces(case.program)
        assert result.passed is True
        assert result.error_class is None


def test_memory_surface_verifier_rejects_bad_layout_programs() -> None:
    results = [verify_memory_surfaces(program) for program in memory_surface_negative_programs()]

    assert [result.passed for result in results] == [False, False]
    assert {result.error_class for result in results} == {
        "undeclared_address_literal",
        "undeclared_static_address",
    }


def test_memory_surface_report_tracks_call_boundaries_and_regions() -> None:
    program = call_frame_roundtrip_program(slot_address=192)
    execution = BytecodeInterpreter().run(program)
    report = analyze_memory_surfaces(program, execution)

    assert report.max_call_depth == 1
    assert report.touched_frame_addresses == (192,)
    assert report.touched_heap_addresses == ()
    assert len(report.boundary_snapshots) == 2
    assert report.boundary_snapshots[0].opcode == "call"
    assert report.boundary_snapshots[1].opcode == "ret"


def test_memory_surface_harness_matches_lowered_path() -> None:
    case = next(case for case in memory_surface_cases() if case.program.name.startswith("bytecode_countdown_helper_call"))
    row = run_memory_surface_case(case)

    assert row.base_trace_match is True
    assert row.base_final_state_match is True
    assert row.memory_surface_verifier_passed is True
    assert row.memory_surface_match is True
    assert row.boundary_snapshot_count >= 2


def test_export_m6_memory_surface_followup_builds_current_rows() -> None:
    module = _load_export_module()
    module.main()

    summary_path = Path("results/M6_memory_surface_followup/summary.json")
    payload = __import__("json").loads(summary_path.read_text(encoding="utf-8"))

    assert payload["summary"]["row_count"] == 6
    assert payload["summary"]["memory_surface_match_count"] == 6
    assert payload["summary"]["memory_surface_verifier_pass_count"] == 6
    assert payload["summary"]["negative_control_count"] == 2
