"""Export the H4 reproduction-mainline return stage-alignment guard."""

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
            "item_id": "master_plan_saved_before_execution",
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
            "notes": "The saved plan should make the return-stage packet explicit before wider edits.",
        },
        {
            "item_id": "current_stage_driver_names_return_packet",
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
                    "`e1c` remains conditional only",
                    "completed baseline",
                ],
            )
            else "blocked",
            "notes": "The canonical active driver should expose the bounded return packet and conditional E1c rule.",
        },
        {
            "item_id": "top_level_docs_align_to_return_stage",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "the active stage is a bounded scientific return",
                    "`h4` resets the driver to reproduction",
                    "`e1a` sharpens the bounded precision story",
                    "`e1b` adds same-scope systems attribution",
                    "`e1c` stays conditional only",
                    "`h5` refreezes through the standing audits",
                ],
            )
            and contains_all(
                status_text,
                [
                    "current active post-`p9` operational stage is a bounded reproduction-mainline return",
                    "`h4`, `e1a`, `e1b`, and `h5`",
                    "`e1c` remains conditional only",
                    "logical lane order stays `e1a` then `e1b`",
                    "frontend widening remains blocked",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should expose the same scientific-return packet.",
        },
        {
            "item_id": "publication_index_and_release_summary_align",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "current_stage_driver.md",
                    "planning_state_taxonomy.md",
                    "current bounded reproduction-return packet",
                    "`h3` / `p10` / `p11` / `f1`",
                    "completed baseline",
                    "conditional_reopen_protocol.md",
                ],
            )
            and contains_all(
                release_summary_text,
                [
                    "the active post-`p9` follow-up is a bounded reproduction-mainline return",
                    "`h4` resets the active driver to the scientific mainline",
                    "`e1a` sharpens bounded precision on current families",
                    "`e1b` adds same-scope systems attribution",
                    "`e1c` remains conditional only",
                    "`h5` refreezes through the standing audits",
                ],
            )
            else "blocked",
            "notes": "Publication-facing short docs should reflect the same active stage.",
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
        "README.md": (
            "readme_text",
            ["The active stage is a bounded scientific return", "`H4` resets the driver to reproduction"],
        ),
        "STATUS.md": (
            "status_text",
            ["bounded reproduction-mainline return", "`H4`, `E1a`, `E1b`, and `H5`"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`H4_reproduction_mainline_return`",
                "`E1a_precision_patch`",
                "`E1b_systems_patch`",
                "completed baseline",
            ],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            ["bounded reproduction-mainline return", "`E1c` remains conditional only"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h4_reproduction_mainline_return_active",
        "active_stage": "h4_reproduction_mainline_return",
        "lane_order": "e1a_then_e1b_then_optional_e1c_then_h5",
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "execute bounded E1a/E1b evidence lanes, keep E1c conditional-only, and refreeze through H5"
            if not blocked_items
            else "resolve the blocked H4 stage-alignment items before continuing bounded evidence work"
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
                "# H4 Reproduction Return Guard",
                "",
                "Machine-readable guard for whether the repo control docs are aligned to the",
                "bounded reproduction-mainline return stage.",
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
