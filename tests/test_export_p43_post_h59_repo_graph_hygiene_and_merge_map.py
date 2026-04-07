from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def _load_module(script_name: str, module_name: str):
    module_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_export_p43_writes_repo_graph_hygiene_summary(tmp_path: Path) -> None:
    module = _load_module(
        "export_p43_post_h59_repo_graph_hygiene_and_merge_map.py",
        "export_p43_post_h59_repo_graph_hygiene_and_merge_map",
    )

    sample_worktree_list = "\n".join(
        [
            "worktree D:/zWenbo/AI/LLMCompute",
            "HEAD deadbeef",
            "branch refs/heads/wip/root-main-parking-2026-03-24",
            "",
            "worktree D:/zWenbo/AI/wt/f34-post-h59-archive-and-reopen-screen",
            "HEAD cafe1234",
            "branch refs/heads/wip/f34-post-h59-archive-and-reopen-screen",
            "",
        ]
    )

    original_out_dir = module.OUT_DIR
    original_root = module.ROOT
    original_git_output = module.git_output
    temp_root = tmp_path / "f34-post-h59-archive-and-reopen-screen"
    temp_root.mkdir(parents=True, exist_ok=True)
    temp_out_dir = tmp_path / "P43_post_h59_repo_graph_hygiene_and_merge_map"
    module.OUT_DIR = temp_out_dir
    module.ROOT = temp_root
    module.git_output = lambda args: (
        "wip/f34-post-h59-archive-and-reopen-screen\n"
        if args == ["rev-parse", "--abbrev-ref", "HEAD"]
        else sample_worktree_list
    )
    try:
        module.main()
    finally:
        module.OUT_DIR = original_out_dir
        module.ROOT = original_root
        module.git_output = original_git_output

    payload = json.loads((temp_out_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload["summary"]["merge_posture"] == "clean_descendant_only_never_dirty_root_main"
    assert payload["summary"]["root_main_quarantined"] is True
    assert payload["summary"]["repo_local_alias_count"] == 1
