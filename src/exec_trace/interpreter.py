"""Reference interpreter for the append-only stack-machine trace DSL."""

from __future__ import annotations

from .dsl import ExecutionResult, ExecutionState, Instruction, Opcode, Program, TraceEvent


class TraceInterpreter:
    """Reference semantics for the first executor milestone."""

    def run(self, program: Program, max_steps: int = 10_000) -> ExecutionResult:
        state = ExecutionState()
        events: list[TraceEvent] = []

        while not state.halted:
            if state.steps >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= state.pc < len(program)):
                raise RuntimeError(f"Program counter out of range: {state.pc}")

            instruction = program.instructions[state.pc]
            event, state = self._step(state, instruction)
            events.append(event)

        return ExecutionResult(program=program, events=tuple(events), final_state=state)

    def _step(self, state: ExecutionState, instruction: Instruction) -> tuple[TraceEvent, ExecutionState]:
        stack = list(state.stack)
        memory = dict(state.memory)
        popped: tuple[int, ...] = ()
        pushed: tuple[int, ...] = ()
        branch_taken: bool | None = None
        memory_read_address: int | None = None
        memory_read_value: int | None = None
        memory_write: tuple[int, int] | None = None
        next_pc = state.pc + 1
        halted = False

        match instruction.opcode:
            case Opcode.PUSH_CONST:
                if instruction.arg is None:
                    raise RuntimeError("push_const requires an integer argument.")
                pushed = (instruction.arg,)
                stack.append(instruction.arg)
            case Opcode.ADD:
                lhs, rhs = self._pop_binary(stack, instruction.opcode)
                result = lhs + rhs
                popped = (lhs, rhs)
                pushed = (result,)
                stack.append(result)
            case Opcode.SUB:
                lhs, rhs = self._pop_binary(stack, instruction.opcode)
                result = lhs - rhs
                popped = (lhs, rhs)
                pushed = (result,)
                stack.append(result)
            case Opcode.EQ:
                lhs, rhs = self._pop_binary(stack, instruction.opcode)
                result = int(lhs == rhs)
                popped = (lhs, rhs)
                pushed = (result,)
                stack.append(result)
            case Opcode.DUP:
                if not stack:
                    raise RuntimeError("dup requires at least one stack element.")
                pushed = (stack[-1],)
                stack.append(stack[-1])
            case Opcode.POP:
                if not stack:
                    raise RuntimeError("pop requires at least one stack element.")
                popped = (stack.pop(),)
            case Opcode.LOAD:
                if instruction.arg is None:
                    raise RuntimeError("load requires an integer address.")
                if instruction.arg < 0:
                    raise RuntimeError("load address must be non-negative.")
                memory_read_address = instruction.arg
                memory_read_value = memory.get(instruction.arg, 0)
                pushed = (memory_read_value,)
                stack.append(memory_read_value)
            case Opcode.STORE:
                if instruction.arg is None:
                    raise RuntimeError("store requires an integer address.")
                if instruction.arg < 0:
                    raise RuntimeError("store address must be non-negative.")
                if not stack:
                    raise RuntimeError("store requires a value on the stack.")
                value = stack.pop()
                popped = (value,)
                memory[instruction.arg] = value
                memory_write = (instruction.arg, value)
            case Opcode.JMP:
                if instruction.arg is None:
                    raise RuntimeError("jmp requires a target PC.")
                branch_taken = True
                next_pc = instruction.arg
            case Opcode.JZ:
                if instruction.arg is None:
                    raise RuntimeError("jz requires a target PC.")
                if not stack:
                    raise RuntimeError("jz requires a condition value on the stack.")
                condition = stack.pop()
                popped = (condition,)
                branch_taken = condition == 0
                next_pc = instruction.arg if branch_taken else state.pc + 1
            case Opcode.HALT:
                halted = True
                next_pc = state.pc
            case _:
                raise RuntimeError(f"Unsupported opcode: {instruction.opcode}")

        event = TraceEvent(
            step=state.steps,
            pc=state.pc,
            opcode=instruction.opcode,
            arg=instruction.arg,
            popped=popped,
            pushed=pushed,
            branch_taken=branch_taken,
            memory_read_address=memory_read_address,
            memory_read_value=memory_read_value,
            memory_write=memory_write,
            next_pc=next_pc,
            stack_depth_before=len(state.stack),
            stack_depth_after=len(stack),
            halted=halted,
        )
        next_state = ExecutionState(
            pc=next_pc,
            stack=tuple(stack),
            memory=tuple(sorted(memory.items())),
            halted=halted,
            steps=state.steps + 1,
        )
        return (event, next_state)

    @staticmethod
    def _pop_binary(stack: list[int], opcode: Opcode) -> tuple[int, int]:
        if len(stack) < 2:
            raise RuntimeError(f"{opcode} requires at least two stack elements.")
        rhs = stack.pop()
        lhs = stack.pop()
        return (lhs, rhs)
