"""Runtime environment inspection helpers for reproducible experiment exports."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import importlib.util
import os
import platform
import shutil
import subprocess
import sys


@dataclass(frozen=True, slots=True)
class PythonRuntimeInfo:
    executable: str
    version: str
    implementation: str
    platform: str
    virtual_env: str | None


@dataclass(frozen=True, slots=True)
class TorchDeviceInfo:
    index: int
    name: str
    capability: tuple[int, int] | None
    total_memory_bytes: int | None


@dataclass(frozen=True, slots=True)
class TorchRuntimeInfo:
    installed: bool
    version: str | None
    cuda_version: str | None
    cuda_available: bool
    device_count: int
    devices: tuple[TorchDeviceInfo, ...]


@dataclass(frozen=True, slots=True)
class RuntimeEnvironment:
    python: PythonRuntimeInfo
    torch: TorchRuntimeInfo
    uv_version: str | None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _detect_virtual_env() -> str | None:
    explicit = os.environ.get("VIRTUAL_ENV")
    if explicit:
        return explicit

    prefix = Path(sys.prefix)
    base_prefix = Path(getattr(sys, "base_prefix", sys.prefix))
    if prefix != base_prefix and (prefix / "pyvenv.cfg").exists():
        return str(prefix)

    return None


def _detect_uv_version() -> str | None:
    if shutil.which("uv") is None:
        return None
    try:
        completed = subprocess.run(
            ["uv", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    return completed.stdout.strip() or None


def _detect_torch() -> TorchRuntimeInfo:
    if importlib.util.find_spec("torch") is None:
        return TorchRuntimeInfo(
            installed=False,
            version=None,
            cuda_version=None,
            cuda_available=False,
            device_count=0,
            devices=(),
        )

    import torch  # pragma: no cover - depends on local runtime

    cuda_available = bool(torch.cuda.is_available())
    devices: list[TorchDeviceInfo] = []
    if cuda_available:
        for index in range(torch.cuda.device_count()):
            properties = torch.cuda.get_device_properties(index)
            devices.append(
                TorchDeviceInfo(
                    index=index,
                    name=properties.name,
                    capability=getattr(properties, "major", None) is not None
                    and (properties.major, properties.minor)
                    or None,
                    total_memory_bytes=getattr(properties, "total_memory", None),
                )
            )

    return TorchRuntimeInfo(
        installed=True,
        version=torch.__version__,
        cuda_version=torch.version.cuda,
        cuda_available=cuda_available,
        device_count=torch.cuda.device_count() if cuda_available else 0,
        devices=tuple(devices),
    )


def detect_runtime_environment() -> RuntimeEnvironment:
    return RuntimeEnvironment(
        python=PythonRuntimeInfo(
            executable=sys.executable,
            version=sys.version,
            implementation=platform.python_implementation(),
            platform=platform.platform(),
            virtual_env=_detect_virtual_env(),
        ),
        torch=_detect_torch(),
        uv_version=_detect_uv_version(),
    )


def project_virtual_env(root: str | Path | None = None) -> Path:
    base = Path(root) if root is not None else Path.cwd()
    return base / ".venv"
