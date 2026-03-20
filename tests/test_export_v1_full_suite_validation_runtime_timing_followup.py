from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_v1_full_suite_validation_runtime_timing_followup.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_v1_full_suite_validation_runtime_timing_followup", module_path
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_select_timing_candidates_prioritizes_model_training_rows() -> None:
    module = _load_export_module()

    rows = module.select_timing_candidates(
        [
            {"file_path": "tests/test_bytecode.py", "category": "bytecode", "test_count": 4, "heuristic_score": 40, "torch_dependent": False},
            {"file_path": "tests/test_model_b.py", "category": "model_or_training", "test_count": 3, "heuristic_score": 18, "torch_dependent": True},
            {"file_path": "tests/test_model_a.py", "category": "model_or_training", "test_count": 3, "heuristic_score": 30, "torch_dependent": True},
        ],
        max_file_count=2,
        heuristic_score_floor=17,
    )

    assert [row["file_path"] for row in rows] == [
        "tests/test_model_a.py",
        "tests/test_model_b.py",
    ]


def test_parse_pytest_timing_output_reads_summary_and_durations() -> None:
    module = _load_export_module()

    parsed = module.parse_pytest_timing_output(
        "\n".join(
            [
                "============================= slowest 2 durations =============================",
                "12.34s call     tests/test_model_a.py::test_train",
                "0.44s call     tests/test_model_a.py::test_eval",
                "2 passed in 12.99s",
            ]
        )
    )

    assert parsed["summary_line"] == "2 passed in 12.99s"
    assert parsed["reported_seconds"] == 12.99
    assert parsed["duration_rows"][0]["test_id"] == "tests/test_model_a.py::test_train"


def test_build_summary_marks_healthy_but_slow_when_rows_pass() -> None:
    module = _load_export_module()

    summary = module.build_summary(
        [
            {
                "file_path": "tests/test_model_a.py",
                "wall_seconds": 75.0,
                "completed": True,
                "timed_out": False,
                "returncode": 0,
                "heuristic_score": 30,
                "summary_line": "2 passed in 74.50s",
            },
            {
                "file_path": "tests/test_model_b.py",
                "wall_seconds": 20.0,
                "completed": True,
                "timed_out": False,
                "returncode": 0,
                "heuristic_score": 18,
                "summary_line": "3 passed in 19.50s",
            },
        ],
        candidate_count=10,
    )

    assert summary["runtime_classification"] == "healthy_but_slow"
    assert summary["selected_file_count"] == 2
    assert summary["slowest_files"][0]["file_path"] == "tests/test_model_a.py"


def test_build_summary_marks_healthy_but_slow_on_aggregate_wall_time() -> None:
    module = _load_export_module()

    summary = module.build_summary(
        [
            {
                "file_path": "tests/test_model_a.py",
                "wall_seconds": 35.0,
                "completed": True,
                "timed_out": False,
                "returncode": 0,
                "heuristic_score": 30,
                "summary_line": "2 passed in 34.50s",
            },
            {
                "file_path": "tests/test_model_b.py",
                "wall_seconds": 30.5,
                "completed": True,
                "timed_out": False,
                "returncode": 0,
                "heuristic_score": 18,
                "summary_line": "3 passed in 30.00s",
            },
        ],
        candidate_count=10,
    )

    assert summary["runtime_classification"] == "healthy_but_slow"


def test_build_timing_rows_uses_runner_output() -> None:
    module = _load_export_module()

    def fake_runner(file_path: str) -> dict[str, object]:
        return {
            "command": ["python", "-m", "pytest", file_path],
            "returncode": 0,
            "completed": True,
            "timed_out": False,
            "stdout": "1.00s call     tests/test_model_a.py::test_train\n1 passed in 1.20s\n",
            "stderr": "",
            "wall_seconds": 1.2345,
            "timeout_seconds": 240,
        }

    rows = module.build_timing_rows(
        [
            {
                "file_path": "tests/test_model_a.py",
                "category": "model_or_training",
                "test_count": 1,
                "heuristic_score": 30,
                "torch_dependent": True,
            }
        ],
        run_file_fn=fake_runner,
    )

    assert rows[0]["file_path"] == "tests/test_model_a.py"
    assert rows[0]["wall_seconds"] == 1.2345
    assert rows[0]["slowest_rows"][0]["seconds"] == 1.0
