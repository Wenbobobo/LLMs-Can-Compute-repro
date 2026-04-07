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


def test_export_f36_writes_qualification_only_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle.py",
        "export_f36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
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
    temp_f35_summary = tmp_path / "f35_summary.json"
    temp_f35_summary.write_text(
        json.dumps(
            {"summary": {"current_execution_candidate_count": 0}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h60_summary_path = module.H60_SUMMARY_PATH
    original_f34_summary_path = module.F34_SUMMARY_PATH
    original_f35_summary_path = module.F35_SUMMARY_PATH
    temp_out_dir = tmp_path / "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle"
    module.OUT_DIR = temp_out_dir
    module.H60_SUMMARY_PATH = temp_h60_summary
    module.F34_SUMMARY_PATH = temp_f34_summary
    module.F35_SUMMARY_PATH = temp_f35_summary
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H60_SUMMARY_PATH = original_h60_summary_path
        module.F34_SUMMARY_PATH = original_f34_summary_path
        module.F35_SUMMARY_PATH = original_f35_summary_path

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "compiled_online_route_qualified_on_paper_only_with_strict_preruntime_gates"
    assert payload["summary"]["admissible_reopen_family"] == "compiled_online_exact_retrieval_primitive_or_attention_coprocessor_route"
    assert payload["summary"]["immediate_stop_rule_count"] == 5
