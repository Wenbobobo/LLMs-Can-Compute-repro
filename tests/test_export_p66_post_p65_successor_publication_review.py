from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "export_p66_post_p65_successor_publication_review.py"
    )
    spec = importlib.util.spec_from_file_location(
        "export_p66_post_p65_successor_publication_review",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p66_writes_successor_publication_review_summary(tmp_path: Path, monkeypatch) -> None:
    module = _load_module()

    def _write_json(name: str, payload: dict[str, object]) -> Path:
        path = tmp_path / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_text(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    temp_p65_summary = _write_json(
        "p65_summary.json",
        {"summary": {"selected_outcome": "published_successor_merge_prep_control_synced_to_h64_stack"}},
    )
    temp_driver = _write_text(
        "current_stage_driver.md",
        [
            "P63_post_p62_published_successor_promotion_prep",
            "P64_post_p63_release_hygiene_rebaseline",
            "P65_post_p64_merge_prep_control_sync",
            "wip/p63-post-p62-tight-core-hygiene",
        ],
    )
    temp_registry = _write_text(
        "branch_worktree_registry.md",
        [
            "wip/p63-post-p62-tight-core-hygiene",
            "wip/p64-post-p63-successor-stack",
            "clean_descendant_only_never_dirty_root_main",
        ],
    )

    original_out_dir = module.OUT_DIR
    original_p65 = module.P65_SUMMARY_PATH
    original_driver = module.CURRENT_STAGE_DRIVER_PATH
    original_registry = module.BRANCH_REGISTRY_PATH
    temp_out_dir = tmp_path / "P66_post_p65_successor_publication_review"
    module.OUT_DIR = temp_out_dir
    module.P65_SUMMARY_PATH = temp_p65_summary
    module.CURRENT_STAGE_DRIVER_PATH = temp_driver
    module.BRANCH_REGISTRY_PATH = temp_registry

    outputs = {
        ("rev-list", "--left-right", "--count", "wip/p63-post-p62-tight-core-hygiene...wip/p64-post-p63-successor-stack"): "0 3",
        ("log", "--oneline", "wip/p63-post-p62-tight-core-hygiene..wip/p64-post-p63-successor-stack"): "\n".join(
            [
                "f95f221 docs(control): promote p63 successor stack",
                "e4cc4b7 feat(export): add post-p63 successor stack exporters",
                "055c482 test(export): cover post-p63 successor stack",
            ]
        ),
        ("diff", "--name-only", "wip/p63-post-p62-tight-core-hygiene..wip/p64-post-p63-successor-stack"): "\n".join(
            [
                "README.md",
                "docs/publication_record/current_stage_driver.md",
                "results/P65_post_p64_merge_prep_control_sync/summary.json",
                "scripts/export_p65_post_p64_merge_prep_control_sync.py",
                "tests/test_export_p65_post_p64_merge_prep_control_sync.py",
            ]
        ),
        ("rev-parse", "--abbrev-ref", "HEAD"): "wip/p66-post-p65-published-successor-freeze",
    }

    def fake_git_output(args: list[str]) -> str:
        key = tuple(args)
        assert key in outputs
        return outputs[key]

    monkeypatch.setattr(module, "git_output", fake_git_output)
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.P65_SUMMARY_PATH = original_p65
        module.CURRENT_STAGE_DRIVER_PATH = original_driver
        module.BRANCH_REGISTRY_PATH = original_registry

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["selected_outcome"] == "successor_publication_review_supports_p67_freeze"
    assert payload["summary"]["review_left_count"] == 0
    assert payload["summary"]["review_right_count"] == 3
    assert payload["summary"]["reviewed_commit_count"] == 3
    assert payload["summary"]["blocked_reviewed_path_count"] == 0
    assert payload["summary"]["blocked_count"] == 0
