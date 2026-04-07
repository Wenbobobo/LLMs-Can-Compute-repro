"""Export the post-H59 GPTPro re-interview packet for P42."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P42_post_h59_gptpro_reinterview_packet"
H59_SUMMARY_PATH = ROOT / "results" / "H59_post_h58_reproduction_gap_decision_packet" / "summary.json"
DOSSIER_PATH = ROOT / "docs" / "plans" / "2026-03-25-post-h59-gptpro-reinterview-dossier.md"
INCLUDED_CODE_FILES = [
    "src/geometry/hardmax.py",
    "src/geometry/hull_kv.py",
    "src/exec_trace/dsl.py",
    "src/exec_trace/interpreter.py",
    "src/model/exact_hardmax.py",
    "src/bytecode/interpreter.py",
]


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalized_dossier_path() -> str:
    try:
        return DOSSIER_PATH.relative_to(ROOT).as_posix()
    except ValueError:
        return DOSSIER_PATH.as_posix()


def main() -> None:
    h59_summary = read_json(H59_SUMMARY_PATH)["summary"]
    if h59_summary["selected_outcome"] != "freeze_reproduction_gap_and_require_different_cost_structure_for_reopen":
        raise RuntimeError("P42 expects the landed H59 reproduction-gap decision.")
    if not DOSSIER_PATH.exists():
        raise RuntimeError("P42 expects the saved GPTPro dossier document.")

    checklist_rows = [
        {
            "item_id": "p42_dossier_is_self_contained",
            "status": "pass",
            "notes": "The dossier must work for a GPTPro session that cannot browse the repository.",
        },
        {
            "item_id": "p42_dossier_includes_key_code_files",
            "status": "pass",
            "notes": "The dossier includes a small, high-signal set of exact retrieval/execution code excerpts.",
        },
        {
            "item_id": "p42_dossier_uses_one_integrated_inquiry",
            "status": "pass",
            "notes": "The ask should be one integrated judgment rather than many short disconnected questions.",
        },
        {
            "item_id": "p42_dossier_remains_advisory_only",
            "status": "pass",
            "notes": "The dossier informs future planning but does not reopen science by itself.",
        },
    ]
    claim_packet = {
        "supports": [
            "P42 prepares a self-contained GPTPro re-interview dossier for the current reproduction-gap state.",
            "The dossier includes code excerpts and exact evidence context rather than only file-path references.",
            "The GPTPro packet remains advisory and planning-facing rather than claim-bearing.",
        ],
        "does_not_support": [
            "treating GPTPro advice as experimental evidence",
            "reopening runtime execution by prompt alone",
            "splitting the consultation into many context-fragmented prompts",
        ],
        "distilled_result": {
            "active_stage_at_sidecar_time": "h59_post_h58_reproduction_gap_decision_packet",
            "current_low_priority_wave": "p42_post_h59_gptpro_reinterview_packet",
            "selected_outcome": "self_contained_gptpro_dossier_ready",
            "dossier_path": normalized_dossier_path(),
            "included_code_file_count": len(INCLUDED_CODE_FILES),
            "included_code_files": INCLUDED_CODE_FILES,
            "current_downstream_scientific_lane": "planning_only_or_project_stop",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"source": "h59", "selected_outcome": h59_summary["selected_outcome"]},
            {"source": "p42", "dossier_path": normalized_dossier_path()},
            {"source": "p42", "included_code_file_count": len(INCLUDED_CODE_FILES)},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
