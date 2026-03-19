from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p1_paper_readiness.py"
    spec = importlib.util.spec_from_file_location("export_p1_paper_readiness", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_markdown_tables_extracts_rows() -> None:
    module = _load_export_module()
    text = """
| A | B |
| --- | --- |
| x | y |
| p | q |
"""
    tables = module.parse_markdown_tables(text)

    assert len(tables) == 1
    assert tables[0][0] == {"A": "x", "B": "y"}
    assert tables[0][1] == {"A": "p", "B": "q"}


def test_extract_backtick_paths_returns_all_paths() -> None:
    module = _load_export_module()
    text = "`results/foo.json`, `docs/bar.md`"

    assert module.extract_backtick_paths(text) == ["results/foo.json", "docs/bar.md"]


def test_get_first_present_value_supports_legacy_and_locked_headers() -> None:
    module = _load_export_module()

    assert (
        module.get_first_present_value({"Boundary note": "locked"}, "Next evidence target", "Boundary note")
        == "locked"
    )


def test_build_claim_bundle_completeness_reads_current_ledgers() -> None:
    module = _load_export_module()
    payload = module.build_claim_bundle_completeness()

    assert payload["summary"]["claim_count"] > 0
    assert any(row["claim_layer"].startswith("C2h") for row in payload["claims"])
    assert any(row["completeness"] == "complete" for row in payload["claims"])


def test_path_exists_supports_globs() -> None:
    module = _load_export_module()

    assert module.path_exists("results/M4_staged_pointer_decoder/*.json") is True
