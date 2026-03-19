from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_e1a_precision_patch.py"
    spec = importlib.util.spec_from_file_location("export_e1a_precision_patch", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_first_failure_rows_detects_single_head_failures() -> None:
    module = _load_export_module()

    c3d_rows = module.flatten_rows(
        module.read_json(Path(__file__).resolve().parents[1] / "results" / "M4_precision_scaling_real_traces" / "horizon_base_sweep.json"),
        suite_bundle="c3d_real",
    )
    c3e_rows = module.flatten_rows(
        module.read_json(Path(__file__).resolve().parents[1] / "results" / "M4_precision_generalization" / "boundary_sweep.json"),
        suite_bundle="c3e_generalized",
    )
    first_failure_rows = module.build_first_failure_rows(module.dedupe_rows([*c3d_rows, *c3e_rows]))

    assert len(first_failure_rows) > 0
    assert all(row["first_failure_horizon_multiplier"] >= 1 for row in first_failure_rows)


def test_build_claim_impact_stays_bounded() -> None:
    module = _load_export_module()

    c3d_rows = module.flatten_rows(
        module.read_json(Path(__file__).resolve().parents[1] / "results" / "M4_precision_scaling_real_traces" / "horizon_base_sweep.json"),
        suite_bundle="c3d_real",
    )
    c3e_rows = module.flatten_rows(
        module.read_json(Path(__file__).resolve().parents[1] / "results" / "M4_precision_generalization" / "boundary_sweep.json"),
        suite_bundle="c3e_generalized",
    )
    all_rows = module.dedupe_rows([*c3d_rows, *c3e_rows])
    first_failure_rows = module.build_first_failure_rows(all_rows)
    family_boundary_rows = module.build_family_boundary_rows(all_rows, first_failure_rows)
    claim_impact = module.build_claim_impact(
        first_failure_rows=first_failure_rows,
        family_boundary_rows=family_boundary_rows,
        organic_claim_impact=module.read_json(
            Path(__file__).resolve().parents[1] / "results" / "M4_precision_organic_traces" / "claim_impact.json"
        ),
    )

    assert claim_impact["target_claims"] == ["C3d", "C3e"]
    assert claim_impact["status"] == "sharpened_current_suite_boundary"
