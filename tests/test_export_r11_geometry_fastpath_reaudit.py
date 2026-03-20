from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r11_geometry_fastpath_reaudit.py"
    spec = importlib.util.spec_from_file_location("export_r11_geometry_fastpath_reaudit", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_r11_bounded_parity_rows_stay_exact() -> None:
    module = _load_export_module()

    rows = module.build_parity_rows()

    assert len(rows) == 5
    assert sum(bool(row["exact_match"]) for row in rows) == 5
    assert next(row for row in rows if row["case_id"] == "seeded_randomized_reference")["query_count"] == 200


def test_r11_same_endpoint_guard_blocks_executor_speedup_wording() -> None:
    module = _load_export_module()

    guard = module.build_same_endpoint_guard(
        {
            "summary": {
                "overall": {"profiled_row_count": 4, "representative_pair_count": 2},
                "claim_impact": {
                    "distilled_result": {
                        "dominant_component": "retrieval_total",
                        "median_exact_vs_lowered_ratio": 2429.0,
                        "median_retrieval_share_of_exact": 0.998,
                        "negative_attribution_explicit": True,
                    }
                },
            }
        }
    )

    assert guard["same_endpoint_fastpath_material"] is False
    assert guard["dominant_exact_component"] == "retrieval_total"


def test_export_r11_writes_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(
        Path("results/R11_geometry_fastpath_reaudit/summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["current_exactness"]["all_cases_exact"] is True
    assert summary["benchmark_reaudit"]["row_count"] == 4
    assert summary["same_endpoint_guard"]["same_endpoint_fastpath_material"] is False
    assert summary["claim_impact"]["next_lane"] == "R12_append_only_executor_long_horizon"
