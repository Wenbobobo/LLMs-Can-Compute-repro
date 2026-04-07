# Scientific Goal Stack

This stack orders the origin-facing scientific ambitions from the currently
supported substrate outward.

| Layer | Scientific target | Current state | Current canonical anchor |
| --- | --- | --- | --- |
| 1 | Append-only traces plus exact retrieval plus a small exact executor | `supported_here` | `H28/R34/R35/H29` |
| 2 | One tiny compiled slice plus one richer same-opcode control/call family on the same substrate | `supported_here` | `R37/R38/R39/H32/H34` |
| 3 | One bounded richer same-substrate value family beyond the prior executor floor | `supported_here` | `H35/R40/H36` |
| 4 | One contradiction-led same-substrate audit of runtime irrelevance or easy-part-only acceleration on the fixed `R40` row pair | `planning_only` | `F14`, saved `R41` design, and `H37` |
| 5 | Restricted semantic-boundary family such as richer Wasm-like value semantics | `blocked_by_scope` | `F9` |
| 6 | Hybrid planner-plus-executor bridge | `requires_new_substrate` | `F11` |
| 7 | Arbitrary `C`, general LLM-computer rhetoric, or broad systems/platform superiority | `requires_new_substrate` | no active lane |

Reading rule:

- layers 1 through 3 are the current supported narrow floor;
- layer 4 is the current top unresolved same-substrate risk, but still not an
  active lane;
- layers 5 through 7 remain blocked or require a new substrate.
