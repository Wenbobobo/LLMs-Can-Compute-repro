"""Export the H2 bundle-lock and release-hygiene audit."""

from __future__ import annotations

import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "H2_bundle_lock_audit"


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
        "readme_text": read_text(ROOT / "README.md"),
        "status_text": read_text(ROOT / "STATUS.md"),
        "publication_readme_text": read_text(ROOT / "docs" / "publication_record" / "README.md"),
        "paper_package_plan_text": read_text(ROOT / "docs" / "publication_record" / "paper_package_plan.md"),
        "release_summary_text": read_text(ROOT / "docs" / "publication_record" / "release_summary_draft.md"),
        "paper_bundle_status_text": read_text(ROOT / "docs" / "publication_record" / "paper_bundle_status.md"),
        "submission_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "submission_candidate_criteria.md"
        ),
        "release_candidate_text": read_text(
            ROOT / "docs" / "publication_record" / "release_candidate_checklist.md"
        ),
        "reopen_protocol_text": read_text(
            ROOT / "docs" / "publication_record" / "conditional_reopen_protocol.md"
        ),
        "layout_log_text": read_text(ROOT / "docs" / "publication_record" / "layout_decision_log.md"),
    }


def build_checklist_rows(
    *,
    readme_text: str,
    status_text: str,
    publication_readme_text: str,
    paper_package_plan_text: str,
    release_summary_text: str,
    paper_bundle_status_text: str,
    submission_candidate_text: str,
    release_candidate_text: str,
    reopen_protocol_text: str,
    layout_log_text: str,
) -> list[dict[str, object]]:
    return [
        {
            "item_id": "readme_and_status_hold_post_p7_stabilization",
            "status": "pass"
            if contains_all(
                readme_text,
                [
                    "post-`p7` stabilization package is now defined",
                    "`p8` locks the submission-candidate bundle",
                    "`h2` promotes bundle-lock and release-hygiene audits",
                    "`p9` freezes the restrained public surface",
                ],
            )
            and contains_all(
                status_text,
                [
                    "post-`p7` stabilization lanes are now defined",
                    "`p8` locks the submission-candidate bundle",
                    "`h2` promotes bundle-lock/release-hygiene audits",
                    "`p9` freezes the restrained public surface",
                ],
            )
            else "blocked",
            "notes": "README and STATUS should both describe the active post-P7 stabilization package rather than another vague planning pass.",
        },
        {
            "item_id": "publication_record_tracks_active_package_driver",
            "status": "pass"
            if contains_all(
                publication_readme_text,
                [
                    "paper_package_plan.md",
                    "active post-`p7` package driver",
                    "submission_candidate_criteria.md",
                    "release_candidate_checklist.md",
                    "conditional_reopen_protocol.md",
                ],
            )
            and contains_all(
                paper_package_plan_text,
                ["## Goal", "## Fixed Inputs", "## Package Write Set", "## Exit Gate"],
            )
            else "blocked",
            "notes": "Publication record docs should name one active post-P7 package driver plus the new control docs.",
        },
        {
            "item_id": "release_summary_and_bundle_status_name_post_p7_package",
            "status": "pass"
            if contains_all(
                release_summary_text,
                [
                    "post-`p7` stabilization package",
                    "`p8` locks the submission-candidate bundle",
                    "`h2` promotes bundle-lock and release-hygiene audits",
                    "`p9` freezes the restrained public surface",
                ],
            )
            and contains_all(
                paper_bundle_status_text,
                [
                    "submission-candidate bundle-lock pass",
                    "default not to reopen claim/evidence scope",
                ],
            )
            else "blocked",
            "notes": "The short release summary and paper bundle status should both point to the same post-P7 package rather than stop at the freeze checkpoint.",
        },
        {
            "item_id": "submission_candidate_criteria_lock_scope",
            "status": "pass"
            if contains_all(
                submission_candidate_text,
                [
                    "freeze-candidate conditions still hold",
                    "manuscript bundle and supporting ledgers are locked together",
                    "appendix minimum package is explicit and complete",
                    "standing audits remain green",
                    "`h2`",
                ],
            )
            else "blocked",
            "notes": "Submission-candidate criteria should define a real bundle-lock gate on the same frozen scope.",
        },
        {
            "item_id": "release_candidate_checklist_stays_downstream",
            "status": "pass"
            if contains_all(
                release_candidate_text,
                [
                    "results/p1_paper_readiness/summary.json",
                    "results/p5_public_surface_sync/summary.json",
                    "results/p5_callout_alignment/summary.json",
                    "results/h2_bundle_lock_audit/summary.json",
                    "blog work remains blocked",
                ],
            )
            else "blocked",
            "notes": "The release-candidate checklist should keep outward sync downstream of the locked bundle and the standing audits.",
        },
        {
            "item_id": "conditional_reopen_protocol_requires_named_patch_lane",
            "status": "pass"
            if contains_all(
                reopen_protocol_text,
                [
                    "allowed triggers",
                    "`e1a_precision_patch`",
                    "`e1b_systems_patch`",
                    "`e1c_compiled_boundary_patch`",
                    "only one patch lane may be active at a time",
                    "returning control to `p8` or `p9`",
                ],
            )
            else "blocked",
            "notes": "Reopen control should force later agents into one named patch lane and a refreeze step.",
        },
        {
            "item_id": "layout_log_records_post_p7_governance",
            "status": "pass"
            if contains_all(layout_log_text, ["Post-`P7` next phase", "Evidence reopen discipline"])
            else "blocked",
            "notes": "The layout decision log should record the current post-P7 governance choices explicitly.",
        },
    ]


