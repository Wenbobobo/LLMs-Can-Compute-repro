"""Export the H2 bundle-lock audit for the current publication bundle."""

from __future__ import annotations

import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H2_bundle_lock_audit"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "current_stage_driver_text": read_text(ROOT / "docs" / "publication_record" / "current_stage_driver.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "paper_bundle_status_text": read_text(ROOT / "docs" / "publication_record" / "paper_bundle_status.md"),
        "submission_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md"
        ),
        "release_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "release_candidate_checklist.md"
        ),
        "conditional_reopen_text": read_text(
            ROOT / "docs" / "publication_record" / "conditional_reopen_protocol.md"
        ),
        "layout_log_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
    }


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    current_stage_driver_text: str,
    release_summary_text: str,
    paper_bundle_status_text: str,
    submission_candidate_text: str,
    release_candidate_text: str,
    conditional_reopen_text: str,
    layout_log_text: str,
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "top_level_surfaces_lock_current_h52_h43_bundle",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                    "`r56_origin_append_only_trace_vm_semantics_gate`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`h36_post_r40_bounded_scalar_family_refreeze`",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "`merge_executed = false`",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should lock the publication bundle onto the current H52 control stack while preserving H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "publication_record_core_docs_expose_current_h52_h43_bundle",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "## current control docs",
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "../milestones/p37_post_h50_narrow_executor_closeout_sync/",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`r55_origin_2d_hardmax_retrieval_equivalence_gate`",
                    "`r56_origin_append_only_trace_vm_semantics_gate`",
                    "`r57_origin_accelerated_trace_vm_comparator_gate`",
                ],
            )
            and contains_all(
                current_stage_driver_text,
                [
                    "the current active stage is:",
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h50_post_r51_r52_scope_decision_packet`",
                    "`h51_post_h50_origin_mechanism_reentry_packet`",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                    "`h43_post_r44_useful_case_refreeze`",
                    "`no_active_downstream_runtime_lane`",
                ],
            )
            else "blocked",
            "notes": "Publication README and current-stage driver should expose the same H52 current-control plus preserved H43 paper bundle.",
        },
        {
            "item_id": "release_summary_and_bundle_status_stay_downstream",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "`h52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                    "`h43` remains the paper-grade endpoint",
                    "`r57` as negative fast-path comparator evidence",
                    "`p37_post_h50_narrow_executor_closeout_sync`",
                ],
            )
            and contains_all(
                paper_bundle_status_text,
                [
                    "`h52` is the current active docs-only closeout packet",
                    "`h43` remains the paper-grade endpoint",
                    "`r57` is the completed negative fast-path comparator gate",
                    "`p37` is the aligned low-priority",
                ],
            )
            else "blocked",
            "notes": "Release summary and paper bundle status should remain downstream of the current H52 control state while preserving H43 as the paper-grade endpoint.",
        },
        {
            "item_id": "submission_and_release_candidate_controls_preserve_h43_bundle_under_h52_control",
            "status": "pass"
            if contains_all(
                submission_candidate_text,
                [
                    "active `h43` docs-only useful-case",
                    "completed `r42/r43/r44/r45` semantic-boundary gate stack",
                    "results/p28_post_h43_publication_surface_sync/summary.json",
                ],
            )
            and contains_all(
                release_candidate_text,
                [
                    "current `h52` active docs-only mechanism closeout packet",
                    "`h43` paper-grade endpoint",
                    "`r42-r43-r44-r45-r55-r56-r57` completed evidence",
                    "results/h52_post_r55_r56_r57_origin_mechanism_decision_packet/summary.json",
                    "results/h43_post_r44_useful_case_refreeze/summary.json",
                ],
            )
            else "blocked",
            "notes": "Submission and release-candidate controls should preserve the paper-grade H43 bundle while exposing H52 as the current control state.",
        },
        {
            "item_id": "conditional_reopen_protocol_stays_closed_by_default",
            "status": "pass"
            if contains_all(
                conditional_reopen_text,
                [
                    "State: `dormant_protocol`.",
                    "Only one patch lane may be active at a time",
                    "`E1a_precision_patch`",
                    "`E1b_systems_patch`",
                    "`E1c_compiled_boundary_patch`",
                ],
            )
            else "blocked",
            "notes": "Bundle lock should still route any reopen through the dormant explicit patch protocol.",
        },
        {
            "item_id": "layout_log_records_bundle_lock_governance",
            "status": "pass"
            if contains_all(
                layout_log_text,
                ["Release-summary reuse", "Post-`P7` next phase", "Evidence reopen discipline"],
            )
            else "blocked",
            "notes": "The layout log should preserve the publication bundle governance choices.",
        },
    ]


