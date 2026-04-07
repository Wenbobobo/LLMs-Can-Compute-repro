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


def test_export_p46_writes_archive_first_publication_sync_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p46_post_h60_archive_first_publication_sync.py",
        "export_p46_post_h60_archive_first_publication_sync",
    )

    temp_h61_summary = tmp_path / "h61_summary.json"
    temp_h61_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "archive_first_consolidation_becomes_default_posture"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_f36_summary = tmp_path / "f36_summary.json"
    temp_f36_summary.write_text(
        json.dumps(
            {"summary": {"selected_outcome": "compiled_online_route_qualified_on_paper_only_with_strict_preruntime_gates"}},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temp_file_a = tmp_path / "README.md"
    temp_file_a.write_text(
        "\n".join(
            [
                "H61_post_h60_archive_first_position_packet",
                "P45_post_h60_clean_descendant_integration_readiness",
                "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
                "P46_post_h60_archive_first_publication_sync",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    temp_file_b = tmp_path / "release_summary_draft.md"
    temp_file_b.write_text(
        "\n".join(
            [
                "archive-first consolidation is now the default repo meaning",
                "narrow mechanistic reproduction plus executor-value partial falsification",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    original_out_dir = module.OUT_DIR
    original_h61_summary_path = module.H61_SUMMARY_PATH
    original_f36_summary_path = module.F36_SUMMARY_PATH
    original_requirements = module.AUDITED_FILE_REQUIREMENTS
    temp_out_dir = tmp_path / "P46_post_h60_archive_first_publication_sync"
    module.OUT_DIR = temp_out_dir
    module.H61_SUMMARY_PATH = temp_h61_summary
    module.F36_SUMMARY_PATH = temp_f36_summary
    module.AUDITED_FILE_REQUIREMENTS = {
        temp_file_a: [
            "H61_post_h60_archive_first_position_packet",
            "P45_post_h60_clean_descendant_integration_readiness",
            "F36_post_h60_conditional_compiled_online_reopen_qualification_bundle",
            "P46_post_h60_archive_first_publication_sync",
        ],
        temp_file_b: [
            "archive-first consolidation is now the default repo meaning",
            "narrow mechanistic reproduction plus executor-value partial falsification",
        ],
    }
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.H61_SUMMARY_PATH = original_h61_summary_path
        module.F36_SUMMARY_PATH = original_f36_summary_path
        module.AUDITED_FILE_REQUIREMENTS = original_requirements

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "publication_surfaces_locked_to_archive_first_partial_falsification_state"
    assert payload["summary"]["audited_file_count"] == 2
    assert payload["summary"]["locked_file_count"] == 2
