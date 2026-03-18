from __future__ import annotations

from dataclasses import dataclass

from .ir import BytecodeOpcode, BytecodeProgram
from .types import BytecodeType


@dataclass(frozen=True, slots=True)
class ControlFrame:
    return_pc: int
    call_target: int


@dataclass(frozen=True, slots=True)
class ControlState:
    pc: int
    frames: tuple[ControlFrame, ...] = ()


@dataclass(frozen=True, slots=True)
class VerifierResult:
    program_name: str
    passed: bool
    first_error_pc: int | None
    error_class: str | None
    expected_stack: tuple[str, ...]
    actual_stack: tuple[str, ...]
    message: str


def _stack_names(stack: tuple[BytecodeType, ...]) -> tuple[str, ...]:
    return tuple(item.value for item in stack)


def _fail(
    program: BytecodeProgram,
    *,
    pc: int,
    error_class: str,
    expected_stack: tuple[BytecodeType, ...],
    actual_stack: tuple[BytecodeType, ...],
    message: str,
) -> VerifierResult:
    return VerifierResult(
        program_name=program.name,
        passed=False,
        first_error_pc=pc,
        error_class=error_class,
        expected_stack=_stack_names(expected_stack),
        actual_stack=_stack_names(actual_stack),
        message=message,
    )


def _transfer(program: BytecodeProgram, *, pc: int, stack: tuple[BytecodeType, ...]):
    instruction = program.instructions[pc]
    opcode = instruction.opcode

    if opcode in {BytecodeOpcode.CONST_I32, BytecodeOpcode.CONST_ADDR} and instruction.arg is None:
        return (), _fail(
            program,
            pc=pc,
            error_class="missing_arg",
            expected_stack=(),
            actual_stack=stack,
            message=f"{opcode.value} requires an integer argument.",
        )
    if opcode in {BytecodeOpcode.LOAD_STATIC, BytecodeOpcode.STORE_STATIC}:
        if instruction.arg is None:
            return (), _fail(
                program,
                pc=pc,
                error_class="missing_arg",
                expected_stack=(),
                actual_stack=stack,
                message=f"{opcode.value} requires a non-negative static address.",
            )
        if instruction.arg < 0:
            return (), _fail(
                program,
                pc=pc,
                error_class="static_address",
                expected_stack=(),
                actual_stack=stack,
                message=f"{opcode.value} expects a non-negative static address.",
            )
    if opcode in {BytecodeOpcode.JMP, BytecodeOpcode.JZ_ZERO}:
        if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
            return (), _fail(
                program,
                pc=pc,
                error_class="branch_target",
                expected_stack=(),
                actual_stack=stack,
                message=f"{opcode.value} target must stay within program bounds.",
            )
    if opcode == BytecodeOpcode.CALL:
        if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
            return (), _fail(
                program,
                pc=pc,
                error_class="call_target",
                expected_stack=(),
                actual_stack=stack,
                message="call target must stay within program bounds.",
            )

    if opcode == BytecodeOpcode.DUP:
        if not stack:
            return (), _fail(
                program,
                pc=pc,
                error_class="stack_underflow",
                expected_stack=(BytecodeType.I32,),
                actual_stack=stack,
                message="dup requires at least one stack value.",
            )
        return (((pc + 1, stack + (stack[-1],)),), None)

    if opcode == BytecodeOpcode.POP:
        if not stack:
            return (), _fail(
                program,
                pc=pc,
                error_class="stack_underflow",
                expected_stack=(BytecodeType.I32,),
                actual_stack=stack,
                message="pop requires at least one stack value.",
            )
        return (((pc + 1, stack[:-1]),), None)

    if len(stack) < len(instruction.in_types):
        return (), _fail(
            program,
            pc=pc,
            error_class="stack_underflow",
            expected_stack=instruction.in_types,
            actual_stack=stack,
            message=f"{opcode.value} requires stack suffix {', '.join(item.value for item in instruction.in_types)}.",
        )

    actual_suffix = stack[-len(instruction.in_types) :] if instruction.in_types else ()
    if instruction.in_types and actual_suffix != instruction.in_types:
        return (), _fail(
            program,
            pc=pc,
            error_class="type_mismatch",
            expected_stack=instruction.in_types,
            actual_stack=actual_suffix,
            message=f"{opcode.value} expected {', '.join(item.value for item in instruction.in_types)}.",
        )

    base_stack = stack[: len(stack) - len(instruction.in_types)] if instruction.in_types else stack
    next_stack = base_stack + instruction.out_types

    if opcode == BytecodeOpcode.HALT:
        return (), None
    if opcode == BytecodeOpcode.CALL:
        return (((instruction.arg, next_stack),), None)
    if opcode == BytecodeOpcode.RET:
        return (((pc + 1, next_stack),), None)

    if opcode == BytecodeOpcode.JMP:
        return (((instruction.arg, next_stack),), None)
    if opcode == BytecodeOpcode.JZ_ZERO:
        return (((pc + 1, next_stack), (instruction.arg, next_stack)), None)

    return (((pc + 1, next_stack),), None)


