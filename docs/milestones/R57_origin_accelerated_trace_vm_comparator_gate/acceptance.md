# R57 Acceptance

- `R57` remains a bounded comparator gate, not a new runtime family;
- the comparator runs only on exact `R56` rows;
- exactness parity must remain visible wherever the comparator is meaningful;
- end-to-end latency and retrieval-share accounting must both be reported;
- a negative value result is first-class evidence; and
- `H52` must read `R57` explicitly rather than infer value by momentum.
