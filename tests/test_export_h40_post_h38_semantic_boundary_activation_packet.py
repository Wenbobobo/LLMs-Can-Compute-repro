from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "export_h40_post_h38_semantic_boundary_activation_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h40_post_h38_semantic_boundary_activation_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h40_writes_semantic_boundary_activation_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H40_post_h38_semantic_boundary_activation_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]
    snapshot_rows = json.loads((temp_out_dir / "snapshot.json").read_text(encoding="utf-8"))["rows"]

    assert payload["summary"]["active_stage"] == "h40_post_h38_semantic_boundary_activation_packet"
    assert payload["summary"]["current_active_routing_stage"] == "h36_post_r40_bounded_scalar_family_refreeze"
    assert payload["summary"]["preserved_prior_docs_only_decision_packet"] == (
        "h38_post_f16_runtime_relevance_reopen_decision_packet"
    )
    assert payload["summary"]["selected_outcome"] == "authorize_r42_origin_append_only_memory_retrieval_contract_gate"
    assert payload["summary"]["authorized_next_runtime_candidate"] == (
        "r42_origin_append_only_memory_retrieval_contract_gate"
    )
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert claim_packet["distilled_result"]["current_semantic_boundary_roadmap"] == (
        "f19_post_f18_restricted_wasm_useful_case_roadmap"
    )
    assert len(snapshot_rows) == 3
