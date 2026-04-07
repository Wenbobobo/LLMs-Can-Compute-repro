# Scientific Goal Stack

This stack orders the origin-facing scientific ambitions from the currently
supported substrate outward. It is a planning aid only.

| Layer | Scientific target | Current state | Current canonical anchor |
| --- | --- | --- | --- |
| 1 | Append-only traces plus exact retrieval plus a small exact executor | `supported_here` | `H28/R34/R35/H29` |
| 2 | One tiny compiled slice plus one richer same-opcode control/call family on the same substrate | `supported_here` | `R37/R38/R39/H32/H34` |
| 3 | One bounded richer same-substrate value family beyond the current executor floor | `planning_only` | `F10`, now to be sharpened by `F13` |
| 4 | One contradiction-led same-substrate audit of runtime irrelevance or easy-part-only acceleration | `planning_only` | `F14` conditional readiness only |
| 5 | Restricted semantic-boundary family such as richer Wasm-like value semantics | `blocked_by_scope` | `F9` |
| 6 | Hybrid planner-plus-executor bridge | `requires_new_substrate` | `F11` |
| 7 | Arbitrary `C`, general LLM-computer rhetoric, or broad systems/platform superiority | `requires_new_substrate` | no active lane |

Reading rule:

- layers 1 and 2 are the current scientific floor;
- layers 3 and 4 are planning-only and inactive;
- layers 5 through 7 remain downstream of a later explicit packet.
