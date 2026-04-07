# R42 Stop Conditions

Stop immediately if any candidate path:

- diverges from the brute-force reference;
- needs hidden mutable state;
- needs heap-like addressing, alias-heavy pointers, or a new substrate;
- uses approximate retrieval instead of exact retrieval;
- changes the task meaning rather than stressing the retrieval contract.
