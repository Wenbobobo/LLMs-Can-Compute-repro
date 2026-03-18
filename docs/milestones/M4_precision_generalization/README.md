# M4 Precision Generalization

Goal: extend real-trace precision evidence beyond the current offset-heavy
suite and turn pass/fail anecdotes into a compact failure taxonomy.

This milestone starts from the current real-trace result:
- offset streams already reproduce the single-head float32 failure mode;
- horizon inflation reveals failures that native-horizon evaluation can hide;
- radix/block decomposition with base `64` remains strong on the current suite.

The open scientific question is whether that story survives on less templated,
more organic, and longer execution traces — and if not, exactly how it fails.