def build_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H50_post_r51_r52_scope_decision_packet`",
                "`H51_post_h50_origin_mechanism_reentry_packet`",
                "`H43_post_r44_useful_case_refreeze`",
                "`R57_origin_accelerated_trace_vm_comparator_gate`",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H50_post_r51_r52_scope_decision_packet`",
                "`H51_post_h50_origin_mechanism_reentry_packet`",
                "`P37_post_h50_narrow_executor_closeout_sync`",
                "`merge_executed = false`",
            ],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`P37_post_h50_narrow_executor_closeout_sync`",
                "`H43_post_r44_useful_case_refreeze`",
                "`R57_origin_accelerated_trace_vm_comparator_gate`",
            ],
        ),
        "docs/publication_record/current_stage_driver.md": (
            "current_stage_driver_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H50_post_r51_r52_scope_decision_packet`",
                "`H51_post_h50_origin_mechanism_reentry_packet`",
                "`P37_post_h50_narrow_executor_closeout_sync`",
                "`H43_post_r44_useful_case_refreeze`",
                "`no_active_downstream_runtime_lane`",
            ],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            [
                "`H52_post_r55_r56_r57_origin_mechanism_decision_packet`",
                "`H43` remains the paper-grade endpoint",
                "`R57` as negative fast-path comparator evidence",
            ],
        ),
        "docs/publication_record/paper_bundle_status.md": (
            "paper_bundle_status_text",
            [
                "`H52` is the current active docs-only closeout packet",
                "`H43` remains the paper-grade endpoint",
                "`R57` is the completed negative fast-path comparator gate",
                "`P37` is the aligned low-priority",
            ],
        ),
        "docs/publication_record/submission_candidate_criteria.md": (
            "submission_candidate_text",
            ["active `H43` docs-only useful-case", "results/P28_post_h43_publication_surface_sync/summary.json"],
        ),
        "docs/publication_record/release_candidate_checklist.md": (
            "release_candidate_text",
            ["current `H43` docs-only useful-case refreeze", "results/H43_post_r44_useful_case_refreeze/summary.json"],
        ),
        "docs/publication_record/conditional_reopen_protocol.md": (
            "conditional_reopen_text",
            ["State: `dormant_protocol`.", "`E1a_precision_patch`", "`E1c_compiled_boundary_patch`"],
        ),
        "docs/publication_record/layout_decision_log.md": (
            "layout_log_text",
            ["Release-summary reuse", "Evidence reopen discipline"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h52_current_control_with_h43_paper_endpoint",
        "bundle_lock_scope": "publication_record_bundle_and_supporting_ledgers",
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "keep the H2 bundle-lock audit green while H52 stays explicit as the current docs-only mechanism closeout packet, preserve H50 as the broader-route value closeout, preserve H51 as the prior mechanism-reentry packet, preserve H43 as the paper-grade endpoint, preserve H42/H41 as the prior docs-only packets, preserve H36 as the routing/refreeze packet, keep R42/R43/R44/R45 as the completed semantic-boundary gate stack, keep R55/R56 as exact mechanism evidence, keep R57 as negative fast-path comparator evidence, preserve P27/P28/P37 as operational release-control context, and keep no_active_downstream_runtime_lane as the current follow-on state"
            if not blocked_items
            else "resolve the blocked H2 bundle-lock items before treating the publication bundle as locked"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "h2_bundle_lock_audit_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "h2_bundle_lock_audit_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "h2_bundle_lock_audit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/README.md",
                "docs/publication_record/current_stage_driver.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/paper_bundle_status.md",
                "docs/publication_record/submission_candidate_criteria.md",
                "docs/publication_record/release_candidate_checklist.md",
                "docs/publication_record/conditional_reopen_protocol.md",
                "docs/publication_record/layout_decision_log.md",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# H2 Bundle Lock Audit",
                "",
                "Machine-readable audit of whether the current publication bundle remains",
                "locked to the current H52 control stack while preserving the H43 paper-grade endpoint and the dormant reopen protocol.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `checklist.json`",
                "- `snapshot.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
