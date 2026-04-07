"""Export the post-P78 archive claim-boundary and reopen-screen sidecar for P79."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P79_post_p78_archive_claim_boundary_and_reopen_screen"
P78_SUMMARY_PATH = ROOT / "results" / "P78_post_p77_legacy_worktree_convergence_and_quarantine_sync" / "summary.json"
CLAIM_BOUNDARY_PATH = ROOT / "docs" / "publication_record" / "partial_falsification_boundary.md"
REOPEN_SCREEN_PATH = ROOT / "docs" / "publication_record" / "future_reopen_screen.md"
PUBLICATION_README_PATH = ROOT / "docs" / "publication_record" / "README.md"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def main() -> None:
    p78_summary = read_json(P78_SUMMARY_PATH)["summary"]
    if p78_summary["selected_outcome"] != "balanced_worktree_convergence_completed_with_quarantines_preserved":
        raise RuntimeError("P79 expects the landed P78 convergence and quarantine sync sidecar.")

    claim_boundary_text = read_text(CLAIM_BOUNDARY_PATH)
    reopen_screen_text = read_text(REOPEN_SCREEN_PATH)
    publication_readme_text = read_text(PUBLICATION_README_PATH)

    checklist_rows = [
        {"item_id": "p79_reads_p78", "status": "pass", "notes": "P79 starts only after the landed P78 convergence sidecar."},
        {
            "item_id": "p79_claim_boundary_packages_partial_falsification",
            "status": "pass"
            if contains_all(
                claim_boundary_text,
                [
                    "supported claims",
                    "unsupported claims",
                    "executor-value lane is closed",
                    "append-only trace",
                    "exact 2d hard-max retrieval",
                    "arbitrary c remains unsupported",
                    "no broad wasm reopening",
                    "dead ends to avoid",
                ],
            )
            else "blocked",
            "notes": "The claim-boundary doc should package the narrow support and broader partial falsification clearly.",
        },
        {
            "item_id": "p79_reopen_screen_locks_non_runtime_gate",
            "status": "pass"
            if contains_all(
                reopen_screen_text,
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
            else "blocked",
            "notes": "The reopen screen should keep any future route non-runtime and materially different in cost structure.",
        },
        {
            "item_id": "p79_publication_router_exposes_boundary_docs",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "partial_falsification_boundary.md",
                    "future_reopen_screen.md",
                    "archive-facing control surfaces",
                ],
            )
            else "blocked",
            "notes": "Publication router should expose the claim-boundary and reopen-screen docs as live control surfaces.",
        },
    ]
    claim_packet = {
        "supports": [
            "P79 packages the strongest honest archive-facing statement: narrow mechanism support with broader executor-value failure.",
            "P79 preserves only a strictly non-runtime, cost-structure-different future gate.",
            "P79 turns prior GPTPro/origin advisory analysis into explicit local control docs without treating it as evidence.",
        ],
        "does_not_support": ["runtime reopen", "same-lane executor-value continuation", "broad Wasm/C claims"],
        "distilled_result": {
            "current_claim_boundary_wave": "p79_post_p78_archive_claim_boundary_and_reopen_screen",
            "selected_outcome": "archive_claim_boundary_and_reopen_screen_locked_after_convergence",
            "next_required_lane": "p80_next_planmode_handoff_sync",
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
            {"field": "claim_boundary_path", "value": str(CLAIM_BOUNDARY_PATH).replace("\\", "/")},
            {"field": "reopen_screen_path", "value": str(REOPEN_SCREEN_PATH).replace("\\", "/")},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