def verify_program(program: BytecodeProgram) -> VerifierResult:
    if not program.instructions:
        return VerifierResult(
            program_name=program.name,
            passed=False,
            first_error_pc=None,
            error_class="empty_program",
            expected_stack=(),
            actual_stack=(),
            message="bytecode program must contain at least one instruction.",
        )

    incoming: dict[ControlState, tuple[BytecodeType, ...]] = {ControlState(0): ()}
    worklist: list[ControlState] = [ControlState(0)]
    halted_reachable = False

    while worklist:
        state = min(
            worklist,
            key=lambda item: (item.pc, tuple((frame.return_pc, frame.call_target) for frame in item.frames)),
        )
        worklist.remove(state)
        pc = state.pc
        stack = incoming[state]
        instruction = program.instructions[pc]

        if instruction.opcode == BytecodeOpcode.CALL:
            if instruction.arg is None or not (0 <= instruction.arg < len(program.instructions)):
                return _fail(
                    program,
                    pc=pc,
                    error_class="call_target",
                    expected_stack=(),
                    actual_stack=stack,
                    message="call target must stay within program bounds.",
                )
            active_targets = {frame.call_target for frame in state.frames}
            if instruction.arg in active_targets:
                return _fail(
                    program,
                    pc=pc,
                    error_class="recursive_call",
                    expected_stack=(),
                    actual_stack=stack,
                    message="recursive or mutually recursive call cycles are out of scope.",
                )
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            next_frames = state.frames + (ControlFrame(return_pc=pc + 1, call_target=instruction.arg),)
            stacked_transitions = tuple(
                (ControlState(target_pc, next_frames), target_stack) for target_pc, target_stack in transitions
            )
        elif instruction.opcode == BytecodeOpcode.RET:
            if not state.frames:
                return _fail(
                    program,
                    pc=pc,
                    error_class="empty_return",
                    expected_stack=(),
                    actual_stack=stack,
                    message="ret requires one pending call frame.",
                )
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            return_pc = state.frames[-1].return_pc
            next_frames = state.frames[:-1]
            stacked_transitions = ((ControlState(return_pc, next_frames), transitions[0][1]),)
        elif instruction.opcode == BytecodeOpcode.HALT:
            if state.frames:
                return _fail(
                    program,
                    pc=pc,
                    error_class="unterminated_frame",
                    expected_stack=(),
                    actual_stack=stack,
                    message="halt is only valid when the call stack is empty.",
                )
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            stacked_transitions = ()
        else:
            transitions, error = _transfer(program, pc=pc, stack=stack)
            if error is not None:
                return error
            stacked_transitions = tuple((ControlState(target_pc, state.frames), target_stack) for target_pc, target_stack in transitions)

        if not stacked_transitions:
            halted_reachable = True
            continue

        for target_state, target_stack in stacked_transitions:
            previous = incoming.get(target_state)
            if previous is None:
                incoming[target_state] = target_stack
                worklist.append(target_state)
                continue
            if previous != target_stack:
                return _fail(
                    program,
                    pc=target_state.pc,
                    error_class="stack_join_mismatch",
                    expected_stack=previous,
                    actual_stack=target_stack,
                    message="control-flow join requires one consistent stack typing.",
                )

    if not halted_reachable:
        return VerifierResult(
            program_name=program.name,
            passed=False,
            first_error_pc=None,
            error_class="no_halt",
            expected_stack=(),
            actual_stack=(),
            message="bytecode program has no reachable halt.",
        )

    return VerifierResult(
        program_name=program.name,
        passed=True,
        first_error_pc=None,
        error_class=None,
        expected_stack=(),
        actual_stack=(),
        message="ok",
    )
