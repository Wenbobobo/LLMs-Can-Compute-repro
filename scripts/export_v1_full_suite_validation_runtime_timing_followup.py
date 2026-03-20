"""Export a bounded per-file timing follow-up for the V1 validation audit."""

from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "results" / "V1_full_suite_validation_runtime_audit"
OUT_DIR = ROOT / "results" / "V1_full_suite_validation_runtime_timing_followup"
PER_FILE_TIMEOUT_SECONDS = 240
MAX_FILE_COUNT = 6
HEURISTIC_SCORE_FLOOR = 17
DURATION_RE = re.compile(r"(?P<seconds>[\d.]+)s\s+\w+\s+(?P<test_id>tests/.*)")
SUMMARY_RE = re.compile(r".*\bin\s+(?P<seconds>[\d.]+)s$")


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def category_priority(category: str) -> int:
    return 0 if category == "model_or_training" else 1


def select_timing_candidates(
    file_inventory_rows: list[dict[str, Any]],
    *,
    max_file_count: int = MAX_FILE_COUNT,
    heuristic_score_floor: int = HEURISTIC_SCORE_FLOOR,
) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in file_inventory_rows
        if int(row["heuristic_score"]) >= heuristic_score_floor
    ]
    candidates.sort(
        key=lambda row: (
            category_priority(str(row["category"])),
            -int(row["heuristic_score"]),
            str(row["file_path"]),
        )
    )
    return candidates[:max_file_count]


def run_pytest_file(
    file_path: str,
    *,
    timeout_seconds: int = PER_FILE_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    command = [sys.executable, "-m", "pytest", "-q", file_path, "--durations=0"]
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        wall_seconds = time.perf_counter() - started
        return {
            "command": command,
            "returncode": None,
            "completed": False,
            "timed_out": True,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "wall_seconds": wall_seconds,
            "timeout_seconds": timeout_seconds,
        }

    wall_seconds = time.perf_counter() - started
    return {
        "command": command,
        "returncode": completed.returncode,
        "completed": True,
        "timed_out": False,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "wall_seconds": wall_seconds,
        "timeout_seconds": timeout_seconds,
    }


def parse_pytest_timing_output(stdout: str) -> dict[str, Any]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    summary_line = ""
    reported_seconds: float | None = None
    duration_rows: list[dict[str, Any]] = []
    for line in lines:
        match = DURATION_RE.fullmatch(line)
        if match:
            duration_rows.append(
                {
                    "seconds": float(match.group("seconds")),
                    "test_id": match.group("test_id"),
                }
            )
    for line in reversed(lines):
        match = SUMMARY_RE.fullmatch(line)
        if match and ("passed" in line or "failed" in line or "error" in line or "skipped" in line):
            summary_line = line
            reported_seconds = float(match.group("seconds"))
            break
    return {
        "summary_line": summary_line,
        "reported_seconds": reported_seconds,
        "duration_rows": duration_rows[:5],
    }


def build_timing_rows(
    candidates: list[dict[str, Any]],
    *,
    run_file_fn: Callable[[str], dict[str, Any]] = run_pytest_file,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        file_path = str(candidate["file_path"])
        run = run_file_fn(file_path)
        parsed = parse_pytest_timing_output(str(run["stdout"]))
        rows.append(
            {
                "file_path": file_path,
                "category": candidate["category"],
                "test_count": int(candidate["test_count"]),
                "heuristic_score": int(candidate["heuristic_score"]),
                "torch_dependent": bool(candidate["torch_dependent"]),
                "completed": bool(run["completed"]),
                "timed_out": bool(run["timed_out"]),
                "returncode": run["returncode"],
                "wall_seconds": round(float(run["wall_seconds"]), 4),
                "timeout_seconds": int(run["timeout_seconds"]),
                "summary_line": parsed["summary_line"],
                "reported_seconds": parsed["reported_seconds"],
                "slowest_rows": parsed["duration_rows"],
            }
        )
    rows.sort(key=lambda row: (-float(row["wall_seconds"]), str(row["file_path"])))
    return rows


def classify_runtime(rows: list[dict[str, Any]]) -> str:
    if any(row["timed_out"] or row["returncode"] not in (0, None) for row in rows):
        return "needs_function_level_split"
    total_wall = sum(float(row["wall_seconds"]) for row in rows)
    max_wall = max((float(row["wall_seconds"]) for row in rows), default=0.0)
    if max_wall >= 60.0 or total_wall >= 60.0:
        return "healthy_but_slow"
    return "bounded_followup_complete"


def build_summary(rows: list[dict[str, Any]], *, candidate_count: int) -> dict[str, Any]:
    classification = classify_runtime(rows)
    wall_seconds = [float(row["wall_seconds"]) for row in rows]
    recommended_next_action = {
        "needs_function_level_split": (
            "split the timed-out or failing file to function-level timings before trusting full pytest -q as a standing unattended gate"
        ),
        "healthy_but_slow": (
            "treat full pytest -q as a healthy but multi-minute gate on the current suite and reserve it for long unattended windows"
        ),
        "bounded_followup_complete": (
            "keep the bounded shortlist artifact as the current runtime classification reference and rerun it before escalating to another full-suite timing claim"
        ),
    }[classification]
    return {
        "runtime_classification": classification,
        "selected_file_count": len(rows),
        "candidate_pool_count": candidate_count,
        "completed_file_count": sum(bool(row["completed"]) for row in rows),
        "timed_out_file_count": sum(bool(row["timed_out"]) for row in rows),
        "median_wall_seconds": round(statistics.median(wall_seconds), 4) if wall_seconds else 0.0,
        "max_wall_seconds": round(max(wall_seconds), 4) if wall_seconds else 0.0,
        "total_wall_seconds": round(sum(wall_seconds), 4),
        "slowest_files": [
            {
                "file_path": row["file_path"],
                "wall_seconds": row["wall_seconds"],
                "heuristic_score": row["heuristic_score"],
                "summary_line": row["summary_line"],
            }
            for row in rows[:3]
        ],
        "selection_rule": (
            "bounded top model_or_training-heavy shortlist by heuristic score, capped at 6 files"
        ),
        "recommended_next_action": recommended_next_action,
        "notes": [
            "This follow-up remains operational and does not change scientific scope.",
            "Per-file timings classify likely runtime-heavy lanes before another full-suite unattended run.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    file_inventory = read_json(AUDIT_DIR / "file_inventory.json")
    candidates = select_timing_candidates(list(file_inventory["rows"]))
    timing_rows = build_timing_rows(candidates)
    summary = build_summary(timing_rows, candidate_count=len(file_inventory["rows"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "selected_candidates.json",
        {
            "experiment": "v1_full_suite_validation_runtime_timing_followup_selected_candidates",
            "environment": environment.as_dict(),
            "rows": candidates,
        },
    )
    write_json(
        OUT_DIR / "per_file_timings.json",
        {
            "experiment": "v1_full_suite_validation_runtime_timing_followup_per_file_timings",
            "environment": environment.as_dict(),
            "rows": timing_rows,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "v1_full_suite_validation_runtime_timing_followup",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/V1_full_suite_validation_runtime_audit/summary.json",
                "results/V1_full_suite_validation_runtime_audit/file_inventory.json",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# V1 Full-Suite Validation Runtime Timing Follow-Up",
                "",
                "Bounded per-file timing follow-up for the V1 validation-runtime audit.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `selected_candidates.json`",
                "- `per_file_timings.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
