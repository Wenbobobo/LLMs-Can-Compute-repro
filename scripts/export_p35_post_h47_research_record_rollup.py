"""Export the post-H47 research-record rollup packet for P35."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P35_post_h47_research_record_rollup"


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
    except Exception as exc:  # pragma: no cover - defensive fallback
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
        "master_plan_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-h47-p35-f23-mainline-extension-master-plan.md"
        ),
        "design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-h47-p35-research-record-rollup-design.md"
        ),
        "p35_readme_text": read_text(ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "README.md"),
        "p35_status_text": read_text(ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "status.md"),
        "p35_todo_text": read_text(ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "todo.md"),
        "p35_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "acceptance.md"
        ),
        "p35_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "artifact_index.md"
        ),
        "artifact_inventory_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "artifact_inventory.md"
        ),
        "root_dirty_quarantine_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "root_dirty_quarantine.md"
        ),
        "push_state_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "push_state.md"
        ),
        "merge_posture_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "merge_posture.md"
        ),
        "negative_result_rollup_text": read_text(
            ROOT / "docs" / "milestones" / "P35_post_h47_research_record_rollup" / "negative_result_rollup.md"
        ),
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h47_summary": read_json(ROOT / "results" / "H47_post_r48_useful_case_bridge_refreeze" / "summary.json"),
        "p31_summary": read_json(ROOT / "results" / "P31_post_h43_blog_guardrails_refresh" / "summary.json"),
        "p27_summary": read_json(ROOT / "results" / "P27_post_h41_clean_promotion_and_explicit_merge_packet" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h47 = inputs["h47_summary"]["summary"]
    p31 = inputs["p31_summary"]["summary"]
    p27 = inputs["p27_summary"]["summary"]
    return [
        {
            "item_id": "p35_docs_define_post_h47_rollup_without_scientific_widening",
            "status": "pass"
            if contains_all(
                inputs["master_plan_text"],
                [
                    "wave 1: `p35_post_h47_research_record_rollup`",
                    "wave 2: `f23_post_h47_numeric_scaling_bundle`",
                    "raw artifacts above `10 mib` do not enter git by default",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`p35_post_h47_research_record_rollup`",
                    "`h47_post_r48_useful_case_bridge_refreeze`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`f23_post_h47_numeric_scaling_bundle`",
                ],
            )
            and contains_all(
                inputs["p35_readme_text"],
                [
                    "completed low-priority operational/docs rollup packet after the post-`h47` stack returned to `no_active_downstream_runtime_lane`",
                    "preserves `h47_post_r48_useful_case_bridge_refreeze` as the current docs-only packet",
                    "preserves `h43_post_r44_useful_case_refreeze` as the paper-grade endpoint",
                ],
            )
            and contains_all(
                inputs["p35_status_text"],
                [
                    "promotes `p35` to the current low-priority operational/docs wave",
                    "demotes `p31/p32/p33/p34` to preserved prior helper refresh packets",
                    "keeps scientific widening inactive here",
                ],
            )
            and contains_all(
                inputs["p35_todo_text"],
                [
                    "record one artifact inventory and one raw-artifact slimming rule",
                    "record one root-dirty quarantine note for root `main`",
                    "hand the next planning question to",
                    "`f23_post_h47_numeric_scaling_bundle`",
                ],
            )
            and contains_all(
                inputs["p35_acceptance_text"],
                [
                    "`p35` becomes the current low-priority operational/docs wave",
                    "`p31/p32/p33/p34` remain preserved prior helper refresh packets only",
                    "`next_required_lane = f23_post_h47_numeric_scaling_bundle`",
                ],
            )
            and contains_all(
                inputs["p35_artifact_index_text"],
                [
                    "docs/plans/2026-03-24-post-h47-p35-f23-mainline-extension-master-plan.md",
                    "docs/plans/2026-03-24-post-h47-p35-research-record-rollup-design.md",
                    "results/p35_post_h47_research_record_rollup/summary.json",
                ],
            )
            else "blocked",
            "notes": "P35 should stay docs-only, preserve H47/H43, and hand the next planning question to F23.",
        },
        {
            "item_id": "p35_hygiene_docs_record_artifact_policy_quarantine_push_and_merge_posture",
            "status": "pass"
            if contains_all(
                inputs["artifact_inventory_text"],
                [
                    "raw artifacts above `10 mib` do not enter git by default",
                    "`results/r20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json`",
                ],
            )
            and contains_all(
                inputs["root_dirty_quarantine_text"],
                [
                    "dirty root `main` is out of scope for the active scientific line",
                    "do not reset, revert, or “clean up” dirty root `main` by momentum",
                ],
            )
            and contains_all(
                inputs["push_state_text"],
                [
                    "`wip/r48-origin-dual-mode-useful-case-model`",
                    "`origin/wip/r48-origin-dual-mode-useful-case-model`",
                    "`wip/p35-f23-post-h47-mainline-extension`",
                ],
            )
            and contains_all(
                inputs["merge_posture_text"],
                [
                    "`promotion_mode = explicit_merge_wave`",
                    "`merge_executed = false`",
                    "no merge to `main` occurs during the `p35/f23/r49/h48` extension line",
                ],
            )
            and contains_all(
                inputs["negative_result_rollup_text"],
                [
                    "`h27` closes the old same-endpoint recovery line negatively",
                    "`r23` keeps the same-endpoint systems verdict mixed",
                    "`r36` sharpens a real finite-precision boundary",
                    "`h47` explicitly restores `no_active_downstream_runtime_lane`",
                ],
            )
            else "blocked",
            "notes": "P35 should record hygiene policy, pushed baseline state, explicit no-merge posture, and preserved negative-result accounting.",
        },
        {
            "item_id": "shared_control_surfaces_make_p35_current_low_priority_wave",
            "status": "pass"
            if str(h47["active_stage"]) == "h47_post_r48_useful_case_bridge_refreeze"
            and str(h47["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(p31["refresh_packet"]) == "p31_post_h43_blog_guardrails_refresh"
            and str(p27["promotion_mode"]) == "explicit_merge_wave"
            and bool(p27["merge_executed"]) is False
            and contains_all(
                inputs["readme_text"],
                [
                    "`p35` is now the current low-priority research-record rollup/docs wave",
                    "`p31/p32/p33/p34` remain preserved prior helper refresh packets",
                ],
            )
            and contains_all(
                inputs["status_text"],
                [
                    "`p35_post_h47_research_record_rollup` is now the current low-priority operational/docs wave",
                    "`p31/p32/p33/p34` remain preserved prior low-priority helper refresh packets",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/milestones/p35_post_h47_research_record_rollup/",
                    "results/p35_post_h47_research_record_rollup/summary.json",
                    "docs/milestones/p31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h47-p35-f23-mainline-extension-master-plan.md",
                    "2026-03-24-post-h47-p35-research-record-rollup-design.md",
                    "../milestones/p35_post_h47_research_record_rollup/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "p35_post_h47_research_record_rollup/` — current low-priority",
                    "p31_post_h43_blog_guardrails_refresh/` — completed prior",
                ],
            )
            and contains_all(
                inputs["current_stage_driver_text"],
                [
                    "`p35_post_h47_research_record_rollup` is now the current low-priority operational/docs wave",
                    "`p31_post_h43_blog_guardrails_refresh`,",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`p35_post_h47_research_record_rollup` is the current low-priority operational/docs wave",
                    "`p31/p32/p33/p34` remain preserved prior helper refresh packets",
                    "`wip/p35-f23-post-h47-mainline-extension` is the clean post-`h47` extension branch",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`h47` `p35` research-record rollup wave",
                    "scripts/export_p35_post_h47_research_record_rollup.py",
                    "results/p35_post_h47_research_record_rollup/summary.json",
                ],
            )
            else "blocked",
            "notes": "Shared control surfaces should keep H47 current while promoting P35 into the current low-priority operational/docs wave.",
        },
    ]


def build_claim_packet() -> dict[str, object]:
    return {
        "supported_here": [
            "P35 records the post-H47 research state without changing scientific stage.",
            "P35 promotes one new low-priority operational/docs wave while preserving H47 and H43.",
            "P35 codifies artifact slimming, root-dirty quarantine, push state, and explicit no-merge posture.",
        ],
        "unsupported_here": [
            "P35 does not authorize a runtime lane.",
            "P35 does not widen useful-case claims beyond H47/H43.",
            "P35 does not merge the repo back to main.",
        ],
        "disconfirmed_here": [
            "The idea that the repo should keep using dirty root main as the live scientific workspace.",
        ],
        "distilled_result": {
            "active_stage": "h47_post_r48_useful_case_bridge_refreeze",
            "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
            "current_low_priority_wave": "p35_post_h47_research_record_rollup",
            "preserved_prior_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
            "current_exact_first_planning_bundle": "f21_post_h43_exact_useful_case_expansion_bundle",
            "current_comparator_planning_bundle": "f22_post_r46_useful_case_model_bridge_bundle",
            "current_merge_posture": "explicit_merge_wave",
            "merge_executed": False,
            "root_dirty_main_quarantined": True,
            "large_artifact_default_policy": "raw_artifacts_over_10_mib_out_of_git",
            "next_required_lane": "f23_post_h47_numeric_scaling_bundle",
        },
    }


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h47-p35-f23-mainline-extension-master-plan.md": (
            "master_plan_text",
            ["wave 1: `p35_post_h47_research_record_rollup`", "wave 2: `f23_post_h47_numeric_scaling_bundle`"],
        ),
        "docs/plans/2026-03-24-post-h47-p35-research-record-rollup-design.md": (
            "design_text",
            ["`p35_post_h47_research_record_rollup`", "`h47_post_r48_useful_case_bridge_refreeze`"],
        ),
        "docs/milestones/P35_post_h47_research_record_rollup/README.md": (
            "p35_readme_text",
            ["completed low-priority operational/docs rollup packet", "`h47_post_r48_useful_case_bridge_refreeze`"],
        ),
        "docs/milestones/P35_post_h47_research_record_rollup/artifact_inventory.md": (
            "artifact_inventory_text",
            ["raw artifacts above `10 mib` do not enter git by default", "`results/r20_d0_runtime_mechanism_ablation_matrix/probe_read_rows.json`"],
        ),
        "docs/milestones/P35_post_h47_research_record_rollup/root_dirty_quarantine.md": (
            "root_dirty_quarantine_text",
            ["dirty root `main` is out of scope", "do not reset, revert, or “clean up” dirty root `main` by momentum"],
        ),
        "README.md": (
            "readme_text",
            ["`p35` is now the current low-priority research-record rollup/docs wave", "`p31/p32/p33/p34` remain preserved prior helper refresh packets"],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            ["`p35_post_h47_research_record_rollup` is now the current low-priority operational/docs wave", "`p31_post_h43_blog_guardrails_refresh`,"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`p35_post_h47_research_record_rollup` is the current low-priority operational/docs wave", "`wip/p35-f23-post-h47-mainline-extension` is the clean post-`h47` extension branch"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_active_stage": "h47_post_r48_useful_case_bridge_refreeze",
        "current_paper_grade_endpoint": "h43_post_r44_useful_case_refreeze",
        "refresh_packet": "p35_post_h47_research_record_rollup",
        "selected_outcome": "research_record_rollup_saved_without_scientific_widening",
        "current_low_priority_wave": "p35_post_h47_research_record_rollup",
        "preserved_prior_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "snapshot_surface_count": len(snapshot_rows),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "next_required_lane": "f23_post_h47_numeric_scaling_bundle",
    }


def main() -> None:
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    claim_packet = build_claim_packet()
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, snapshot_rows)

    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p35_post_h47_research_record_rollup",
            "environment": environment_payload(),
            "summary": summary,
        },
    )
    write_json(OUT_DIR / "checklist.json", {"rows": checklist_rows})
    write_json(OUT_DIR / "claim_packet.json", {"summary": claim_packet})
    write_json(OUT_DIR / "snapshot.json", {"rows": snapshot_rows})


if __name__ == "__main__":
    main()
