# Value Family Matrix

`F10` stays planning-only. The table below does not activate any lane. It only
states which richer value families would count as a real semantic delta beyond
the current Origin-core floor.

| Value family | Representative examples | Relation to the current Origin-core line | Current status | Why it matters |
| --- | --- | --- | --- | --- |
| Current executor floor | append-only event ids, exact addresses, stack slots, return targets, and the current small exact executor state | already supported on the landed `H28/R34/R35/H29/R36/R37/R38/R39/H34` chain | `supported_here` | this is the current scientific floor and the baseline every richer family must preserve |
| Bounded scalar locals and flags | exact booleans, bounded integer-like counters, loop flags, and literal local cells that remain fully visible to the exact executor | smallest richer same-substrate family that could still stay close to the current line | `planning_only_current_wave` | this is the nearest family where a later semantic-boundary story could become scientifically sharper without immediately requiring a new substrate |
| Typed memory words and verifier-visible records | fixed-width cells, structured local records, multi-cell updates, and typed stack-frame payloads | richer than the current floor and likely upstream of any restricted semantic-boundary family | `planning_only_downstream` | this is where a future semantic-boundary family would start to need stronger comparator discipline than the current compiled-boundary line |
| Cross-module symbolic references and indirect tables | labels, import/export tables, indirect call targets, symbolic handles | no longer a tiny local extension of the current same-substrate line | `blocked_by_scope` | this kind of value family risks turning a narrow semantic-boundary discussion into a broader frontend story by wording alone |
| External effect and environment values | host I/O tokens, environment reads, nondeterministic effect channels | outside the current exact executor claim | `blocked_by_scope` | the repo has no current evidence that would make host-effect semantics a same-substrate follow-on rather than a scope change |
| Planner-mediated semantic values | planner-produced subgoals, latent task objects, semantic summaries handed to an executor | outside the current exact executor substrate entirely | `requires_new_substrate` | this is the first true hybrid-family step and cannot be smuggled in as a richer value vocabulary alone |

Working rule:

- only the first row is currently supported;
- the second row is why `F10` is the current admissible planning wave;
- later rows remain downstream of a future explicit packet and must not be
  inferred from current `H34` wording.
