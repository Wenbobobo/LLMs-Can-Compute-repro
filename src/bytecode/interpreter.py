from __future__ import annotations

from exec_trace.dsl import ExecutionResult, ExecutionState, TraceEvent

from .ir import BytecodeInstruction, BytecodeOpcode, BytecodeProgram
from .lowering import LOWERING_MAP


class BytecodeInterpreter:
    def run(self, program: BytecodeProgram, max_steps: int = 10_000) -> ExecutionResult:
        state = ExecutionState()
        events: list[TraceEvent] = []

        while not state.halted:
            if state.steps >= max_steps:
                raise RuntimeError(f"Maximum step budget exceeded for program {program.name!r}.")
            if not (0 <= state.pc < len(program.instructions)):
                raise RuntimeError(f"Program counter out of range: {state.pc}")

            instruction = program.instructions[state.pc]
            event, state = self._step(state, instruction)
            events.append(event)

        return ExecutionResult(program=program, events=tuple(events), final_state=state)

    def _step(self, state: ExecutionState, instruction: BytecodeInstruction) -> tuple[TraceEvent, ExecutionState]:
        stack = list(state.stack)
        memory = dict(state.memory)
        call_stack = list(state.call_stack)
        popped: tuple[int, ...] = ()
        pushed: tuple[int, ...] = ()
        branch_taken: bool | None = None
        memory_read_address: int | None = None
        memory_read_value: int | None = None
        memory_write: tuple[int, int] | None = None
        next_pc = state.pc + 1
        halted = False

        match instruction.opcode:
            case BytecodeOpcode.CONST_I32 | BytecodeOpcode.CONST_ADDR:
                if instruction.arg is None:
                    raise RuntimeError(f"{instruction.opcode.value} requires an integer argument.")
                pushed = (instruction.arg,)
                stack.append(instruction.arg)
            case BytecodeOpcode.DUP:
                if not stack:
                    raise RuntimeError("dup requires at least one stack element.")
                pushed = (stack[-1],)
                stack.append(stack[-1])
            case BytecodeOpcode.POP:
                if not stack:
                    raise RuntimeError("pop requires at least one stack element.")
                popped = (stack.pop(),)
            case BytecodeOpcode.ADD_I32:
                lhs, rhs = self._pop_binary(stack, instruction.opcode.value)
                pushed = (lhs + rhs,)
                popped = (lhs, rhs)
                stack.append(lhs + rhs)
            case BytecodeOpcode.SUB_I32:
                lhs, rhs = self._pop_binary(stack, instruction.opcode.value)
                pushed = (lhs - rhs,)
                popped = (lhs, rhs)
                stack.append(lhs - rhs)
            case BytecodeOpcode.EQ_I32:
                lhs, rhs = self._pop_binary(stack, instruction.opcode.value)
                pushed = (int(lhs == rhs),)
                popped = (lhs, rhs)
                stack.append(int(lhs == rhs))
            case BytecodeOpcode.LOAD_STATIC:
                if instruction.arg is None:
                    raise RuntimeError("load_static requires an integer address.")
                if instruction.arg < 0:
                    raise RuntimeError("load_static address must be non-negative.")
                memory_read_address = instruction.arg
                memory_read_value = memory.get(instruction.arg, 0)
                pushed = (memory_read_value,)
                stack.append(memory_read_value)
            case BytecodeOpcode.STORE_STATIC:
                if instruction.arg is None:
                    raise RuntimeError("store_static requires an integer address.")
                if instruction.arg < 0:
                    raise RuntimeError("store_static address must be non-negative.")
                if not stack:
                    raise RuntimeError("store_static requires a value on the stack.")
                value = stack.pop()
                popped = (value,)
                memory[instruction.arg] = value
                memory_write = (instruction.arg, value)
            case BytecodeOpcode.LOAD_INDIRECT:
                if not stack:
                    raise RuntimeError("load_indirect requires an address on the stack.")
                address = stack.pop()
                if address < 0:
                    raise RuntimeError("load_indirect address must be non-negative.")
                popped = (address,)
                memory_read_address = address
                memory_read_value = memory.get(address, 0)
                pushed = (memory_read_value,)
                stack.append(memory_read_value)
            case BytecodeOpcode.STORE_INDIRECT:
                if len(stack) < 2:
                    raise RuntimeError("store_indirect requires a value and address on the stack.")
                address = stack.pop()
                value = stack.pop()
                if address < 0:
                    raise RuntimeError("store_indirect address must be non-negative.")
                popped = (value, address)
                memory[address] = value
                memory_write = (address, value)
            case BytecodeOpcode.JMP:
                if instruction.arg is None:
                    raise RuntimeError("jmp requires a target PC.")
                branch_taken = True
                next_pc = instruction.arg
            case BytecodeOpcode.JZ_ZERO:
                if instruction.arg is None:
                    raise RuntimeError("jz_zero requires a target PC.")
                if not stack:
                    raise RuntimeError("jz_zero requires a condition value on the stack.")
                condition = stack.pop()
                popped = (condition,)
                branch_taken = condition == 0
                next_pc = instruction.arg if branch_taken else state.pc + 1
            case BytecodeOpcode.CALL:
                if instruction.arg is None:
                    raise RuntimeError("call requires a target PC.")
                call_stack.append(state.pc + 1)
                branch_taken = True
                next_pc = instruction.arg
            case BytecodeOpcode.RET:
                if not call_stack:
                    raise RuntimeError("ret requires a pending return address.")
                branch_taken = True
                next_pc = call_stack.pop()
            case BytecodeOpcode.HALT:
                halted = True
                next_pc = state.pc
            case _:
                raise RuntimeError(f"Unsupported bytecode opcode: {instruction.opcode}")

        event = TraceEvent(
            step=state.steps,
            pc=state.pc,
            opcode=LOWERING_MAP[instruction.opcode],
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
            call_stack=tuple(call_stack),
            halted=halted,
            steps=state.steps + 1,
        )
        return event, next_state

    @staticmethod
    def _pop_binary(stack: list[int], opcode_name: str) -> tuple[int, int]:
        if len(stack) < 2:
            raise RuntimeError(f"{opcode_name} requires at least two stack elements.")
        rhs = stack.pop()
        lhs = stack.pop()
        return lhs, rhs
