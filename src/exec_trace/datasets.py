"""Small deterministic programs for the trace milestone."""

from __future__ import annotations

from .dsl import Instruction, Opcode, Program


def countdown_program(start: int) -> Program:
    if start < 0:
        raise ValueError("countdown_program expects a non-negative start.")

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 6),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.JMP, 1),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name=f"countdown_{start}")


def equality_branch_program(lhs: int, rhs: int) -> Program:
    instructions = (
        Instruction(Opcode.PUSH_CONST, lhs),
        Instruction(Opcode.PUSH_CONST, rhs),
        Instruction(Opcode.EQ),
        Instruction(Opcode.JZ, 6),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.HALT),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name=f"eq_{lhs}_{rhs}")


def call_chain_program() -> Program:
    """Exercise nested call/return control flow on the tiny stack machine."""

    instructions = (
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.CALL, 4),
        Instruction(Opcode.HALT),
        Instruction(Opcode.ADD),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.CALL, 8),
        Instruction(Opcode.RET),
        Instruction(Opcode.ADD),
        Instruction(Opcode.RET),
    )
    return Program(instructions=instructions, name="call_chain")


def latest_write_program() -> Program:
    """Overwrite one address and read it back to expose last-write semantics."""

    instructions = (
        Instruction(Opcode.PUSH_CONST, 7),
        Instruction(Opcode.STORE, 0),
        Instruction(Opcode.PUSH_CONST, 9),
        Instruction(Opcode.STORE, 0),
        Instruction(Opcode.LOAD, 0),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name="latest_write")


def memory_accumulator_program() -> Program:
    """Write, read, and combine two explicit memory slots."""

    instructions = (
        Instruction(Opcode.PUSH_CONST, 7),
        Instruction(Opcode.STORE, 0),
        Instruction(Opcode.PUSH_CONST, 5),
        Instruction(Opcode.STORE, 1),
        Instruction(Opcode.LOAD, 0),
        Instruction(Opcode.LOAD, 1),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE, 2),
        Instruction(Opcode.LOAD, 2),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name="memory_accumulator")


def dynamic_memory_program() -> Program:
    """Use runtime-computed addresses for reads and writes."""

    instructions = (
        Instruction(Opcode.PUSH_CONST, 7),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 11),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name="dynamic_memory")


def dynamic_latest_write_program() -> Program:
    """Exercise indirect latest-write behavior on one runtime-computed address."""

    instructions = (
        Instruction(Opcode.PUSH_CONST, 13),
        Instruction(Opcode.PUSH_CONST, 4),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 17),
        Instruction(Opcode.PUSH_CONST, 4),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 4),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name="dynamic_latest_write")


def dynamic_memory_transfer_program() -> Program:
    """Read two indirect addresses, combine them, and write the result back indirectly."""

    instructions = (
        Instruction(Opcode.PUSH_CONST, 4),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 9),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.ADD),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name="dynamic_memory_transfer")


def loop_indirect_memory_program(
    start: int,
    *,
    counter_address: int = 4,
    accumulator_address: int = 5,
) -> Program:
    """Loop over an indirect counter and accumulate through indirect memory reads/writes."""

    if start < 0:
        raise ValueError("loop_indirect_memory_program expects a non-negative start.")
    if counter_address < 0 or accumulator_address < 0:
        raise ValueError("loop_indirect_memory_program expects non-negative addresses.")

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.PUSH_CONST, counter_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.PUSH_CONST, accumulator_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, counter_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 22),
        Instruction(Opcode.PUSH_CONST, accumulator_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.ADD),
        Instruction(Opcode.PUSH_CONST, accumulator_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, counter_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.PUSH_CONST, counter_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.JMP, 6),
        Instruction(Opcode.POP),
        Instruction(Opcode.PUSH_CONST, accumulator_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.HALT),
    )
    return Program(
        instructions=instructions,
        name=f"loop_indirect_memory_{start}_a{counter_address}_b{accumulator_address}",
    )


