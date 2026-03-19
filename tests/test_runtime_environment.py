from __future__ import annotations

from pathlib import Path

from utils.runtime_env import _detect_virtual_env


def test_detect_virtual_env_prefers_explicit_environment(monkeypatch, tmp_path: Path) -> None:
    explicit = tmp_path / "explicit-venv"
    monkeypatch.setenv("VIRTUAL_ENV", str(explicit))
    monkeypatch.setattr("sys.prefix", str(tmp_path / "ignored-prefix"))
    monkeypatch.setattr("sys.base_prefix", str(tmp_path / "ignored-base"))

    assert _detect_virtual_env() == str(explicit)


def test_detect_virtual_env_falls_back_to_sys_prefix(monkeypatch, tmp_path: Path) -> None:
    prefix = tmp_path / ".venv"
    prefix.mkdir()
    (prefix / "pyvenv.cfg").write_text("home = ignored\n", encoding="utf-8")

    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.setattr("sys.prefix", str(prefix))
    monkeypatch.setattr("sys.base_prefix", str(tmp_path / "base-python"))

    assert _detect_virtual_env() == str(prefix)


def test_detect_virtual_env_returns_none_without_signal(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.setattr("sys.prefix", str(tmp_path / "base-python"))
    monkeypatch.setattr("sys.base_prefix", str(tmp_path / "base-python"))

    assert _detect_virtual_env() is None
