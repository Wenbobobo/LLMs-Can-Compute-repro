from __future__ import annotations

import random
from fractions import Fraction

from exec_trace import (
    TraceInterpreter,
    call_chain_program,
    countdown_program,
    dynamic_memory_program,
    latest_write_program,
    memory_accumulator_program,
)
from model import (
    LatestWriteDecodeConfig,
    MemoryOperation,
    encode_latest_write_key,
    encode_latest_write_query,
    extract_call_frame_operations,
    extract_memory_operations,
    extract_stack_slot_operations,
    run_latest_write_decode,
    run_latest_write_decode_for_call_events,
    run_latest_write_decode_for_stack_events,
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
    assert [row.label for row in decode_run.candidate_rows] == [
        "default:memory:a0",
        "store:memory:a0:s1:r1",
        "store:memory:a0:s3:r2",
    ]
    assert observation.linear_maximizer_indices == (2,)
    assert observation.accelerated_maximizer_indices == (2,)


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


def test_latest_write_decode_matches_dynamic_address_trace_example() -> None:
    interpreter = TraceInterpreter()
    result = interpreter.run(dynamic_memory_program())

    decode_run = run_latest_write_decode(
        extract_memory_operations(result.events),
        LatestWriteDecodeConfig(max_steps=result.final_state.steps, addresses=(2,)),
    )

    observed = [obs.expected_value for obs in decode_run.observations]
    linear = [obs.linear_value for obs in decode_run.observations]
    accelerated = [obs.accelerated_value for obs in decode_run.observations]

    assert observed == [11, 11]
    assert linear == observed
    assert accelerated == observed


def test_stack_slot_decode_matches_countdown_trace_example() -> None:
    interpreter = TraceInterpreter()
    result = interpreter.run(countdown_program(4))

    operations = extract_stack_slot_operations(result.events)
    assert any(operation.kind == "load" for operation in operations)
    assert any(operation.kind == "store" for operation in operations)

    decode_run = run_latest_write_decode_for_stack_events(result.events)

    observed = [(obs.address, obs.expected_value) for obs in decode_run.observations[:6]]
    linear = [(obs.address, obs.linear_value) for obs in decode_run.observations[:6]]
    accelerated = [(obs.address, obs.accelerated_value) for obs in decode_run.observations[:6]]

    assert observed == [(1, 4), (0, 4), (1, 1), (1, 3), (0, 3), (1, 1)]
    assert linear == observed
    assert accelerated == observed


def test_stack_slot_decode_matches_dynamic_memory_trace_example() -> None:
    interpreter = TraceInterpreter()
    result = interpreter.run(dynamic_memory_program())

    decode_run = run_latest_write_decode_for_stack_events(result.events)

    assert len(decode_run.observations) > 0
    for observation in decode_run.observations:
        assert observation.linear_value == observation.expected_value
        assert observation.accelerated_value == observation.expected_value


def test_call_frame_decode_matches_call_chain_trace_example() -> None:
    interpreter = TraceInterpreter()
    result = interpreter.run(call_chain_program())

    operations = extract_call_frame_operations(result.events)
    assert [operation.kind for operation in operations] == ["store", "store", "load", "load"]

    decode_run = run_latest_write_decode_for_call_events(result.events)
    observed = [(obs.address, obs.expected_value) for obs in decode_run.observations]
    accelerated = [(obs.address, obs.accelerated_value) for obs in decode_run.observations]

    assert observed == [(1, 7), (0, 3)]
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


def test_latest_write_decode_records_duplicate_row_identity_ties() -> None:
    decode_run = run_latest_write_decode(
        (
            MemoryOperation(step=0, kind="store", address=5, value=3),
            MemoryOperation(step=0, kind="store", address=5, value=7),
            MemoryOperation(step=1, kind="load", address=5, value=5),
        ),
        LatestWriteDecodeConfig(max_steps=1, addresses=(5,)),
    )

    observation = decode_run.observations[0]

    assert observation.expected_value == 5
    assert observation.linear_value == 5
    assert observation.accelerated_value == 5
    assert observation.linear_maximizer_indices == (1, 2)
    assert observation.accelerated_maximizer_indices == (1, 2)
    assert [row.label for row in decode_run.candidate_rows] == [
        "default:memory:a5",
        "store:memory:a5:s0:r1",
        "store:memory:a5:s0:r2",
    ]
