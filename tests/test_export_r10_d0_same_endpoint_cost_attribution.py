from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_r10_d0_same_endpoint_cost_attribution.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_r10_d0_same_endpoint_cost_attribution",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r10_representative_selection_is_bounded() -> None:
    module = _load_export_module()

    cases, selection_rows = module.load_representative_cases()

    assert len(selection_rows) == module.REPRESENTATIVE_TOP_FAMILY_PAIRS
    assert len(cases) == module.REPRESENTATIVE_TOP_FAMILY_PAIRS * 2
    assert {row["selection_rule"] for row in selection_rows} == {
        "top_2_harder_families_by_bytecode_step_count_plus_matched_r6_source_rows"
    }
    assert all(row["event_growth_vs_source"] >= 1.0 for row in selection_rows)


def test_r10_summary_distills_negative_attribution() -> None:
    module = _load_export_module()

    rows = [
        {
            "dominant_exact_component": "trace_bookkeeping",
            "exact_vs_lowered_ratio": 10.0,
            "retrieval_share_of_exact": 0.3,
            "harness_share_of_pipeline": 0.1,
        },
        {
            "dominant_exact_component": "local_transition",
            "exact_vs_lowered_ratio": 12.0,
            "retrieval_share_of_exact": 0.25,
            "harness_share_of_pipeline": 0.2,
        },
    ]
    selection_rows = [{"pair_rank": 1}, {"pair_rank": 2}]
    pair_rows = [{"pair_rank": 1}, {"pair_rank": 2}]

    summary = module.build_summary(rows, selection_rows, pair_rows)

    assert summary["overall"]["representative_pair_count"] == 2
    assert summary["overall"]["profiled_row_count"] == 2
    assert summary["overall"]["nonretrieval_dominant_row_count"] == 2
    assert summary["claim_impact"]["next_lane"] == "H12_refreeze_and_record_sync"