def stack_memory_ping_pong_program(*, base_address: int = 0) -> Program:
    """Bounce values between stack and memory to stress mixed latest-write state."""

    if base_address < 0:
        raise ValueError("stack_memory_ping_pong_program expects a non-negative base address.")

    address0 = base_address
    address1 = base_address + 1
    address2 = base_address + 2
    instructions = (
        Instruction(Opcode.PUSH_CONST, 4),
        Instruction(Opcode.STORE, address0),
        Instruction(Opcode.PUSH_CONST, 9),
        Instruction(Opcode.STORE, address1),
        Instruction(Opcode.LOAD, address0),
        Instruction(Opcode.LOAD, address1),
        Instruction(Opcode.ADD),
        Instruction(Opcode.DUP),
        Instruction(Opcode.STORE, address2),
        Instruction(Opcode.PUSH_CONST, address2),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.ADD),
        Instruction(Opcode.DUP),
        Instruction(Opcode.STORE, address0),
        Instruction(Opcode.LOAD, address0),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT),
    )
    return Program(instructions=instructions, name=f"stack_memory_ping_pong_a{base_address}")


def alternating_memory_loop_program(start: int, *, base_address: int = 0) -> Program:
    """Alternate between two accumulators under a memory-stored branch flag."""

    if start < 0:
        raise ValueError("alternating_memory_loop_program expects a non-negative start.")
    if base_address < 0:
        raise ValueError("alternating_memory_loop_program expects a non-negative base address.")

    counter_address = base_address
    flag_address = base_address + 1
    left_address = base_address + 2
    right_address = base_address + 3

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, left_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, right_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 32),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, flag_address),
        Instruction(Opcode.JZ, 21),
        Instruction(Opcode.LOAD, right_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE, right_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.JMP, 27),
        Instruction(Opcode.LOAD, left_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE, left_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.JMP, 8),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, left_address),
        Instruction(Opcode.LOAD, right_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT),
    )
    return Program(
        instructions=instructions,
        name=f"alternating_memory_loop_{start}_a{base_address}",
    )


def flagged_indirect_accumulator_program(start: int, *, base_address: int = 0) -> Program:
    """Accumulate into alternating indirect targets selected by a memory-stored flag."""

    if start < 0:
        raise ValueError("flagged_indirect_accumulator_program expects a non-negative start.")
    if base_address < 0:
        raise ValueError("flagged_indirect_accumulator_program expects a non-negative base address.")

    counter_address = base_address
    flag_address = base_address + 1
    left_slot_address = base_address + 2
    right_slot_address = base_address + 3
    left_address = base_address + 4
    right_address = base_address + 5

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.PUSH_CONST, left_address),
        Instruction(Opcode.STORE, left_slot_address),
        Instruction(Opcode.PUSH_CONST, right_address),
        Instruction(Opcode.STORE, right_slot_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, left_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, right_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 40),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, flag_address),
        Instruction(Opcode.JZ, 27),
        Instruction(Opcode.LOAD, right_slot_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.LOAD, right_slot_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.JMP, 35),
        Instruction(Opcode.LOAD, left_slot_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.LOAD, left_slot_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.JMP, 12),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, left_address),
        Instruction(Opcode.LOAD, right_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT),
    )
    return Program(
        instructions=instructions,
        name=f"flagged_indirect_accumulator_{start}_a{base_address}",
    )


