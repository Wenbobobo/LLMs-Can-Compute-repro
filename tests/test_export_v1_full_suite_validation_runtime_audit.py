from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_v1_full_suite_validation_runtime_audit.py"
    spec = importlib.util.spec_from_file_location("export_v1_full_suite_validation_runtime_audit", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_collect_output_reads_ids_and_summary() -> None:
    module = _load_export_module()

    parsed = module.parse_collect_output(
        "\n".join(
            [
                "tests/test_alpha.py::test_one",
                "tests/test_beta.py::test_two",
                "2 tests collected in 0.12s",
            ]
        )
    )

    assert parsed["test_ids"] == [
        "tests/test_alpha.py::test_one",
        "tests/test_beta.py::test_two",
    ]
    assert parsed["reported_count"] == 2
    assert parsed["reported_seconds"] == 0.12


def test_build_file_inventory_scores_torch_training_files_higher() -> None:
    module = _load_export_module()

    rows = module.build_file_inventory(
        [
            "tests/test_model_runtime.py::test_train_executor",
            "tests/test_model_runtime.py::test_rollout_executor",
            "tests/test_export_guard.py::test_small_export",
        ],
        {
            "tests/test_model_runtime.py": 'import pytest\n@pytest.mark.skipif(importlib.util.find_spec("torch") is None, reason="torch")\n',
            "tests/test_export_guard.py": "def test_small_export():\n    pass\n",
        },
    )

    assert rows[0]["file_path"] == "tests/test_model_runtime.py"
    assert rows[0]["torch_dependent"] is True
    assert rows[0]["heuristic_score"] > rows[1]["heuristic_score"]


def test_build_file_inventory_ignores_torch_strings_inside_literals() -> None:
    module = _load_export_module()

    rows = module.build_file_inventory(
        ["tests/test_export_guard.py::test_fixture"],
        {
            "tests/test_export_guard.py": (
                'def test_fixture():\n'
                '    source = \'@pytest.mark.skipif(importlib.util.find_spec("torch") is None)\'\n'
                "    assert source\n"
            ),
        },
    )

    assert rows[0]["torch_dependent"] is False


def test_build_summary_marks_runtime_classification_needed() -> None:
    module = _load_export_module()

    summary = module.build_summary(
        collect_run={
            "returncode": 0,
            "wall_seconds": 9.5,
        },
        parsed={
            "reported_count": 188,
            "reported_seconds": 9.07,
        },
        file_inventory=[
            {
                "file_path": "tests/test_model_runtime.py",
                "category": "model_or_training",
                "test_count": 12,
                "torch_dependent": True,
                "heavy_name_hit_count": 5,
                "heuristic_score": 37,
            },
            {
                "file_path": "tests/test_export_guard.py",
                "category": "export_guard",
                "test_count": 4,
                "torch_dependent": False,
                "heavy_name_hit_count": 0,
                "heuristic_score": 4,
            },
        ],
    )

    assert summary["validation_gate_status"] == "needs_runtime_classification"
    assert summary["collect_only_completed"] is True
    assert summary["collected_test_count"] == 188
    assert summary["likely_heavy_file_count"] == 1
    assert summary["likely_heavy_files"][0]["file_path"] == "tests/test_model_runtime.py"
