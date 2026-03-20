"""Export the H11 post-H9 mainline rollover guard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H11_post_h9_mainline_rollover_guard"


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
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "release_preflight_summary_text": read_text(
            ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
        ),
        "release_preflight_summary": read_json(
            ROOT / "results" / "release_preflight_checklist_audit" / "summary.json"
        ),
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
    release_preflight_summary_text: str,
    release_preflight_summary: dict[str, Any],
    m7_decision_text: str,
) -> list[dict[str, object]]:
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
                    "`r9_d0_real_trace_precision_boundary_companion`",
                    "`r10_d0_same_endpoint_cost_attribution`",
                    "`h12_refreeze_and_record_sync`",
                ],
            )
            else "blocked",
            "notes": "The saved plan should make the H10/H11/R8/R9/R10/H12 packet explicit before implementation closes.",
        },
        {
            "item_id": "current_stage_driver_names_retrieval_pressure_packet",
            "status": "pass"
            if contains_all(
                current_stage_driver_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`h13_post_h12_rollover_and_next_stage_staging` remains preserved",
                    "`v1_full_suite_validation_runtime_audit` remains a standing operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint follow-up packet",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline underneath",
                    "`h6/r3/r4/(inactive r5)/h7` remains the deeper historical baseline",
                ],
            )
            else "blocked",
            "notes": "The canonical driver should expose current H15, preserve H14/H13/V1 state, preserve the completed H12 checkpoint, and preserve both older baselines.",
        },
        {
            "item_id": "top_level_docs_align_to_retrieval_pressure_packet",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "`h10-h12` | completed bounded `d0` retrieval-pressure packet",
                    "| `h13-v1` | completed governance/runtime handoff preserved as a control baseline",
                    "| `h14-h15` | completed bounded core-first reopen/refreeze packet",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "v1 remains a standing operational reference under the preserved `h13`",
                    "`h8/r6/r7/h9` now sits as the completed direct same-endpoint baseline",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`v1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`healthy_but_slow`",
                    "the completed reopen wave ran through",
                    "`h8/r6/r7/h9` remains the completed direct same-endpoint baseline",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should expose the same completed H12 checkpoint plus current H15 and preserved H14/H13/V1 state.",
        },
        {
            "item_id": "publication_index_and_release_summary_align",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "current_stage_driver.md",
                    "`h15` refreeze-and-decision-sync",
                    "`h14` / `r11` / `r12` remain the completed reopen packet",
                    "`h13` / `v1` remain the completed governance/runtime handoff",
                    "`h10` / `h11` / `r8` / `r9` / `r10` / `h12` remain the latest completed",
                    "`h8` / `r6` / `r7` / `h9` remain the completed bounded long-horizon direct baseline",
                ],
            )
            and contains_all(
                release_summary_text,
                [
                    "`h10/h11/r8/r9/r10/h12` is now the latest completed same-endpoint follow-up packet",
                    "`h13/v1` is now the preserved governance/runtime handoff",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "`e1c` remains conditional only",
                ],
            )
            else "blocked",
            "notes": "Publication-facing short docs should reflect the same preserved H12 checkpoint, preserved H14/H13/V1 state, and current H15 stage.",
        },
        {
            "item_id": "release_preflight_audit_is_green",
            "status": "pass"
            if release_preflight_summary["summary"]["preflight_state"] == "docs_and_audits_green"
            and int(release_preflight_summary["summary"]["blocked_count"]) == 0
            and str(release_preflight_summary["summary"]["release_commit_state"])
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and contains_all(
                release_preflight_summary_text,
                [
                    "\"preflight_scope\": \"outward_release_surface_and_frozen_paper_bundle\"",
                    "\"release_commit_state\":",
                    "release_worktree_hygiene_snapshot",
                ],
            )
            else "blocked",
            "notes": "The active post-H12 stage should keep outward sync routed through the release-preflight audit rather than prose-only checks.",
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
            "notes": "The new packet must not weaken the prior no-widening decision.",
        },
    ]


def build_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    lookup = {
        "tmp/2026-03-20-post-h9-d0-retrieval-pressure-plan.md": (
            "master_plan_text",
            ["Post-H9 D0 Retrieval-Pressure Plan", "`H10_r7_reconciliation_and_refreeze`", "`R8_d0_retrieval_pressure_gate`"],
        ),
        "README.md": (
            "readme_text",
            [
                "`H10-H12` | completed bounded `D0` retrieval-pressure packet",
                "| `H13-V1` | completed governance/runtime handoff preserved as a control baseline",
                "| `H14-H15` | completed bounded core-first reopen/refreeze packet",
                "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`V1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint",
                "`healthy_but_slow`",
            ],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`H13_post_h12_rollover_and_next_stage_staging` remains preserved",
                "`V1_full_suite_validation_runtime_audit` remains a standing operational reference",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint follow-up packet",
            ],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            [
                "`H10/H11/R8/R9/R10/H12` is now the latest completed same-endpoint follow-up packet",
                "`H13/V1` is now the preserved governance/runtime handoff",
                "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`",
                "`E1c` remains conditional only",
            ],
        ),
        "results/release_preflight_checklist_audit/summary.json": (
            "release_preflight_summary_text",
            [
                "\"preflight_scope\": \"outward_release_surface_and_frozen_paper_bundle\"",
                "\"preflight_state\": \"docs_and_audits_green\"",
                "outward-sync control reference",
            ],
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
        "active_stage": "h15_refreeze_and_decision_sync",
        "lane_order": "preserve_h12_then_preserve_h14_then_hold_refrozen_until_next_full_plan",
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "keep H10/H11/R8/R9/R10/H12 aligned as the latest completed checkpoint while H15 remains the current refrozen stage, preserve H14/R11/R12 as the completed reopen packet, preserve H13/V1 as handoff state, and use release_preflight_checklist_audit plus release_worktree_hygiene_snapshot as the outward-sync control reference"
            if not blocked_items
            else "resolve the blocked H11 stage-alignment items before treating the post-H12 rollover as canonical"
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
        {"experiment": "h11_post_h9_mainline_rollover_guard_checklist", "environment": environment.as_dict(), "rows": rows},
    )
    snapshot_payload = {
        "experiment": "h11_post_h9_mainline_rollover_guard_snapshot",
        "environment": environment.as_dict(),
        "rows": snapshot,
    }
    write_json(OUT_DIR / "snapshot.json", snapshot_payload)
    write_json(OUT_DIR / "surface_snapshot.json", snapshot_payload)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h11_post_h9_mainline_rollover_guard",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "tmp/2026-03-20-post-h9-d0-retrieval-pressure-plan.md",
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "results/release_preflight_checklist_audit/summary.json",
                "results/M7_frontend_candidate_decision/decision_summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# H11 Post-H9 Mainline Rollover Guard",
                "",
                "Machine-readable guard for whether the repo control docs are aligned to the",
                "bounded `H10/H11/R8/R9/R10/H12` packet while preserving",
                "`H8/R6/R7/H9` and `H6/R3/R4/(inactive R5)/H7` as completed baselines.",
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
