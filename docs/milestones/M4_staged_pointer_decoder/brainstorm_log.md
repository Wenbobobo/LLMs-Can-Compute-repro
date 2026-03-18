# Brainstorm Log

- Started from broad structural masks to keep the comparison fair.
- Added `opcode_shape` as an intermediate regime after structural-only rollout
  stayed too weak to separate mask strength from learned source prediction.
- Added `alternating_memory_loop` so the staged result would not rest only on
  the earlier loop/ping-pong slice.
- Kept all three rollout regimes in the export to make the caveat visible.
