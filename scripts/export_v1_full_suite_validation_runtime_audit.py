"""Export a bounded audit of the current full-suite validation runtime surface."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "V1_full_suite_validation_runtime_audit"
COLLECT_TIMEOUT_SECONDS = 180
SUMMARY_RE = re.compile(r"(?P<count>\d+)\s+tests collected in (?P<seconds>[\d.]+)s")
HEAVY_NAME_TOKENS = (
    "train",
    "training",
    "fit",
    "rollout",
    "executor",
    "stress",
    "precision",
    "generalize",
    "heldout",
)


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_collect_only(timeout_seconds: int = COLLECT_TIMEOUT_SECONDS) -> dict[str, Any]:
    command = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    wall_seconds = time.perf_counter() - started
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "wall_seconds": wall_seconds,
        "timeout_seconds": timeout_seconds,
    }


def parse_collect_output(stdout: str) -> dict[str, Any]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    test_ids = [line for line in lines if line.startswith("tests/") and "::" in line]
    summary_line = ""
    collected_count = len(test_ids)
    reported_seconds: float | None = None
    for line in reversed(lines):
        match = SUMMARY_RE.fullmatch(line)
        if match:
            summary_line = line
            collected_count = int(match.group("count"))
            reported_seconds = float(match.group("seconds"))
            break
    return {
        "test_ids": test_ids,
        "summary_line": summary_line,
        "reported_count": collected_count,
        "reported_seconds": reported_seconds,
    }


def file_category(file_path: str) -> str:
    path = Path(file_path)
    name = path.name
    if name.startswith("test_export_"):
        return "export_guard"
    if "model_" in name:
        return "model_or_training"
    if "bytecode_" in name:
        return "bytecode"
    if "geometry_" in name or "trace_" in name:
        return "core_runtime"
    return "other"


def is_torch_dependent_source(text: str) -> bool:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return 'find_spec("torch")' in text or "import torch" in text

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "torch" for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom):
            if node.module == "torch":
                return True
        if isinstance(node, ast.Call):
            if node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == "torch":
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr in {"find_spec", "importorskip"}:
                    return True
                if isinstance(func, ast.Name) and func.id == "importorskip":
                    return True
    return False


def build_file_inventory(test_ids: list[str], file_texts: dict[str, str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = {}
    for test_id in test_ids:
        file_path, _, _ = test_id.partition("::")
        grouped.setdefault(file_path, []).append(test_id)

    rows: list[dict[str, Any]] = []
    for file_path, ids in sorted(grouped.items()):
        text = file_texts.get(file_path, "")
        lowered_ids = [test_id.lower() for test_id in ids]
        torch_dependent = is_torch_dependent_source(text)
        heavy_name_hits = sum(any(token in test_id for token in HEAVY_NAME_TOKENS) for test_id in lowered_ids)
        category = file_category(file_path)
        heuristic_score = len(ids) + heavy_name_hits * 3 + (10 if torch_dependent else 0)
        rows.append(
            {
                "file_path": file_path,
                "category": category,
                "test_count": len(ids),
                "torch_dependent": torch_dependent,
                "heavy_name_hit_count": heavy_name_hits,
                "heuristic_score": heuristic_score,
                "sample_tests": ids[:5],
            }
        )
    rows.sort(key=lambda row: (-int(row["heuristic_score"]), str(row["file_path"])))
    return rows


def build_summary(
    *,
    collect_run: dict[str, Any],
    parsed: dict[str, Any],
    file_inventory: list[dict[str, Any]],
) -> dict[str, Any]:
    likely_heavy = [row for row in file_inventory if int(row["heuristic_score"]) >= 12][:10]
    torch_dependent_count = sum(bool(row["torch_dependent"]) for row in file_inventory)
    return {
        "validation_gate_status": "needs_runtime_classification",
        "collect_only_returncode": int(collect_run["returncode"]),
        "collect_only_completed": int(collect_run["returncode"]) == 0,
        "collected_test_count": int(parsed["reported_count"]),
        "test_file_count": len(file_inventory),
        "collect_only_reported_seconds": parsed["reported_seconds"],
        "collect_only_wall_seconds": round(float(collect_run["wall_seconds"]), 4),
        "torch_dependent_file_count": torch_dependent_count,
        "likely_heavy_file_count": len(likely_heavy),
        "likely_heavy_files": [
            {
                "file_path": row["file_path"],
                "category": row["category"],
                "test_count": row["test_count"],
                "torch_dependent": row["torch_dependent"],
                "heuristic_score": row["heuristic_score"],
            }
            for row in likely_heavy
        ],
        "recommended_next_action": (
            "run bounded per-file timings on the highest-scoring files before treating full pytest -q as a stable unattended standing gate"
        ),
        "notes": [
            "This audit classifies validation-runtime risk without changing scientific scope.",
            "Successful collect-only means the current uncertainty is runtime behavior, not test discovery.",
        ],
    }


def main() -> None:
    environment = detect_runtime_environment()
    collect_run = run_collect_only()
    parsed = parse_collect_output(str(collect_run["stdout"]))
    file_texts = {
        test_id.partition("::")[0]: read_text(ROOT / test_id.partition("::")[0])
        for test_id in parsed["test_ids"]
    }
    file_inventory = build_file_inventory(parsed["test_ids"], file_texts)
    summary = build_summary(collect_run=collect_run, parsed=parsed, file_inventory=file_inventory)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "collected_tests.json",
        {
            "experiment": "v1_full_suite_validation_runtime_audit_collected_tests",
            "environment": environment.as_dict(),
            "command": collect_run["command"],
            "test_ids": parsed["test_ids"],
            "summary_line": parsed["summary_line"],
        },
    )
    write_json(
        OUT_DIR / "file_inventory.json",
        {
            "experiment": "v1_full_suite_validation_runtime_audit_file_inventory",
            "environment": environment.as_dict(),
            "rows": file_inventory,
        },
    )
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "v1_full_suite_validation_runtime_audit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "pyproject.toml",
                "tests/",
            ],
            "summary": summary,
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# V1 Full-Suite Validation Runtime Audit",
                "",
                "Machine-readable audit of the current full-suite pytest collection",
                "surface and likely runtime-heavy files.",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `file_inventory.json`",
                "- `collected_tests.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
