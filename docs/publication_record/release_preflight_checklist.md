# Release Preflight Checklist

- confirm the current archive-facing control stack is
  `H65/P77/P78/P79/P80`
- confirm the `P72` hygiene-only archive-polish and explicit-stop handoff
  sidecar remains aligned below that current stack
- confirm the `P69/P70/P71` hygiene-only cleanup sidecars remain aligned below
  `P72`
- preserve `P74/P75/P76` as the immediate publication lineage for the live
  `wip/p75-post-p74-published-successor-freeze` branch
- preserve `P66/P67/P68` as the prior published successor stack
- confirm the preserved `H64/P56/P57/P58/P59/F38` foundation remains aligned
  underneath the current live stack
- keep `H58` as the value-negative closeout
- keep `H43` as the preserved paper-grade endpoint
- keep `P72/P69/P70/P71` framed as hygiene/control sidecars rather than new
  runtime or evidence-bearing packets
- explicit stop or no further action
- keep dirty root `main` outside any integration path
