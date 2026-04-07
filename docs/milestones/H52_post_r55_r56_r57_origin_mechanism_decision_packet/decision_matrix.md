# H52 Decision Matrix

| Outcome | Meaning | Downstream effect |
| --- | --- | --- |
| `freeze_origin_mechanism_supported_with_fastpath_value` | retrieval equivalence, trace semantics, and bounded comparator value all survive on the narrowed lane | freeze the mechanism chain positively and require a later explicit packet before any broader route |
| `freeze_origin_mechanism_supported_without_fastpath_value` | retrieval equivalence and trace semantics survive, but bounded fast-path value does not | close the lane as mechanism support only without value expansion |
| `stop_as_partial_mechanism_only` | the narrowed mechanism chain fails before full positive support is established | stop broadening and preserve only the surviving partial evidence explicitly |
