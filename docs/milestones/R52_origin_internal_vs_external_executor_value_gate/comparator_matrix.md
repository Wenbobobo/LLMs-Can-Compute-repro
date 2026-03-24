# R52 Comparator Matrix

| Comparator | Purpose | Required outputs |
| --- | --- | --- |
| internal accelerated exact executor | test the current internal fast path under the bounded post-`R51` rows | exactness, latency, retrieval-share decomposition |
| internal linear/reference executor | isolate whether acceleration changes only cost or also semantics | exactness parity, latency, first-fail difference if any |
| plain external interpreter/runtime | test whether the internal route has bounded value over simpler baselines | latency, debugging burden, exactness context |
