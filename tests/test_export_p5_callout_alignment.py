from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p5_callout_alignment.py"
    spec = importlib.util.spec_from_file_location("export_p5_callout_alignment", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_contains_all_tolerates_wrapped_text() -> None:
    module = _load_export_module()

    assert module.contains_all(
        "The main text supports this endpoint with two artifacts:\nfrontend boundary diagram\nexact-trace/final-state success table\n",
        ["frontend boundary diagram", "exact-trace/final-state success table"],
    )


def test_build_alignment_rows_accepts_current_repo_state() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_alignment_rows(**inputs)

    assert all(row["status"] == "pass" for row in rows)


def test_build_summary_reports_zero_blocked_rows() -> None:
    module = _load_export_module()

    inputs = module.load_inputs()
    rows = module.build_alignment_rows(**inputs)
    summary = module.build_summary(rows)

    assert summary["alignment_scope"] == "p5_main_text_callout_and_caption_pairs"
    assert summary["blocked_count"] == 0
    assert summary["recommended_next_action"] == (
        "continue manuscript-freeze candidate assembly while keeping the current main-text artifact pairings fixed"
    )
