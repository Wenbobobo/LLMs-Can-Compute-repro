"""Export the H6 deeper-baseline preservation guard after H11 rollover."""

from __future__ import annotations

import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H6_mainline_rollover_guard"


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
        "master_plan_text": read_text(ROOT / "tmp" / "2026-03-19-d0-mainline-r3-r5-master-plan.md"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "m7_decision_text": read_text(ROOT / "results" / "M7_frontend_candidate_decision" / "decision_summary.json"),
    }


def build_checklist_rows(
    *,
    master_plan_text: str,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    release_summary_text: str,
    m7_decision_text: str,
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "historical_h6_plan_is_preserved",
            "status": "pass"
            if contains_all(
                master_plan_text,
                [
                    "d0 mainline r3-r5 master plan",
                    "`h6_mainline_rollover_and_backlog_sync`",
                    "`r3_d0_exact_execution_stress_gate`",
                    "`r4_mechanistic_retrieval_closure`",
                    "`h7_refreeze_and_record_sync`",
                ],
            )
            else "blocked",
            "notes": "The historical H6 packet plan should remain preserved under tmp/ for archiveability.",
        },
        {
            "item_id": "current_stage_driver_preserves_h6_packet_as_deeper_baseline",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`h6/r3/r4/(inactive r5)/h7` remains the deeper historical baseline",
                    "`docs/milestones/h6_mainline_rollover_and_backlog_sync/result_digest.md`",
                    "`docs/milestones/r3_d0_exact_execution_stress_gate/result_digest.md`",
                ],
            )
            else "blocked",
            "notes": "The current driver should preserve H6/R3/R4/(inactive R5)/H7 as the deeper baseline.",
        },
        {
            "item_id": "top_level_docs_keep_h6_packet_visible_as_deeper_baseline",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "| `h6-h7` | bounded exactness/mechanism packet completed and preserved as the deeper baseline",
                    "`h6/r3/r4/(inactive r5)/h7` remains the older exactness/mechanism baseline",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h6/r3/r4/(inactive r5)/h7` remains the completed bounded exactness /",
                    "mechanism baseline underneath the current same-endpoint packets",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should preserve H6 as the deeper baseline after H11 rollover.",
        },
        {
            "item_id": "publication_short_docs_preserve_h6_baseline",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "`h6` / `r3` / `r4` / inactive `r5` / `h7` remain the completed bounded",
                    "exactness/mechanism baseline underneath the current packet",
                ],
            )
            and contains_all(
                release_summary_text,
                [
                    "the older `h6/r3/r4/(inactive r5)/h7` packet remains the deeper",
                    "exactness/mechanism baseline on the same endpoint",
                ],
            )
            else "blocked",
            "notes": "Publication-facing docs should keep the H6 packet visible as the deeper baseline.",
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
            "notes": "Preserving the H6 baseline must not weaken the prior no-widening decision.",
        },
    ]


def build_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    lookup = {
        "tmp/2026-03-19-d0-mainline-r3-r5-master-plan.md": (
            "master_plan_text",
            ["D0 Mainline R3-R5 Master Plan", "`H6_mainline_rollover_and_backlog_sync`"],
        ),
        "README.md": (
            "readme_text",
            ["| `H6-H7` |", "deeper baseline", "`H6/R3/R4/(inactive R5)/H7` remains the older"],
        ),
        "STATUS.md": (
            "status_text",
            ["`H6/R3/R4/(inactive R5)/H7` remains the completed bounded exactness /", "same-endpoint packets"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["`H10_r7_reconciliation_and_refreeze`", "`H6/R3/R4/(inactive R5)/H7` remains the deeper historical baseline"],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            ["older `H6/R3/R4/(inactive R5)/H7` packet remains the deeper", "baseline on the same endpoint"],
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
        "preserved_baseline_stage": "h6_mainline_rollover_and_backlog_sync",
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "preserve the completed H6/R3/R4/(inactive R5)/H7 packet as the deeper baseline while H15 keeps H14/R11/R12 preserved as the completed reopen packet, H10/H11/R8/R9/R10/H12 as the latest completed checkpoint on the same fixed D0 scope, and H13/V1 as preserved handoff state"
            if not blocked_items
            else "restore the missing H6 baseline references before relying on the new packet state"
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
        {"experiment": "h6_deeper_baseline_preservation_guard_checklist", "environment": environment.as_dict(), "rows": rows},
    )
    snapshot_payload = {
        "experiment": "h6_deeper_baseline_preservation_guard_snapshot",
        "environment": environment.as_dict(),
        "rows": snapshot,
    }
    write_json(OUT_DIR / "snapshot.json", snapshot_payload)
    write_json(OUT_DIR / "surface_snapshot.json", snapshot_payload)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h6_mainline_rollover_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "tmp/2026-03-19-d0-mainline-r3-r5-master-plan.md",
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# H6 Deeper Baseline Preservation Guard",
                "",
                "Machine-readable guard for whether the completed",
                "`H6/R3/R4/(inactive R5)/H7` packet remains visible as the deeper",
                "baseline after the H11 rollover.",
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
