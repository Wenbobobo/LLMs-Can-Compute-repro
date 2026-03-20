# R10 D0 Same-Endpoint Cost Attribution

Explain where current same-endpoint time is actually spent without reopening a
broader systems lane.

The live implementation path is now narrowed by runtime budget: a full
component-wise exact attribution on the heaviest `R8` row exceeded `150s`
without finishing, so `R10` will attribute representative admitted rows rather
than naively profiling every admitted long row.

The bounded attribution is now closed on the current packet: the top `2`
harder `R8` families plus their matched admitted `R6` source rows show that
exact runtime remains overwhelmingly retrieval-dominated rather than harness-
or transition-dominated.