def build_snapshot(inputs: dict[str, str]) -> list[dict[str, object]]:
    lookup = {
        "README.md": (
            "readme_text",
            [
                "post-`P7` stabilization package is now defined",
                "`P8` locks the submission-candidate bundle",
                "`P9` freezes the restrained public surface",
            ],
        ),
        "STATUS.md": (
            "status_text",
            [
                "post-`P7` stabilization lanes are now defined",
                "`P8` locks the submission-candidate bundle",
                "`H2` promotes bundle-lock/release-hygiene audits",
            ],
        ),
        "docs/publication_record/README.md": (
            "publication_readme_text",
            [
                "paper_package_plan.md",
                "submission_candidate_criteria.md",
                "release_candidate_checklist.md",
                "conditional_reopen_protocol.md",
            ],
        ),
        "docs/publication_record/paper_package_plan.md": (
            "paper_package_plan_text",
            ["## Goal", "## Fixed Inputs", "## Package Write Set", "## Exit Gate"],
        ),
        "docs/publication_record/release_summary_draft.md": (
            "release_summary_text",
            [
                "post-`P7` stabilization package",
                "`P8` locks the submission-candidate bundle",
                "`H2` promotes bundle-lock and release-hygiene audits",
                "`P9` freezes the restrained public surface",
            ],
        ),
        "docs/publication_record/paper_bundle_status.md": (
            "paper_bundle_status_text",
            ["submission-candidate bundle-lock pass", "default not to reopen claim/evidence scope"],
        ),
        "docs/publication_record/submission_candidate_criteria.md": (
            "submission_candidate_text",
            [
                "Freeze-candidate conditions still hold",
                "Manuscript bundle and supporting ledgers are locked together",
                "Standing audits remain green",
            ],
        ),
        "docs/publication_record/release_candidate_checklist.md": (
            "release_candidate_text",
            [
                "results/P1_paper_readiness/summary.json",
                "results/P5_public_surface_sync/summary.json",
                "results/H2_bundle_lock_audit/summary.json",
                "Blog work remains blocked",
            ],
        ),
        "docs/publication_record/conditional_reopen_protocol.md": (
            "reopen_protocol_text",
            [
                "`E1a_precision_patch`",
                "`E1b_systems_patch`",
                "`E1c_compiled_boundary_patch`",
                "Only one patch lane may be active at a time",
            ],
        ),
        "docs/publication_record/layout_decision_log.md": (
            "layout_log_text",
            ["Post-`P7` next phase", "Evidence reopen discipline"],
        ),
    }
    rows: list[dict[str, object]] = []
    for path, (input_key, needles) in lookup.items():
        rows.append(
            {
                "path": path,
                "matched_lines": extract_matching_lines(inputs[input_key], needles=needles),
            }
        )
    return rows


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    blocked_items = [row["item_id"] for row in rows if row["status"] != "pass"]
    return {
        "current_paper_phase": "post_p7_submission_release_stabilization_active",
        "bundle_lock_scope": "publication_record_bundle_and_supporting_ledgers",
        "check_count": len(rows),
        "pass_count": sum(row["status"] == "pass" for row in rows),
        "blocked_count": sum(row["status"] != "pass" for row in rows),
        "blocked_items": blocked_items,
        "recommended_next_action": (
            "execute the P8 submission-candidate lock and P9 restrained public-surface freeze while keeping the H2 bundle-lock audit green"
            if not blocked_items
            else "resolve the blocked post-P7 bundle-lock or release-hygiene items before another outward sync"
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
        {
            "experiment": "h2_bundle_lock_audit_checklist",
            "environment": environment.as_dict(),
            "rows": rows,
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
                "docs/publication_record/paper_package_plan.md",
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
                "Machine-readable audit of the post-P7 bundle-lock and release-hygiene",
                "package used by the submission/release stabilization phase.",
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
