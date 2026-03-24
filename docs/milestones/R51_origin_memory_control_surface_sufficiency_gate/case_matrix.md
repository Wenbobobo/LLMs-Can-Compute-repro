# R51 Case Matrix

| Family | Purpose | Required readout |
| --- | --- | --- |
| latest-write overwrite-after-gap | test repeated overwrite and delayed readback on append-only history | exact value, exact maximizer-row identity, first-fail location |
| stack-relative read under deeper control | test stack-slot retrieval under longer control structure | exact trace, exact final state, first-fail location |
| loop-carried state | test repeated state update and reuse over longer horizons | exact trace, exact final state, read-source identity |
| nested call/return | test control-state reconstruction without hidden call-stack side state | exact trace, return-target identity, first-fail artifact |
| bounded multi-step static-memory lowered row | test a richer lowered tiny-`C`-style memory/control row without arbitrary `C` scope | exact trace, exact final state, annotation-budget accounting |
