"""Export the post-H43 historical/regeneration wording refresh packet for P32."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P32_post_h43_historical_wording_refresh"


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


def get_claim_reason(payload: dict[str, Any], claim_id: str) -> str:
    for row in payload.get("rows", []):
        if row.get("claim_id") == claim_id:
            return str(row.get("reason", ""))
    raise KeyError(claim_id)


def get_h0_note(payload: dict[str, Any], check_id: str) -> str:
    for row in payload.get("rows", []):
        if row.get("check_id") == check_id:
            return str(row.get("notes", ""))
    raise KeyError(check_id)


def load_inputs() -> dict[str, Any]:
    h0_public_surface_audit = read_json(
        ROOT / "results" / "H0_repo_consolidation_and_release_hygiene" / "public_surface_audit.json"
    )
    p3_unsupported_claims = read_json(
        ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "unsupported_claims.json"
    )
    return {
        "p32_readme_text": read_text(ROOT / "docs" / "milestones" / "P32_post_h43_historical_wording_refresh" / "README.md"),
        "p32_status_text": read_text(ROOT / "docs" / "milestones" / "P32_post_h43_historical_wording_refresh" / "status.md"),
        "p32_todo_text": read_text(ROOT / "docs" / "milestones" / "P32_post_h43_historical_wording_refresh" / "todo.md"),
        "p32_acceptance_text": read_text(
            ROOT / "docs" / "milestones" / "P32_post_h43_historical_wording_refresh" / "acceptance.md"
        ),
        "p32_artifact_index_text": read_text(
            ROOT / "docs" / "milestones" / "P32_post_h43_historical_wording_refresh" / "artifact_index.md"
        ),
        "design_text": read_text(ROOT / "docs" / "plans" / "2026-03-24-post-h43-p32-historical-wording-refresh-design.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "plans_index_text": read_text(ROOT / "docs" / "plans" / "README.md"),
        "milestones_index_text": read_text(ROOT / "docs" / "milestones" / "README.md"),
        "active_wave_plan_text": read_text(ROOT / "tmp" / "active_wave_plan.md"),
        "experiment_manifest_text": read_text(ROOT / "docs" / "publication_record" / "experiment_manifest.md"),
        "h0_public_surface_audit": h0_public_surface_audit,
        "h0_public_surface_audit_text": read_text(
            ROOT / "results" / "H0_repo_consolidation_and_release_hygiene" / "public_surface_audit.json"
        ),
        "p3_unsupported_claims": p3_unsupported_claims,
        "p3_unsupported_claims_text": read_text(
            ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "unsupported_claims.json"
        ),
        "p3_artifact_map_text": read_text(
            ROOT / "results" / "P3_paper_freeze_and_evidence_mapping" / "artifact_map.json"
        ),
        "h43_summary": read_json(ROOT / "results" / "H43_post_r44_useful_case_refreeze" / "summary.json"),
        "p31_summary": read_json(ROOT / "results" / "P31_post_h43_blog_guardrails_refresh" / "summary.json"),
    }


def build_checklist_rows(inputs: dict[str, Any]) -> list[dict[str, object]]:
    h0_note = get_h0_note(inputs["h0_public_surface_audit"], "m7_no_widening_recorded")
    p3_arbitrary_c_reason = get_claim_reason(inputs["p3_unsupported_claims"], "unsupported_arbitrary_c")
    old_h0_phrase = "The current compiled endpoint remains D0."
    old_p3_phrase = (
        "The current compiled boundary is intentionally fixed to a tiny typed bytecode "
        "and should not be inflated into arbitrary-C coverage."
    )
    return [
        {
            "item_id": "p32_packet_docs_define_auxiliary_historical_regeneration_refresh",
            "status": "pass"
            if contains_all(
                inputs["p32_readme_text"],
                [
                    "completed auxiliary historical/regeneration wording refresh packet",
                    "does not displace `P31` as the current low-priority wave",
                ],
            )
            and contains_all(
                inputs["p32_status_text"],
                [
                    "active scientific stage remains `H43_post_r44_useful_case_refreeze`",
                    "current operational wave remains `P31_post_h43_blog_guardrails_refresh`",
                    "`P32_post_h43_historical_wording_refresh` is recorded as a completed auxiliary follow-on",
                ],
            )
            and contains_all(
                inputs["p32_todo_text"],
                [
                    "refresh `export_h0_release_hygiene.py`",
                    "refresh `export_p3_paper_freeze.py`",
                    "add a focused `P32` exporter plus tests/results",
                ],
            )
            and contains_all(
                inputs["p32_acceptance_text"],
                [
                    "`P31` remains the current low-priority",
                    "`P32` as a completed auxiliary packet",
                    "current `H43` paper endpoint",
                ],
            )
            and contains_all(
                inputs["p32_artifact_index_text"],
                [
                    "results/H0_repo_consolidation_and_release_hygiene/public_surface_audit.json",
                    "results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json",
                    "results/P32_post_h43_historical_wording_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["design_text"],
                [
                    "`P32_post_h43_historical_wording_refresh`",
                    "`historical_wording_regeneration_surfaces_refreshed_to_h43`",
                    "Rejected: promote `P32` to the current low-priority wave",
                ],
            )
            else "blocked",
            "notes": "P32 should remain a narrow auxiliary docs/regeneration packet and must not displace P31 or reopen any runtime lane.",
        },
        {
            "item_id": "h0_and_p3_machine_readable_surfaces_demote_d0_from_current_endpoint_language",
            "status": "pass"
            if contains_all(
                h0_note,
                [
                    "preserved first compiled step remains D0",
                    "current H43 paper endpoint",
                ],
            )
            and contains_all(
                p3_arbitrary_c_reason,
                [
                    "preserved first compiled boundary",
                    "current H43 paper endpoint",
                ],
            )
            and contains_none(inputs["h0_public_surface_audit_text"], [old_h0_phrase])
            and contains_none(inputs["p3_unsupported_claims_text"], [old_p3_phrase])
            and contains_none(inputs["p3_artifact_map_text"], [old_p3_phrase])
            else "blocked",
            "notes": "Regenerated H0/P3 outputs should treat D0 as preserved first compiled support inside the broader current H43 endpoint, not as the whole current endpoint.",
        },
        {
            "item_id": "indexes_and_handoff_preserve_p31_current_and_record_p32_auxiliary_completion",
            "status": "pass"
            if contains_all(
                inputs["status_text"],
                [
                    "guardrail refresh wave `P31`",
                    "`P32`",
                ],
            )
            and contains_all(
                inputs["publication_readme_text"],
                [
                    "docs/milestones/P31_post_h43_blog_guardrails_refresh/",
                    "docs/milestones/P32_post_h43_historical_wording_refresh/",
                    "results/P32_post_h43_historical_wording_refresh/summary.json",
                ],
            )
            and contains_all(
                inputs["plans_index_text"],
                [
                    "2026-03-24-post-h43-p32-historical-wording-refresh-design.md",
                    "../milestones/P32_post_h43_historical_wording_refresh/",
                    "../milestones/P31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["milestones_index_text"],
                [
                    "P32_post_h43_historical_wording_refresh/",
                    "P31_post_h43_blog_guardrails_refresh/",
                ],
            )
            and contains_all(
                inputs["active_wave_plan_text"],
                [
                    "`P31_post_h43_blog_guardrails_refresh` is the current low-priority",
                    "`P32` is the completed auxiliary historical/regeneration wording refresh packet",
                    "wip/p32-h43-historical-wording-refresh",
                ],
            )
            and contains_all(
                inputs["experiment_manifest_text"],
                [
                    "post-`H43` `P32` historical-wording refresh wave",
                    "scripts/export_p32_post_h43_historical_wording_refresh.py",
                    "results/P32_post_h43_historical_wording_refresh/summary.json",
                ],
            )
            else "blocked",
            "notes": "Status, index, and handoff surfaces should keep P31 current while recording P32 as a completed auxiliary historical-wording packet.",
        },
        {
            "item_id": "upstream_h43_and_p31_packets_remain_preserved",
            "status": "pass"
            if str(inputs["h43_summary"]["summary"]["selected_outcome"]) == "freeze_r44_as_narrow_supported_here"
            and str(inputs["h43_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            and str(inputs["p31_summary"]["summary"]["selected_outcome"]) == "blocked_blog_guardrails_refreshed_to_h43"
            and str(inputs["p31_summary"]["summary"]["next_required_lane"]) == "no_active_downstream_runtime_lane"
            else "blocked",
            "notes": "P32 should stay strictly downstream of the landed H43 and P31 packets while preserving their selected outcomes.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "docs/plans/2026-03-24-post-h43-p32-historical-wording-refresh-design.md": (
            "design_text",
            ["`P32_post_h43_historical_wording_refresh`", "`historical_wording_regeneration_surfaces_refreshed_to_h43`"],
        ),
        "results/H0_repo_consolidation_and_release_hygiene/public_surface_audit.json": (
            "h0_public_surface_audit_text",
            ["preserved first compiled step remains D0", "current H43 paper endpoint"],
        ),
        "results/P3_paper_freeze_and_evidence_mapping/unsupported_claims.json": (
            "p3_unsupported_claims_text",
            ["preserved first compiled boundary", "current H43 paper endpoint"],
        ),
        "results/P3_paper_freeze_and_evidence_mapping/artifact_map.json": (
            "p3_artifact_map_text",
            ["preserved first compiled boundary", "current H43 paper endpoint"],
        ),
        "STATUS.md": (
            "status_text",
            ["guardrail refresh wave `P31`", "`P32`"],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            ["docs/milestones/P32_post_h43_historical_wording_refresh/", "results/P32_post_h43_historical_wording_refresh/summary.json"],
        ),
        "docs/publication_record/experiment_manifest.md": (
            "experiment_manifest_text",
            ["post-`H43` `P32` historical-wording refresh wave", "results/P32_post_h43_historical_wording_refresh/summary.json"],
        ),
        "tmp/active_wave_plan.md": (
            "active_wave_plan_text",
            ["`P31_post_h43_blog_guardrails_refresh` is the current low-priority", "`P32_post_h43_historical_wording_refresh` is the completed auxiliary"],
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
        "refresh_packet": "p32_post_h43_historical_wording_refresh",
        "refresh_scope": "historical_regeneration_wording_surfaces",
        "selected_outcome": "historical_wording_regeneration_surfaces_refreshed_to_h43",
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
            "experiment": "p32_post_h43_historical_wording_refresh",
            "environment": environment.as_dict(),
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "p32_post_h43_historical_wording_refresh",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "p32_post_h43_historical_wording_refresh",
            "environment": environment.as_dict(),
            "rows": snapshot_rows,
        },
    )


if __name__ == "__main__":
    main()
