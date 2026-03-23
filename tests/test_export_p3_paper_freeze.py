from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_p3_paper_freeze.py"
    spec = importlib.util.spec_from_file_location("export_p3_paper_freeze", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_claim_evidence_bullets_reads_current_claims() -> None:
    module = _load_export_module()
    text = (Path(__file__).resolve().parents[1] / "docs" / "publication_record" / "claim_evidence_table.md").read_text(
        encoding="utf-8"
    )

    sections = module.parse_claim_evidence_bullets(text)

    assert "current_evidence" in sections
    assert any(row["claim_id"] == "D0" for row in sections["current_evidence"])


def test_build_claim_scope_rows_includes_current_d0_row() -> None:
    module = _load_export_module()

    rows = module.build_claim_scope_rows()

    assert any(row["claim_layer"].startswith("D0") for row in rows)
    assert any(all(item["exists"] for item in row["best_evidence"]) for row in rows)


def test_get_first_present_value_supports_locked_header_name() -> None:
    module = _load_export_module()

    assert (
        module.get_first_present_value({"Boundary note": "locked"}, "Next evidence target", "Boundary note")
        == "locked"
    )


def test_build_unsupported_claims_captures_arbitrary_c_and_runtime_superiority() -> None:
    module = _load_export_module()

    rows = module.build_unsupported_claims()
    claim_ids = {row["claim_id"] for row in rows}
    arbitrary_c = next(row for row in rows if row["claim_id"] == "unsupported_arbitrary_c")

    assert "unsupported_arbitrary_c" in claim_ids
    assert "unsupported_current_scope_end_to_end_runtime_superiority" in claim_ids
    assert "current H43 paper endpoint" in arbitrary_c["reason"]
    assert "current compiled boundary is intentionally fixed" not in arbitrary_c["reason"]
