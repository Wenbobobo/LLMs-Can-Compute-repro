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


def test_export_p51_writes_paper_package_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p51_post_h62_paper_facing_partial_falsification_package.py",
        "export_p51_post_h62_paper_facing_partial_falsification_package",
    )

    temp_h62_summary = tmp_path / "h62_summary.json"
    temp_h62_summary.write_text(
        json.dumps({"summary": {"default_downstream_lane": "archive_or_hygiene_stop"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_p50_summary = tmp_path / "p50_summary.json"
    temp_p50_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "control_surfaces_locked_to_post_h62_archive_first_closeout"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_f37_summary = tmp_path / "f37_summary.json"
    temp_f37_summary.write_text(
        json.dumps({"summary": {"runtime_authorization": "closed"}}, indent=2) + "\n",
        encoding="utf-8",
    )

    pattern_sets = {
        "paper_bundle_status.md": [
            "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "archive-first partial-falsification closeout framing",
            "F38_post_h62_r63_dormant_eligibility_profile_dossier",
        ],
        "review_boundary_summary.md": [
            "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "dormant no-go dossier at `F38`",
            "executor-value on the strongest justified lane is closed negative",
        ],
        "release_summary_draft.md": [
            "archive-first closeout is now the default repo meaning",
            "R63 remains dormant",
            "paper-facing partial falsification",
        ],
        "claim_ladder.md": [
            "P51 paper-facing partial-falsification package",
            "F38 dormant R63 eligibility dossier",
            "H63 archive-first closeout packet",
        ],
        "claim_evidence_table.md": [
            "H63 is now the current active docs-only packet",
            "F38 is the current dormant future dossier",
            "P51 is the current paper-facing partial-falsification package",
        ],
        "archival_repro_manifest.md": [
            "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
            "scripts/export_p51_post_h62_paper_facing_partial_falsification_package.py",
            "scripts/export_f38_post_h62_r63_dormant_eligibility_profile_dossier.py",
        ],
        "submission_packet_index.md": [
            "../milestones/P51_post_h62_paper_facing_partial_falsification_package/",
            "../milestones/F38_post_h62_r63_dormant_eligibility_profile_dossier/",
            "../milestones/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/",
        ],
    }
    required_files = {}
    for name, patterns in pattern_sets.items():
        path = tmp_path / name
        path.write_text("\n".join(patterns) + "\n", encoding="utf-8")
        required_files[path] = patterns

    original_out_dir = module.OUT_DIR
    original_h62 = module.H62_SUMMARY_PATH
    original_p50 = module.P50_SUMMARY_PATH
    original_f37 = module.F37_SUMMARY_PATH
    original_requirements = module.AUDITED_FILE_REQUIREMENTS
    temp_out_dir = tmp_path / "P51_post_h62_paper_facing_partial_falsification_package"
    module.OUT_DIR = temp_out_dir
    module.H62_SUMMARY_PATH = temp_h62_summary
    module.P50_SUMMARY_PATH = temp_p50_summary
    module.F37_SUMMARY_PATH = temp_f37_summary
    module.AUDITED_FILE_REQUIREMENTS = required_files
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H62_SUMMARY_PATH = original_h62
        module.P50_SUMMARY_PATH = original_p50
        module.F37_SUMMARY_PATH = original_f37
        module.AUDITED_FILE_REQUIREMENTS = original_requirements

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "paper_surfaces_locked_to_archive_first_partial_falsification_closeout"
    assert payload["summary"]["audited_file_count"] == 7
    assert payload["summary"]["locked_file_count"] == 7
