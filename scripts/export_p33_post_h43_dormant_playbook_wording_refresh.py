"""Export the post-H43 dormant playbook wording refresh packet for P33."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P33_post_h43_dormant_playbook_wording_refresh"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
        "p33_readme_text": read_text(
            ROOT / "docs" / "milestones" / "P33_post_h43_dormant_playbook_wording_refresh" / "README.md"
        ),
        "p33_status_text": read_text(
            ROOT / "docs" / "milestones" / "P33_post_h43_dormant_playbook_wording_refresh" / "status.md"
        ),
        "p33_todo_text": read_text(
            ROOT / "docs" / "milestones" / "P33_post_h43_dormant_playbook_wording_refresh" / "todo.md"
        ),
        "p33_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P33_post_h43_dormant_playbook_wording_refresh" / "acceptance.md"
        ),
        "p33_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P33_post_h43_dormant_playbook_wording_refresh" / "artifact_index.md"
        ),
        "design_text": read_text(
            ROOT / "docs" / "plans" / "2026-03-24-post-h43-p33-dormant-playbook-wording-refresh-design.md"
        ),
        "e1_matrix_text": read_text(ROOT / "docs" / "publication_record" / "e1_patch_playbook_matrix.md"),
        "e1b_text": read_text(ROOT / "docs" / "publication_record" / "e1b_systems_patch_playbook.md"),
        "e1c_text": read_text(ROOT / "docs" / "publication_record" / "e1c_compiled_boundary_patch_playbook.md"),
        "layout_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "p31_summary": read_json(ROOT / "results" / "P31_post_h43_blog_guardrails_refresh" / "summary.json"),
        "p32_summary": read_json(ROOT / "results" / "P32_post_h43_historical_wording_refresh" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    return [
        {
            "item_id": "p33_packet_docs_define_auxiliary_dormant_playbook_refresh",
            "status": "pass"
            if contains_all(
                inputs["p33_readme_text"],
                [
                    "completed auxiliary dormant playbook/historical-helper wording refresh packet",
                    "does not displace `P31` as the current low-priority wave",
                ],
            )
            and contains_all(
                inputs["p33_status_text"],
                [
                    "active scientific stage remains `H43_post_r44_useful_case_refreeze`",
                    "current operational wave remains `P31_post_h43_blog_guardrails_refresh`",
                    "`P33_post_h43_dormant_playbook_wording_refresh` is recorded as a completed auxiliary",
                ],
            )
            and contains_all(
                inputs["p33_todo_text"],
                [
                    "refresh `docs/publication_record/e1_patch_playbook_matrix.md`",
                    "refresh `docs/publication_record/e1b_systems_patch_playbook.md`",
                    "add a focused `P33` exporter plus tests/results",
                ],
            )
            and contains_all(
                inputs["p33_acceptance_text"],
                [
                    "`P31` remains the current low-priority",
                    "`P33` as a completed auxiliary packet",
                    "preserved same-endpoint systems gate",
                ],
            )
            and contains_all(
                inputs["p33_artifact_index_text"],
                [
                    "docs/publication_record/e1b_systems_patch_playbook.md",
                    "docs/publication_record/experiment_manifest.md",
                    "results/P33_post_h43_dormant_playbook_wording_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`P33_post_h43_dormant_playbook_wording_refresh`",
                    "`dormant_playbook_wording_surfaces_refreshed_to_h43`",
                    "Rejected: promote `P33` to the current low-priority wave",
                ],
            )
            else "blocked",
            "notes": "P33 should remain a narrow auxiliary dormant-playbook/helper wording packet and must not displace P31 or activate any dormant execution lane.",
        },
        {
            "item_id": "dormant_playbook_and_helper_surfaces_demote_preserved_r2_d0_from_current_endpoint_language",
            "status": "pass"
            if contains_all(
                inputs["e1_matrix_text"],
                [
                    "preserved same-endpoint scope",
                    "preserved first tiny typed-bytecode `D0` boundary only",
                ],
            )
            and contains_all(
                inputs["e1b_text"],
                [
                    "preserved same-endpoint scope",
                    "preserved positive `D0` suites from that earlier line",
                ],
            )
            and contains_all(
                inputs["e1c_text"],
                [
                    "preserved first compiled boundary from the old same-endpoint line",
                    "broader current `H43` paper endpoint",
                    "preserved first-step `D0` supported where proven",
                ],
            )
            and contains_all(
                inputs["layout_text"],
                [
                    "preserved-first-step `D0` compiled-boundary line",
                    "rather than treating that older `D0` evidence as the whole current endpoint",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "freezes the preserved first `D0` slice from the old same-endpoint line at the planning layer",
                    "preserved `M2` geometry benchmark and preserved positive `D0` bytecode/spec suites from that stage",
                    "do not widen the preserved first compiled `D0` boundary",
                    "`scripts/export_e1b_systems_patch.py` over the existing `R2` geometry/runtime bundle and preserved positive `D0` suites from that stage",
                    "`scripts/export_r4_mechanistic_retrieval_closure.py` over the preserved positive `D0` suites from that stage",
                ],
            )
            and contains_none(
                inputs["e1b_text"],
                [
                    "current frozen scope. The target is the mixed `R2` systems gate",
                    "present `D0` scope",
                    "current mixed systems gate",
                ],
            )
            and contains_none(
                inputs["e1c_text"],
                [
                    "current compiled boundary",
                    "current `D0` boundary",
                ],
            )
            and contains_none(
                inputs["experiment_manifest_text"],
                [
                    "do not widen the current compiled endpoint",
                    "with current `M2` geometry benchmark and current positive `D0` bytecode/spec suites",
                    "over the existing `R2` geometry/runtime bundle and current positive `D0` suites",
                    "over the current positive `D0` suites with source-event bridge rows",
                ],
            )
            else "blocked",
            "notes": "Dormant playbooks and helper rows should treat R2/D0 as preserved same-endpoint support inside the broader current H43 paper endpoint, not as the whole current endpoint.",
        },
        {
            "item_id": "indexes_and_handoff_preserve_p31_current_and_record_p33_auxiliary_completion",
            "status": "pass"
            if contains_all(
                inputs["status_text"],
                [
                    "guardrail refresh wave `P31`",
                    "`P32`",
                    "`P33`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/plans/2026-03-24-post-h43-p33-dormant-playbook-wording-refresh-design.md",
                    "docs/milestones/P33_post_h43_dormant_playbook_wording_refresh/",
                    "results/P33_post_h43_dormant_playbook_wording_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h43-p33-dormant-playbook-wording-refresh-design.md",
                    "../milestones/P33_post_h43_dormant_playbook_wording_refresh/",
                    "../milestones/P31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "P33_post_h43_dormant_playbook_wording_refresh/",
                    "P31_post_h43_blog_guardrails_refresh/",
                    "P32_post_h43_historical_wording_refresh/",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`P31_post_h43_blog_guardrails_refresh` is the current low-priority",
                    "`P33_post_h43_dormant_playbook_wording_refresh` is the completed auxiliary",
                    "wip/p33-h43-dormant-playbook-wording-refresh",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`H43` `P33` dormant-playbook wording refresh wave",
                    "scripts/export_p33_post_h43_dormant_playbook_wording_refresh.py",
                    "results/P33_post_h43_dormant_playbook_wording_refresh/summary.json",
                ],
            )
            else "blocked",
            "notes": "Status, index, and handoff surfaces should keep P31 current while recording P33 as a completed auxiliary dormant-playbook wording packet.",
        },
        {
            "item_id": "upstream_h43_p31_and_p32_packets_remain_preserved",
            "status": "pass"
            if str(inputs["h43_summary"]["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(inputs["h43_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p31_summary"]["summary"]["selected_outcome"]) == "blocked_blog_guardrails_refreshed_to_h43"
            and str(inputs["p31_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and (
                str(inputs["p32_summary"]["summary"]["selected_outcome"])
                == "historical_wording_regeneration_surfaces_refreshed_to_h43"
            )
            else "blocked",
            "notes": "P33 should stay strictly downstream of the landed H43, P31, and P32 packets while preserving their selected outcomes.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h43-p33-dormant-playbook-wording-refresh-design.md": (
            "design_text",
            ["`P33_post_h43_dormant_playbook_wording_refresh`", "`dormant_playbook_wording_surfaces_refreshed_to_h43`"],
        ),
        "docs/publication_record/e1_patch_playbook_matrix.md": (
            "e1_matrix_text",
            ["preserved same-endpoint scope", "preserved first tiny typed-bytecode `D0` boundary only"],
        ),
        "docs/publication_record/e1b_systems_patch_playbook.md": (
            "e1b_text",
            ["preserved same-endpoint scope", "preserved positive `D0` suites from that earlier line"],
        ),
        "docs/publication_record/e1c_compiled_boundary_patch_playbook.md": (
            "e1c_text",
            ["preserved first compiled boundary from the old same-endpoint line", "broader current `H43` paper endpoint"],
        ),
        "docs/publication_record/layout_decision_log.md": (
            "layout_text",
            ["preserved-first-step `D0` compiled-boundary line", "whole current endpoint"],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            ["post-`H43` `P33` dormant-playbook wording refresh wave", "preserved first `D0` slice from the old same-endpoint line"],
        ),
        "STATUS.md": (
            "status_text",
            ["guardrail refresh wave `P31`", "`P33`"],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            ["docs/milestones/P33_post_h43_dormant_playbook_wording_refresh/", "results/P33_post_h43_dormant_playbook_wording_refresh/summary.json"],
        ),
        "docs/plans/README.md": (
            "plans_index_text",
            ["2026-03-24-post-h43-p33-dormant-playbook-wording-refresh-design.md", "../milestones/P33_post_h43_dormant_playbook_wording_refresh/"],
        ),
        "docs/milestones/README.md": (
            "milestones_index_text",
            ["P33_post_h43_dormant_playbook_wording_refresh/", "P32_post_h43_historical_wording_refresh/"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`P31_post_h43_blog_guardrails_refresh` is the current low-priority", "`P33_post_h43_dormant_playbook_wording_refresh` is the completed auxiliary"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], snapshot_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h43_post_r44_useful_case_refreeze_active",
        "current_low_priority_wave": "p31_post_h43_blog_guardrails_refresh",
        "refresh_packet": "p33_post_h43_dormant_playbook_wording_refresh",
        "refresh_scope": "dormant_playbook_and_historical_helper_wording_surfaces",
        "selected_outcome": "dormant_playbook_wording_surfaces_refreshed_to_h43",
        "refreshed_surface_count": len(snapshot_rows),
        "next_required_lane": "no_active_downstream_runtime_lane",
        "check_count": len(checklist_rows),
        "pass_count": sum(1 for row in checklist_rows if row["status"] == "pass"),
        "blocked_count": len(blocked_items),
        "blocked_items": blocked_items,
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(inputs)
    snapshot_rows = build_snapshot(inputs)
    summary = build_summary(checklist_rows, snapshot_rows)

    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "p33_post_h43_dormant_playbook_wording_refresh",
            "environment": environment.as_dict(),
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p33_post_h43_dormant_playbook_wording_refresh",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p33_post_h43_dormant_playbook_wording_refresh",
            "environment": environment.as_dict(),
            "rows": snapshot_rows,
        },
    )


if __name__ == "__main__":
    main()
