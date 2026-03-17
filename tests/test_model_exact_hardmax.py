from __future__ import annotations

import random
from fractions import Fraction

from exec_trace import TraceInterpreter, latest_write_program, memory_accumulator_program
from model import (
    LatestWriteDecodeConfig,
    MemoryOperation,
    encode_latest_write_key,
    encode_latest_write_query,
    extract_memory_operations,
    run_latest_write_decode,
)


def test_latest_write_key_encoding_prefers_exact_match_then_latest_step() -> None:
    epsilon = Fraction(1, 200)
    query = encode_latest_write_query(3)
    exact_old = encode_latest_write_key(3, 1, epsilon)
    exact_new = encode_latest_write_key(3, 5, epsilon)
    wrong_addr = encode_latest_write_key(2, 100, epsilon)

    score_exact_old = (query[0] * exact_old[0]) + exact_old[1]
    score_exact_new = (query[0] * exact_new[0]) + exact_new[1]
    score_wrong_addr = (query[0] * wrong_addr[0]) + wrong_addr[1]

    assert score_exact_new > score_exact_old
    assert score_exact_old > score_wrong_addr


def test_latest_write_decode_matches_trace_example() -> None:
    interpreter = TraceInterpreter()
    result = interpreter.run(latest_write_program())

    decode_run = run_latest_write_decode(
        extract_memory_operations(result.events),
        LatestWriteDecodeConfig(max_steps=result.final_state.steps, addresses=(0,)),
    )

    assert len(decode_run.observations) == 1
    observation = decode_run.observations[0]
    assert observation.expected_value == 9
    assert observation.linear_value == 9
    assert observation.accelerated_value == 9


def test_latest_write_decode_matches_multi_slot_trace_example() -> None:
    interpreter = TraceInterpreter()
    result = interpreter.run(memory_accumulator_program())

    decode_run = run_latest_write_decode(
        extract_memory_operations(result.events),
        LatestWriteDecodeConfig(max_steps=result.final_state.steps, addresses=(0, 1, 2)),
    )

    observed = [obs.expected_value for obs in decode_run.observations]
    linear = [obs.linear_value for obs in decode_run.observations]
    accelerated = [obs.accelerated_value for obs in decode_run.observations]

    assert observed == [7, 5, 12]
    assert linear == observed
    assert accelerated == observed


def test_latest_write_decode_modes_match_random_operation_stream() -> None:
    rng = random.Random(0)
    addresses = (0, 1, 2, 3)
    operations = []
    last_values = {address: 0 for address in addresses}

    for step in range(1, 80):
        if rng.random() < 0.6:
            address = rng.choice(addresses)
            value = rng.randint(-20, 20)
            last_values[address] = value
            operations.append(("store", step, address, value))
        else:
            address = rng.choice(addresses)
            operations.append(("load", step, address, last_values[address]))

    decode_run = run_latest_write_decode(
        [
            MemoryOperation(step=step, kind=kind, address=address, value=value)
            for kind, step, address, value in operations
        ],
        LatestWriteDecodeConfig(max_steps=80, addresses=addresses),
    )

    for observation in decode_run.observations:
        assert observation.linear_value == observation.expected_value
        assert observation.accelerated_value == observation.expected_value
