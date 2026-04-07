# Stop Conditions

Stop the bounded same-substrate reading immediately if any of the following
becomes necessary:

- typed multi-cell records rather than single-cell scalar slots;
- symbolic references, indirect targets, or cross-module handles as value
  payloads;
- host effects or environment reads;
- planner-mediated objects or latent summaries;
- a new opcode surface;
- a new substrate or hybrid interface.

If any stop condition fires:

- this family no longer belongs in a same-substrate bounded-scalar packet;
- route it back to blocked scope review or new-substrate review rather than
  widening by momentum.
