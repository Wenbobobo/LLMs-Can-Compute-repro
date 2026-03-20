from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_r4_mechanistic_retrieval_closure.py"
    spec = importlib.util.spec_from_file_location("export_r4_mechanistic_retrieval_closure", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_load_positive_cases_returns_current_union() -> None:
    module = _load_export_module()

    cases = module.load_positive_cases()
    names = {case.program.name for case in cases}

    assert len(cases) == 32
    assert "bytecode_call_add_halt" in names
    assert "bytecode_helper_checkpoint_braid_long_18_a312_s0" in names


def test_export_r4_mechanistic_retrieval_closure_builds_expected_summary() -> None:
    module = _load_export_module()
    module.main()

    payload = json.loads(
        Path("results/R4_mechanistic_retrieval_closure/summary.json").read_text(encoding="utf-8")
    )
    summary = payload["summary"]

    assert summary["overall"]["program_count"] == 32
    assert summary["overall"]["unexplained_event_count"] == 0
    assert summary["overall"]["parity_failure_count"] == 0
    assert summary["overall"]["contradiction_candidate_count"] == 0
    assert summary["overall"]["primitive_event_counts"]["latest_write"] > 0
    assert summary["overall"]["primitive_event_counts"]["stack"] > 0
    assert summary["overall"]["primitive_event_counts"]["control"] > 0
    assert summary["overall"]["primitive_event_counts"]["local_transition"] > 0
    assert summary["diagnostic_companion_role"] == "diagnostic_only_mask_strength_evidence"
    assert summary["claim_impact"]["r5_status"] == "not_justified"
    assert summary["claim_impact"]["next_lane"] == "H7_refreeze_and_record_sync"
