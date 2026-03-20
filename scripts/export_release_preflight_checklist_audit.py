"""Export a machine-readable audit for the release preflight checklist."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "release_preflight_checklist_audit"


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
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "release_preflight_text": read_text(
            ROOT / "docs" / "publication_record" / "release_preflight_checklist.md"
        ),
        "manuscript_text": read_text(ROOT / "docs" / "publication_record" / "manuscript_bundle_draft.md"),
        "paper_bundle_status_text": read_text(
            ROOT / "docs" / "publication_record" / "paper_bundle_status.md"
        ),
        "layout_log_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
        "freeze_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "freeze_candidate_criteria.md"
        ),
        "main_text_order_text": read_text(ROOT / "docs" / "publication_record" / "main_text_order.md"),
        "appendix_scope_text": read_text(
            ROOT / "docs" / "publication_record" / "appendix_companion_scope.md"
        ),
        "blog_rules_text": read_text(ROOT / "docs" / "publication_record" / "blog_release_rules.md"),
        "p1_summary": read_json(ROOT / "results" / "P1_paper_readiness" / "summary.json"),
        "p5_summary": read_json(ROOT / "results" / "P5_public_surface_sync" / "summary.json"),
        "p5_callout_summary": read_json(ROOT / "results" / "P5_callout_alignment" / "summary.json"),
        "h2_summary": read_json(ROOT / "results" / "H2_bundle_lock_audit" / "summary.json"),
        "worktree_hygiene_summary_text": read_text(
            ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
        ),
        "worktree_hygiene_summary": read_json(
            ROOT / "results" / "release_worktree_hygiene_snapshot" / "summary.json"
        ),
        "v1_timing_summary": read_json(
            ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup" / "summary.json"
        ),
    }


def ready_count_from_p1_summary(p1_summary: dict[str, Any]) -> int:
    for row in p1_summary["figure_table_status_summary"]["by_status"]:
        if row["status"] == "ready":
            return int(row["count"])
    return 0


def blocked_count_from_summary(summary_doc: dict[str, Any]) -> int:
    summary = summary_doc["summary"]
    if "blocked_count" in summary:
        return int(summary["blocked_count"])
    return int(summary["blocked_rows"])


def runtime_classification_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["runtime_classification"])


def timed_out_count_from_summary(summary_doc: dict[str, Any]) -> int:
    return int(summary_doc["summary"]["timed_out_file_count"])


def release_commit_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["release_commit_state"])


def diff_check_state_from_summary(summary_doc: dict[str, Any]) -> str:
    return str(summary_doc["summary"]["git_diff_check_state"])


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    release_summary_text: str,
    release_preflight_text: str,
    manuscript_text: str,
    paper_bundle_status_text: str,
    layout_log_text: str,
    freeze_candidate_text: str,
    main_text_order_text: str,
    appendix_scope_text: str,
    blog_rules_text: str,
    p1_summary: dict[str, Any],
    p5_summary: dict[str, Any],
    p5_callout_summary: dict[str, Any],
    h2_summary: dict[str, Any],
    worktree_hygiene_summary_text: str,
    worktree_hygiene_summary: dict[str, Any],
    v1_timing_summary: dict[str, Any],
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "top_level_release_surface_stays_narrow_and_active_stage_explicit",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "does **not** claim that general llms are computers",
                    "arbitrary c has been reproduced",
                    "| `h13-v1` | completed governance/runtime handoff preserved as a control baseline",
                    "| `h14-h15` | completed bounded core-first reopen/refreeze packet",
                ],
            )
            and contains_all(
                status_text,
                [
                    "`h15_refreeze_and_decision_sync`",
                    "`h14_core_first_reopen_and_scope_lock`",
                    "`v1_full_suite_validation_runtime_audit` remains the standing bounded operational reference",
                    "`healthy_but_slow`",
                    "`h10/h11/r8/r9/r10/h12` remains the latest completed same-endpoint",
                    "`e1c` remains conditional only",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should keep the narrow scope explicit while naming current H15, preserved H14/H13/V1 state, and bounded runtime classification.",
        },
        {
            "item_id": "release_preflight_checklist_tracks_current_machine_guards",
            "status": "pass"
            if contains_all(
                release_preflight_text,
                [
                    "results/P1_paper_readiness/summary.json",
                    "results/P5_public_surface_sync/summary.json",
                    "results/P5_callout_alignment/summary.json",
                    "results/H2_bundle_lock_audit/summary.json",
                    "results/release_worktree_hygiene_snapshot/summary.json",
                    "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
                ],
            )
            else "blocked",
            "notes": "The human release checklist should point at the current standing machine guards, including the V1 timing follow-up.",
        },
        {
            "item_id": "release_summary_and_blog_rules_stay_downstream",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "narrow execution-substrate claim",
                    "`h13/v1` is now the preserved governance/runtime handoff",
                    "the current active post-`p9` stage is `h15_refreeze_and_decision_sync`",
                    "`e1c` remains conditional only",
                ],
            )
            and contains_all(
                blog_rules_text,
                [
                    "release_candidate_checklist.md",
                    "blog stays blocked unless all of the following are true",
                    "no arbitrary c",
                    "no broad “llms are computers” framing",
                ],
            )
            else "blocked",
            "notes": "Release summary and blog rules must remain downstream of the frozen manuscript bundle and current release gates.",
        },
        {
            "item_id": "manuscript_bundle_stays_section_ordered",
            "status": "pass"
            if contains_all(
                manuscript_text,
                [
                    "## 1. Abstract",
                    "## 10. Reproducibility Appendix",
                    "The no-widening decision is part",
                    "Companion appendix material stays clearly downstream",
                ],
            )
            else "blocked",
            "notes": "The manuscript bundle should remain a section-shaped frozen draft rather than drifting back into planning notes.",
        },
        {
            "item_id": "paper_facing_ledgers_stay_synchronized",
            "status": "pass"
            if contains_all(
                paper_bundle_status_text,
                [
                    "locked submission-candidate bundle",
                    "claim/evidence scope kept closed by default",
                    "current submission/release controls",
                ],
            )
            and contains_all(
                layout_log_text,
                ["Post-`P7` next phase", "Release-summary reuse", "Evidence reopen discipline"],
            )
            and contains_all(
                freeze_candidate_text,
                [
                    "claim boundaries stay fixed",
                    "main-text artifact set stays fixed and ready",
                    "appendix companions stay scoped and auditable",
                    "release-facing derivatives remain downstream",
                    "docs/publication_record/release_preflight_checklist.md",
                ],
            )
            and contains_all(
                main_text_order_text,
                [
                    "## Fixed order",
                    "Introduction and Claim Ladder",
                    "Compiled Boundary",
                    "Do not promote the full `R2` runtime matrix",
                ],
            )
            and contains_all(
                appendix_scope_text,
                [
                    "## Required companions",
                    "## Allowed optional companions",
                    "## Out of scope on the current freeze candidate",
                    "Broader compiled demos or any frontend widening beyond `D0`",
                ],
            )
            else "blocked",
            "notes": "The frozen manuscript, bundle-status, figure-order, and appendix-scope ledgers should continue to agree.",
        },
        {
            "item_id": "release_worktree_hygiene_snapshot_classifies_commit_state",
            "status": "pass"
            if release_commit_state_from_summary(worktree_hygiene_summary)
            in {
                "dirty_worktree_release_commit_blocked",
                "clean_worktree_ready_if_other_gates_green",
            }
            and diff_check_state_from_summary(worktree_hygiene_summary) != "content_issues_present"
            else "blocked",
            "notes": "The worktree hygiene snapshot should classify current release-commit readiness and rule out diff-check content issues.",
        },
        {
            "item_id": "standing_audits_remain_green",
            "status": "pass"
            if ready_count_from_p1_summary(p1_summary) == 10
            and not p1_summary["blocked_or_partial_items"]
            and blocked_count_from_summary(p5_summary) == 0
            and blocked_count_from_summary(p5_callout_summary) == 0
            and blocked_count_from_summary(h2_summary) == 0
            and runtime_classification_from_summary(v1_timing_summary) == "healthy_but_slow"
            and timed_out_count_from_summary(v1_timing_summary) == 0
            else "blocked",
            "notes": "The current release-preflight surface still depends on the frozen P1/P5/H2 chain and the bounded V1 timing classification.",
        },
    ]


def build_snapshot(inputs: dict[str, Any]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "| `H13-V1` | completed governance/runtime handoff preserved as a control baseline",
                "| `H14-H15` | completed bounded core-first reopen/refreeze packet",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "`H15_refreeze_and_decision_sync`",
                "`H14_core_first_reopen_and_scope_lock`",
                "`H13_post_h12_rollover_and_next_stage_staging` is no longer the active stage",
                "`healthy_but_slow`",
                "`H10/H11/R8/R9/R10/H12` remains the latest completed same-endpoint",
            ],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            [
                "`H13/V1` is now the preserved governance/runtime handoff",
                "The current active post-`P9` stage is `H15_refreeze_and_decision_sync`",
                "`E1c` remains conditional only",
            ],
        ),
        "docs/publication_record/release_preflight_checklist.md": (
            "release_preflight_text",
            [
                "results/P1_paper_readiness/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
            ],
        ),
        "results/release_worktree_hygiene_snapshot/summary.json": (
            "worktree_hygiene_summary_text",
            [
                "\"release_commit_state\":",
                "\"git_diff_check_state\":",
            ],
        ),
        "docs/publication_record/manuscript_bundle_draft.md": (
            "manuscript_text",
            [
                "## 1. Abstract",
                "The no-widening decision is part",
                "Companion appendix material stays clearly downstream",
                "## 10. Reproducibility Appendix",
            ],
        ),
        "docs/publication_record/paper_bundle_status.md": (
            "paper_bundle_status_text",
            [
                "locked submission-candidate bundle",
                "claim/evidence scope kept closed by default",
                "current submission/release controls",
            ],
        ),
        "docs/publication_record/freeze_candidate_criteria.md": (
            "freeze_candidate_text",
            [
                "Claim boundaries stay fixed",
                "Appendix companions stay scoped and auditable",
                "Release-facing derivatives remain downstream",
            ],
        ),
        "docs/publication_record/main_text_order.md": (
            "main_text_order_text",
            [
                "## Fixed order",
                "Compiled Boundary",
                "Do not promote the full `R2` runtime matrix",
            ],
        ),
        "docs/publication_record/appendix_companion_scope.md": (
            "appendix_scope_text",
            [
                "## Required companions",
                "## Allowed optional companions",
                "## Out of scope on the current freeze candidate",
            ],
        ),
        "docs/publication_record/blog_release_rules.md": (
            "blog_rules_text",
            [
                "release_candidate_checklist.md",
                "blog stays blocked unless all of the following are true",
                "no broad “llms are computers” framing",
            ],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append({"path": path, "matched_lines": extract_matching_lines(inputs[input_key], needles=needles)})
    return rows


def build_summary(checklist_rows: list[dict[str, object]], worktree_hygiene_summary: dict[str, Any]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in checklist_rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "h15_refreeze_and_decision_sync_complete",
        "preflight_scope": "outward_release_surface_and_frozen_paper_bundle",
        "preflight_state": "docs_and_audits_green" if not blocked_items else "blocked",
        "release_commit_state": release_commit_state_from_summary(worktree_hygiene_summary),
        "git_diff_check_state": diff_check_state_from_summary(worktree_hygiene_summary),
        "check_count": len(checklist_rows),
        "pass_count": sum(row["status"] == "pass" for row in checklist_rows),
        "blocked_count": sum(row["status"] != "pass" for row in checklist_rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "use this audit together with release_worktree_hygiene_snapshot as the outward-sync control reference while H15 remains the current refrozen stage, H14/R11/R12 remains the completed reopen packet, and H13/V1 remains preserved handoff state"
            if not blocked_items
            else "resolve the blocked release-preflight items before treating outward-sync docs as stable"
        ),
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    checklist_rows = build_checklist_rows(**inputs)
    snapshot = build_snapshot(inputs)
    summary = build_summary(checklist_rows, inputs["worktree_hygiene_summary"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "checklist.json",
        {
            "experiment": "release_preflight_checklist_audit_checklist",
            "environment": environment.as_dict(),
            "rows": checklist_rows,
        },
    )
    write_json(
        OUT_DIR / "snapshot.json",
        {
            "experiment": "release_preflight_checklist_audit_snapshot",
            "environment": environment.as_dict(),
            "rows": snapshot,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "release_preflight_checklist_audit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "README.md",
                "STATUS.md",
                "docs/publication_record/release_summary_draft.md",
                "docs/publication_record/release_preflight_checklist.md",
                "docs/publication_record/manuscript_bundle_draft.md",
                "docs/publication_record/paper_bundle_status.md",
                "docs/publication_record/layout_decision_log.md",
                "docs/publication_record/freeze_candidate_criteria.md",
                "docs/publication_record/main_text_order.md",
                "docs/publication_record/appendix_companion_scope.md",
                "docs/publication_record/blog_release_rules.md",
                "results/P1_paper_readiness/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/P5_callout_alignment/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "results/release_worktree_hygiene_snapshot/summary.json",
                "results/V1_full_suite_validation_runtime_timing_followup/summary.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Release Preflight Checklist Audit",
                "",
                "Machine-readable audit of whether the current outward release-facing docs",
                "and frozen paper bundle remain aligned on the current H15 refrozen",
                "stage, the preserved H14 reopen packet, and the preserved H13/V1 handoff. Current release-commit readiness is carried by the",
                "separate worktree hygiene snapshot.",
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
