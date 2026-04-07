"""Export the post-H49 cleanline hygiene and artifact policy packet for P36."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P36_post_h49_cleanline_hygiene_and_artifact_policy"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def environment_payload() -> dict[str, object]:
    try:
        return detect_runtime_environment().as_dict()
    except Exception as exc:  # pragma: no cover
        return {"runtime_detection": "fallback", "error": f"{type(exc).__name__}: {exc}"}


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
        "p36_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "README.md"
        ),
        "p36_status_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "status.md"
        ),
        "p36_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "todo.md"
        ),
        "p36_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "acceptance.md"
        ),
        "p36_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "artifact_index.md"
        ),
        "worktree_strategy_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "worktree_strategy.md"
        ),
        "artifact_policy_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "artifact_policy.md"
        ),
        "commit_cadence_text": read_text(
            ROOT / "docs" / "milestones" / "P36_post_h49_cleanline_hygiene_and_artifact_policy" / "commit_cadence.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
        "p35_summary": read_json(ROOT / "results" / "P35_post_h47_research_record_rollup" / "summary.json"),
        "h49_summary": read_json(ROOT / "results" / "H49_post_r50_tinyc_lowering_decision_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    p27 = inputs["p27_summary"]["summary"]
    p35 = inputs["p35_summary"]["summary"]
    h49 = inputs["h49_summary"]["summary"]
    return [
        {
            "item_id": "p36_docs_define_post_h49_cleanline_hygiene_packet",
            "status": "pass"
            if contains_all(inputs["p36_readme_text"], ["completed operational/docs hygiene packet", "preserves `h49` as the current active docs-only packet", "`f26 -> r51 -> r52 -> h50`"])
            and contains_all(inputs["p36_status_text"], ["only scientific execution surface", "quarantines dirty root `main`", "`merge_executed = false`"])
            and contains_all(inputs["p36_todo_text"], ["record one clean worktree strategy", "record one artifact policy", "record one commit cadence"])
            and contains_all(inputs["p36_acceptance_text"], ["raw probe/per-read dumps stay out of git by default", "merge back to `main` does not occur during `f26/r51/r52/h50`", "future lfs use remains opt-in"])
            else "blocked",
            "notes": "P36 should save the cleanline execution and artifact policy without changing scientific stage.",
        },
        {
            "item_id": "p36_records_worktree_artifact_and_commit_policy",
            "status": "pass"
            if contains_all(inputs["worktree_strategy_text"], ["clean execution surface for this wave", "dirty root `main` is not a scientific execution surface", "`r51` and `r52` should execute from clean descendant worktrees"])
            and contains_all(inputs["artifact_policy_text"], ["raw per-read dumps", "out of git by default", "git lfs remains inactive by default"])
            and contains_all(inputs["commit_cadence_text"], ["commit `f26` planning surfaces separately", "commit `r51` runtime outputs separately from `r52` comparator/value outputs", "do not mix packet closeout, runtime execution, and merge-posture changes"])
            and contains_all(inputs["p36_artifact_index_text"], ["docs/milestones/p36_post_h49_cleanline_hygiene_and_artifact_policy/worktree_strategy.md", "results/p36_post_h49_cleanline_hygiene_and_artifact_policy/summary.json"])
            else "blocked",
            "notes": "P36 should codify worktree strategy, artifact slimming, and commit cadence explicitly.",
        },
        {
            "item_id": "shared_control_surfaces_make_p36_current_low_priority_wave",
            "status": "pass"
            if bool(p27["merge_executed"]) is False
            and str(p35["current_low_priority_wave"]) == "p35_post_h47_research_record_rollup"
            and str(h49["active_stage"]) == "h49_post_r50_tinyc_lowering_decision_packet"
            and contains_all(inputs["readme_text"], ["`p36_post_h49_cleanline_hygiene_and_artifact_policy` is now the current low-priority operational/docs wave", "`p35_post_h47_research_record_rollup` is now the preserved prior low-priority"])
            and contains_all(inputs["status_text"], ["`p36_post_h49_cleanline_hygiene_and_artifact_policy` is now the current low-priority operational/docs wave", "`p35_post_h47_research_record_rollup` is now the preserved prior low-priority"])
            and contains_all(inputs["publication_readme_text"], ["`p36` as the current low-priority operational/docs wave", "`p35` as the preserved prior low-priority wave"])
            and contains_all(inputs["plans_index_text"], ["2026-03-24-post-h49-origin-core-next-wave-design.md", "../milestones/p36_post_h49_cleanline_hygiene_and_artifact_policy/"])
            and contains_all(inputs["milestones_index_text"], ["p36_post_h49_cleanline_hygiene_and_artifact_policy/", "p35_post_h47_research_record_rollup/"])
            and contains_all(inputs["current_stage_driver_text"], ["the current low-priority operational/docs wave is:", "- `p36_post_h49_cleanline_hygiene_and_artifact_policy`"])
            and contains_all(inputs["active_wave_plan_text"], ["dirty root `main` remains quarantined", "`p36_post_h49_cleanline_hygiene_and_artifact_policy` is the current low-priority operational/docs wave"])
            and contains_all(inputs["experiment_manifest_text"], ["post-`h49` `f26/p36` next-wave planning and hygiene wave", "new `results/p36_post_h49_cleanline_hygiene_and_artifact_policy/summary.json`"])
            else "blocked",
            "notes": "Shared control surfaces should promote P36 into the current low-priority wave while preserving H49 as active stage.",
        },
    ]


def build_summary(inputs: dict[str, Any], checklist_rows: list[dict[str, object]]) -> dict[str, Any]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    pass_count = sum(1 for row in checklist_rows if row["status"] == "pass")
    return {
        "experiment": "p36_post_h49_cleanline_hygiene_and_artifact_policy",
        "environment": environment_payload(),
        "summary": {
            "current_active_stage": "h49_post_r50_tinyc_lowering_decision_packet",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "refresh_packet": "p36_post_h49_cleanline_hygiene_and_artifact_policy",
            "selected_outcome": "cleanline_hygiene_saved_without_scientific_widening",
            "current_low_priority_wave": "p36_post_h49_cleanline_hygiene_and_artifact_policy",
            "preserved_prior_low_priority_wave": "p35_post_h47_research_record_rollup",
            "current_post_h49_planning_bundle": "f26_post_h49_origin_claim_delta_and_next_question_bundle",
            "current_merge_posture": "explicit_merge_wave",
            "merge_executed": False,
            "root_dirty_main_quarantined": True,
            "large_artifact_default_policy": "raw_probe_rows_out_of_git",
            "snapshot_surface_count": 8,
            "check_count": len(checklist_rows),
            "pass_count": pass_count,
            "blocked_count": len(blocked_items),
            "blocked_items": blocked_items,
            "next_required_lane": "r51_origin_memory_control_surface_sufficiency_gate",
        },
    }


def build_claim_packet(summary_payload: dict[str, Any]) -> dict[str, Any]:
    distilled = summary_payload["summary"]
    keys = [
        "current_active_stage",
        "current_paper_grade_endpoint",
        "refresh_packet",
        "selected_outcome",
        "current_low_priority_wave",
        "preserved_prior_low_priority_wave",
        "current_post_h49_planning_bundle",
        "current_merge_posture",
        "merge_executed",
        "root_dirty_main_quarantined",
        "large_artifact_default_policy",
        "next_required_lane",
    ]
    return {
        "summary": {
            "supported_here": [
                "P36 codifies the post-H49 clean worktree as the only scientific execution surface for this wave.",
                "P36 promotes one new low-priority hygiene packet while preserving H49 as the active docs-only stage.",
                "P36 keeps raw probe-style artifacts out of git by default and keeps merge posture explicit.",
            ],
            "unsupported_here": [
                "P36 does not authorize a runtime lane.",
                "P36 does not merge the repo back to main.",
                "P36 does not widen useful-case or model claims.",
            ],
            "disconfirmed_here": [
                "The idea that dirty root main should keep serving as the live scientific execution surface for the post-H49 wave."
            ],
            "distilled_result": {key: distilled[key] for key in keys},
        }
    }


def build_snapshot(inputs: dict[str, Any]) -> dict[str, Any]:
    rows = [
        ("docs/milestones/P36_post_h49_cleanline_hygiene_and_artifact_policy/worktree_strategy.md", inputs["worktree_strategy_text"], ["clean execution surface for this wave", "dirty root `main` is not a scientific execution surface"]),
        ("docs/milestones/P36_post_h49_cleanline_hygiene_and_artifact_policy/artifact_policy.md", inputs["artifact_policy_text"], ["raw per-read dumps", "Git LFS remains inactive by default"]),
        ("docs/milestones/P36_post_h49_cleanline_hygiene_and_artifact_policy/commit_cadence.md", inputs["commit_cadence_text"], ["commit `F26` planning surfaces separately", "commit `H50` decision surfaces only after `R51/R52` are explicit"]),
        ("README.md", inputs["readme_text"], ["`P36_post_h49_cleanline_hygiene_and_artifact_policy` is now the current low-priority operational/docs wave"]),
        ("STATUS.md", inputs["status_text"], ["`P36_post_h49_cleanline_hygiene_and_artifact_policy` is now the current low-priority operational/docs wave"]),
        ("docs/publication_record/current_stage_driver.md", inputs["current_stage_driver_text"], ["The current low-priority operational/docs wave is:", "- `P36_post_h49_cleanline_hygiene_and_artifact_policy`"]),
        ("docs/publication_record/README.md", inputs["publication_readme_text"], ["`P36` as the current low-priority operational/docs wave"]),
        ("tmp/active_wave_plan.md", inputs["active_wave_plan_text"], ["dirty root `main` remains quarantined", "`P36_post_h49_cleanline_hygiene_and_artifact_policy` is the current low-priority operational/docs wave"]),
    ]
    return {"rows": [{"path": path, "matched_lines": extract_matching_lines(text, needles=needles)} for path, text, needles in rows]}


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    summary_payload = build_summary(inputs, checklist_rows)
    write_json(OUT_DIR / "summary.json", summary_payload)
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", build_claim_packet(summary_payload))
    write_json(OUT_DIR / "snapshot.json", build_snapshot(inputs))


if __name__ == "__main__":
    main()
