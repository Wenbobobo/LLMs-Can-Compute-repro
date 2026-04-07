from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p79_post_p78_archive_claim_boundary_and_reopen_screen.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p79_post_p78_archive_claim_boundary_and_reopen_screen",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p79_writes_claim_boundary_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p78_summary = _write_json(
        "p78_summary.json",
        {"summary": {"selected_outcome": "balanced_worktree_convergence_completed_with_quarantines_preserved"}},
    )
    temp_boundary = _write_text(
        "partial_falsification_boundary.md",
        [
            "supported claims",
            "unsupported claims",
            "executor-value lane is closed",
            "append-only trace",
            "exact 2D hard-max retrieval",
            "arbitrary C remains unsupported",
            "no broad Wasm reopening",
            "dead ends to avoid",
        ],
    )
    temp_reopen = _write_text(
        "future_reopen_screen.md",
        [
            "strictly non-runtime",
            "cost-structure-different route only",
            "useful target",
            "comparator",
            "cost share",
            "query:insert ratio",
            "tie burden",
            "cost model",
            "do not reopen same-lane executor-value work",
        ],
    )
    temp_publication_readme = _write_text(
        "publication_readme.md",
        [
            "partial_falsification_boundary.md",
            "future_reopen_screen.md",
            "archive-facing control surfaces",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p78 = module.P78_SUMMARY_PATH
    original_boundary = module.CLAIM_BOUNDARY_PATH
    original_reopen = module.REOPEN_SCREEN_PATH
    original_publication = module.PUBLICATION_README_PATH
    temp_out_dir = tmp_path / "P79_post_p78_archive_claim_boundary_and_reopen_screen"
    module.OUT_DIR = temp_out_dir
    module.P78_SUMMARY_PATH = temp_p78_summary
    module.CLAIM_BOUNDARY_PATH = temp_boundary
    module.REOPEN_SCREEN_PATH = temp_reopen
    module.PUBLICATION_README_PATH = temp_publication_readme
    monkeypatch.setattr(module, "environment_payload", lambda: {"runtime_detection": "test"})
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P78_SUMMARY_PATH = original_p78
        module.CLAIM_BOUNDARY_PATH = original_boundary
        module.REOPEN_SCREEN_PATH = original_reopen
        module.PUBLICATION_README_PATH = original_publication

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "archive_claim_boundary_and_reopen_screen_locked_after_convergence"
    assert payload["summary"]["blocked_count"] == 0
