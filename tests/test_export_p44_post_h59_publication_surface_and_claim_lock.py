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


def test_export_p44_writes_publication_claim_lock_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p44_post_h59_publication_surface_and_claim_lock.py",
        "export_p44_post_h59_publication_surface_and_claim_lock",
    )

    temp_h60_summary = tmp_path / "h60_summary.json"
    temp_h60_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "remain_planning_only_and_prepare_stop_or_archive"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f34_summary = tmp_path / "f34_summary.json"
    temp_f34_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "admissible_reopen_family": "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_file_a = tmp_path / "README.md"
    temp_file_a.write_text(
        "H60_post_f34_next_lane_decision_packet\nP44_post_h59_publication_surface_and_claim_lock\n",
        encoding="utf-8",
    )
    temp_file_b = tmp_path / "claim_evidence_table.md"
    temp_file_b.write_text(
        "\n".join(
            [
                "narrow positive mechanism result survives",
                "broad headline reproduction did not land",
                "same-lane executor-value microvariants remain inadmissible",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h60_summary_path = module.H60_SUMMARY_PATH
    original_f34_summary_path = module.F34_SUMMARY_PATH
    original_requirements = module.AUDITED_FILE_REQUIREMENTS
    temp_out_dir = tmp_path / "P44_post_h59_publication_surface_and_claim_lock"
    module.OUT_DIR = temp_out_dir
    module.H60_SUMMARY_PATH = temp_h60_summary
    module.F34_SUMMARY_PATH = temp_f34_summary
    module.AUDITED_FILE_REQUIREMENTS = {
        temp_file_a: [
            "H60_post_f34_next_lane_decision_packet",
            "P44_post_h59_publication_surface_and_claim_lock",
        ],
        temp_file_b: [
            "narrow positive mechanism result survives",
            "broad headline reproduction did not land",
            "same-lane executor-value microvariants remain inadmissible",
        ],
    }
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H60_SUMMARY_PATH = original_h60_summary_path
        module.F34_SUMMARY_PATH = original_f34_summary_path
        module.AUDITED_FILE_REQUIREMENTS = original_requirements

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "publication_surfaces_locked_to_post_h59_archive_state"
    assert payload["summary"]["audited_file_count"] == 2
    assert payload["summary"]["locked_file_count"] == 2
