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


def test_export_p53_writes_claim_sync_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p53_post_h63_paper_archive_claim_sync.py",
        "export_p53_post_h63_paper_archive_claim_sync",
    )

    temp_h63_summary = tmp_path / "h63_summary.json"
    temp_h63_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "archive_first_closeout_becomes_current_active_route_and_r63_stays_dormant"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_h58_summary = tmp_path / "h58_summary.json"
    temp_h58_summary.write_text(
        json.dumps({"summary": {"selected_outcome": "stop_as_mechanism_supported_but_no_bounded_executor_value"}}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    temp_h43_summary = tmp_path / "h43_summary.json"
    temp_h43_summary.write_text(
        json.dumps({"summary": {"claim_d_state": "supported_here_narrowly"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_f38_summary = tmp_path / "f38_summary.json"
    temp_f38_summary.write_text(
        json.dumps({"summary": {"runtime_authorization": "closed"}}, indent=2) + "\n",
        encoding="utf-8",
    )

    pattern_sets = {
        "publication_readme.md": [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P53_post_h63_paper_archive_claim_sync",
            "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
            "P55_post_h63_clean_descendant_promotion_prep",
        ],
        "paper_bundle_status.md": [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P53_post_h63_paper_archive_claim_sync",
            "P55_post_h63_clean_descendant_promotion_prep",
            "archive-first partial-falsification closeout framing",
        ],
        "review_boundary_summary.md": [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "executor-value on the strongest justified lane is closed negative",
            "dormant no-go dossier at `F38`",
        ],
        "release_summary_draft.md": [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "archive-first freeze is now the default repo meaning",
            "R63 remains dormant",
        ],
        "claim_ladder.md": [
            "P53 paper/archive claim sync",
            "P54 Clean-descendant hygiene and artifact slimming",
            "P55 Clean-descendant promotion prep",
            "H64 archive-first freeze packet",
        ],
        "claim_evidence_table.md": [
            "H64` is now the current active docs-only packet",
            "P53` is the current paper/archive claim-sync wave",
            "P54` is the current repo-hygiene sidecar",
        ],
        "submission_candidate_criteria.md": [
            "H64_post_p53_p54_p55_f38_archive_first_freeze_packet",
            "P53_post_h63_paper_archive_claim_sync",
            "P54_post_h63_clean_descendant_hygiene_and_artifact_slimming",
            "P55_post_h63_clean_descendant_promotion_prep",
        ],
        "archival_repro_manifest.md": [
            "results/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/summary.json",
            "scripts/export_p53_post_h63_paper_archive_claim_sync.py",
            "scripts/export_h64_post_p53_p54_p55_f38_archive_first_freeze_packet.py",
        ],
        "submission_packet_index.md": [
            "../milestones/P53_post_h63_paper_archive_claim_sync/",
            "../milestones/H64_post_p53_p54_p55_f38_archive_first_freeze_packet/",
        ],
    }
    required_files = {}
    for name, patterns in pattern_sets.items():
        path = tmp_path / name
        path.write_text("\n".join(patterns) + "\n", encoding="utf-8")
        required_files[path] = patterns

    original_out_dir = module.OUT_DIR
    original_h63 = module.H63_SUMMARY_PATH
    original_h58 = module.H58_SUMMARY_PATH
    original_h43 = module.H43_SUMMARY_PATH
    original_f38 = module.F38_SUMMARY_PATH
    original_requirements = module.AUDITED_FILE_REQUIREMENTS
    temp_out_dir = tmp_path / "P53_post_h63_paper_archive_claim_sync"
    module.OUT_DIR = temp_out_dir
    module.H63_SUMMARY_PATH = temp_h63_summary
    module.H58_SUMMARY_PATH = temp_h58_summary
    module.H43_SUMMARY_PATH = temp_h43_summary
    module.F38_SUMMARY_PATH = temp_f38_summary
    module.AUDITED_FILE_REQUIREMENTS = required_files
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H63_SUMMARY_PATH = original_h63
        module.H58_SUMMARY_PATH = original_h58
        module.H43_SUMMARY_PATH = original_h43
        module.F38_SUMMARY_PATH = original_f38
        module.AUDITED_FILE_REQUIREMENTS = original_requirements

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "paper_archive_review_surfaces_locked_to_h64_archive_first_freeze"
    assert payload["summary"]["audited_file_count"] == 9
    assert payload["summary"]["locked_file_count"] == 9
