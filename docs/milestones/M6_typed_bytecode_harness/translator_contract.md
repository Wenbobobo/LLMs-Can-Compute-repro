# Translator Contract

## Bytecode IR

- `BytecodeInstruction`
  - `opcode`: one of the frozen v1 bytecode opcodes
  - `arg`: optional integer argument
  - `in_types`: tuple of stack types consumed
  - `out_types`: tuple of stack types produced
- `BytecodeProgram`
  - `instructions`: ordered tuple of `BytecodeInstruction`
  - `name`: program identifier

## Frozen v1 type system

- `i32`
  General integer value.
- `addr`
  Non-negative address value expected by static or indirect memory ops.
- `flag`
  Branch condition value used by `jz_zero`.

## Verifier contract

The verifier must return:
- `program_name`
- `passed`
- `first_error_pc`
- `error_class`
- `expected_stack`
- `actual_stack`
- `message`

The verifier checks:
- stack underflow by opcode;
- static address arguments are present and non-negative;
- `load_indirect` consumes `addr`;
- `store_indirect` consumes `i32, addr` in that order;
- `jz_zero` consumes `flag` or a value already proven to be `flag`;
- branch targets stay within program bounds.

## Lowering rules

- `const_i32(x)` -> `PUSH_CONST(x)`
- `const_addr(a)` -> `PUSH_CONST(a)`
- `dup` -> `DUP`
- `pop` -> `POP`
- `add_i32` -> `ADD`
- `sub_i32` -> `SUB`
- `eq_i32` -> `EQ`
- `load_static(a)` -> `LOAD(a)`
- `store_static(a)` -> `STORE(a)`
- `load_indirect` -> `LOAD_AT`
- `store_indirect` -> `STORE_AT`
- `jmp(pc)` -> `JMP(pc)`
- `jz_zero(pc)` -> `JZ(pc)`
- `halt` -> `HALT`

Lowering must not insert hidden bookkeeping instructions.
