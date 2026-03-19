"""Export the P10 submission/archive packet readiness audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P10_submission_archive_ready"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


def contains_none(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() not in lowered for needle in needles)


def extract_matching_lines(text: str, *, needles: list[str], max_lines: int = 8) -> list[str]:
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles):
            if line not in seen:
                hits.append(line)
                seen.add(line)
        if len(hits) >= max_lines:
            break
    return hits


def load_inputs() -> dict[str, Any]:
    return {
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "planning_state_taxonomy_text": read_text(ROOT / "docs" / "publication_record" / "planning_state_taxonomy.md"),
        "submission_packet_index_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_packet_index.md"
        ),
        "archival_repro_manifest_text": read_text(
            ROOT / "docs" / "publication_record" / "archival_repro_manifest.md"
        ),
        "review_boundary_summary_text": read_text(
            ROOT / "docs" / "publication_record" / "review_boundary_summary.md"
        ),
        "external_release_note_skeleton_text": read_text(
            ROOT / "docs" / "publication_record" / "external_release_note_skeleton.md"
        ),
        "p1_summary": read_json(ROOT / "results" / "P1_paper_readiness" / "summary.json"),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "p5_callout_summary": read_json(ROOT / "results" / "P5_callout_alignment" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
    }


def ready_count_from_p1_summary(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["blocked_count"])


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    planning_state_taxonomy_text: str,
    submission_packet_index_text: str,
    archival_repro_manifest_text: str,
    review_boundary_summary_text: str,
    external_release_note_skeleton_text: str,
    p1_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    p5_callout_summary: dict[str, Any],
    h2_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "active_driver_names_current_packet",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h4_reproduction_mainline_return`",
                    "`e1a_precision_patch`",
                    "`e1b_systems_patch`",
                    "`h5_repro_sync_and_refreeze`",
                    "`e1c_compiled_boundary_patch`",
                    "logical lane order remains `e1a_precision_patch` -> `e1b_systems_patch`",
                    "completed baseline",
                ],
            )
            else "blocked",
            "notes": "The current-stage driver should expose the active bounded return packet and conditional compiled lane.",
        },
        {
            "item_id": "planning_taxonomy_assigns_single_active_driver",
            "status": "pass"
            if contains_all(
                planning_state_taxonomy_text,
                [
                    "`active_driver`",
                    "`standing_gate`",
                    "`historical_complete`",
                    "`dormant_protocol`",
                    "`docs/publication_record/current_stage_driver.md`",
                    "`docs/publication_record/release_candidate_checklist.md`",
                    "`docs/publication_record/paper_package_plan.md`",
                    "`docs/publication_record/conditional_reopen_protocol.md`",
                ],
            )
            else "blocked",
            "notes": "The planning taxonomy should make active-driver and gate ownership explicit.",
        },
        {
            "item_id": "submission_packet_names_canonical_bundle",
            "status": "pass"
            if contains_all(
                submission_packet_index_text,
                [
                    "`manuscript_bundle_draft.md`",
                    "`main_text_order.md`",
                    "`appendix_companion_scope.md`",
                    "`claim_ladder.md`",
                    "`claim_evidence_table.md`",
                    "`current_stage_driver.md`",
                    "`results/p1_paper_readiness/summary.json`",
                    "`results/p10_submission_archive_ready/summary.json`",
                ],
            )
            else "blocked",
            "notes": "The packet index should identify the canonical manuscript, appendix, control docs, and audit anchors.",
        },
        {
            "item_id": "archival_manifest_names_regeneration_and_restrictions",
            "status": "pass"
            if contains_all(
                archival_repro_manifest_text,
                [
                    "python `3.12`",
                    "`uv`",
                    "uv run python scripts/export_p1_paper_readiness.py",
                    "uv run python scripts/export_p5_public_surface_sync.py",
                    "uv run python scripts/export_h2_bundle_lock_audit.py",
                    "uv run python scripts/export_p10_submission_archive_ready.py",
                    "`docs/Origin/`",
                    "`docs/origin/`",
                ],
            )
            else "blocked",
            "notes": "The archival manifest should document regeneration commands and explicit restricted-source exclusions.",
        },
        {
            "item_id": "review_boundary_summary_preserves_scope",
            "status": "pass"
            if contains_all(
                review_boundary_summary_text,
                [
                    "append-only execution trace",
                    "structured 2d hard-max mechanism",
                    "tiny typed-bytecode `d0`",
                    "no general “llms are computers” claim",
                    "`e1a_precision_patch`",
                    "`e1b_systems_patch`",
                    "`e1c_compiled_boundary_patch`",
                ],
            )
            else "blocked",
            "notes": "The review-boundary summary should preserve supported claims, blocked claims, and explicit reopen routing.",
        },
        {
            "item_id": "external_release_note_stays_downstream",
            "status": "pass"
            if contains_all(
                external_release_note_skeleton_text,
                [
                    "downstream-only skeleton",
                    "narrow execution-substrate claim",
                    "tiny typed-bytecode `d0`",
                    "results/p10_submission_archive_ready/summary.json",
                    "blog remains blocked",
                ],
            )
            else "blocked",
            "notes": "The release-note skeleton should remain restrained and explicitly downstream-only.",
        },
        {
            "item_id": "top_level_docs_align_with_current_driver",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "the active stage is a bounded scientific return",
                    "`h4` resets the driver to reproduction",
                    "`e1a` sharpens the bounded precision story",
                    "`e1c` stays conditional only",
                ],
            )
            and contains_all(
                status_text,
                [
                    "current active post-`p9` operational stage is a bounded reproduction-mainline return",
                    "`h4`, `e1a`, `e1b`, and `h5`",
                    "`e1c` remains conditional only",
                    "logical lane order stays `e1a` then `e1b`",
                ],
            )
            and contains_all(
                publication_readme_text,
                [
                    "`current_stage_driver.md`",
                    "`planning_state_taxonomy.md`",
                    "`submission_packet_index.md`",
                    "`archival_repro_manifest.md`",
                ],
            )
            else "blocked",
            "notes": "README, STATUS, and the publication index should all reflect the same active driver and packet docs.",
        },
        {
            "item_id": "packet_docs_keep_restricted_sources_out_of_public_bundle",
            "status": "pass"
            if contains_none(
                submission_packet_index_text + "\n" + review_boundary_summary_text + "\n" + external_release_note_skeleton_text,
                ["docs/origin/", "docs/Origin/"],
            )
            else "blocked",
            "notes": "Public packet docs other than the archive manifest should not depend on restricted-source paths.",
        },
        {
            "item_id": "standing_audits_remain_green",
            "status": "pass"
            if ready_count_from_p1_summary(p1_summary) == 10
            and not p1_summary["blocked_or_partial_items"]
            and blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(p5_callout_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            else "blocked",
            "notes": "The existing standing audits must stay green before the packet is called archive-ready.",
        },
    ]


def build_packet_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "The active stage is a bounded scientific return",
                "`H4` resets the driver to reproduction",
                "`E1a` sharpens the bounded precision story",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "current active post-`P9` operational stage is a bounded reproduction-mainline return",
                "`H4`, `E1a`, `E1b`, and `H5`",
                "`E1c` remains conditional only",
            ],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`H4_reproduction_mainline_return`",
                "`E1a_precision_patch`",
                "`E1b_systems_patch`",
                "`H5_repro_sync_and_refreeze`",
                "completed baseline",
            ],
        ),
        "docs/publication_record/submission_packet_index.md": (
            "submission_packet_index_text",
            [
                "`manuscript_bundle_draft.md`",
                "`appendix_companion_scope.md`",
                "`current_stage_driver.md`",
                "`results/P10_submission_archive_ready/summary.json`",
            ],
        ),
        "docs/publication_record/archival_repro_manifest.md": (
            "archival_repro_manifest_text",
            [
                "Python `3.12`",
                "`uv`",
                "uv run python scripts/export_p10_submission_archive_ready.py",
                "`docs/Origin/`",
            ],
        ),
        "docs/publication_record/review_boundary_summary.md": (
            "review_boundary_summary_text",
            [
                "append-only execution trace",
                "tiny typed-bytecode `D0`",
                "no arbitrary C reproduction claim",
                "`E1a_precision_patch`",
            ],
        ),
        "docs/publication_record/external_release_note_skeleton.md": (
            "external_release_note_skeleton_text",
            [
                "downstream-only skeleton",
                "narrow execution-substrate claim",
                "tiny typed-bytecode `D0`",
                "blog remains blocked",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append(
            {
                "path": path,
                "matched_lines": extract_matching_lines(inputs[input_key], needles=needles),
            }
        )
    return rows


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "reproduction_mainline_return_active",
        "packet_state": "archive_ready" if not blocked_items else "blocked",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use submission_packet_index.md plus archival_repro_manifest.md as the canonical handoff for venue-specific packaging while keeping scope fixed"
            if not blocked_items
            else "resolve the blocked packet-readiness items before treating the bundle as archive-ready"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    rows = build_checklist_rows(**inputs)
    snapshot = build_packet_snapshot(inputs)
    summary = build_summary(rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p10_submission_archive_ready_checklist",
            "environment": environment.as_dict(),
            "rows": rows,
        },
    )
    write_json(
        OUT_DIR / "packet_snapshot.json",
        {
            "experiment": "p10_submission_archive_ready_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p10_submission_archive_ready",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/planning_state_taxonomy.md",
                "docs/publication_record/submission_packet_index.md",
                "docs/publication_record/archival_repro_manifest.md",
                "docs/publication_record/review_boundary_summary.md",
                "docs/publication_record/external_release_note_skeleton.md",
                "results/P1_paper_readiness/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/P5_callout_alignment/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# P10 Submission Archive Ready",
                "",
                "Machine-readable audit of whether the current locked checkpoint can be",
                "handed off as a venue-agnostic submission/archive packet without widening",
                "scientific scope.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `packet_snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
