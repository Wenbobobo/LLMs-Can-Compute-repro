"""Model-side experimental branches for the reproduction project."""

from .exact_hardmax import (
    config_for_operations,
    DecodeObservation,
    DecodeRun,
    LatestWriteDecodeConfig,
    MemoryOperation,
    encode_latest_write_key,
    encode_latest_write_query,
    extract_memory_operations,
    run_latest_write_decode,
    run_latest_write_decode_for_events,
)

__all__ = [
    "config_for_operations",
    "DecodeObservation",
    "DecodeRun",
    "LatestWriteDecodeConfig",
    "MemoryOperation",
    "encode_latest_write_key",
    "encode_latest_write_query",
    "extract_memory_operations",
    "run_latest_write_decode",
    "run_latest_write_decode_for_events",
]
