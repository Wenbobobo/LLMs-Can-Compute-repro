# M4 Factorized Event Decoder

Goal: replace the opcode-conditioned rule-table decoder with a richer
history-aware event-value decoder that predicts direct event fields.

Current outcome:
- Teacher-forced label accuracy is clearly above chance.
- Free-running exact rollout is still weak.
- The main error surface is concentrated in `push_value_0` and `next_pc`.
