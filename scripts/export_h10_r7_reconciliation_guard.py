"""Export the H10 R7 reconciliation guard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H10_r7_reconciliation_guard"


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
        "master_plan_text": read_text(ROOT / "tmp" / "2026-03-20-post-h9-d0-retrieval-pressure-plan.md"),
        "r7_summary": read_json(ROOT / "results" / "R7_d0_same_endpoint_runtime_bridge" / "summary.json"),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "claim_ladder_text": read_text(ROOT / "docs" / "publication_record" / "claim_ladder.md"),
        "negative_results_text": read_text(ROOT / "docs" / "publication_record" / "negative_results.md"),
        "r7_status_text": read_text(ROOT / "docs" / "milestones" / "R7_d0_same_endpoint_runtime_bridge" / "status.md"),
        "r7_digest_text": read_text(
            ROOT / "docs" / "milestones" / "R7_d0_same_endpoint_runtime_bridge" / "result_digest.md"
        ),
        "h9_digest_text": read_text(
            ROOT / "docs" / "milestones" / "H9_refreeze_and_record_sync" / "result_digest.md"
        ),
    }


def build_checklist_rows(
    *,
    master_plan_text: str,
    r7_summary: dict[str, Any],
    readme_text: str,
    status_text: str,
    current_stage_driver_text: str,
    release_summary_text: str,
    claim_ladder_text: str,
    negative_results_text: str,
    r7_status_text: str,
    r7_digest_text: str,
    h9_digest_text: str,
) -> list[dict[str, object]]:
    overall = r7_summary["summary"]["overall"]
    return [
        {
            "item_id": "master_plan_saved_before_execution",
            "status": "pass"
            if contains_all(
                master_plan_text,
                [
                    "post-h9 d0 retrieval-pressure plan",
                    "`h10_r7_reconciliation_and_refreeze`",
                    "`h11_post_h9_mainline_rollover`",
                    "`r8_d0_retrieval_pressure_gate`",
                ],
            )
            else "blocked",
            "notes": "The saved plan should make the reconciliation packet explicit before implementation closes.",
        },
        {
            "item_id": "r7_artifact_reports_bounded_top4_profile",
            "status": "pass"
            if int(overall["exact_admitted_family_count"]) == 8
            and int(overall["profiled_row_count"]) == 4
            and int(overall["profiled_family_count"]) == 4
            and overall["profile_selection_rule"] == "top_4_exact_admitted_families_by_bytecode_step_count"
            else "blocked",
            "notes": "The on-disk R7 artifact is the authority and must remain a bounded top-4 profile.",
        },
        {
            "item_id": "top_level_docs_match_reconciled_r7_wording",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "profiled the top `4` heaviest family representatives",
                    "`0.973x`",
                    "`1980.3x`",
                    "`h8/r6/r7/h9` now sits as the completed direct same-endpoint baseline",
                ],
            )
            and contains_all(
                status_text,
                [
                    "profiled only the top `4` heaviest family representatives",
                    "`0.973x`",
                    "`1980.3x`",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should restate the reconciled R7 stop result precisely.",
        },
        {
            "item_id": "publication_ledgers_match_reconciled_r7_wording",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint follow-up packet",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline",
                ],
            )
            and contains_all(
                release_summary_text,
                [
                    "profiles only the top `4` heaviest representatives",
                    "`0.973x`",
                    "`1980.3x`",
                ],
            )
            and contains_all(
                claim_ladder_text,
                [
                    "profiles only the top `4` heaviest representatives",
                    "`h10/h11/r8/r9/r10/h12`",
                ],
            )
            and contains_all(
                negative_results_text,
                [
                    "profiles the top `4` heaviest representatives",
                    "`0.973x`",
                    "`1980.3x`",
                ],
            )
            else "blocked",
            "notes": "Current driver and publication ledgers should all match the same R7 stop wording.",
        },
        {
            "item_id": "milestone_digests_match_reconciled_r7_wording",
            "status": "pass"
            if contains_all(
                r7_status_text,
                [
                    "top `4` heaviest family representatives",
                    "all `4/4` profiled rows stayed exact",
                    "`0.973x`",
                    "`1980.3x`",
                ],
            )
            and contains_all(
                r7_digest_text,
                [
                    "top `4` heaviest family representatives",
                    "`0.973x`",
                    "`1980.3x`",
                ],
            )
            and contains_all(h9_digest_text, ["bounded top-`4`-profile `r7` stop result"])
            else "blocked",
            "notes": "R7 and H9 milestone docs should agree on the reconciled stop result.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": ("readme_text", ["top `4` heaviest family representatives", "`0.973x`", "`1980.3x`"]),
        "STATUS.md": ("status_text", ["top `4` heaviest family representatives", "`0.973x`", "`1980.3x`"]),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["top-`4` profile result", "`0.973x`", "`1980.3x`"],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            ["top `4` heaviest representatives", "`0.973x`", "`1980.3x`"],
        ),
        "docs/milestones/R7_d0_same_endpoint_runtime_bridge/status.md": (
            "r7_status_text",
            ["top `4` heaviest family representatives", "all `4/4` profiled rows", "`0.973x`", "`1980.3x`"],
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
        "reconciled_stage": "h10_r7_reconciliation_and_refreeze",
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "treat H8/R6/R7/H9 as the completed direct baseline and keep all future R7 wording on the bounded top-4-profile evidence while H15 preserves H14/R11/R12 as the completed reopen packet, H10/H11/R8/R9/R10/H12 as the latest completed checkpoint, and H13/V1 as preserved handoff state"
            if not blocked_items
            else "resolve the blocked R7 reconciliation items before relying on the next packet"
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
        {"experiment": "h10_r7_reconciliation_guard_checklist", "environment": environment.as_dict(), "rows": rows},
    )
    snapshot_payload = {
        "experiment": "h10_r7_reconciliation_guard_snapshot",
        "environment": environment.as_dict(),
        "rows": snapshot,
    }
    write_json(OUT_DIR / "snapshot.json", snapshot_payload)
    write_json(OUT_DIR / "surface_snapshot.json", snapshot_payload)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h10_r7_reconciliation_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "tmp/2026-03-20-post-h9-d0-retrieval-pressure-plan.md",
                "results/R7_d0_same_endpoint_runtime_bridge/summary.json",
                "README.md",
                "STATUS.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/claim_ladder.md",
                "docs/publication_record/negative_results.md",
                "docs/milestones/R7_d0_same_endpoint_runtime_bridge/status.md",
                "docs/milestones/R7_d0_same_endpoint_runtime_bridge/result_digest.md",
                "docs/milestones/H9_refreeze_and_record_sync/result_digest.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# H10 R7 Reconciliation Guard",
                "",
                "Machine-readable guard for whether the completed `R7` stop result",
                "is restated everywhere as the artifact-backed bounded top-4 profile.",
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
