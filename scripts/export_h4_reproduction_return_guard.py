"""Export the preserved H4 reproduction-mainline return historical guard."""

from __future__ import annotations

import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H4_reproduction_return_guard"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_text_space(text: str) -> str:
    return " ".join(text.split())


def contains_all(text: str, needles: list[str]) -> bool:
    lowered = normalize_text_space(text).lower()
    return all(normalize_text_space(needle).lower() in lowered for needle in needles)


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


def load_inputs() -> dict[str, str]:
    return {
        "master_plan_text": read_text(ROOT / "tmp" / "2026-03-19-reproduction-mainline-return-master-plan.md"),
        "h4_status_text": read_text(ROOT / "docs" / "milestones" / "H4_reproduction_mainline_return" / "status.md"),
        "h4_todo_text": read_text(ROOT / "docs" / "milestones" / "H4_reproduction_mainline_return" / "todo.md"),
        "h5_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "H5_repro_sync_and_refreeze" / "artifact_index.md"
        ),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "m7_decision_text": read_text(ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json"),
    }


def build_checklist_rows(
    *,
    master_plan_text: str,
    h4_status_text: str,
    h4_todo_text: str,
    h5_artifact_index_text: str,
    experiment_manifest_text: str,
    current_stage_driver_text: str,
    m7_decision_text: str,
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "historical_h4_plan_is_preserved",
            "status": "pass"
            if contains_all(
                master_plan_text,
                [
                    "reproduction mainline return",
                    "`h4_reproduction_mainline_return`",
                    "`e1a_precision_patch`",
                    "`e1b_systems_patch`",
                    "`h5_repro_sync_and_refreeze`",
                ],
            )
            else "blocked",
            "notes": "The saved H4 plan should remain preserved under tmp/ for archiveability.",
        },
        {
            "item_id": "h4_milestone_marks_the_packet_completed",
            "status": "pass"
            if contains_all(
                h4_status_text,
                [
                    "opened and completed on 2026-03-19",
                    "reproduction mainline",
                    "bounded scientific follow-up",
                ],
            )
            and contains_all(
                h4_todo_text,
                [
                    "- [x] Save the full current-round return plan to `tmp/`.",
                    "- [x] Add one `H4` guard export and regression test.",
                    "- [x] Record the `H4` batch in `experiment_manifest.md`.",
                ],
            )
            else "blocked",
            "notes": "The H4 milestone docs should now mark the packet completed rather than still-open work.",
        },
        {
            "item_id": "current_stage_driver_has_advanced_beyond_h4",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "is the current refrozen control stage",
                    "`docs/milestones/h15_refreeze_and_decision_sync/result_digest.md`",
                ],
            )
            else "blocked",
            "notes": "The repo should have advanced to the later H15 refrozen state instead of still treating H4 as active.",
        },
        {
            "item_id": "manifest_and_h5_archive_preserve_h4_artifacts",
            "status": "pass"
            if contains_all(
                experiment_manifest_text,
                [
                    "| 2026-03-19 | `h4_reproduction_mainline_return` |",
                    "scripts/export_h4_reproduction_return_guard.py",
                    "new `results/h4_reproduction_return_guard/`",
                ],
            )
            and contains_all(
                h5_artifact_index_text,
                [
                    "- `results/h4_reproduction_return_guard/summary.json`",
                    "- `results/e1a_precision_patch/summary.json`",
                    "- `results/e1b_systems_patch/summary.json`",
                ],
            )
            else "blocked",
            "notes": "The manifest and H5 archive should keep the completed H4 packet visible as history.",
        },
        {
            "item_id": "m7_no_widening_still_explicit",
            "status": "pass"
            if contains_all(
                m7_decision_text,
                [
                    "\"frontend_widening_authorized\": false",
                    "\"public_demo_authorized\": false",
                    "\"selected_candidate_id\": \"stay_on_tiny_typed_bytecode\"",
                ],
            )
            else "blocked",
            "notes": "The active return stage must not weaken the prior no-widening decision.",
        },
    ]


def build_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    lookup = {
        "tmp/2026-03-19-reproduction-mainline-return-master-plan.md": (
            "master_plan_text",
            ["Scientific target", "`H4_reproduction_mainline_return`", "`E1a_precision_patch`"],
        ),
        "docs/milestones/H4_reproduction_mainline_return/status.md": (
            "h4_status_text",
            ["Opened and completed on 2026-03-19", "bounded scientific follow-up"],
        ),
        "docs/milestones/H4_reproduction_mainline_return/todo.md": (
            "h4_todo_text",
            ["- [x] Add one `H4` guard export and regression test.", "- [x] Record the `H4` batch in `experiment_manifest.md`."],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            ["| 2026-03-19 | `H4_reproduction_mainline_return` |", "new `results/H4_reproduction_return_guard/`"],
        ),
        "docs/milestones/H5_repro_sync_and_refreeze/artifact_index.md": (
            "h5_artifact_index_text",
            ["- `results/H4_reproduction_return_guard/summary.json`", "- `results/E1a_precision_patch/summary.json`"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["`H15_refreeze_and_decision_sync`", "is the current refrozen control stage"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "preserved_baseline_stage": "h4_reproduction_mainline_return",
        "successor_refreeze_stage": "h5_repro_sync_and_refreeze",
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "preserve the completed H4 return packet as the historical pivot into the later E1/H5 and H15 control chain while keeping the current repo state refrozen on H15"
            if not blocked_items
            else "restore the missing H4 archival links before relying on the later refrozen control chain"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {"experiment": "h4_reproduction_return_guard_checklist", "environment": environment.as_dict(), "rows": rows},
    )
    snapshot_payload = {
        "experiment": "h4_reproduction_return_guard_snapshot",
        "environment": environment.as_dict(),
        "rows": snapshot,
    }
    write_json(OUT_DIR / "snapshot.json", snapshot_payload)
    write_json(OUT_DIR / "surface_snapshot.json", snapshot_payload)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h4_reproduction_return_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "tmp/2026-03-19-reproduction-mainline-return-master-plan.md",
                "docs/milestones/H4_reproduction_mainline_return/status.md",
                "docs/milestones/H4_reproduction_mainline_return/todo.md",
                "docs/milestones/H5_repro_sync_and_refreeze/artifact_index.md",
                "docs/publication_record/experiment_manifest.md",
                "docs/publication_record/current_stage_driver.md",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# H4 Reproduction Return Guard",
                "",
                "Machine-readable guard for whether the completed H4",
                "reproduction-mainline return packet remains preserved as a",
                "historical archive after later stage rollover.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `snapshot.json`",
                "- `surface_snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
