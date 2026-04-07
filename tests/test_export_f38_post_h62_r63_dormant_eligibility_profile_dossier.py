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


def test_export_f38_writes_dormant_dossier_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_f38_post_h62_r63_dormant_eligibility_profile_dossier.py",
        "export_f38_post_h62_r63_dormant_eligibility_profile_dossier",
    )

    temp_h62_summary = tmp_path / "h62_summary.json"
    temp_h62_summary.write_text(
        json.dumps({"summary": {"default_downstream_lane": "archive_or_hygiene_stop"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_f37_summary = tmp_path / "f37_summary.json"
    temp_f37_summary.write_text(
        json.dumps(
            {
                "summary": {
                    "runtime_authorization": "closed",
                    "narrow_target": "compiled_exact_hardmax_attention_coprocessor_on_lifted_useful_kernel_decode",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_gap = tmp_path / "eligibility_gap.md"
    temp_gap.write_text(
        "\n".join(
            [
                "compiled_exact_hardmax_attention_coprocessor_on_lifted_useful_kernel_decode",
                "honest comparator on the same lifted useful-kernel decode route: unresolved",
                "retrieval-head cost share: unresolved",
                "expected query:insert ratio: unresolved",
                "tie frequency and tie-handling burden: unresolved",
                "material cost-structure delta versus `R62/H58`: unresolved",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    temp_no_go = tmp_path / "no_go_rule.md"
    temp_no_go.write_text("R63\ndormant\nnon-runtime\n", encoding="utf-8")
    temp_protocol = tmp_path / "conditional_reopen_protocol.md"
    temp_protocol.write_text("R63\ndormant\nnon-runtime\n", encoding="utf-8")

    original_out_dir = module.OUT_DIR
    original_h62 = module.H62_SUMMARY_PATH
    original_f37 = module.F37_SUMMARY_PATH
    original_gap = module.ELIGIBILITY_GAP_PATH
    original_no_go = module.NO_GO_RULE_PATH
    original_protocol = module.CONDITIONAL_REOPEN_PROTOCOL_PATH
    temp_out_dir = tmp_path / "F38_post_h62_r63_dormant_eligibility_profile_dossier"
    module.OUT_DIR = temp_out_dir
    module.H62_SUMMARY_PATH = temp_h62_summary
    module.F37_SUMMARY_PATH = temp_f37_summary
    module.ELIGIBILITY_GAP_PATH = temp_gap
    module.NO_GO_RULE_PATH = temp_no_go
    module.CONDITIONAL_REOPEN_PROTOCOL_PATH = temp_protocol
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H62_SUMMARY_PATH = original_h62
        module.F37_SUMMARY_PATH = original_f37
        module.ELIGIBILITY_GAP_PATH = original_gap
        module.NO_GO_RULE_PATH = original_no_go
        module.CONDITIONAL_REOPEN_PROTOCOL_PATH = original_protocol

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "r63_profile_remains_dormant_and_ineligible_without_cost_profile_fields"
    assert payload["summary"]["exact_target_declared"] is True
    assert payload["summary"]["comparator_declared"] is False
    assert payload["summary"]["cost_share_declared"] is False
