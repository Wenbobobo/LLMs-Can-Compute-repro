# R43 Stop Conditions

Stop immediately if execution:

- breaks exact free-running trace match;
- breaks final-state match;
- needs heap, recursion, indirect calls, or a new substrate;
- requires a hidden mutable side channel outside the trace;
- changes the program family rather than testing bounded-memory execution.
