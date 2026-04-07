from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_h35_post_p23_bounded_scalar_family_runtime_decision_packet.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_h35_post_p23_bounded_scalar_family_runtime_decision_packet",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_h35_writes_bounded_scalar_runtime_decision_packet(tmp_path: Path) -> None:
    module = _load_export_module()
    original_out_dir = module.OUT_DIR
    temp_out_dir = tmp_path / "H35_post_p23_bounded_scalar_family_runtime_decision_packet"
    module.OUT_DIR = temp_out_dir

    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    checklist_rows = json.loads((temp_out_dir / "checklist.json").read_text(encoding="utf-8"))["rows"]
    claim_packet = json.loads((temp_out_dir / "claim_packet.json").read_text(encoding="utf-8"))["summary"]

    assert payload["summary"]["active_stage"] == "h35_post_p23_bounded_scalar_family_runtime_decision_packet"
    assert payload["summary"]["selected_outcome"] == "authorize_one_bounded_scalar_family_runtime_gate"
    assert payload["summary"]["authorized_next_runtime_candidate"] == "r40_origin_bounded_scalar_locals_and_flags_gate"
    assert payload["summary"]["blocked_count"] == 0
    assert payload["summary"]["pass_count"] == len(checklist_rows)
    assert (
        claim_packet["distilled_result"]["authorized_runtime_scope"]
        == "same_substrate_same_opcode_frame_only_bounded_scalar_locals_and_flags"
    )
