# Decision Log

- First frontend fixed to tiny typed bytecode.
- First harness compares bytecode reference semantics against lowered
  `exec_trace` semantics.
- First verifier reports the earliest stack-typing or opcode-argument error,
  not a bag of all errors.
