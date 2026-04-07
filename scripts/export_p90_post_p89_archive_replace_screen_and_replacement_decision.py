"""Export the post-P89 archive-replace screen and replacement-decision packet for P90."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
DIRTY_ROOT = Path("D:/zWenbo/AI/LLMCompute")
OUT_DIR = ROOT / "results" / "P90_post_p89_archive_replace_screen_and_replacement_decision"
P89_SUMMARY_PATH = ROOT / "results" / "P89_post_p88_docs_consolidation_and_live_router_sync" / "summary.json"
CURRENT_BRANCH = "wip/p85-post-p84-main-rebaseline"
SCREENED_NOW = [
    "docs/publication_record/archival_repro_manifest.md",
    "docs/publication_record/release_candidate_checklist.md",
    "docs/publication_record/release_preflight_checklist.md",
    "docs/publication_record/submission_candidate_criteria.md",
    "docs/publication_record/submission_packet_index.md",
    "docs/publication_record/experiment_manifest.md",
]
DOC_REQUIREMENTS = {
    "README.md": [
        "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
        "P90_post_p89_archive_replace_screen_and_replacement_decision",
        "archive-then-replace closeout",
        "H66_post_p90_archive_replace_terminal_stop_packet",
    ],
    "STATUS.md": [
        "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
        "P90_post_p89_archive_replace_screen_and_replacement_decision",
        "archive-then-replace closeout",
        "file-specific salvage case",
    ],
    "docs/README.md": [
        "H65 + P90 + P89 + P88 + P87 + P86 + P85",
        "publication_record/current_stage_driver.md",
        "branch_worktree_registry.md",
        "plans/README.md",
    ],
    "docs/plans/README.md": [
        "P90",
        "current archive-replace decision wave",
        "current clean rebaseline branch",
        CURRENT_BRANCH,
    ],
    "docs/milestones/README.md": [
        "P90_post_p89_archive_replace_screen_and_replacement_decision",
        "P89_post_p88_docs_consolidation_and_live_router_sync",
        "P88_post_p87_salvage_screen_and_no_import_decision",
    ],
    "docs/publication_record/README.md": [
        "P90_post_p89_archive_replace_screen_and_replacement_decision",
        "root_salvage_shortlist.md",
        "current_stage_driver.md",
        "archival_repro_manifest.md",
    ],
    "docs/publication_record/current_stage_driver.md": [
        "P90_post_p89_archive_replace_screen_and_replacement_decision",
        "archive-then-replace closeout",
        "H66_post_p90_archive_replace_terminal_stop_packet",
        "file-specific salvage case",
    ],
    "docs/publication_record/root_salvage_shortlist.md": [
        "Keep Clean And Archive Root Only",
        "docs/publication_record/archival_repro_manifest.md",
        "docs/publication_record/release_candidate_checklist.md",
        "docs/publication_record/release_preflight_checklist.md",
        "docs/publication_record/submission_candidate_criteria.md",
        "docs/publication_record/submission_packet_index.md",
        "docs/publication_record/experiment_manifest.md",
    ],
}
FILE_RULES = {
    "docs/publication_record/archival_repro_manifest.md": {
        "clean_needles": [
            "results/H65_post_p66_p67_p68_archive_first_terminal_freeze_packet/summary.json",
            "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
            "Preserved immediate publication lineage",
        ],
        "dirty_stale_needles": [
            "results/H63_post_p50_p51_p52_f38_archive_first_closeout_packet/summary.json",
            "results/P50_post_h62_archive_first_control_sync/summary.json",
        ],
        "reason": "dirty-root version is keyed to the older H63/P50/P51/P52 closeout stack while the clean branch already carries the H65 archive-facing bundle.",
    },
    "docs/publication_record/release_candidate_checklist.md": {
        "clean_needles": [
            "`H65/P56/P57/P58/P59/P77/P78/P79/P80/F38`",
            "preserved `H64/H58/H43`",
        ],
        "dirty_stale_needles": [
            "State: `standing_gate`",
            "current `H25` active / `H23` frozen stack",
        ],
        "reason": "dirty-root version is an older H25/H23-era checklist and should not replace the restrained H65 release candidate surface.",
    },
    "docs/publication_record/release_preflight_checklist.md": {
        "clean_needles": [
            "`H65/P77/P78/P79/P80`",
            "`P72` hygiene-only archive-polish and explicit-stop handoff sidecar",
        ],
        "dirty_stale_needles": [
            "current active `H25` decision packet",
            "current frozen `H23` scientific state",
        ],
        "reason": "dirty-root version is bound to older H25/H23 preflight wording while the clean branch already reflects the H65 archive-facing control stack.",
    },
    "docs/publication_record/submission_candidate_criteria.md": {
        "clean_needles": [
            "`H65_post_p66_p67_p68_archive_first_terminal_freeze_packet`",
            "`H58_post_r62_origin_value_boundary_closeout_packet`",
            "`H43_post_r44_useful_case_refreeze`",
        ],
        "dirty_stale_needles": [
            "current active `H25` routing",
            "frozen `H23` evidence",
        ],
        "reason": "dirty-root version is still scoped to the old H25/H23 submission gate rather than the current H65 archive-facing closeout state.",
    },
    "docs/publication_record/submission_packet_index.md": {
        "clean_needles": [
            "H65_post_p66_p67_p68_archive_first_terminal_freeze_packet",
            "results/P80_post_p79_next_planmode_handoff_sync/summary.json",
            "do not widen the paper-facing evidence bundle",
        ],
        "dirty_stale_needles": [
            "H63_post_p50_p51_p52_f38_archive_first_closeout_packet",
            "P50_post_h62_archive_first_control_sync",
        ],
        "reason": "dirty-root version still points at the older H63/P50 archive-first packet instead of the current H65 bundle.",
    },
    "docs/publication_record/experiment_manifest.md": {
        "clean_needles": [
            "| 2026-03-26 | post-`H63` archive-first freeze wave |",
            "| 2026-03-26 | post-`H62` archive-first closeout wave |",
            "| 2026-03-26 | post-`H61` hygiene-first reauthorization prep |",
        ],
        "dirty_missing_needles": [
            "| 2026-03-26 | post-`H63` archive-first freeze wave |",
            "| 2026-03-26 | post-`H62` archive-first closeout wave |",
        ],
        "reason": "dirty-root version is missing the later archive-first closeout lineage that the clean branch already preserves in the manifest.",
    },
}


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


def git_output(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()
    except Exception:  # pragma: no cover
        return "unknown"


def normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize(text)
    return all(normalize(needle) in lowered for needle in needles)


def ahead_behind(left: str, right: str) -> str:
    value = git_output(["rev-list", "--left-right", "--count", f"{left}...{right}"])
    if value == "unknown":
        return value
    return value.replace(" ", "/")


def doc_sync_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative_path, needles in DOC_REQUIREMENTS.items():
        path = ROOT / relative_path
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "path": relative_path,
                "exists": exists,
                "needle_count": len(needles),
                "ok": exists and contains_all(text, needles),
            }
        )
    return rows


def classify_screen_row(relative_path: str) -> dict[str, object]:
    clean_text = read_text(ROOT / relative_path)
    dirty_path = DIRTY_ROOT / relative_path
    dirty_exists = dirty_path.exists()
    dirty_text = read_text(dirty_path) if dirty_exists else ""
    rule = FILE_RULES[relative_path]
    clean_ok = contains_all(clean_text, rule["clean_needles"])
    stale_dirty = False
    if "dirty_stale_needles" in rule:
        stale_dirty = any(normalize(needle) in normalize(dirty_text) for needle in rule["dirty_stale_needles"])
    if "dirty_missing_needles" in rule:
        stale_dirty = stale_dirty or not contains_all(dirty_text, rule["dirty_missing_needles"])

    if clean_ok and dirty_exists and stale_dirty:
        decision = "keep_clean_replace_root"
    else:
        decision = "file_specific_salvage_required"

    return {
        "path": relative_path,
        "dirty_exists": dirty_exists,
        "clean_ok": clean_ok,
        "decision": decision,
        "reason": rule["reason"],
    }


def main() -> None:
    p89_summary = read_json(P89_SUMMARY_PATH)["summary"]
    if p89_summary["selected_outcome"] != "docs_consolidation_and_live_router_sync_after_p88":
        raise RuntimeError("P90 expects the landed green P89 docs-consolidation summary.")
    if p89_summary["blocked_count"] != 0:
        raise RuntimeError("P90 expects a green P89 summary before archive-replace screening.")

    current_branch_name = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    current_head = git_output(["rev-parse", "--short", "HEAD"])
    origin_main_head = git_output(["rev-parse", "--short", "origin/main"])
    doc_rows = doc_sync_rows()
    screen_rows = [classify_screen_row(path) for path in SCREENED_NOW]

    checklist_rows = [
        {
            "item_id": "p90_reads_green_p89_summary",
            "status": "pass",
            "notes": "P90 begins only after the landed green P89 docs-consolidation packet.",
        },
        {
            "item_id": "p90_archive_replace_screen_resolves_remaining_publication_candidates",
            "status": "pass"
            if all(row["decision"] == "keep_clean_replace_root" for row in screen_rows)
            else "blocked",
            "notes": "The remaining six publication docs should close as keep-clean/archive-root-only unless a real file-specific salvage case appears.",
        },
        {
            "item_id": "p90_live_docs_shift_current_control_to_archive_replace_screen",
            "status": "pass" if all(bool(row["ok"]) for row in doc_rows) else "blocked",
            "notes": "Routers and publication docs should make P90 the current archive-replace decision wave.",
        },
    ]

    claim_packet = {
        "supports": [
            "P90 screens the remaining six dirty-root publication docs and closes them as keep-clean/archive-root-only decisions.",
            "P90 leaves no remaining mandatory selective-salvage follow-through on the clean branch.",
            "P90 narrows the next route to an H66 terminal-stop packet rather than more dirty-root imports.",
        ],
        "does_not_support": [
            "dirty-root integration",
            "runtime reopen",
            "same-lane executor-value reopen",
            "broad Wasm or arbitrary C scope expansion",
        ],
        "distilled_result": {
            "current_archive_replace_wave": "p90_post_p89_archive_replace_screen_and_replacement_decision",
            "current_branch": CURRENT_BRANCH if current_branch_name == "unknown" else current_branch_name,
            "current_branch_head": current_head,
            "merged_main_head": origin_main_head,
            "origin_main_to_p90_left_right": ahead_behind("origin/main", "HEAD"),
            "selected_outcome": "archive_replace_screen_completed_with_no_additional_salvage_after_p89",
            "next_recommended_route": "h66_archive_replace_terminal_stop_packet",
        },
    }
    summary = {
        "summary": {
            **claim_packet["distilled_result"],
            "screened_now_count": len(screen_rows),
            "keep_clean_replace_root_count": sum(row["decision"] == "keep_clean_replace_root" for row in screen_rows),
            "archive_only_preserve_root_count": 0,
            "file_specific_salvage_required_count": sum(
                row["decision"] == "file_specific_salvage_required" for row in screen_rows
            ),
            "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
            "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        },
        "runtime_environment": environment_payload(),
    }
    snapshot = {
        "rows": [
            {"field": "p89_summary", "value": p89_summary},
            {"field": "screen_rows", "value": screen_rows},
            {"field": "doc_sync_rows", "value": doc_rows},
        ]
    }

    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", snapshot)
    write_json(OUT_DIR / "summary.json", summary)


if __name__ == "__main__":
    main()
