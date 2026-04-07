from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h33_post_h32_conditional_next_question_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h33_post_h32_conditional_next_question_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h33_writes_conditional_next_question_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H33_post_h32_conditional_next_question_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    assert payload["summary"]["active_stage"] == "h33_post_h32_conditional_next_question_packet"
    assert payload["summary"]["current_active_routing_stage"] == "h32_post_r38_compiled_boundary_refreeze"
    assert payload["summary"]["selected_outcome"] == "authorize_one_origin_core_substrate_question"
    assert payload["summary"]["authorized_next_runtime_candidate"] == "r39_origin_compiler_control_surface_dependency_audit"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert (
        claim_packet["distilled_result"]["authorized_runtime_scope"]
        == "same_substrate_same_opcode_same_admitted_and_boundary_rows_only"
    )
