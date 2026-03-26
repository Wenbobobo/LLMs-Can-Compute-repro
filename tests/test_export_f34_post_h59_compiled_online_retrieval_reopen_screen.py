from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module(script_name: str, module_name: str):
    module_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_f34_writes_compiled_online_reopen_screen(tmp_path: Path) -> None:
    module = _load_module(
        "export_f34_post_h59_compiled_online_retrieval_reopen_screen.py",
        "export_f34_post_h59_compiled_online_retrieval_reopen_screen",
    )

    temp_h59_summary = tmp_path / "h59_summary.json"
    temp_h59_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f33_summary = tmp_path / "f33_summary.json"
    temp_f33_summary.write_text(
        json.dumps(
            {"summary": {"admissible_reopen_requirement": "materially_different_cost_structure"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_p42_summary = tmp_path / "p42_summary.json"
    temp_p42_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "self_contained_gptpro_dossier_ready"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h59_summary_path = module.H59_SUMMARY_PATH
    original_f33_summary_path = module.F33_SUMMARY_PATH
    original_p42_summary_path = module.P42_SUMMARY_PATH
    temp_out_dir = tmp_path / "F34_post_h59_compiled_online_retrieval_reopen_screen"
    module.OUT_DIR = temp_out_dir
    module.H59_SUMMARY_PATH = temp_h59_summary
    module.F33_SUMMARY_PATH = temp_f33_summary
    module.P42_SUMMARY_PATH = temp_p42_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H59_SUMMARY_PATH = original_h59_summary_path
        module.F33_SUMMARY_PATH = original_f33_summary_path
        module.P42_SUMMARY_PATH = original_p42_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["admissible_reopen_family"] == "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"
    assert payload["summary"]["later_authorization_gate"] == "no_runtime_lane_open_until_later_explicit_authorization"
    assert payload["summary"]["project_default_fallback"] == "planning_only_or_project_stop"
