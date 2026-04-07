# R40 Status

- completed bounded-scalar same-substrate runtime gate after `H35`;
- validates one admitted explicit-flag loop row and one same-family longer
  boundary row on the current substrate;
- keeps the opcode surface fixed to the existing local arithmetic / static
  memory / branch subset;
- rejects the declared negative controls across verifier, memory-surface, or
  family-scope boundaries as intended;
- does not authorize threat-stress, restricted-Wasm, or hybrid widening by
  itself.
