from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_m7_frontend_candidate_decision.py"
    spec = importlib.util.spec_from_file_location("export_m7_frontend_candidate_decision", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_load_gate_inputs_reads_current_gate_bundles() -> None:
    module = _load_export_module()

    inputs = module.load_gate_inputs()

    assert inputs["p3_summary"]["summary"]["unsupported_claim_count"] >= 1
    assert inputs["r1_summary"]["summary"]["claim_update"] == "narrowed_positive_with_boundary"
    assert inputs["r2_summary"]["gate_summary"]["gate_status"] == "asymptotic_positive_but_end_to_end_not_yet_competitive"


def test_build_candidate_matrix_selects_restraint_on_current_results() -> None:
    module = _load_export_module()

    inputs = module.load_gate_inputs()
    rows = module.build_candidate_matrix(**inputs)

    selected = [row for row in rows if row["decision"] == "selected"]
    assert [row["candidate_id"] for row in selected] == ["stay_on_tiny_typed_bytecode"]
    assert any(row["candidate_id"] == "minimal_frontend_widening" and row["decision"] == "blocked" for row in rows)


def test_classify_minimal_widening_status_reopens_only_after_positive_systems_gate() -> None:
    module = _load_export_module()

    assert module.classify_minimal_widening_status(r2_gate_status="positive_current_scope", paper_scope_ready=True) == "revisit"
    assert module.classify_minimal_widening_status(r2_gate_status="positive_current_scope", paper_scope_ready=False) == "blocked"
    assert module.classify_minimal_widening_status(
        r2_gate_status="asymptotic_positive_but_end_to_end_not_yet_competitive",
        paper_scope_ready=True,
    ) == "blocked"
