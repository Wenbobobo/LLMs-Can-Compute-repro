# R51 Stop Conditions

Stop and report a negative or mixed result if any are true:

1. full-trace or final-state exactness breaks on a mandatory row;
2. maximizer-row identity breaks while the retrieved value still looks correct;
3. hidden mutable side state becomes necessary to preserve exactness;
4. the declared bounded surface must widen materially to keep the lane alive; or
5. annotation/query/head budget explodes in a way that destroys the meaning of
   the runtime claim.
