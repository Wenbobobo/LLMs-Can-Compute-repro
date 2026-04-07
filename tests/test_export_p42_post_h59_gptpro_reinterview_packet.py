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


def test_export_p42_writes_gptpro_packet_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p42_post_h59_gptpro_reinterview_packet.py",
        "export_p42_post_h59_gptpro_reinterview_packet",
    )

    temp_h59_summary = tmp_path / "h59_summary.json"
    temp_h59_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "selected_outcome": "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_dossier = tmp_path / "dossier.md"
    temp_dossier.write_text("# dossier\n", encoding="utf-8")

    original_out_dir = module.OUT_DIR
    original_h59_summary_path = module.H59_SUMMARY_PATH
    original_dossier_path = module.DOSSIER_PATH
    temp_out_dir = tmp_path / "P42_post_h59_gptpro_reinterview_packet"
    module.OUT_DIR = temp_out_dir
    module.H59_SUMMARY_PATH = temp_h59_summary
    module.DOSSIER_PATH = temp_dossier
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H59_SUMMARY_PATH = original_h59_summary_path
        module.DOSSIER_PATH = original_dossier_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "self_contained_gptpro_dossier_ready"
    assert payload["summary"]["included_code_file_count"] == 6
    assert payload["summary"]["current_downstream_scientific_lane"] == "planning_only_or_project_stop"
