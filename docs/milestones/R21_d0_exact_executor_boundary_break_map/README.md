# R21 D0 Exact Executor Boundary Break Map

Landed boundary-mapping lane after `R19` and `R20`. `R21` does not try to fix
the current exact runtime. It measured the current exact executor on a bounded
same-endpoint grid and recorded that the scan stayed exact on every executed
candidate rather than localizing a failure inside that bounded surface.
