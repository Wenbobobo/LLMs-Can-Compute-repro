from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r1_precision_mechanism_closure.py"
    spec = importlib.util.spec_from_file_location("export_r1_precision_mechanism_closure", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_load_rows_reads_offset_and_organic_precision_bundles() -> None:
    module = _load_export_module()

    rows, claim_impact = module.load_rows()

    assert len(rows) > 0
    assert any(row["suite_bundle"] == "offset" for row in rows)
    assert any(row["suite_bundle"] == "organic" for row in rows)
    assert claim_impact["target_claim"] == "C3e"


def test_build_stream_summary_finds_single_head_failure_rows() -> None:
    module = _load_export_module()
    rows, _ = module.load_rows()

    stream_rows = module.build_stream_summary(rows)

    assert any(row["single_head_first_failure_multiplier"] == 1 for row in stream_rows)
    assert any(row["decomposition_has_fully_passing_config"] for row in stream_rows)


def test_build_summary_reports_distilled_boundary_sections() -> None:
    module = _load_export_module()
    rows, claim_impact = module.load_rows()
    stream_rows = module.build_stream_summary(rows)
    family_rows = module.build_family_summary(stream_rows)
    scheme_rows = module.build_scheme_summary(rows)

    summary = module.build_summary(
        rows=rows,
        stream_summary_rows=stream_rows,
        family_summary_rows=family_rows,
        scheme_summary_rows=scheme_rows,
        claim_impact=claim_impact,
    )

    assert summary["stream_count"] > 0
    assert "helps_here" in summary["distilled_boundary"]
    assert summary["single_head_failure_stream_count"] >= 1
