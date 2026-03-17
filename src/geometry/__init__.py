"""Geometry primitives for exact 2D hard-max retrieval."""

from .hardmax import HardmaxResult, brute_force_hardmax_2d
from .hull_kv import HullKVCache

__all__ = ["HardmaxResult", "HullKVCache", "brute_force_hardmax_2d"]
