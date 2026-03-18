from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from bytecode import (
    helper_checkpoint_braid_long_program,
    helper_checkpoint_braid_program,
    invalid_helper_checkpoint_braid_branch_program,
    invalid_helper_checkpoint_braid_surface_program,
    run_stress_reference_case,
    stress_reference_cases,
    validate_program_contract,
    validate_surface_literals,
)


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_m6_stress_reference_followup.py"
    spec = importlib.util.spec_from_file_location("export_m6_stress_reference_followup", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_spec_contract_accepts_helper_checkpoint_braid_positives() -> None:
    for program in (
        helper_checkpoint_braid_program(6, base_address=200, selector_seed=0),
        helper_checkpoint_braid_program(6, base_address=216, selector_seed=1),
        helper_checkpoint_braid_long_program(18, base_address=232, selector_seed=0),
    ):
        result = validate_program_contract(program)
        assert result.passed is True
        assert result.error_class is None


def test_spec_contract_rejects_helper_checkpoint_branch_negative() -> None:
    result = validate_program_contract(invalid_helper_checkpoint_braid_branch_program(6, base_address=248, selector_seed=0))

    assert result.passed is False
    assert result.first_error_pc == 19
    assert result.error_class == "type_mismatch"


def test_surface_literal_contract_rejects_helper_checkpoint_surface_negative() -> None:
    result = validate_surface_literals(invalid_helper_checkpoint_braid_surface_program(6, base_address=264, selector_seed=1))

    assert result.passed is False
    assert result.first_error_pc == 7
    assert result.error_class == "undeclared_static_address"


def test_stress_reference_harness_reports_clean_positive_rows() -> None:
    medium_row = run_stress_reference_case(stress_reference_cases()[0])
    long_row = run_stress_reference_case(stress_reference_cases()[2])

    assert medium_row["mismatch_class"] is None
    assert medium_row["trace_match_current_lowered"] is True
    assert medium_row["trace_match_current_spec"] is True
    assert medium_row["trace_match_lowered_spec"] is True
    assert medium_row["diagnostic_surface_match"] is True
    assert long_row["mismatch_class"] is None
    assert long_row["all_final_state_match"] is True
    assert long_row["diagnostic_surface_match"] is True


def test_stress_reference_harness_matches_negative_controls() -> None:
    branch_row = run_stress_reference_case(stress_reference_cases()[3])
    surface_row = run_stress_reference_case(stress_reference_cases()[4])

    assert branch_row["mismatch_class"] is None
    assert branch_row["verifier_error_class"] == "type_mismatch"
    assert branch_row["spec_contract_error_class"] == "type_mismatch"
    assert surface_row["mismatch_class"] is None
    assert surface_row["surface_verifier_error_class"] == "undeclared_static_address"
    assert surface_row["surface_contract_error_class"] == "undeclared_static_address"


def test_export_m6_stress_reference_followup_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    summary_path = Path("results/M6_stress_reference_followup/summary.json")
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    assert payload["summary"]["row_count"] == 5
    assert payload["summary"]["positive_row_count"] == 3
    assert payload["summary"]["negative_control_count"] == 2
    assert payload["summary"]["exact_trace_match_count"] == 2
    assert payload["summary"]["exact_final_state_match_count"] == 1
    assert payload["summary"]["matched_negative_count"] == 2
    assert payload["summary"]["diagnostic_surface_match_count"] == 3