def selector_checkpoint_bank_program(start: int, *, base_address: int = 0) -> Program:
    """Cycle across three banks through a checkpointed target-address slot."""

    if start < 0:
        raise ValueError("selector_checkpoint_bank_program expects a non-negative start.")
    if base_address < 0:
        raise ValueError("selector_checkpoint_bank_program expects a non-negative base address.")

    counter_address = base_address
    selector_address = base_address + 1
    checkpoint_address = base_address + 2
    bank0_slot_address = base_address + 3
    bank1_slot_address = base_address + 4
    bank2_slot_address = base_address + 5
    bank0_address = base_address + 6
    bank1_address = base_address + 7
    bank2_address = base_address + 8

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, selector_address),
        Instruction(Opcode.PUSH_CONST, bank0_address),
        Instruction(Opcode.STORE, bank0_slot_address),
        Instruction(Opcode.PUSH_CONST, bank1_address),
        Instruction(Opcode.STORE, bank1_slot_address),
        Instruction(Opcode.PUSH_CONST, bank2_address),
        Instruction(Opcode.STORE, bank2_slot_address),
        Instruction(Opcode.PUSH_CONST, bank0_address),
        Instruction(Opcode.STORE, checkpoint_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, bank0_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, bank1_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, bank2_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 63),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, selector_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 31),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.EQ),
        Instruction(Opcode.JZ, 35),
        Instruction(Opcode.LOAD, bank1_slot_address),
        Instruction(Opcode.STORE, checkpoint_address),
        Instruction(Opcode.JMP, 37),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, bank0_slot_address),
        Instruction(Opcode.STORE, checkpoint_address),
        Instruction(Opcode.JMP, 37),
        Instruction(Opcode.LOAD, bank2_slot_address),
        Instruction(Opcode.STORE, checkpoint_address),
        Instruction(Opcode.LOAD, checkpoint_address),
        Instruction(Opcode.LOAD_AT),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.LOAD, checkpoint_address),
        Instruction(Opcode.STORE_AT),
        Instruction(Opcode.LOAD, selector_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 52),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.EQ),
        Instruction(Opcode.JZ, 56),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.STORE, selector_address),
        Instruction(Opcode.JMP, 58),
        Instruction(Opcode.POP),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.STORE, selector_address),
        Instruction(Opcode.JMP, 58),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, selector_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.JMP, 18),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, bank0_address),
        Instruction(Opcode.LOAD, bank1_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.LOAD, bank2_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT),
    )
    return Program(
        instructions=instructions,
        name=f"selector_checkpoint_bank_{start}_a{base_address}",
    )


def hotspot_memory_rewrite_program(start: int, *, base_address: int = 0) -> Program:
    """Rewrite a small hotspot bank repeatedly to stress stale-read behavior."""

    if start < 0:
        raise ValueError("hotspot_memory_rewrite_program expects a non-negative start.")
    if base_address < 0:
        raise ValueError("hotspot_memory_rewrite_program expects a non-negative base address.")

    counter_address = base_address
    flag_address = base_address + 1
    hot0_address = base_address + 2
    hot1_address = base_address + 3
    hot2_address = base_address + 4

    instructions = (
        Instruction(Opcode.PUSH_CONST, start),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.STORE, hot0_address),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.STORE, hot1_address),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.STORE, hot2_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 46),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, flag_address),
        Instruction(Opcode.DUP),
        Instruction(Opcode.JZ, 27),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.EQ),
        Instruction(Opcode.JZ, 35),
        Instruction(Opcode.LOAD, hot1_address),
        Instruction(Opcode.LOAD, hot2_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE, hot1_address),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.JMP, 41),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, hot0_address),
        Instruction(Opcode.LOAD, hot1_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE, hot0_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.JMP, 41),
        Instruction(Opcode.LOAD, hot2_address),
        Instruction(Opcode.LOAD, hot0_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE, hot2_address),
        Instruction(Opcode.PUSH_CONST, 0),
        Instruction(Opcode.STORE, flag_address),
        Instruction(Opcode.LOAD, counter_address),
        Instruction(Opcode.PUSH_CONST, 1),
        Instruction(Opcode.SUB),
        Instruction(Opcode.STORE, counter_address),
        Instruction(Opcode.JMP, 10),
        Instruction(Opcode.POP),
        Instruction(Opcode.LOAD, hot0_address),
        Instruction(Opcode.LOAD, hot1_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.LOAD, hot2_address),
        Instruction(Opcode.ADD),
        Instruction(Opcode.HALT),
    )
    return Program(
        instructions=instructions,
        name=f"hotspot_memory_rewrite_{start}_a{base_address}",
    )


def stack_fanout_sum_program(depth: int, *, base_value: int = 1) -> Program:
    """Build a deep stack fanout and reduce it back through straight-line adds."""

    if depth <= 0:
        raise ValueError("stack_fanout_sum_program expects a positive depth.")

    instructions = tuple(Instruction(Opcode.PUSH_CONST, base_value) for _ in range(depth)) + tuple(
        Instruction(Opcode.ADD) for _ in range(depth - 1)
    ) + (Instruction(Opcode.HALT),)
    return Program(
        instructions=instructions,
        name=f"stack_fanout_sum_{depth}_v{base_value}",
    )
