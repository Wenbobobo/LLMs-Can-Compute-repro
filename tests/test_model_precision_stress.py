from __future__ import annotations

from model.precision_stress import check_precision_range


def test_float64_and_float32_pass_small_exhaustive_ranges() -> None:
    for fmt in ("float64", "float32"):
        assert check_precision_range(64, fmt=fmt, kind="identity", mode="exhaustive").passed is True
        assert check_precision_range(64, fmt=fmt, kind="latest_write", mode="exhaustive").passed is True


def test_bfloat16_breaks_identity_retrieval_early() -> None:
    result = check_precision_range(32, fmt="bfloat16", kind="identity", mode="exhaustive")

    assert result.passed is False
    assert result.first_failure is not None
    assert result.first_failure.query_address == 16


def test_float16_breaks_latest_write_tie_break_early() -> None:
    result = check_precision_range(16, fmt="float16", kind="latest_write", mode="exhaustive")

    assert result.passed is False
    assert result.first_failure is not None
    assert result.first_failure.query_address == 8
